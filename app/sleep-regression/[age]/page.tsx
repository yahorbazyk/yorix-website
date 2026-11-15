import { notFound } from 'next/navigation';
import { EnglishArticlePage } from '../../article/EnglishArticlePage';
import { englishArticles, englishArticleMetadata, getEnglishArticle } from '../../article/english-catalog';

type Props = { params: { age: string } };

export function generateStaticParams() {
  return englishArticles.filter((article) => article.slug.startsWith('sleep-regression/'))
    .map((article) => ({ age: article.slug.split('/')[1] }));
}

export function generateMetadata({ params }: Props) {
  const article = getEnglishArticle(`sleep-regression/${params.age}`);
  return article ? englishArticleMetadata(article) : {};
}

export default function RegressionAgePage({ params }: Props) {
  const article = getEnglishArticle(`sleep-regression/${params.age}`);
  if (!article) notFound();
  return <EnglishArticlePage slug={article.slug} />;
}
