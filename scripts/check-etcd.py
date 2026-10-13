#!/usr/bin/env python3
"""Validate the reviewed etcd snapshot in every language, optionally with a build.

Fingerprints bind this acceptance to exact bytes; they do not establish semantic
accuracy. The accompanying record describes the actual human/agent review scope.
This read-only gate never refreshes approvals or creates build artifacts.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / 'content/docs/etcd'
RECORD = PROJECT / 'data/translation-audits/etcd.json'
LANGUAGES = {'en': 'en-US', 'zh': 'zh-CN', 'fr': 'fr-FR',
             'ja': 'ja-JP', 'de': 'de-DE', 'ru': 'ru-RU'}


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, PROJECT / 'scripts' / filename)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


generic = module('etcd_all_generic', 'etcd_structure.py')
german = module('etcd_all_german', 'check-etcd-german.py')
pages = module('etcd_all_pages', 'check-etcd-ja-rendered.py')
printing = german.printing
parity = german.parity
links = german.links


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources():
    return sorted(p for p in CONTENT.rglob('*.md') if parity.is_english_source(p))


def prefix(language):
    return '' if language == 'en' else '/' + language


def logical_path(source):
    relative = source.relative_to(PROJECT / 'content')
    route = relative.parent if source.stem in {'_index', 'index'} else relative.with_suffix('')
    return Path(route.as_posix().lower())


def heading_anchor_ids(body):
    return [heading.anchor for heading in parity.heading_rows(body)]


def weighted_tree(node, weights):
    children = node.get('children', [])
    values = [weights[child['id']] for child in children]
    assert values == sorted(values), 'navigation sibling weights are not ordered'
    return node['id'], tuple(sorted((weighted_tree(child, weights) for child in children),
                                  key=lambda item: item[0]))


def technical_inline(body):
    _, prose = generic.parse_fenced_blocks(body)
    return Counter(value for value in generic.INLINE_CODE_RE.findall(prose)
                   if re.search(r'[A-Za-z0-9]', value)
                   and (' ' not in value or re.search(r'[/_=:0-9]|--', value)))


def table_numbers(body, language='en'):
    # French decimal commas and grouped thousands are presentation changes.
    # Normalize within cells, preserving their position and units.
    for block in german.fenced_blocks(body):
        body = body.replace(block, '', 1)
    rows = []
    for line in body.splitlines():
        if not line.lstrip().startswith('|'):
            continue
        cells = []
        for value in re.split(r'(?<!\\)\|', line):
            if language == 'fr':
                value = re.sub(r'(?<=\d)[ \u00a0\u202f](?=\d{3}(?:\D|$))', '', value)
                value = re.sub(r'(?<=\d),(?=\d)', '.', value)
            else:
                value = re.sub(r'(?<=\d),(?=\d{3}(?:\D|$))', '', value)
            cells.append(Counter(parity.NUMBER_RE.findall(value)))
        rows.append(cells)
    return rows


def pair_checks(source, target, row):
    errors = []
    sf, sb = generic.split_front_matter(source.read_text())
    tf, tb = generic.split_front_matter(target.read_text())
    lang = target.name.rsplit('.', 2)[-2]
    en_front, target_front = parity.front_matter_blocks(sf), parity.front_matter_blocks(tf)
    structural_keys = (set(en_front) | set(target_front)) - parity.TRANSLATABLE_FRONT_MATTER
    for key in structural_keys:
        if en_front.get(key) != target_front.get(key):
            errors.append('metadata ' + key)
    for name, expected, actual in (
        ('fenced code/output', german.fenced_blocks(sb), german.fenced_blocks(tb)),
        ('table shape', generic.table_signature(sb), generic.table_signature(tb)),
        ('table numeric cells', table_numbers(sb), table_numbers(tb, lang)),
        ('list structure', generic.list_signature(sb), generic.list_signature(tb)),
        ('heading levels', [x.level for x in parity.heading_rows(sb)],
         [x.level for x in parity.heading_rows(tb)]),
        ('HTML comments', generic.html_comments(sb), generic.html_comments(tb)),
    ):
        if expected != actual:
            exception = row.get('exceptions', {}).get(name, {})
            # Exceptions require the exact approved source/target bytes and a
            # narrow stated reason. Any later edit invalidates the approval.
            valid = bool(exception.get('reason') and row.get('source_sha256') == digest(source)
                         and row.get('target_sha256') == digest(target))
            if name == 'fenced code/output' and valid:
                # Localized YAML comments can differ; configuration values,
                # diagnostics and executable lines remain byte-for-byte equal.
                def without_yaml_comments(block):
                    if not re.match(r'^[ \t]*(?:>[ \t]*)*`{3,}yaml\s*\n', block):
                        return block
                    return ''.join(line for line in block.splitlines(keepends=True)
                                   if not re.match(r'^[ \t]*(?:>[ \t]*)*#', line))
                valid = ([without_yaml_comments(x) for x in expected]
                         == [without_yaml_comments(x) for x in actual])
            if not valid:
                errors.append(name)
    missing = technical_inline(sb) - technical_inline(tb)
    if missing:
        errors.append('technical inline literals: ' + repr(list(missing.elements())[:8]))
    en_links = Counter(generic.link_targets(sb, 'etcd'))
    translated_links = Counter(x.replace('/' + lang + '/docs/etcd/', '/docs/etcd/')
                               for x in generic.link_targets(tb, 'etcd'))
    if en_links != translated_links:
        errors.append('link/asset destinations')
    return errors


def validate(record, rendered=None):
    errors = []
    def require(value, message):
        if not value:
            errors.append(message)
    srcs = sources()
    require(len(srcs) == 99, 'English page count differs from reviewed 99-page edition')
    actual_assets = {str(p.relative_to(PROJECT)) for p in CONTENT.rglob('*')
                     if p.is_file() and p.suffix != '.md'}
    asset_rows = record.get('shared_assets', [])
    require(len(asset_rows) == len(actual_assets) == 42 and
            {a['source'] for a in asset_rows} == actual_assets,
            'shared asset inventory differs from the reviewed42files')
    for asset in asset_rows:
        path = PROJECT / asset['source']
        require(path.is_file() and digest(path) == asset['sha256'], asset['source'] + ': shared asset changed')
    rows = record.get('pages', [])
    by_target = {row['target']: row for row in rows}
    expected_targets = {str(s.with_suffix('.' + l + '.md').relative_to(PROJECT))
                        for s in srcs for l in LANGUAGES if l != 'en'}
    require(len(rows) == len(by_target) == 495, 'review pair count/uniqueness differs')
    require(set(by_target) == expected_targets, 'review record page set differs')
    for lang in LANGUAGES:
        if lang == 'en':
            continue
        expected = {s.with_suffix('.' + lang + '.md') for s in srcs}
        require(set(CONTENT.rglob('*.' + lang + '.md')) == expected,
                lang + ': missing or orphan translations')
        for source in srcs:
            target = source.with_suffix('.' + lang + '.md')
            key = str(target.relative_to(PROJECT))
            row = by_target.get(key, {})
            require(row.get('source') == str(source.relative_to(PROJECT)), key + ': wrong source pair')
            require(row.get('source_sha256') == digest(source), key + ': source changed since acceptance')
            if not target.is_file():
                continue
            require(row.get('target_sha256') == digest(target), key + ': translation changed since acceptance')
            for issue in pair_checks(source, target, row):
                errors.append(key + ': ' + issue)
    if not rendered:
        return errors
    root = rendered.resolve()
    for asset in asset_rows:
        output = root / asset['source'].removeprefix('content/')
        require(output.is_file() and digest(output) == asset['sha256'],
                asset['source'] + ': rendered shared asset differs')
    documents = {}
    def document(route):
        path = root / route.strip('/') / 'index.html'
        require(path.is_file(), 'missing HTML ' + route)
        if path.is_file() and route not in documents:
            documents[route] = (german.Document(path), pages.Page(path.read_text()))
        return documents.get(route)
    weights = {german.route(s): int(generic.front_value(
        generic.split_front_matter(s.read_text())[0], 'weight')[0]) for s in srcs}
    expected_tree = next((n for n in german.flatten(json.loads(
        (root / 'navigation.json').read_text())['root']) if n['id'] == '/docs/etcd/'), None)
    require(expected_tree is not None, 'English navigation lacks etcd root')
    for lang, html_language in LANGUAGES.items():
        routes = {prefix(lang) + german.route(s) for s in srcs}
        bundle_path = root / prefix(lang).strip('/') / 'docs/etcd/llms-full.txt'
        require(bundle_path.is_file(), lang + ': missing LLMS bundle')
        bundle = bundle_path.read_text() if bundle_path.is_file() else ''
        indexes = list(root.glob('offline-search-index.' + lang + '.*.json'))
        require(len(indexes) == 1, lang + ': search index count differs')
        entries = json.loads(indexes[0].read_text()) if len(indexes) == 1 else []
        search_rows = [r for r in entries if r['ref'].startswith(prefix(lang) + '/docs/etcd/')]
        require(len(search_rows) == 99 and {r['ref'] for r in search_rows} == routes,
                lang + ': search page set differs')
        search = {r['ref']: r for r in search_rows}
        nav_path = root / prefix(lang).strip('/') / 'navigation.json'
        require(nav_path.is_file(), lang + ': missing navigation.json')
        nav = german.flatten(json.loads(nav_path.read_text())['root']) if nav_path.is_file() else []
        nav = [n for n in nav if n['id'].startswith('/docs/etcd/')]
        locale_tree = next((n for n in nav if n['id'] == '/docs/etcd/'), None)
        if expected_tree is not None and locale_tree is not None:
            try:
                require(weighted_tree(expected_tree, weights) == weighted_tree(locale_tree, weights),
                        lang + ': navigation hierarchy/weighted order differs')
            except (AssertionError, KeyError) as exc:
                errors.append(lang + ': invalid weighted navigation: ' + str(exc))
        require(len(nav) == 99 and {urlsplit(n['url']).path for n in nav} == routes,
                lang + ': navigation page set differs')
        for node in nav:
            require(node['url'] == 'https://pig.center' + prefix(lang) + node['id']
                    and node['markdown'] == node['url'] + 'index.md', lang + ': navigation destination differs')
        for source in srcs:
            target = source if lang == 'en' else source.with_suffix('.' + lang + '.md')
            route = prefix(lang) + german.route(source)
            docs = document(route)
            english = document(german.route(source))
            if not docs or not english:
                continue
            doc, content = docs
            require(doc.language == html_language, route + ': HTML language differs')
            require(doc.canonical == 'https://pig.center' + route and not doc.redirect,
                    route + ': canonical/fallback differs')
            require(len(doc.sidebar) == 99 and set(doc.sidebar) == routes, route + ': sidebar page set differs')
            require(doc.sidebar == [urlsplit(n['url']).path for n in nav], route + ': sidebar/navigation order differs')
            if route in doc.sidebar:
                pos = doc.sidebar.index(route)
                pager = {}
                if pos:
                    pager['prev'] = doc.sidebar[pos - 1]
                if pos + 1 < len(doc.sidebar):
                    pager['next'] = doc.sidebar[pos + 1]
                require(doc.pager == pager, route + ': pager differs from reading order')
            require(set(doc.switches) == {prefix(l) + german.route(source) for l in LANGUAGES if l != lang},
                    route + ': language switching page set differs')
            require(not any('/docs/etcd/' in x for x in doc.fallbacks), route + ': English fallback remains')
            require(content.headings == english[1].headings, route + ': English heading IDs differ')
            require(search.get(route, {}).get('title') == german.front_text(target, 'title'),
                    route + ': search title differs')
            _, heading_texts, _ = german.rendered_body(root / route.strip('/') / 'index.html')
            expected_headings = german.visible_text(' '.join(t for tag, t in heading_texts[1:] if tag in {'h2', 'h3', 'h4'}))
            require(german.visible_text(search.get(route, {}).get('headings', '')) == expected_headings,
                    route + ': search heading text differs')
            if lang != 'en':
                row = by_target.get(str(target.relative_to(PROJECT)), {})
                require(row.get('rendered_body_sha256') == german.rendered_body(root / route.strip('/') / 'index.html')[0],
                        route + ': rendered body changed since acceptance')
            markdown = root / route.strip('/') / 'index.md'
            require(markdown.is_file(), route + ': missing Markdown')
            if markdown.is_file():
                text = markdown.read_text().strip()
                require(generic.split_front_matter(target.read_text())[1].strip() in text,
                        route + ': Markdown body truncated/changed')
                entry = 'Source: https://pig.center' + route + 'index.md\n================\n\n' + text
                require(bundle.count(entry) == 1, route + ': LLMS body omitted/duplicated/changed')
            for alias in re.findall(r'/[A-Za-z0-9_./-]+', parity.front_matter_blocks(generic.split_front_matter(target.read_text())[0]).get('aliases', '')):
                alias_doc = document(prefix(lang) + alias)
                if alias_doc:
                    require(alias_doc[0].canonical == alias_doc[0].redirect == 'https://pig.center' + route,
                            route + ': legacy redirect differs')
        if lang != 'en':
            print_errors, _ = printing.check_print(root, srcs, PROJECT / 'content',
                                                  locale=lang, component='etcd', compare_metadata=True)
            errors.extend(lang + ': ' + e for e in print_errors)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rendered-dir', type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(RECORD.read_text()), args.rendered_dir)
    except (OSError, ValueError, KeyError) as exc:
        errors = [str(exc)]
    if errors:
        print('\n'.join(errors[:100]), file=sys.stderr)
        if len(errors) > 100:
            print(f'... {len(errors) - 100} more', file=sys.stderr)
        return 1
    print('Validated 495 current-English etcd translation pairs' +
          (' and 594 pages, search/navigation/aliases, Markdown/LLMS and five complete print bundles.' if args.rendered_dir else '.'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
