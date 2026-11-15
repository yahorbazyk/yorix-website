import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { HomeLanding } from '../home/HomeLanding';
import { EnglishArticlePage } from '../article/EnglishArticlePage';
import { englishArticles, englishArticleMetadata, getEnglishArticle } from '../article/english-catalog';
import { siteUrl } from '../content';
import { siteCopy } from '../i18n';
import { isLocale, localeAlternates, localeCopy, locales } from '../locales';

type ArticleRouteProps = {
  params: {
    locale: string;
  };
};

export function generateStaticParams() {
  return [
    ...englishArticles.filter((article) => !article.slug.includes('/')).map((article) => ({ locale: article.slug })),
    ...locales.map((locale) => ({ locale })),
  ];
}

export function generateMetadata({ params }: ArticleRouteProps): Metadata {
  if (isLocale(params.locale)) {
    const copy = { ...siteCopy(params.locale).home, ogLocale: localeCopy[params.locale].ogLocale };

    return {
      title: `Yorix | ${copy.hero.title}`,
      description: copy.hero.body,
      alternates: {
        canonical: `/${params.locale}`,
        languages: {
          'x-default': '/',
          en: '/',
          ...localeAlternates(),
        },
      },
      openGraph: {
        title: `Yorix | ${copy.hero.title}`,
        description: copy.hero.body,
        url: `${siteUrl}/${params.locale}`,
        type: 'website',
        locale: copy.ogLocale,
      },
    };
  }

  const page = getEnglishArticle(params.locale);

  if (!page) {
    return {};
  }

  return englishArticleMetadata(page);
}

export default function ArticleRoute({ params }: ArticleRouteProps) {
  if (isLocale(params.locale)) {
    return <HomeLanding locale={params.locale} />;
  }

  const page = getEnglishArticle(params.locale);

  if (!page) {
    notFound();
  }

  return <EnglishArticlePage slug={page.slug} />;
}
