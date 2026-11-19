# Phase 3: expansion pilot

Adds the ten approved pilot articles, including four week snapshots (2, 6, 8
and 12 weeks). Applies the pilot FAQ instructions as 13 insertions on existing
pages and adds Phase 3 inbound links. `summary.json` records the new slugs,
26 modified existing sources, inserted questions and original source hashes.

The English library has 124 articles. The two sitemaps each have 484 URLs.
The four snapshots are grouped as “Sleep by week” in Guides and ordered by age.
The full week hub and previous/next navigation belong to Phase 4 and are not
published early. No translation, food page, week-16+ URL or duplicate regression
URL is introduced. Existing language-navigation fixes remain in place.

The three pilot pages named as already containing their FAQ are not duplicated.
Supporting FAQ pointers use the destinations specified in the handoff rather
than copying the complete safety explanation. Four route-management notes are
omitted from reader copy; their exact wording is retained in the summary.
Medical figures, disclaimers and numbered sources are retained.

Published/Updated dates use November 16, 2026 (Europe/Warsaw). Prior publication
dates remain pinned. If publishing later, regenerate with the actual date:

```sh
python3 -B scripts/prepare-english-articles.py --date YYYY-MM-DD --release-phase 3 --release-date YYYY-MM-DD
pnpm run check
pnpm build
```

Validation: source/schema/link/FAQ tests, TypeScript, production build, rendered
article and technical SEO crawls, and the 26-case browser-language navigation
check. After the authorized automatic merge, verify Workers Builds and public
URLs, resubmit sitemap and request indexing for key pilot articles.
