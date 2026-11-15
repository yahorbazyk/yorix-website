import type { Metadata } from 'next';
import { EnglishArticlePage } from '../article/EnglishArticlePage';
import { getEnglishArticle, englishArticleMetadata } from '../article/english-catalog';

const page = getEnglishArticle('4-month-old-sleep-schedule');

export const metadata: Metadata = englishArticleMetadata(page!);

export default function FourMonthOldSleepSchedulePage() {
  return <EnglishArticlePage slug={page!.slug} />;
}
