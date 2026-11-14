# Optional GA4 website measurement

## Created in Google Analytics

- Account: Alexander (`258409724`).
- Property: `yorix-ai-baby-sleep-tracker` (`533997632`).
- Web stream: `Yorix website — yorix-app.com` (`16341022098`).
- Website: `https://yorix-app.com`.
- Measurement ID: `G-NBZ2G9XC1E` (public; not a secret).
- Enhanced measurement is off; the site explicitly sends the events below.
- The existing iOS stream is unchanged.

The stream is created. Website code must still be deployed by the owner of
the Cloudflare account containing `yorix-website`. The Cloudflare account
currently accessible on this Mac (`79831376babc1d05eda908b16ccf680c`) contains
only the social automation Workers; do not create a replacement website there.
The site's domain setup script identifies account `d8fb623c7f273b6064d02b397751d0f5`.

## Runtime behavior

- The optional analytics prompt and settings button are localized in all 23
  site languages, including RTL. Accept and decline are both directly available.
- No Google analytics script, analytics request or consent ping is loaded
  before consent. The script loads only on `yorix-app.com`, never on previews.
- Consent is remembered for 180 days and can be changed through the settings
  button on any page. Withdrawal disables measurement, clears the two GA4
  cookies and reloads the page to unload the SDK.
- Only known public marketing routes are measured. Checkout, gift redemption,
  codes, unknown routes and legal documents are excluded.
- Events: `page_view`, one `scroll` at 90% per public page, and `app_store_click`
  for this app's App Store links. Sessions and approximate geography are GA4
  metrics derived from these visits; they are not custom events.
- Locations and links exclude query strings and fragments. Referrers from
  other sites retain only the origin; internal referrers retain only a known
  public path. This intentionally omits UTM campaign attribution.
- Advertising storage, advertising user data, personalization and Google
  signals are disabled. No account ID, form contents, diary data, payment
  information or gift codes are sent in event parameters.
- CSP keeps nonce-based `strict-dynamic` script protection; only Google's
  analytics transport endpoints are added to image/connect destinations.

The privacy policy is archived and updated in Russian and English, with its
edition changed to November 14, 2026. Article text, pricing, payment rules and
the other legal editions are unchanged.

## Check and publish

```sh
pnpm install --frozen-lockfile
node --experimental-strip-types --test scripts/analytics.test.mjs
./node_modules/.bin/tsc --noEmit
pnpm build
```

Local preview deliberately sends no real analytics. Test the consent controls
there, including decline, changing the choice and RTL.

Verified locally: seven analytics tests, targeted lint, TypeScript, production
build, all 418 sitemap URLs, and browser consent controls in Russian and Arabic.
Existing locale copy and article content are unchanged apart from the new
analytics consent labels; archived legal files match the preceding commit.

From the existing authorized Cloudflare deployment environment:

```sh
git switch premium-web-payments
git pull --ff-only
NODE_OPTIONS=--dns-result-order=ipv4first pnpm run deploy
```

After publishing, open a public page, opt in and inspect GA4 Realtime / DebugView
or the browser's Google Analytics collection requests. Before opting in, and
after declining, there must be no analytics requests. Check the page URL and
click destination parameters contain no query strings or codes. Standard
reports populate after processing; an empty report before deployment is expected.
