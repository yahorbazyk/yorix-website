"""Check public sitemap URLs against a running build without third-party packages.

Usage: python3 scripts/check-technical-seo.py --base http://localhost:3002
The crawler does not follow redirects: a sitemap entry must itself be indexable.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SITE = re.search(r"export const siteUrl = '([^']+)'", (ROOT / 'app/content.ts').read_text()).group(1)
LOCALES = re.findall(r"'([a-z]{2})'", (ROOT / 'app/locales.ts').read_text().split('] as const;')[0])
SALES = re.compile(r'^/(?:ru/)?subscription(?:/(?:payment|offer|gift))?/?$')
NAMESPACE = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}


def normalize_url(url):
    parts = urlsplit(url)
    return parts._replace(path=parts.path or '/').geturl()


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html = {}
        self.canonical = []
        self.languages = {}
        self.switches = {}
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.html = attrs
        elif tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(normalize_url(attrs['href']))
        elif tag == 'link' and attrs.get('rel') == 'alternate' and 'hreflang' in attrs:
            self.languages[attrs['hreflang']] = normalize_url(attrs['href'])
        elif tag == 'a' and 'hreflang' in attrs:
            self.switches[attrs['hreflang']] = attrs.get('href')
        elif tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property'))] = attrs.get('content', '')


def request(base, path, headers=None):
    values = {'User-Agent': 'Googlebot', 'Accept-Language': 'en',
              'x-yorix-document-locale': 'invalid-caller-value'}
    values.update(headers or {})
    req = Request(base.rstrip('/') + path, headers=values)
    try:
        response = build_opener(NoRedirect()).open(req, timeout=45)
    except HTTPError as error:
        response = error
    with response:
        return response.status, response.headers, response.read().decode('utf-8')


def check_page(base, url):
    path = urlsplit(url).path or '/'
    status, headers, html = request(base, path)
    assert status == 200, f'{path}: HTTP {status}'
    assert 'noindex' not in headers.get('X-Robots-Tag', '').lower(), path
    assert 'text/html' in headers.get('Content-Type', ''), path
    page = Page()
    page.feed(html)
    prefix = path.split('/')[1]
    locale = prefix if prefix in LOCALES else 'en'
    assert page.html.get('lang') == locale, f'{path}: incorrect document language'
    assert page.html.get('dir') == ('rtl' if locale in ('ar', 'he') else 'ltr'), path
    assert page.canonical == [url], f'{path}: canonical {page.canonical}'
    assert 'noindex' not in page.meta.get('robots', '').lower(), path
    assert page.languages.get(locale) == url, f'{path}: missing self hreflang'
    assert page.meta.get('twitter:title') == page.meta.get('og:title'), f'{path}: stale Twitter title'
    assert page.meta.get('twitter:description') == page.meta.get('og:description'), f'{path}: stale Twitter description'
    english = page.languages.get('en')
    if english and (path.endswith('/guides') or urlsplit(english).path.count('/') == 1
                    and urlsplit(english).path not in ('/', '/about', '/support')):
        for lang, destination in page.languages.items():
            if lang != 'x-default':
                expected = f'{urlsplit(destination).path}?lang={lang}'
                assert page.switches.get(lang) == expected, f'{path}: language switch {lang}'
    return url, page.languages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='http://localhost:3002')
    args = parser.parse_args()
    maps = [ET.parse(ROOT / 'public' / name) for name in ('sitemap.xml', 'sitemap-pages.xml')]
    lists = [[node.text for node in tree.findall('s:url/s:loc', NAMESPACE)] for tree in maps]
    urls = lists[0]
    assert urls == lists[1], 'Sitemap aliases disagree'
    assert len(urls) == len(set(urls)), 'Duplicate sitemap URLs'
    for url in urls:
        parts = urlsplit(url)
        assert f'{parts.scheme}://{parts.netloc}' == SITE and not parts.query and not parts.fragment, url
        assert not SALES.fullmatch(parts.path), f'Region-gated sales URL in public sitemap: {url}'
    for locale in ['en', *LOCALES]:
        prefix = '' if locale == 'en' else f'/{locale}'
        for suffix in ('', '/guides', '/about', '/support'):
            assert SITE + (prefix + suffix or '/') in urls, (locale, suffix)
    for name in ('sitemap.xml', 'sitemap-pages.xml'):
        status, headers, xml = request(args.base, '/' + name)
        assert status == 200 and 'xml' in headers.get('Content-Type', ''), name
        assert ET.tostring(ET.fromstring(xml)) == ET.tostring(ET.parse(ROOT / 'public' / name).getroot()), name
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = dict(pool.map(lambda url: check_page(args.base, url), urls))
    for url, languages in results.items():
        for language, alternate in languages.items():
            assert alternate in results, f'{url}: alternate missing from sitemap: {alternate}'
            assert results[alternate] == languages, f'{url}: missing hreflang return links ({language})'
    # Public discovery must not weaken the purchase gate or block gift redemption.
    for path in ('/subscription', '/subscription/offer', '/subscription/payment',
                 '/ru/subscription', '/ru/subscription/offer', '/ru/subscription/payment'):
        status, _, _ = request(args.base, path, {'CF-IPCountry': 'US'})
        assert status == 302, f'Purchase gate changed: {path}'
        status, _, _ = request(args.base, path, {'CF-IPCountry': 'BY'})
        assert status == 200, f'Allowed purchase route blocked: {path}'
    for path in ('/gift', '/ru/gift', '/ar/gift', '/subscription/privacy', '/subscription/terms'):
        status, _, _ = request(args.base, path, {'CF-IPCountry': 'US'})
        assert status == 200, f'Public route blocked: {path}'
    # A language choice sets the preference but lands on the same article.
    path = '/ru/4-month-old-sleep-schedule?lang=ru'
    status, headers, _ = request(args.base, path)
    assert status == 302 and urlsplit(headers['Location']).path == path.split('?')[0], path
    assert 'yorix-lang=ru' in headers.get('Set-Cookie', ''), 'Language preference was not saved'
    print(f'PASS: {len(urls)} sitemap URLs; reciprocal hreflang, canonical, document language,')
    print('language switches, social metadata, regional purchase gates and public legal/gift routes.')


if __name__ == '__main__':
    main()
