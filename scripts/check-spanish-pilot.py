"""Read-only rendered checks for the complete neutral Spanish pilot."""
import argparse,concurrent.futures,importlib.util,json,re,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('render',ROOT/'scripts/check-english-articles.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://localhost:3004');args=parser.parse_args()
items=json.loads((ROOT/'app/article/pilot-articles.generated.json').read_text());items=[p for p in items if p['locale']=='es'];assert len(items)==30
base='https://yorix-app.com'
def get(path):
 req=urllib.request.Request(args.base+path,headers={'User-Agent':'Mozilla/5.0','Accept-Language':'ru','Cookie':'yorix-lang=ru'})
 with urllib.request.urlopen(req,timeout=40) as response:
  assert response.geturl()==args.base+path,(path,response.geturl())
  return response.read().decode()
def check(p):
 path=p['canonical'].removeprefix(base);html=get(path);page=m.Article();page.feed(html)
 assert '<html lang="es"' in html,path
 assert page.h1==1 and page.title==p['title'],path
 assert len(page.json)==1 and json.loads(page.json[0])==p['schema'],path
 assert set(page.anchors)<=page.ids,(path,set(page.anchors)-page.ids)
 assert 'Nota de implementación' not in html,path
 if '| ---' in p['body']:assert page.tables,path
 for link in re.findall(r'\]\((/es/[^)#]+)',p['body']):get(link)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(check,items))
guides=get('/es/guides');assert all('href="/es/'+p['slug']+'"' in guides for p in items)
xml=ET.fromstring(get('/sitemap.xml'));urls={u.find('{*}loc').text for u in xml};assert len(urls)==565
assert all(p['canonical'] in urls for p in items)
print('PASS: 30 Spanish pages, links, nested route, metadata, guide cards and 565 sitemap URLs')
