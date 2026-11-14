'use client';

import { useEffect, useRef, useState, useSyncExternalStore } from 'react';
import { usePathname } from 'next/navigation';
import type { SiteTranslation } from '../i18n/types';
import { createAnalyticsClient, publicAnalyticsPath, readAnalyticsChoice, saveAnalyticsChoice, type AnalyticsChoice } from './measurement';

type Props = {
  copy: SiteTranslation['analyticsConsent'];
  siteUrl: string;
  appStoreId: string;
  basePaths: string[];
  additionalPaths: string[];
  locales: string[];
  privacyPath: string;
};

const subscribeHydration = () => () => {};
const clientReady = () => true;
const serverReady = () => false;

function initialChoice(): AnalyticsChoice | null {
  if (typeof window === 'undefined') return null;
  try { return readAnalyticsChoice(window.localStorage); } catch { return null; }
}

export function AnalyticsConsent({ copy, privacyPath, ...settings }: Props) {
  const pathname = usePathname() ?? '/';
  const ready = useSyncExternalStore(subscribeHydration, clientReady, serverReady);
  const [choice, setChoice] = useState<AnalyticsChoice | null>(initialChoice);
  const [editing, setEditing] = useState(false);
  const client = useRef<ReturnType<typeof createAnalyticsClient> | null>(null);
  const settingsRef = useRef(settings);

  useEffect(() => {
    client.current = createAnalyticsClient(window, document, settingsRef.current);
    return () => client.current?.dispose();
  }, []);

  useEffect(() => {
    if (ready) client.current?.update(pathname, choice === 'granted');
  }, [choice, pathname, ready]);

  useEffect(() => {
    const sync = () => {
      try { setChoice(readAnalyticsChoice(window.localStorage)); } catch { setChoice(null); }
    };
    window.addEventListener('storage', sync);
    return () => window.removeEventListener('storage', sync);
  }, []);

  function choose(next: AnalyticsChoice) {
    try { saveAnalyticsChoice(window.localStorage, next); } catch { /* Keep the choice for this page. */ }
    const withdrawing = choice === 'granted' && next === 'denied';
    if (next === 'denied') {
      client.current?.disable();
      client.current?.clearCookies();
    }
    setChoice(next);
    setEditing(false);
    // Remove the loaded SDK and its automatic handlers after withdrawal.
    if (withdrawing) window.location.reload();
  }

  if (!ready) return null;
  const publicPage = publicAnalyticsPath(pathname, settings.basePaths, settings.locales, settings.additionalPaths);
  const visible = editing || (publicPage && choice === null);
  const button = 'min-h-10 rounded-full border border-[#818CF8]/50 px-5 py-2 text-sm font-semibold transition hover:-translate-y-0.5 hover:border-white focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-white';

  return (
    <>
      {visible && (
        <section aria-label={copy.title} className="fixed inset-x-4 bottom-4 z-[100] mx-auto max-w-xl rounded-3xl border border-[#818CF8]/50 bg-[#1E1B4B] p-5 text-white motion-safe:animate-[yorix-consent-in_180ms_ease-out] sm:p-6">
          <h2 className="text-lg font-semibold">{copy.title}</h2>
          <p className="mt-2 text-sm leading-6 text-white/80">{copy.body}</p>
          <a className="mt-2 inline-block text-sm text-[#C7D2FE] underline underline-offset-4 hover:text-white" href={privacyPath}>{copy.privacy}</a>
          <div className="mt-4 flex flex-wrap gap-3">
            <button className={button} onClick={() => choose('denied')} type="button">{copy.reject}</button>
            <button className={`${button} bg-[#4F46E5]`} onClick={() => choose('granted')} type="button">{copy.accept}</button>
            {choice !== null && <button className="ms-auto px-2 text-sm text-white/75 underline hover:text-white" onClick={() => setEditing(false)} type="button">{copy.close}</button>}
          </div>
        </section>
      )}
      {!visible && (
        <button className="fixed bottom-3 start-3 z-[90] rounded-full border border-[#818CF8]/40 bg-[#1E1B4B] px-3 py-2 text-xs text-[#E0E7FF] transition hover:border-white hover:text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#818CF8]" onClick={() => setEditing(true)} type="button">
          {copy.settings}
        </button>
      )}
    </>
  );
}
