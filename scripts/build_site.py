from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "content" / "notes"
CODE_DIR = ROOT / "content" / "code"
ABC_DIR = ROOT / "ABC板刷"
ABC_NOTES_DIR = ABC_DIR / "云遥栈"
OUT_DIR = ROOT / "generated"
PROBLEMS_DIR = OUT_DIR / "problems"
CONTESTS_DIR = OUT_DIR / "contests"
CONTEST_CODE_DIR = OUT_DIR / "contest-code"

SITE_CSS = """
:root {
  --bg: #f7f1e9;
  --paper: #fffaf4;
  --paper-soft: #f6ede2;
  --ink: #1f1e1a;
  --muted: #6f675f;
  --accent: #b56a45;
  --teal: #5f7c7f;
  --line: rgba(31, 30, 26, 0.1);
  --shadow: 0 22px 60px rgba(72, 52, 40, 0.12);
  --radius-lg: 28px;
  --radius-md: 18px;
  --wrap: 1120px;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: "Georgia", "Times New Roman", serif;
  color: var(--ink);
  background:
    radial-gradient(circle at top left, rgba(181, 106, 69, 0.18), transparent 28%),
    radial-gradient(circle at top right, rgba(95, 124, 127, 0.12), transparent 24%),
    linear-gradient(180deg, #fbf6ef 0%, #f2e7d9 100%);
}
a { color: inherit; }
.wrap { width: min(var(--wrap), calc(100vw - 28px)); margin: 20px auto 32px; }
.shell {
  border: 1px solid rgba(255, 255, 255, 0.48);
  border-radius: 34px;
  background: rgba(255, 250, 244, 0.76);
  backdrop-filter: blur(14px);
  box-shadow: var(--shadow);
  overflow: hidden;
}
.shell > * { position: relative; }
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 22px 28px;
  border-bottom: 1px solid rgba(31, 30, 26, 0.06);
  background: rgba(255, 250, 244, 0.82);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 4;
}
.brand {
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 12px;
}
.brand-mark {
  width: 40px;
  height: 40px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  background: linear-gradient(145deg, #d79b74, #8e4f33);
  color: #fff8f2;
}
.brand-text strong,
.brand-text span { display: block; }
.brand-text strong { font-size: 1rem; }
.brand-text span {
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}
.nav-links {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  align-items: center;
}
.nav-links a {
  text-decoration: none;
  color: var(--muted);
}
.pill {
  padding: 10px 16px;
  border-radius: 999px;
  background: var(--ink);
  color: #fff8f2 !important;
}
.hero {
  padding: 30px 28px 20px;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 20px;
  align-items: start;
}
.card {
  padding: 26px;
  border-radius: var(--radius-lg);
  background: rgba(255, 251, 246, 0.84);
  border: 1px solid rgba(31, 30, 26, 0.06);
  box-shadow: 0 10px 30px rgba(72, 52, 40, 0.05);
}
.eyebrow {
  display: inline-flex;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 0.82rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #7f4326;
  background: rgba(181, 106, 69, 0.12);
}
h1, h2, h3, p, pre { margin: 0; }
h1 {
  margin-top: 18px;
  font-size: clamp(2.5rem, 7vw, 4.8rem);
  line-height: 0.96;
}
h2 {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  line-height: 1;
}
h3 { font-size: 1.25rem; }
p {
  color: var(--muted);
  line-height: 1.8;
}
.hero p { margin-top: 18px; }
.meta-grid,
.entry-grid,
.detail-grid {
  display: grid;
  gap: 18px;
}
.meta-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin-top: 22px;
}
.meta {
  padding: 18px;
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.56);
  border: 1px solid rgba(31, 30, 26, 0.06);
}
.meta strong,
.meta span { display: block; }
.meta strong { font-size: 1.3rem; }
.meta span { margin-top: 6px; color: var(--muted); font-size: 0.92rem; }
.section { padding: 16px 28px 30px; }
.section + .section { border-top: 1px solid rgba(31, 30, 26, 0.06); }
.section-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: end;
  margin-bottom: 22px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(31, 30, 26, 0.08);
}
.section-head p { max-width: 38rem; }
.entry-grid {
  grid-template-columns: 1fr;
}
.entry-card {
  text-decoration: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 18px;
  align-items: start;
}
.entry-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 36px rgba(72, 52, 40, 0.08);
}
.entry-main { min-width: 0; }
.entry-side {
  min-width: 180px;
  text-align: right;
}
.tag-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 14px;
}
.tag {
  display: inline-flex;
  padding: 7px 11px;
  border-radius: 999px;
  background: rgba(181, 106, 69, 0.11);
  color: #7f4326;
  font-size: 0.84rem;
}
.detail-grid {
  grid-template-columns: minmax(0, 0.86fr) minmax(0, 1.14fr);
}
.contest-grid {
  display: grid;
  gap: 18px;
  grid-template-columns: minmax(0, 0.78fr) minmax(0, 1.22fr);
}
.stack {
  display: grid;
  gap: 18px;
}
.code-list {
  display: grid;
  gap: 14px;
}
.code-nav {
  display: grid;
  gap: 12px;
}
.code-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 16px 18px;
  border-radius: 16px;
  text-decoration: none;
  background: rgba(255, 255, 255, 0.58);
  border: 1px solid rgba(31, 30, 26, 0.06);
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.code-link:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 26px rgba(72, 52, 40, 0.06);
  border-color: rgba(127, 67, 38, 0.14);
}
.code-link-main {
  min-width: 0;
}
.code-link-main strong,
.code-link-main span {
  display: block;
}
.code-link-main strong {
  font-size: 1rem;
  color: var(--ink);
}
.code-link-main span {
  margin-top: 6px;
  color: var(--muted);
  font-size: 0.92rem;
}
.code-link-side {
  color: #7f4326;
  font-size: 0.9rem;
  white-space: nowrap;
}
.code-item {
  padding: 18px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.52);
  border: 1px solid rgba(31, 30, 26, 0.06);
}
.code-item h4 {
  margin: 0 0 10px;
  font-size: 1rem;
}
.hint {
  padding: 16px 18px;
  border-radius: 16px;
  background: rgba(181, 106, 69, 0.08);
  color: var(--muted);
}
.side-panel {
  position: sticky;
  top: 100px;
}
.note {
  padding: 4px 0;
}
.note h1,
.note h2,
.note h3,
.note h4 {
  margin-top: 26px;
  margin-bottom: 12px;
  line-height: 1.2;
}
.note h1:first-child,
.note h2:first-child,
.note h3:first-child,
.note h4:first-child { margin-top: 0; }
.note ul {
  margin: 10px 0 0 1.2rem;
  color: var(--muted);
  line-height: 1.8;
}
.note ol {
  margin: 10px 0 0 1.25rem;
  color: var(--muted);
  line-height: 1.8;
}
.note hr {
  border: 0;
  border-top: 1px solid rgba(31, 30, 26, 0.1);
  margin: 24px 0;
}
.note blockquote {
  margin: 14px 0 0;
  padding: 12px 16px;
  border-left: 3px solid rgba(181, 106, 69, 0.42);
  background: rgba(181, 106, 69, 0.06);
  color: var(--muted);
}
.note .math-block {
  margin-top: 14px;
  padding: 16px 18px;
  border-radius: 18px;
  background: linear-gradient(180deg, #f6efe7, #f2e8dc);
  border: 1px solid rgba(95, 124, 127, 0.12);
  color: #4b5758;
  overflow: auto;
  font-family: "Times New Roman", "Georgia", serif;
  font-size: 1rem;
  line-height: 1.75;
  white-space: pre-wrap;
}
.note img {
  max-width: 100%;
  border-radius: 16px;
  display: block;
  margin-top: 14px;
}
.note p + p { margin-top: 12px; }
.note pre,
.code-block {
  margin-top: 14px;
  padding: 18px;
  border-radius: 18px;
  background: linear-gradient(180deg, #fbf6ef, #f4ebdf);
  color: #2b2925;
  border: 1px solid rgba(127, 67, 38, 0.12);
  overflow: auto;
  font-size: 0.92rem;
  line-height: 1.65;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7);
  font-family: "SFMono-Regular", "Menlo", "Consolas", monospace;
}
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(31, 30, 26, 0.08);
}
.muted { color: var(--muted); }
.footer {
  padding: 8px 28px 30px;
  color: var(--muted);
  font-size: 0.92rem;
  border-top: 1px solid rgba(31, 30, 26, 0.06);
}
.page-transition {
  position: fixed;
  inset: 0;
  background: rgba(251, 246, 239, 0.82);
  backdrop-filter: blur(10px);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.28s ease;
  z-index: 20;
}
body.is-transitioning .page-transition { opacity: 1; }
body.is-entering .shell {
  opacity: 0;
  transform: translateY(12px);
}
body .shell { transition: opacity 0.45s ease, transform 0.45s ease; }
code {
  padding: 2px 6px;
  border-radius: 999px;
  background: rgba(181, 106, 69, 0.1);
  font-size: 0.92em;
}
pre code {
  padding: 0;
  background: transparent;
  color: inherit;
}
.MathJax {
  font-size: 1.02em !important;
}
@media (max-width: 920px) {
  .hero,
  .entry-grid,
  .detail-grid,
  .meta-grid,
  .contest-grid { grid-template-columns: 1fr; }
  .entry-card { grid-template-columns: 1fr; }
  .code-link {
    align-items: flex-start;
    flex-direction: column;
  }
  .entry-side {
    text-align: left;
    min-width: 0;
  }
  .side-panel { position: static; }
}
@media (max-width: 720px) {
  .wrap { width: min(var(--wrap), calc(100vw - 16px)); margin-top: 10px; }
  .nav, .hero, .section, .footer { padding-left: 18px; padding-right: 18px; }
  .nav { flex-direction: column; align-items: flex-start; }
  .nav-links {
    width: 100%;
    gap: 10px;
  }
  .nav-links a {
    width: 100%;
    padding: 10px 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.48);
  }
  .pill {
    background: var(--ink) !important;
    color: #fff8f2 !important;
    text-align: center;
  }
  .shell {
    border-radius: 24px;
  }
  .card {
    padding: 18px;
    border-radius: 20px;
  }
  h1 {
    margin-top: 14px;
    font-size: clamp(2rem, 10vw, 3rem);
    line-height: 1;
  }
  h2 {
    font-size: clamp(1.45rem, 7vw, 2rem);
  }
  h3 {
    font-size: 1.08rem;
  }
  p {
    font-size: 0.96rem;
  }
  .meta {
    padding: 16px;
  }
  .section {
    padding-top: 14px;
    padding-bottom: 24px;
  }
  .section-head {
    align-items: flex-start;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 18px;
    padding-bottom: 12px;
  }
  .section-head p {
    max-width: none;
  }
  .toolbar {
    align-items: flex-start;
    flex-direction: column;
    gap: 6px;
  }
  .tag-row {
    gap: 8px;
  }
  .tag {
    font-size: 0.8rem;
  }
  .note pre,
  .code-block,
  .note .math-block {
    margin-left: -4px;
    margin-right: -4px;
    padding: 14px;
    border-radius: 14px;
    font-size: 0.86rem;
  }
  .note img {
    border-radius: 12px;
  }
  .code-link {
    padding: 14px;
    gap: 10px;
  }
  .code-link-main strong {
    font-size: 0.96rem;
  }
  .code-link-main span,
  .code-link-side,
  .muted {
    font-size: 0.88rem;
  }
}
@media (max-width: 420px) {
  .wrap {
    width: min(var(--wrap), calc(100vw - 10px));
  }
  .nav, .hero, .section, .footer {
    padding-left: 14px;
    padding-right: 14px;
  }
  .brand-mark {
    width: 36px;
    height: 36px;
    border-radius: 12px;
  }
  .brand-text strong {
    font-size: 0.92rem;
  }
  .brand-text span {
    font-size: 0.72rem;
  }
  .card {
    padding: 16px;
  }
  h1 {
    font-size: clamp(1.8rem, 9vw, 2.5rem);
  }
}
"""


@dataclass
class Entry:
    slug: str
    title: str
    note_html: str
    excerpt: str
    note_path: str | None
    code_path: str | None
    code_text: str | None


@dataclass
class ContestCode:
    filename: str
    path: str
    title: str
    code_text: str
    slug: str


@dataclass
class ContestEntry:
    contest_id: str
    title: str
    slug: str
    note_html: str | None
    note_title: str | None
    note_excerpt: str
    note_path: str | None
    codes: list[ContestCode]


def slugify(value: str) -> str:
    value = value.strip().lower().replace("\\", "/")
    value = re.sub(r"[^a-z0-9/_-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-/").replace("/", "-") or "entry"


def markdown_to_html(text: str) -> tuple[str, str, str]:
    lines = text.splitlines()
    html_parts: list[str] = []
    paragraph: list[str] = []
    bullets: list[str] = []
    ordered_items: list[str] = []
    quote_lines: list[str] = []
    in_code = False
    in_math = False
    code_lines: list[str] = []
    math_lines: list[str] = []
    title = ""
    excerpt = ""

    def flush_paragraph() -> None:
      nonlocal excerpt
      if not paragraph:
          return
      raw = " ".join(part.strip() for part in paragraph).strip()
      if raw:
          rendered = render_inline(raw)
          html_parts.append(f"<p>{rendered}</p>")
          if not excerpt:
              excerpt = raw
      paragraph.clear()

    def flush_bullets() -> None:
        if not bullets:
            return
        html_parts.append("<ul>" + "".join(f"<li>{render_inline(item)}</li>" for item in bullets) + "</ul>")
        bullets.clear()

    def flush_ordered() -> None:
        if not ordered_items:
            return
        html_parts.append("<ol>" + "".join(f"<li>{render_inline(item)}</li>" for item in ordered_items) + "</ol>")
        ordered_items.clear()

    def flush_quote() -> None:
        if not quote_lines:
            return
        html_parts.append("<blockquote>" + "<br>".join(render_inline(item) for item in quote_lines) + "</blockquote>")
        quote_lines.clear()

    def flush_math() -> None:
        if not math_lines:
            return
        html_parts.append(f"<div class=\"math-block\">$${escape(chr(10).join(math_lines))}$$</div>")
        math_lines.clear()

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            flush_quote()
            flush_math()
            if in_code:
                html_parts.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            continue

        if stripped == "$$":
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            flush_quote()
            if in_math:
                flush_math()
                in_math = False
            else:
                in_math = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if in_math:
            math_lines.append(line)
            continue

        if not stripped:
            flush_paragraph()
            flush_quote()
            flush_math()
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            flush_ordered()
            flush_quote()
            bullets.append(stripped[2:])
            continue

        ordered_match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if ordered_match:
            flush_paragraph()
            flush_bullets()
            flush_quote()
            ordered_items.append(ordered_match.group(1))
            continue

        if re.fullmatch(r"---+", stripped):
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            flush_quote()
            flush_math()
            html_parts.append("<hr>")
            continue

        if stripped.startswith("> "):
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            quote_lines.append(stripped[2:])
            continue

        match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if match:
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            flush_quote()
            flush_math()
            level = len(match.group(1))
            content = render_inline(match.group(2))
            plain = match.group(2).strip()
            if not title and level == 1:
                title = plain
            html_parts.append(f"<h{level}>{content}</h{level}>")
            continue

        paragraph.append(stripped)

    flush_paragraph()
    flush_bullets()
    flush_ordered()
    flush_quote()
    flush_math()

    if code_lines:
        html_parts.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")

    return "\n".join(html_parts), title, excerpt


def render_inline(text: str) -> str:
    math_store: list[str] = []

    def stash_math(match: re.Match[str]) -> str:
        math_store.append(match.group(0))
        return f"@@MATH{len(math_store) - 1}@@"

    protected = re.sub(r"\$\$(.+?)\$\$|\$(.+?)\$", stash_math, text)
    result = escape(protected)
    result = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", lambda m: f'<img src="{escape(m.group(2), quote=True)}" alt="{escape(m.group(1), quote=True)}">', result)
    result = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{escape(m.group(2), quote=True)}">{escape(m.group(1))}</a>', result)
    result = re.sub(r"`([^`]+)`", lambda m: f"<code>{escape(m.group(1))}</code>", result)
    result = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", result)
    result = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", result)
    for idx, math_text in enumerate(math_store):
        result = result.replace(f"@@MATH{idx}@@", escape(math_text))
    return result


def cpp_title(path: Path) -> str:
    try:
        first = path.read_text(encoding="utf-8").splitlines()[0].strip()
    except Exception:
        first = ""
    if first.startswith("//"):
        return first[2:].strip()
    return path.stem


def collect_entries() -> list[Entry]:
    notes = {}
    for path in NOTES_DIR.rglob("*.md"):
        key = path.relative_to(NOTES_DIR).with_suffix("").as_posix()
        notes[key] = path

    codes = {}
    for ext in ("*.cpp", "*.cc", "*.cxx"):
        for path in CODE_DIR.rglob(ext):
            key = path.relative_to(CODE_DIR).with_suffix("").as_posix()
            codes[key] = path

    keys = sorted(set(notes) | set(codes))
    entries: list[Entry] = []

    for key in keys:
        note_path = notes.get(key)
        code_path = codes.get(key)

        note_html = "<p class=\"muted\">还没有对应题解，后面可以把 Markdown 放进来。</p>"
        title = Path(key).name.replace("-", " ").replace("_", " ").title()
        excerpt = "把这道题的思路、坑点和复杂度分析写在对应的 Markdown 里。"

        if note_path:
            note_text = note_path.read_text(encoding="utf-8")
            note_html, md_title, md_excerpt = markdown_to_html(note_text)
            if md_title:
                title = md_title
            if md_excerpt:
                excerpt = md_excerpt

        code_text = code_path.read_text(encoding="utf-8") if code_path else None
        slug = slugify(key)

        entries.append(
            Entry(
                slug=slug,
                title=title,
                note_html=note_html,
                excerpt=excerpt,
                note_path=note_path.relative_to(ROOT).as_posix() if note_path else None,
                code_path=code_path.relative_to(ROOT).as_posix() if code_path else None,
                code_text=code_text,
            )
        )

    return entries


def collect_contest_entries() -> list[ContestEntry]:
    contests: list[ContestEntry] = []
    if not ABC_DIR.exists():
        return contests

    contest_ids = set()
    for path in ABC_DIR.iterdir():
        if path.is_dir() and path.name.isdigit():
            contest_ids.add(path.name)
    for path in ABC_NOTES_DIR.glob("*.md"):
        if path.stem.isdigit():
            contest_ids.add(path.stem)

    for contest_id in sorted(contest_ids):
        note_path = ABC_NOTES_DIR / f"{contest_id}.md"
        note_html = None
        note_title = None
        note_excerpt = "这一场暂时还没有题解，但代码已经保留下来了。"
        note_path_str = None

        if note_path.exists():
            html, title, excerpt = markdown_to_html(note_path.read_text(encoding="utf-8"))
            note_html = html
            note_title = title or f"AtCoder Beginner Contest {contest_id}"
            note_excerpt = excerpt or note_excerpt
            note_path_str = note_path.relative_to(ROOT).as_posix()

        codes: list[ContestCode] = []
        code_dir = ABC_DIR / contest_id
        if code_dir.exists():
            for ext in ("*.cpp", "*.cc", "*.cxx"):
                for path in sorted(code_dir.glob(ext)):
                    codes.append(
                        ContestCode(
                            filename=path.name,
                            path=path.relative_to(ROOT).as_posix(),
                            title=cpp_title(path),
                            code_text=path.read_text(encoding="utf-8"),
                            slug=slugify(f"{contest_id}-{path.stem}"),
                        )
                    )

        contests.append(
            ContestEntry(
                contest_id=contest_id,
                title=note_title or f"AtCoder Beginner Contest {contest_id}",
                slug=f"abc-{contest_id}",
                note_html=note_html,
                note_title=note_title,
                note_excerpt=note_excerpt,
                note_path=note_path_str,
                codes=codes,
            )
        )

    return contests


def layout(title: str, body: str, home_href: str, archive_href: str, nav_right: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <style>{SITE_CSS}</style>
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }},
      svg: {{
        fontCache: 'global'
      }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
  <div class="page-transition" aria-hidden="true"></div>
  <div class="wrap">
    <div class="shell">
      <header class="nav">
        <a class="brand" href="{home_href}">
          <div class="brand-mark">Y</div>
          <div class="brand-text">
            <strong>Yunayu ACM</strong>
            <span>Code & Notes</span>
          </div>
        </a>
        <nav class="nav-links">
          <a href="{home_href}">Home</a>
          <a href="{archive_href}">Archive</a>
          {nav_right}
        </nav>
      </header>
      {body}
      <footer class="footer">Static archive for ACM solutions and markdown editorials.</footer>
    </div>
  </div>
  <script>
    document.body.classList.add("is-entering");
    window.requestAnimationFrame(() => {{
      document.body.classList.remove("is-entering");
    }});

    const internalLinks = Array.from(document.querySelectorAll('a[href]')).filter((link) => {{
      const href = link.getAttribute("href");
      return href && !href.startsWith("#") && !href.startsWith("http") && !link.hasAttribute("download");
    }});

    internalLinks.forEach((link) => {{
      link.addEventListener("click", (event) => {{
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        document.body.classList.add("is-transitioning");
        window.setTimeout(() => {{
          window.location.href = link.href;
        }}, 180);
      }});
    }});
  </script>
</body>
</html>
"""


def index_layout(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <style>{SITE_CSS}</style>
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }},
      svg: {{
        fontCache: 'global'
      }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
  <div class="page-transition" aria-hidden="true"></div>
  <div class="wrap">
    <div class="shell">
      <header class="nav">
        <a class="brand" href="../index.html">
          <div class="brand-mark">Y</div>
          <div class="brand-text">
            <strong>Yunayu ACM</strong>
            <span>Code & Notes</span>
          </div>
        </a>
        <nav class="nav-links">
          <a href="../index.html">Home</a>
          <a class="pill" href="#entries">Problems</a>
        </nav>
      </header>
      {body}
      <footer class="footer">Put your files into <code>content/notes</code> and <code>content/code</code>, then rerun the builder.</footer>
    </div>
  </div>
  <script>
    document.body.classList.add("is-entering");
    window.requestAnimationFrame(() => {{
      document.body.classList.remove("is-entering");
    }});

    const internalLinks = Array.from(document.querySelectorAll('a[href]')).filter((link) => {{
      const href = link.getAttribute("href");
      return href && !href.startsWith("#") && !href.startsWith("http") && !link.hasAttribute("download");
    }});

    internalLinks.forEach((link) => {{
      link.addEventListener("click", (event) => {{
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        document.body.classList.add("is-transitioning");
        window.setTimeout(() => {{
          window.location.href = link.href;
        }}, 180);
      }});
    }});
  </script>
</body>
</html>
"""


def render_archive(entries: list[Entry]) -> str:
    cards = []
    for entry in entries:
        tags = []
        if entry.note_path:
            tags.append("<span class=\"tag\">Markdown Editorial</span>")
        if entry.code_path:
            tags.append("<span class=\"tag\">C++ Solution</span>")
        if not tags:
            tags.append("<span class=\"tag\">Placeholder</span>")

        cards.append(
            f"""
            <a class="card entry-card" href="problems/{entry.slug}.html">
              <div class="entry-main">
                <span class="eyebrow">Problem Entry</span>
                <h3 style="margin-top: 16px;">{escape(entry.title)}</h3>
                <p style="margin-top: 12px;">{escape(entry.excerpt[:160])}</p>
                <div class="tag-row">{''.join(tags)}</div>
              </div>
              <div class="entry-side">
                <p style="font-size: 0.92rem;">{escape(entry.note_path or 'No markdown yet')}</p>
                <p style="margin-top: 10px; font-size: 0.92rem;">{escape(entry.code_path or 'No code yet')}</p>
              </div>
            </a>
            """
        )

    body = f"""
    <section class="hero">
      <article class="card">
        <span class="eyebrow">ACM Archive</span>
        <h1>把题解和代码整理成一个真正能翻的题库。</h1>
        <p>这个页面会自动汇总 <code>content/notes</code> 和 <code>content/code</code> 下面的内容。题解和代码同名时会自动配成一条题目记录。</p>
        <div class="meta-grid">
          <div class="meta"><strong>{len(entries)}</strong><span>当前题目条目</span></div>
          <div class="meta"><strong>{sum(1 for item in entries if item.note_path)}</strong><span>Markdown 题解</span></div>
          <div class="meta"><strong>{sum(1 for item in entries if item.code_path)}</strong><span>C++ 代码</span></div>
        </div>
      </article>
      <article class="card">
        <h3>命名约定</h3>
        <p style="margin-top: 14px;">推荐把同一道题写成同名文件，比如 <code>content/notes/luogu-p1001.md</code> 和 <code>content/code/luogu-p1001.cpp</code>。这样站点会自动给它们做跳转和整合。</p>
        <div class="tag-row">
          <span class="tag">Luogu</span>
          <span class="tag">Codeforces</span>
          <span class="tag">AtCoder</span>
          <span class="tag">NOI / ICPC</span>
        </div>
      </article>
    </section>
    <section class="section" id="entries">
      <div class="section-head">
        <h2>Problem List</h2>
        <p>点击任意卡片可以进入题目详情页，里面会把题解和代码并排放在一起。</p>
      </div>
      <div class="entry-grid">
        {''.join(cards) if cards else '<article class="card"><h3>还没有条目</h3><p style="margin-top: 12px;">把你的文件放进 content 目录后重新生成，这里就会自动出现。</p></article>'}
      </div>
    </section>
    """
    return index_layout("Yunayu ACM Archive", body)


def render_detail(entry: Entry) -> str:
    code_html = (
        f"<pre class=\"code-block\"><code>{escape(entry.code_text)}</code></pre>"
        if entry.code_text
        else "<p class=\"muted\">还没有对应代码，后面可以在 content/code 里补上同名 C++ 文件。</p>"
    )
    body = f"""
    <section class="hero">
      <article class="card">
        <span class="eyebrow">Problem Detail</span>
        <h1>{escape(entry.title)}</h1>
        <p>{escape(entry.excerpt)}</p>
        <div class="tag-row">
          <span class="tag">{escape(entry.note_path or 'No markdown')}</span>
          <span class="tag">{escape(entry.code_path or 'No cpp')}</span>
        </div>
      </article>
        <article class="card">
          <h3>导航</h3>
          <p style="margin-top: 14px;">这个题目页会把 Markdown 题解和 C++ 代码放在同一页里，适合复习时横向对照。</p>
          <div class="tag-row">
          <a class="tag" href="../acm.html">返回题库</a>
          <a class="tag" href="../../index.html">返回首页</a>
          </div>
        </article>
      </section>
    <section class="section">
      <div class="section-head">
        <h2>Editorial & Code</h2>
        <p>左侧是题解内容，右侧是对应代码。你后面也可以继续扩成“多份代码对比”或“题目标签筛选”。</p>
      </div>
      <div class="detail-grid">
        <article class="card">
          <div class="toolbar">
            <h3>Markdown Editorial</h3>
            <span class="muted">{escape(entry.note_path or 'No markdown')}</span>
          </div>
          <div class="note">{entry.note_html}</div>
        </article>
        <article class="card side-panel">
          <div class="toolbar">
            <h3>C++ Solution</h3>
            <span class="muted">{escape(entry.code_path or 'No code')}</span>
          </div>
          {code_html}
        </article>
      </div>
    </section>
    """
    nav_right = '<a class="pill" href="../acm.html">Back</a>'
    return layout(
        f"{entry.title} | Yunayu ACM",
        body,
        home_href="../../index.html",
        archive_href="../acm.html",
        nav_right=nav_right,
    )


def render_contest_archive(contests: list[ContestEntry]) -> str:
    cards = []
    for contest in contests:
        tags = []
        tags.append(f'<span class="tag">{len(contest.codes)} 份代码</span>')
        tags.append(f'<span class="tag">{"有题解" if contest.note_path else "暂无题解"}</span>')
        cards.append(
            f"""
            <a class="card entry-card" href="contests/{contest.slug}.html">
              <div class="entry-main">
                <span class="eyebrow">Contest {escape(contest.contest_id)}</span>
                <h3 style="margin-top: 16px;">{escape(contest.title)}</h3>
                <p style="margin-top: 12px;">{escape(contest.note_excerpt[:170])}</p>
                <div class="tag-row">{''.join(tags)}</div>
              </div>
              <div class="entry-side">
                <p style="font-size: 0.92rem;">{escape(contest.note_path or 'No markdown')}</p>
                <p style="margin-top: 10px; font-size: 0.92rem;">{len(contest.codes)} code files</p>
              </div>
            </a>
            """
        )

    body = f"""
    <section class="hero">
      <article class="card">
        <span class="eyebrow">ABC Archive</span>
        <h1>按比赛编号整理你的 AtCoder 板刷记录。</h1>
        <p>这里会自动识别 <code>ABC板刷/042</code> 这样的比赛目录，也会把 <code>ABC板刷/云遥栈/042.md</code> 这种同编号题解挂到同一场比赛下。即使某一场缺题解或缺代码，也会保留对应页面。</p>
        <div class="meta-grid">
          <div class="meta"><strong>{len(contests)}</strong><span>比赛场次</span></div>
          <div class="meta"><strong>{sum(1 for item in contests if item.note_path)}</strong><span>已有题解的比赛</span></div>
          <div class="meta"><strong>{sum(len(item.codes) for item in contests)}</strong><span>总代码文件数</span></div>
        </div>
      </article>
      <article class="card">
        <h3>对应规则</h3>
        <p style="margin-top: 14px;">比赛编号一一对应，例如 <code>042</code> 会自动合并目录 <code>ABC板刷/042/</code> 与题解 <code>ABC板刷/云遥栈/042.md</code>。你不用强行保证每一题都同时存在题解和代码。</p>
        <div class="tag-row">
          <span class="tag">042 -> 042.md</span>
          <span class="tag">允许缺题解</span>
          <span class="tag">允许缺代码</span>
        </div>
      </article>
    </section>
    <section class="section" id="entries">
      <div class="section-head">
        <h2>Contest List</h2>
        <p>点进每一场比赛后，可以看到这一场的所有代码文件，以及对应的整场题解。</p>
      </div>
      <div class="entry-grid">
        {''.join(cards) if cards else '<article class="card"><h3>还没有比赛条目</h3><p style="margin-top: 12px;">把比赛目录放进 ABC板刷 后重新生成即可。</p></article>'}
      </div>
    </section>
    """
    return index_layout("Yunayu ABC Archive", body)


def render_contest_detail(contest: ContestEntry) -> str:
    note_html = contest.note_html or '<div class="hint">这一场暂时还没有题解 Markdown，但页面已经保留好了，之后补上 <code>ABC板刷/云遥栈/' + escape(contest.contest_id) + '.md</code> 就会自动显示。</div>'
    if contest.codes:
        code_links = []
        for code in contest.codes:
            code_links.append(
                f"""
                <a class="code-link" href="../contest-code/{code.slug}.html">
                  <div class="code-link-main">
                    <strong>{escape(code.filename)}</strong>
                    <span>{escape(code.title)}</span>
                  </div>
                  <div class="code-link-side">查看代码 →</div>
                </a>
                """
            )
        codes_html = '<div class="code-nav">' + "".join(code_links) + '</div>'
    else:
        codes_html = '<div class="hint">这一场目前没有检测到代码文件，但比赛页面已经建立好了。</div>'

    body = f"""
    <section class="hero">
      <article class="card">
        <span class="eyebrow">Contest Detail</span>
        <h1>{escape(contest.title)}</h1>
        <p>{escape(contest.note_excerpt)}</p>
        <div class="tag-row">
          <span class="tag">Contest #{escape(contest.contest_id)}</span>
          <span class="tag">{len(contest.codes)} code files</span>
          <span class="tag">{'Markdown ready' if contest.note_path else 'No markdown yet'}</span>
        </div>
      </article>
      <article class="card">
        <h3>导航</h3>
        <p style="margin-top: 14px;">左边是这场比赛对应的整场题解，右边是这一场目前收录到的所有 C++ 代码文件。</p>
        <div class="tag-row">
          <a class="tag" href="../abc.html">返回比赛列表</a>
          <a class="tag" href="../../index.html">返回首页</a>
        </div>
      </article>
    </section>
    <section class="section">
      <div class="section-head">
        <h2>Editorial</h2>
        <p>这里把整场题解作为主阅读内容来展示，代码不再直接铺在旁边，而是放到页面下方作为补充入口。</p>
      </div>
      <article class="card">
        <div class="toolbar">
          <h3>Markdown Editorial</h3>
          <span class="muted">{escape(contest.note_path or 'No markdown')}</span>
        </div>
        <div class="note">{note_html}</div>
      </article>
    </section>
    <section class="section">
      <div class="section-head">
        <h2>Code Index</h2>
        <p>如果你想看具体实现，可以从这里进入每一题的独立代码页。这样比赛页会更专注于题解本身。</p>
      </div>
      <article class="card">
        <div class="toolbar">
          <h3>C++ Files</h3>
          <span class="muted">{len(contest.codes)} files</span>
        </div>
        {codes_html}
      </article>
    </section>
    """
    return layout(
        f"{contest.title} | Yunayu ABC",
        body,
        home_href="../../index.html",
        archive_href="../abc.html",
        nav_right='<a class="pill" href="../abc.html">Back</a>',
    )


def render_contest_code_detail(contest: ContestEntry, code: ContestCode) -> str:
    body = f"""
    <section class="hero">
      <article class="card">
        <span class="eyebrow">Code Detail</span>
        <h1>{escape(code.filename)}</h1>
        <p>{escape(code.title)}</p>
        <div class="tag-row">
          <span class="tag">Contest #{escape(contest.contest_id)}</span>
          <span class="tag">{escape(code.path)}</span>
        </div>
      </article>
      <article class="card">
        <h3>导航</h3>
        <p style="margin-top: 14px;">这页只展示单个代码文件，适合在读完题解后再按题目查看具体实现。</p>
        <div class="tag-row">
          <a class="tag" href="../contests/{contest.slug}.html">返回比赛题解</a>
          <a class="tag" href="../abc.html">返回比赛列表</a>
        </div>
      </article>
    </section>
    <section class="section">
      <div class="section-head">
        <h2>Source Code</h2>
        <p>代码被单独放到了这一页，避免比赛题解正文被大段实现细节打断。</p>
      </div>
      <article class="card">
        <div class="toolbar">
          <h3>{escape(code.filename)}</h3>
          <span class="muted">{escape(code.path)}</span>
        </div>
        <pre class="code-block"><code>{escape(code.code_text)}</code></pre>
      </article>
    </section>
    """
    return layout(
        f"{code.filename} | {contest.title}",
        body,
        home_href="../../index.html",
        archive_href="../abc.html",
        nav_right=f'<a class="pill" href="../contests/{contest.slug}.html">Back</a>',
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PROBLEMS_DIR.mkdir(parents=True, exist_ok=True)
    CONTESTS_DIR.mkdir(parents=True, exist_ok=True)
    CONTEST_CODE_DIR.mkdir(parents=True, exist_ok=True)

    entries = collect_entries()
    contests = collect_contest_entries()

    (OUT_DIR / "acm.html").write_text(render_archive(entries), encoding="utf-8")
    (OUT_DIR / "abc.html").write_text(render_contest_archive(contests), encoding="utf-8")

    for existing in PROBLEMS_DIR.glob("*.html"):
        existing.unlink()
    for existing in CONTESTS_DIR.glob("*.html"):
        existing.unlink()
    for existing in CONTEST_CODE_DIR.glob("*.html"):
        existing.unlink()

    for entry in entries:
        (PROBLEMS_DIR / f"{entry.slug}.html").write_text(render_detail(entry), encoding="utf-8")
    for contest in contests:
        (CONTESTS_DIR / f"{contest.slug}.html").write_text(render_contest_detail(contest), encoding="utf-8")
        for code in contest.codes:
            (CONTEST_CODE_DIR / f"{code.slug}.html").write_text(
                render_contest_code_detail(contest, code),
                encoding="utf-8",
            )

    print(
        f"Built {len(entries)} standalone entries and {len(contests)} contest entries into {OUT_DIR.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
