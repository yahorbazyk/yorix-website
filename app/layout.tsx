import type { Metadata } from 'next';
import { headers } from 'next/headers';
import { appStoreId, siteUrl, topicPages } from './content';
import { DOCUMENT_LOCALE_HEADER, isLocale, localeAlternates, locales } from './locales';
import { siteCopy } from './i18n';
import { campaignLocales } from './i18n/campaigns/instagram';
import { AnalyticsConsent } from './analytics/AnalyticsConsent';
import { Spotlight } from './subscription/Spotlight';
import { SmoothScroll } from './SmoothScroll';
import './globals.css';

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: 'Baby Schedule App | Calm Nap and Feeding Routine',
    template: '%s | Yorix',
  },
  description:
    'Build a calmer baby schedule with nap windows, feeding rhythm, sleep tracking, and gentle routine support for parents.',
  alternates: {
    canonical: '/',
    languages: {
      'x-default': '/',
      en: '/',
      ...localeAlternates(),
    },
  },
  openGraph: {
    title: 'Baby Schedule App | Calm Nap and Feeding Routine',
    description:
      'Track sleep, feeds, diapers, and daily rhythm to create a baby schedule that follows your real day.',
    url: '/',
    siteName: 'Yorix',
    type: 'website',
    locale: 'en_US',
    images: [
      {
        url: '/og.png',
        width: 1024,
        height: 1024,
        alt: 'Yorix app icon with a sleeping baby on a crescent moon',
      },
    ],
  },
  twitter: {
    card: 'summary',
    // Inherit each page's localized Open Graph title and description.
    images: ['/og.png'],
  },
  icons: {
    icon: '/app-icon.png',
    shortcut: '/app-icon.png',
    apple: '/app-icon.png',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const value = (await headers()).get(DOCUMENT_LOCALE_HEADER) ?? 'en';
  const locale = isLocale(value) ? value : 'en';
  return (
    <html lang={locale} dir={locale === 'ar' || locale === 'he' ? 'rtl' : 'ltr'}>
      <body>
        <SmoothScroll />
        <Spotlight />
        {children}
        <AnalyticsConsent
          additionalPaths={campaignLocales.map((language) => `/${language}/start`)}
          appStoreId={appStoreId}
          basePaths={['/', '/guides', '/about', '/support', ...topicPages.map((page) => `/${page.slug}`)]}
          copy={siteCopy(locale).analyticsConsent}
          locales={[...locales]}
          privacyPath={locale === 'ru' ? '/ru/subscription/privacy' : '/subscription/privacy'}
          siteUrl={siteUrl}
        />
      </body>
    </html>
  );
}
