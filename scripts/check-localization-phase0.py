import urllib.request,json,xml.etree.ElementTree as ET,concurrent.futures
from html.parser import HTMLParser
from pathlib import Path
root=Path(__file__).resolve().parents[1]
tree=ET.parse(root/'public/sitemap.xml');expected={u.find('{*}loc').text:{l.get('hreflang'):l.get('href') for l in u.findall('{http://www.w3.org/1999/xhtml}link')} for u in tree.getroot()}
class P(HTMLParser):
 def __init__(self):super().__init__();self.links={};self.schema=[];self.active=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='link' and a.get('hreflang'):self.links[a['hreflang']]=a['href']
  if t=='script':self.active=a.get('type')=='application/ld+json'
 def handle_data(self,d):
  if self.active:self.schema.append(json.loads(d))
 def handle_endtag(self,t):
  if t=='script':self.active=False
urls=list(expected)
def check(url):
 req=urllib.request.Request(url.replace('https://yorix-app.com','http://localhost:3004'),headers={'User-Agent':'Mozilla/5.0','Accept-Language':'de','Cookie':'yorix-lang=ru'})
 with urllib.request.urlopen(req,timeout=40) as r:s=r.read().decode()
 p=P();p.feed(s);actual={k:('https://yorix-app.com'+v if v.startswith('/') else v) for k,v in p.links.items()}
 assert {k:v.rstrip('/') for k,v in actual.items()}=={k:v.rstrip('/') for k,v in expected[url].items()},(url,actual,expected[url])
 if '/newborn-sleep-schedule' in url:
  assert len(p.schema)==1,url
  g=p.schema[0]['@graph'];assert [v['@type'] for v in g]==['Article','BreadcrumbList'],url
  assert g[0]['url']==url,url
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(check,urls))
assert (root/'public/robots.txt').read_text().count('Sitemap:')==1
print('PASS: all HTML/sitemap alternate sets match; localized JSON-LD and single robots sitemap verified')
