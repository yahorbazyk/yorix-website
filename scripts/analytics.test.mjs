import assert from 'node:assert/strict';
import test from 'node:test';
import {
  ANALYTICS_CHOICE_KEY, CONSENT_LIFETIME, GA_MEASUREMENT_ID,
  createAnalyticsClient, publicAnalyticsPath, readAnalyticsChoice, saveAnalyticsChoice,
} from '../app/analytics/measurement.ts';

const settings = {
  siteUrl: 'https://yorix-app.com', appStoreId: '6788705252',
  basePaths: ['/', '/guides', '/support', '/4-month-old-sleep-schedule'],
  locales: ['ru', 'ar', 'fr'],
  additionalPaths: ['/ru/start', '/ar/start', '/en/start'],
};

function fixture(hostname = 'yorix-app.com') {
  const scripts = [], cookies = [], windowListeners = new Map(), documentListeners = new Map();
  const doc = {
    title: 'Sleep guide', referrer: 'https://www.google.com/search?q=private-example',
    documentElement: { scrollHeight: 2000 },
    set cookie(value) { cookies.push(value); },
    querySelector(selector) { return selector === 'script[nonce]' ? { nonce: 'trusted-nonce' } : scripts[0]; },
    createElement() { return { dataset: {} }; },
    head: { appendChild(script) { scripts.push(script); } },
    addEventListener(name, fn) { documentListeners.set(name, fn); },
    removeEventListener(name) { documentListeners.delete(name); },
  };
  const browser = {
    location: { hostname }, innerHeight: 1000, scrollY: 0,
    addEventListener(name, fn) { windowListeners.set(name, fn); },
    removeEventListener(name) { windowListeners.delete(name); },
  };
  const client = createAnalyticsClient(browser, doc, settings);
  const commands = () => (browser.dataLayer ?? []).map(args => Array.from(args));
  const events = () => commands().filter(args => args[0] === 'event');
  return { client, browser, doc, scripts, cookies, commands, events, windowListeners, documentListeners };
}

test('consent is optional, expiring, and resilient to unavailable browser storage', () => {
  let stored;
  const storage = { getItem: () => stored ?? null, setItem: (key, value) => { assert.equal(key, ANALYTICS_CHOICE_KEY); stored = value; } };
  assert.equal(readAnalyticsChoice(storage, 1000), null);
  saveAnalyticsChoice(storage, 'granted', 1000);
  assert.equal(readAnalyticsChoice(storage, 1000), 'granted');
  assert.equal(readAnalyticsChoice(storage, 1000 + CONSENT_LIFETIME * 1000), null);
  stored = '{invalid';
  assert.equal(readAnalyticsChoice(storage), null);
  assert.equal(readAnalyticsChoice({ getItem() { throw new Error('blocked'); } }), null);
  assert.doesNotThrow(() => saveAnalyticsChoice({ setItem() { throw new Error('blocked'); } }, 'denied'));
});

test('only known public pages are measured, including their translations', () => {
  for (const path of ['/', '/ru', '/ar/guides', '/fr/4-month-old-sleep-schedule', '/en/start', '/ru/start']) {
    assert.equal(publicAnalyticsPath(path, settings.basePaths, settings.locales, settings.additionalPaths), path);
  }
  for (const path of ['/gift/PRIVATE-CODE', '/ru/gift/PRIVATE-CODE', '/subscription', '/support/private', '/unknown', '/fr/start', '/en/guides']) {
    assert.equal(publicAnalyticsPath(path, settings.basePaths, settings.locales, settings.additionalPaths), null);
  }
});

test('no analytics tag, event or consent ping before a positive choice', () => {
  const f = fixture();
  f.client.update('/ru/guides', false);
  assert.equal(f.scripts.length, 0);
  assert.equal(f.commands().length, 0);
  assert.equal(f.browser[`ga-disable-${GA_MEASUREMENT_ID}`], true);
});

test('one page view per public navigation, without duplicate tags or advertising', () => {
  const f = fixture();
  f.client.update('/ru/guides', true);
  f.client.update('/ru/guides', true);
  f.client.update('/fr/4-month-old-sleep-schedule', true);
  f.client.update('/en/start', true);
  assert.equal(f.scripts.length, 1);
  assert.equal(f.scripts[0].nonce, 'trusted-nonce');
  assert.match(f.scripts[0].src, /gtag\/js\?id=G-NBZ2G9XC1E$/);
  assert.deepEqual(f.events().map(args => args[1]), ['page_view', 'page_view', 'page_view']);
  assert.equal(f.events()[1][2].page_location, 'https://yorix-app.com/fr/4-month-old-sleep-schedule');
  assert.equal(f.events()[2][2].page_location, 'https://yorix-app.com/en/start');
  assert.equal(f.events()[0][2].page_referrer, 'https://www.google.com/');
  const config = f.commands().find(args => args[0] === 'config')[2];
  assert.equal(config.send_page_view, false);
  assert.equal(config.allow_google_signals, false);
  assert.equal(config.allow_ad_personalization_signals, false);
  assert.ok(!JSON.stringify(f.commands()).includes('private-example'));
});

test('records a single 90% scroll and sanitized App Store click', () => {
  const f = fixture();
  f.client.update('/ru/guides', true);
  f.browser.scrollY = 900;
  f.windowListeners.get('scroll')();
  f.windowListeners.get('scroll')();
  f.documentListeners.get('click')({ target: { closest: () => ({ href: 'https://apps.apple.com/app/apple-store/id6788705252?ct=PRIVATE-QUERY' }) } });
  assert.deepEqual(f.events().map(args => args[1]), ['page_view', 'scroll', 'app_store_click']);
  assert.equal(f.events()[2][2].link_url, 'https://apps.apple.com/app/id6788705252');
  assert.ok(!JSON.stringify(f.events()).includes('PRIVATE-QUERY'));
});

test('withdrawal stops listeners and expires only the analytics cookies', () => {
  const f = fixture();
  f.client.update('/ru/guides', true);
  const before = f.commands().length;
  f.client.update('/ru/guides', false);
  assert.equal(f.commands().length, before);
  assert.equal(f.browser[`ga-disable-${GA_MEASUREMENT_ID}`], true);
  assert.equal(f.documentListeners.size + f.windowListeners.size, 0);
  assert.equal(f.cookies.length, 6);
  assert.ok(f.cookies.every(cookie => cookie.startsWith('_ga=') || cookie.startsWith('_ga_NBZ2G9XC1E=')));
});

test('private routes and local previews cannot load analytics', () => {
  const privatePage = fixture();
  privatePage.client.update('/gift/PRIVATE-CODE', true);
  assert.equal(privatePage.scripts.length, 0);
  assert.equal(privatePage.events().length, 0);
  const preview = fixture('localhost');
  preview.client.update('/ru/guides', true);
  assert.equal(preview.scripts.length, 0);
  assert.equal(preview.events().length, 0);
});
