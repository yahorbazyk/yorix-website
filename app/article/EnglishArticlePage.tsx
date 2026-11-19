import { Children, isValidElement, type ReactNode } from 'react';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ArrowRight, BookOpen } from 'lucide-react';
import articles from './english-articles.generated.json';
import { ArticleToc } from './ArticleToc';
import { articleLanguages } from '../article-metadata';
import { appStoreUrl } from '../content';
import { siteCopy } from '../i18n';
import { SellerFooter } from '../SellerFooter';
import { SiteHeader } from '../SiteHeader';
import { StarField } from '../subscription/StarField';
import { ScrollProgress } from '../subscription/ScrollProgress';
import './english-article.css';

function plainText(children: ReactNode): string {
  return Children.toArray(children).map((child) => {
    if (typeof child === 'string' || typeof child === 'number') return String(child);
    return isValidElement<{ children?: ReactNode }>(child) ? plainText(child.props.children) : '';
  }).join('');
}

function headingId(text: string) {
  return text.toLowerCase().replace(/[*_`]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

export function EnglishArticlePage({ slug }: { slug: string }) {
  const article = articles.find((item) => item.slug === slug);
  if (!article) throw new Error(`Missing English article: ${slug}`);
  const toc = [...article.body.matchAll(/^## (.+)$/gm)].map((match, index) => ({
    id: headingId(match[1]), label: match[1], number: index + 1,
  }));
  const store = appStoreUrl(`guide-en-${article.slug}`);
  const regressionChild = article.path.startsWith('/sleep-regression/');
  const weekMatch = article.slug.match(/^(\d+)-week-old-baby-sleep$/);
  const week = weekMatch ? Number(weekMatch[1]) : null;

  return (
    <main className="home-page relative flex min-h-screen flex-col overflow-x-clip text-white" lang="en">
      <ScrollProgress />
      <StarField />
      <div className="relative z-10">
        <SiteHeader locale="en" languagePaths={articleLanguages(article.slug)} />
        <div className="mx-auto max-w-7xl px-5 pb-16 sm:px-8 lg:px-10">
          <nav aria-label="Breadcrumb" className="mb-7 text-sm leading-7 text-[#C7D2FE]">
            {/* Match body links: this pinned runtime uses document navigation. */}
            <ol className="flex flex-wrap items-center gap-x-2">
              <li><Link href="/" prefetch={false} target="_top">Home</Link></li><li aria-hidden="true">/</li>
              <li><Link href="/guides" prefetch={false} target="_top">Guides</Link></li><li aria-hidden="true">/</li>
              {regressionChild && <><li><Link href="/sleep-regression" prefetch={false} target="_top">Sleep regression ages</Link></li><li aria-hidden="true">/</li></>}
              <li aria-current="page" className="text-white/65">{article.heading}</li>
            </ol>
          </nav>
          <div className="grid items-start gap-10 lg:grid-cols-[minmax(0,1fr)_300px] lg:gap-14">
            <article className="min-w-0" id="english-article-body">
              <div className="mb-5 flex flex-wrap items-center gap-3 text-sm text-[#C7D2FE]">
                <span className="rounded-full border border-white/20 px-3 py-1">{article.category}</span>
                <span>{article.readTime}</span>
              </div>
              <div className="english-article-prose">
                <ReactMarkdown remarkPlugins={[remarkGfm]} skipHtml components={{
                  h2: ({ children }) => <h2 id={headingId(plainText(children))}>{children}</h2>,
                  h3: ({ children }) => <h3 id={headingId(plainText(children))}>{children}</h3>,
                  a: ({ href, children }) => href?.startsWith('/')
                    // Vinext beta's RSC navigation exports fail in production.
                    // Keep Next Link semantics with normal document navigation.
                    ? <Link href={href} prefetch={false} target="_top">{children}</Link>
                    : <a href={href} rel="noopener">{children}</a>,
                  table: ({ children }) => (
                    // eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex -- Keyboard users must be able to scroll a wide table.
                    <section className="article-table-scroll" aria-label="Article reference table" tabIndex={0}><table>{children}</table></section>
                  ),
                }}>{article.body}</ReactMarkdown>
              </div>
              {week !== null && <nav aria-label="Week by week" className="mt-10 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-white/20 bg-white/5 p-4 text-sm text-[#C7D2FE]">
                {week > 1 && <Link href={`/${week - 1}-week-old-baby-sleep`} prefetch={false} target="_top" rel="prev" className="rounded-xl px-3 py-2 transition hover:bg-white/10">← Week {week - 1}</Link>}
                <Link href="/baby-sleep-by-week" prefetch={false} target="_top" className="rounded-xl px-3 py-2 font-semibold transition hover:bg-white/10">All weeks</Link>
                <Link href={week < 15 ? `/${week + 1}-week-old-baby-sleep` : '/4-month-old-sleep-schedule'} prefetch={false} target="_top" rel="next" className="rounded-xl px-3 py-2 transition hover:bg-white/10">{week < 15 ? `Week ${week + 1}` : '4 month sleep schedule'} →</Link>
              </nav>}
              <section className="mt-12 rounded-3xl border border-[#818CF8]/40 bg-[#6366F1]/15 p-6 sm:p-8" aria-label="Try Yorix">
                <BookOpen className="mb-4 h-7 w-7 text-[#C7D2FE]" aria-hidden="true" />
                <h2 className="text-2xl font-semibold">Put your baby’s day in one place</h2>
                <p className="mt-3 text-base leading-7 text-white/80">Track sleep, feeding and symptoms with Yorix, and see how the day’s pattern changes over time.</p>
                <a className="mt-5 inline-flex min-h-12 items-center gap-3 rounded-full bg-[#6366F1] px-6 py-3 font-semibold text-white transition hover:bg-[#4F46E5]" href={store} rel="noopener noreferrer" target="_blank">Try Yorix on your iPhone <ArrowRight className="h-4 w-4" aria-hidden="true" /></a>
              </section>
            </article>
            <aside className="hidden rounded-[1.75rem] lg:sticky lg:top-6 lg:block lg:max-h-[calc(100dvh-3rem)] lg:overflow-y-auto">
              <ArticleToc items={toc} title="In this guide" progressLabel="Reading progress" bodyId="english-article-body">
                <a className="mt-5 inline-flex min-h-11 w-full items-center justify-center rounded-full bg-[#6366F1] px-4 py-3 text-sm font-semibold text-white transition hover:bg-[#4F46E5]" href={store}>Download Yorix</a>
              </ArticleToc>
            </aside>
          </div>
        </div>
        <SellerFooter home="/" locale="en" note={siteCopy('en').home.footer} />
      </div>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(article.schema).replace(/</g, '\\u003c') }} />
    </main>
  );
}
