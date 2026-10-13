#!/usr/bin/env python3
"""Deliberate corruption probes for the shared pgBackRest publication gate."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from copy import deepcopy

spec = importlib.util.spec_from_file_location('pgbackrest_gate', Path(__file__).with_name('check-pgbackrest.py'))
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
sync = gate.load('pgbackrest_example_sync', 'sync-pgbackrest-examples.py')

EN = '''---
title: "Backup reference"
weight: 20
upstream_link: "https://pgbackrest.org/"
---
## Backups

Use `--set` to select a backup. Wait 30 seconds.

- Store the backup in [the repository](/docs/pgbackrest/configuration/#repositories).

```ini
# Keep this comment.
process-max=2
```
'''
FR = '''---
title: "Référence des sauvegardes"
weight: 20
upstream_link: "https://pgbackrest.org/"
---
## Sauvegardes {#backups}

Utilisez `--set` pour sélectionner une sauvegarde. Attendez 30 secondes.

- Stockez la sauvegarde dans [le dépôt](/fr/docs/pgbackrest/configuration/#repositories).

```ini
# Keep this comment.
process-max=2
```
'''


class PublicationGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='pgbackrest-regression-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.addCleanup(patch.stopall)
        patch.object(gate, 'PROJECT', self.root).start()
        self.source = self.root / 'backup.md'
        self.target = self.root / 'backup.fr.md'

    def check(self, english=EN, translated=FR, row=None):
        self.source.write_text(english)
        self.target.write_text(translated)
        return gate.technical_errors(self.source, self.target, row or {})

    def test_valid_translation(self):
        self.assertEqual(self.check(), [])

    def test_corrupt_technical_content(self):
        for old, new, diagnostic in [
            ('process-max=2', 'process-max=3', 'code/config/output'),
            ('# Keep this comment.', '# Traduction', 'code/config/output'),
            ('`--set`', '`--sets`', 'literals'),
            ('30 secondes', '300 secondes', 'numbers'),
            ('weight: 20', 'weight: 30', 'shared metadata'),
            ('{#backups}', '', 'missing explicit'),
            ('\n- Stockez', '\nStockez', 'list structure'),
            ('configuration/#repositories', 'faq/#repositories', 'destinations'),
            ('#repositories)', '#incorrect-section)', 'destinations'),
            ('/fr/docs/', '/docs/', 'still points to English'),
            ('Attendez 30 secondes.', 'Attendez 30 secondes. TODO', 'placeholder'),
        ]:
            with self.subTest(old=old):
                self.assertTrue(any(diagnostic in e for e in self.check(translated=FR.replace(old, new))))

    def test_missing_prose_unit(self):
        omitted = FR.replace('Utilisez `--set` pour sélectionner une sauvegarde. Attendez 30 secondes.\n', '')
        self.assertTrue(any('prose unit coverage' in e for e in self.check(translated=omitted)))

    def test_original_diagnostic_is_not_translated(self):
        errors = self.check(EN + '\nThe error is "could not find WAL segment".\n',
                            FR + '\nErreur : « segment WAL introuvable ».\n')
        self.assertTrue(any('original diagnostic changed' in e for e in errors))

    def test_review_fingerprints_are_independent(self):
        self.check()
        row = {'source_sha256': gate.sha256(self.source), 'translation_sha256': gate.sha256(self.target)}
        self.assertEqual(gate.fingerprint_errors(self.source, self.target, row), [])
        self.target.write_text(FR.replace('sélectionner', 'choisir'))
        self.assertTrue(gate.fingerprint_errors(self.source, self.target, row))
        self.target.write_text(FR)
        self.source.write_text(EN.replace('select', 'choose'))
        self.assertTrue(gate.fingerprint_errors(self.source, self.target, row))

    def test_exception_does_not_hide_other_changes(self):
        english = EN + '\nUse a `space`.\n'
        translated = FR + '\nUtilisez une espace.\n'
        row = {'reviewed_variants': [{'unit': 4, 'difference': {
            'numbers': {'missing': {}, 'extra': {}}, 'literals': ['space']},
            'reason': 'Prose word, not a program identifier.'}]}
        self.assertEqual(self.check(english, translated, row), [])
        self.assertTrue(self.check(english, translated.replace('une espace.', '300 espaces.'), row))
        self.assertTrue(any('obsolete' in e for e in self.check(english, translated.replace('une espace.', 'un `space`.'), row)))

    def test_date_normalization_preserves_numbers(self):
        english = 'Released May 1, 2026. Keep three backups; wait 30 seconds.'
        french = 'Publié le 1er mai 2026. Conserver 3 sauvegardes ; attendre 30 secondes.'
        self.assertEqual(gate.numeric_delta(english, french), {'missing': {}, 'extra': {}})
        self.assertTrue(gate.numeric_delta(english, french.replace('30', '300'))['missing'])

    def test_equivalent_root_urls(self):
        self.assertEqual(gate.links('[site](https://example.com/)', self.source),
                         gate.links('[site](https://example.com)', self.source))


class ExampleSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='pgbackrest-example-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.addCleanup(patch.stopall)
        patch.object(sync, 'ROOT', self.root).start()
        self.old_time = '2026-09-27 10:19:58.808792+00'
        self.new_time = '2026-10-02 19:07:12.060959+00'
        entries = [
            {'type': 'exe', 'key': {'cmd': ['pgbackrest info']}, 'value': {'output': ['pgBackRest 2.59.2', '', 'backup ready']}},
            {'type': 'exe', 'key': {'cmd': ['read-label']}, 'value': {'output': ['20260927-101911F']}},
            {'type': 'exe', 'key': {'cmd': ['pgbackrest --set=20260927-101911F --target=' + self.old_time]}, 'value': {}},
        ]
        self.old = {env: {'all': {'user-guide': deepcopy(entries)}} for env in ('default', '{"os-type":"rhel"}')}
        self.new = deepcopy(self.old)
        for env in self.new.values():
            rows = env['all']['user-guide']
            rows[0]['value']['output'][0] = 'pgBackRest 2.59.3'
            rows[1]['value']['output'] = ['20261002-190624F']
            rows[2]['key']['cmd'][0] = rows[2]['key']['cmd'][0].replace('20260927-101911F', '20261002-190624F').replace(self.old_time, self.new_time)
        self.original = ('Reviewed PITR explanation.\n\n```text\npgBackRest 2.59.2\nbackup ready\n```\n\n'
                         '```sh\npgbackrest --set=20260927-101911F --target=' + self.old_time + '\n```\n')
        for name in ('user-guide', 'user-guide-rhel'):
            for lang in sync.LANGUAGES:
                (self.root / (name + ('' if lang == 'en' else '.' + lang) + '.md')).write_text(self.original)

    def test_cache_outputs_and_interpolated_selectors_remain_consistent(self):
        changes, receipt = sync.prepare(self.old, self.new, '2.59.2', '2.59.3')
        self.assertEqual(len(changes), 12)
        for path, text in changes.items():
            self.assertEqual(path.read_text(), self.original)  # preparation is read-only
            self.assertIn('Reviewed PITR explanation.', text)
            self.assertIn('pgBackRest 2.59.3\n\nbackup ready', text)
            self.assertIn('20261002-190624F', text)
            self.assertIn(self.new_time, text)
            self.assertNotIn(self.old_time, text)
        self.assertEqual(receipt['user-guide']['updated_selector_values'], 2)

    def test_changed_command_identity_requires_manual_review(self):
        self.new['default']['all']['user-guide'][0]['key']['cmd'] = ['pgbackrest restore']
        with self.assertRaisesRegex(ValueError, 'command identity'):
            sync.prepare(self.old, self.new, '2.59.2', '2.59.3')

    def test_changed_translation_block_prevents_all_writes(self):
        path = self.root / 'user-guide-rhel.ru.md'
        path.write_text(self.original.replace('backup ready', 'backup damaged'))
        before = {p: p.read_bytes() for p in self.root.iterdir()}
        with self.assertRaisesRegex(ValueError, 'protected blocks differ'):
            sync.prepare(self.old, self.new, '2.59.2', '2.59.3')
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.iterdir()})

    def test_unmatched_upstream_output_is_not_silently_skipped(self):
        self.old['default']['all']['user-guide'][0]['value']['output'] = ['unmatched old output']
        with self.assertRaisesRegex(ValueError, 'does not match'):
            sync.prepare(self.old, self.new, '2.59.2', '2.59.3')


if __name__ == '__main__':
    unittest.main()
