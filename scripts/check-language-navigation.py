"""Check that explicit document URLs retain their language for real browsers.

Usage: python3 -B scripts/check-language-navigation.py --base http://localhost:3003
"""

import argparse
import importlib.util
from pathlib import Path
import sys
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('seo', ROOT / 'scripts/check-technical-seo.py')
seo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seo)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='http://localhost:3003')
    args = parser.parse_args()
    browser = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8'}
    count = 0
    for cookie in ('', 'yorix-lang=ru', 'yorix-lang=de'):
        for path, locale in (
            ('/cluster-feeding', 'en'), ('/newborn-sleep-schedule', 'en'),
            ('/guides', 'en'), ('/about', 'en'), ('/support', 'en'),
            ('/ru/newborn-sleep-schedule', 'ru'), ('/de/newborn-sleep-schedule', 'de'),
        ):
            status, _, html = seo.request(args.base, path, {**browser, 'Cookie': cookie})
            page = seo.Page()
            page.feed(html)
            assert status == 200 and page.html.get('lang') == locale, (path, cookie, status, page.html)
            count += 1
    for navigation in (
        {'Referer': args.base + '/cluster-feeding'},
        {'Referer': 'https://yorix-app.com/cluster-feeding'},
        {'Sec-Fetch-Site': 'same-origin'},
    ):
        status, _, html = seo.request(args.base, '/', {**browser, 'Cookie': 'yorix-lang=ru', **navigation})
        page = seo.Page()
        page.feed(html)
        assert status == 200 and page.html.get('lang') == 'en', ('internal home', status, page.html)
        count += 1
    status, headers, _ = seo.request(args.base, '/', browser)
    assert status == 302 and urlsplit(headers['Location']).path == '/ru', 'Initial language selection changed'
    count += 1
    status, headers, _ = seo.request(args.base, '/ru/newborn-sleep-schedule?lang=ru', browser)
    assert status == 302 and urlsplit(headers['Location']).path == '/ru/newborn-sleep-schedule'
    assert 'yorix-lang=ru' in headers.get('Set-Cookie', ''), 'Explicit language choice was not saved'
    count += 1
    print(f'PASS: {count} browser-language navigation cases; explicit URLs, cookies, homepage and language menu.')


if __name__ == '__main__':
    main()
