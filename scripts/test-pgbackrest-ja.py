#!/usr/bin/env python3
"""Regression probes for failures the Japanese current-source gate must catch."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("japanese_parity", Path(__file__).with_name("check-pgbackrest-ja.py"))
parity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parity)

EN = '''---
title: "Backup reference"
weight: 20
upstream_link: "https://pgbackrest.org/"
---
## Backups

Use `--set` to select a backup. Wait 30 seconds.

- Store the backup in [the repository](/docs/pgbackrest/configuration/).

```ini
# Keep this comment.
process-max=2
```
'''
JA = '''---
title: "バックアップリファレンス"
weight: 20
upstream_link: "https://pgbackrest.org/"
---
## バックアップ {#backups}

`--set`でバックアップを選びます。30秒待ちます。

- [リポジトリ](/ja/docs/pgbackrest/configuration/)にバックアップを保存します。

```ini
# Keep this comment.
process-max=2
```
'''


class GateTests(unittest.TestCase):
    def test_translated_pair(self):
        self.assertEqual(parity.compare_text(EN, JA), [])

    def test_technical_and_structure_regressions(self):
        for before, after, diagnostic in [
            ('process-max=2', 'process-max=3', 'code/config/output'),
            ('# Keep this comment.', '# コメント', 'code/config/output'),
            ('`--set`', '`--sets`', 'inline technical'),
            ('30秒', '300秒', 'numeric facts'),
            ('weight: 20', 'weight: 30', 'metadata'),
            ('{#backups}', '', 'lacks explicit'),
            ('\n- [', '\n[', 'list structure'),
            ('/ja/docs/pgbackrest/configuration/', '/ja/docs/pgbackrest/faq/', 'targets'),
        ]:
            with self.subTest(before=before):
                self.assertTrue(any(diagnostic in e for e in parity.compare_text(EN, JA.replace(before, after))))

    def test_english_left_in_mixed_prose(self):
        broken = JA.replace('30秒待ちます。', '30秒待ちます。 The backup must remain in the repository.')
        self.assertTrue(any('explanatory English' in e for e in parity.compare_text(EN, broken)))

    def test_localized_dates_and_spelled_counts(self):
        self.assertEqual(parity.numeric_errors('Released September 27, 2026. Three levels.', '2026年9月27日リリース。3つのレベル。'), [])
        self.assertTrue(parity.numeric_errors('Wait 30 seconds.', '300秒待ちます。'))

    def test_short_text_and_diagnostic_regressions(self):
        self.assertTrue(any('untranslated explanatory heading' in e for e in parity.compare_text(EN, JA.replace('バックアップ {#backups}', 'Backups {#backups}'))))
        a=EN.replace('weight: 20', 'linkTitle: "Commands"\nweight: 20')
        b=JA.replace('weight: 20', 'linkTitle: "Commands"\nweight: 20')
        self.assertTrue(any('linkTitle' in e for e in parity.compare_text(a,b)))
        a=EN+'\nThe error is "could not find WAL segment".\n'
        b=JA+'\nエラーは「WALセグメントが見つかりません」です。\n'
        self.assertTrue(any('program diagnostic' in e for e in parity.compare_text(a,b)))

    def test_table_numbers_remain_on_the_correct_row(self):
        a=EN+"\n| Directory | Lines |\n| --- | --- |\n| src | 30 |\n| test | 40 |\n"
        b=JA+"\n| ディレクトリ | 行数 |\n| --- | --- |\n| src | 40 |\n| test | 30 |\n"
        self.assertTrue(any('row' in e and 'numeric facts' in e for e in parity.compare_text(a,b)))
        self.assertTrue(parity.numeric_errors('Wait one second.', '2秒待ちます。'))

    def test_rendered_component_navigation_never_falls_back(self):
        en=parity.Rendered();ja=parity.Rendered()
        en.feed('<a class="td-shell-tree__link" href="/docs/pgbackrest/configuration/">Configuration</a>')
        ja.feed('<a class="td-shell-tree__link" href="/ja/docs/pgbackrest/configuration/">設定</a>')
        self.assertEqual(parity.navigation_errors(en,ja), [])
        for attrs in ['href="/docs/pgbackrest/configuration/"', 'href="/ja/docs/pgbackrest/configuration/" data-fallback-language="en"']:
            broken=parity.Rendered()
            broken.feed('<a class="td-shell-tree__link" '+attrs+'>設定</a>')
            self.assertTrue(any('fallback' in e for e in parity.navigation_errors(en,broken)))

    def test_legal_diagnostics_are_literal(self):
        self.assertEqual(parity.english_residue('「could not find WAL segment」エラー。'), [])
        self.assertTrue(parity.english_residue('You must enable archiving before the backup.'))

    def test_security_product_heading_is_retained_exactly(self):
        source = EN + '\n### OpenSSL 1.0 {#weak-encryption-openssl-1-0}\n'
        target = JA + '\n### OpenSSL 1.0 {#weak-encryption-openssl-1-0}\n'
        self.assertEqual(parity.compare_text(source, target), [])
        self.assertTrue(parity.compare_text(source, target.replace('### OpenSSL 1.0', '### OpenSSL 1.1')))


if __name__ == '__main__':
    unittest.main()
