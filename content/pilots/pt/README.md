# Brazilian Portuguese localization pilot

Imports all 30 approved Brazilian Portuguese articles from the November 22
localization handoff: 12 replacements, 14 English pairs and four Brazil-only
topics. Source Markdown is retained verbatim; the generated body and JSON-LD
use the actual publication date, November 24, 2026 (Europe/Minsk).

Rebuild with `python3 -B scripts/prepare-portuguese-pilot.py --date YYYY-MM-DD`,
then `python3 -B scripts/prepare-english-articles.py --date YYYY-MM-DD`.
Portuguese pages use `<html lang="pt-BR">`, while hreflang remains `pt`.
Portuguese-only pages use self and x-default without an invented English URL.

Wave 2 (phase `wave2`, published November 25, 2026) is rebuilt with
`python3 -B scripts/prepare-localized-batch.py --lang pt --phase wave2 --date YYYY-MM-DD`.
