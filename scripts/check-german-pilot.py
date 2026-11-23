"""Read-only rendered checks for the complete German pilot."""
import argparse,concurrent.futures,importlib.util,json,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('render',ROOT/'scripts/check-english-articles.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://localhost:3004');args=parser.parse_args()
items=json.loads((ROOT/'app/article/pilot-articles.generated.json').read_text());items=[p for p in items if p['locale']=='de'];assert len(items)==20
base='https://yorix-app.com'
def get(path):
 req=urllib.request.Request(args.base+path,headers={'User-Agent':'Mozilla/5.0','Accept-Language':'ru','Cookie':'yorix-lang=ru'})
 with urllib.request.urlopen(req,timeout=40) as r:
  assert r.geturl()==args.base+path,(path,r.geturl())
  return r.read().decode()
def check(p):
 html=get(p['canonical'].removeprefix(base));page=m.Article();page.feed(html)
 assert page.h1==1 and page.title==p['title'],p['slug']
 assert len(page.json)==1 and json.loads(page.json[0])==p['schema'],p['slug']
 assert set(page.anchors)<=page.ids,(p['slug'],set(page.anchors)-page.ids)
 assert 'Implementierungsnotiz' not in html,p['slug']
 if '| ---' in p['body']:assert page.tables,p['slug']
 assert 'lang="de"' in html,p['slug']
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(check,items))
guides=get('/de/guides');assert all('href="/de/'+p['slug']+'"' in guides for p in items)
xml=ET.fromstring(get('/sitemap.xml'));urls={u.find('{*}loc').text for u in xml};assert len(urls)==529
assert all(p['canonical'] in urls for p in items)
print('PASS: 20 German pages, metadata, source anchors, tables, guide cards and 529 sitemap URLs')
