#!/usr/bin/env python3
"""Check every German pgBackRest source and its production-rendered outputs."""

import argparse
from collections import Counter
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

PROJECT = Path(__file__).resolve().parent.parent
ROOT = PROJECT / 'content/docs/pgbackrest'
def helper(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


parity = helper('german_parity', 'check-german-parity.py')
links = helper('local_links', 'check-local-links.py')
# The shared print comparator accepts a locale; its Japanese entry point also
# has regression tests for missing/reordered prose, tables, lists and code.
printing = helper('pgbackrest_print', 'check-pgbackrest-ja-print.py')
shared = helper('pgbackrest_shared_review', 'check-pgbackrest.py')


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.headings, self.links, self.canonical, self.language, self.refresh = [], [], [], [], []
        self.index_sources = []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('data-td-index-src'): self.index_sources.append(attrs['data-td-index-src'])
        if re.fullmatch('h[1-6]', tag) and attrs.get('id'):
            self.headings.append((int(tag[1]), attrs['id']))
        if tag == 'a': self.links.append(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical.append(attrs.get('href'))
        if tag == 'html': self.language.append(attrs.get('lang'))
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            self.refresh.append(attrs.get('content', '').partition('url=')[2])


def route(source):
    relative = source.relative_to(PROJECT / 'content')
    path = relative.parent if source.stem == '_index' else relative.with_suffix('')
    return '/' + path.as_posix() + '/'


def nodes(node):
    yield node
    for child in node.get('children', []): yield from nodes(child)


def front_text(front, key):
    raw = parity.front_matter_blocks(front).get(key, '').partition(':')[2].strip()
    if raw.startswith('"'): return json.loads(raw)
    if raw.startswith("'") and raw.endswith("'"): return raw[1:-1].replace("''", "'")
    return raw


def heading_signature(section, namespace=''):
    title = printing.heading(section)
    result = []
    for node in section.walk():
        if not re.fullmatch('h[1-6]', node.tag): continue
        text = re.sub(r'\s+', ' ', node.text()).strip()
        anchor = node.attrs.get('id', '')
        if node is title:
            anchor = ''  # Print chapter IDs and numbering are generated.
            if namespace: text = re.sub(r'^\d+(?:\.\d+)* - ', '', text)
        elif namespace:
            anchor = anchor.removeprefix(namespace + '--')
        result.append((node.tag, anchor, text))
    return result


def print_structure(build, sources, ordered_routes):
    sections = printing.content_sections(printing.read_document(build / 'de/_print/docs/pgbackrest/index.html'))
    section_ids = [title.attrs.get('id') if (title := printing.heading(section)) else None for section in sections]
    indexed = dict(zip(section_ids, sections))
    expected_ids, errors = {}, []
    for source in sources:
        url = route(source)
        relative = parity.german_target(source).relative_to(PROJECT / 'content').as_posix()
        namespace = 'pg-' + hashlib.md5(relative.encode()).hexdigest()
        expected_ids[url] = None if source == ROOT / '_index.md' else namespace
        printed = indexed.get(expected_ids[url])
        normal = printing.content_sections(printing.read_document(build / 'de' / url.lstrip('/') / 'index.html'))
        # Missing/duplicate sections are reported by the shared body comparator.
        if printed is not None and len(normal) == 1:
            if heading_signature(normal[0]) != heading_signature(printed, namespace):
                errors.append(url + ': print heading order, text, levels or IDs differ')
    if section_ids != [expected_ids.get(url, 'missing:' + url) for url in ordered_routes]:
        errors.append('print chapter order differs from navigation.json')
    return errors


def search_metadata(entries, expected):
    indexed = {entry['ref']: entry for entry in entries}
    errors = []
    for url, metadata in expected.items():
        entry = indexed.get(url, {})
        for key in ('title', 'description'):
            if entry.get(key) != metadata[key]:
                errors.append(url + ': search ' + key + ' differs from current German metadata')
        for key in ('excerpt', 'headings'):
            if key == 'headings' and not metadata['has_headings']: continue
            value = entry.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(url + ': search ' + key + ' is empty')
    return errors


def component_links(build, sources):
    """Reuse the site's resolver for every component link, asset and fragment."""
    build = build.resolve()
    pages = [build / 'de' / route(p).lstrip('/') / 'index.html' for p in sources]
    pages.append(build / 'de/_print/docs/pgbackrest/index.html')
    cache, errors = {}, []
    def document(path):
        if path not in cache: cache[path] = links.load_document(path)
        return cache[path]
    for page in pages:
        for attribute, url in document(page).links:
            target, fragment = links.resolve_target(build, page, url)
            if target is None: continue
            if not target.is_relative_to(build):
                errors.append(f'{page.relative_to(build)}: site-root escape {url}')
                continue
            if links.LEGACY_COMPONENT_ROUTE.match(target.relative_to(build).as_posix()):
                errors.append(f'{page.relative_to(build)}: legacy component route {url}')
            if not target.exists():
                errors.append(f'{page.relative_to(build)}: missing {attribute} target {url}')
            elif fragment and target.suffix == '.html' and 'third_party' not in target.parts:
                anchors = document(target).anchors
                print_anchor = '_print' in target.parts and any(a.endswith('--' + fragment) for a in anchors)
                if fragment not in anchors and not print_anchor:
                    errors.append(f'{page.relative_to(build)}: missing fragment {url}')
    return errors


def check(build):
    sources = sorted(p for p in ROOT.rglob('*.md') if parity.is_english_source(p))
    expected = {parity.german_target(p) for p in sources}
    actual = set(ROOT.rglob('*.de.md'))
    errors = [f'missing German page: {p}' for p in sorted(expected - actual)]
    errors += [f'orphan German page: {p}' for p in sorted(actual - expected)]
    print_ids = Counter()
    search_expected = {}
    review = json.loads(shared.AUDIT.read_text())
    reviewed = {row['translation']: row for row in review['pages']}
    llms = (build / 'de/docs/pgbackrest/llms-full.txt').read_text(encoding='utf-8')
    for source in sources:
        target = parity.german_target(source)
        if target not in actual: continue
        url = route(source)
        # The shared gate checks aligned units and exact review fingerprints.
        # Generic uppercase-word heuristics mistake translated NOTE/WARNING
        # labels and localized thousands separators for technical changes.
        row = reviewed.get(target.relative_to(PROJECT).as_posix(), {})
        errors.extend(shared.fingerprint_errors(source, target, row))
        errors.extend(shared.technical_errors(source, target, row))
        en = Page(build / url.lstrip('/') / 'index.html')
        de = Page(build / 'de' / url.lstrip('/') / 'index.html')
        if en.headings != de.headings: errors.append(url + ': rendered heading order/IDs changed')
        if de.canonical != ['https://doc.pg.center/de' + url]: errors.append(url + ': wrong canonical')
        if de.language != ['de-DE']: errors.append(url + ': wrong HTML language')
        old = Page(build / 'de' / url.removeprefix('/docs/') / 'index.html')
        if old.canonical != de.canonical or old.refresh != de.canonical:
            errors.append(url + ': wrong legacy alias redirect')
        for label, select in [
            ('sidebar', lambda a: 'td-shell-tree__link' in a.get('class', '')),
            ('pager', lambda a: 'data-td-pager-prev' in a or 'data-td-pager-next' in a),
        ]:
            en_links = [urlsplit(a.get('href', '')).path for a in en.links if select(a)]
            de_links = [urlsplit(a.get('href', '')).path for a in de.links if select(a)]
            if de_links != ['/de' + value for value in en_links]:
                errors.append(url + ': ' + label + ' order/locale differs')
        switches = [urlsplit(a.get('href', '')).path for a in de.links if a.get('hreflang') == 'en-US']
        if not switches or any(value != url for value in switches):
            errors.append(url + ': English language switch does not target same page')
        if not any(urlsplit(a.get('href', '')).path == '/de' + url for a in en.links if a.get('hreflang') == 'de-DE'):
            errors.append(url + ': English page lacks matching German switch')
        front, body = parity.split_front_matter(target.read_text(encoding='utf-8'))
        body = body.strip()
        search_expected['/de' + url] = {
            'title': front_text(front, 'title'), 'description': front_text(front, 'description'),
            'has_headings': bool(parity.heading_rows(body)),
        }
        markdown = (build / 'de' / url.lstrip('/') / 'index.md').read_text(encoding='utf-8')
        if body not in markdown: errors.append(url + ': incomplete Markdown body')
        if 'Source: https://doc.pg.center/de' + url + 'index.md' not in llms or body not in llms:
            errors.append(url + ': incomplete LLMS body/source')
        print_ids.update(h.anchor for h in parity.heading_rows(body))
    printed = Page(build / 'de/_print/docs/pgbackrest/index.html')
    actual_ids = Counter(anchor.split('--', 1)[1] for _, anchor in printed.headings if '--' in anchor)
    if print_ids != actual_ids: errors.append('print bundle heading coverage differs')
    print_errors, print_pages = printing.check_print(build, sources, PROJECT / 'content', locale='de')
    errors.extend(print_errors)
    errors.extend(component_links(build, sources))
    nav = []
    for prefix in ['', 'de']:
        payload = json.loads((build / prefix / 'navigation.json').read_text(encoding='utf-8'))
        nav.append(next(n for n in nodes(payload['root']) if n['id'] == '/docs/pgbackrest/'))
    en_nodes, de_nodes = list(nodes(nav[0])), list(nodes(nav[1]))
    if [n['id'] for n in en_nodes] != [n['id'] for n in de_nodes] or len(de_nodes) != len(sources):
        errors.append('navigation.json order/coverage differs')
    errors.extend(print_structure(build, sources, [node['id'] for node in de_nodes]))
    for node in de_nodes:
        if node['url'] != 'https://doc.pg.center/de' + node['id'] or node['markdown'] != node['url'] + 'index.md':
            errors.append('navigation.json wrong locale/output: ' + node['id'])
    home = Page(build / 'de/index.html')
    if len(home.index_sources) != 1:
        errors.append('homepage must reference exactly one German search index')
    else:
        entries = json.loads((build / home.index_sources[0].lstrip('/')).read_text(encoding='utf-8'))
        indexed = [entry for entry in entries if '/docs/pgbackrest/' in entry.get('ref', '')]
        if Counter(entry['ref'] for entry in indexed) != Counter('/de' + route(p) for p in sources):
            errors.append('search index page coverage or German routes differ')
        errors.extend(search_metadata(indexed, search_expected))
    home_links = [a for a in home.links if '/docs/pgbackrest/' in a.get('href', '')]
    if not home_links: errors.append('homepage has no pgBackRest entrance')
    for anchor in home_links:
        if anchor.get('data-fallback-language') or not urlsplit(anchor['href']).path.startswith('/de/docs/pgbackrest/'):
            errors.append('homepage still falls back for pgBackRest')
    return {'component': 'pgbackrest', 'language': 'de', 'source': 'current English',
            'expected': len(sources), 'paired': len(expected & actual),
            'missing': len(expected - actual), 'orphans': len(actual - expected),
            'print_body_blocks': sum(p['expected_blocks'] for p in print_pages), 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rendered-dir', required=True, type=Path)
    parser.add_argument('--report', type=Path, help='optional JSON report; keep generated reports outside Git')
    args = parser.parse_args()
    try:
        result = check(args.rendered_dir)
    except (OSError, ValueError, KeyError, StopIteration) as exc:
        print(f'German pgBackRest rendered validation failed: {exc}', file=sys.stderr)
        return 1
    if args.report: args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for error in result['errors']: print(error, file=sys.stderr)
    if result['errors']: return 1
    print(f"Validated {result['paired']}/{result['expected']} German pgBackRest pages: current source, rendered anchors, routes, aliases, sidebar/pager order, language switches, search index, links/assets, Markdown, complete print bodies ({result['print_body_blocks']} blocks), LLMS, navigation and homepage.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
