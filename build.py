#!/usr/bin/env python3
"""
Makeover build script for prashobhpaul.com

Applies surgical edits to the existing single-page profile site:
  - reframes hero copy to a governance/agentic positioning
  - adds anonymised "Currently Shipping" instrument strip
  - inserts new Writing, Systems, Labs, and Field Notes sections
  - rewrites About text and current Qualizeal role bullets
  - adds new Phoenix KB intents covering the new positioning
  - never names clients — positioning is capability-first

Run:
    python3 build.py [source_html] [output_html]

Defaults:
    source = ./index.html
    output = ./index_new.html
"""
import pathlib, sys

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
DST = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "index_new.html")

if not SRC.exists():
    print(f"ERROR: source not found: {SRC}", file=sys.stderr)
    print(f"Usage: python3 build.py [source.html] [output.html]", file=sys.stderr)
    sys.exit(1)

s = SRC.read_text(encoding="utf-8")

# ─────────────────────────────────────────────────────────────────────────
# 1. NAV LINKS — add Writing, Systems, Labs, Notes (between existing items)
# ─────────────────────────────────────────────────────────────────────────
old_nav = """  <ul class="nav-links" id="navLinks">
    <li><a href="#about"      onclick="closeNav()">About</a></li>
    <li><a href="#experience" onclick="closeNav()">Experience</a></li>
    <li><a href="#skills"     onclick="closeNav()">Skills</a></li>
    <li><a href="#education"  onclick="closeNav()">Education</a></li>
    <li><a href="#contact"    onclick="closeNav()">Contact</a></li>
  </ul>"""

new_nav = """  <ul class="nav-links" id="navLinks">
    <li><a href="#about"      onclick="closeNav()">About</a></li>
    <li><a href="#deep-dives" onclick="closeNav()">Deep Dives</a></li>
    <li><a href="#experience" onclick="closeNav()">Experience</a></li>
    <li><a href="#systems"    onclick="closeNav()">Systems</a></li>
    <li><a href="#labs"       onclick="closeNav()">Labs</a></li>
    <li><a href="#notes"      onclick="closeNav()">Notes</a></li>
    <li><a href="#contact"    onclick="closeNav()">Contact</a></li>
  </ul>"""

assert old_nav in s, "nav block not found"
s = s.replace(old_nav, new_nav)

# ─────────────────────────────────────────────────────────────────────────
# 2. NEW CSS — inserted before the closing </style>. Reuses existing tokens.
# ─────────────────────────────────────────────────────────────────────────
new_css = r"""
/* ══════════════════════════════
   MAKEOVER ADDITIONS — uses existing tokens
══════════════════════════════ */

/* SHIPPING STRIP — instrument bar between hero and about */
.shipping {
  background: var(--navy);
  border-top: 1px solid rgba(201,168,76,0.18);
  border-bottom: 1px solid rgba(201,168,76,0.18);
  padding: 1.6rem 0;
  position: relative;
  overflow: hidden;
}
.shipping::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.ship-grid {
  max-width: 1160px;
  margin: 0 auto;
  padding: 0 3.5rem;
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 2.5rem;
  align-items: center;
}
.ship-label {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.66rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 600;
}
.ship-label::before {
  content: '';
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #4ade80;
  box-shadow: 0 0 8px #4ade80;
  animation: ship-pulse 2.2s ease-in-out infinite;
}
@keyframes ship-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.85); }
}
.ship-rows {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}
.ship-row {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding-left: 1rem;
  border-left: 1px solid rgba(201,168,76,0.18);
}
.ship-k {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.62rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-muted);
}
.ship-v {
  font-size: 0.86rem;
  color: rgba(255,255,255,0.86);
  line-height: 1.4;
}
.ship-v em {
  font-style: normal;
  color: var(--gold-light);
  font-weight: 600;
}

/* WRITING — featured piece w/ inline diagram */
#deep-dives { background: var(--cream); }
.writing-grid {
  margin-top: 3rem;
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.4rem;
}
.featured-piece {
  display: grid;
  grid-template-columns: 0.95fr 1.1fr;
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.25s, transform 0.25s;
}
.featured-piece:hover { border-color: var(--gold); transform: translateY(-3px); }
.fp-visual {
  position: relative;
  min-height: 320px;
  background:
    radial-gradient(circle at 30% 40%, rgba(201,168,76,0.08), transparent 60%),
    var(--navy);
  border-right: 1px solid var(--border);
}
.fp-visual svg { position: absolute; inset: 0; width: 100%; height: 100%; }
.fp-body {
  padding: 2.4rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  justify-content: center;
}
.fp-meta {
  display: flex;
  gap: 0.9rem;
  flex-wrap: wrap;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.66rem;
  color: var(--text-muted);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.fp-meta .gold { color: var(--gold); font-weight: 600; }
.fp-title {
  font-family: 'DM Serif Display', serif;
  font-size: clamp(1.5rem, 2.5vw, 1.95rem);
  line-height: 1.15;
  color: var(--navy);
  margin: 0;
}
.fp-title em { font-style: italic; color: var(--gold); }
.fp-hook { color: var(--text-mid); margin: 0; font-size: 0.97rem; line-height: 1.7; }
.fp-link {
  align-self: flex-start;
  margin-top: 0.6rem;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 600;
  border-bottom: 1px solid rgba(201,168,76,0.3);
  padding-bottom: 4px;
  transition: border-color 0.22s;
}
.featured-piece:hover .fp-link { border-color: var(--gold); }
.fp-link::after { content: ' →'; }

.writing-list {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1.2rem;
  margin-top: 1.4rem;
}
.wl-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1.6rem;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.22s, transform 0.22s;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}
.wl-card:hover { border-color: var(--gold); transform: translateY(-3px); }
.wl-tag {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.62rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 600;
}
.wl-title {
  font-family: 'DM Serif Display', serif;
  font-size: 1.1rem;
  line-height: 1.3;
  color: var(--navy);
  margin: 0;
}
.wl-title em { font-style: italic; color: var(--gold); }
.wl-hook {
  font-size: 0.84rem;
  color: var(--text-mid);
  line-height: 1.6;
  margin: 0;
}
.wl-foot {
  margin-top: auto;
  padding-top: 0.7rem;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.66rem;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  text-transform: uppercase;
}

/* SYSTEMS — architecture reference cards */
#systems { background: var(--navy); }
#systems .section-title { color: var(--white); }
.sys-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.4rem;
  margin-top: 3rem;
}
.sys-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(201,168,76,0.16);
  border-radius: 4px;
  overflow: hidden;
  transition: border-color 0.22s, transform 0.22s;
  display: flex;
  flex-direction: column;
}
.sys-card:hover { border-color: rgba(201,168,76,0.45); transform: translateY(-3px); }
.sys-visual {
  height: 180px;
  position: relative;
  background:
    linear-gradient(180deg, rgba(0,0,0,0.2), transparent),
    rgba(255,255,255,0.02);
  border-bottom: 1px solid rgba(201,168,76,0.14);
}
.sys-visual svg { position: absolute; inset: 0; width: 100%; height: 100%; }
.sys-body {
  padding: 1.4rem 1.6rem 1.6rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  flex: 1;
}
.sys-tag {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.62rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 600;
}
.sys-title {
  font-family: 'DM Serif Display', serif;
  font-size: 1.12rem;
  line-height: 1.3;
  color: var(--white);
  margin: 0;
}
.sys-title em { font-style: italic; color: var(--gold-light); }
.sys-desc {
  font-size: 0.82rem;
  color: rgba(255,255,255,0.62);
  line-height: 1.65;
  margin: 0;
  flex: 1;
}
.sys-foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.62rem;
  color: var(--text-muted);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-top: 0.6rem;
  padding-top: 0.8rem;
  border-top: 1px solid rgba(201,168,76,0.1);
}
.sys-foot .stage { color: var(--gold); }

/* APPLIED LABS — practitioner research */
#labs { background: var(--cream); }
.lab-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.4rem;
  margin-top: 3rem;
}
.lab-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1.8rem;
  text-decoration: none;
  color: inherit;
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.7rem;
  position: relative;
  transition: border-color 0.22s, transform 0.22s;
}
.lab-card:hover { border-color: var(--gold); transform: translateY(-3px); }
.lab-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}
.lab-domain {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.62rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 600;
}
.lab-status {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.6rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #4ade80;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.lab-status::before {
  content: '';
  width: 5px; height: 5px;
  border-radius: 50%;
  background: #4ade80;
}
.lab-status.archived { color: var(--text-muted); }
.lab-status.archived::before { background: var(--text-muted); }
.lab-title {
  font-family: 'DM Serif Display', serif;
  font-size: 1.25rem;
  line-height: 1.25;
  color: var(--navy);
  margin: 0;
}
.lab-title em { font-style: italic; color: var(--gold); }
.lab-hook {
  font-size: 0.9rem;
  color: var(--text-mid);
  line-height: 1.7;
  margin: 0;
}
.lab-tech {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  margin-top: 0.6rem;
}
.lab-tech span {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.66rem;
  color: var(--text-mid);
  background: var(--cream);
  border: 1px solid var(--border);
  padding: 0.22rem 0.6rem;
  border-radius: 2px;
}

/* FIELD NOTES */
#notes { background: var(--white); }
.notes-list {
  display: flex;
  flex-direction: column;
  margin-top: 3rem;
}
.note-row {
  display: grid;
  grid-template-columns: 130px 1fr auto;
  gap: 2rem;
  padding: 1.4rem 0;
  border-top: 1px solid var(--border);
  align-items: baseline;
  transition: padding 0.22s;
}
.note-row:last-child { border-bottom: 1px solid var(--border); }
.note-row:hover { padding-left: 0.6rem; }
.note-date {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  color: var(--text-muted);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.note-content { min-width: 0; }
.note-title {
  font-family: 'DM Serif Display', serif;
  font-size: 1.05rem;
  color: var(--navy);
  margin: 0 0 0.35rem;
  line-height: 1.35;
}
.note-title em { font-style: italic; color: var(--gold); }
.note-excerpt {
  font-size: 0.86rem;
  color: var(--text-mid);
  line-height: 1.65;
  margin: 0;
}
.note-cat {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.62rem;
  color: var(--gold);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  font-weight: 600;
}

/* SECTION-LABEL DARK VARIANT — for navy-bg sections */
.section-label-light {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 0.8rem;
}
.section-label-light::before {
  content: '';
  display: block;
  width: 22px; height: 1px;
  background: var(--gold);
  flex-shrink: 0;
}
.section-sub-light {
  font-size: 0.95rem;
  color: rgba(255,255,255,0.6);
  line-height: 1.75;
  max-width: 580px;
}

/* RESPONSIVE — for the new sections */
@media (max-width: 1100px) {
  .ship-grid { padding: 0 2.5rem; grid-template-columns: 1fr; gap: 1.2rem; }
  .ship-rows { grid-template-columns: repeat(2, 1fr); }
  .featured-piece { grid-template-columns: 1fr; }
  .fp-visual { min-height: 220px; border-right: 0; border-bottom: 1px solid var(--border); }
  .writing-list { grid-template-columns: 1fr 1fr; }
  .sys-grid { grid-template-columns: 1fr 1fr; }
  .lab-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 900px) {
  .ship-grid { padding: 0 1.5rem; }
  .ship-rows { grid-template-columns: 1fr 1fr; gap: 1rem; }
  .writing-list { grid-template-columns: 1fr; }
  .sys-grid { grid-template-columns: 1fr; }
  .lab-grid { grid-template-columns: 1fr; }
  .note-row { grid-template-columns: 100px 1fr; gap: 1rem; }
  .note-cat { display: none; }
  .fp-body { padding: 1.8rem; }
}
@media (max-width: 600px) {
  .ship-grid { padding: 0 1rem; }
  .ship-rows { grid-template-columns: 1fr; }
  .note-row { grid-template-columns: 1fr; gap: 0.3rem; }
  .note-date { font-size: 0.66rem; }
}

/* CONTENT LOADER — empty states, overlay, lightbox */
.content-empty {
  grid-column: 1 / -1;
  padding: 3rem 1.5rem;
  text-align: center;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.86rem;
  color: var(--text-muted);
  background: var(--white);
  border: 1px dashed var(--border);
  border-radius: 4px;
  line-height: 1.7;
}
.content-empty-dark {
  grid-column: 1 / -1;
  padding: 3rem 1.5rem;
  text-align: center;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.86rem;
  color: rgba(255,255,255,0.45);
  background: rgba(255,255,255,0.03);
  border: 1px dashed rgba(201,168,76,0.18);
  border-radius: 4px;
  line-height: 1.7;
}

/* OVERLAY for reading a deep dive / lab inline */
#overlay {
  position: fixed;
  inset: 0;
  background: rgba(11,22,40,0.86);
  backdrop-filter: blur(8px);
  z-index: 9990;
  display: none;
  align-items: flex-start;
  justify-content: center;
  padding: 4rem 2rem 2rem;
  overflow-y: auto;
}
#overlay.open { display: flex; }
.ov-card {
  background: var(--white);
  max-width: 780px;
  width: 100%;
  border-radius: 6px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.4);
  position: relative;
  overflow: hidden;
  animation: ov-in 0.32s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes ov-in {
  from { opacity: 0; transform: translateY(20px) scale(0.96); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
.ov-close {
  position: absolute;
  top: 18px; right: 18px;
  width: 32px; height: 32px;
  border: 1px solid var(--border);
  background: var(--white);
  color: var(--text-mid);
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex; align-items: center; justify-content: center;
  z-index: 2;
  transition: border-color 0.18s, color 0.18s;
}
.ov-close:hover { border-color: var(--gold); color: var(--navy); }
.ov-meta {
  padding: 2.4rem 2.6rem 0.8rem;
  display: flex;
  gap: 0.9rem;
  flex-wrap: wrap;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.66rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
}
.ov-meta .gold { color: var(--gold); font-weight: 600; }
.ov-title {
  padding: 0 2.6rem 1rem;
  font-family: 'DM Serif Display', serif;
  font-size: clamp(1.6rem, 2.6vw, 2.1rem);
  line-height: 1.18;
  color: var(--navy);
  margin: 0;
}
.ov-title em { font-style: italic; color: var(--gold); }
.ov-body {
  padding: 0.4rem 2.6rem 2.6rem;
  font-size: 0.96rem;
  line-height: 1.85;
  color: var(--text-mid);
  border-top: 1px solid var(--border);
  margin-top: 0.6rem;
  padding-top: 1.4rem;
}
.ov-body h1, .ov-body h2, .ov-body h3 {
  font-family: 'DM Serif Display', serif;
  color: var(--navy);
  line-height: 1.25;
  margin: 1.6rem 0 0.6rem;
}
.ov-body h1 { font-size: 1.5rem; }
.ov-body h2 { font-size: 1.25rem; }
.ov-body h3 { font-size: 1.05rem; }
.ov-body h2 em, .ov-body h3 em { font-style: italic; color: var(--gold); }
.ov-body p { margin: 0 0 1rem; }
.ov-body strong { color: var(--navy); font-weight: 600; }
.ov-body em { font-style: italic; }
.ov-body ul, .ov-body ol { margin: 0.6rem 0 1rem 1.2rem; padding-left: 0.6rem; }
.ov-body li { margin-bottom: 0.4rem; }
.ov-body code {
  font-family: 'DM Mono', ui-monospace, SFMono-Regular, monospace;
  background: var(--cream);
  border: 1px solid var(--border);
  padding: 0.08rem 0.4rem;
  border-radius: 2px;
  font-size: 0.86em;
  color: var(--navy);
}
.ov-body pre {
  background: var(--cream);
  border: 1px solid var(--border);
  border-radius: 2px;
  padding: 1rem;
  margin: 1rem 0;
  overflow-x: auto;
  font-size: 0.84rem;
  line-height: 1.6;
}
.ov-body pre code { background: transparent; border: 0; padding: 0; }
.ov-body blockquote {
  margin: 1rem 0;
  padding: 0.4rem 1.2rem;
  border-left: 3px solid var(--gold);
  color: var(--text-mid);
  font-style: italic;
}
.ov-body a { color: var(--navy-light); text-decoration: underline; }
.ov-foot {
  padding: 1rem 2.6rem;
  border-top: 1px solid var(--border);
  background: var(--cream);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
  display: flex; justify-content: space-between; align-items: center;
}
.ov-foot a {
  color: var(--gold);
  font-weight: 600;
  text-decoration: none;
  border-bottom: 1px solid rgba(201,168,76,0.3);
  padding-bottom: 2px;
}
.ov-foot a:hover { border-color: var(--gold); }
@media (max-width: 640px) {
  #overlay { padding: 2rem 1rem 1rem; }
  .ov-meta, .ov-title, .ov-body, .ov-foot { padding-left: 1.4rem; padding-right: 1.4rem; }
  .ov-meta { padding-top: 1.6rem; }
}

/* SYSTEMS — content-rendered cards (image-based) */
.sys-card.from-content { cursor: zoom-in; }
.sys-card .sys-visual.image-bg {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.sys-card .sys-visual.image-bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(11,22,40,0) 40%, rgba(11,22,40,0.55) 100%);
}

/* LIGHTBOX for system diagrams */
#lightbox {
  position: fixed;
  inset: 0;
  background: rgba(11,22,40,0.96);
  z-index: 9991;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  cursor: zoom-out;
}
#lightbox.open { display: flex; }
#lightbox img {
  max-width: 95%;
  max-height: 90%;
  border: 1px solid rgba(201,168,76,0.3);
  border-radius: 4px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.6);
  animation: ov-in 0.3s cubic-bezier(0.34,1.56,0.64,1);
}
.lb-caption {
  position: fixed;
  bottom: 1.4rem;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  color: var(--gold-light);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
"""

# inject CSS before </style>
old_style_close = "</style>\n</head>"
assert old_style_close in s, "</style></head> not found"
s = s.replace(old_style_close, new_css + "\n</style>\n</head>")

# ─────────────────────────────────────────────────────────────────────────
# 3. SHIPPING STRIP — inserted RIGHT AFTER </section> closing #hero, BEFORE #about
# ─────────────────────────────────────────────────────────────────────────
shipping_html = """
<!-- SHIPPING STRIP — currently active engagements, anonymised -->
<div class="shipping">
  <div class="ship-grid">
    <div class="ship-label">Currently Shipping</div>
    <div class="ship-rows">
      <div class="ship-row">
        <span class="ship-k">Engagement A</span>
        <span class="ship-v">Agentic AI for <em>SDLC</em><br><span style="font-size:0.74rem;color:var(--text-muted)">Kiro · 5-agent topology</span></span>
      </div>
      <div class="ship-row">
        <span class="ship-k">Engagement B</span>
        <span class="ship-v">Agentic AI for <em>STLC</em><br><span style="font-size:0.74rem;color:var(--text-muted)">MS Agent FW · .NET</span></span>
      </div>
      <div class="ship-row">
        <span class="ship-k">Internal Platforms</span>
        <span class="ship-v">AI <em>validation</em> &amp; eval<br><span style="font-size:0.74rem;color:var(--text-muted)">QMentisAI · ValidAIte</span></span>
      </div>
      <div class="ship-row">
        <span class="ship-k">Governance</span>
        <span class="ship-v"><em>9</em>-gate HITL · file-based<br><span style="font-size:0.74rem;color:var(--text-muted)">handshake contracts</span></span>
      </div>
    </div>
  </div>
</div>
"""

# Find the </section> that closes #hero — it's the one right before the comment "<!-- ABOUT -->"
hero_end_marker = "</section>\n\n<!-- ABOUT -->"
assert hero_end_marker in s, "hero/about boundary not found"
s = s.replace(hero_end_marker, "</section>\n" + shipping_html + "\n<!-- ABOUT -->")

# ─────────────────────────────────────────────────────────────────────────
# 4. WRITING SECTION — inserted between ABOUT and EXPERIENCE
# ─────────────────────────────────────────────────────────────────────────
writing_html = """
<!-- DEEP DIVES — content-driven (rendered from contents/manifest.json) -->
<section id="deep-dives">
  <div class="container">
    <div class="section-label">Deep Dives</div>
    <h2 class="section-title">Long-form thinking on<br>agentic systems &amp; <em style="font-style:italic;color:var(--gold)">governance</em></h2>
    <p class="section-sub">Long-form pieces on the architectural and operational realities of running autonomous AI in production. The kind of writing I'd hand to a CIO before a procurement conversation — not generic explainers.</p>

    <div id="deep-dives-mount" class="writing-grid" data-section="deepDives" data-empty-text="No deep dives published yet. Drop a markdown, txt, or docx file into contents/deep-dives/ and run build_content.py.">
      <div class="content-empty">Loading deep dives…</div>
    </div>
  </div>
</section>
"""

# inject WRITING right before EXPERIENCE
about_to_exp_marker = "<!-- EXPERIENCE -->"
assert about_to_exp_marker in s, "experience marker not found"
s = s.replace(about_to_exp_marker, writing_html + "\n" + about_to_exp_marker)

# ─────────────────────────────────────────────────────────────────────────
# 5. SYSTEMS — inserted between SKILLS and EDUCATION
# ─────────────────────────────────────────────────────────────────────────
systems_html = """
<!-- SYSTEMS — content-driven (architecture diagrams from contents/systems/) -->
<section id="systems">
  <div class="container">
    <div class="section-label-light">Reference Architectures</div>
    <h2 class="section-title" style="color:var(--white)">Designs drawn from<br><em style="font-style:italic;color:var(--gold-light)">real</em> engagements</h2>
    <p class="section-sub-light">Cleaned-up reference architectures from production work — the shapes that survived contact with regulated procurement, real ops teams, and live agents. Anonymized.</p>

    <div id="systems-mount" class="sys-grid" data-section="systems" data-empty-text="No architecture diagrams yet. Drop a .jpg or .png into contents/systems/ (with optional .json sidecar) and run build_content.py.">
      <div class="content-empty-dark">Loading architectures…</div>
    </div>
  </div>
</section>
"""

# Insert SYSTEMS between SKILLS and EDUCATION
edu_marker = "<!-- EDUCATION -->"
assert edu_marker in s
s = s.replace(edu_marker, systems_html + "\n" + edu_marker)

# ─────────────────────────────────────────────────────────────────────────
# 6. APPLIED LABS + FIELD NOTES — between EDUCATION and CONTACT
# ─────────────────────────────────────────────────────────────────────────
labs_notes_html = """
<!-- APPLIED LABS — content-driven (from contents/labs/) -->
<section id="labs">
  <div class="container">
    <div class="section-label">Applied Labs</div>
    <h2 class="section-title">Practitioner research,<br>shipped <em style="font-style:italic;color:var(--gold)">in public</em></h2>
    <p class="section-sub">Things I run as production-grade labs to test ideas in the open — under my own constraints, with real users, real data, and real downtime when I get it wrong. The patterns that survive get folded back into client work.</p>

    <div id="labs-mount" class="lab-grid" data-section="labs" data-empty-text="No labs published yet. Drop a .md, .txt, or .docx into contents/labs/ and run build_content.py.">
      <div class="content-empty">Loading labs…</div>
    </div>
  </div>
</section>

<!-- FIELD NOTES — content-driven (from contents/notes/) -->
<section id="notes">
  <div class="container">
    <div class="section-label">Field Notes</div>
    <h2 class="section-title">Running notes from<br><em style="font-style:italic;color:var(--gold)">the workbench</em></h2>
    <p class="section-sub">Half-formed observations, posted because the half-formed version is more useful than the polished version that never ships. Updated as the engagements move.</p>

    <div id="notes-mount" class="notes-list" data-section="notes" data-empty-text="No field notes yet. Drop a .txt or .md into contents/notes/ and run build_content.py.">
      <div class="content-empty">Loading notes…</div>
    </div>
  </div>
</section>
"""

contact_marker = "<!-- CONTACT -->"
assert contact_marker in s
s = s.replace(contact_marker, labs_notes_html + "\n" + contact_marker)

# ─────────────────────────────────────────────────────────────────────────
# 7. ABOUT — refine the two paragraphs to match the new positioning
# Replace ONLY the two paragraphs inside .about-text, not the contact list.
# ─────────────────────────────────────────────────────────────────────────
old_about = """        <p>I'm an independent AI Solutions Leader with 11+ years of experience spanning Generative AI, NLP, robotics, and enterprise AI transformation. I architect agentic AI systems, lead multi-agent orchestration initiatives, and advise enterprises on AI strategy and governance.</p>
        <p>My journey spans healthcare NLP, BFSI predictive analytics, autonomous robotics, and large-scale multi-agent orchestration — giving me a uniquely broad perspective on how AI can be applied strategically across industries.</p>"""

new_about = """        <p>I'm an AI Architect with 11+ years across Generative AI, agentic systems, NLP, robotics, and enterprise data science. My current focus is the governed end of agentic AI — the architectures, gates, and observability that let autonomous systems run inside regulated, mission-critical environments without quietly going off the rails.</p>
        <p>Recent work has included agentic AI for SDLC lifecycles (Kiro-based, 5-agent topology with 9 HITL governance gates) and agentic AI for STLC lifecycles (Microsoft Agent Framework on .NET) — alongside internal AI evaluation and validation platforms (QMentisAI, ValidAIte). My earlier journey across healthcare NLP, BFSI predictive analytics, and autonomous robotics is what gave me the breadth to design for that governed end.</p>"""

assert old_about in s
s = s.replace(old_about, new_about)

# ─────────────────────────────────────────────────────────────────────────
# 8. HERO — refine title + summary to match the new positioning
# ─────────────────────────────────────────────────────────────────────────
old_hero_title = """    <p class="hero-title">Consulting · Corporate Trainings · Interview Prep · Enterprise AI</p>
    <p class="hero-summary">Helping businesses and individuals harness AI — from enterprise GenAI strategy and agentic system design to corporate AI trainings and career-focused interview preparation.</p>"""

new_hero_title = """    <p class="hero-title">Agentic Systems · Governance · Enterprise GenAI · Training</p>
    <p class="hero-summary">Most AI prototypes look impressive. Very few survive governance, scale, and real operational friction. I design and ship the ones that do.</p>"""

assert old_hero_title in s
s = s.replace(old_hero_title, new_hero_title)

# ─────────────────────────────────────────────────────────────────────────
# 9. EXPERIENCE — sanitise the Qualizeal entry to remove any client traces
#    (the current copy is already clean, but tighten it to match new framing)
# ─────────────────────────────────────────────────────────────────────────
old_qz = """          <div class="tl-role">AI Architect &amp; Strategy Planner</div>
          <ul class="tl-bullets">
            <li>Leading and delivering Agentic AI enterprise initiatives from the AI Think Tank / Center of Excellence.</li>
            <li>Designing and implementing multi-agent systems using LangGraph, CrewAI, and AutoGen.</li>
            <li>Driving AI architecture strategy, governance, and scalable GenAI adoption across enterprise programs.</li>
          </ul>"""

new_qz = """          <div class="tl-role">AI Architect</div>
          <ul class="tl-bullets">
            <li>Leading agentic AI engagements from the AI Center of Excellence — including SDLC automation with Kiro (5-agent topology, 9 HITL governance gates) and STLC automation with Microsoft Agent Framework on .NET.</li>
            <li>Architecting internal AI evaluation and validation platforms — QMentisAI EV and ValidAIte — covering multi-agent eval, drift detection, and model behaviour testing.</li>
            <li>Driving AI architecture strategy, governance frameworks, and scalable GenAI adoption across enterprise programs in regulated industries.</li>
          </ul>"""

assert old_qz in s
s = s.replace(old_qz, new_qz)

# ─────────────────────────────────────────────────────────────────────────
# 10. SKILLS — add a "Lifecycle Automation" group reflecting Kiro / MS Agent FW
#     Replace the "Leadership & Services" group to also tighten language.
# ─────────────────────────────────────────────────────────────────────────
old_skill_last = """      <div class="skill-group fi" style="transition-delay:0.24s"><div class="sg-title">Leadership & Services</div><div class="skill-tags"><span class="stag">Corporate Training</span><span class="stag">Interview Prep</span><span class="stag">IT Consulting</span><span class="stag">Team Mentoring</span><span class="stag">AI Advisory</span><span class="stag">Program Delivery</span></div></div>"""

new_skill_last = """      <div class="skill-group fi" style="transition-delay:0.24s"><div class="sg-title">Lifecycle Automation</div><div class="skill-tags"><span class="stag">Agentic SDLC</span><span class="stag">Agentic STLC</span><span class="stag">Kiro</span><span class="stag">MS Agent Framework</span><span class="stag">.NET</span><span class="stag">HITL Governance</span><span class="stag">File-based Handshake</span></div></div>
      <div class="skill-group fi" style="transition-delay:0.32s"><div class="sg-title">Leadership &amp; Services</div><div class="skill-tags"><span class="stag">AI Advisory</span><span class="stag">Architecture Reviews</span><span class="stag">Corporate Training</span><span class="stag">Interview Prep</span><span class="stag">Team Mentoring</span><span class="stag">Program Delivery</span></div></div>"""

assert old_skill_last in s
s = s.replace(old_skill_last, new_skill_last)

# also: widen skills-grid responsive break — there are now 7 groups
# (existing CSS already handles repeat(3,1fr) fine, so leave it)

# ─────────────────────────────────────────────────────────────────────────
# 11. PHOENIX KB — add new intents covering the new positioning.
#     Positioning is capability-first (Agentic SDLC, Agentic STLC, eval/validation
#     platforms) — never client-named.
# ─────────────────────────────────────────────────────────────────────────
# Insert after the "AGENTIC GOVERNANCE & ARCHITECTURE" entry's closing }, so it
# appears near the architecture section of the KB. Easiest: prepend new entries
# inside KB just before the final closing "];".
new_kb_block = r"""
  /* ════════════════════════════════
     AGENTIC SDLC / KIRO POSITIONING (anonymised)
  ════════════════════════════════ */
  {
    p: /agentic ai (for )?sdlc|sdlc (lifecycle|automation|with kiro|agents)|kiro (subagent|topology|framework|agent)|5.agent topology|9 gate|9.gate|hitl gate|governed sdlc/i,
    q: ['agentic ai for sdlc','sdlc automation','sdlc with kiro','kiro agents','5 agent topology','9 hitl gates','governed sdlc','hitl gates'],
    a: (_) => "One of Prashobh's current focus areas. He works on agentic AI for SDLC lifecycles using Kiro — a 5-agent topology (feature → dev → review → test → docs) with 9 HITL governance gates and file-based handshake contracts. Designed for regulated, mission-critical environments where governance can't be an afterthought.\n\nFor a deeper conversation:\n📅 https://calendly.com/prashobhpaulnambadan\n📧 prashobhpaulnambadan@gmail.com"
  },

  /* ════════════════════════════════
     AGENTIC STLC / MS AGENT FRAMEWORK / .NET
  ════════════════════════════════ */
  {
    p: /agentic ai (for )?stlc|stlc (lifecycle|automation|agents)|microsoft agent framework|ms agent framework|\.net.*agent|agent.*\.net/i,
    q: ['agentic ai for stlc','stlc automation','microsoft agent framework','ms agent framework','agentic ai with .net','dotnet agents'],
    a: (_) => "Another active engagement. He works on agentic AI for STLC lifecycles using Microsoft Agent Framework on .NET — paired with MCP for tool access and Azure-native deployment. The choice of .NET over Python-native orchestration is deliberate when the target stack is .NET-heavy.\n\nFor architecture-level discussion:\n📅 https://calendly.com/prashobhpaulnambadan\n📧 prashobhpaulnambadan@gmail.com"
  },

  /* ════════════════════════════════
     INTERNAL AI PLATFORMS — QMentisAI / ValidAIte
  ════════════════════════════════ */
  {
    p: /qmentisai|qmentis ai|qmentis|validaite|valid ai te|validate ai|ai (testing|validation|evaluation) (platform|framework)/i,
    q: ['qmentisai','validaite','ai validation platform','ai testing platform','ai evaluation framework','what is qmentis','what is validaite'],
    a: (_) => "QMentisAI and ValidAIte are internal AI platforms Prashobh contributes to — covering multi-agent evaluation, drift detection, model behaviour testing, and validation for enterprise AI deployments.\n\nThey're not public products, but the underlying patterns inform a lot of his architecture work.\n\nFor a conversation on AI evaluation design:\n📅 https://calendly.com/prashobhpaulnambadan"
  },

  /* ════════════════════════════════
     APPLIED LABS — ProfitPilot / IPLBuzz / Pachaka Lokam / RVonWheelz
  ════════════════════════════════ */
  {
    p: /profit ?pilot|profitpilot|nse (analysis|stock|tool)|stock analysis (pwa|tool|app)/i,
    q: ['profitpilot','what is profitpilot','nse stock analysis','stock analysis app'],
    a: (_) => "ProfitPilot is one of Prashobh's Applied Labs — a backtest-gated NSE stock analysis pipeline with FinBERT sentiment, CANSLIM fundamentals, and a 20+ indicator rules engine, shipped as a PWA. It's where he works out how to keep an ML pipeline honest about its own failure modes.\n\n🐙 https://github.com/PrashobhPaul/StockAnalysis_IndianMarket"
  },
  {
    p: /ipl ?buzz|ipl prediction|cricket (prediction|analytics|app)|sports (prediction|analytics)/i,
    q: ['iplbuzz','ipl prediction','cricket analytics','sports prediction app'],
    a: (_) => "IPLBuzz is an Applied Lab — a production-grade rule-based statistical match prediction engine for the IPL with a multi-voice NLG narrative layer. No LLM in the prediction path, by design. Built to study where rule-based engines still out-discipline LLMs.\n\n🐙 https://github.com/PrashobhPaul"
  },
  {
    p: /pachaka ?lokam|meal planner|kerala (food|meal|recipe)|household (planner|app)/i,
    q: ['pachaka lokam','meal planner','kerala meal app','household planner'],
    a: (_) => "Pachaka Lokam is an Applied Lab — a Kerala-style household meal planning PWA with pantry-aware suggestions, weekly templates with smart substitution, and maid/milk delivery tracking. Shipped to the Play Store via TWA.\n\n🌐 https://pachakalokam.prashobhpaul.com"
  },
  {
    p: /rv ?on ?wheelz|rvonwheelz|carpool|society (app|carpool)/i,
    q: ['rvonwheelz','carpooling app','society app','community carpool'],
    a: (_) => "RVonWheelz is an Applied Lab — a society carpooling app for a residential community with tab navigation, auto-destination filters, and real-time matching. A study in keeping a small, useful product small and useful.\n\n🌐 https://rvonwheelz.lovable.app"
  },

  /* ════════════════════════════════
     APPLIED LABS — overview
  ════════════════════════════════ */
  {
    p: /(applied )?labs|side projects?|personal projects?|hobby projects?|github (work|projects)|what (does he|has he) build(t|s|ed)? (on the side|outside work|personally)/i,
    q: ['applied labs','side projects','personal projects','hobby projects','his github work','what does he build personally'],
    a: (_) => "Prashobh runs his personal builds as Applied Labs — production-grade research shipped in public, under his own constraints, with real users and real downtime when something goes wrong. Patterns that survive there get folded back into client work.\n\nCurrent active labs include ProfitPilot (capital markets ML), IPLBuzz (sports analytics, rule-based), Pachaka Lokam (household meal planning PWA), and RVonWheelz (community carpool).\n\n🐙 https://github.com/PrashobhPaul"
  },
"""

# Insert this block right after the very first "/* ════════════════════════════════" sentinel
# that follows the "AGENTIC GOVERNANCE & ARCHITECTURE" entry. Easier and safer:
# inject it at the start of KB, right after "const KB = [\n"
kb_anchor = "const KB = [\n"
assert kb_anchor in s
s = s.replace(kb_anchor, kb_anchor + new_kb_block + "\n")

# ─────────────────────────────────────────────────────────────────────────
# 12. Quick-reply buttons — add a "Writing" pill to surface deep dives in chat
# ─────────────────────────────────────────────────────────────────────────
old_qr = """    <button class="qr-btn" onclick="sendQuick('Tell me about your experience')">Experience</button>
    <button class="qr-btn" onclick="sendQuick('Do you offer corporate training?')">Training</button>"""

new_qr = """    <button class="qr-btn" onclick="sendQuick('Tell me about your experience')">Experience</button>
    <button class="qr-btn" onclick="sendQuick('Agentic AI for SDLC')">Agentic Work</button>
    <button class="qr-btn" onclick="sendQuick('Do you offer corporate training?')">Training</button>"""

assert old_qr in s
s = s.replace(old_qr, new_qr)

# ─────────────────────────────────────────────────────────────────────────
# 13. CONTENT LOADER — inject overlay DOM + runtime script that fetches
#     contents/manifest.json and renders the four content-driven sections.
# ─────────────────────────────────────────────────────────────────────────

overlay_dom = """
<!-- CONTENT OVERLAY (deep dive / lab reader) -->
<div id="overlay" onclick="if(event.target.id==='overlay')closeOverlay()">
  <article class="ov-card">
    <button class="ov-close" onclick="closeOverlay()" aria-label="Close">✕</button>
    <div class="ov-meta" id="ov-meta"></div>
    <h2 class="ov-title" id="ov-title"></h2>
    <div class="ov-body" id="ov-body"></div>
    <div class="ov-foot" id="ov-foot"></div>
  </article>
</div>

<!-- LIGHTBOX (systems diagrams) -->
<div id="lightbox" onclick="closeLightbox()">
  <img id="lb-img" src="" alt="" />
  <div class="lb-caption" id="lb-cap"></div>
</div>
"""

content_loader_js = r"""
/* ══════════════════════════════════════════════════════════════
   CONTENT LOADER — fetches contents/manifest.json and renders
   deep-dives, systems, labs, notes from disk-driven content.
   ══════════════════════════════════════════════════════════════ */
(function() {
  const MANIFEST_URL = 'contents/manifest.json';

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function emph(s) {
    // Allow a single *word* or *short phrase* in titles to render in italic gold
    return esc(s).replace(/\*([^*]{1,40})\*/g, '<em>$1</em>');
  }
  function fmtDate(iso) {
    if (!iso) return '';
    try {
      const d = new Date(iso);
      if (isNaN(d)) return iso;
      return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    } catch (e) { return iso; }
  }

  function render(manifest) {
    renderDeepDives(manifest.deepDives || []);
    renderSystems(manifest.systems || []);
    renderLabs(manifest.labs || []);
    renderNotes(manifest.notes || []);
  }

  /* ───── DEEP DIVES ───── */
  function renderDeepDives(items) {
    const mount = document.getElementById('deep-dives-mount');
    if (!mount) return;
    if (!items.length) {
      mount.innerHTML = '<div class="content-empty">' + esc(mount.dataset.emptyText) + '</div>';
      return;
    }
    const featured = items.find(it => it.featured) || items[0];
    const rest = items.filter(it => it !== featured).slice(0, 6);

    let html = '';
    html += `
      <a class="featured-piece" href="#" onclick="event.preventDefault();openContent('deepDives','${esc(featured.slug)}')">
        <div class="fp-visual">${featured.diagram || defaultDiveSvg()}</div>
        <div class="fp-body">
          <div class="fp-meta">
            <span>${esc(fmtDate(featured.date))}</span>
            <span class="gold">${esc((featured.kicker || 'Featured Deep Dive').toUpperCase())}</span>
            ${featured.readingTime ? `<span>${esc(featured.readingTime)}</span>` : ''}
          </div>
          <h3 class="fp-title">${emph(featured.title)}</h3>
          <p class="fp-hook">${esc(featured.hook || '')}</p>
          <span class="fp-link">Read the dive</span>
        </div>
      </a>`;
    if (rest.length) {
      html += '<div class="writing-list">';
      rest.forEach(it => {
        html += `
          <a class="wl-card" href="#" onclick="event.preventDefault();openContent('deepDives','${esc(it.slug)}')">
            <span class="wl-tag">${esc((it.kicker || 'Deep Dive').toUpperCase())}</span>
            <h4 class="wl-title">${emph(it.title)}</h4>
            <p class="wl-hook">${esc(it.hook || '')}</p>
            <span class="wl-foot">${esc([it.readingTime, ...(it.tags || []).slice(0, 2)].filter(Boolean).join(' · '))}</span>
          </a>`;
      });
      html += '</div>';
    }
    mount.innerHTML = html;
  }

  /* ───── SYSTEMS (architecture images) ───── */
  function renderSystems(items) {
    const mount = document.getElementById('systems-mount');
    if (!mount) return;
    if (!items.length) {
      mount.innerHTML = '<div class="content-empty-dark">' + esc(mount.dataset.emptyText) + '</div>';
      return;
    }
    mount.innerHTML = items.slice(0, 6).map(it => `
      <div class="sys-card from-content" onclick="openLightbox('${esc(it.image)}','${esc(it.title)}')">
        <div class="sys-visual image-bg" style="background-image:url('${esc(it.image)}')"></div>
        <div class="sys-body">
          <span class="sys-tag">${esc((it.tag || 'Architecture').toUpperCase())}</span>
          <h3 class="sys-title">${emph(it.title)}</h3>
          <p class="sys-desc">${esc(it.description || '')}</p>
          <div class="sys-foot">
            <span>${esc((it.meta || '').toUpperCase())}</span>
            <span class="stage">${esc((it.stage || 'Reference').toUpperCase())}</span>
          </div>
        </div>
      </div>`).join('');
  }

  /* ───── LABS ───── */
  function renderLabs(items) {
    const mount = document.getElementById('labs-mount');
    if (!mount) return;
    if (!items.length) {
      mount.innerHTML = '<div class="content-empty">' + esc(mount.dataset.emptyText) + '</div>';
      return;
    }
    mount.innerHTML = items.slice(0, 8).map(it => `
      <a class="lab-card" href="#" onclick="event.preventDefault();openContent('labs','${esc(it.slug)}')">
        <div class="lab-head">
          <span class="lab-domain">${esc((it.domain || 'Lab').toUpperCase())}</span>
          <span class="lab-status ${it.status === 'archived' ? 'archived' : ''}">${esc(it.status || 'Live')}</span>
        </div>
        <h3 class="lab-title">${emph(it.title)}</h3>
        <p class="lab-hook">${esc(it.hook || '')}</p>
        <div class="lab-tech">
          ${(it.tech || []).map(t => `<span>${esc(t)}</span>`).join('')}
        </div>
      </a>`).join('');
  }

  /* ───── NOTES ───── */
  function renderNotes(items) {
    const mount = document.getElementById('notes-mount');
    if (!mount) return;
    if (!items.length) {
      mount.innerHTML = '<div class="content-empty">' + esc(mount.dataset.emptyText) + '</div>';
      return;
    }
    mount.innerHTML = items.slice(0, 10).map(it => `
      <div class="note-row" onclick="openContent('notes','${esc(it.slug)}')" style="cursor:pointer">
        <div class="note-date">${esc(fmtDate(it.date))}</div>
        <div class="note-content">
          <h4 class="note-title">${emph(it.title)}</h4>
          <p class="note-excerpt">${esc(it.hook || '')}</p>
        </div>
        <div class="note-cat">${esc((it.category || '').toUpperCase())}</div>
      </div>`).join('');
  }

  /* ───── CONTENT OVERLAY ───── */
  let currentManifest = null;
  window.openContent = function(section, slug) {
    if (!currentManifest) return;
    const item = (currentManifest[section] || []).find(x => x.slug === slug);
    if (!item) return;
    const meta = [];
    if (item.date) meta.push(`<span>${esc(fmtDate(item.date))}</span>`);
    if (item.kicker || item.domain || item.category) meta.push(`<span class="gold">${esc((item.kicker || item.domain || item.category).toUpperCase())}</span>`);
    if (item.readingTime) meta.push(`<span>${esc(item.readingTime)}</span>`);
    document.getElementById('ov-meta').innerHTML = meta.join('');
    document.getElementById('ov-title').innerHTML = emph(item.title);
    document.getElementById('ov-body').innerHTML =
      '<p style="color:var(--text-muted);font-family:\'DM Sans\',sans-serif;font-size:0.8rem">Loading…</p>';

    let footHtml = '';
    if (item.source) footHtml += `<span>Source: ${esc(item.source.split('/').pop())}</span>`;
    footHtml += `<a href="#contact" onclick="closeOverlay()">Reach out →</a>`;
    document.getElementById('ov-foot').innerHTML = footHtml;

    document.getElementById('overlay').classList.add('open');
    document.body.style.overflow = 'hidden';

    fetch(item.html, { cache: 'no-cache' })
      .then(r => r.ok ? r.text() : Promise.reject(r.status))
      .then(t => { document.getElementById('ov-body').innerHTML = t; })
      .catch(err => {
        document.getElementById('ov-body').innerHTML =
          `<p style="color:var(--text-muted)">Could not load content (${err}). Please check that build_content.py has been run.</p>`;
      });
  };
  window.closeOverlay = function() {
    document.getElementById('overlay').classList.remove('open');
    document.body.style.overflow = '';
  };

  /* ───── LIGHTBOX ───── */
  window.openLightbox = function(src, caption) {
    document.getElementById('lb-img').src = src;
    const clean = String(caption || '').replace(/\*([^*]+)\*/g, '$1');
    document.getElementById('lb-img').alt = clean;
    document.getElementById('lb-cap').textContent = clean;
    document.getElementById('lightbox').classList.add('open');
    document.body.style.overflow = 'hidden';
  };
  window.closeLightbox = function() {
    document.getElementById('lightbox').classList.remove('open');
    document.body.style.overflow = '';
  };

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      if (document.getElementById('lightbox').classList.contains('open')) closeLightbox();
      else if (document.getElementById('overlay').classList.contains('open')) closeOverlay();
    }
  });

  /* ───── DEFAULT DIVE SVG (when a piece has no diagram of its own) ───── */
  function defaultDiveSvg() {
    return `<svg viewBox="0 0 600 320" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <linearGradient id="ddv-flow" x1="0" x2="1">
          <stop offset="0" stop-color="#c9a84c" stop-opacity="0"/>
          <stop offset=".5" stop-color="#c9a84c" stop-opacity=".6"/>
          <stop offset="1" stop-color="#c9a84c" stop-opacity="0"/>
        </linearGradient>
        <pattern id="ddv-grid" width="40" height="40" patternUnits="userSpaceOnUse">
          <path d="M40 0H0V40" fill="none" stroke="rgba(201,168,76,.06)" stroke-width="1"/>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#ddv-grid)"/>
      <g fill="none" stroke="#c9a84c" stroke-width="1.2">
        <rect x="60"  y="135" width="78" height="55" rx="1"/>
        <rect x="178" y="135" width="78" height="55" rx="1"/>
        <rect x="296" y="135" width="78" height="55" rx="1"/>
        <rect x="414" y="135" width="78" height="55" rx="1"/>
        <rect x="520" y="135" width="46" height="55" rx="1"/>
      </g>
      <g fill="none" stroke="rgba(201,168,76,.55)" stroke-width="1">
        <circle cx="158" cy="100" r="11"/><circle cx="276" cy="100" r="11"/>
        <circle cx="394" cy="100" r="11"/><circle cx="506" cy="100" r="11"/>
      </g>
      <g font-family="DM Sans" font-size="10" font-weight="600" fill="#c9a84c" text-anchor="middle">
        <text x="158" y="104">G1</text><text x="276" y="104">G3</text>
        <text x="394" y="104">G6</text><text x="506" y="104">G9</text>
      </g>
      <g stroke="url(#ddv-flow)" stroke-width="1.5" fill="none">
        <path d="M138 162 L178 162"/><path d="M256 162 L296 162"/>
        <path d="M374 162 L414 162"/><path d="M492 162 L520 162"/>
      </g>
      <g stroke="rgba(201,168,76,.3)" stroke-width="1" stroke-dasharray="2 3">
        <path d="M158 111 L158 135"/><path d="M276 111 L276 135"/>
        <path d="M394 111 L394 135"/><path d="M506 111 L506 135"/>
      </g>
      <g font-family="DM Sans" font-size="10" fill="rgba(255,255,255,0.55)" text-anchor="middle" letter-spacing="0.06em">
        <text x="99" y="212">FEATURE</text><text x="217" y="212">DEV</text>
        <text x="335" y="212">REVIEW</text><text x="453" y="212">TEST</text>
        <text x="543" y="212">DOCS</text>
      </g>
      <circle cx="543" cy="162" r="14" fill="none" stroke="#e8c97a" stroke-width="1.2">
        <animate attributeName="r" values="14;26;14" dur="3s" repeatCount="indefinite"/>
        <animate attributeName="stroke-opacity" values="0.8;0;0.8" dur="3s" repeatCount="indefinite"/>
      </circle>
      <g font-family="DM Sans" font-size="9" fill="rgba(255,255,255,0.4)" letter-spacing="0.12em">
        <text x="60" y="275">5-AGENT TOPOLOGY · 9 HITL GATES · FILE-BASED HANDSHAKE</text>
        <text x="60" y="292" fill="#c9a84c">AGENTIC SDLC · GOVERNED · PRODUCTION REFERENCE</text>
      </g>
    </svg>`;
  }

  /* ───── BOOT ───── */
  fetch(MANIFEST_URL, { cache: 'no-cache' })
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(m => { currentManifest = m; render(m); })
    .catch(err => {
      console.warn('[content-loader] no manifest:', err);
      // Show empty states everywhere
      ['deep-dives-mount','systems-mount','labs-mount','notes-mount'].forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        const cls = id === 'systems-mount' ? 'content-empty-dark' : 'content-empty';
        el.innerHTML = `<div class="${cls}">${esc(el.dataset.emptyText)}</div>`;
      });
    });
})();
"""

# Inject the overlay DOM right before the chatbot launcher
chat_anchor = "<!-- CHATBOT LAUNCHER -->"
assert chat_anchor in s
s = s.replace(chat_anchor, overlay_dom + "\n" + chat_anchor)

# Inject the content loader JS right before the existing closing </script>
# (it's the LAST </script> in the file, which closes the Phoenix code)
last_script_close = s.rfind("</script>")
assert last_script_close > 0
s = s[:last_script_close] + content_loader_js + "\n" + s[last_script_close:]

# ─────────────────────────────────────────────────────────────────────────
# WRITE OUT
# ─────────────────────────────────────────────────────────────────────────
DST.write_text(s, encoding="utf-8")
print(f"✓ wrote {DST}  ({len(s):,} chars)")
print(f"  source preserved at {SRC}")
