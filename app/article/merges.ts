// Owner-approved merges apply to English and existing translations alike.
export const articleMerges: Record<string, string> = {
  'newborn-sleep-first-28-days': 'newborn-sleep-schedule',
  'baby-sleep-parent-stress': 'survive-night-wakings-new-parents',
};

export function isRetiredArticle(slug: string): boolean {
  return Object.hasOwn(articleMerges, slug);
}
