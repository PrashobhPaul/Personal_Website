#!/usr/bin/env python3
"""
build_content.py
================
Scan contents/ subfolders, render each file to HTML, and emit
contents/manifest.json so the site can render the Deep Dives,
Systems, Labs, and Notes sections without code changes.

Folder layout expected:

  contents/
    deep-dives/      *.md, *.txt, *.docx           (long-form pieces)
    notes/           *.txt, *.md                   (quick observations)
    systems/         *.jpg, *.png  (+ optional .json sidecar)
    labs/            *.md, *.txt, *.docx           (experiment notes)

File-naming convention (recommended, optional):
    YYYY-MM-DD_slug-with-dashes.ext
e.g.  2026-05-12_9-gate-hitl-topology.md

Title is taken from (in order):
  1) the first heading (#) inside markdown
  2) the first non-empty line of a txt
  3) the docx's first heading-styled paragraph, or first paragraph
  4) the filename slug, prettified

Hook (the short preview shown on the card) is taken from:
  1) a "hook:" front-matter line, OR
  2) the first paragraph after the title

Optional YAML-ish front-matter at the top of any file:

  ---
  title: Designing a 9-gate HITL topology
  date: 2026-05-12
  kicker: Featured Deep Dive
  hook: When agents write, review, and test code on your behalf...
  readingTime: 14 min
  tags: [governance, agentic-sdlc, hitl]
  featured: true
  ---
  (then the body)

For systems/, you can drop a .json sidecar next to the image:

  governance-stack.jpg
  governance-stack.json   ->  { "title": "...", "tag": "...",
                                "description": "...", "meta": "4 LAYERS · 9 GATES",
                                "stage": "Production" }

Run:
    pip install python-docx markdown          # one time
    python3 build_content.py                  # in the site root

Generates:
    contents/manifest.json
    contents/deep-dives/_rendered/<slug>.html
    contents/labs/_rendered/<slug>.html
    contents/notes/_rendered/<slug>.html

Idempotent. Safe to run on every git push (or wire to a GitHub Action).
"""
from __future__ import annotations
import json, re, sys, html, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CONTENTS = ROOT / "contents"

# ───────────────────────── helpers ─────────────────────────

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Very small YAML-ish parser — supports key: value and key: [a, b, c]."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            meta[k] = [x.strip().strip('"\'') for x in v[1:-1].split(",") if x.strip()]
        elif v.lower() in ("true", "false"):
            meta[k] = v.lower() == "true"
        else:
            meta[k] = v.strip('"\'')
    return meta, text[m.end():]


SLUG_PREFIX_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})[_-](.+)$")

def derive_slug_and_date(stem: str) -> tuple[str, str | None]:
    m = SLUG_PREFIX_DATE_RE.match(stem)
    if m:
        return m.group(2).lower(), m.group(1)
    return stem.lower(), None


def prettify_slug(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def first_paragraph(body: str) -> str:
    body = body.strip()
    if not body:
        return ""
    blocks = re.split(r"\n\s*\n", body, maxsplit=1)
    return re.sub(r"\s+", " ", blocks[0]).strip()


def reading_time(body: str) -> str:
    words = len(re.findall(r"\w+", body))
    minutes = max(1, round(words / 220))
    return f"{minutes} min"


# ───────────────────────── format readers ─────────────────────────

def read_md(path: pathlib.Path) -> tuple[dict, str, str]:
    """Return (meta, body_html, hook)."""
    try:
        import markdown
    except ImportError:
        print("ERROR: pip install markdown", file=sys.stderr); sys.exit(1)
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)

    # Pull H1 from body if no title in front-matter
    if "title" not in meta:
        h1 = re.match(r"^#\s+(.+)$", body.strip(), re.M)
        if h1:
            meta["title"] = h1.group(1).strip()
            body = body.replace(h1.group(0), "", 1).lstrip()

    hook = meta.get("hook") or first_paragraph(re.sub(r"^#+\s.*$", "", body, flags=re.M))
    body_html = markdown.markdown(body, extensions=["extra", "sane_lists"])
    return meta, body_html, hook


def parse_bare_frontmatter(text: str) -> tuple[dict, str]:
    """Like parse_frontmatter, but also accepts a leading key-value block
    that isn't wrapped in --- delimiters. The block ends at the first blank
    line. Used for .txt notes where '---' fences look heavy-handed."""
    meta, rest = parse_frontmatter(text)
    if meta:
        return meta, rest
    # Try bare style: first lines look like `key: value` until a blank line
    lines = text.splitlines()
    consumed = 0
    bare = {}
    for line in lines:
        if not line.strip():
            break
        m = re.match(r"^([A-Za-z][\w-]*)\s*:\s*(.+)$", line)
        if not m:
            break
        k, v = m.group(1).strip(), m.group(2).strip()
        if v.startswith("[") and v.endswith("]"):
            bare[k] = [x.strip().strip('"\'') for x in v[1:-1].split(",") if x.strip()]
        elif v.lower() in ("true", "false"):
            bare[k] = v.lower() == "true"
        else:
            bare[k] = v.strip('"\'')
        consumed += 1
    if bare and consumed >= 2:
        # require at least 2 key-value lines to be confident it's frontmatter
        rest_text = "\n".join(lines[consumed:]).lstrip("\n")
        return bare, rest_text
    return {}, text


def read_txt(path: pathlib.Path) -> tuple[dict, str, str]:
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_bare_frontmatter(raw)

    if "title" not in meta:
        # First non-empty line
        for line in body.splitlines():
            if line.strip():
                meta["title"] = line.strip().lstrip("#").strip()
                body = body.replace(line, "", 1).lstrip()
                break

    hook = meta.get("hook") or first_paragraph(body)

    # Convert plain text to HTML paragraphs (preserve blank-line paragraph breaks)
    paras = re.split(r"\n\s*\n", body.strip())
    body_html = "\n".join(f"<p>{html.escape(p).replace(chr(10), '<br>')}</p>" for p in paras if p.strip())
    return meta, body_html, hook


def read_docx(path: pathlib.Path) -> tuple[dict, str, str]:
    try:
        import docx
    except ImportError:
        print("ERROR: pip install python-docx", file=sys.stderr); sys.exit(1)
    d = docx.Document(str(path))

    paras = []
    title = None
    for p in d.paragraphs:
        text = p.text.strip()
        if not text:
            paras.append(("blank", ""))
            continue
        style = (p.style.name or "").lower()
        if "heading 1" in style and title is None:
            title = text
            continue
        if "heading" in style:
            level = "h2" if "1" in style or "2" in style else "h3"
            paras.append((level, text))
        else:
            paras.append(("p", text))

    if title is None:
        for kind, text in paras:
            if kind == "p":
                title = text
                paras = [(k, t) for (k, t) in paras if not (k == "p" and t == text)] if False else paras[1:]
                break

    body_parts = []
    for kind, text in paras:
        if kind == "blank":
            continue
        if kind == "p":
            body_parts.append(f"<p>{html.escape(text)}</p>")
        else:
            body_parts.append(f"<{kind}>{html.escape(text)}</{kind}>")
    body_html = "\n".join(body_parts)

    # Hook = first paragraph after title
    hook = ""
    for kind, text in paras:
        if kind == "p":
            hook = text
            break

    meta = {"title": title or prettify_slug(path.stem)}
    return meta, body_html, hook


# ───────────────────────── per-section walkers ─────────────────────────

DOC_EXTS = (".md", ".txt", ".docx")
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")


def render_doc(path: pathlib.Path):
    """Dispatch to the right reader based on extension."""
    ext = path.suffix.lower()
    if ext == ".md":   return read_md(path)
    if ext == ".txt":  return read_txt(path)
    if ext == ".docx": return read_docx(path)
    raise ValueError(f"unsupported: {path}")


def process_doc_section(folder: pathlib.Path, section_key: str) -> list[dict]:
    if not folder.exists():
        return []
    rendered_dir = folder / "_rendered"
    rendered_dir.mkdir(exist_ok=True)

    entries = []
    for path in sorted(folder.iterdir()):
        if path.name.startswith(".") or path.suffix.lower() not in DOC_EXTS:
            continue
        if path.parent.name == "_rendered":
            continue

        slug_part, date_part = derive_slug_and_date(path.stem)
        try:
            meta, body_html, hook = render_doc(path)
        except Exception as e:
            print(f"  ! skip {path.name}: {e}")
            continue

        slug = meta.get("slug", slug_part).lower().strip()
        date = meta.get("date") or date_part or datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()
        title = meta.get("title") or prettify_slug(slug)
        rt = meta.get("readingTime") or reading_time(re.sub(r"<[^>]+>", " ", body_html))

        # Write rendered HTML next to source
        html_path = rendered_dir / f"{slug}.html"
        html_path.write_text(body_html, encoding="utf-8")

        entry = {
            "slug": slug,
            "title": title,
            "date": date,
            "hook": hook[:340] + ("…" if len(hook) > 340 else ""),
            "readingTime": rt,
            "html": str(html_path.relative_to(ROOT)).replace("\\", "/"),
            "source": str(path.relative_to(ROOT)).replace("\\", "/"),
        }

        # Optional fields that map to specific section card layouts
        for k in ("kicker", "tags", "featured", "domain", "category", "status", "tech"):
            if k in meta:
                entry[k] = meta[k]

        entries.append(entry)

    # Sort newest first
    entries.sort(key=lambda e: e.get("date", ""), reverse=True)
    print(f"  {section_key}: {len(entries)} entries")
    return entries


def process_systems(folder: pathlib.Path) -> list[dict]:
    if not folder.exists():
        return []
    entries = []
    for path in sorted(folder.iterdir()):
        if path.name.startswith(".") or path.suffix.lower() not in IMG_EXTS:
            continue
        slug_part, _ = derive_slug_and_date(path.stem)
        slug = slug_part.lower()

        # Optional sidecar
        sidecar = path.with_suffix(".json")
        meta = {}
        if sidecar.exists():
            try:
                meta = json.loads(sidecar.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"  ! bad sidecar {sidecar.name}: {e}")

        entries.append({
            "slug": slug,
            "title": meta.get("title", prettify_slug(slug)),
            "tag": meta.get("tag", "Architecture"),
            "description": meta.get("description", ""),
            "meta": meta.get("meta", ""),
            "stage": meta.get("stage", "Reference"),
            "image": str(path.relative_to(ROOT)).replace("\\", "/"),
        })
    print(f"  systems: {len(entries)} entries")
    return entries


# ───────────────────────── main ─────────────────────────

def main():
    if not CONTENTS.exists():
        print(f"ERROR: {CONTENTS} not found. Create it and add subfolders: deep-dives, notes, systems, labs",
              file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {CONTENTS}/")
    manifest = {
        "generatedAt": datetime.datetime.now().isoformat(timespec="seconds"),
        "deepDives": process_doc_section(CONTENTS / "deep-dives", "deepDives"),
        "labs":      process_doc_section(CONTENTS / "labs",       "labs"),
        "notes":     process_doc_section(CONTENTS / "notes",      "notes"),
        "systems":   process_systems(CONTENTS / "systems"),
    }

    out = CONTENTS / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    total = sum(len(v) for k, v in manifest.items() if isinstance(v, list))
    print(f"\n✓ wrote {out.relative_to(ROOT)} — {total} entries total")
    print(f"  commit + push (or run a GitHub Action) to update the site")


if __name__ == "__main__":
    main()
