# Phase 2: Batch 6

Adds eight English articles from the MASTER handoff and applies all 24 Batch 6
merge items as 33 insertions on the named pages. `summary.json` records the new
slugs, 49 modified existing files, exact insertion locations and inbound-link
requirements. The catalog has 114 English articles; both sitemaps have 474 URLs.
No translation or future-phase article is introduced.

`approved-merges.md` retains the supplied Phase 2 instructions. Four internal
route-creation notes embedded in the supplied reader copy are omitted; their
exact text is recorded in `summary.json`. No medical numbers or guidance are
rewritten. Numbered source additions are deduplicated against existing citations.
Current official travel/weather, childcare and NICU source URLs are recorded in
the summary. The AAP/UK distinctions in the supplied text are retained.

Publication dates are the Europe/Warsaw release date, November 16, 2026. If this
phase is released later, regenerate before publishing:

```sh
python3 -B scripts/prepare-english-articles.py --date YYYY-MM-DD --release-phase 2 --release-date YYYY-MM-DD
pnpm run check
pnpm build
```

The owner explicitly authorized automatic publication after Phase 1. Keep one
PR per phase, wait for checks, merge, and verify Workers Builds plus public URLs.
Phase 3 must not ship before these targets are live.
