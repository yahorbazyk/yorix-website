import type { Metadata } from 'next';
import { SeoArticlePage } from '../SeoArticlePage';
import { getTopicPage } from '../content';
import { articleMetadata } from '../article-metadata';

const page = getTopicPage('baby-feeding-schedule');

export const metadata: Metadata = articleMetadata(page!);

export default function BabyFeedingSchedulePage() {
  return <SeoArticlePage page={page!} />;
}
