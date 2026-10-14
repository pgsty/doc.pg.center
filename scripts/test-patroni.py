#!/usr/bin/env python3
"""Exercise actual publication regressions without changing the checkout."""
from __future__ import annotations

from copy import deepcopy
from collections import Counter
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

from patroni_parity import reviewed_delta

spec = importlib.util.spec_from_file_location('patroni_gate_tests', Path(__file__).with_name('check-patroni.py'))
C = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = C
spec.loader.exec_module(C)


class PublicationRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(C.AUDIT.read_text())

    def check(self, page, transform=lambda s: s, language='fr', source_transform=lambda s: s):
        source = C.ROOT / page
        target = source.with_suffix('.' + language + '.md')
        review = self.audit['pages'][page]['translations'][language]
        return C.technical_errors(source_transform(source.read_text()), transform(target.read_text()), language,
                                  review.get('numeric_variant'), command_page=page == 'patronictl.md')

    def test_current_review_covers_all_120_pairs(self):
        errors, sources = C.source_errors(self.audit)
        self.assertEqual([], errors)
        self.assertEqual(24, len(sources))

    def test_translated_code_is_rejected(self):
        failures = self.check('config/dynamic.md', lambda s: s.replace('type: logical', 'type: logique', 1))
        self.assertIn('code/config/output fences', failures)

    def test_wrong_default_is_rejected(self):
        failures = self.check('config/dynamic.md', lambda s: s.replace('Valeur par défaut : 10', 'Valeur par défaut : 20', 1))
        self.assertTrue(any('numeric delta' in failure for failure in failures))

    def test_translated_warning_marker_is_rejected(self):
        failures = self.check('patronictl.md', lambda s: s.replace('[!WARNING]', '[!AVERTISSEMENT]', 1))
        self.assertIn('admonition types/order', failures)

    def test_correct_anchor_in_wrong_place_is_rejected(self):
        failures = self.check('patronictl.md', lambda s: s.replace('<a id="patronictl_list"></a>\n\n', '').replace('### patronictl history', '<a id="patronictl_list"></a>\n\n### patronictl history', 1))
        self.assertTrue(any('misplaced command anchor' in failure for failure in failures))

    def test_missing_english_heading_id_is_rejected(self):
        failures = self.check('replication_modes.md', lambda s: s.replace(' {#synchronous-mode}', '', 1))
        self.assertIn('English heading IDs', failures)

    def test_lost_tls_reference_is_rejected(self):
        failures = self.check('config/yaml.md', lambda s: s.replace('https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS', 'https://example.com/', 1))
        self.assertIn('link/asset targets', failures)

    def test_metadata_reordering_is_rejected(self):
        failures = self.check('config/yaml.md', lambda s: s.replace('weight: 20', 'weight: 10', 1))
        self.assertIn('non-translatable metadata: weight', failures)

    def test_duplicate_json_key_is_rejected(self):
        failures = self.check('rest_api.md', lambda s: s.replace('"database_system_identifier": "7408277255830290455",', '"database_system_identifier": "old",\n  "database_system_identifier": "7408277255830290455",', 1))
        self.assertIn('duplicate JSON key: database_system_identifier', failures)

    def test_phantom_history_flag_is_rejected(self):
        failures = self.check('patronictl.md', lambda s: s.replace('### patronictl history', '### patronictl history --force', 1))
        self.assertIn('unsupported history --force option', failures)

    def test_source_signal_typo_is_rejected_even_when_mirrored(self):
        failures = self.check('faq.md', lambda s: s.replace('SIGHUP', 'SIHGUP'), source_transform=lambda s: s.replace('SIGHUP', 'SIHGUP'))
        self.assertIn('known source literal typo', failures)

    def test_zero_width_space_is_rejected(self):
        failures = self.check('security.md', lambda s: s.replace('Patroni', 'Patro\u200bni', 1))
        self.assertIn('invisible characters', failures)

    def test_detached_release_explanation_is_rejected_in_fr_and_ja(self):
        source = (C.ROOT / 'releases.md').read_text()
        texts = {'en': source}
        for language in ('fr', 'ja'):
            target = (C.ROOT / ('releases.' + language + '.md')).read_text()
            explanation = re.search(r'\n\n(  \S[^\n]*(?:\n  \S[^\n]*)*)', target)
            self.assertIsNotNone(explanation)
            detached = target[:explanation.start(1)] + '\n'.join(
                line[2:] for line in explanation[1].splitlines()) + target[explanation.end(1):]
            review = self.audit['pages']['releases.md']['translations'][language]
            # Headers, list markers, numbers, literals and text remain equal;
            # only the paragraph's actual Markdown list ownership changes.
            self.assertEqual([], C.technical_errors(source, detached, language, review.get('numeric_variant')))
            texts[language] = detached
        errors = C.release_ownership_errors(texts)
        for language in ('fr', 'ja'):
            self.assertIn(language + ': release explanation/list ownership differs from English', errors)

    def test_release_ownership_accepts_wrapping_and_repeated_titles(self):
        english = '- Same title\n\n  First explanation.\n\n- Same title\n\n  - Nested condition\n    continued explanation\n\n    More explanation.\n'
        target = '- Même titre\n\n  Première\n  explication.\n\n- Même titre\n\n  - Condition imbriquée et\n    suite\n\n    Autre explication.\n'
        self.assertEqual([], C.release_ownership_errors({'en': english, 'fr': target}))

    def test_release_ownership_checks_marker_content_indent(self):
        english = '- Permission fix\n\n  Explanation.\n'
        target = '-  Permission fix\n\n  Explanation.\n'
        self.assertEqual(['fr: release explanation/list ownership differs from English'],
                         C.release_ownership_errors({'en': english, 'fr': target}))

    def test_stale_translation_fingerprint_is_rejected(self):
        audit = deepcopy(self.audit)
        audit['pages']['faq.md']['translations']['fr']['translation_sha256'] = '0' * 64
        self.assertTrue(any('fingerprint is stale' in failure for failure in C.source_errors(audit)[0]))

    def test_incomplete_review_is_rejected(self):
        audit = deepcopy(self.audit)
        del audit['pages']['faq.md']
        self.assertTrue(any('24 current English pages' in failure for failure in C.source_errors(audit)[0]))

    def test_focused_review_cannot_claim_complete_semantic_acceptance(self):
        audit = deepcopy(self.audit)
        audit['semantic_review']['status'] = 'focused'
        self.assertIn('complete semantic review is required for all 120 pairs', C.source_errors(audit)[0])

    def test_notation_exception_rejects_stale_source_or_target(self):
        source = C.ROOT / 'faq.md'
        english, target = source.read_text(), source.with_suffix('.de.md').read_text()
        expected = Counter(C.G.INLINE_CODE_RE.findall(C.G.parse_fenced_blocks(C.G.split_front_matter(english)[1])[1]))
        actual = Counter(C.G.INLINE_CODE_RE.findall(C.G.parse_fenced_blocks(C.G.split_front_matter(target)[1])[1]))
        args = ('de', 'inline_literal_variant', expected, actual)
        self.assertTrue(reviewed_delta(source, english, target, *args))
        self.assertFalse(reviewed_delta(source, english + '\n', target, *args))
        self.assertFalse(reviewed_delta(source, english, target + '\n', *args))

    def test_notation_exception_rejects_unreviewed_delta(self):
        source = C.ROOT / 'releases.md'
        english, target = source.read_text(), source.with_suffix('.de.md').read_text()
        expected = C.G.number_facts(*C.G.split_front_matter(english))
        actual = C.G.number_facts(*C.G.split_front_matter(target))
        self.assertTrue(reviewed_delta(source, english, target, 'de', 'numeric_variant', expected, actual))
        self.assertFalse(reviewed_delta(source, english, target, 'de', 'numeric_variant', expected, actual + Counter({'99': 1})))

    def test_only_patroni_root_alias_is_normalized(self):
        self.assertEqual('/patroni', C.normalize('/de/patroni'))
        self.assertEqual('/de/pgbackrest', C.normalize('/de/pgbackrest'))
        external = 'https://example.com/de/patroni'
        self.assertEqual(external, C.normalize(external))
        self.assertEqual('/patroni', C.G.normalize_german_target('/de/patroni'))
        self.assertEqual(external, C.G.normalize_german_target(external))

    def test_symlinked_build_root_preserves_local_links(self):
        # macOS /var/folders resolves through /private/var. Valid assets must
        # not be rejected merely because the build was supplied via an alias.
        with tempfile.TemporaryDirectory(prefix='patroni-path-test-') as temp:
            root = Path(temp) / 'build'
            root.mkdir()
            (root / 'search.json').write_text('[]')
            (root / 'asset.txt').write_text('shared asset')
            for language in C.LANGUAGES:
                local = root if language == 'en' else root / language
                local.mkdir(exist_ok=True)
                (local / 'navigation.json').write_text(json.dumps({'root': {'children': []}}))
                (local / 'index.html').write_text('<html><body data-td-index-src="/search.json"></body></html>')
                manual = local / 'docs/patroni'
                manual.mkdir(parents=True)
                (manual / 'llms-full.txt').write_text('')
                printing = local / '_print/docs/patroni'
                printing.mkdir(parents=True)
                (printing / 'index.html').write_text('<a href="/asset.txt">asset</a>')
            alias = Path(temp) / 'alias'
            alias.symlink_to(root, target_is_directory=True)
            self.assertEqual([], C.rendered_errors(alias, [])[0])


if __name__ == '__main__':
    unittest.main()
