# prashobhpaul.com — Makeover (v2 · content-driven)

A targeted makeover of the existing single-page site, with the four new sections (**Deep Dives**, **Systems**, **Labs**, **Notes**) wired to a `contents/` folder so anyone can add a file and have it appear — without touching the code.

## TL;DR — adding content

```
contents/
├── deep-dives/     ← .md / .txt / .docx  (long-form pieces)
├── notes/          ← .txt / .md          (quick observations)
├── systems/        ← .jpg / .png         (architecture diagrams + optional .json sidecar)
└── labs/           ← .md / .txt / .docx  (experiment notes)
```

Drop a file in the right folder. Run **one command**. Push.

```bash
python3 build_content.py
git add . && git commit -m "Add new deep dive" && git push
```

That's it. The site reads `contents/manifest.json` at runtime and re-renders the four sections. Optionally, the included GitHub Action runs `build_content.py` for you on every push, so the local step is skipped entirely.

## What changed from v1

### Hero copy

The hero summary is now memorable, not generic:

> *"Most AI prototypes look impressive. Very few survive governance, scale, and real operational friction. I design and ship the ones that do."*

### Section renamed

**Writing** → **Deep Dives**. Anchor changed from `#writing` to `#deep-dives`. Nav, CSS, and chat KB references all updated to match.

### Four content-driven sections

| Section | Folder | Accepts | What gets shown |
|---|---|---|---|
| **Deep Dives** | `contents/deep-dives/` | `.md`, `.txt`, `.docx` | Featured piece (large) + supporting cards. Clicking opens the full piece in an inline reader overlay |
| **Systems** | `contents/systems/` | `.jpg`, `.png` (+ optional `.json` sidecar) | Architecture cards with image backgrounds. Clicking opens a fullscreen lightbox |
| **Labs** | `contents/labs/` | `.md`, `.txt`, `.docx` | Lab cards with domain · status · tech chips |
| **Field Notes** | `contents/notes/` | `.txt`, `.md` | Date-stamped running notes with category tags |

## File conventions

### Recommended filename pattern

```
YYYY-MM-DD_short-slug-here.ext
```

Example: `2026-05-12_9-gate-hitl-topology.md` → slug `9-gate-hitl-topology`, date `2026-05-12`.

If you don't use a date prefix, the file's modification time is used as a fallback.

### Front-matter (optional but recommended)

**For `.md` files** — standard YAML-ish fenced front-matter:

```markdown
---
title: Designing a *9-gate HITL topology* for governed agentic SDLC
date: 2026-05-12
kicker: Featured Deep Dive
featured: true
readingTime: 14 min
tags: [governance, agentic-sdlc, hitl]
hook: When agents write, review, and test code on your behalf, governance can't be a checklist at the end...
---

# The shape of governed agentic SDLC

Most agentic SDLC stacks I see...
```

**For `.txt` files** — bare key-value lines at the top (no `---` required):

```
title: When the *subagent pattern* outperforms the orchestrator
date: 2026-05-12
category: Agentic Patterns

Three engagements in, the pattern is clear: file-based handshake contracts...
```

**For `.docx` files** — use real Word heading styles. The first **Heading 1** becomes the title; the first non-empty paragraph becomes the hook. No front-matter needed (Word doesn't have a clean way to express it).

### Field meanings

| Field | Used in | Default |
|---|---|---|
| `title` | all | filename, prettified |
| `date` | all | filename prefix or file mtime |
| `hook` | all | first paragraph |
| `readingTime` | docs | auto-computed at ~220 wpm |
| `kicker` | deep dives | "Deep Dive" |
| `featured: true` | deep dives | first item is featured |
| `tags` | all | `[]` |
| `domain` | labs | "Lab" |
| `status` | labs | "Live" (use `archived` for grayed-out status) |
| `tech` | labs | `[]` (renders as chips) |
| `category` | notes | "" |

### Italic-gold emphasis in titles

A single `*word or phrase*` inside any title renders as italic gold — matches the existing visual rhythm of the site. Example: `*9-gate HITL topology*` shows up as italic gold inside the otherwise navy serif title. Keep emphasised phrases under 40 chars to stay clean visually.

### Systems sidecar metadata

For each image in `contents/systems/`, drop a `<same-name>.json` next to it:

```json
{
  "title": "Layered *governance stack*",
  "tag": "Governed SDLC",
  "description": "Four horizontal layers separate policy from gates from topology from artifacts — so each can evolve without breaking the others.",
  "meta": "4 layers · 9 gates",
  "stage": "Production"
}
```

Without a sidecar, the card title is derived from the filename and the description is empty.

## Files in this bundle

| File | What it does |
|---|---|
| `build.py` | **One-time** site makeover. Reads your existing `index.html` (the source), writes `index_new.html` (the made-over version). Run once. |
| `build_content.py` | **Every time** you add content. Scans `contents/`, parses docs/images, writes rendered HTML and `contents/manifest.json`. |
| `index_new.html` | Pre-built reference site (the result of running `build.py` against a known-good source). |
| `contents/` | Seed content — four deep dives, five notes, three systems, four labs. Edit or replace freely. |
| `.github/workflows/build-content.yml` | Optional GitHub Action — runs `build_content.py` automatically on every push so you don't have to run it locally. |
| `README.md` | This file. |

## First-time setup

```bash
# 1. One-time Python deps for the content builder
pip install python-docx markdown

# 2. Apply the makeover to your existing index.html
python3 build.py index.html index_new.html

# 3. Build the manifest from contents/
python3 build_content.py

# 4. Test locally
python3 -m http.server 8000
# → open http://localhost:8000/index_new.html

# 5. When you're happy:
mv index.html index_old_backup.html
mv index_new.html index.html
git add . && git commit -m "Site makeover v2 (content-driven)"
git push
```

## Ongoing workflow — adding a deep dive

1. Drop `contents/deep-dives/2026-05-20_new-piece.md` (with front-matter)
2. `python3 build_content.py`
3. `git add . && git commit -m "Add: new piece on..." && git push`

If you've enabled the GitHub Action (see `.github/workflows/build-content.yml`), you can skip step 2 — the action runs `build_content.py` automatically and commits the regenerated `contents/manifest.json` back to the branch.

## What's never on the live site

Despite all the new sections, **no client names**, no project codenames, no internal program names. Positioning is capability-first throughout (*"Agentic AI for SDLC lifecycles with Kiro"*, *"Agentic AI for STLC lifecycles with Microsoft Agent Framework on .NET"*). Safe for procurement to read, specific enough to be credible.

## Behaviour when contents/ is empty or missing

Each section shows a polite empty state with hints:

> *"No deep dives published yet. Drop a markdown, txt, or docx file into contents/deep-dives/ and run build_content.py."*

If `contents/manifest.json` is missing entirely, all four sections show their respective empty states. The site never breaks — it just degrades gracefully.

## Re-running the makeover

`build.py` is idempotent on a clean source — it asserts every marker it expects to find. If you've already promoted `index_new.html` to `index.html` and try to re-run it on the new file, the asserts will fail loudly. That's by design.

If you want to apply further makeover changes later, edit `build.py` (the source of truth for site-level changes) and re-run against your backed-up source.
