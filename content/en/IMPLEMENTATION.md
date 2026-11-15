# Yorix — English content implementation brief (for an AI coding agent)

Prepared 15 Nov 2026. Repository: the Next.js site behind https://yorix-app.com (22 locales + English).
This package contains 51 finished English articles (Markdown in `articles/`, Word copies in `docx/`), a master table, a link-check report and step-by-step instructions. Read this whole file before changing code.

## 1. Goal

Publish the 51 English articles on yorix-app.com: replace the text of 12 existing English guides, add 39 new English pages, and merge 2 old URLs into existing pages with 301 redirects. Every page must render correctly (title, meta, tables, byline, dates, disclaimer, JSON-LD, canonical, OG tags) and appear in the sitemap.

## 2. Scope and hard rules

1. **English only for now.** Change only English (root) pages. Other locales will be translated later.
2. **Do NOT machine-translate or overwrite other locales' existing content.** The 22 locale versions of the 12 replaced guides (`/de/wake-windows-by-age`, etc.) keep their current text and must keep working (HTTP 200, same URL).
3. New pages are English only. Do not create empty or auto-translated locale versions of them; locale routes for new slugs should return 404 (not a copy of the English page).
4. **hreflang:** only between versions that actually exist. Replaced guides: en + the 22 locales that already have that slug, plus `x-default` → English. New pages: English only — either no hreflang, or self `en` + `x-default`. Never point hreflang to a locale URL that does not exist. (Currently the live site has no hreflang tags and no `xhtml:link` alternates in the sitemap, so this is an addition, not a change.)
5. Do not edit article wording, numbers or sources. The texts were fact-checked against the listed sources and checked for uniqueness. Allowed: technical fixes (link URLs to match routes, dates, markup).
6. Lines starting with `> **Implementation note (not for publication):**` (in `newborn-sleep-schedule.md` and `survive-night-wakings-new-parents.md`, line 13) are instructions for you. **Do not render them.** Front-matter fields `merge_note`, `meta_title_note`, `*_character_count`, `secondary_queries`, `primary_query` are internal and must not be rendered.

## 3. Current live structure (verified 15 Nov 2026 by fetching the live site)

- `https://yorix-app.com/robots.txt` lists `sitemap.xml` and `sitemap-pages.xml`. `sitemap.xml` has 418 URLs, all `lastmod` 2026-09-07, no `xhtml:link` alternates.
- **Route pattern:** English pages live at the root: `https://yorix-app.com/<slug>` (no `/en/` prefix, no `/guides/` prefix). Locale pages: `https://yorix-app.com/<lang>/<slug>`.
- Locales (22): `ar cs da de es fr he hi id it ja ms nl no pl pt ru sv th tr uk vi`.
- Hub page: `/guides` (and `/<lang>/guides`). Other pages: `/about`, `/support`, `/subscription/privacy`, `/subscription/terms`.
- Live HTML: `<html lang="en" dir="ltr">` (locale pages `lang="de"` etc.), self-referencing canonical, OG tags (`og:title`, `og:description`, `og:url`, `og:type=article`, `og:locale`), `twitter:card=summary`. **No JSON-LD and no hreflang tags** on article pages today.
- Served by nginx behind **Cloudflare** (`cf-ray` header present).
- Existing English URLs found in the sitemap:
  - `/`
  - `/10-month-old-sleep-schedule`
  - `/3-month-old-sleep-schedule`
  - `/4-month-old-sleep-schedule`
  - `/5-month-old-sleep-schedule`
  - `/about`
  - `/baby-feeding-schedule`
  - `/baby-nap-schedule-by-age`
  - `/baby-sleep-parent-stress`
  - `/ferber-method-baby-sleep`
  - `/guides`
  - `/newborn-sleep-first-28-days`
  - `/newborn-sleep-schedule`
  - `/sleep-training-methods-explained`
  - `/subscription/privacy`
  - `/subscription/terms`
  - `/support`
  - `/survive-night-wakings-new-parents`
  - `/wake-windows-by-age`
  - `/white-noise-for-baby-sleep`

### Route mapping used in this package

- All flat slugs map 1:1 to the root: `articles/<slug>.md` → `https://yorix-app.com/<slug>`. This matches the existing pattern, so the 12 replaced guides keep their URLs.
- **New section – sleep regressions (decision for the owner before launch):** the files use a nested route: hub `/sleep-regression` + children `/sleep-regression/3-months`, `/4-months`, `/6-months`, `/8-months`, `/12-months`, `/18-months`, `/2-years` (canonicals, internal links and BreadcrumbList are already written this way). Implement it as a nested Next.js route (e.g. `app/sleep-regression/[age]/page.tsx` or the equivalent in the repo's routing), placed in the same layout as guides. File names in `articles/` are flattened (`sleep-regression-4-months.md` → `/sleep-regression/4-months`).
  - Alternative (only if the owner asks for it): flat `/4-month-sleep-regression` etc. In that case update canonical, every internal link, and JSON-LD URLs consistently. Default = nested.
- Comparison pages stay flat: `/yorix-vs-huckleberry`, `/yorix-vs-napper`.
- Add every new page to the `/guides` hub (group them: Sleep schedules by month, Sleep regressions, Sleep problems & methods, Development & feeding, Comparisons).

## 4. Counts

- REPLACE existing English page: **12** (2 of them are also merge targets).
- NEW page: **39** (28 sleep/comparison pages + 1 four-month regression page + 10 development/feeding pages).
- MERGED (old URL removed, 301 redirect, no file): **2** — `/newborn-sleep-first-28-days`, `/baby-sleep-parent-stress`.
- Total article files: **51**.

## 5. Master table of all articles

Character counts in brackets. `primary_query` = main target search query (internal, do not render). The same table is in `articles-table.csv` (with word counts).

| # | URL path | Status | Group | File | Title (chars) | Meta description (chars) | Primary query | H1 |
|---|---|---|---|---|---|---|---|---|
| 1 | `/newborn-sleep-schedule` | REPLACE + MERGE TARGET | Sleep | `articles/newborn-sleep-schedule.md` | Newborn Sleep Schedule: What's Normal Week by Week \| Yorix (58) | Is there a newborn sleep schedule? What's normal in the first weeks, how many hours newborns sleep, feeding at night, day-night cues, and red flags to know. (156) | newborn sleep schedule | Newborn Sleep Schedule: What's Normal, Week by Week |
| 2 | `/survive-night-wakings-new-parents` | REPLACE + MERGE TARGET | Sleep | `articles/survive-night-wakings-new-parents.md` | Baby Waking at Night: A Guide for Exhausted Parents \| Yorix (59) | Why babies wake at night, what's normal by age, hunger vs comfort, safe sleep when you're exhausted, sharing the night shift, and when parents need help. (153) | baby waking at night | Baby Waking at Night: How to Get Through It (and Look After Yourself) |
| 3 | `/10-month-old-sleep-schedule` | REPLACE | Sleep | `articles/10-month-old-sleep-schedule.md` | 10 Month Old Sleep Schedule: Naps, Standing & Nights \| Yorix (60) | 10 month old sleep schedule: 12–16 hours a day (AASM), two naps, wake windows, an example day, and help with standing in the crib and separation anxiety. (153) | 10 month old sleep schedule | 10 Month Old Sleep Schedule: Two Naps, New Skills, and Night Waking |
| 4 | `/3-month-old-sleep-schedule` | REPLACE | Sleep | `articles/3-month-old-sleep-schedule.md` | 3 Month Old Sleep Schedule: Naps & Night Stretches \| Yorix (58) | A 3 month old sleep schedule: how much sleep at 12 weeks (14–17 hours per NSF), how many naps, longer night stretches, night feeds, and an example day. (151) | 3 month old sleep schedule | 3 Month Old Sleep Schedule: Naps, Night Stretches, and an Example Day |
| 5 | `/4-month-old-sleep-schedule` | REPLACE | Sleep | `articles/4-month-old-sleep-schedule.md` | 4 Month Old Sleep Schedule: Naps, Bedtime & Totals \| Yorix (58) | A 4 month old sleep schedule with 3-nap and 4-nap example days, how much a 4 month old should sleep (12–16 hours), short naps, bedtime, and night feeds. (152) | 4 month old sleep schedule | 4 Month Old Sleep Schedule: Naps, Bedtime, and How Much Sleep Is Enough |
| 6 | `/5-month-old-sleep-schedule` | REPLACE | Sleep | `articles/5-month-old-sleep-schedule.md` | 5 Month Old Sleep Schedule: 3 Naps, Bedtime & Nights \| Yorix (60) | 5 month old sleep schedule: 12–16 hours a day (AASM), when 4 naps become 3, why 30-minute naps are so common, night waking, and an example 3-nap day. (149) | 5 month old sleep schedule | 5 Month Old Sleep Schedule: Moving to 3 Naps and Steadier Nights |
| 7 | `/baby-feeding-schedule` | REPLACE | Sleep | `articles/baby-feeding-schedule.md` | Baby Feeding Schedule by Age: First-Year Chart \| Yorix (54) | Baby feeding schedule by age: how often and how much breast milk or formula from newborn to 12 months, when to start solids, hunger cues, and red flags. (152) | baby feeding schedule | Baby Feeding Schedule by Age: How Often and How Much, Birth to 12 Months |
| 8 | `/baby-nap-schedule-by-age` | REPLACE | Sleep | `articles/baby-nap-schedule-by-age.md` | Baby Nap Schedule by Age: Chart & Nap Transitions \| Yorix (57) | How many naps a baby needs by age, how long naps last, and when babies drop from 3 to 2 and from 2 to 1 nap, with example nap days and source-backed ranges. (156) | baby nap schedule by age | Baby Nap Schedule by Age: Nap Chart and Nap Transitions |
| 9 | `/ferber-method-baby-sleep` | REPLACE | Sleep | `articles/ferber-method-baby-sleep.md` | Ferber Method: Interval Chart, Steps & Right Age \| Yorix (56) | The Ferber method step by step: the 7-night check-in interval chart, what to do on night wakings, the age to start, when to stop, and what research shows. (154) | ferber method | The Ferber Method: Check-In Chart, Step-by-Step Plan, and When to Stop |
| 10 | `/sleep-training-methods-explained` | REPLACE | Sleep | `articles/sleep-training-methods-explained.md` | Sleep Training Methods Compared: Which One Fits? \| Yorix (56) | Sleep training methods side by side: cry it out, Ferber, check and console, chair, pick up/put down, bedtime fading and no-cry, with age, crying and evidence. (158) | sleep training methods | Sleep Training Methods Explained: A Side-by-Side Comparison |
| 11 | `/wake-windows-by-age` | REPLACE | Sleep | `articles/wake-windows-by-age.md` | Wake Windows by Age: Chart from Newborn to 12 Months \| Yorix (60) | Wake windows by age from newborn to 12 months, with ranges from Sleep Foundation and Cleveland Clinic, a 3–6 month table, tired cues, and how to time naps. (155) | wake windows by age | Wake Windows by Age: A Chart From Newborn to 12 Months |
| 12 | `/white-noise-for-baby-sleep` | REPLACE | Sleep | `articles/white-noise-for-baby-sleep.md` | Baby White Noise: Safe Volume, Placement & Weaning \| Yorix (58) | Does white noise help babies sleep? What the studies show, why sound machines can get too loud, AAP placement and volume advice, and how to wean off it. (152) | white noise for baby sleep | Baby White Noise: Does It Help, and How to Use a Sound Machine Safely |
| 13 | `/1-month-old-sleep-schedule` | NEW | Sleep | `articles/1-month-old-sleep-schedule.md` | 1 Month Old Sleep Schedule & 4 Week Old Wake Windows \| Yorix (60) | 1 month old sleep schedule for weeks 4–7: how much sleep is normal, 4 week old wake windows, an example day built around feeds, and a first bedtime routine. (156) | 1 month old sleep schedule | 1 Month Old Sleep Schedule: Weeks 4 to 7, Wake Windows, and a First Routine |
| 14 | `/11-month-old-sleep-schedule` | NEW | Sleep | `articles/11-month-old-sleep-schedule.md` | 11 Month Old Sleep & Feeding Schedule: Sample Day \| Yorix (57) | 11 month old sleep and feeding schedule: two naps, wake windows of about 3–4 hours, meals and milk amounts from the AAP, and a sample day. Sources checked. (155) | 11 month old sleep schedule | 11 Month Old Sleep and Feeding Schedule: Two Naps, Three Meals |
| 15 | `/12-month-old-sleep-schedule` | NEW | Sleep | `articles/12-month-old-sleep-schedule.md` | 12 Month Old Sleep Schedule (1 Year Old) & Naps \| Yorix (55) | 12 month old sleep schedule: how much sleep a 1 year old needs, a sample two-nap day, wake windows, bedtime, and the milk, cup and crib changes at age one. (155) | 12 month old sleep schedule | 12 Month Old Sleep Schedule: A Day in the Life of a One-Year-Old |
| 16 | `/15-month-old-sleep-schedule` | NEW | Sleep | `articles/15-month-old-sleep-schedule.md` | 15 Month Old Sleep Schedule: 2 to 1 Nap Transition \| Yorix (58) | 15 month old sleep schedule: 11–14 hours of sleep, when and how to move from 2 naps to 1, sample one-nap and two-nap days, wake windows and a toddler bedtime. (158) | sleep schedule for 15 month old | 15 Month Old Sleep Schedule and the Switch From Two Naps to One |
| 17 | `/2-month-old-sleep-schedule` | NEW | Sleep | `articles/2-month-old-sleep-schedule.md` | 2 Month Old Sleep Schedule: Naps & Wake Windows \| Yorix (55) | 2 month old sleep schedule: 14–17 hours, 4–5 short naps, wake windows of about 1–1.5 hours, a sample 8-week day and a simple bedtime routine, with sources. (155) | 2 month old sleep schedule | 2 Month Old Sleep Schedule: What an 8- to 11-Week Day Can Look Like |
| 18 | `/6-month-old-sleep-schedule` | NEW | Sleep | `articles/6-month-old-sleep-schedule.md` | 6 Month Old Sleep Schedule, Naps & Wake Windows \| Yorix (55) | 6 month old sleep schedule: how much sleep, 3-nap and 2-nap example days, wake windows, a bedtime routine and a simple sleep plan, all with sources checked. (156) | 6 month old sleep schedule | 6 Month Old Sleep Schedule: Naps, Wake Windows, Bedtime Routine, and a Simple Plan |
| 19 | `/7-month-old-sleep-schedule` | NEW | Sleep | `articles/7-month-old-sleep-schedule.md` | 7 Month Old Sleep Schedule: 3 to 2 Naps & Bedtime \| Yorix (57) | 7 month old sleep schedule: how much sleep, whether to keep 3 naps or move to 2, 7 month wake windows, example days and a bedtime routine. Sources checked. (155) | 7 month old sleep schedule | 7 Month Old Sleep Schedule: Keeping Three Naps or Moving to Two |
| 20 | `/8-month-old-sleep-schedule` | NEW | Sleep | `articles/8-month-old-sleep-schedule.md` | 8 Month Old Sleep Schedule: 2-Nap Day & Wake Windows \| Yorix (60) | 8 month old sleep schedule: a typical 2-nap day, 8 month wake windows, bedtime, meals and milk around sleep, and how a schedule differs from a regression. (154) | 8 month old sleep schedule | 8 Month Old Sleep Schedule: A Typical Two-Nap Day |
| 21 | `/9-month-old-sleep-schedule` | NEW | Sleep | `articles/9-month-old-sleep-schedule.md` | 9 Month Old Sleep Schedule: 2 Naps & Wake Windows \| Yorix (57) | 9 month old sleep schedule: two naps, 9 month wake windows of about 3 hours, a sample day, bedtime timing and how to handle separation worries at night. (152) | 9 month old sleep schedule | 9 Month Old Sleep Schedule: Settling Into Two Naps |
| 22 | `/baby-waking-every-hour` | NEW | Sleep | `articles/baby-waking-every-hour.md` | Baby Waking Every Hour at Night: Causes & Fixes \| Yorix (55) | Why babies wake every hour at night by age, what's normal and what isn't, the signs to call your pediatrician, and practical steps toward longer stretches. (155) | baby waking every hour | Baby Waking Every Hour at Night: Why It Happens and What Helps |
| 23 | `/contact-naps` | NEW | Sleep | `articles/contact-naps.md` | Contact Naps: Safety Rules & Moving to the Crib \| Yorix (55) | Contact naps explained: why babies love sleeping on you, safety rules from AAP-based guidance, when they become a problem, and gentle ways to move to the crib. (159) | contact naps | Contact Naps: Safety Rules, Benefits, and How to Transition to the Crib |
| 24 | `/cry-it-out-method` | NEW | Sleep | `articles/cry-it-out-method.md` | Cry It Out Method: Age, Research & Gentler Options \| Yorix (58) | The cry it out method explained: what extinction means, why it's not for newborns, what research on crying and attachment shows, fuss it out, and no-cry options (160) | cry it out method | The Cry It Out Method: What It Is, When It's Used, and What the Research Says |
| 25 | `/dream-feed` | NEW | Sleep | `articles/dream-feed.md` | Dream Feed: What It Is, How to Do It & When to Stop \| Yorix (59) | Dream feed guide: what a dream feed is, how to do it safely, when to start and stop, and what the research actually shows about whether dream feeding works. (156) | dream feed | Dream Feed: What It Is, How to Do It Safely, and When to Stop |
| 26 | `/early-morning-waking` | NEW | Sleep | `articles/early-morning-waking.md` | Baby Waking at 5am? Early Morning Waking Fixes \| Yorix (54) | Why babies wake at 4:30 or 5am, how to tell if it's too early or just enough sleep, and a step-by-step plan for light, naps, bedtime and calm morning responses. (160) | baby waking at 5am | Baby Waking at 5am: Causes of Early Morning Waking and How to Shift It |
| 27 | `/false-starts` | NEW | Sleep | `articles/false-starts.md` | False Starts: Baby Wakes 30–45 Minutes After Bedtime \| Yorix (60) | Baby wakes 30–45 minutes after bedtime? What false starts are, how to tell overtired from undertired, and how to adjust the last wake window to stop them. (154) | false starts baby sleep | False Starts: Why Your Baby Wakes Soon After Bedtime and How to Fix It |
| 28 | `/newborn-grunting-in-sleep` | NEW | Sleep | `articles/newborn-grunting-in-sleep.md` | Newborn Grunting in Sleep: Normal or a Warning Sign? \| Yorix (60) | Why newborns grunt and squirm in their sleep, what grunting baby syndrome is, and the breathing red flags that mean you should call the doctor or 911. (150) | newborn grunting in sleep | Newborn Grunting in Sleep: What's Normal and When to Call the Doctor |
| 29 | `/short-naps` | NEW | Sleep | `articles/short-naps.md` | Short Naps: Why Your Baby Only Naps 30 Minutes \| Yorix (54) | Baby only takes 30 minute naps? Why short naps happen at 3, 4, 5 and 6 months, when they usually lengthen, and calm, step-by-step ways to stretch them. (151) | baby short naps | Short Naps: Why Your Baby Wakes After 30 Minutes (and What Helps) |
| 30 | `/sleep-regression` | NEW | Sleep | `articles/sleep-regression.md` | Sleep Regression Ages: What Happens at Each Stage \| Yorix (57) | Sleep regression ages explained: what the evidence says about 3–4, 6, 8, 12 and 18 months and 2 years, whether newborns have one, signs and how long it lasts. (158) | sleep regression ages | Sleep Regression Ages: A Stage-by-Stage Guide From Birth to Age 2 |
| 31 | `/sleep-regression/12-months` | NEW | Sleep | `articles/sleep-regression-12-months.md` | 12 Month Sleep Regression: Walking, Naps & Help \| Yorix (55) | 12 month sleep regression: why first steps, separation anxiety and nap changes can disrupt sleep around age one, how long it lasts, and why 2 naps still fit. (157) | 12 month sleep regression | 12 Month Sleep Regression: Sleep Around the First Birthday |
| 32 | `/sleep-regression/18-months` | NEW | Sleep | `articles/sleep-regression-18-months.md` | 18 Month Sleep Regression: Toddler Bedtime Battles \| Yorix (58) | The 18 month sleep regression: bedtime battles, separation anxiety, the move to one nap and new words. What the evidence says, how long it lasts, what helps. (157) | 18 month sleep regression | 18 Month Sleep Regression: Bedtime Battles, One Nap, and a Busy Brain |
| 33 | `/sleep-regression/2-years` | NEW | Sleep | `articles/sleep-regression-2-years.md` | 2 Year Old Sleep Regression: Naps, Stalling & Beds \| Yorix (58) | The 2 year old sleep regression: nap strikes, bedtime stalling, early waking and the move from crib to bed. What the evidence says and calm, practical fixes. (157) | 2 year old sleep regression | 2 Year Old Sleep Regression: Nap Strikes, Bedtime Stalling, and the Big-Kid Bed |
| 34 | `/sleep-regression/3-months` | NEW | Sleep | `articles/sleep-regression-3-months.md` | 3 Month Sleep Regression: Is It Real? What to Do \| Yorix (56) | Is the 3 month sleep regression real? How it relates to the 4 month shift, how to tell it from normal 3-month sleep, what to rule out first, and what helps. (156) | 3 month sleep regression | 3 Month Sleep Regression: Is It Real, and What Is Actually Going On? |
| 35 | `/sleep-regression/4-months` | NEW | Sleep | `articles/sleep-regression-4-months.md` | 4 Month Sleep Regression: Signs, How Long It Lasts & What Helps \| Yorix (71) | The 4 month sleep regression is usually temporary. Learn typical signs, how long it lasts, how much a 4 month old should sleep, wake windows, and what helps. (157) | 4 month sleep regression | 4 Month Sleep Regression: Signs, How Long It Lasts, and What Helps |
| 36 | `/sleep-regression/6-months` | NEW | Sleep | `articles/sleep-regression-6-months.md` | 6 Month Sleep Regression: Real or Myth? What Helps \| Yorix (58) | Is the 6 month sleep regression real? Many babies don't have one. Signs, likely causes, how long it lasts, and calm ways to handle more night waking. (149) | 6 month sleep regression | 6 Month Sleep Regression: Is It Real, and What Can You Do? |
| 37 | `/sleep-regression/8-months` | NEW | Sleep | `articles/sleep-regression-8-months.md` | 8 Month Sleep Regression (8–10 Months): What Helps \| Yorix (58) | The 8, 9 or 10 month sleep regression: why crawling, pulling to stand, teething and separation anxiety can disrupt sleep, how long it lasts, and what helps. (156) | 8 month sleep regression | 8 Month Sleep Regression: Why Sleep Gets Bumpy Between 8 and 10 Months |
| 38 | `/split-nights` | NEW | Sleep | `articles/split-nights.md` | Split Nights: Baby Awake for Hours at Night? \| Yorix (52) | Baby wide awake and happy for 1–3 hours at 2am? What split nights are, why too much time in bed causes them, and a schedule fix that usually works in a week. (157) | split nights baby | Split Nights: Why Your Baby Is Wide Awake for Hours in the Middle of the Night |
| 39 | `/when-to-start-sleep-training` | NEW | Sleep | `articles/when-to-start-sleep-training.md` | When to Start Sleep Training: Best Age & Readiness \| Yorix (58) | What age to start sleep training, signs your baby is ready, when babies can self-soothe, and why there's no rush: guidance from pediatricians and research. (155) | when to start sleep training | When to Start Sleep Training: Age, Readiness Signs, and Self-Soothing |
| 40 | `/12-month-milestones` | NEW | Development/feeding (recommend expert review) | `articles/12-month-milestones.md` | 12 Month Milestones: 1-Year-Old Checklist \| Yorix (49) | 12 month milestones from CDC's 2022 checklist: waving, 'mama' or 'dada', pulling to stand, cruising, pincer grasp. When walking is expected and when to ask. (156) | 12 month milestones | 12 Month Milestones: What Most 1-Year-Olds Can Do |
| 41 | `/4-month-milestones` | NEW | Development/feeding (recommend expert review) | `articles/4-month-milestones.md` | 4 Month Milestones: What Most Babies Do \| Yorix (47) | 4 month milestones based on CDC's 2022 checklist: social, language, thinking, and movement skills most babies show by 4 months, play ideas, and when to ask. (156) | 4 month milestones | 4 Month Milestones: What Most Babies Can Do and When to Talk to Your Doctor |
| 42 | `/6-month-milestones` | NEW | Development/feeding (recommend expert review) | `articles/6-month-milestones.md` | 6 Month Milestones: Checklist & Play Ideas \| Yorix (50) | 6 month milestones from CDC's 2022 checklist: rolling, pushing up, laughing, babbling, and reaching. What changes after 4 months, play ideas, and when to ask. (158) | 6 month milestones | 6 Month Milestones: What Most Babies Do by Half a Year |
| 43 | `/9-month-milestones` | NEW | Development/feeding (recommend expert review) | `articles/9-month-milestones.md` | 9 Month Milestones: Sitting, Babbling & Shyness \| Yorix (55) | 9 month milestones from CDC's 2022 checklist: sitting alone, babbling, raking food, stranger shyness, object permanence. Plus crawling facts and when to ask. (157) | 9 month milestones | 9 Month Milestones: Development Checklist for a 9 Month Old |
| 44 | `/baby-led-weaning` | NEW | Development/feeding (recommend expert review) | `articles/baby-led-weaning.md` | Baby-Led Weaning: First Foods, Safety & How to Start \| Yorix (60) | Baby-led weaning (BLW): when to start, first finger foods and how to cut them, gagging vs choking, iron and allergens, and what research says about safety. (155) | baby led weaning | Baby-Led Weaning (BLW): First Foods, Safety, and How to Start |
| 45 | `/colic` | NEW | Development/feeding (recommend expert review) | `articles/colic.md` | Colic in Babies: Signs, How Long It Lasts & Relief \| Yorix (58) | Baby colic explained: the rule of 3s, evening colic, when it peaks and ends, which remedies have evidence, red flags that are not colic, and how to cope safely. (160) | colic baby | Colic in Babies: What It Is, How Long It Lasts, and What Actually Helps |
| 46 | `/introducing-allergens` | NEW | Development/feeding (recommend expert review) | `articles/introducing-allergens.md` | Introducing Allergens to Baby: Peanut & Egg \| Yorix (51) | When and how to introduce allergens to your baby: peanut, egg, dairy, wheat, fish, sesame. NIAID risk groups, safe forms, reaction signs, and when to call. (155) | introducing allergens to baby | Introducing Allergens to Your Baby: When, How, and What to Watch For |
| 47 | `/teething-symptoms` | NEW | Development/feeding (recommend expert review) | `articles/teething-symptoms.md` | Teething Symptoms: Signs, Fever, Rash & Timing \| Yorix (54) | Teething symptoms explained: when babies start teething, which signs are real, why a true fever or diaper rash isn't teething, safe remedies, and when to call. (159) | teething symptoms | Teething Symptoms: What's Really Teething, What Isn't, and How to Help |
| 48 | `/tummy-time` | NEW | Development/feeding (recommend expert review) | `articles/tummy-time.md` | Tummy Time by Age: How Long, When to Start & Tips \| Yorix (57) | Tummy time from newborn to 6 months: when to start, minutes a day by age, positions that work, what to do if your baby hates it, and safety rules. (146) | tummy time | Tummy Time by Age: When to Start, How Long, and How to Make It Easier |
| 49 | `/when-to-start-solids` | NEW | Development/feeding (recommend expert review) | `articles/when-to-start-solids.md` | When to Start Solids: Signs, Cereal & Purees \| Yorix (52) | When can babies start eating food? The 4–6 month rule, readiness signs, first purees, infant cereal and rice arsenic, a first-weeks plan, and what to avoid. (156) | when can infants start eating food | When to Start Solids: Readiness Signs, First Foods, and a Simple Plan |
| 50 | `/yorix-vs-huckleberry` | NEW | Comparison | `articles/yorix-vs-huckleberry.md` | Huckleberry App vs Yorix: Features & Prices Compared \| Yorix (60) | Huckleberry app vs Yorix: an honest look at nap predictions, AI help, free tiers, prices, languages, devices and privacy, to pick the baby app that fits you. (157) | huckleberry app | Huckleberry vs Yorix: A Fair Comparison of Two Baby Sleep Apps |
| 51 | `/yorix-vs-napper` | NEW | Comparison | `articles/yorix-vs-napper.md` | Napper App vs Yorix: Price, Features, Platforms \| Yorix (55) | Napper app review and comparison with Yorix: free vs paid features, prices on 15 Nov 2026, Android and Apple Watch support, languages and data storage. (151) | napper app | Napper vs Yorix: Which Baby Sleep App Fits Your Family? |

Notes on metadata:
- `/sleep-regression/4-months`: front-matter `title` is 70 characters (too long for Google). **Use the shorter alternative in `meta_title`: "4 Month Sleep Regression: Signs, Duration & Help | Yorix" (58 chars)** for `<title>`/`og:title`, unless the owner decides otherwise. Also update `headline`/`name` in its JSON-LD to the same value.
- All other titles ≤ 60 characters; descriptions ≤ 160.

## 6. Redirects and merges

Add permanent (301) redirects in English and all 22 locales:

| From | To |
|---|---|
| `/newborn-sleep-first-28-days` | `/newborn-sleep-schedule` |
| `/<lang>/newborn-sleep-first-28-days` | `/<lang>/newborn-sleep-schedule` |
| `/baby-sleep-parent-stress` | `/survive-night-wakings-new-parents` |
| `/<lang>/baby-sleep-parent-stress` | `/<lang>/survive-night-wakings-new-parents` |

- Implement in `next.config` `redirects()` (or middleware) with `permanent: true`, single hop (no chains). If nginx config is in the repo and handles redirects, one place only.
- Remove the old URLs from the sitemap(s), the `/guides` hub, navigation, hreflang sets and every internal link in all locales (replace with the target URL in the same locale).
- The English content of the old pages is already merged into the new texts of the targets. For locales, the target pages keep their existing locale text (no translation now).

## 7. Rendering rules (for every article)

1. **Source format:** each `.md` = YAML front matter, Markdown body, then a fenced ```` ```json ```` block at the very end with JSON-LD. The JSON block must not be shown as text; inject it as `<script type="application/ld+json">`.
2. **Head:** `<title>` = `title` (except 4-month, see §5); `<meta name="description">` = `meta_description`; `<link rel="canonical">` = `canonical` (absolute, root route, no trailing slash, matches the site's current format); `og:title`, `og:description`, `og:url` (= canonical), `og:type=article`, `og:locale=en_US`, `og:site_name=Yorix`, `twitter:card` (keep site default); `<html lang="en">`.
3. **Body:** render Markdown fully, including GFM tables (many pages have tables; make them horizontally scrollable on mobile), bold/italic, ordered/unordered lists, H2/H3 hierarchy (only one H1 = the `# ` line), and links. Internal links are root-relative and must become Next.js `<Link>`s. External source links open normally (`rel="noopener"`; keep them followable).
4. **Byline and dates:** each file has `**By the Yorix team**` and `**Published:** [Month DD, YYYY] · **Updated:** [Month DD, YYYY]`. Replace the placeholders with real dates:
   - NEW pages: Published = Updated = the actual deploy date.
   - REPLACED pages: Published = the original publish date of that page if the repo has it (otherwise the deploy date), Updated = the deploy date.
   - In JSON-LD set `datePublished` / `dateModified` in ISO format (`YYYY-MM-DD`) to the same values. **No `[YYYY-MM-DD]` or `[Month DD, YYYY]` placeholders may remain anywhere** (grep the build output).
5. **Disclaimer:** the italic paragraph under the byline (medical/general-information disclaimer) must be rendered as written, visible above the fold.
6. **JSON-LD:** keep the `@graph` with `Article` + `BreadcrumbList` from each file. Check that every URL in it (`mainEntityOfPage`, breadcrumb `item`s) equals the real route. Breadcrumbs: Home → Guides (`/guides`) → page; regression children: Home → Guides → Sleep regression ages (`/sleep-regression`) → page. `author` and `publisher` = `Organization` "Yorix" (keep; do not invent a person). **Do not add FAQPage schema** (none is in the files; do not create it).
7. **Sitemap:** add all new URLs to the sitemap that currently lists the guides, with real `lastmod` = the page's Updated date; update `lastmod` for replaced pages; remove the 2 merged URLs. Locale URLs of new pages must not be added (they do not exist).
8. **Fix the broken "Example day" template block.** On the live site, 10 English pages (3-, 5-, 10-month schedules, feeding schedule, white noise, Ferber, sleep-training methods, night wakings, parent stress, first 28 days) show an auto-generated "Example day" block with nonsense like "Uses 12-16 hours as context for the next plan". This template/component must be removed from English article pages; the new Markdown texts contain proper example days written by hand. Do not render any template-generated schedule block on top of the Markdown. (Check whether the same component appears on locale pages; if it does, flag it to the owner but do not rewrite locale text.)
9. **Images:** none are included. Do not add stock or generated images unless the owner asks. Keep the site's default OG image.
10. Internal links: all 486 internal links in the package resolve (see §10). After implementing routes, run a crawl to confirm every internal link returns 200 with no redirect hop.

## 8. Publish order

1. **Batch 1 — all sleep pages together** (REPLACE 12 + new sleep pages + regression hub/children + comparisons), plus the redirects. They link to each other heavily, so publish them in one deploy to avoid 404 links.
2. **Batch 2 — development & feeding pages (10)**: `/12-month-milestones`, `/4-month-milestones`, `/6-month-milestones`, `/9-month-milestones`, `/baby-led-weaning`, `/colic`, `/introducing-allergens`, `/teething-symptoms`, `/tummy-time`, `/when-to-start-solids`. These are medical/health topics: **recommend expert (pediatrician/dietitian) review before publishing — the owner decides.** Note: 4 sleep pages link to batch-2 pages: `4-month-old-sleep-schedule` → `/4-month-milestones`, `6-month-old-sleep-schedule` → `/6-month-milestones`, `9-month-old-sleep-schedule` → `/9-month-milestones`, `12-month-old-sleep-schedule` → `/12-month-milestones`. If batch 2 is delayed, temporarily render links to unpublished batch-2 pages as plain text (or hold them) and restore them on publish — do not leave 404 links.
   - `/newborn-grunting-in-sleep` is in batch 1 but is also health-related; an expert review is recommended there too (optional).

## 9. Known issues / notes for the owner

- App Store description says the app supports **14 languages**, while the App Store listing shows **20** and the site has 22 locales + English. Not a code task; the owner should align the App Store text.
- App figures inside articles are labelled "App example" — keep that label.
- `/sleep-regression/...` nested vs flat route: decision needed before launch (default nested).
- Other locales still show the old texts for replaced guides; translation is a later task.

## 10. Link-check report (run 15 Nov 2026 on all 51 files)

- Method: every root-relative Markdown link `](/...)` in every file (JSON-LD excluded), anchors stripped, compared to (a) the 51 canonical paths in this package and (b) the English URLs in the live sitemap.
- Result: **486 internal links, 0 broken.** All 486 links point to pages in this package. No links to the merged/redirected URLs.
- No internal link points to a page outside the package. Full list: `link-check.csv`.
- Only 4 links from batch-1 pages depend on batch 2 (the 4/6/9/12-month schedules → milestones pages, see §8).

## 11. Post-deploy checklist

1. `npm run build` passes; no placeholders: `grep -R "\[YYYY\|\[Month DD" .next/ out/` returns nothing.
2. Spot-check 5 pages (one per group): H1, title, description, canonical, tables, byline with dates, disclaimer, no "Implementation note", no "Example day" template block, JSON-LD valid in https://validator.schema.org / Rich Results Test.
3. 301s: `curl -I https://yorix-app.com/newborn-sleep-first-28-days` → 301 to `/newborn-sleep-schedule` (also `/de/...` etc.).
4. Locale pages of replaced guides still 200 with their old text and `lang` attribute correct; new slugs under `/<lang>/` → 404.
5. hreflang: only existing versions; sitemap valid XML, new URLs present, merged URLs absent, real `lastmod`.
6. **Purge Cloudflare cache** (everything or at least the changed URLs, `/guides`, `/sitemap.xml`, `/sitemap-pages.xml`).
7. Re-check live: `<html lang>`, canonical, hreflang, sitemap on the live domain (not just locally).
8. Google Search Console: resubmit the sitemap; **request indexing** for `/guides`, `/sleep-regression`, and the main pages (e.g. `/newborn-sleep-schedule`, `/wake-windows-by-age`, `/yorix-vs-napper`, `/yorix-vs-huckleberry`); others will be found via the sitemap.

## 12. Package contents

- `IMPLEMENTATION.md` — this file.
- `articles/` — 51 `.md` files, flat, named after the URL path (`/` → `-`).
- `docx/` — the same 51 articles as Word files (for human review only; the `.md` files are the source of truth).
- `articles-table.csv` — master table (with word counts).
- `link-check.csv` — link-check report.
