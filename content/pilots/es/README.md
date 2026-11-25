# Spanish localization pilot

Imports all 30 approved neutral Spanish articles from the November 22
localization handoff: 12 replacements, 17 English pairs and one Spanish-only
topic. Source Markdown is retained verbatim; generated content and JSON-LD use
the actual publication date, November 24, 2026 (Europe/Minsk).

Rebuild with `python3 -B scripts/prepare-spanish-pilot.py --date YYYY-MM-DD`,
then `python3 -B scripts/prepare-english-articles.py --date YYYY-MM-DD`.
The nested source file `sleep-regression--4-months.md` is published at
`/es/sleep-regression/4-months`.

Wave 2 (phase `wave2`, published November 25, 2026) is rebuilt with
`python3 -B scripts/prepare-localized-batch.py --lang es --phase wave2 --date YYYY-MM-DD`.
