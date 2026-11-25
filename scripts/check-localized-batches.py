"""Read-only rendered checks for every localized article batch (all pilot locales)."""
import argparse, concurrent.futures, importlib.util, json, re, urllib.error, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('render', ROOT / 'scripts/check-english-articles.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
parser = argparse.ArgumentParser()
parser.add_argument('--base', default='http://localhost:3004')
parser.add_argument('--sitemap-urls', type=int, required=True)
args = parser.parse_args()
items = json.loads((ROOT / 'app/article/pilot-articles.generated.json').read_text())
base = 'https://yorix-app.com'
seen = {}


def get(path):
    if path in seen:
        return seen[path]
    req = urllib.request.Request(args.base + path, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'ru', 'Cookie': 'yorix-lang=ru'})
    with urllib.request.urlopen(req, timeout=60) as response:
        assert response.geturl() == args.base + path, (path, response.geturl())
        seen[path] = response.read().decode()
        return seen[path]


def alternates(html):
    tags = re.findall(r'<link rel="alternate"[^>]*>', html)
    return {re.search(r'hreflang="([^"]+)"', t, re.I)[1]: re.search(r' href="([^"]+)"', t)[1] for t in tags if re.search(r'hreflang=', t, re.I)}


def check(p):
    path = p['canonical'].removeprefix(base)
    html = get(path)
    page = m.Article()
    page.feed(html)
    lang = 'pt-BR' if p['locale'] == 'pt' else p['locale']
    assert f'<html lang="{lang}" dir="{"rtl" if p["locale"] == "ar" else "ltr"}"' in html, path
    assert f'<link rel="canonical" href="{p["canonical"]}"' in html, path
    assert page.h1 == 1 and page.title == p['title'], path
    assert len(page.json) == 1 and json.loads(page.json[0]) == p['schema'], path
    assert set(page.anchors) <= page.ids, (path, set(page.anchors) - page.ids)
    if '| ---' in p['body']:
        assert page.tables, path
    for link in re.findall(r'\]\((/[^)#\s]+)', p['body']):
        get(link)
    links = alternates(html)
    assert links.get(p['locale']) in (p['canonical'], path), (path, links)
    for href in links.values():
        get(href.removeprefix(base))
    return path, links


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(check, items))
clusters = {}
for (path, links), p in zip(results, items):
    if p['type'] != 'LANG-ONLY':
        clusters.setdefault(p['slug'], []).append((path, links))
for slug, members in clusters.items():
    english = alternates(get('/' + slug))
    for path, links in members:
        assert {k: v.removeprefix(base) for k, v in links.items()} == {k: v.removeprefix(base) for k, v in english.items()}, (path, links, english)
for locale in sorted({p['locale'] for p in items}):
    guides = get(f'/{locale}/guides')
    missing = [p['slug'] for p in items if p['locale'] == locale and f'href="/{locale}/{p["slug"]}"' not in guides]
    assert not missing, (locale, missing)
xml = ET.fromstring(get('/sitemap.xml'))
urls = {u.find('{*}loc').text for u in xml}
assert len(urls) == args.sitemap_urls, len(urls)
assert all(p['canonical'] in urls for p in items)
print(f'PASS: {len(items)} localized pages, links, hreflang clusters, guide cards and {len(urls)} sitemap URLs')
