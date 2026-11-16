# Week hub and prev/next nav

Publish `/baby-sleep-by-week` from `hub/baby-sleep-by-week.md` (and the matching `.docx`) in **Phase 4**, together with the 11 remaining week pages. The four pilot week pages (2, 6, 8, 12) must already be live from Phase 3 — add prev/next and the hub link on those four if missing.

The hub is a **table of contents**, not a competing week article. Put the 15 week URLs under this hub on `/guides`, not as a second set of month schedules.

## Week order

1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15.

- Week 1 has no previous link.
- Week 15 next goes to `/4-month-old-sleep-schedule` (not a week-16 URL).
- Neighbours 2, 6, 8, and 12 were written in the pilot pack (Phase 3).

## Suggested nav markup (optional but recommended)

Place this nav near the top or bottom of each `/N-week-old-baby-sleep` page (in addition to Related reading). Do not invent week 16.

```html
<nav aria-label="Week by week">
  <!-- prev: omitted on week 1 -->
  <a href="/baby-sleep-by-week">All weeks</a>
  <!-- next: /N-week-old-baby-sleep, or /4-month-old-sleep-schedule on week 15 -->
</nav>
```

## Exact prev / hub / next for each week

| Week | Page | Previous | Hub | Next |
| ---: | --- | --- | --- | --- |
| 1 | [`/1-week-old-baby-sleep`](/1-week-old-baby-sleep) | — | [/baby-sleep-by-week](/baby-sleep-by-week) | [/2-week-old-baby-sleep](/2-week-old-baby-sleep) |
| 2 | [`/2-week-old-baby-sleep`](/2-week-old-baby-sleep) | [/1-week-old-baby-sleep](/1-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/3-week-old-baby-sleep](/3-week-old-baby-sleep) |
| 3 | [`/3-week-old-baby-sleep`](/3-week-old-baby-sleep) | [/2-week-old-baby-sleep](/2-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/4-week-old-baby-sleep](/4-week-old-baby-sleep) |
| 4 | [`/4-week-old-baby-sleep`](/4-week-old-baby-sleep) | [/3-week-old-baby-sleep](/3-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/5-week-old-baby-sleep](/5-week-old-baby-sleep) |
| 5 | [`/5-week-old-baby-sleep`](/5-week-old-baby-sleep) | [/4-week-old-baby-sleep](/4-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/6-week-old-baby-sleep](/6-week-old-baby-sleep) |
| 6 | [`/6-week-old-baby-sleep`](/6-week-old-baby-sleep) | [/5-week-old-baby-sleep](/5-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/7-week-old-baby-sleep](/7-week-old-baby-sleep) |
| 7 | [`/7-week-old-baby-sleep`](/7-week-old-baby-sleep) | [/6-week-old-baby-sleep](/6-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/8-week-old-baby-sleep](/8-week-old-baby-sleep) |
| 8 | [`/8-week-old-baby-sleep`](/8-week-old-baby-sleep) | [/7-week-old-baby-sleep](/7-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/9-week-old-baby-sleep](/9-week-old-baby-sleep) |
| 9 | [`/9-week-old-baby-sleep`](/9-week-old-baby-sleep) | [/8-week-old-baby-sleep](/8-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/10-week-old-baby-sleep](/10-week-old-baby-sleep) |
| 10 | [`/10-week-old-baby-sleep`](/10-week-old-baby-sleep) | [/9-week-old-baby-sleep](/9-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/11-week-old-baby-sleep](/11-week-old-baby-sleep) |
| 11 | [`/11-week-old-baby-sleep`](/11-week-old-baby-sleep) | [/10-week-old-baby-sleep](/10-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/12-week-old-baby-sleep](/12-week-old-baby-sleep) |
| 12 | [`/12-week-old-baby-sleep`](/12-week-old-baby-sleep) | [/11-week-old-baby-sleep](/11-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/13-week-old-baby-sleep](/13-week-old-baby-sleep) |
| 13 | [`/13-week-old-baby-sleep`](/13-week-old-baby-sleep) | [/12-week-old-baby-sleep](/12-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/14-week-old-baby-sleep](/14-week-old-baby-sleep) |
| 14 | [`/14-week-old-baby-sleep`](/14-week-old-baby-sleep) | [/13-week-old-baby-sleep](/13-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/15-week-old-baby-sleep](/15-week-old-baby-sleep) |
| 15 | [`/15-week-old-baby-sleep`](/15-week-old-baby-sleep) | [/14-week-old-baby-sleep](/14-week-old-baby-sleep) | [/baby-sleep-by-week](/baby-sleep-by-week) | [/4-month-old-sleep-schedule](/4-month-old-sleep-schedule) |

Related problem pages that sit next to a week (already in Related reading; also list them on the hub where the hub draft already does):

- Week 6: `/6-week-sleep-regression`
- Week 8: `/8-week-old-short-naps`
- Week 12: `/12-week-old-false-starts`
- Week 15 / from week 16: `/4-month-old-sleep-schedule` and `/sleep-regression/4-months`
