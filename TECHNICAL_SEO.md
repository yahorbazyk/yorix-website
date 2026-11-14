# Technical SEO maintenance

## November 14, 2026 batch

- Render the document language and direction from the URL on the server.
  Middleware overwrites the internal locale header, so a caller cannot change
  the document language independently of its path.
- Use one article metadata builder for English and localized routes. Each
  article publishes its own canonical URL and the same reciprocal language
  alternatives, including English and `x-default`.
- Publish reciprocal alternatives on the English guides index too.
- Keep readers on the corresponding article or guides index when switching
  languages, retaining the existing language-preference cookie behavior.
- Derive social preview metadata from each page's existing localized copy.
- Keep both existing sitemap aliases synchronized. Exclude the six regional
  storefront, offer and payment URLs; include all localized about and support
  pages and the two public terms-of-use pages. Keep existing modification
  dates; do not invent dates for the newly listed URLs.

The resulting maps each list 418 unique canonical URLs: 322 articles, 23 home
pages, 23 guides indexes, 46 about/support pages and four public legal pages.
The two aliases are retained for existing Search Console submissions and links.

Article data, translations, article body markup, prices, legal wording and
regional sales rules are unchanged.

## Verification

Run the type check and production build, then start that build locally:

```sh
./node_modules/.bin/tsc --noEmit
pnpm build
NODE_OPTIONS=--dns-result-order=ipv4first pnpm start --port 3002 --local
```

In another terminal:

```sh
python3 scripts/check-technical-seo.py --base http://localhost:3002
```

The standard-library-only checker validates both XML files and every listed
URL without following redirects. It checks canonical URLs, indexability,
document language/direction, reciprocal language alternatives, contextual
language switches and social metadata. It also checks that region-restricted
purchase pages still redirect outside supported countries, remain accessible
in Belarus, and do not restrict public legal or gift-redemption pages.

Stop the local server after checking. Deployment is a separate explicit action
under `AGENTS.md`; committing or pushing this batch does not deploy it.

## Search Console

The two XML sitemap submissions were already successful. The separate
`https://yorix-app.com/en/start` submission was removed on November 14 because
it is an HTML page, not a sitemap. This does not remove the page from the site
or request removal from search results.

Sitemap discovery and technically eligible pages do not guarantee indexing.
Recheck the published version after deployment before requesting a recrawl.
