#!/usr/bin/env python3
"""Regression checks for HAProxy's exact Russian prose/code review boundary."""

import contextlib
import importlib.util
import io
import json
from collections import Counter
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import translation_fences as fences

spec = importlib.util.spec_from_file_location(
    "russian_parity", Path(__file__).with_name("check-russian-parity.py")
)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
translator_spec = importlib.util.spec_from_file_location(
    "russian_translator", Path(__file__).with_name("translate-russian-docs.py")
)
translator = importlib.util.module_from_spec(translator_spec)
sys.modules[translator_spec.name] = translator
translator_spec.loader.exec_module(translator)
SOURCE = checker.CONTENT / "docs/haproxy/filters.md"


class RussianParityTests(unittest.TestCase):
    def test_parameter_prefix_cannot_open_a_pre_block(self):
        document = (
            '**`server-template <prefix> <num-or-range> <fqdn>[:<port>]`**\n'
            'См. [global](/docs/haproxy/global/#section-3).\n'
            'Буквальный `<pre>` и <code><pre></code> и <kbd><pre></kbd>.\n'
            'См. [proxies](/docs/haproxy/proxies/).\n'
            '`/docs/haproxy/global/`\n'
            '<code>/docs/haproxy/global/</code>\n'
            '<kbd>/docs/haproxy/global/</kbd>\n'
            '![image](/docs/haproxy/image.svg)\n'
        )
        expected = document.replace('](/docs/haproxy/global/#', '](/ru/docs/haproxy/global/#')
        expected = expected.replace('](/docs/haproxy/proxies/)', '](/ru/docs/haproxy/proxies/)')
        localized = translator.localize_internal_links(document)
        self.assertEqual(localized, expected)
        self.assertEqual(translator.localize_internal_links(localized), localized)
        self.assertEqual(translator.normalize_localized_routes(localized), document)

    def test_real_pre_and_other_code_blocks_keep_literal_routes(self):
        document = (
            '<PRE class="literal">\n/docs/haproxy/global/\n</PRE >\n'
            'См. [global](/docs/haproxy/global/).\n\n'
            '```shell\n/docs/haproxy/global/\n```\n\n'
            '    /docs/haproxy/global/\n\n'
            'См. [proxies](/docs/haproxy/proxies/).\n'
        )
        expected = document.replace('](/docs/haproxy/global/)', '](/ru/docs/haproxy/global/)')
        expected = expected.replace('](/docs/haproxy/proxies/)', '](/ru/docs/haproxy/proxies/)')
        localized = translator.localize_internal_links(document)
        self.assertEqual(localized, expected)
        self.assertEqual(translator.normalize_localized_routes(localized), document)

    def test_nested_list_routes_roundtrip_with_the_same_code_boundary(self):
        document = '- Родитель\n\n    - [global](/docs/haproxy/global/)\n'
        localized = translator.localize_internal_links(document)
        self.assertIn('](/ru/docs/haproxy/global/)', localized)
        self.assertEqual(translator.normalize_localized_routes(localized), document)

    def test_route_normalization_cannot_hide_an_external_url_change(self):
        external = '[external](https://example.org/ru/docs/haproxy/global/)\n'
        self.assertEqual(translator.localize_internal_links(external), external)
        self.assertEqual(translator.normalize_localized_routes(external), external)
        changed = external.replace('/ru/docs/', '/docs/')
        self.assertNotEqual(translator.normalize_localized_routes(external),
                            translator.normalize_localized_routes(changed))

    def test_parity_route_normalization_preserves_external_and_embedded_paths(self):
        for value in (
                'https://example.org/ru/docs/haproxy/global/',
                '<a href="https://example.org/ru/docs/haproxy/global/">',
                '[external]: https://example.org/ru/docs/haproxy/global/',
                '/other/ru/docs/haproxy/global/'):
            self.assertEqual(checker.normalized_target(value), value)
        for value in (
                '/ru/docs/haproxy/global/',
                '<a href="/ru/docs/haproxy/global/">',
                '[local]: /ru/docs/haproxy/global/',
                'https://doc.pg.center/ru/docs/haproxy/global/'):
            self.assertEqual(checker.normalized_target(value), value.replace('/ru/docs/', '/docs/'))

    def test_external_url_queries_and_embedded_paths_remain_literal(self):
        for localized in (
                'https://example.org/-/ru/docs/haproxy/global/',
                '/other-/ru/docs/haproxy/global/',
                'https://example.org/?url=/ru/docs/haproxy/global/',
                '<a href="https://example.org/-/ru/docs/haproxy/global/">',
                '[external]: https://example.org/-/ru/docs/haproxy/global/'):
            self.assertEqual(checker.normalized_target(localized), localized)
            self.assertEqual(translator.normalize_localized_routes(localized), localized)
            english = localized.replace('/ru/docs/', '/docs/')
            self.assertEqual(translator.localize_internal_links(english), english)
        root = '/docs/haproxy/global/?next=/docs/haproxy/proxies/#example'
        localized = '/ru' + root
        self.assertEqual(translator.localize_internal_links(root), localized)
        self.assertEqual(translator.normalize_localized_routes(localized), root)
        self.assertEqual(checker.normalized_target(localized), root)

    def test_route_transforms_leave_non_url_html_attributes_exact(self):
        original = '<a id="/docs/haproxy/global/" data-note="/docs/haproxy/global/" href="/docs/haproxy/global/">'
        localized = original.replace('href="/docs/', 'href="/ru/docs/')
        self.assertEqual(translator.localize_internal_links(original), localized)
        self.assertEqual(translator.normalize_localized_routes(localized), original)
        self.assertEqual(checker.normalized_target(localized), original)
        fake_anchor = localized.replace('id="/docs/', 'id="/ru/docs/')
        self.assertNotEqual(checker.normalized_target(fake_anchor), original)

    def test_route_localization_preserves_frontmatter_aliases(self):
        header = '---\ntitle: Тест\naliases:\n  - /docs/haproxy/old/\n---\n'
        document = header + '[global](/docs/haproxy/global/)\n'
        localized = header + '[global](/ru/docs/haproxy/global/)\n'
        self.assertEqual(translator.localize_internal_links(document), localized)
        self.assertEqual(translator.localize_internal_links(localized), localized)
        self.assertEqual(translator.normalize_localized_routes(localized), document)

    def test_balanced_parentheses_in_urls_cannot_expose_an_inner_route(self):
        for value in ('https://example.org/(x)/ru/docs/haproxy/global/',
                      '/other(x)/ru/docs/haproxy/global/'):
            self.assertEqual(checker.normalized_target(value), value)
            self.assertEqual(translator.normalize_localized_routes(value), value)
            english = value.replace('/ru/docs/', '/docs/')
            self.assertEqual(translator.localize_internal_links(english), english)
        image = '![image](/docs/haproxy/image.svg).\n'
        self.assertEqual(translator.localize_internal_links(image), image)
        document = '[global](/docs/haproxy/global/?arg=(x))\n'
        localized = document.replace('](/docs/', '](/ru/docs/')
        self.assertEqual(translator.localize_internal_links(document), localized)
        self.assertEqual(translator.normalize_localized_routes(localized), document)

    def test_inline_arguments_are_not_html_but_remain_protected(self):
        en = 'Size at `<offset1>` for `<length>` bytes.\n<a id="real"></a>\n'
        ru = 'Размер поля длиной `<length>` байтов по смещению `<offset1>`.\n<a id="real"></a>\n'
        left, right = checker.protected_inline(en), checker.protected_inline(ru)
        self.assertEqual(Counter(left[1]), Counter(right[1]))
        self.assertEqual(left[3], right[3])
        self.assertEqual(left[3], ['<a id="real">', '</a>'])
        changed_code = checker.protected_inline(ru.replace('`<length>`', '`<other>`'))
        self.assertNotEqual(Counter(left[1]), Counter(changed_code[1]))
        changed_html = checker.protected_inline(ru.replace('id="real"', 'id="other"'))
        self.assertNotEqual(left[3], changed_html[3])

    def test_placeholder_in_reviewed_explanation_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'filters.ru.md'
            en = '```text\n<name> is required.\n```\n'
            ru = '```text\n<name> обязателен. TRANSLATE_ME\n```\n'
            target.write_text('---\ntitle: Тест\n---\n' + ru)
            registry = self.reviewed(en, ru)
            with patch.object(checker, 'read_source', return_value=('---\ntitle: Test\n---\n' + en, None)), \
                    patch.object(fences, 'load_manifest', return_value=registry):
                errors = checker.strict_structure(SOURCE, target, True)
            self.assertTrue(any('placeholder' in error for error in errors), errors)
            code = '```shell\necho TODO\n```\n'
            target.write_text('---\ntitle: Тест\n---\n' + code)
            with patch.object(checker, 'read_source', return_value=('---\ntitle: Test\n---\n' + code, None)), \
                    patch.object(fences, 'load_manifest', return_value={}):
                self.assertEqual(checker.strict_structure(SOURCE, target, True), [])

    def test_language_metadata_cannot_hide_english_prose_links(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / 'ru/docs/haproxy/filters/index.html'
            page.parent.mkdir(parents=True)
            for name in ('filters', 'global'):
                destination = root / f'docs/haproxy/{name}/index.html'
                destination.parent.mkdir(parents=True)
                destination.write_text('<html></html>')
            metadata = '<link rel="canonical" href="https://doc.pg.center/ru/docs/haproxy/filters/">'
            alternate = '<link rel="alternate" hreflang="en-US" href="https://doc.pg.center/docs/haproxy/filters/">'
            switch = '<a class="td-language-selector__item" hreflang="en-US" href="/docs/haproxy/filters/">English</a>'
            notice = '<div class="td-page-meta__translation"><span><a href="/docs/haproxy/filters/">оригинал</a></span></div>'
            page.write_text(metadata + alternate + switch + notice)
            self.assertEqual(checker.check_collection_links('haproxy', root, [page]), [])
            for fake in (
                    '<a hreflang="en" href="/docs/haproxy/global/">Other page</a>',
                    '<a class="td-language-selector__item" hreflang="en-US" href="/docs/haproxy/global/">Other page</a>',
                    '<a href="../../../../docs/haproxy/global/">Relative English page</a>',
                    '<a href="/%64ocs/haproxy/global/">Encoded English page</a>',
                    '<a _translation_notice="true" href="/docs/haproxy/filters/">Forged source notice</a>',
                    '<a href="https://doc.pg.center/docs/haproxy/filters/">Same page in prose</a>'):
                page.write_text(metadata + alternate + switch + notice + fake)
                errors = checker.check_collection_links('haproxy', root, [page])
                self.assertTrue(any('English fallback' in error for error in errors), errors)

    def test_shared_stylesheet_cannot_acquire_a_locale_prefix(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / 'ru/docs/haproxy/filters/index.html'
            page.parent.mkdir(parents=True)
            for relative in ('css/site.css', 'ru/css/site.css'):
                asset = root / relative
                asset.parent.mkdir(parents=True)
                asset.write_text('body{}')
            page.write_text('<link rel="stylesheet" href="/css/site.css">')
            self.assertEqual(checker.check_collection_links('haproxy', root, [page]), [])
            for href in ('/ru/css/site.css', '/ru/%63ss/site.css', '../../../css/site.css'):
                page.write_text(f'<link rel="stylesheet" href="{href}">')
                errors = checker.check_collection_links('haproxy', root, [page])
                self.assertTrue(any('locale prefix' in error for error in errors), errors)

    def reviewed(self, english, russian, **extra):
        return {"fences": [{
            "index": 1, "classification": "mixed-explanation",
            "source_sha256": fences.sha256(english),
            "target_sha256": fences.sha256(russian), **extra,
        }]}

    def check_fences(self, english, russian, manifest):
        errors = []
        with patch.object(fences, "load_manifest", return_value=manifest):
            fences.validate_fences(SOURCE, english, russian, errors, language="ru")
        return errors

    def test_translation_registry_does_not_exempt_other_code(self):
        en = '```text\n<name> is required.\n```\n'
        ru = '```text\n<name> обязателен.\n```\n'
        code = '```haproxy\nserver app 127.0.0.1:80\n```\n'
        registry = self.reviewed(en, ru)
        self.assertEqual(self.check_fences([en, code], [ru, code], registry), [])
        self.assertTrue(self.check_fences([en, code], [ru, code.replace(':80', ':81')], registry))
        self.assertTrue(self.check_fences([en], [ru], {}))

    def test_exact_source_and_target_hashes_are_both_required(self):
        en = '```text\n<name> is required.\n```\n'
        ru = '```text\n<name> обязателен.\n```\n'
        registry = self.reviewed(en, ru)
        self.assertTrue(self.check_fences([en.replace('required', 'optional')], [ru], registry))
        self.assertTrue(self.check_fences([en], [ru.replace('обязателен', 'необязателен')], registry))

    def test_rehashing_cannot_hide_protected_code_or_numeric_changes(self):
        en = '```text\nserver app 127.0.0.1:80\n<name> waits 10 ms.\n```\n'
        ru = '```text\nserver app 127.0.0.1:80\n<name> ждёт 10 ms.\n```\n'
        protections = {"protected_lines": ['server app 127.0.0.1:80'],
                       "protected_literals": ['ms']}
        for changed in (ru.replace('server app', 'server other'),
                        ru.replace('10 ms', '11 ms'), ru.replace('ms', 's'),
                        ru.replace('<name>', '<other>')):
            registry = self.reviewed(en, changed, **protections)
            self.assertTrue(self.check_fences([en], [changed], registry))

    def test_explanatory_inline_labels_are_page_and_language_scoped(self):
        source = checker.CONTENT / "docs/haproxy/starting.md"
        inline = Counter({'`- the version`': 1, '`-v`': 1})
        expected = Counter({'`- версия`': 1, '`-v`': 1})
        self.assertEqual(fences.translated_inline_labels(source, inline, 'ru'), expected)
        self.assertNotEqual(fences.translated_inline_labels(source, inline, 'de'), expected)
        self.assertEqual(fences.translated_inline_labels(SOURCE, inline, 'ru'), inline)

    def test_arbitrary_haproxy_fence_cannot_be_called_a_prose_label(self):
        en = '```haproxy\nserver app 127.0.0.1:80\n```\n'
        ru = '```haproxy\nсервер app 127.0.0.1:80\n```\n'
        registry = self.reviewed(en, ru)
        registry['fences'][0]['classification'] = 'explanation-label'
        self.assertTrue(self.check_fences([en], [ru], registry))

    def test_unfenced_real_output_remains_protected(self):
        source = checker.CONTENT / 'docs/haproxy/starting.md'
        output = 'Total: 3 (3 usable), will use epoll.\n'
        with patch.object(fences, 'literal_blocks', return_value=[output]):
            with patch.object(fences, 'load_manifest', return_value={}):
                good, bad = [], []
                fences.validate_literal_blocks(source, output, good, 'ru')
                fences.validate_literal_blocks(source, output.replace('Total', 'Итого'), bad, 'ru')
        self.assertEqual(good, [])
        self.assertTrue(bad)

    def test_literal_snippets_preserve_commands_inside_translated_prose(self):
        command = 'server app 127.0.0.1:80 check'
        english = 'Example: ' + command + '\nAgain: ' + command + '\n'
        russian = 'Пример: ' + command + '\nПовтор: ' + command + '\n'
        registry = {'literal_snippets': [{
            'text': command, 'classification': 'configuration',
            'source_sha256': fences.sha256(command),
        }]}
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'page.md'
            source.write_text(english)
            with patch.object(fences, 'load_manifest', return_value=registry):
                good, altered, missing = [], [], []
                fences.validate_literal_blocks(source, russian, good, 'ru')
                fences.validate_literal_blocks(source, russian.replace('check', 'проверка'), altered, 'ru')
                fences.validate_literal_blocks(source, russian.splitlines()[0], missing, 'ru')
                self.assertNotIn(command, fences.prose_for_lint(source, russian, 'ru'))
            self.assertEqual(good, [])
            self.assertTrue(altered)
            self.assertTrue(missing)
            registry['literal_snippets'][0]['source_sha256'] = 'stale'
            with self.assertRaises(ValueError):
                fences.literal_blocks(source, registry)

    def test_russian_third_party_does_not_waive_other_numeric_facts(self):
        self.assertEqual(checker.numeric_tokens('a 3rd party with 10 clients'),
                         checker.numeric_tokens('стороной третьей стороны с 10 клиентами'))
        self.assertNotEqual(checker.numeric_tokens('a 3rd party with 10 clients'),
                            checker.numeric_tokens('стороной третьей стороны с 11 клиентами'))

    def test_indented_explanation_review_is_exact(self):
        en, ru = 'FCGI_MAX_REQS accepts 1 request.', 'FCGI_MAX_REQS принимает 1 запрос.'
        registry = {'indented_prose': [{
            'source_sha256': checker.text_digest(en),
            'target_sha256': checker.text_digest(ru),
            'reason': 'Connection-variable explanation, not output.',
            'protected_literals': ['FCGI_MAX_REQS'],
        }]}
        with patch.object(checker, 'load_manifest', return_value=registry):
            good, bad = [], []
            checker.validate_indented_explanations(SOURCE, '    '+en, '    '+ru, good)
            checker.validate_indented_explanations(SOURCE, '    '+en, '    '+ru+'!', bad)
        self.assertEqual(good, [])
        self.assertTrue(bad)

    def test_rendered_code_exemption_is_an_exact_pair_not_a_block_index(self):
        en = ['Description.\n', 'server app 127.0.0.1:80\n']
        ru = ['Описание.\n', en[1]]
        reviewed = {('Description.', 'Описание.')}
        self.assertTrue(checker.rendered_code_matches(en, ru, reviewed))
        self.assertFalse(checker.rendered_code_matches(en, [ru[0], en[1].replace(':80', ':81')], reviewed))
        self.assertFalse(checker.rendered_code_matches(en, ru[:1], reviewed))

    def test_rendered_indented_prose_splits_at_fences_without_losing_code(self):
        body = '    Before.\n\n```text\nserver app 127.0.0.1:80\n```\n\n    After.\n'
        self.assertEqual(checker.indented_fragments(body, split_at_fences=True), ['Before.', 'After.'])
        self.assertEqual(len(checker.indented_fragments(body)), 1)
        reviewed = {('Before.', 'До.'), ('After.', 'После.')}
        en = ['Before.\n', 'server app 127.0.0.1:80\n', 'After.\n']
        ru = ['До.\n', 'server app 127.0.0.1:80\n', 'После.\n']
        self.assertTrue(checker.rendered_code_matches(en, ru, reviewed))
        self.assertFalse(checker.rendered_code_matches(en, [ru[0], ru[1].replace(':80', ':81'), ru[2]], reviewed))

    def strict(self, english, russian):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'page.ru.md'
            target.write_text('---\ntitle: Тест\n---\n'+russian)
            with patch.object(checker, 'read_source', return_value=('---\ntitle: Test\n---\n'+english, None)):
                return checker.strict_structure(SOURCE, target, True)

    def test_wrapped_dates_are_not_lists_but_real_numbering_is_protected(self):
        self.assertEqual(self.strict('Released in early\n2015. See RFC\n4492).\n',
                                     'Выпущено в начале 2015. См. RFC 4492).\n'), [])
        self.assertTrue(self.strict('1. First\n2. Second\n', '1. Первый\n3. Второй\n'))
        self.assertTrue(self.strict('- First\n  - Nested\n', '- Первый\n- Вложенный\n'))

    def test_component_gate_requires_missing_pages_and_rejects_orphans(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            component = root / 'content/docs/haproxy'
            component.mkdir(parents=True)
            (component / '_index.md').write_text('---\ntitle: Test\n---\n')
            args = ['check-russian-parity.py', '--component', 'haproxy', '--current-source']
            with patch.object(checker, 'PROJECT', root), patch.object(checker, 'CONTENT', root/'content'), patch.object(sys, 'argv', args), patch.object(checker, 'compare_pair', return_value=[]):
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(checker.main(), 1)
                    (component / '_index.ru.md').write_text('---\ntitle: Тест\n---\n')
                    self.assertEqual(checker.main(), 0)
                    (component / 'orphan.ru.md').write_text('---\ntitle: Тест\n---\n')
                    self.assertEqual(checker.main(), 1)

    def test_complete_llms_bodies_and_order_are_required(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            nodes = [{'id': '/docs/haproxy/'}, {'id': '/docs/haproxy/proxies/'}]
            bodies = ['# Руководство\n\nПервый абзац.\n\nПоследний абзац.\n',
                      '# Прокси\n\n- Условие\n- Исключение\n']
            for node, body in zip(nodes, bodies):
                path = root / 'ru' / node['id'].lstrip('/') / 'index.md'
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body)
            entries = ['================\nSource: https://doc.pg.center/ru' + node['id'] +
                       'index.md\n================\n\n' + body for node, body in zip(nodes, bodies)]
            llms = root / 'ru/docs/haproxy/llms-full.txt'
            llms.write_text('\n'.join(entries))
            self.assertEqual(checker.check_full_agent_outputs(root, nodes), [])
            llms.write_text('\n'.join(entries).replace('Последний абзац.', ''))
            self.assertTrue(checker.check_full_agent_outputs(root, nodes))
            llms.write_text('\n'.join(reversed(entries)))
            self.assertTrue(checker.check_full_agent_outputs(root, nodes))

    def test_semantic_review_is_bound_to_final_source_and_target_hashes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'content/docs/haproxy/proxies.md'
            source.parent.mkdir(parents=True)
            target = source.with_name('proxies.ru.md')
            source.write_text('Current English')
            target.write_text('Проверенный перевод')
            path = root / 'data/translation-audits/haproxy-ru.json'
            path.parent.mkdir(parents=True)
            row = {'source': source.relative_to(root).as_posix(), 'change': 'added',
                   'source_sha256': checker.text_digest(source.read_text()),
                   'target_sha256': checker.text_digest(target.read_text()),
                   'semantic_review': {'status': 'complete', 'method': 'separate comparison',
                                       'separate_review': 'complete', 'note': 'All conditions reviewed'}}
            path.write_text(json.dumps({'pages': [row]}))
            with patch.object(checker, 'PROJECT', root):
                self.assertEqual(checker.check_semantic_review('haproxy', [source]), [])
                target.write_text('Позднее неподтверждённое изменение')
                self.assertTrue(checker.check_semantic_review('haproxy', [source]))
                target.write_text('Проверенный перевод')
                row['semantic_review']['separate_review'] = 'pending'
                path.write_text(json.dumps({'pages': [row]}))
                self.assertTrue(checker.check_semantic_review('haproxy', [source]))
                for invalid in (None, 'typo'):
                    row['change'] = invalid
                    path.write_text(json.dumps({'pages': [row]}))
                    errors = checker.check_semantic_review('haproxy', [source])
                    self.assertTrue(any('classification' in error for error in errors), errors)

    def test_legacy_alias_formats_and_canonical_refresh(self):
        self.assertEqual(checker.front_aliases('aliases: [/haproxy/a/, /haproxy/b/]\n'),
                         ['/haproxy/a/', '/haproxy/b/'])
        self.assertEqual(checker.front_aliases('aliases:\n  - /haproxy/a/\n  - /haproxy/b/\nweight: 10\n'),
                         ['/haproxy/a/', '/haproxy/b/'])
        with tempfile.TemporaryDirectory() as folder:
            page = Path(folder) / 'alias.html'
            destination = 'https://doc.pg.center/ru/docs/haproxy/proxies/'
            page.write_text('<html lang="ru-RU"><link rel="canonical" href="' + destination +
                            '"><meta http-equiv="refresh" content="0; url=' + destination + '"></html>')
            document = checker.RenderedContent(page)
            self.assertEqual(document.canonical, [destination])
            self.assertEqual(document.refresh, [destination])


if __name__ == '__main__':
    unittest.main()
