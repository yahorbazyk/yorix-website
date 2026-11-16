"""Check fidelity to the approved package, metadata, links and route coverage."""

import importlib.util
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prepare_articles', ROOT / 'scripts/prepare-english-articles.py')
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


class EnglishArticlesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.articles = json.loads((ROOT / 'app/article/english-articles.generated.json').read_text())
        cls.catalog = json.loads((ROOT / 'app/article/english-catalog.generated.json').read_text())

    def test_generated_content_matches_source_exactly_with_only_technical_changes(self):
        date = self.articles[0]['updated']
        expected, hashes = prepare.compile_articles(date)
        self.assertEqual(self.articles, expected)
        self.assertEqual(hashes, json.loads((ROOT / 'content/en/source-checksums.json').read_text()))
        self.assertEqual(self.catalog, [{k: v for k, v in a.items() if k not in ('body', 'schema')} for a in expected])

    def test_counts_and_english_only_scope(self):
        self.assertEqual(len(self.articles), 147)
        self.assertEqual(sum(a['kind'] == 'article' for a in self.articles), 146)
        self.assertEqual(sum(a['kind'] == 'hub' for a in self.articles), 1)
        self.assertEqual(sum(a['replaces'] for a in self.articles), 12)
        self.assertEqual(len({a['path'] for a in self.articles}), 147)
        self.assertEqual(sum(a['path'].startswith('/sleep-regression/') for a in self.articles), 7)

    def test_dates_hidden_notes_and_schema(self):
        for a in self.articles:
            with self.subTest(article=a['slug']):
                self.assertNotIn('[Month DD, YYYY]', a['body'])
                self.assertNotIn('Implementation note', a['body'])
                self.assertNotIn('```json', a['body'])
                self.assertEqual(len(re.findall(r'^# ', a['body'], re.M)), 1)
                graph = a['schema']['@graph']
                self.assertEqual([x['@type'] for x in graph], ['Article', 'BreadcrumbList'])
                article = graph[0]
                self.assertEqual(article['url'], a['canonical'])
                self.assertEqual(article['datePublished'], a['published'])
                self.assertEqual(article['dateModified'], a['updated'])
                self.assertEqual(article['author']['name'], 'Yorix')
                self.assertEqual(graph[1]['itemListElement'][-1]['item'], a['canonical'])
                if a['kind'] == 'article':
                    self.assertIn('## Short answer', a['body'])
                    self.assertTrue('|' in a['body'] or len(re.findall(r'^- \*\*', a['body'], re.M)) >= 3, a['slug'])
        replaced = next(a for a in self.articles if a['slug'] == 'newborn-sleep-schedule')
        self.assertEqual(replaced['published'], '2026-09-03')
        special = next(a for a in self.articles if a['slug'] == 'sleep-regression/4-months')
        self.assertEqual(special['title'], '4 Month Sleep Regression: Signs, Duration & Help | Yorix')

    def test_all_links_resolve_directly_to_the_package(self):
        paths = {a['path'] for a in self.articles}
        links = [link for a in self.articles for link in re.findall(r'\]\((/[^)]+)\)', a['body'])]
        self.assertGreater(len(links), 1200)
        self.assertTrue(all(link.split('#')[0] in paths for link in links))

    def test_phase_one_scope_and_inbound_requirements(self):
        release = json.loads((ROOT / 'content/en/releases/phase-1/summary.json').read_text())
        articles = {a['path']: a for a in self.articles}
        self.assertEqual(len(release['newSlugs']), 55)
        forbidden = {'/baby-snoring', '/baby-sleeping-with-mouth-open', '/foods', '/sleep-training-for-naps'}
        self.assertFalse(forbidden & articles.keys())
        for source, targets in release['inboundRequirements'].items():
            links = re.findall(r'\]\((/[^)]+)\)', articles[source]['body'])
            for target in targets:
                if target.split('#')[0] != source:
                    self.assertTrue(any(link.split('#')[0] == target.split('#')[0] for link in links), (source, target))

    def test_phase_two_scope_insertions_and_inbound_requirements(self):
        release = json.loads((ROOT / 'content/en/releases/phase-2/summary.json').read_text())
        articles = {a['path']: a for a in self.articles}
        self.assertEqual(len(release['newSlugs']), 8)
        self.assertEqual(len(release['approvedInsertions']), 33)
        for insertion in release['approvedInsertions']:
            self.assertIn(insertion['heading'], articles['/' + insertion['slug']]['body'])
        for source, targets in release['inboundRequirements'].items():
            links = re.findall(r'\]\((/[^)]+)\)', articles[source]['body'])
            for target in targets:
                if target.split('#')[0] != source:
                    self.assertTrue(any(link.split('#')[0] == target.split('#')[0] for link in links), (source, target))
        for a in self.articles:
            for note in release['editorialRouteNotesRemoved']:
                self.assertNotIn(note.strip(), a['body'])

    def test_cross_article_heading_anchors(self):
        articles = {a['path']: a for a in self.articles}
        for a in self.articles:
            for link in re.findall(r'\]\(([#/][^)]+)\)', a['body']):
                path, _, anchor = link.partition('#')
                path = path or a['path']
                if not anchor:
                    continue
                headings = re.findall(r'^#{1,6} (.+)$', articles[path]['body'], re.M)
                ids = {re.sub(r'[^a-z0-9]+', '-', re.sub(r'[*_`]', '', h.lower())).strip('-') for h in headings}
                self.assertIn(anchor, ids, (a['path'], link))

    def test_phase_three_faq_scope_and_week_group(self):
        release = json.loads((ROOT / 'content/en/releases/phase-3/summary.json').read_text())
        articles = {a['path']: a for a in self.articles}
        self.assertEqual(len(release['newSlugs']), 10)
        self.assertEqual(len(release['approvedFaqInsertions']), 13)
        self.assertTrue(all(articles['/' + slug]['category'] == 'Sleep by week' for slug in release['newSlugs'] if re.fullmatch(r'\d+-week-old-baby-sleep', slug)))
        for insertion in release['approvedFaqInsertions']:
            body = articles['/' + insertion['slug']]['body']
            for question in insertion['questions']:
                self.assertEqual(body.count('**' + question + '**'), 1, (insertion['slug'], question))
        for source, targets in release['inboundRequirements'].items():
            links = re.findall(r'\]\((/[^)]+)\)', articles[source]['body'])
            for target in targets:
                if target.split('#')[0] != source:
                    self.assertTrue(any(link.split('#')[0] == target.split('#')[0] for link in links), (source, target))
        for slug, notes in release['editorialRouteNotesRemoved'].items():
            for note in notes:
                self.assertNotIn(note.strip(), articles['/' + slug]['body'])

    def test_sitemaps_have_no_retired_or_invented_translations(self):
        ns = {'s': prepare.NS}
        first = (ROOT / 'public/sitemap.xml').read_bytes()
        self.assertEqual(first, (ROOT / 'public/sitemap-pages.xml').read_bytes())
        tree = ET.fromstring(first)
        urls = {u.find('s:loc', ns).text: u.find('s:lastmod', ns) for u in tree}
        self.assertEqual(len(urls), 507)
        for url in urls:
            self.assertNotIn(url.rsplit('/', 1)[-1], prepare.MERGES)
        for a in self.articles:
            self.assertEqual(urls[a['canonical']].text, a['updated'])
            if not a['replaces']:
                self.assertFalse(any(url.endswith(a['path']) and url != a['canonical'] for url in urls))

    def test_phase_four_week_hub_and_no_duplicate_pilot_faqs(self):
        release = json.loads((ROOT / 'content/en/releases/phase-4/summary.json').read_text())
        articles = {a['path']: a for a in self.articles}
        self.assertEqual(len(release['newArticleSlugs']), 11)
        self.assertEqual(articles['/baby-sleep-by-week']['kind'], 'hub')
        self.assertEqual(sum(a['category'] == 'Sleep by week' for a in self.articles), 16)
        for week in range(1, 16):
            path = f'/{week}-week-old-baby-sleep'
            self.assertIn(path, articles)
            self.assertIn(f']({path})', articles['/baby-sleep-by-week']['body'])
            self.assertIn('](/baby-sleep-by-week)', articles[path]['body'])
        self.assertFalse(any(re.fullmatch(r'/(?:1[6-9]|[2-9]\d)-week-old-baby-sleep', path) for path in articles))
        for source, targets in release['inboundRequirements'].items():
            links = re.findall(r'\]\((/[^)]+)\)', articles[source]['body'])
            for target in targets:
                if target.split('#')[0] != source:
                    self.assertTrue(any(link.split('#')[0] == target.split('#')[0] for link in links), (source, target))
        pilot = json.loads((ROOT / 'content/en/releases/phase-3/summary.json').read_text())
        for insertion in pilot['approvedFaqInsertions']:
            for question in insertion['questions']:
                self.assertEqual(articles['/' + insertion['slug']]['body'].count('**' + question + '**'), 1)

    def test_phase_five_scope_inbound_links_and_source_correction(self):
        release = json.loads((ROOT / 'content/en/releases/phase-5/summary.json').read_text())
        articles = {a['slug']: a for a in self.articles}
        self.assertEqual(len(release['newSlugs']), 11)
        for insertion in release['approvedInsertions']:
            body = articles[insertion['slug']]['body']
            for question in insertion['questions']:
                self.assertEqual(body.count('**' + question + '**'), 1, (insertion['slug'], question))
        for source, targets in release['inboundRequirements'].items():
            links = re.findall(r'\]\((/[^)]+)\)', articles[source.lstrip('/')]['body'])
            for target in targets:
                if target.split('#')[0] != source:
                    self.assertTrue(any(link.split('#')[0] == target.split('#')[0] for link in links), (source, target))
        nap = articles['should-you-wake-a-baby-from-a-nap']['body']
        self.assertNotIn('Health Canada', nap)
        self.assertIn(release['sourceAttributionCorrection']['verifiedUrl'], nap)
        for slug in ['baby-sleeping-on-stomach', '4-month-old-sleep-schedule']:
            body = articles[slug]['body']
            question = '**Can a 4 month old sleep on their stomach if they roll over?**'
            answer = body.split(question, 1)[1].split('\n\n', 1)[0]
            self.assertIn('both ways', answer)


if __name__ == '__main__':
    unittest.main()
