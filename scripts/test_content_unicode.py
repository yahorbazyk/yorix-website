"""Regression tests for multilingual preservation and opt-in file changes."""

from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import content_unicode as hygiene


class UnicodeProfileTests(unittest.TestCase):
    def test_removes_embedded_bom_and_unneeded_zero_width_spaces(self):
        text = '\ufeffHello\u200b world. При\u200bвет!\ufeff'
        self.assertEqual(hygiene.clean_text(text), 'Hello world. Привет!')
        positions, findings, _ = hygiene.analyze_text(text)
        self.assertEqual(len(positions), 4)
        self.assertEqual(sum(item['count'] for item in findings), 4)

    def test_preserves_multilingual_prose(self):
        samples = [
            'Baby sleep', 'Bebek uykusu İı', 'Sommeil du bébé', 'Süßer Schlaf',
            'Сон ребёнка', 'Slaap van je baby', 'Il sonno del bebè', 'Sono do bebê',
            'Sueño del bebé', 'การนอนของทารก', 'Barnets sömn', 'Tidur bayi',
            '赤ちゃんの睡眠', 'Sen niemowlęcia', 'Spánek miminka', 'Barnets søvn',
            'نوم الرضيع', 'Babyens søvn', 'שינת תינוקות', 'Сон немовляти',
            'Giấc ngủ của bé', 'Tidur bayi anda', 'शिशु की नींद',
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertEqual(hygiene.clean_text(sample), sample)

    def test_preserves_se_asian_word_boundaries(self):
        for sample in ['ทา\u200bรก', 'ລ\u200bາ', 'ក\u200bខ', 'က\u200bခ',
                       'ท\u200b\u200btext', 'text\u200bท', 'ท' + '\u200b' * 10000]:
            with self.subTest(sample=sample[:20]):
                self.assertEqual(hygiene.clean_text(sample), sample)

    def test_only_protects_boundaries_next_to_relevant_scripts(self):
        self.assertEqual(hygiene.clean_text('ทารก Hello\u200b world'), 'ทารก Hello world')

    def test_preserves_rtl_controls_and_joiners(self):
        sample = '\u200fשלום \u2067العربية\u2069 \u202bنوم\u202c می\u200cروم क्\u200dष'
        self.assertEqual(hygiene.clean_text(sample), sample)

    def test_preserves_emoji_glue_and_variation_selectors(self):
        sample = '👨\u200d👩\u200d👧\u200d👦 ❤️ 🏳️\u200d🌈 🏴\U000e0067\U000e0062\U000e007f'
        self.assertEqual(hygiene.clean_text(sample), sample)

    def test_preserves_typography_and_line_break_controls(self):
        sample = 'un\u00adbroken\u2060word\u00a0space\u202fnarrow\u2009thin\u3000wide — “yes”'
        self.assertEqual(hygiene.clean_text(sample), sample)

    def test_removes_noncharacters_and_reserved_ignorables(self):
        self.assertEqual(hygiene.clean_text('a\ufdd0b\ufffec\U0010ffffd\u2065e'), 'abcde')

    def test_preserves_private_use_and_unassigned_characters(self):
        sample = 'a\ue000b\u0378c'
        self.assertEqual(hygiene.clean_text(sample), sample)

    def test_does_not_interpret_escaped_code_literals(self):
        sample = r'const escaped = "\u200B";'
        self.assertEqual(hygiene.clean_text(sample), sample)

    def test_cleaning_is_idempotent(self):
        once = hygiene.clean_text('\ufeffa\u200bb ท\u200bา 👨\u200d👧')
        self.assertEqual(hygiene.clean_text(once), once)

    def test_pinned_sources_match_manifest(self):
        manifest = json.loads((hygiene.VENDOR / 'upstream.json').read_text())
        for filename, entry in manifest['files'].items():
            actual = hashlib.sha256((hygiene.VENDOR / filename).read_bytes()).hexdigest()
            self.assertEqual(actual, entry['sha256'])

    def test_refuses_tampered_vendor(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'text_unicode.py').write_text('raise RuntimeError("must not execute")')
            (root / 'upstream.json').write_text(json.dumps({
                'files': {'text_unicode.py': {'sha256': 'invalid'}}
            }))
            with patch.object(hygiene, 'VENDOR', root), self.assertRaisesRegex(ValueError, 'checksum'):
                hygiene.load_engine()


class FileSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.path = self.root / 'article.ts'
        self.before = '\ufeffconst text = "baby\u200b sleep";\r\n'.encode('utf-8')
        self.path.write_bytes(self.before)
        self.config = {'include': ['*.ts']}

    def run_mode(self, mode):
        output = io.StringIO()
        with redirect_stdout(output):
            status = hygiene.run(mode, self.root, self.config, json_output=True)
        return status, json.loads(output.getvalue())

    def test_check_reports_without_writing(self):
        status, report = self.run_mode('check')
        self.assertEqual(status, 1)
        self.assertEqual(report['removable_characters'], 2)
        self.assertEqual(self.path.read_bytes(), self.before)

    def test_inspect_does_not_write_or_treat_legitimate_hits_as_failures(self):
        self.path.write_text('שלום\u200f 👨\u200d👧')
        before = self.path.read_bytes()
        status, report = self.run_mode('inspect')
        self.assertEqual(status, 0)
        self.assertEqual(report['files_with_findings'], 0)
        self.assertGreater(report['files'][0]['upstream_inspection']['suspicious_total'], 0)
        self.assertEqual(self.path.read_bytes(), before)

    def test_clean_preserves_crlf_mode_and_unaffected_mtime(self):
        self.path.chmod(0o640)
        status, _ = self.run_mode('clean')
        self.assertEqual(status, 0)
        self.assertEqual(self.path.read_bytes(), b'const text = "baby sleep";\r\n')
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o640)
        original_mtime = self.path.stat().st_mtime_ns
        _, report = self.run_mode('clean')
        self.assertEqual(report['removable_characters'], 0)
        self.assertEqual(self.path.stat().st_mtime_ns, original_mtime)
        self.assertFalse(list(self.root.glob('.unicode-*')))

    def test_excludes_unrelated_files_and_explicit_exclusions(self):
        for name in ['secret.env', 'policy.html', 'excluded.ts']:
            (self.root / name).write_bytes(self.before)
        self.config['exclude'] = ['excluded.ts']
        self.run_mode('clean')
        for name in ['secret.env', 'policy.html', 'excluded.ts']:
            self.assertEqual((self.root / name).read_bytes(), self.before)

    def test_rejects_symlink(self):
        (self.root / 'linked.ts').symlink_to(self.path)
        with self.assertRaisesRegex(ValueError, 'Symlinks'):
            self.run_mode('check')

    def test_rejects_path_traversal(self):
        with self.assertRaisesRegex(ValueError, 'inside the repository'):
            hygiene.content_paths(self.root, {'include': ['../*.ts']})

    def test_refuses_to_replace_changed_source(self):
        self.path.write_bytes(b'new changes')
        with self.assertRaisesRegex(ValueError, 'Source changed'):
            hygiene.replace_file(self.path, self.before, b'cleaned')
        self.assertEqual(self.path.read_bytes(), b'new changes')

    def test_rejects_empty_scope(self):
        self.config = {'include': ['missing.ts']}
        with self.assertRaisesRegex(ValueError, 'No content sources'):
            self.run_mode('check')

    def test_rejects_invalid_utf8(self):
        self.path.write_bytes(b'\xff')
        with self.assertRaises(UnicodeDecodeError):
            self.run_mode('check')

    def test_rejects_oversized_source(self):
        with patch.object(hygiene, 'MAX_FILE_BYTES', 1), self.assertRaisesRegex(ValueError, 'limit'):
            self.run_mode('check')


if __name__ == '__main__':
    unittest.main()
