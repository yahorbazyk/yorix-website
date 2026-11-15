import type { Metadata } from 'next';
import { EnglishArticlePage } from '../article/EnglishArticlePage';
import { getEnglishArticle, englishArticleMetadata } from '../article/english-catalog';

const page = getEnglishArticle('wake-windows-by-age');

export const metadata: Metadata = englishArticleMetadata(page!);

export default function WakeWindowsByAgePage() {
  return <EnglishArticlePage slug={page!.slug} />;
}
