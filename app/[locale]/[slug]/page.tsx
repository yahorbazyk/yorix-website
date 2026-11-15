import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import {
  getLocalizedTopicPage,
  getTranslatedLocalesForArticle,
  isTranslatedArticleSlug,
  translatedArticleSlugs,
} from '../../article-localizations';
import { SeoArticlePage } from '../../SeoArticlePage';
import { articleMetadata } from '../../article-metadata';
import { isLocale, type Locale } from '../../locales';
import { isRetiredArticle } from '../../article/merges';

type LocalizedArticleRouteProps = {
  params: {
    locale: string;
    slug: string;
  };
};

export function generateStaticParams() {
  return translatedArticleSlugs.filter((slug) => !isRetiredArticle(slug)).flatMap((slug) =>
    getTranslatedLocalesForArticle(slug).map((locale) => ({ locale, slug })),
  );
}

export function generateMetadata({ params }: LocalizedArticleRouteProps): Metadata {
  if (!isLocale(params.locale) || !isTranslatedArticleSlug(params.slug)) {
    return {};
  }

  const page = getLocalizedTopicPage(params.locale, params.slug);

  if (!page) {
    return {};
  }

  return articleMetadata(page, params.locale);
}

export default function LocalizedArticleRoute({ params }: LocalizedArticleRouteProps) {
  if (!isLocale(params.locale) || !isTranslatedArticleSlug(params.slug)) {
    notFound();
  }

  const locale = params.locale as Locale;
  const page = getLocalizedTopicPage(locale, params.slug);

  if (!page) {
    notFound();
  }

  return <SeoArticlePage page={page} locale={locale} />;
}
