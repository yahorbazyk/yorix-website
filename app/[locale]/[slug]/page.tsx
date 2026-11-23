import pilots from '../../article/pilot-articles.generated.json';
import { getPilot, pilotMetadata, PilotArticlePage } from '../../article/PilotArticlePage';
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
  return [...pilots.map(p => ({ locale: p.locale, slug: p.slug })), ...translatedArticleSlugs.filter((slug) => !isRetiredArticle(slug)).flatMap((slug) =>
    getTranslatedLocalesForArticle(slug).filter(locale => !getPilot(locale, slug)).map((locale) => ({ locale, slug })),
  )];
}

export function generateMetadata({ params }: LocalizedArticleRouteProps): Metadata {
  const pilot = getPilot(params.locale, params.slug);
  if (pilot) return pilotMetadata(pilot);
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
  const pilot = getPilot(params.locale, params.slug);
  if (pilot) return <PilotArticlePage article={pilot} />;
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
