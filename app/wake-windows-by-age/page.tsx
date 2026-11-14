import type { Metadata } from 'next';
import { SeoArticlePage } from '../SeoArticlePage';
import { getTopicPage } from '../content';
import { articleMetadata } from '../article-metadata';

const page = getTopicPage('wake-windows-by-age');

export const metadata: Metadata = articleMetadata(page!);

export default function WakeWindowsByAgePage() {
  return <SeoArticlePage page={page!} />;
}
