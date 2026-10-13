#!/usr/bin/env python3
"""Regression tests for rendered Japanese pgBackRest print body coverage."""

import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location(
    'print_parity', Path(__file__).with_name('check-pgbackrest-ja-print.py')
)
parity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parity)


class PrintBodyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.content = self.base / 'content'
        self.build = self.base / 'build'
        self.sources = [
            self.content / 'docs/pgbackrest/_index.md',
            self.content / 'docs/pgbackrest/command/backup.md',
            self.content / 'docs/pgbackrest/command/restore.md',
        ]
        for source in self.sources:
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text('---\ntitle: Reference\n---\n', encoding='utf-8')

        self.backup_id = self.section_id('command/backup.ja.md')
        self.restore_id = self.section_id('command/restore.ja.md')
        self.paragraph = '<p>バックアップには<code>--set</code>を指定します。</p>'
        self.item = '<li>最初のリポジトリを使用します。</li>'
        self.code = '<pre><code>process-max=2\nrepo1-path=/backup\n</code></pre>'
        self.table = (
            '<table><thead><tr><th>項目</th><th>値</th></tr></thead>'
            '<tbody><tr><td>process-max</td><td>2</td></tr></tbody></table>'
        )
        self.backup_body = (
            '<h2 id="options">オプション</h2>' + self.paragraph
            + '<ul>' + self.item + '<li>保存先を確認します。</li></ul>'
            + self.code + self.table
        )
        root_body = '<hr><h2 id="introduction">はじめに</h2><p>バックアップの概要です。</p>'
        restore_body = '<h2 id="restore">リストア</h2><p>バックアップからリストアします。</p>'
        normal_pages = [
            ('docs/pgbackrest', 'pgBackRest', root_body),
            ('docs/pgbackrest/command/backup', 'バックアップ', self.backup_body),
            ('docs/pgbackrest/command/restore', 'リストア', restore_body),
        ]
        for route, title, body in normal_pages:
            normal = (
                '<html><body><main><div class="td-content">'
                '<div class="td-page-heading"><h1>' + title + '</h1></div>'
                '<div class="lead"><p>通常ページのリード文。</p></div>'
                '<header class="td-article-meta"><ul><li>カテゴリー</li></ul></header>'
                + body
                + '<div class="td-section-index"><p>自動生成されたページ一覧。</p></div>'
                '<div class="td-page-end"><p>コメント欄。</p></div>'
                '</div></main></body></html>'
            )
            self.write(self.build / 'ja' / route / 'index.html', normal)

        self.backup_section = self.print_section(self.backup_id, '1 - バックアップ', self.backup_body)
        self.restore_section = self.print_section(self.restore_id, '2 - リストア', restore_body)
        self.bundle = (
            '<html><body><main><div class="td-content">'
            '<div class="td-page-notice"><p>複数ページの印刷画面です。</p></div>'
            '<h1 class="title">pgBackRest</h1><div class="lead">印刷用リード文。</div>'
            '<ul><li>1: <a href="#' + self.backup_id + '">バックアップ</a></li>'
            '<li>2: <a href="#' + self.restore_id + '">リストア</a></li></ul>'
            + root_body + '</div>' + self.backup_section + self.restore_section
            + '</main></body></html>'
        )
        self.bundle_path = self.build / 'ja/_print/docs/pgbackrest/index.html'
        self.write(self.bundle_path, self.bundle)

    @staticmethod
    def section_id(relative):
        return 'pg-' + hashlib.md5(('docs/pgbackrest/' + relative).encode()).hexdigest()

    @staticmethod
    def print_section(section_id, title, body):
        return (
            '<div class="td-content" style="page-break-before:always">'
            '<h1 id="' + section_id + '">' + title + '</h1>'
            '<div class="lead">印刷用の説明。</div>' + body + '</div>'
        )

    @staticmethod
    def write(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def check(self, bundle=None):
        if bundle is not None:
            self.write(self.bundle_path, bundle)
        return parity.check_print(self.build, self.sources, self.content)

    def assert_body_failure(self, bundle):
        errors, _ = self.check(bundle)
        self.assertTrue(any('print body differs' in error for error in errors), errors)

    def test_complete_body_matches_despite_generated_page_chrome(self):
        errors, pages = self.check()
        self.assertEqual(errors, [])
        self.assertEqual(len(pages), 3)
        self.assertTrue(all(page['match'] and page['expected_blocks'] > 0 for page in pages))

    def test_missing_paragraph_list_code_and_table_content(self):
        for label, fragment in [
            ('paragraph', self.paragraph),
            ('list item', self.item),
            ('code', self.code),
            ('table', self.table),
            ('table heading', '<th>値</th>'),
            ('table cell', '<td>2</td>'),
        ]:
            with self.subTest(label=label):
                self.assertIn(fragment, self.bundle)
                self.assert_body_failure(self.bundle.replace(fragment, '', 1))

    def test_heading_only_print_section_fails(self):
        broken = self.bundle.replace(self.backup_body, '<h2 id="options">オプション</h2>', 1)
        self.assert_body_failure(broken)

    def test_reordered_and_duplicated_content_fails(self):
        reordered = self.backup_body.replace(self.paragraph, '').replace(self.code, self.code + self.paragraph)
        for replacement in [reordered, self.backup_body + self.paragraph]:
            with self.subTest(replacement=replacement):
                self.assert_body_failure(self.bundle.replace(self.backup_body, replacement, 1))

    def test_changed_code_value_or_whitespace_fails(self):
        for before, after in [('process-max=2', 'process-max=3'), ('repo1-path=/backup\n', 'repo1-path=/backup \n')]:
            with self.subTest(before=before, after=after):
                self.assert_body_failure(self.bundle.replace(before, after, 1))

    def test_wrong_chapter_ids_fail(self):
        broken = self.bundle.replace('id="' + self.backup_id + '"', 'id="temporary"')
        broken = broken.replace('id="' + self.restore_id + '"', 'id="' + self.backup_id + '"')
        broken = broken.replace('id="temporary"', 'id="' + self.restore_id + '"')
        self.assert_body_failure(broken)

    def test_missing_and_duplicate_chapters_fail(self):
        for label, broken, diagnostic in [
            ('missing', self.bundle.replace(self.restore_section, ''), 'missing print section'),
            ('duplicate', self.bundle.replace('</main>', self.backup_section + '</main>'), 'duplicate print section ID'),
        ]:
            with self.subTest(label=label):
                errors, _ = self.check(broken)
                self.assertTrue(any(diagnostic in error for error in errors), errors)


if __name__ == '__main__':
    unittest.main()
