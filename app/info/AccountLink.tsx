'use client';

import { CircleCheck } from 'lucide-react';
import { useState, useSyncExternalStore } from 'react';
import type { SiteLocale } from '../i18n';
import { API_BASE } from '../subscription/config';
import { Spinner } from '../subscription/ui';
import { accountLinkCopy } from './accountLinkCopy';

type State = 'idle' | 'busy' | 'done' | 'invalid' | 'error' | 'popup';

const LINK = /^[A-Za-z0-9_-]{16,64}$/;
const noSubscription = () => () => {};
function linkFromUrl(): string {
  const found = new URLSearchParams(window.location.search).get('link') ?? '';
  return LINK.test(found) ? found : '';
}

// Shown only when the page is opened from the desk's letter (`?link=`): the
// parent signs in with Apple and the request is tied to that account, so they
// never have to find or copy an account code.
export function AccountLink({ locale }: { locale: SiteLocale }) {
  const copy = accountLinkCopy[locale];
  // The page is static: the server renders no link, the browser reads it from the address.
  const token = useSyncExternalStore(noSubscription, linkFromUrl, () => '');
  const [state, setState] = useState<State>('idle');

  if (!token && state !== 'done') return null;

  const link = async () => {
    setState('busy');
    const { appleSignInToken } = await import('../subscription/account');
    const signed = await appleSignInToken(locale);
    if ('error' in signed) {
      setState(signed.error === 'popupBlocked' ? 'popup' : signed.error === 'cancelled' ? 'idle' : 'error');
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/v1/web/support-link`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Firebase-Token': signed.token },
        body: JSON.stringify({ token }),
      });
      if (res.ok) {
        setState('done');
        window.history.replaceState(null, '', window.location.pathname);
        return;
      }
      setState(res.status === 410 || res.status === 400 ? 'invalid' : 'error');
    } catch {
      setState('error');
    }
  };

  const message = state === 'invalid' ? copy.invalid : state === 'error' ? copy.error : state === 'popup' ? copy.popup : null;
  return (
    <section className="mx-auto w-full max-w-3xl px-5 pb-4 pt-2 sm:px-8" id="link">
      <div aria-live="polite" className="rounded-[1.75rem] border border-[#FDE68A]/35 bg-[#1E1B4B]/70 p-6 backdrop-blur-xl sm:p-8">
        {state === 'done' ? (
          <p className="flex items-start gap-3 text-lg font-semibold leading-7 text-white">
            <CircleCheck aria-hidden="true" className="enter-pop mt-0.5 h-6 w-6 shrink-0 text-[#A7F3D0]" />
            {copy.done}
          </p>
        ) : (
          <>
            <h2 className="text-[1.6rem] font-semibold leading-tight text-white sm:text-[1.9rem]">{copy.title}</h2>
            <p className="mt-3 text-base leading-7 text-white/80">{copy.body}</p>
            {message ? (
              <p className="enter-rise mt-4 rounded-2xl bg-[#FDE68A]/15 px-4 py-3 text-sm font-medium text-[#FDE68A]" role="alert">
                {message}
              </p>
            ) : null}
            {state !== 'invalid' ? (
              <button
                className="mt-6 inline-flex min-h-14 w-full items-center justify-center gap-2.5 rounded-full bg-white px-7 text-base font-semibold text-[#1E1B4B] transition hover:-translate-y-0.5 hover:bg-[#EEF2FF] focus:outline-none focus-visible:ring-4 focus-visible:ring-white/30 active:translate-y-0 active:scale-[0.98] disabled:translate-y-0 disabled:opacity-70 sm:w-auto"
                disabled={state === 'busy'}
                onClick={() => void link()}
                type="button"
              >
                {state === 'busy' ? <Spinner className="h-5 w-5" /> : <AppleMark />}
                {state === 'busy' ? copy.busy : copy.button}
              </button>
            ) : null}
          </>
        )}
      </div>
    </section>
  );
}

function AppleMark() {
  return (
    <svg aria-hidden="true" className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
      <path d="M16.37 12.6c-.02-2.2 1.8-3.26 1.88-3.31-1.03-1.5-2.62-1.7-3.18-1.73-1.35-.14-2.64.8-3.33.8-.69 0-1.74-.78-2.87-.76-1.47.02-2.83.86-3.59 2.18-1.53 2.66-.39 6.6 1.1 8.76.73 1.06 1.6 2.24 2.73 2.2 1.1-.05 1.51-.71 2.84-.71 1.32 0 1.7.71 2.86.69 1.18-.02 1.93-1.07 2.65-2.13.84-1.22 1.18-2.41 1.2-2.47-.03-.01-2.3-.88-2.32-3.52zM14.2 6.13c.6-.73 1.01-1.75.9-2.76-.87.04-1.92.58-2.54 1.31-.56.65-1.05 1.69-.92 2.68.97.08 1.96-.49 2.56-1.23z" />
    </svg>
  );
}
