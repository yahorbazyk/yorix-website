// Public identifiers; no API secret is needed for browser measurement.
export const GA_MEASUREMENT_ID = 'G-NBZ2G9XC1E';
export const ANALYTICS_CHOICE_KEY = 'yorix-analytics-consent-v1';
export const CONSENT_LIFETIME = 180 * 24 * 60 * 60;
export type AnalyticsChoice = 'granted' | 'denied';

export function readAnalyticsChoice(storage: Pick<Storage, 'getItem'>, now = Date.now()): AnalyticsChoice | null {
  try {
    const saved = JSON.parse(storage.getItem(ANALYTICS_CHOICE_KEY) ?? 'null');
    return saved && (saved.choice === 'granted' || saved.choice === 'denied') &&
      typeof saved.expires === 'number' && saved.expires > now ? saved.choice : null;
  } catch {
    return null;
  }
}

export function saveAnalyticsChoice(storage: Pick<Storage, 'setItem'>, choice: AnalyticsChoice, now = Date.now()) {
  try {
    storage.setItem(ANALYTICS_CHOICE_KEY, JSON.stringify({ choice, expires: now + CONSENT_LIFETIME * 1000 }));
  } catch {
    // Consent still applies in memory if this browser does not allow storage.
  }
}

// Only public marketing routes are measured. Gift codes, checkout, support
// form values, URL queries and fragments never become event parameters.
export function publicAnalyticsPath(pathname: string, basePaths: readonly string[], locales: readonly string[], additionalPaths: readonly string[] = []): string | null {
  const path = pathname.replace(/\/$/, '') || '/';
  if (additionalPaths.includes(path)) return path;
  const parts = path.split('/');
  const localized = locales.includes(parts[1]);
  const base = localized ? '/' + parts.slice(2).join('/') : path;
  return basePaths.includes(base) ? path : null;
}

type Settings = {
  siteUrl: string;
  appStoreId: string;
  basePaths: readonly string[];
  locales: readonly string[];
  additionalPaths?: readonly string[];
};
type AnalyticsWindow = Window & {
  dataLayer?: IArguments[];
  gtag?: (...args: unknown[]) => void;
};

export function createAnalyticsClient(browser: AnalyticsWindow, doc: Document, settings: Settings) {
  const origin = new URL(settings.siteUrl).origin;
  const disableKey = `ga-disable-${GA_MEASUREMENT_ID}`;
  const flags = browser as unknown as Record<string, unknown>;
  let configured = false;
  let lastPage: string | null = null;
  let stopListeners = () => {};

  const command = (...args: unknown[]) => browser.gtag?.(...args);
  function disable() {
    flags[disableKey] = true;
    stopListeners();
    lastPage = null;
  }

  function clearCookies() {
    const names = ['_ga', `_ga_${GA_MEASUREMENT_ID.slice(2)}`];
    const hostname = new URL(origin).hostname;
    for (const name of names) {
      for (const domain of ['', `; Domain=${hostname}`, `; Domain=.${hostname}`]) {
        doc.cookie = `${name}=; Max-Age=0; Path=/; SameSite=Lax${domain}`;
      }
    }
  }

  function update(pathname: string, consent: boolean) {
    const path = publicAnalyticsPath(pathname, settings.basePaths, settings.locales, settings.additionalPaths);
    if (!consent || !path || browser.location.hostname !== new URL(origin).hostname) {
      disable();
      if (!consent) clearCookies();
      return;
    }
    flags[disableKey] = false;
    if (lastPage === path) return;
    stopListeners();
    browser.dataLayer ??= [];
    // Match Google's standard gtag bootstrap: queue an arguments object.
    // eslint-disable-next-line prefer-rest-params
    browser.gtag ??= function () { browser.dataLayer!.push(arguments); };
    const referrer = (() => {
      try {
        const url = new URL(doc.referrer);
        if (!['http:', 'https:'].includes(url.protocol)) return '';
        if (url.origin !== origin) return url.origin + '/';
        const safePath = publicAnalyticsPath(url.pathname, settings.basePaths, settings.locales, settings.additionalPaths);
        return safePath ? origin + safePath : '';
      } catch { return ''; }
    })();
    const page = { page_location: origin + path, page_referrer: referrer, page_title: doc.title };
    if (!configured) {
      command('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
      command('set', 'ads_data_redaction', true);
      command('js', new Date());
      command('consent', 'update', { analytics_storage: 'granted' });
      command('config', GA_MEASUREMENT_ID, {
        ...page, send_page_view: false, allow_google_signals: false,
        allow_ad_personalization_signals: false,
        cookie_expires: CONSENT_LIFETIME, cookie_update: false,
      });
      configured = true;
    }
    command('set', page);
    command('event', 'page_view', { ...page, send_to: GA_MEASUREMENT_ID });
    lastPage = path;
    let scrolled = false;
    const scroll = () => {
      const distance = doc.documentElement.scrollHeight - browser.innerHeight;
      if (!scrolled && distance > 0 && browser.scrollY / distance >= 0.9) {
        scrolled = true;
        command('event', 'scroll', { ...page, percent_scrolled: 90, send_to: GA_MEASUREMENT_ID });
      }
    };
    const click = (event: Event) => {
      const link = (event.target as Element | null)?.closest?.('a[href]') as HTMLAnchorElement | null;
      if (!link) return;
      try {
        const url = new URL(link.href);
        if (url.hostname !== 'apps.apple.com' || !url.pathname.endsWith(`/id${settings.appStoreId}`)) return;
        command('event', 'app_store_click', {
          ...page, link_domain: 'apps.apple.com',
          link_url: `https://apps.apple.com/app/id${settings.appStoreId}`,
          send_to: GA_MEASUREMENT_ID,
        });
      } catch { /* Ignore non-URL links. */ }
    };
    browser.addEventListener('scroll', scroll, { passive: true });
    doc.addEventListener('click', click, true);
    stopListeners = () => {
      browser.removeEventListener('scroll', scroll);
      doc.removeEventListener('click', click, true);
    };
    if (!doc.querySelector('script[data-yorix-analytics]')) {
      const script = doc.createElement('script');
      script.async = true;
      script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
      script.dataset.yorixAnalytics = '';
      const nonce = doc.querySelector<HTMLScriptElement>('script[nonce]')?.nonce;
      if (nonce) script.nonce = nonce;
      doc.head.appendChild(script);
    }
  }

  return { update, disable, clearCookies, dispose: disable };
}
