import { EnglishArticlePage } from '../article/EnglishArticlePage';
import { englishArticleMetadata, getEnglishArticle } from '../article/english-catalog';

export const metadata = englishArticleMetadata(getEnglishArticle('sleep-regression')!);

export default function SleepRegressionPage() {
  return <EnglishArticlePage slug="sleep-regression" />;
}
