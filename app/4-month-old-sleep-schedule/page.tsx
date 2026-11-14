import type { Metadata } from 'next';
import { SeoArticlePage } from '../SeoArticlePage';
import { getTopicPage } from '../content';
import { articleMetadata } from '../article-metadata';

const page = getTopicPage('4-month-old-sleep-schedule');

export const metadata: Metadata = articleMetadata(page!);

export default function FourMonthOldSleepSchedulePage() {
  return <SeoArticlePage page={page!} />;
}
