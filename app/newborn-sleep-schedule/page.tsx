import type { Metadata } from 'next';
import { SeoArticlePage } from '../SeoArticlePage';
import { getTopicPage } from '../content';
import { articleMetadata } from '../article-metadata';

const page = getTopicPage('newborn-sleep-schedule');

export const metadata: Metadata = articleMetadata(page!);

export default function NewbornSleepSchedulePage() {
  return <SeoArticlePage page={page!} />;
}
