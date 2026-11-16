# Implementation checklist (tick per phase)

Work **one phase at a time** on a feature branch, then open a pull request. Do not push straight to `main`. Do not start a later phase until the earlier URLs that phase links to are live (or included in the same PR if you ship two phases together — still keep the order inside the PR).

Dates: set Published / Updated and JSON-LD `datePublished` / `dateModified` to the **real publish date** (Europe/Warsaw). Do not leave `[YYYY-MM-DD]` or `[Month DD, YYYY]` placeholders on the live site.

hreflang: new pages are **English only**. Point `en` (and `x-default` only if that is already site policy) at the English URL. **Do not** invent hreflang targets for the other 21 locales until a real translated page exists.

JSON-LD: `Article` + `BreadcrumbList` only. **No `FAQPage`.**

Food pages stay postponed. `/foods` is not in this ship.

## Every phase (repeat)

- [ ] Feature branch created (see `MASTER-INSTRUCTIONS.md` for names)
- [ ] New article files added in the same location/pattern as a live guide (infer from the repo; implement from the `.md`, not the `.docx`)
- [ ] Front matter mapped (`title`, `meta_description`, `canonical`); do not render `meta_*_character_count`, `primary_query`, or `secondary_queries`
- [ ] Real dates filled in the byline and JSON-LD
- [ ] Related reading / in-body links: only to URLs that are already live or are in this phase (see `reference/deferred-links.csv`)
- [ ] Edits in `edits/` for this phase applied (skip superseded blocks; skip weeks FAQ duplicates already pasted in Phase 3)
- [ ] Inbound links for this phase added on existing pages
- [ ] New slugs added to `/guides` in a sensible group
- [ ] `sitemap.xml` updated with lastmod = publish date
- [ ] Build and lint pass
- [ ] PR opened; no direct push to `main`
- [ ] After merge/deploy: each new URL returns 200
- [ ] JSON-LD present and valid (`Article` + `BreadcrumbList`, no `FAQPage`)
- [ ] Sitemap includes the new URLs
- [ ] Google Search Console: submit the sitemap; request indexing for the key pages in this phase

## Phase 1 — Batches 1–5 (55 new articles)

- [ ] All 55 Phase 1 URLs published
- [ ] Batch 3 MERGE pastes applied (4-to-3 nap transition, catnapping, standing in the crib, gas at night, smiling/laughing in sleep)
- [ ] Batch 5 MERGE pastes applied (crib standards, “second night”, nap training)
- [ ] Phase 1 inbound links added
- [ ] Do **not** also publish `/baby-snoring` or `/baby-sleeping-with-mouth-open`

## Phase 2 — Batch 6 (8 new articles)

- [ ] All 8 Phase 2 URLs published
- [ ] Batch 6 MERGE pastes applied (see `edits/`; 24 original pastes)
- [ ] Phase 2 inbound links added
- [ ] Fixed typo routes if you see them in older notes: `/teething-and-sleep` → `/teething-symptoms`; `/separation-anxiety-at-night` → `/separation-anxiety-and-sleep`

## Phase 3 — Expansion pilot (10 new articles)

- [ ] Weeks 2, 6, 8, 12 snapshots plus `/6-week-sleep-regression`, `/8-week-old-short-naps`, `/12-week-old-false-starts`, `/can-a-newborn-sleep-too-much`, `/why-does-my-baby-wake-up-at-4am`, `/why-is-my-baby-suddenly-sleeping-more`
- [ ] Pilot FAQ additions pasted onto the named existing pages
- [ ] Phase 3 inbound links added

## Phase 4 — Remaining weeks + hub (11 new articles + 1 hub)

- [ ] Weeks 1, 3, 4, 5, 7, 9, 10, 11, 13, 14, 15 published
- [ ] Hub `/baby-sleep-by-week` published from `hub/baby-sleep-by-week.md`
- [ ] Prev/next nav added on all 15 week pages (spec in `hub/WEEK-NAV.md`); week 15 next = `/4-month-old-sleep-schedule`
- [ ] Prev/next + hub link added on the four Phase 3 week pages if missing
- [ ] Weeks MERGE pastes applied; **skip Section D FAQ rows already pasted in Phase 3**
- [ ] Do **not** publish week 16–52 URLs or new 13–24 month schedule URLs
- [ ] Phase 4 inbound links added (month overviews → week snapshots)

## Phase 5 — Batch 7 (11 new articles)

- [ ] All 11 Phase 5 URLs published
- [ ] Batch 7 new MERGE pastes applied (skip Section B “already written”)
- [ ] Phase 5 inbound links added
- [ ] Add pointers from earlier short sections to the new standalone pages (eyes open, sweating, startle, eat–play–sleep, fight sleep, etc.)

## Phase 6 — Batch 8 (2 new articles)

- [ ] `/breastfed-vs-formula-fed-sleep` and `/baby-hiccups-and-sleep` published
- [ ] Batch 8 MERGE pastes applied **except items 5–7** (blackout, mattress firmness, pack-and-play) — those are superseded in Phase 7. If you are shipping Phase 6 and 7 close together, you may skip 5–7 entirely and go straight to the Phase 7 shrinks.
- [ ] Phase 6 inbound links added

## Phase 7 — Batch 9 (8 new articles + shrink-and-link)

- [ ] All 8 Phase 7 URLs published (pack-and-play, swings/bouncers, positioners/loungers, darkness, monitors, humidifiers, crib mattress, cribs/bassinets/bedside sleepers)
- [ ] Shrink-and-link edits applied the same day (or immediately after)
- [ ] If Batch 8 items 5–7 were already pasted, **replace** them with the shorter linked versions
- [ ] Phase 7 inbound (including optional related-reading bullets) added
- [ ] Do **not** publish a second white-noise, TOG, or swaddle-types URL

## Phase 8 — Batch 10 (4 new articles + shrink-and-link)

- [ ] All 4 Phase 8 URLs published (lovey, sleepwalking/talking, bedwetting, developmental leaps)
- [ ] Shrink-and-link edits applied the same day
- [ ] Two MERGE pastes applied (ear-infection FAQ on `/sick-baby-sleep`; baby-massage note on `/bedtime-routine-for-baby`)
- [ ] Phase 8 inbound (including optional pointers) added
- [ ] Do not rewrite week-by-week articles around Wonder Weeks

## Phase 9 — Optional Lighthouse fixes (not content)

Do this in its own PR. It is not required to publish the articles.

- [ ] Header App Store icon-only link: add a visible or at least programmatically available name (`aria-label`, e.g. “Download on the App Store”)
- [ ] Article download CTA contrast: white on `#6366F1` is about **4.46:1** (below the 4.5:1 AA minimum) — darken the purple until contrast is at least 4.5:1
- [ ] Homepage images are oversized (~400 KB extra); compress / serve modern sizes so LCP moves toward 2.5 s (it was about 3.1 s on a phone)
- [ ] Star-rating control: add correct ARIA (name, role, and current value) so the rating is announced
- [ ] Language switcher: add an `aria-label` (e.g. “Choose language”)
- [ ] Console RSC / Next.js prefetch error on article pages: fix or remove the bad prefetch so the console is clean (SEO is not affected, but it should be fixed)
- [ ] Re-run Lighthouse on the homepage and one article (phone) and keep SEO at 100

## Final count check

- [ ] English article URLs total **160** (51 already live + 109 new). Hub `/baby-sleep-by-week` is a 161st URL but is **not** in the 160.
- [ ] No slug collisions with the live 51
- [ ] No week 16+ or extra month-factory URLs
