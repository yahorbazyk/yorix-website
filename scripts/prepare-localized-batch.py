"""Rebuild one approved localization batch without rewriting prose.

Rows of content/pilots/<lang>/manifest.csv whose phase matches --phase are
compiled into app/article/pilot-articles.generated.json with --date as the
publication date; every other article already in that file stays untouched.
"""
import argparse, csv, json, re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES = {
    'de': (lambda d: f'{d.day}. {"Januar Februar März April Mai Juni Juli August September Oktober November Dezember".split()[d.month-1]} {d.year}', '{} Min.', 'Babyschlaf'),
    'es': (lambda d: f'{d.day} de {"enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()[d.month-1]} de {d.year}', '{} min de lectura', 'Sueño del bebé'),
    'pt': (lambda d: f'{d.day} de {"janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split()[d.month-1]} de {d.year}', '{} min de leitura', 'Sono do bebê'),
    'ar': (lambda d: f'{d.day} {"يناير فبراير مارس أبريل مايو يونيو يوليو أغسطس سبتمبر أكتوبر نوفمبر ديسمبر".split()[d.month-1]} {d.year}', '{} دقائق للقراءة', 'نوم الطفل'),
    'tr': (lambda d: f'{d.day} {"Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık".split()[d.month-1]} {d.year}', '{} dk okuma', 'Bebek uykusu'),
}

parser = argparse.ArgumentParser()
parser.add_argument('--lang', required=True, choices=LOCALES)
parser.add_argument('--phase', required=True)
parser.add_argument('--date', required=True)
args = parser.parse_args()
day = date.fromisoformat(args.date)
label, read_time, category = LOCALES[args.lang]
# The handoffs were dated on the day they were written, not the day they go live.
handoff_labels = [label(date(2026, 11, n)) for n in (22, 24)]

source = ROOT / 'content/pilots' / args.lang
rows = [r for r in csv.DictReader((source / 'manifest.csv').open()) if r['phase'] == args.phase]
assert rows, f'no rows for phase {args.phase}'
items = []
for row in rows:
    raw = (source / Path(row['file']).name).read_text()
    fm, rest = raw.split('---', 2)[1:]
    meta = {}
    for line in fm.splitlines():
        if ': ' in line:
            key, value = line.split(': ', 1)
            if key in ['title', 'meta_description', 'canonical']:
                meta[key] = json.loads(value)
    match = re.search(r'```json\s*(.*?)\s*```', rest, re.S)
    assert match, row['slug']
    body = rest[:match.start()].strip()
    for old in handoff_labels:
        body = body.replace(old, label(day))
    schema = json.loads(match[1])
    heading = re.search(r'^# (.+)$', body, re.M)[1]
    for entry in schema['@graph']:
        if entry['@type'] == 'Article':
            entry['datePublished'] = entry['dateModified'] = args.date
    assert meta['canonical'] == f'https://yorix-app.com/{args.lang}/{row["slug"]}', row['slug']
    items.append(dict(locale=args.lang, documentLanguage='pt-BR' if args.lang == 'pt' else args.lang, slug=row['slug'], type=row['type'],
                      title=meta['title'], description=meta['meta_description'], canonical=meta['canonical'], heading=heading, body=body,
                      schema=schema, date=args.date, readTime=read_time.format(max(1, round(len(body.split()) / 200))), category=category,
                      coverClass='from-[#1E1B4B] to-[#6366F1]'))

path = ROOT / 'app/article/pilot-articles.generated.json'
previous = json.loads(path.read_text()) if path.exists() else []
fresh = {(p['locale'], p['slug']) for p in items}
path.write_text(json.dumps([p for p in previous if (p['locale'], p['slug']) not in fresh] + items, ensure_ascii=False, indent=2) + '\n')
print(f'Prepared {len(items)} {args.lang} articles ({args.phase})')
