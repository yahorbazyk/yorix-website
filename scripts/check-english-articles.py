"""Crawl rendered package pages, permanent merges and missing translations.

Usage: python3 scripts/check-english-articles.py --base http://localhost:3002
All requests are read-only. Use --base https://yorix-app.com after publishing.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('technical_seo', ROOT / 'scripts/check-technical-seo.py')
seo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seo)


class Article(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.tables = 0
        self.script = None
        self.json = []
        self.text = []
        self.title = ''
        self.in_title = False
        self.ids = set()
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'table':
            self.tables += 1
        if tag == 'title':
            self.in_title = True
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.anchors.append(attrs['href'][1:])
        if tag == 'script':
            self.script = attrs.get('type', 'script')

    def handle_data(self, data):
        if self.script == 'application/ld+json':
            self.json.append(data)
        elif not self.script:
            self.text.append(data)
        if self.in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == 'script':
            self.script = None
        if tag == 'title':
            self.in_title = False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='http://localhost:3002')
    args = parser.parse_args()
    articles = json.loads((ROOT / 'app/article/english-articles.generated.json').read_text())

    def check(article):
        status, _, html = seo.request(args.base, article['path'])
        assert status == 200, (article['path'], status)
        page = Article()
        page.feed(html)
        visible = ' '.join(page.text)
        assert page.h1 == 1, (article['path'], 'H1')
        assert page.title == article['title'], (article['path'], page.title)
        assert page.tables >= 1, (article['path'], 'tables')
        assert len(page.json) == 1, (article['path'], 'JSON-LD')
        assert json.loads(page.json[0]) == article['schema'], (article['path'], 'schema')
        assert 'Implementation note' not in visible and '[Month DD' not in visible
        assert 'By the Yorix team' in visible
        assert 'not medical advice' in visible, article['path']
        assert set(page.anchors) <= page.ids, (article['path'], set(page.anchors) - page.ids)
        return article['path']

    with ThreadPoolExecutor(max_workers=3) as pool:
        for index, path in enumerate(pool.map(check, articles), 1):
            if index % 10 == 0:
                print(f'Rendered article check: {index}/{len(articles)}', flush=True)
    merges = {
        'newborn-sleep-first-28-days': 'newborn-sleep-schedule',
        'baby-sleep-parent-stress': 'survive-night-wakings-new-parents',
    }
    for locale in ['en', *seo.LOCALES]:
        prefix = '' if locale == 'en' else f'/{locale}'
        for old, new in merges.items():
            status, headers, _ = seo.request(args.base, f'{prefix}/{old}')
            assert status == 301, (locale, old, status)
            assert urlsplit(headers['Location']).path == f'{prefix}/{new}'
            status, _, _ = seo.request(args.base, f'{prefix}/{new}')
            assert status == 200, (locale, new, status)
    # Every new slug in Russian; a representative flat and nested slug in
    # every other language. Route validation is shared across all locales.
    missing = {f'/ru{a["path"]}' for a in articles if not a['replaces']}
    missing.update(f'/{lang}/short-naps' for lang in seo.LOCALES)
    missing.update(f'/{lang}/sleep-regression/4-months' for lang in seo.LOCALES)
    for path in sorted(missing):
        status, _, _ = seo.request(args.base, path)
        assert status == 404, (path, status)
    status, _, html = seo.request(args.base, '/guides')
    assert status == 200
    for article in articles:
        assert f'href="{article["path"]}"' in html, ('missing guide card', article['path'])
    print(f'PASS: {len(articles)} rendered articles, 46 direct 301 merges, {len(missing)} missing-translation 404s, and all guide cards.', flush=True)


if __name__ == '__main__':
    main()
