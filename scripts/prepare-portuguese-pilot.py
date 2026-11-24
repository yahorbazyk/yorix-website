"""Rebuild the approved Brazilian Portuguese pilot without rewriting prose."""
import argparse,csv,json,re
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--date',required=True);args=parser.parse_args();day=date.fromisoformat(args.date)
months='janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro'.split()
label=f'{day.day} de {months[day.month-1]} de {day.year}'
source=ROOT/'content/pilots/pt';items=[]
for row in csv.DictReader((source/'manifest.csv').open()):
 raw=(source/(row['slug']+'.md')).read_text();fm,rest=raw.split('---',2)[1:];meta={}
 for line in fm.splitlines():
  if ': ' in line:
   key,value=line.split(': ',1)
   if key in ['title','meta_description','canonical']:meta[key]=json.loads(value)
 match=re.search(r'```json\s*(.*?)\s*```',rest,re.S);assert match,row['slug']
 body=rest[:match.start()].strip().replace('22 de novembro de 2026',label);schema=json.loads(match[1]);heading=re.search(r'^# (.+)$',body,re.M)[1]
 for entry in schema['@graph']:
  if entry['@type']=='Article':entry['datePublished']=entry['dateModified']=args.date
 items.append(dict(locale='pt',documentLanguage='pt-BR',slug=row['slug'],type=row['type'],title=meta['title'],description=meta['meta_description'],canonical=meta['canonical'],heading=heading,body=body,schema=schema,date=args.date,readTime=f'{max(1,round(len(body.split())/200))} min de leitura',category='Sono do bebê',coverClass='from-[#1E1B4B] to-[#6366F1]'))
assert len(items)==30
p=ROOT/'app/article/pilot-articles.generated.json';previous=json.loads(p.read_text()) if p.exists() else []
p.write_text(json.dumps([v for v in previous if v['locale']!='pt']+items,ensure_ascii=False,indent=2)+'\n')
print('Prepared 30 Brazilian Portuguese articles')
