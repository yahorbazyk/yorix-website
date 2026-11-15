import type { Metadata } from 'next';
import { EnglishArticlePage } from '../article/EnglishArticlePage';
import { getEnglishArticle, englishArticleMetadata } from '../article/english-catalog';

const page = getEnglishArticle('newborn-sleep-schedule');

export const metadata: Metadata = englishArticleMetadata(page!);

export default function NewbornSleepSchedulePage() {
  return <EnglishArticlePage slug={page!.slug} />;
}
