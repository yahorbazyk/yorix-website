import type { Metadata } from 'next';
import { SeoArticlePage } from '../SeoArticlePage';
import { getTopicPage } from '../content';
import { articleMetadata } from '../article-metadata';

const page = getTopicPage('baby-nap-schedule-by-age');

export const metadata: Metadata = articleMetadata(page!);

export default function BabyNapScheduleByAgePage() {
  return <SeoArticlePage page={page!} />;
}
