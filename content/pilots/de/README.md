# German localization pilot

Imports all 20 approved German articles from the November 22 localization
handoff: 12 replacements, five English pairs and three German-only topics.
Source Markdown is retained verbatim; the generated body and JSON-LD use the
actual publication date, November 23, 2026 (Europe/Berlin).

Rebuild with `python3 -B scripts/prepare-german-pilot.py --date YYYY-MM-DD`,
then `python3 -B scripts/prepare-english-articles.py --date YYYY-MM-DD`.
The shared sitemap generator adds the pilot URLs and reciprocal alternates.
German-only pages use self and x-default, without an invented English route.

Validation: TypeScript, 14 existing content tests, production build, all
20 rendered pages (headings, schema, tables, numbered source anchors), guide
cards, and all 529 HTML/XML alternate clusters. German regression routes
are intentionally not published in this pilot. English article bodies are
unchanged. Phase 0 was published separately in PR #11.
