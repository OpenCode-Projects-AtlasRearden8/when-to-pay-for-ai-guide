#!/usr/bin/env python3
"""Build the static HTML site from the docs/ markdown manual.

Usage:  python3 tools/build.py

Reads every .md file in docs/ (in explicit chapter order), converts it to a
styled HTML page in site/, rewriting internal .md links to .html. Requires
only the Python standard library plus the `markdown` package (GFM extras).
"""

import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

PAGE_ORDER = [
    "index.md",
    "01-free-tier-ceilings.md",
    "02-what-subscriptions-unlock.md",
    "03-decision-flow.md",
    "04-trial-checklists.md",
    "05-downgrade-with-dignity.md",
]

TITLES = {
    "index.md": "When to Pay for AI",
    "01-free-tier-ceilings.md": "Free-Tier Ceilings",
    "02-what-subscriptions-unlock.md": "What Subscriptions Actually Unlock",
    "03-decision-flow.md": "The Month-by-Month Decision Flow",
    "04-trial-checklists.md": "Trial Checklists",
    "05-downgrade-with-dignity.md": "Downgrade With Dignity",
}


def md_links_to_html(html: str) -> str:
    """Rewrite internal hrefs ending in .md to .html (leave absolute/external alone)."""
    def repl(m):
        href = m.group(1)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        return f'href="{href.rsplit(".md", 1)[0]}.html"'

    return re.sub(r'href="([^"]+\.md)"', repl, html)


def chapter_nav(current: str) -> str:
    items = []
    for name in PAGE_ORDER:
        page = name.removesuffix(".md") + ".html"
        label = TITLES[name]
        here = ' class="here"' if name == current else ""
        items.append(f'<li><a{here} href="{page}">{label}</a></li>')
    return "\n".join(items)


def pager(current: str) -> str:
    idx = PAGE_ORDER.index(current)
    left = center = right = ""
    if idx > 0:
        prev = PAGE_ORDER[idx - 1].removesuffix(".md") + ".html"
        left = f'<a href="{prev}">&larr; {TITLES[PAGE_ORDER[idx - 1]]}</a>'
    center = f'<a href="index.html">Contents</a>'
    if idx < len(PAGE_ORDER) - 1:
        nxt = PAGE_ORDER[idx + 1].removesuffix(".md") + ".html"
        right = f'<a href="{nxt}">{TITLES[PAGE_ORDER[idx + 1]]} &rarr;</a>'
    return left or " " , center, right or " "


def template(title: str, current: str, body: str) -> str:
    p_left, p_center, p_right = pager(current)
    brand = "Asdale Dynamics · The Massive AI Manual series"
    full_title = title if title == TITLES["index.md"] else f"{title} — When to Pay for AI"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A friendly manual for deciding when free AI tiers are enough, and when a subscription genuinely pays off. Free forever, no affiliate links.">
<title>{full_title}</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="site">
  <div class="brand">{brand}</div>
  <h1>When to Pay for AI</h1>
  <nav class="chapter" aria-label="Chapters">
    <ol>
{chapter_nav(current)}
    </ol>
  </nav>
</header>
<div class="wrap">
<main>
{body}
</main>
<footer class="site">
  <div class="pager">
    <span>{p_left}</span>
    <span>{p_center}</span>
    <span>{p_right}</span>
  </div>
  <div class="colophon">
    <p><em>When to Pay for AI</em> — a companion to <em>ai-model-picker-cli</em> (which helps you choose a model, not a plan).
    Free forever, no affiliate links. Prices and tier limits change often; always verify on the provider&#8217;s own pricing page.
    Education only, never professional advice.</p>
    <p>Copyright (c) 2026 Asdale Dynamics, LLC · MIT License</p>
  </div>
</footer>
</div>
</body>
</html>
"""


def task_boxes(md_text: str) -> str:
    """Render GFM-style `- [ ] ` checklist items with a checkbox glyph."""
    return re.sub(r"^(\s*)- \[ \] ", r"\1- ☐ ", md_text, flags=re.MULTILINE)


def build() -> None:
    SITE.mkdir(exist_ok=True)
    missing = [n for n in PAGE_ORDER if not (DOCS / n).exists()]
    if missing:
        sys.exit(f"Missing docs: {missing}")
    for name in PAGE_ORDER:
        md_text = (DOCS / name).read_text(encoding="utf-8")
        body = markdown.markdown(
            task_boxes(md_text),
            extensions=["extra", "sane_lists", "smarty"],
            output_format="html",
        )
        body = md_links_to_html(body)
        title = TITLES[name]
        out = SITE / (name.removesuffix(".md") + ".html")
        out.write_text(template(title, name, body), encoding="utf-8")
        print(f"built {out.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
