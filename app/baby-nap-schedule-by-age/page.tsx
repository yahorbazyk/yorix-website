import type { Metadata } from 'next';
import { EnglishArticlePage } from '../article/EnglishArticlePage';
import { getEnglishArticle, englishArticleMetadata } from '../article/english-catalog';

const page = getEnglishArticle('baby-nap-schedule-by-age');

export const metadata: Metadata = englishArticleMetadata(page!);

export default function BabyNapScheduleByAgePage() {
  return <EnglishArticlePage slug={page!.slug} />;
}
