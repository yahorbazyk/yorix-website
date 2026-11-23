import pilots from './article/pilot-articles.generated.json';
import type { Metadata } from 'next';
import { translatedArticleAlternates } from './article-localizations';
import { siteUrl, type TopicPage } from './content';
import { localeCopy, type Locale } from './locales';

// Every language in an article cluster must publish the same return links.
export function articleLanguages(slug: string) {
  return { 'x-default': `/${slug}`, en: `/${slug}`, ...translatedArticleAlternates(slug), ...Object.fromEntries(pilots.filter(p => p.slug === slug && p.type !== 'LANG-ONLY').map(p => [p.locale, `/${p.locale}/${p.slug}`])) };
}

export function articleMetadata(page: TopicPage, locale?: Locale): Metadata {
  const path = `${locale ? `/${locale}` : ''}/${page.slug}`;
  return {
    title: page.title,
    description: page.description,
    alternates: { canonical: path, languages: articleLanguages(page.slug) },
    openGraph: {
      title: page.title,
      description: page.description,
      url: `${siteUrl}${path}`,
      type: 'article',
      locale: locale ? localeCopy[locale].ogLocale : 'en_US',
    },
    twitter: {
      card: 'summary',
      title: page.title,
      description: page.description,
      images: ['/og.png'],
    },
  };
}
