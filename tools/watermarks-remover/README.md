# Offline content Unicode hygiene

This directory vendors the Unicode inspection module (Layer A) from
[watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover/tree/5a62be6338d2812372b1da440e55c82922f97d53),
pinned to commit `5a62be6338d2812372b1da440e55c82922f97d53` under its MIT license.
The source is unmodified; `upstream.json` records its paths and SHA-256 hashes.
The CLI verifies those hashes before loading the module.

Only the Unicode module is integrated. The upstream server, agents, rewriting
providers, and file/media metadata removal are not installed. No API key,
external service, paid translation tool, or Python package installation is needed.
Python 3.10 or newer is required for these maintenance commands; the website's
build and production runtime do not depend on Python.

## Commands

Run from the repository root:

```sh
pnpm content:check
pnpm content:inspect > /tmp/yorix-unicode-report.json
pnpm test:content
```

Without pnpm, use `python3 -B scripts/content_unicode.py check` (or `inspect`).
Check and inspect never modify files. Check exits with status 1 when the Yorix
profile finds removable characters, 0 when clear, and 2 for CLI errors.
Inspect includes the upstream module's broader findings, including legitimate
directional controls and typography. Its warnings are not proof of a watermark.
Reports contain code points, counts and character offsets, rather than prose
snippets. The configured scope excludes credentials and legal documents.

After reviewing a finding, optional cleanup is available:

```sh
pnpm content:clean
git diff
pnpm content:check
```

Clean changes only files with findings, preserves their line endings and file
modes, and replaces them atomically. It does not make a backup; review the Git
diff before committing. Do not use it to approve a changed article automatically.

## Conservative multilingual profile

`scripts/content_unicode.py` uses upstream inspection and applies a narrower
Yorix profile. It removes raw U+FEFF byte-order marks, Unicode noncharacters,
reserved ignorables, and U+200B zero-width spaces. U+200B runs adjacent to Thai,
Lao, Khmer or Myanmar script are retained as possible word boundaries.

The profile retains accents, punctuation, ordinary and nonbreaking spaces,
soft hyphens, word joiners, Arabic/Indic ZWJ and ZWNJ, RTL controls, variation
selectors, emoji sequences, and private-use characters. It does not apply NFKC
normalization, replace lookalike letters, or paraphrase sentences.

`content-unicode.config.json` defines the content source files to scan, including
the site's locale dictionaries. Paths must stay inside the repository; symlinks
and files over 4 MiB are rejected. This checks **raw UTF-8 sources**: an ASCII
code escape such as `\u200B`, an HTML entity, or text fetched at runtime is not
decoded or assessed. Add new source locations explicitly when content moves.

The GitHub workflow runs regression tests and a read-only scan on pull requests
and pushes to `main` and `premium-web-payments`. It neither rewrites articles nor
publishes the website. The initial integration scan checked 30 content source
files and found no characters removable by this profile; article and translation
text was left unchanged.

## Limits and editorial policy

Unicode cleanup cannot remove a watermark encoded statistically in word choices.
The [primary technical announcement](https://www.anthropic.com/news/claude-text-watermark)
explicitly distinguishes that mechanism from hidden characters. This integration
does not detect or claim to erase statistical watermarks or establish authorship.

There is no promised ranking benefit. Google's
[guidance for generative content](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content)
and [helpful content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
focus on useful, reliable content. Keep source citations, review medical claims,
and improve articles for readers; do not treat an invisible-character scan as
an editorial or SEO quality score.

## Updating the vendor

Review the upstream changes first. Copy only the reviewed module and license,
preserving the license notice, then update the pinned commit and checksums in
`upstream.json`. Run the multilingual preservation and file-safety tests and the
read-only repository scan. Never fetch or execute a moving upstream revision
automatically during a build or content edit.
