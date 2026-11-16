"""Compile the owner-supplied Markdown package without changing its prose.

Usage: python3 scripts/prepare-english-articles.py --date YYYY-MM-DD
Dates are pinned in publication-dates.json so rebuilding does not redate old pages.
Use --release-phase N --release-date YYYY-MM-DD before a later release date.
Only quoted JSON-compatible front matter and bare scalar values are accepted.
No source Markdown, HTML or embedded code is executed.
"""

import argparse
import csv
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'content/en'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
MERGES = {
    'newborn-sleep-first-28-days': 'newborn-sleep-schedule',
    'baby-sleep-parent-stress': 'survive-night-wakings-new-parents',
}


def compile_articles(deploy_date):
    date.fromisoformat(deploy_date)
    with (SOURCE / 'articles-table.csv').open(encoding='utf-8-sig') as table:
        rows = list(csv.DictReader(table))
    previous = {}
    for filename in ('app/content.ts', 'app/research-guides.ts'):
        text = (ROOT / filename).read_text()
        for slug, published in re.findall(r"slug: '([^']+)'(?:(?!slug:).)*?date: '([^']+)'", text, re.S):
            previous[slug] = datetime.strptime(published, '%B %d, %Y').date().isoformat()
    articles = []
    checksums = {}
    publication_dates = json.loads((SOURCE / 'publication-dates.json').read_text())
    for row in rows:
        filename = row['file']
        if Path(filename).name != filename or not filename.endswith('.md'):
            raise ValueError('Invalid article filename')
        raw = (SOURCE / 'articles' / filename).read_bytes()
        checksums[filename] = hashlib.sha256(raw).hexdigest()
        text = raw.decode('utf-8')
        _, front, body = text.split('---', 2)
        fields = {}
        for line in front.strip().splitlines():
            key, value = line.split(':', 1)
            value = value.strip()
            try:
                fields[key] = json.loads(value)
            except json.JSONDecodeError:
                if not re.fullmatch(r'[A-Za-z0-9_-]+', value):
                    raise ValueError(f'Unsupported front matter in {filename}: {key}')
                fields[key] = value
        canonical = fields['canonical']
        if canonical != row['url'] or not canonical.startswith('https://yorix-app.com/'):
            raise ValueError(f'Canonical mismatch: {filename}')
        path = canonical.removeprefix('https://yorix-app.com')
        slug = path.removeprefix('/')
        published = previous.get(slug, deploy_date) if row['status'].startswith('REPLACE') else deploy_date
        dates = publication_dates[slug]
        published, modified = dates['published'], dates['updated']
        date.fromisoformat(published)
        date.fromisoformat(modified)
        body = re.sub(r'^> \*\*Implementation note \(not for publication\):\*\*.*\n?', '', body, flags=re.M)
        match = re.search(r'\n```json\s*\n(.*?)\n```\s*$', body, re.S)
        if not match:
            raise ValueError(f'Missing final JSON-LD: {filename}')
        schema = json.loads(match.group(1))
        body = body[:match.start()].strip()
        published_label = date.fromisoformat(published).strftime('%B %-d, %Y')
        updated_label = date.fromisoformat(modified).strftime('%B %-d, %Y')
        body = body.replace('**Published:** [Month DD, YYYY]', f'**Published:** {published_label}')
        body = body.replace('**Updated:** [Month DD, YYYY]', f'**Updated:** {updated_label}')
        title = fields.get('meta_title', fields['title'])
        # The brief explicitly selects this alternative despite the longer
        # value still present in the supplied front matter. Keep source intact.
        if slug == 'sleep-regression/4-months':
            title = '4 Month Sleep Regression: Signs, Duration & Help | Yorix'
        for item in schema['@graph']:
            if item['@type'] == 'Article':
                item['datePublished'] = published
                item['dateModified'] = modified
                if fields.get('meta_title'):
                    item['headline'] = item['name'] = title
                assert item['url'] == canonical
                assert item['mainEntityOfPage']['@id'] == canonical
        headings = re.findall(r'^# (.+)$', body, re.M)
        assert len(headings) == 1, filename
        if '[YYYY-MM-DD]' in json.dumps(schema) or '[Month DD, YYYY]' in body:
            raise ValueError(f'Unresolved date in {filename}')
        if row['group'] == 'Comparison':
            group = 'Comparisons'
        elif row['group'].startswith('Development') or slug == 'baby-feeding-schedule':
            group = 'Development & feeding'
        elif slug.startswith('sleep-regression'):
            group = 'Sleep regressions'
        elif re.fullmatch(r'\d+-week-old-baby-sleep', slug) or slug == 'baby-sleep-by-week':
            group = 'Sleep by week'
        elif 'sleep-schedule' in slug or slug in ('baby-nap-schedule-by-age', 'wake-windows-by-age'):
            group = 'Sleep schedules by month'
        else:
            group = 'Sleep problems & methods'
        articles.append({
            'slug': slug, 'path': path, 'canonical': canonical,
            'kind': 'hub' if row['status'] == 'HUB' else 'article',
            'title': title, 'heading': headings[0], 'description': fields['meta_description'],
            'category': group, 'published': published, 'updated': modified,
            'readTime': f"{max(1, round(len(body.split()) / 225))} min read",
            'replaces': row['status'].startswith('REPLACE'), 'body': body, 'schema': schema,
        })
    paths = {article['path'] for article in articles}
    for article in articles:
        for link in re.findall(r'\]\((/[^)]+)\)', article['body']):
            assert link.split('#')[0] in paths, (article['path'], link)
    return articles, checksums


def write_outputs(deploy_date):
    articles, checksums = compile_articles(deploy_date)
    target = ROOT / 'app/article'
    (target / 'english-articles.generated.json').write_text(json.dumps(articles, ensure_ascii=False, indent=2) + '\n')
    catalog = [{key: value for key, value in article.items() if key not in ('body', 'schema')} for article in articles]
    (target / 'english-catalog.generated.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    (SOURCE / 'source-checksums.json').write_text(json.dumps(checksums, indent=2) + '\n')
    ET.register_namespace('', NS)
    tree = ET.parse(ROOT / 'public/sitemap.xml')
    root = tree.getroot()
    for node in list(root):
        url = node.find(f'{{{NS}}}loc').text
        if url.rsplit('/', 1)[-1] in MERGES or url.removeprefix('https://yorix-app.com') in {a['path'] for a in articles}:
            root.remove(node)
    for article in articles:
        node = ET.SubElement(root, f'{{{NS}}}url')
        ET.SubElement(node, f'{{{NS}}}loc').text = article['canonical']
        ET.SubElement(node, f'{{{NS}}}lastmod').text = article['updated']
    ET.indent(tree, space='  ')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode') + '\n'
    for name in ('sitemap.xml', 'sitemap-pages.xml'):
        (ROOT / 'public' / name).write_text(xml)
    print(f'Prepared {len(articles)} English articles; {len(root)} sitemap URLs.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', required=True)
    parser.add_argument('--phase-one-release-date')
    parser.add_argument('--release-phase', type=int)
    parser.add_argument('--release-date')
    args = parser.parse_args()
    if bool(args.release_phase) != bool(args.release_date):
        parser.error('--release-phase and --release-date must be supplied together')
    if args.phase_one_release_date and args.release_date:
        parser.error('Choose either the legacy phase-one flag or --release-phase/--release-date')
    if args.phase_one_release_date or args.release_date:
        release_date = date.fromisoformat(args.phase_one_release_date or args.release_date).isoformat()
        phase = args.release_phase or 1
        release_path = SOURCE / f'releases/phase-{phase}/summary.json'
        release = json.loads(release_path.read_text())
        dates_path = SOURCE / 'publication-dates.json'
        dates = json.loads(dates_path.read_text())
        for slug in release['newSlugs']:
            dates[slug] = {'published': release_date, 'updated': release_date}
        with (SOURCE / 'articles-table.csv').open() as table:
            for row in csv.DictReader(table):
                if row['file'] in release['modifiedExistingFiles']:
                    dates[row['url'].removeprefix('https://yorix-app.com/')]['updated'] = release_date
        dates_path.write_text(json.dumps(dates, indent=2) + '\n')
        release['candidateDate'] = release_date
        release_path.write_text(json.dumps(release, indent=2) + '\n')
    write_outputs(args.date)
