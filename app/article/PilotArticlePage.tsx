import type { Metadata } from 'next';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import pilots from './pilot-articles.generated.json';
import { articleLanguages } from '../article-metadata';
import { SiteHeader } from '../SiteHeader';
import { SellerFooter } from '../SellerFooter';
import { siteCopy } from '../i18n';
import type { SiteLocale } from '../i18n';
import { appStoreUrl } from '../content';
import './english-article.css';

type Pilot = (typeof pilots)[number];
export const getPilot = (locale: string, slug: string) => pilots.find(p => p.locale === locale && p.slug === slug);
const languages = (p: Pilot) => p.type === 'LANG-ONLY' ? { [p.locale]: p.canonical, 'x-default': p.canonical } : articleLanguages(p.slug);
const copy = {
  de: { language: 'de', ogLocale: 'de_DE', sources: '## Quellen', nav: 'Brotkrumennavigation', home: 'Start', guides: 'Ratgeber', table: 'Übersichtstabelle', cta: 'Yorix im App Store ausprobieren' },
  pt: { language: 'pt-BR', ogLocale: 'pt_BR', sources: '## Fontes', nav: 'Navegação estrutural', home: 'Início', guides: 'Guias', table: 'Tabela informativa', cta: 'Experimentar o Yorix na App Store' },
} as const;
export function pilotMetadata(p: Pilot): Metadata {
  const ui = copy[p.locale as keyof typeof copy];
  return { title: { absolute: p.title }, description: p.description, alternates: { canonical: p.canonical, languages: languages(p) }, openGraph: { title: p.title, description: p.description, url: p.canonical, type: 'article', locale: ui.ogLocale, images: ['/og.png'] } };
}
export function PilotArticlePage({ article: p }: { article: Pilot }) {
  const ui = copy[p.locale as keyof typeof copy];
  const locale = p.locale as SiteLocale;
  const languagePaths = Object.fromEntries(Object.entries(languages(p)).filter(([language]) => language !== 'x-default')) as Partial<Record<SiteLocale, string>>;
  const sourceStart = p.body.indexOf(ui.sources);
  const sourceLines = Object.fromEntries(p.body.split('\n').map((line, i) => [i + 1, p.body.slice(0, p.body.indexOf(line)).length >= sourceStart ? line.match(/^(\d+)\. /)?.[1] : undefined]).filter(([, n]) => n));
  const body = p.body.replace(/\[(\d+)\](?!\()/g, '[$1](#quelle-$1)');
  return <main className="home-page min-h-screen text-white" lang={ui.language}>
    <SiteHeader locale={locale} languagePaths={languagePaths} />
    <article className="mx-auto max-w-4xl px-5 py-10 sm:px-8">
      <nav aria-label={ui.nav} className="mb-8 text-[#C7D2FE]"><Link href={`/${p.locale}`} prefetch={false} target="_top">{ui.home}</Link> / <Link href={`/${p.locale}/guides`} prefetch={false} target="_top">{ui.guides}</Link> / {p.heading}</nav>
      <div className="english-article-prose"><ReactMarkdown remarkPlugins={[remarkGfm]} skipHtml components={{
        li: ({ node, children }) => <li id={sourceLines[node?.position?.start.line ?? 0] ? `quelle-${sourceLines[node?.position?.start.line ?? 0]}` : undefined}>{children}</li>,
        // eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex -- Wide tables need keyboard scrolling.
        table: ({ children }) => <section className="article-table-scroll" aria-label={ui.table} tabIndex={0}><table>{children}</table></section>,
        a: ({ href, children }) => <a href={href} rel={href?.startsWith('http') ? 'noopener' : undefined}>{children}</a>,
      }}>{body}</ReactMarkdown></div>
      <a href={appStoreUrl(`guide-${p.locale}-${p.slug}`)} className="mt-8 inline-flex rounded-full bg-[#4F46E5] px-6 py-3 font-semibold">{ui.cta}</a>
    </article>
    <SellerFooter home={`/${p.locale}`} locale={locale} note={siteCopy(locale).home.footer} />
    <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(p.schema).replace(/</g, '\\u003c') }} />
  </main>;
}
