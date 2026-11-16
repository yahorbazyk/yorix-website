# Yorix MASTER instructions — English sleep ship (ChatGPT / implementer)

Prepared 16 November 2026 (Europe/Warsaw). This is the **single combined handoff** of every unpublished English sleep article and every edit to existing pages, through Batch 10.

You have access to the Yorix GitHub repository and to Google Search Console. **Implement from the Markdown** in `articles/` and `hub/`. The `.docx` files are for the owner’s records only.

The site is Next.js: English routes are `https://yorix-app.com/<slug>`, other locales are `https://yorix-app.com/<lang>/<slug>`. Regression pages already use nested paths such as `/sleep-regression/4-months`. **Do not flatten those to a second slug** and do not invent `/en/` prefixes on English URLs.

**Currently live:** 51 English articles (listed in `reference/live-51.csv`). **In this zip:** 109 new English articles + the `/baby-sleep-by-week` hub. After this ship: **160** English articles, plus the hub as a table of contents (not a 161st competing article).

Food / complementary-feeding pages stay **postponed**. `/foods` was still 404 on 16 November 2026 and is not in this queue.

## Non-negotiable rules

1. **Repo workflow.** One feature branch and one pull request **per phase**. Do **not** push directly to `main` (or to any branch that auto-deploys production) without the owner’s explicit approval of that PR. Do not force-push. Do not rewrite article wording, numbers, or sources except for technical fixes (dates, routes, markup) and the packed `edits/` changes.
2. **Do not auto-translate.** These pages are English only.
3. **App-feature claims.** Yorix may be described as tracking **sleep, feeding, and symptoms** only. Do not claim food logging or other features.
4. **No expert-review flags.** Older batch notes (especially batches 1–5) may mention recommended or YMYL expert review. The standing instruction is: keep the standard medical disclaimer and numbered sources only. Do not add new “needs expert review” flags.
5. **JSON-LD:** paste the fenced json block into a script tag of type application/ld+json. **`Article` + `BreadcrumbList` only. No `FAQPage` schema.** Visible FAQ HTML is required; the schema type is not.
6. **Dates.** Replace `[Month DD, YYYY]` in the byline and `[YYYY-MM-DD]` in JSON-LD with the **real publish date**. Use the same date for `datePublished` and `dateModified` on first publish. Use Europe/Warsaw calendar dates.
7. **hreflang.** New pages have no translations in this zip. Emit `en` (and `x-default` only if that is already site policy) pointing at the English canonical. **Do not** add `hreflang` to `/de/…`, `/es/…`, or any other locale that does not actually have this page yet.
8. **Canonical, title, description** come from front matter `title` / `meta_description` / `canonical`. Do **not** render `meta_title_character_count`, `meta_description_character_count`, `primary_query`, or `secondary_queries` in the HTML.
9. **Do not create URLs listed in `reference/do-not-publish.md`** (week 16–52, extra month factories, `/baby-snoring`, `/baby-sleeping-with-mouth-open`, a second white-noise page, food pages, and so on).
10. **Do not average source conflicts.** Where AAP / NHS / NSF / AASM / Red Nose disagree, the article already shows both sides. Keep that wording.

## How to add an article (infer paths from the repo)

The exact file location is not hardcoded here because it must match the live Next.js tree. **Open the repository and copy the pattern of a live English guide**, for example `/newborn-sleep-schedule` (flat slug) and `/sleep-regression/4-months` (nested slug). Typical things to look for: a `content/` or `app/` route, MDX/MD collection, a CMS schema, or a generated page that reads front matter.

Then, for each new slug in this phase:

1. Create the route/file the same way the live article is created.
2. Copy body structure: H1; byline “By the Yorix team”; Published/Updated; medical disclaimer; Short answer; key-number or routing table; H2s; visible FAQ; Yorix block; Related reading; numbered Sources; JSON-LD.
3. Set `canonical` to `https://yorix-app.com/<slug>` as already written in the Markdown (regression pages keep the nested path).
4. Fill real dates.
5. In **Related reading and in-body links**, include only targets that are already live or that you are publishing in **this same phase**. The Markdown in `articles/` is the **final** text and may contain later-phase links. Those later links are listed in `reference/deferred-links.csv` and in section A of the source page’s `edits/<slug>.md`. Omit them on first publish; add them when the target phase goes live so the page ends up matching the final Markdown.
6. Add the slug to the `/guides` hub, in a group with related live pages. Week URLs go under `/baby-sleep-by-week`, not as a second set of month schedules.
7. Add the slug to `sitemap.xml` with `lastmod` equal to the publish date.

## Phase order (do not skip ahead)

Later packs link back to earlier URLs. Publish in this order. You may combine two adjacent phases in one PR only if every earlier URL in that PR is included and internal links are consistent; prefer **one PR per phase**.

| Phase | What to publish | New article count | Edits |
| ---: | --- | ---: | --- |
| 1 | Batches 1–5 | 55 | Batch 3 and Batch 5 MERGE pastes + Phase 1 inbound links |
| 2 | Batch 6 | 8 | Batch 6 MERGE pastes (24) + Phase 2 inbound |
| 3 | Expansion pilot | 10 | Pilot FAQ additions + Phase 3 inbound |
| 4 | Remaining weeks + hub `/baby-sleep-by-week` | 11 articles + 1 hub | Weeks MERGE pastes (skip FAQ rows already done in Phase 3); prev/next nav; Phase 4 inbound |
| 5 | Batch 7 | 11 | Batch 7 MERGE pastes (skip “already written” Section B) + Phase 5 inbound |
| 6 | Batch 8 | 2 | Batch 8 MERGE pastes **except items 5–7** (see supersessions) + Phase 6 inbound |
| 7 | Batch 9 | 8 | Shrink-and-link the same day; replace any Batch 8 items 5–7 already pasted; Phase 7 inbound |
| 8 | Batch 10 | 4 | Shrink-and-link the same day; two extra MERGE pastes; Phase 8 inbound |
| 9 (optional) | Lighthouse accessibility / performance | 0 | Separate PR; see below |

Suggested branch names: `content/sleep-phase-1-batches-1-5`, `content/sleep-phase-2-batch6`, `content/sleep-phase-3-pilot`, `content/sleep-phase-4-weeks-hub`, `content/sleep-phase-5-batch7`, `content/sleep-phase-6-batch8`, `content/sleep-phase-7-batch9`, `content/sleep-phase-8-batch10`, `fix/lighthouse-a11y-perf`.

### Phase 1 slugs (55)

- `/18-month-old-sleep-schedule` — 18-month-old-sleep-schedule.md
- `/2-to-1-nap-transition` — 2-to-1-nap-transition.md
- `/2-year-old-sleep-schedule` — 2-year-old-sleep-schedule.md
- `/3-to-2-nap-transition` — 3-to-2-nap-transition.md
- `/3-year-old-sleep-schedule` — 3-year-old-sleep-schedule.md
- `/5-s-soothing-a-crying-baby` — 5-s-soothing-a-crying-baby.md
- `/baby-crying-in-sleep` — baby-crying-in-sleep.md
- `/baby-sleep-and-travel` — baby-sleep-and-travel.md
- `/baby-sleep-cues` — baby-sleep-cues.md
- `/baby-sleep-cycles` — baby-sleep-cycles.md
- `/baby-sleeping-in-car-seat` — baby-sleeping-in-car-seat.md
- `/baby-sleeping-on-stomach` — baby-sleeping-on-stomach.md
- `/baby-snoring-and-mouth-breathing` — baby-snoring-and-mouth-breathing.md
- `/baby-twitching-in-sleep` — baby-twitching-in-sleep.md
- `/baby-wont-nap` — baby-wont-nap.md
- `/baby-wont-sleep-in-crib` — baby-wont-sleep-in-crib.md
- `/bed-sharing-and-co-sleeping` — bed-sharing-and-co-sleeping.md
- `/bedtime-routine-for-baby` — bedtime-routine-for-baby.md
- `/crib-to-toddler-bed` — crib-to-toddler-bed.md
- `/daycare-and-baby-sleep` — daycare-and-baby-sleep.md
- `/daylight-saving-baby-sleep` — daylight-saving-baby-sleep.md
- `/fear-of-the-dark` — fear-of-the-dark.md
- `/gentle-sleep-training` — gentle-sleep-training.md
- `/how-much-sleep-does-a-baby-need` — how-much-sleep-does-a-baby-need.md
- `/how-to-dress-baby-for-sleep` — how-to-dress-baby-for-sleep.md
- `/how-to-swaddle-a-baby` — how-to-swaddle-a-baby.md
- `/naps-on-the-go` — naps-on-the-go.md
- `/newborn-day-night-confusion` — newborn-day-night-confusion.md
- `/night-lights-and-baby-sleep` — night-lights-and-baby-sleep.md
- `/night-terrors` — night-terrors.md
- `/night-weaning` — night-weaning.md
- `/nursing-to-sleep` — nursing-to-sleep.md
- `/overtired-baby` — overtired-baby.md
- `/pacifier-and-sleep` — pacifier-and-sleep.md
- `/preemie-sleep` — preemie-sleep.md
- `/reflux-and-baby-sleep` — reflux-and-baby-sleep.md
- `/reverse-cycling` — reverse-cycling.md
- `/safe-sleep-for-babies` — safe-sleep-for-babies.md
- `/self-soothing` — self-soothing.md
- `/separation-anxiety-and-sleep` — separation-anxiety-and-sleep.md
- `/should-you-wake-a-sleeping-baby` — should-you-wake-a-sleeping-baby.md
- `/siblings-sharing-a-room` — siblings-sharing-a-room.md
- `/sick-baby-sleep` — sick-baby-sleep.md
- `/sleep-associations` — sleep-associations.md
- `/sleep-sacks` — sleep-sacks.md
- `/toddler-bedtime-battles` — toddler-bedtime-battles.md
- `/toddler-wont-stay-in-bed` — toddler-wont-stay-in-bed.md
- `/twins-and-sleep` — twins-and-sleep.md
- `/when-can-baby-sleep-with-a-blanket` — when-can-baby-sleep-with-a-blanket.md
- `/when-do-babies-sleep-through-the-night` — when-do-babies-sleep-through-the-night.md
- `/when-do-toddlers-stop-napping` — when-do-toddlers-stop-napping.md
- `/when-to-move-baby-to-crib` — when-to-move-baby-to-crib.md
- `/when-to-move-baby-to-own-room` — when-to-move-baby-to-own-room.md
- `/why-wont-my-baby-sleep` — why-wont-my-baby-sleep.md
- `/witching-hour` — witching-hour.md

### Phase 2 slugs (8)

- `/4-year-old-sleep-schedule` — 4-year-old-sleep-schedule.md
- `/autism-and-sleep` — autism-and-sleep.md
- `/baby-head-banging-and-body-rocking` — baby-head-banging-and-body-rocking.md
- `/cluster-feeding` — cluster-feeding.md
- `/melatonin-and-childrens-sleep` — melatonin-and-childrens-sleep.md
- `/responsive-settling` — responsive-settling.md
- `/sleep-after-separation-or-divorce` — sleep-after-separation-or-divorce.md
- `/teeth-grinding-in-sleep` — teeth-grinding-in-sleep.md

### Phase 3 slugs (10)

- `/12-week-old-baby-sleep` — 12-week-old-baby-sleep.md
- `/12-week-old-false-starts` — 12-week-old-false-starts.md
- `/2-week-old-baby-sleep` — 2-week-old-baby-sleep.md
- `/6-week-old-baby-sleep` — 6-week-old-baby-sleep.md
- `/6-week-sleep-regression` — 6-week-sleep-regression.md
- `/8-week-old-baby-sleep` — 8-week-old-baby-sleep.md
- `/8-week-old-short-naps` — 8-week-old-short-naps.md
- `/can-a-newborn-sleep-too-much` — can-a-newborn-sleep-too-much.md
- `/why-does-my-baby-wake-up-at-4am` — why-does-my-baby-wake-up-at-4am.md
- `/why-is-my-baby-suddenly-sleeping-more` — why-is-my-baby-suddenly-sleeping-more.md

### Phase 4 slugs (11) and hub

- `/1-week-old-baby-sleep` — 1-week-old-baby-sleep.md
- `/10-week-old-baby-sleep` — 10-week-old-baby-sleep.md
- `/11-week-old-baby-sleep` — 11-week-old-baby-sleep.md
- `/13-week-old-baby-sleep` — 13-week-old-baby-sleep.md
- `/14-week-old-baby-sleep` — 14-week-old-baby-sleep.md
- `/15-week-old-baby-sleep` — 15-week-old-baby-sleep.md
- `/3-week-old-baby-sleep` — 3-week-old-baby-sleep.md
- `/4-week-old-baby-sleep` — 4-week-old-baby-sleep.md
- `/5-week-old-baby-sleep` — 5-week-old-baby-sleep.md
- `/7-week-old-baby-sleep` — 7-week-old-baby-sleep.md
- `/9-week-old-baby-sleep` — 9-week-old-baby-sleep.md

- `/baby-sleep-by-week` — from `hub/baby-sleep-by-week.md`. Prev/next spec: `hub/WEEK-NAV.md`.

### Phase 5 slugs (11)

- `/baby-sleeping-with-eyes-open` — baby-sleeping-with-eyes-open.md
- `/baby-sweating-in-sleep` — baby-sweating-in-sleep.md
- `/eat-play-sleep` — eat-play-sleep.md
- `/is-sleep-training-harmful` — is-sleep-training-harmful.md
- `/potty-training-and-sleep` — potty-training-and-sleep.md
- `/screens-and-toddler-sleep` — screens-and-toddler-sleep.md
- `/should-you-wake-a-baby-from-a-nap` — should-you-wake-a-baby-from-a-nap.md
- `/startle-reflex-and-sleep` — startle-reflex-and-sleep.md
- `/toddler-sleep-after-a-new-baby` — toddler-sleep-after-a-new-baby.md
- `/what-time-should-baby-go-to-bed` — what-time-should-baby-go-to-bed.md
- `/why-does-my-baby-fight-sleep` — why-does-my-baby-fight-sleep.md

### Phase 6 slugs (2)

- `/baby-hiccups-and-sleep` — baby-hiccups-and-sleep.md
- `/breastfed-vs-formula-fed-sleep` — breastfed-vs-formula-fed-sleep.md

### Phase 7 slugs (8)

- `/baby-monitors-and-safe-sleep` — baby-monitors-and-safe-sleep.md
- `/baby-swings-and-bouncers` — baby-swings-and-bouncers.md
- `/crib-mattress-safety` — crib-mattress-safety.md
- `/cribs-bassinets-and-bedside-sleepers` — cribs-bassinets-and-bedside-sleepers.md
- `/how-dark-should-babys-room-be` — how-dark-should-babys-room-be.md
- `/humidifiers-and-baby-sleep` — humidifiers-and-baby-sleep.md
- `/pack-and-play-sleep` — pack-and-play-sleep.md
- `/sleep-positioners-and-loungers` — sleep-positioners-and-loungers.md

### Phase 8 slugs (4)

- `/bedwetting-and-sleep` — bedwetting-and-sleep.md
- `/developmental-leaps-and-baby-sleep` — developmental-leaps-and-baby-sleep.md
- `/sleepwalking-and-sleep-talking` — sleepwalking-and-sleep-talking.md
- `/when-can-baby-have-a-lovey` — when-can-baby-have-a-lovey.md

## Edits to existing pages

All MERGE pastes, shrink-and-link replacements, and inbound-link additions are **consolidated per target page** in `edits/`.

- Start with `edits/_INDEX.md` (one row per target).
- Open `edits/<slug>.md` for that page. Apply blocks **in phase order**.
- Read `edits/_CONFLICTS-AND-SUPERSESSIONS.md` before Phase 6–8. Where a later shrink replaces an earlier merge, the earlier text is folded under “do not paste” and the FINAL shrink text is the one to use.
- `edits/_INBOUND-LINKS-BY-PHASE.md` is the compact inbound table.

**Apply a phase’s edits after that phase’s new URLs exist** (or in the same PR, after the files are added). A MERGE that targets a page first published in an earlier phase should be applied in the MERGE’s own phase, not delayed until the end of the whole ship.

Paste onto the named heading; create the heading if it is missing. Add listed sources and renumber. Do not create the merged / skipped slugs as new URLs.

## Week hub and prev/next

See `hub/WEEK-NAV.md`. Publish the hub in Phase 4. Week 1 has no previous; week 15 next is `/4-month-old-sleep-schedule`. Add prev/next and the hub link on the four Phase 3 week pages (2, 6, 8, 12) if they are missing.

## Redirects

No new redirects are required for URLs that were never live.

- If you discover live thin URLs `/baby-snoring` or `/baby-sleeping-with-mouth-open`, redirect them to `/baby-snoring-and-mouth-breathing`.
- Keep any existing redirect from `/4-month-sleep-regression` to `/sleep-regression/4-months`. Do not publish the alias as a second page. New articles in this zip already use the canonical nested path (this was corrected in the handoff).
- Do not flatten `/sleep-regression/<age>` to a hyphenated flat slug, or the other way around.

## Sitemap, `/guides`, build, and Search Console

After each phase:

1. Add every new slug (including `/baby-sleep-by-week` in Phase 4) to `sitemap.xml` with `lastmod` = the publish date.
2. Add the new guides to `/guides`, grouped with related pages. Week URLs belong under the week hub.
3. Run the project’s build and lint (whatever the repo already uses, for example `npm run build` / `npm run lint`). Fix only implementation issues you introduced; do not drive-by refactor.
4. Open the PR, wait for the owner to approve and merge.
5. **Post-deploy checklist**
   - Each new URL returns **200** (not 404, not a locale-prefixed English duplicate).
   - View source: JSON-LD parses, contains `Article` and `BreadcrumbList`, does **not** contain `FAQPage`. Dates are real.
   - Canonical is `https://yorix-app.com/<slug>`.
   - `sitemap.xml` lists the new URLs.
   - In Google Search Console: submit (or resubmit) the sitemap. Request indexing for the key pages in that phase (safe-sleep and “how much sleep” in Phase 1; the week hub and a few week URLs in Phase 4; the eight gear guides in Phase 7; and any other high-intent slugs). You do not need to request indexing for every one of the 109 on day one, but do submit the sitemap so all of them can be discovered.

## Phase 9 (optional) — Lighthouse fixes

A phone Lighthouse run on 16 November 2026 scored **SEO 100** on both the homepage and a sample article (a 4-month schedule page). These are quality fixes, not a content requirement. Ship them in a separate PR (`fix/lighthouse-a11y-perf`):

1. **Header App Store icon.** The header control is an icon without an accessible name. Add `aria-label="Download on the App Store"` (or visible text).
2. **Article CTA contrast.** White text on `#6366F1` is about **4.46:1**, just under the WCAG AA 4.5:1 minimum. Darken the purple until contrast is at least 4.5:1 (re-check with a contrast tool; do not guess).
3. **Homepage images.** They are heavier than they need to be (~400 KB extra), and the main block appeared in about 3.1 s (a good target is 2.5 s). Compress, serve correctly sized modern formats, and avoid oversized sources.
4. **Star-rating ARIA.** Give the star-rating control an accessible name, role, and current value so assistive tech can announce it.
5. **Language switcher.** Add `aria-label="Choose language"` (or equivalent) on the control.
6. **Console RSC / Next.js prefetch error** on article pages. Clear the bad prefetch so the console is clean. This does not change SEO scores, but it should be fixed.

Re-run Lighthouse (phone) on the homepage and one article after the fix. Keep SEO at 100.

## Source conflicts to keep (do not average)

A short master list; fuller notes live in the articles themselves:

- **0–3 month totals:** NSF 14–17 (KidsHealth) vs Sleep Foundation / Pregnancy, Birth and Baby 11–19 vs NHS about 8–18 vs HealthyChildren.org about 16–17. No official week-specific totals.
- **Weeks 13–15:** between the NSF 0–3 month label and AASM 12–16 hours from 4 months (~16 weeks). Report both; do not back-fit AASM onto weeks 11–15.
- **Wake to feed:** KidsHealth about every 3–4 hours in the first weeks until weight gain is good, vs HealthyChildren.org formula Q&A (wake in the first month if more than 4–5 hours). The clinician’s plan wins.
- **“Through the night” at 1–3 months** often means a 5–6 hour stretch (KidsHealth), not 10–12 hours.
- **Body clock:** Pregnancy, Birth and Baby around 4–6 weeks (a start); Sleep Foundation melatonin/cortisol around 8–9 weeks.
- **Formal sleep training:** Sleep Foundation generally discusses readiness around 4–6 months.
- **Room temperature:** AAP “comfortable for an adult,” one extra layer, check the chest, vs NHS-style 16–20°C on the dressing page. Do not average.
- **Moro / startle timing:** HealthyChildren.org vs KidsHealth vs MedlinePlus disagree on when it fades. Do not average.
- **Lovey timing:** AAP / Michigan DHHS nothing in the crib until at least 12 months, vs Red Nose Australia 7 vs 12 months. Do not average 7 and 12.
- **Moses baskets:** Lullaby Trust / NHS (BS EN 1466) vs HealthyChildren.org warning about many U.S. mini-baskets. Show both.
- **Mattress gap:** AAP wants a snug fit. The federal 16 CFR 1241 rule is a *manufacturer* lab test, not a parent instruction to leave a 3-inch gap.
- **Screens:** 2016 daily-cap wording vs later “move beyond simple caps” / hour-before-bed advice. Show both.
- **Breast vs formula and “sleeping through”:** HealthyChildren.org frequency differences vs Australian Breastfeeding Association “no evidence they differ in when they start sleeping through.” These are not the same question.
- Community threads may have shaped H2s and FAQs in the pilot, weeks, and later packs. **Never treat forum anecdotes as medical facts or numbers.**

Unverified claims already marked in earlier articles (keep the marking): the circulating “2 hours in a car seat” rule, a timed cortisol spike, the red-light vision claim, and informal TOG charts that are not official AAP figures.

## Files in this zip

```
MASTER-INSTRUCTIONS.md      ← this file
CHECKLIST.md                ← tick boxes per phase
manifest.csv                ← every new article, the hub, and every edited existing page
articles/                   ← 109 new English articles, .md + .docx, one folder, no duplicates
hub/baby-sleep-by-week.md   ← TOC page (+ .docx)
hub/WEEK-NAV.md             ← prev/next spec for weeks 1–15
edits/                      ← one file per target page, plus _INDEX, _CONFLICTS, _INBOUND
reference/live-51.csv
reference/do-not-publish.md
reference/deferred-links.csv
```

## Counts (for a final check)

| Item | Count |
| --- | ---: |
| Already live English articles | 51 |
| New English articles in `articles/` | 109 |
| Hub (`/baby-sleep-by-week`) | 1 |
| **English articles after this ship** | **160** |
| Pages with an `edits/` file (live + earlier-phase pages that gain pastes or inbound links) | 111 |
| Of those, already-live pages | 42 |
| MERGE / shrink blocks parsed | 127 |
| Of those, officially superseded (do not paste) | 3 |
| Unique inbound link rows (from, to, phase) | 501 |
| Deferred later-phase links already in final Markdown | 0 |

If any count does not match after implementation, stop and compare the live sitemap to `manifest.csv` before adding more URLs.

## What was already corrected in this handoff

Three broken internal routes were found in source articles and **fixed in the Markdown (and Word copies) in this zip**:

- `/4-month-sleep-regression` → `/sleep-regression/4-months` (week 13–15 articles)
- `/teething-and-sleep` → `/teething-symptoms` (`teeth-grinding-in-sleep`)
- `/separation-anxiety-at-night` → `/separation-anxiety-and-sleep` (`sleep-after-separation-or-divorce`)

If you still see the old paths in an older zip or note, use the canonical slugs above.
