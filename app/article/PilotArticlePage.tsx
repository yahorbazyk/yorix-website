import type { Metadata } from 'next';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import pilots from './pilot-articles.generated.json';
import { articleLanguages } from '../article-metadata';
import { SiteHeader } from '../SiteHeader';
import { SellerFooter } from '../SellerFooter';
import { siteCopy } from '../i18n';
import { appStoreUrl } from '../content';
import './english-article.css';

type Pilot = (typeof pilots)[number];
export const getPilot = (locale: string, slug: string) => pilots.find(p => p.locale === locale && p.slug === slug);
const languages = (p: Pilot) => p.type === 'LANG-ONLY' ? { de: p.canonical, 'x-default': p.canonical } : articleLanguages(p.slug);
export function pilotMetadata(p: Pilot): Metadata {
  return { title: { absolute: p.title }, description: p.description, alternates: { canonical: p.canonical, languages: languages(p) }, openGraph: { title: p.title, description: p.description, url: p.canonical, type: 'article', locale: 'de_DE', images: ['/og.png'] } };
}
export function PilotArticlePage({ article: p }: { article: Pilot }) {
  const sourceStart = p.body.indexOf('## Quellen');
  const sourceLines = Object.fromEntries(p.body.split('\n').map((line, i) => [i + 1, p.body.slice(0, p.body.indexOf(line)).length >= sourceStart ? line.match(/^(\d+)\. /)?.[1] : undefined]).filter(([, n]) => n));
  const body = p.body.replace(/\[(\d+)\](?!\()/g, '[$1](#quelle-$1)');
  return <main className="home-page min-h-screen text-white" lang="de">
    <SiteHeader locale="de" languagePaths={languages(p)} />
    <article className="mx-auto max-w-4xl px-5 py-10 sm:px-8">
      <nav aria-label="Brotkrumennavigation" className="mb-8 text-[#C7D2FE]"><Link href="/de" prefetch={false} target="_top">Start</Link> / <Link href="/de/guides" prefetch={false} target="_top">Ratgeber</Link> / {p.heading}</nav>
      <div className="english-article-prose"><ReactMarkdown remarkPlugins={[remarkGfm]} skipHtml components={{
        li: ({ node, children }) => <li id={sourceLines[node?.position?.start.line ?? 0] ? `quelle-${sourceLines[node?.position?.start.line ?? 0]}` : undefined}>{children}</li>,
        // eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex -- Wide tables need keyboard scrolling.
        table: ({ children }) => <section className="article-table-scroll" aria-label="Übersichtstabelle" tabIndex={0}><table>{children}</table></section>,
        a: ({ href, children }) => <a href={href} rel={href?.startsWith('http') ? 'noopener' : undefined}>{children}</a>,
      }}>{body}</ReactMarkdown></div>
      <a href={appStoreUrl(`guide-de-${p.slug}`)} className="mt-8 inline-flex rounded-full bg-[#4F46E5] px-6 py-3 font-semibold">Yorix im App Store ausprobieren</a>
    </article>
    <SellerFooter home="/de" locale="de" note={siteCopy('de').home.footer} />
    <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(p.schema).replace(/</g, '\\u003c') }} />
  </main>;
}
