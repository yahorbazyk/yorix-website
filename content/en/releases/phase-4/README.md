# Phase 4: complete weekly snapshots and hub

Adds 11 weekly snapshots and `/baby-sleep-by-week`, a table of contents rather
than a competing weekly article. All 15 snapshots (including Phase 3 weeks 2,
6, 8 and 12) link to the hub and have previous/hub/next navigation. Week 1 has
no previous link; week 15 continues to `/4-month-old-sleep-schedule`.

The English library has **135 articles plus one hub** (136 documents). Both
sitemaps contain 496 URLs. `kind` separates articles from the hub in the
catalog; the supplied Article/BreadcrumbList JSON-LD is retained. The supplied
new snapshots use fact lists in place of tables, which the renderer preserves.
Guides nests the 15 weekly links beneath their hub instead of creating another
set of monthly schedule cards. No week-16+ or extra monthly routes are added.

`summary.json` records new paths, 40 existing source files changed, inbound
requirements, the 37 approved merge insertions/replacements and source hashes.
The eight-week-regression FAQ is updated in place. Merge 26 and Section D
(33–43) repeat Phase 3 FAQs and are skipped; the existing two-week-regression
answer is retained. The newborn overview receives its requested pointer.
Targets named only for cross-linking retain their article rather than receiving
an unrelated primary paste. Editorial route-management notes are omitted or
adapted for readers, with each change recorded; clinical figures and numbered
sources are preserved.

The release date is November 16, 2026 (Europe/Warsaw); older Published dates are
preserved. If publication moves, regenerate using the actual date:

```sh
python3 -B scripts/prepare-english-articles.py --date YYYY-MM-DD --release-phase 4 --release-date YYYY-MM-DD
pnpm run check
pnpm build
```

Validate source/schema/link/FAQ tests, TypeScript, production build, scoped
lint, rendered navigation for all 15 weeks, full technical SEO crawl and the
26-case browser-language check. After the authorized merge/deploy, verify
public pages and sitemap, then submit the sitemap and key indexing requests.
