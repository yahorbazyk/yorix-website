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
        self.assertEqual(len(self.articles), 114)
        self.assertEqual(sum(a['replaces'] for a in self.articles), 12)
        self.assertEqual(len({a['path'] for a in self.articles}), 114)
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
                self.assertIn('|', a['body'])
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

    def test_sitemaps_have_no_retired_or_invented_translations(self):
        ns = {'s': prepare.NS}
        first = (ROOT / 'public/sitemap.xml').read_bytes()
        self.assertEqual(first, (ROOT / 'public/sitemap-pages.xml').read_bytes())
        tree = ET.fromstring(first)
        urls = {u.find('s:loc', ns).text: u.find('s:lastmod', ns) for u in tree}
        self.assertEqual(len(urls), 474)
        for url in urls:
            self.assertNotIn(url.rsplit('/', 1)[-1], prepare.MERGES)
        for a in self.articles:
            self.assertEqual(urls[a['canonical']].text, a['updated'])
            if not a['replaces']:
                self.assertFalse(any(url.endswith(a['path']) and url != a['canonical'] for url in urls))


if __name__ == '__main__':
    unittest.main()
