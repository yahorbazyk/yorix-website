# Approved English article package

The owner supplied `yorix-implementation-package.zip` and authorized site
changes and publication on November 15, 2026. The 51 files in `articles/`
are the unchanged Markdown sources; the Word duplicates are not needed by the
website. `articles-table.csv`, `link-check.csv` and `IMPLEMENTATION.md` retain
the supplied editorial brief and route inventory. Internal notes are never
rendered as article content.

Regenerate the Worker-compatible JSON and both public sitemaps with:

```sh
python3 scripts/prepare-english-articles.py --date 2026-11-15
pnpm test:articles
```

Use the actual publication date for a future authorized update, rather than
changing dates automatically on every build. Existing publication dates come
from the preceding article data. The generated copies are checked against the
source, including its SHA-256 checksums. The compiler changes only publication
placeholders, hidden implementation notes and the technical metadata exception
specified by the brief for the four-month regression page.

## Scope

- 12 replaced English articles and 39 new English-only pages, including seven
  nested regression articles and the regression hub.
- Two retired slugs permanently redirect to their corresponding replacement
  in English and all 22 existing locales. Locale target text is unchanged.
- Existing translated article data remains in `app/article-localizations.ts`,
  `app/i18n/`, `app/content.ts` and `app/research-guides.ts`. The English
  renderer does not feed new prose into those fallback translations.
- The 51 owner-approved articles are released together, including development
  and feeding pages, so all 486 package links have a published destination.
  No expert-review byline or review claim is added by the implementation.
- Comparison article prices are the supplied, dated App Store comparisons;
  they do not change website checkout prices or the regional purchase gate.
- No article images have been added. Existing site branding and the shared
  Open Graph image are retained.

## Checks

`scripts/check-english-articles.py` checks the rendered 51 articles, JSON-LD,
dates, guide cards, all 46 permanent redirects, and missing-translation 404s.
`scripts/check-technical-seo.py` checks all 411 sitemap URLs and reciprocal
language links. Run the latter with `--public-only` on the real Cloudflare
host: country headers cannot be spoofed there for the local purchase-gate
simulation.

The inherited example-day template still appears on the Russian nap chart
(`/ru/baby-nap-schedule-by-age`). It is intentionally unchanged in this English
batch. New English pages render only their authored Markdown tables, with no
generated schedule blocks.

Internal article links use Next Link without automatic prefetch and with
`target="_top"` for normal document navigation. The pinned Vinext beta's RSC
prefetch and client-navigation exports fail in the production browser bundle.
Document navigation was verified by clicking both breadcrumbs and article-body
links in a production preview; it preserves real, crawlable hrefs and avoids
that framework path without changing site-wide routing or dependencies.
