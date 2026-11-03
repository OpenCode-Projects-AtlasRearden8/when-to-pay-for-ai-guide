# When to Pay for AI

*A friendly manual for deciding when free AI tiers are enough — and when a subscription genuinely pays off.*

Part of the [Massive AI Manual](https://dylanasdale.github.io) family of guides by Dylan Asdale, explained "like a friend would": plain English, step by step, never condescending. This one answers the money question — it picks a **plan**, the way its CLI sibling **ai-model-picker-cli** picks a **model**.

## What's inside

- `docs/` — the manual in Markdown, five chapters:
  1. **Free-Tier Ceilings** — where free plans run out (usage caps, model access, file sizes, feature walls, peak-hour slowdowns)
  2. **What Subscriptions Actually Unlock** — what paying really buys, and the fine print it usually doesn't
  3. **The Month-by-Month Decision Flow** — a one-note log + weekly cadence that turns "should I pay?" into evidence
  4. **Trial Checklists** — a 7-day trial test plan with honest keep/cancel rules
  5. **Downgrade With Dignity** — clean, un-shameful exits, data evacuation, and how to re-pick habits that match the ceiling
- `site/` — the same manual as a static HTML website (built from `docs/`)
- `tools/build.py` — one-command site build
- `tests/test_pages.py` — page tests: HTML well-formedness, link integrity, no-affiliate and no-secrets checks

## How to run it

```bash
# Build the static site from docs/ (requires Python 3 with the `markdown` package)
python3 tools/build.py

# Run the test suite
python3 tests/test_pages.py
# or, if pytest is installed:
python3 -m pytest tests/ -v
```

Then open `site/index.html` in any browser. No server, no build dependencies beyond Python's `markdown`, no tracking scripts. Everything runs locally.

## House rules (this project's promises)

- **Free forever.** No paywalls on the guide itself.
- **No affiliate links, no referral codes, no tracking.** We name providers only to explain patterns, never to earn a commission.
- **Local-first.** The site is plain static HTML/CSS with zero scripts.
- **No secrets.** No API keys or personal data live in this repo.
- **Honest hedging.** AI pricing and limits change every few months; the chapters teach the *method* and flag numbers as "verify current."

## Credits

Created and maintained by **Asdale Dynamics, LLC** — Dylan Asdale's company for beginner-friendly AI education, books, and practical tools.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
