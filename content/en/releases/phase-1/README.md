# Phase 1 release candidate

This candidate implements only Phase 1 of the owner-supplied MASTER handoff:
55 new English articles, approved Batch 3/5 merges, and Phase 1 inbound links.
The catalog has 106 English articles and the two equivalent sitemaps have 466 URLs.
No translated article, future-phase URL, new food page, price, checkout rule or
legal document is changed. The copied edit instructions include later phases for
reference; only Phase 1 sections have been applied to article sources.

`summary.json` records the 55 slugs, the 39 existing source files changed, and the
inbound link requirements. Raw Markdown remains in `content/en/articles`; existing
renderer and metadata helpers handle all new routes. The supplied broken local
anchor in `night-terrors.md` is corrected to match the rendered heading ID.

The original per-target edit inventory omits a `colic.md` file. Its approved
Phase 1 gas-at-night insertion is explicitly supplied in the
`edits/newborn-grunting-in-sleep.md` block and has been applied to `/colic`.
The shared app CTA is limited to sleep, feeding and symptoms tracking.

## Publication dates and approval

November 16, 2026 is the **candidate** release date, not a claim that these URLs
have already been published. Before approving the PR for a later release day,
regenerate using that actual calendar date in Europe/Warsaw:

```sh
python3 -B scripts/prepare-english-articles.py --date YYYY-MM-DD --phase-one-release-date YYYY-MM-DD
pnpm run check
pnpm build
```

Commit those generated changes to this feature branch before merge. The date
command updates new articles' Published/Updated dates and changed existing
articles' Updated dates; it preserves earlier publication dates and untouched
articles' dates. `publication-dates.json` is authoritative for reproducible builds.

Do not merge or push directly to `main` without owner approval of this PR.
After the approved deploy, run both rendered and technical SEO crawlers against
the public origin, check sitemap retrieval, and request indexing for key URLs.
Do not start Phase 2 until its Phase 1 link targets are live.

## Validation

- `pnpm run check`: analytics, TypeScript, Unicode hygiene and article tests.
- `pnpm build`: production Worker/client bundles.
- `python3 -B scripts/check-english-articles.py --base http://localhost:3003`:
  rendered articles, metadata, tables, schemas, anchors, merge redirects,
  guide cards and missing-translation 404s.
- `python3 -B scripts/check-technical-seo.py --base http://localhost:3003`:
  sitemap routes, canonical, hreflang, document language and regional gates.
- Lint: the changed renderer passes. Full lint has the same 49 pre-existing
  diagnostics as `origin/main`; this candidate introduces none.
