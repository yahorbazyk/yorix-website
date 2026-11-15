import type { Metadata } from 'next';
import { EnglishArticlePage } from '../article/EnglishArticlePage';
import { getEnglishArticle, englishArticleMetadata } from '../article/english-catalog';

const page = getEnglishArticle('baby-feeding-schedule');

export const metadata: Metadata = englishArticleMetadata(page!);

export default function BabyFeedingSchedulePage() {
  return <EnglishArticlePage slug={page!.slug} />;
}
