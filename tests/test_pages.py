#!/usr/bin/env python3
"""Test suite for the When to Pay for AI guide.

Run with:  python3 tests/test_pages.py   (or: python3 -m pytest tests/)

Checks, per page:
- every docs/ chapter builds to a site/ page and vice versa (no strays)
- generated HTML is well-formed (all opened tags are closed, in order)
- every internal link/file reference resolves (md, html, css, image refs)
- required boilerplate is present (charset, viewport, stylesheet, license line)
Repo-wide:
- no affiliate/referral markers anywhere in committed files
- no obvious secrets (API key patterns) anywhere
- LICENSE contains the exact required copyright line
- README credits Asdale Dynamics, LLC
"""

import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"
LICENSE = ROOT / "LICENSE"
README = ROOT / "README.md"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}

CHAPTERS = [
    "01-free-tier-ceilings.md",
    "02-what-subscriptions-unlock.md",
    "03-decision-flow.md",
    "04-trial-checklists.md",
    "05-downgrade-with-dignity.md",
]


class WellFormednessChecker(HTMLParser):
    """HTMLParser-based tag-balance checker. Never resolves external refs."""

    def __init__(self, path: str):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag: str):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"{self.path}:{self.getpos()[0]} stray </{tag}>")
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.errors.append(
                f"{self.path}:{self.getpos()[0]} </{tag}> closes <{open_tag}> (opened line {line})")

    def close(self):
        super().close()
        for open_tag, line in self.stack:
            self.errors.append(f"{self.path}:{line} <{open_tag}> never closed")


def local_refs(text: str):
    """Yield (source, target) for href/src links that look local."""
    for m in re.finditer(r'(?:href|src)="([^"]+)"', text):
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:#")) or target.startswith("http"):
            continue
        if target.startswith("#"):
            continue
        yield target


class TestDocs(unittest.TestCase):
    def test_expected_docs_exist(self):
        for name in ["index.md", *CHAPTERS]:
            self.assertTrue((DOCS / name).exists(), f"missing docs/{name}")

    def test_no_unexpected_md_files(self):
        found = {p.name for p in DOCS.glob("*.md")}
        expected = {"index.md", *CHAPTERS}
        self.assertEqual(found, expected, f"unexpected extra docs: {found - expected}")


class TestSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {
            "index.html": SITE / "index.html",
            **{c.removesuffix(".md") + ".html": SITE / (c.removesuffix(".md") + ".html")
               for c in CHAPTERS},
        }
        cls.cuda_fail = [str(p) for p in cls.pages.values() if not p.exists()]
        if cls.cuda_fail:
            raise unittest.SkipTest(
                f"site pages missing (run `python3 tools/build.py` first): {cls.cuda_fail}")

    def test_no_stray_generated_pages(self):
        html_pages = {p.name for p in SITE.glob("*.html")}
        extra = html_pages - set(self.pages)
        self.assertFalse(extra, f"unexpected extra pages in site/: {extra}")

    def test_html_is_well_formed(self):
        for name, path in self.pages.items():
            parser = WellFormednessChecker(name)
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()
            self.assertEqual(parser.errors, [], f"malformed HTML in {name}")

    def test_every_page_has_required_boilerplate(self):
        for name, path in self.pages.items():
            text = path.read_text(encoding="utf-8")
            self.assertIn('<meta charset="utf-8">', text, name)
            self.assertIn('name="viewport"', text, name)
            self.assertIn('href="styles.css"', text, name)
            self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", text, name)

    def test_site_links_all_resolve(self):
        for name, path in self.pages.items():
            text = path.read_text(encoding="utf-8")
            for target in local_refs(text):
                self.assertTrue(
                    (SITE / target).exists(), f"{name} links to missing '{target}'")

    def test_css_referenced_exists(self):
        self.assertTrue((SITE / "styles.css").exists())

    def test_css_is_balanced(self):
        css = (SITE / "styles.css").read_text(encoding="utf-8")
        braces = css.count("{") - css.count("}")
        self.assertEqual(braces, 0, "unbalanced braces in styles.css")


class TestContentSafety(unittest.TestCase):
    FILE_PATTERNS = ["*.md", "site/*.html", "site/*.css", "tools/*.py"]

    ALL_TEXT = []

    @classmethod
    def setUpClass(cls):
        cls.ALL_TEXT = []
        for pattern in cls.FILE_PATTERNS:
            for path in ROOT.glob(pattern):
                cls.ALL_TEXT.append(
                    (str(path.relative_to(ROOT)), path.read_text(encoding="utf-8")))

    def test_no_affiliate_markers(self):
        # Prose may honestly say "no affiliate links"; we only flag link-shaped markers.
        affiliate_url_re = re.compile(
            r"amzn\.to|utm_[a-z]+|/\?tag=|[?&](ref|affid|aff|aid|cid)=",
            re.IGNORECASE,
        )
        # The prose must contain promo clauses — that's on the list.
        affiliate_link_words_re = re.compile(
            r"\]\([^)\s]*(affiliat|referral|shareasale|impact\.com|partnerize)[^)]*\)",
            re.IGNORECASE,
        )
        for name, text in self.ALL_TEXT:
            self.assertIsNone(affiliate_url_re.search(text),
                              f"possible affiliate URL marker in {name}")
            self.assertIsNone(affiliate_link_words_re.search(text),
                              f"possible affiliate/referral link in {name}")

    def test_no_ext_links_with_query_referrers(self):
        http_re = re.compile(r'https?://[^\s"\'<>]+\?[^\s"\'<>]*(utm_|tag=|ref=|affid|\bid=)', re.I)
        for name, text in self.ALL_TEXT:
            self.assertIsNone(http_re.search(text),
                              f"external link with tracking params in {name}")

    def test_no_obvious_secrets(self):
        secret_re = re.compile(
            r"(sk-[A-Za-z0-9]{20,}| AIzaSy[A-Za-z0-9_-]{30,}|"
            r"xox[bap]-[A-Za-z0-9-]{10,}|ghp_[A-Za-z0-9]{30,}|"
            r"AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
        for name, text in self.ALL_TEXT:
            self.assertIsNone(secret_re.search(text), f"possible secret in {name}")


class TestMeta(unittest.TestCase):
    def test_license_exact_copyright_line(self):
        text = LICENSE.read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", text)

    def test_license_is_mit(self):
        text = LICENSE.read_text(encoding="utf-8")
        self.assertIn("MIT License", text)

    def test_readme_credits_asdale(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", text)

    def test_md_internal_links_resolve(self):
        link_re = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
        for path in sorted(DOCS.glob("*.md")) + [README]:
            base = path.parent
            for target in link_re.findall(path.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://")):
                    continue
                self.assertTrue((base / target).exists(),
                                f"{path.name} links to missing '{target}'")


if __name__ == "__main__":
    unittest.main(verbosity=2)
