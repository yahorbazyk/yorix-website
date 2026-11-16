# Phase 5: Batch 7

Adds 11 English articles and the new Batch 7 merge instructions, without
repeating the already-written earlier batches. The library now has 146 articles
plus the existing weekly hub (147 English documents); sitemaps have 507 URLs.

`summary.json` records 49 modified existing source files, 47 FAQ/pointer
insertions, inbound requirements and original source hashes. Earlier short
sections about eyes opening, sweating, eat–play–sleep, startle, new siblings and
daytime waking now point to the focused standalone guides. The full 1–15-week
navigation and language-preservation fixes remain in place.

Source corrections are explicitly recorded: the nap-waking draft misattributes
the formula Q&A to Health Canada; it is HealthyChildren.org (AAP), whose exact
official URL is added. The new rolling FAQs retain the both-directions
qualifier already in the site's cited AAP guidance. No clinical figures are
changed. The vaccination FAQ adds the supplied NHS inform and Lullaby Trust
sources, deduplicated against each target's existing source list. Internal
route-management notes are omitted/adapted for readers, with a receipt.

Release date: November 16, 2026 (Europe/Warsaw). Previous Published dates are
preserved. If publishing later, regenerate with the actual date:

```sh
python3 -B scripts/prepare-english-articles.py --date YYYY-MM-DD --release-phase 5 --release-date YYYY-MM-DD
pnpm run check
pnpm build
```

Validation: source/schema/link/FAQ tests, TypeScript, production build, rendered
document and weekly navigation checks, full technical SEO and 26 browser-language
scenarios. After the authorized merge, verify Workers Builds and changed public
pages, submit the sitemap and request indexing for key new articles.
