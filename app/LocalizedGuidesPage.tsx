import pilots from './article/pilot-articles.generated.json';
import { getLocalizedTopicPages } from './article-localizations';
import { GuidesIndex } from './home/GuidesIndex';
import { siteCopy } from './i18n';
import type { Locale } from './locales';

export function LocalizedGuidesPage({ locale }: { locale: Locale }) {
  const copy = siteCopy(locale);

  return (
    <GuidesIndex
      body={copy.guides.body}
      cta={copy.home.cta}
      eyebrow={copy.guides.eyebrow}
      footer={copy.articleUi.footer}
      guides={[...getLocalizedTopicPages(locale).filter(page => !pilots.some(p => p.locale === locale && p.slug === page.slug)).map(page => ({ ...page, href: `/${locale}/${page.slug}` })), ...pilots.filter(p => p.locale === locale).map(p => ({ ...p, href: `/${locale}/${p.slug}` }))]}
      home={`/${locale}`}
      locale={locale}
      title={copy.guides.title}
    />
  );
}
