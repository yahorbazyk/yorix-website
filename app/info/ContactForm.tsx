'use client';

import { CircleCheck, Send } from 'lucide-react';
import { useEffect, useRef, useState, type SubmitEvent } from 'react';
import type { SiteLocale } from '../i18n';
import type { SupportCopy } from '../i18n/types';
import { API_BASE, turnstileSiteKey } from '../subscription/config';
import { Spinner } from '../subscription/ui';
import { AppleMark, GoogleMark } from './AccountLink';
import { accountLinkCopy } from './accountLinkCopy';

type State = 'idle' | 'sending' | 'sent' | 'invalid' | 'error';
type Account = 'none' | 'apple' | 'google' | 'linked';

// The worker accepts plain addresses only (no quotes, brackets or display names).
const EMAIL = /^[A-Za-z0-9._%+'-]{1,64}@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,24}$/;

const text = (value: FormDataEntryValue | null) => (typeof value === 'string' ? value : '');

// «Write to us» without a mail app and without an address on the page: the
// worker mails the message to support with the writer as Reply-To. The hidden
// field and the time on the page are what the worker uses to drop bots
// without telling them.
export function ContactForm({ copy, lang, page }: { copy: SupportCopy['form']; lang: string; page: string }) {
  const opened = useRef(0);
  const [state, setState] = useState<State>('idle');
  const [account, setAccount] = useState<Account>('none');
  const [accountError, setAccountError] = useState<string | null>(null);
  const linkCopy = accountLinkCopy[lang as SiteLocale] ?? accountLinkCopy.en;
  useEffect(() => {
    opened.current = Date.now();
    // Already signed in on the site (bought here before): the message goes out linked.
    void import('../subscription/account')
      .then((m) => m.signedInToken())
      .then((token) => { if (token) setAccount('linked'); })
      .catch(() => {});
  }, []);
  const linkAccount = async (kind: 'apple' | 'google') => {
    setAccount(kind);
    setAccountError(null);
    const { accountSignInToken } = await import('../subscription/account');
    const signed = await accountSignInToken(kind, lang);
    if ('error' in signed) {
      setAccount('none');
      if (signed.error !== 'cancelled') setAccountError(signed.error === 'popupBlocked' ? linkCopy.popup : linkCopy.error);
      return;
    }
    setAccount('linked');
  };
  // The widget writes its answer into a hidden field of this form.
  useEffect(() => {
    if (!turnstileSiteKey || document.querySelector('script[data-turnstile]')) return;
    const script = document.createElement('script');
    script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js';
    script.async = true;
    script.defer = true;
    script.dataset.turnstile = 'true';
    document.head.appendChild(script);
  }, []);

  const submit = async (event: SubmitEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (state === 'sending') return;
    const form = new FormData(event.currentTarget);
    const payload = {
      name: text(form.get('name')).trim(),
      email: text(form.get('email')).trim(),
      message: text(form.get('message')).trim(),
      website: text(form.get('website')),
      turnstile: text(form.get('cf-turnstile-response')),
      lang,
      page,
      elapsedMs: Date.now() - opened.current,
    };
    if (!EMAIL.test(payload.email) || payload.message.length < 10) {
      setState('invalid');
      return;
    }
    setState('sending');
    try {
      const token = account === 'linked' ? await import('../subscription/account').then((m) => m.signedInToken()).catch(() => null) : null;
      const res = await fetch(`${API_BASE}/v1/web/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(token ? { 'X-Firebase-Token': token } : {}) },
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        setState('sent');
        return;
      }
      const body = (await res.json().catch(() => ({}))) as { error?: string };
      setState(body.error === 'invalid_email' || body.error === 'invalid_message' ? 'invalid' : 'error');
    } catch {
      setState('error');
    }
  };

  if (state === 'sent') {
    return (
      <output className="flex min-h-[16rem] flex-col items-center justify-center gap-4 text-center">
        <CircleCheck aria-hidden="true" className="enter-pop h-14 w-14 text-[#A7F3D0]" />
        <span className="enter-rise max-w-sm text-lg font-semibold leading-7 text-white [animation-delay:180ms]">{copy.sent}</span>
      </output>
    );
  }

  const label = 'block text-sm font-semibold text-white';
  const field =
    'mt-2 w-full rounded-2xl border border-white/20 bg-white/[0.08] px-4 py-3 text-base text-white placeholder:text-white/40 transition focus:border-[#FDE68A]/80 focus:bg-white/[0.12] focus:outline-none';
  const alert = 'enter-rise rounded-2xl bg-[#FDE68A]/15 px-4 py-3 text-sm font-medium text-[#FDE68A]';
  return (
    <form className="grid gap-4" noValidate onSubmit={(event) => void submit(event)}>
      <div className="grid gap-4 sm:grid-cols-2">
        <label className={label}>
          {copy.name}
          <input autoComplete="name" className={field} maxLength={80} name="name" />
        </label>
        <label className={label}>
          {copy.email}
          <input autoComplete="email" className={field} inputMode="email" maxLength={254} name="email" required type="email" />
        </label>
      </div>
      <label className={label}>
        {copy.message}
        <textarea className={`${field} min-h-36 resize-y`} maxLength={4000} minLength={10} name="message" placeholder={copy.messagePlaceholder} required />
      </label>
      <div className="rounded-2xl border border-white/15 bg-white/[0.05] p-4">
        {account === 'linked' ? (
          <p className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm font-medium text-white">
            <CircleCheck aria-hidden="true" className="h-5 w-5 shrink-0 text-[#A7F3D0]" />
            <span className="flex-1">{linkCopy.formLinked}</span>
            <button className="text-sm font-semibold text-white/75 underline decoration-white/30 underline-offset-4 hover:text-white" onClick={() => setAccount('none')} type="button">
              {linkCopy.formChange}
            </button>
          </p>
        ) : (
          <>
            <p className="text-sm font-semibold text-white">{linkCopy.formTitle}</p>
            <p className="mt-1 text-sm leading-6 text-white/70">{linkCopy.formHint}</p>
            <div className="mt-3 grid gap-2 sm:grid-cols-2">
              {(['apple', 'google'] as const).map((kind) => (
                <button
                  className="inline-flex min-h-12 items-center justify-center gap-2 rounded-full border border-white/25 bg-white/[0.08] px-4 text-sm font-semibold text-white transition hover:bg-white/[0.14] focus:outline-none focus-visible:ring-4 focus-visible:ring-white/30 disabled:opacity-60"
                  disabled={account === 'apple' || account === 'google'}
                  key={kind}
                  onClick={() => void linkAccount(kind)}
                  type="button"
                >
                  {account === kind ? <Spinner className="h-4 w-4" /> : kind === 'apple' ? <AppleMark /> : <GoogleMark />}
                  {kind === 'apple' ? linkCopy.button : linkCopy.google}
                </button>
              ))}
            </div>
            {accountError ? (
              <p className="mt-3 text-sm font-medium text-[#FDE68A]" role="alert">
                {accountError}
              </p>
            ) : null}
          </>
        )}
      </div>
      {turnstileSiteKey ? <div className="cf-turnstile" data-language={lang} data-sitekey={turnstileSiteKey} data-theme="dark" /> : null}
      {/* Humans never see or fill this; bots do. */}
      <input aria-hidden="true" autoComplete="off" className="absolute -left-[9999px] h-px w-px opacity-0" name="website" tabIndex={-1} />
      {state === 'invalid' ? (
        <p className={alert} role="alert">
          {copy.invalid}
        </p>
      ) : null}
      {state === 'error' ? (
        <p className={alert} role="alert">
          {copy.error}
        </p>
      ) : null}
      <button
        className="group inline-flex min-h-14 w-full items-center justify-center gap-2.5 rounded-full bg-white px-7 text-base font-semibold text-[#1E1B4B] shadow-[0_18px_50px_rgb(255_255_255/14%)] transition hover:-translate-y-0.5 hover:bg-[#EEF2FF] focus:outline-none focus-visible:ring-4 focus-visible:ring-white/30 active:translate-y-0 active:scale-[0.98] disabled:translate-y-0 disabled:scale-100 disabled:opacity-70"
        disabled={state === 'sending'}
        type="submit"
      >
        {state === 'sending' ? <Spinner className="h-5 w-5" /> : <Send aria-hidden="true" className="h-5 w-5 transition-transform duration-300 group-hover:-translate-y-0.5 group-hover:translate-x-0.5 rtl:-scale-x-100 rtl:group-hover:-translate-x-0.5" />}
        {state === 'sending' ? copy.sending : copy.send}
      </button>
    </form>
  );
}
