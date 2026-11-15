import type { Metadata } from 'next';
import catalog from './english-catalog.generated.json';
import { articleLanguages } from '../article-metadata';

export const englishArticles = catalog;
export type EnglishArticleSummary = (typeof catalog)[number];

export function getEnglishArticle(slug: string) {
  return englishArticles.find((article) => article.slug === slug);
}

export function englishArticleMetadata(article: EnglishArticleSummary): Metadata {
  return {
    title: { absolute: article.title },
    description: article.description,
    alternates: { canonical: article.canonical, languages: articleLanguages(article.slug) },
    openGraph: {
      title: article.title, description: article.description, url: article.canonical,
      type: 'article', locale: 'en_US', siteName: 'Yorix',
      publishedTime: article.published, modifiedTime: article.updated,
      images: [{ url: '/og.png', width: 1024, height: 1024, alt: 'Yorix' }],
    },
    twitter: { card: 'summary', title: article.title, description: article.description, images: ['/og.png'] },
  };
}

export const englishGuideCards = englishArticles.map((article) => ({
  ...article, href: article.path, title: article.heading, date: article.updated,
  coverClass: 'from-[#1E1B4B] via-[#312E81] to-[#6366F1]',
})).sort((a, b) => {
  const rank = (slug: string) => {
    if (slug === 'newborn-sleep-schedule' || slug === 'sleep-regression') return 0;
    if (slug.endsWith('2-years')) return 24;
    return Number(slug.match(/(?:^|\/)(\d+)-month/)?.[1] ?? 100);
  };
  return rank(a.slug) - rank(b.slug);
});
