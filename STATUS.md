# STATUS.md — When to Pay for AI

**Status: complete and verified** (built 2026-11-03)

## What was built

A beginner-friendly manual for deciding when free AI tiers are enough (vs. when to subscribe), plus a static HTML site and a small build/test pipeline. Complements `ai-model-picker-cli` (that one picks a *model*; this one picks a *plan*).

- **`docs/` — the manual (Markdown, 6 pages):**
  - `index.md` — who it's for, how to use it, no-hype ground rules
  - `01-free-tier-ceilings.md` — the five ceilings: usage caps, model access, file/attachment limits, feature walls, peak-hour reliability
  - `02-what-subscriptions-unlock.md` — what paid tiers really buy (price buckets, five real unlocks) and the fine print they usually don't
  - `03-decision-flow.md` — the core routine: a one-note tally log, Weeks 1–4, gauntlets for staying free or trying paid, a 90-day loop
  - `04-trial-checklists.md` — a 7-day trial test plan with keep/cancel/downgrade rules and the three hygiene traps
  - `05-downgrade-with-dignity.md` — clean exits: billing timing, data evacuation, rebuilding a free workflow, no-shame framing
- **`site/` — static HTML website:** all six pages with shared `styles.css` (warm cream/amber palette), header chapter nav, footer prev/next pager, license colophon. Zero JavaScript, zero tracking.
- **`tools/build.py`** — converts `docs/*.md` → `site/*.html` (Python `markdown` package, GFM extras, checkbox-glyph preprocessing, internal `.md` → `.html` link rewriting).
- **`tests/test_pages.py`** — 15 unittest checks (runnable with `pytest` too).
- **`README.md`**, **`LICENSE`** (MIT), **`.markdownlint.json`** (line-length off, per house style).

## How to run it

```bash
python3 tools/build.py        # rebuild site/ from docs/
python3 tests/test_pages.py   # run the test suite (15 tests)
python3 -m pytest tests/ -q   # same suite under pytest
markdownlint docs README.md   # lint (optional)
```

Open `site/index.html` in a browser. No server required; everything is local.

## Verification results

- `python3 tools/build.py` — builds all 6 pages cleanly (re-runnable, idempotent).
- `python3 tests/test_pages.py` — **15/15 passed**: docs/site page parity (no strays), HTML well-formedness (tag-balance parser), every internal link in HTML and Markdown resolves, required boilerplate (charset, viewport, stylesheet, license line) present on every page, no affiliate/tracking-link markers, no secret/API-key patterns, LICENSE contains the exact required line, README credits the LLC, CSS brace-balance.
- `python3 -m pytest tests/ -q` — 15 passed.
- `markdownlint docs README.md` — no errors (after config + content fixes).
- Manual spot checks: checkbox glyphs render in checklist chapters, footnote-style nav and prev/next pager correct, title tags correct per page.

## Known gaps / limitations

- Prices and platform limits are deliberately hedged "rough buckets, as of late 2026" — no exact per-provider numbers are pinned, so the guide won't silently go stale. Reader is asked to verify on each provider's pricing page.
- No per-provider deep-dives (ChatGPT vs. Claude vs. Gemini pricing pages compared in detail) — deliberately out of scope to keep the guide evergreen and vendor-neutral; can be a separate chapter that's refreshed per release.
- The site is intentionally script-free: no printable-page CSS, dark mode, or search — candidates for later polish.
- `markdown` package (PyPI) is a runtime dependency of the build script only; the built site itself is fully static. Test suite is stdlib-only.
- Git history begins at this initial commit; no prior history exists.
