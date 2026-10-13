#!/usr/bin/env python3
"""Exercise meaningful regressions in the all-language etcd acceptance gate."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('etcd_test_gate', Path(__file__).with_name('check-etcd.py'))
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
ru_gate = gate


class AcceptanceTests(unittest.TestCase):
    def pair(self, mutate):
        with tempfile.TemporaryDirectory(prefix='etcd-gate-test-') as tmp:
            source = Path(tmp) / 'sample.md'
            target = Path(tmp) / 'sample.fr.md'
            source.write_text('''---
title: Sample
weight: 10
upstream_link: "https://etcd.io/docs/v3.7/"
---
## Read

Use `--limit=10` and [API](/docs/etcd/learning/api/).

```shell
etcdctl get foo
```

| Size | Value |
| --- | --- |
| 1000 | 1.25ms |
''')
            translated = source.read_text().replace('Sample', 'Exemple').replace('## Read', '## Lire {#read}').replace('Use ', 'Utiliser ').replace(' and ', ' et ').replace('/docs/etcd/', '/fr/docs/etcd/').replace('| 1000 | 1.25ms |', '| 1 000 | 1,25ms |')
            target.write_text(mutate(translated))
            row = {'source_sha256':gate.digest(source), 'target_sha256':gate.digest(target)}
            return gate.pair_checks(source, target, row)

    def test_localized_numbers(self):
        self.assertEqual(self.pair(lambda x: x), [])

    def test_changed_command(self):
        self.assertIn('fenced code/output', self.pair(lambda x: x.replace('etcdctl get foo', 'etcdctl del foo')))

    def test_swapped_numeric_columns(self):
        self.assertIn('table numeric cells', self.pair(lambda x: x.replace('| 1 000 | 1,25ms |', '| 1,25ms | 1 000 |')))

    def test_changed_inline_parameter(self):
        self.assertTrue(any('technical inline' in x for x in self.pair(lambda x: x.replace('--limit=10', '--limit=1'))))

    def test_changed_local_link(self):
        self.assertIn('link/asset destinations', self.pair(lambda x: x.replace('learning/api/', 'op-guide/recovery/')))

    def test_changed_source_version(self):
        self.assertIn('metadata upstream_link', self.pair(lambda x: x.replace('/v3.7/', '/v3.6/')))

    def test_comment_exception_cannot_change_values(self):
        with tempfile.TemporaryDirectory(prefix='etcd-gate-test-') as tmp:
            source, target = Path(tmp) / 'sample.md', Path(tmp) / 'sample.fr.md'
            source.write_text('---\ntitle: Sample\n---\n```yaml\n# 10 minutes\nwatch-progress-notify-interval: 600000000000\n```\n')
            target.write_text(source.read_text().replace('# 10 minutes', '# 10 minutes en nanosecondes').replace('600000000000', '60000000000'))
            row = {'source_sha256':gate.digest(source), 'target_sha256':gate.digest(target),
                   'exceptions':{'fenced code/output':{'reason':'localized YAML comments'}}}
            self.assertIn('fenced code/output', gate.pair_checks(source, target, row))

    def test_no_fingerprint_auto_approval(self):
        record = json.loads(gate.RECORD.read_text())
        record['pages'][0]['target_sha256'] = '0' * 64
        self.assertTrue(any('translation changed since acceptance' in x for x in gate.validate(record)))

    def test_missing_pair_record(self):
        record = json.loads(gate.RECORD.read_text())
        record['pages'].pop()
        self.assertTrue(any('review record page set differs' in x for x in gate.validate(record)))

    def test_leaf_bundle_route(self):
        source = gate.PROJECT / 'content/docs/etcd/feature-gates/index.md'
        self.assertEqual(ru_gate.logical_path(source).as_posix(), 'docs/etcd/feature-gates')

    def test_setext_anchor_is_required(self):
        self.assertEqual(ru_gate.heading_anchor_ids('Заголовок {#heading}\n======\n'), ['heading'])
        self.assertEqual(ru_gate.heading_anchor_ids('Заголовок\n======\n'), [None])

    def test_translated_title_order_at_equal_weights(self):
        a, b = {'id':'/a/', 'children':[{'id':'/a/one/'}]}, {'id':'/b/'}
        weights = {'/a/':6000, '/b/':6000, '/a/one/':100}
        self.assertEqual(ru_gate.weighted_tree({'id':'/', 'children':[a,b]}, weights),
                         ru_gate.weighted_tree({'id':'/', 'children':[b,a]}, weights))

    def test_navigation_hierarchy_is_preserved(self):
        weights = {'/a/':6000, '/b/':6000, '/a/one/':100}
        expected = {'id':'/', 'children':[{'id':'/a/', 'children':[{'id':'/a/one/'}]}, {'id':'/b/'}]}
        moved = {'id':'/', 'children':[{'id':'/a/'}, {'id':'/b/', 'children':[{'id':'/a/one/'}]}]}
        self.assertNotEqual(ru_gate.weighted_tree(expected, weights), ru_gate.weighted_tree(moved, weights))

    def test_different_weights_cannot_be_reordered(self):
        with self.assertRaises(AssertionError):
            ru_gate.weighted_tree({'id':'/', 'children':[{'id':'/b/'}, {'id':'/a/'}]}, {'/a/':100, '/b/':200})


if __name__ == '__main__':
    unittest.main()
