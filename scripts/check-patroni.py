#!/usr/bin/env python3
"""Check all five Patroni translations against current English and a build.

Technical checks are independent of the recorded review fingerprints. Neither
the fingerprints nor structural parity alone establish prose quality.
"""
from __future__ import annotations

import argparse
from collections import Counter
from html.parser import HTMLParser
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit, urlunsplit

import pgbouncer_validation as P

PROJECT = Path(__file__).resolve().parent.parent
ROOT = PROJECT / 'content/docs/patroni'
AUDIT = PROJECT / 'data/translation-audits/patroni.json'
PREFIX = '/docs/patroni/'
LANGUAGES = {'en': 'en-US', 'zh': 'zh-CN', 'fr': 'fr-FR', 'ja': 'ja-JP', 'de': 'de-DE', 'ru': 'ru-RU'}


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


G = load('patroni_structure', 'check-german-parity.py')
L = load('patroni_links', 'check-local-links.py')


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def route(source):
    rel = source.relative_to(PROJECT / 'content')
    return '/' + (rel.parent if source.stem == '_index' else rel.with_suffix('')).as_posix() + '/'


def normalize(value):
    parsed = urlsplit(value)
    if parsed.netloc and parsed.netloc not in {'doc.pg.center', 'www.doc.pg.center'}:
        return value
    path = re.sub(r'^/(?:zh|fr|ja|de|ru)(?=/(?:docs|patroni)(?:/|$))', '', parsed.path)
    return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))


def numeric_delta(english, target):
    ef, eb = G.split_front_matter(english)
    tf, tb = G.split_front_matter(target)
    en, tr = G.number_facts(ef, eb), G.number_facts(tf, tb)
    return {'missing': dict(en - tr), 'added': dict(tr - en)}


def command_anchor_errors(body):
    """A correct ID in the wrong command section still breaks a deep link."""
    _, prose = G.parse_fenced_blocks(body)
    errors, command, subsection = [], None, 0
    for match in re.finditer(r'^(#{3,4}) (.+)$', prose, re.M):
        level, title = match.groups()
        if level == '###':
            command_match = re.match(r'patronictl ([^\s{]+)', title)
            if not command_match:
                command = None
                continue
            command, subsection = command_match[1].replace('-', '_'), 0
            expected = 'patronictl_' + command
        elif command:
            if subsection >= 4:
                errors.append('unexpected patronictl command subsection')
                continue
            expected = 'patronictl_' + command + '_' + ('synopsis', 'description', 'parameters', 'examples')[subsection]
            subsection += 1
        else:
            continue
        before = prose[:match.start()]
        anchor = re.search(r'<a id="([^"]+)"></a>\s*$', before)
        if not anchor or anchor[1] != expected:
            errors.append('misplaced command anchor: ' + expected)
    return errors


def duplicate_json_keys(body):
    errors = []
    for block in G.parse_fenced_blocks(body)[0]:
        start = block.find('{')
        if start < 0:
            continue
        duplicates = []
        def object_pairs(pairs):
            seen = set()
            for key, _ in pairs:
                if key in seen:
                    duplicates.append(key)
                seen.add(key)
            return dict(pairs)
        try:
            json.JSONDecoder(object_pairs_hook=object_pairs).raw_decode(block[start:])
        except ValueError:
            continue  # A YAML, shell or Python fence is not a JSON document.
        errors.extend('duplicate JSON key: ' + key for key in duplicates)
    return errors


def literal_missing(source_prose, target_prose):
    # Formatting and repeated explanatory labels may differ. Copyable fenced
    # examples are checked byte-for-byte; every inline value stays present.
    flat = target_prose.replace('`', '').replace('**', '')
    missing = []
    for quoted in sorted(set(G.INLINE_CODE_RE.findall(source_prose))):
        value = quoted.strip('`').rstrip('.')
        if value and not re.search(r'(?<![A-Za-z0-9_])' + re.escape(value) + r'(?![A-Za-z0-9_])', flat):
            missing.append(quoted)
    return missing


def technical_errors(english, target, language, numeric_variant=None, *, command_page=False):
    errors = []
    ef, eb = G.split_front_matter(english)
    tf, tb = G.split_front_matter(target)
    en_fences, ep = G.parse_fenced_blocks(eb)
    tr_fences, tp = G.parse_fenced_blocks(tb)
    def require(condition, message):
        if not condition:
            errors.append(message)
    en_meta, tr_meta = G.front_matter_blocks(ef), G.front_matter_blocks(tf)
    require(en_meta.keys() == tr_meta.keys(), 'front matter key set')
    for key in en_meta.keys() & tr_meta.keys() - G.TRANSLATABLE_FRONT_MATTER:
        require(en_meta[key] == tr_meta[key], 'non-translatable metadata: ' + key)
    require(en_fences == tr_fences, 'code/config/output fences')
    require(P.blockquoted_fenced_blocks(eb) == P.blockquoted_fenced_blocks(tb), 'quoted code fences')
    require(G.normalized_html_tags(ep) == G.normalized_html_tags(tp), 'HTML tags or explicit anchors')
    require(G.COMMENT_RE.findall(ep) == G.COMMENT_RE.findall(tp), 'HTML comments')
    require(G.SHORTCODE_RE.findall(ep) == G.SHORTCODE_RE.findall(tp), 'shortcodes')
    require(Counter(G.FOOTNOTE_RE.findall(ep)) == Counter(G.FOOTNOTE_RE.findall(tp)), 'footnote references')
    require(G.FOOTNOTE_DEFINITION_RE.findall(ep) == G.FOOTNOTE_DEFINITION_RE.findall(tp), 'footnote definitions')
    require(G.list_signature(eb) == G.list_signature(tb), 'list structure')
    require(G.table_signature(eb) == G.table_signature(tb), 'table structure')
    require(G.thematic_break_signature(eb) == G.thematic_break_signature(tb), 'thematic breaks')
    require(re.findall(r'\[!([A-Z]+)\]', ep) == re.findall(r'\[!([A-Z]+)\]', tp), 'admonition types/order')
    require(Counter(normalize(x) for x in G.link_targets(eb)) == Counter(normalize(x) for x in G.link_targets(tb)), 'link/asset targets')
    for value in G.link_targets(tb):
        parsed = urlsplit(value)
        if parsed.netloc and parsed.netloc not in {'doc.pg.center', 'www.doc.pg.center'}:
            continue
        path = parsed.path
        if path.startswith('/docs/') and not G.is_shared_asset(value):
            errors.append('document link lacks locale: ' + value)
        if re.match(r'^/(?:zh|fr|ja|de|ru)/', path) and G.is_shared_asset(value):
            errors.append('shared asset incorrectly localized: ' + value)
    eh, th = G.heading_rows(eb), G.heading_rows(tb)
    require([h.level for h in eh] == [h.level for h in th], 'heading levels')
    require(G.inferred_heading_ids(eh) == [h.anchor for h in th], 'English heading IDs')
    missing = literal_missing(ep, tp)
    require(not missing, 'inline literals missing: ' + repr(missing))
    actual = numeric_delta(english, target)
    expected = numeric_variant.get('delta') if numeric_variant else {'missing': {}, 'added': {}}
    require(actual == expected, 'unreviewed numeric delta: ' + repr(actual))
    if numeric_variant:
        require(bool(numeric_variant.get('reason')), 'numeric variant needs a review reason')
    errors.extend(duplicate_json_keys(eb))
    errors.extend(duplicate_json_keys(tb))
    if command_page:
        errors.extend(command_anchor_errors(eb))
        errors.extend(command_anchor_errors(tb))
        for body in (eb, tb):
            history = re.search(r'^### patronictl history\b(.*?)(?=^### |\Z)', body, re.M | re.S)
            require(not history or '--force' not in history[1], 'unsupported history --force option')
    require(not re.search(r'\b(?:SIHGUP|DENTIFY_SYSTEM)\b|`--s`', english + target), 'known source literal typo')
    require(not re.search('[\u200b\ufeff]', target), 'invisible characters')
    return errors


def release_block_signatures(texts):
    """Use Hugo's Markdown parser to bind each block to its list ancestors.

    Line wrapping, translated/repeated titles and marker widths are irrelevant;
    Goldmark decides whether an explanation actually belongs to a list item.
    This isolated rendering has no theme, modules or network dependencies.
    """
    class Shape(HTMLParser):
        def __init__(self):
            super().__init__()
            self.signature, self.lists, self.items = [], [], []
            self.list_number = 0

        def handle_starttag(self, tag, attrs):
            if tag in {'ul', 'ol'}:
                self.list_number += 1
                self.lists.append([self.list_number, 0])
            if tag == 'li':
                self.lists[-1][1] += 1
                self.items.append(tuple(self.lists[-1]))
            if tag in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li',
                       'p', 'blockquote', 'pre', 'table', 'thead', 'tbody',
                       'tr', 'th', 'td', 'hr'}:
                self.signature.append((tag, 'open', tuple(self.items)))

        def handle_endtag(self, tag):
            if tag in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li',
                       'p', 'blockquote', 'pre', 'table', 'thead', 'tbody',
                       'tr', 'th', 'td'}:
                self.signature.append((tag, 'close', tuple(self.items)))
            if tag == 'li':
                self.items.pop()
            if tag in {'ul', 'ol'}:
                self.lists.pop()

    with tempfile.TemporaryDirectory(prefix='patroni-release-ownership-') as temp:
        root = Path(temp)
        (root / 'content').mkdir()
        (root / 'layouts/_default').mkdir(parents=True)
        (root / 'hugo.toml').write_text('baseURL = "https://example.invalid/"\ndisableKinds = ["taxonomy", "term", "RSS", "sitemap"]\n[markup.goldmark.renderer]\nunsafe = true\n')
        (root / 'layouts/_default/single.html').write_text('{{ .RenderString (dict "display" "block") .RawContent }}')
        for name, text in texts.items():
            body = G.split_front_matter(text)[1] if text.startswith('---\n') else text
            (root / 'content' / (name + '.md')).write_text('---\ntitle: Release ownership\n---\n' + body)
        subprocess.run(['hugo', '--source', str(root), '--destination', str(root / 'public'),
                        '--cacheDir', str(root / 'cache')], check=True,
                       capture_output=True, text=True)
        signatures = {}
        for name in texts:
            shape = Shape()
            shape.feed((root / 'public' / name / 'index.html').read_text())
            signatures[name] = shape.signature
        return signatures


def release_ownership_errors(texts):
    try:
        signatures = release_block_signatures(texts)
    except (OSError, subprocess.CalledProcessError, IndexError) as error:
        detail = (error.stdout + error.stderr).strip() if isinstance(error, subprocess.CalledProcessError) else str(error)
        return ['release explanation ownership rendering failed: ' + detail]
    return [language + ': release explanation/list ownership differs from English'
            for language, signature in signatures.items()
            if language != 'en' and signature != signatures['en']]


def source_errors(audit):
    errors = []
    sources = sorted(p for p in ROOT.rglob('*.md') if G.is_english_source(p))
    rows = audit.get('pages', {})
    expected = {p.relative_to(ROOT).as_posix() for p in sources}
    if len(sources) != 24 or set(rows) != expected:
        errors.append('review must cover exactly the 24 current English pages')
    if audit.get('semantic_review', {}).get('status') != 'complete':
        errors.append('complete semantic review is required for all 120 pairs')
    for source in sources:
        row = rows.get(source.relative_to(ROOT).as_posix(), {})
        if row.get('source_sha256') != sha256(source):
            errors.append(source.name + ': source review fingerprint is stale')
        translations = row.get('translations', {})
        if set(translations) != set(LANGUAGES) - {'en'}:
            errors.append(source.name + ': review must cover all five languages')
        for language in set(LANGUAGES) - {'en'}:
            target = source.with_suffix('.' + language + '.md')
            if not target.is_file():
                errors.append(str(target) + ': missing translation')
                continue
            review = translations.get(language, {})
            if review.get('semantic_review') != 'complete':
                errors.append(target.name + ': complete semantic review is missing')
            if review.get('translation_sha256') != sha256(target):
                errors.append(target.name + ': translation review fingerprint is stale')
            for failure in technical_errors(source.read_text(), target.read_text(), language, review.get('numeric_variant'), command_page=source.name == 'patronictl.md'):
                errors.append(str(target.relative_to(PROJECT)) + ': ' + failure)
    release = ROOT / 'releases.md'
    texts = {language: (release if language == 'en' else release.with_suffix('.' + language + '.md')).read_text()
             for language in LANGUAGES if (release if language == 'en' else release.with_suffix('.' + language + '.md')).is_file()}
    if 'en' in texts:
        errors.extend(release_ownership_errors(texts))
    return errors, sources


def collection_nodes(build, language):
    payload = json.loads((build / ('' if language == 'en' else language) / 'navigation.json').read_text())
    result = []
    def walk(node):
        if node.get('id', '').startswith(PREFIX):
            result.append(node)
        for child in node.get('children', []):
            walk(child)
    walk(payload['root'])
    return result


def rendered_errors(build, sources):
    build = build.resolve()
    errors, reports = [], {}
    def require(condition, message):
        if not condition:
            errors.append(message)
    en_nodes = collection_nodes(build, 'en')
    ids = [n['id'] for n in en_nodes]
    by_route = {route(s): s for s in sources}
    require(Counter(ids) == Counter(by_route.keys()), 'English navigation coverage/duplicates')
    ordered = [by_route[url] for url in ids]
    english = {url: P.RenderedContent(build / url.lstrip('/') / 'index.html') for url in ids}
    for language, locale in LANGUAGES.items():
        local = '' if language == 'en' else '/' + language
        nodes = collection_nodes(build, language)
        require([n['id'] for n in nodes] == ids, language + ': navigation order/coverage')
        home = P.read_document(build / local.lstrip('/') / 'index.html')
        index_urls = [node.attrs['data-td-index-src'] for node in home.root.walk() if node.attrs.get('data-td-index-src')]
        require(len(index_urls) == 1, language + ': search index')
        if len(index_urls) != 1:
            continue
        search_rows = json.loads((build / index_urls[0].lstrip('/')).read_text())
        search = {r['ref']: r for r in search_rows}
        require(Counter(r['ref'] for r in search_rows if r['ref'].startswith(local + PREFIX)) == Counter(local + url for url in ids), language + ': search coverage/duplicates')
        pages = []
        for node in nodes:
            url = local + node['id']
            source = by_route[node['id']]
            target = source if language == 'en' else source.with_suffix('.' + language + '.md')
            front, body = P.split_front_matter(target.read_text())
            page = build / url.lstrip('/') / 'index.html'
            pages.append(page)
            doc, en = P.RenderedContent(page), english[node['id']]
            require('td-page-meta__translation' not in page.read_text(), url + ': reader-facing translation-policy annotation')
            require(doc.canonical == ['https://doc.pg.center' + url], url + ': canonical')
            require(doc.html_languages == [locale], url + ': HTML language')
            require(doc.headings == en.headings, url + ': headings/anchors')
            require(doc.code == en.code, url + ': complete rendered code/output')
            require(doc.sidebar == [local + href for href in en.sidebar], url + ': sidebar order/locale')
            require(doc.pager == [(direction, local + href) for direction, href in en.pager], url + ': pager order/locale')
            for other, other_locale in LANGUAGES.items():
                alternate = ('' if other == 'en' else '/' + other) + node['id']
                require(doc.alternates.get(other_locale) == 'https://doc.pg.center' + alternate, url + ': alternate ' + other)
                if other != language:
                    require(alternate in doc.languages, url + ': language switch ' + other)
            markdown = (build / url.lstrip('/') / 'index.md').read_text()
            require(body.strip() in markdown, url + ': complete Markdown body')
            for field in ('title', 'description'):
                require(' '.join(search.get(url, {}).get(field, '').split()) == ' '.join((P.front_text(front, field) or '').split()), url + ': search ' + field)
            require(node['url'] == 'https://doc.pg.center' + url and node['markdown'] == node['url'] + 'index.md', url + ': navigation URLs')
            for alias in P.front_aliases(front):
                redirected = P.RenderedContent(build / (local + alias).lstrip('/') / 'index.html')
                require(redirected.canonical == doc.canonical and redirected.refresh == doc.canonical, url + ': alias ' + alias)
        expected_llms = [('https://doc.pg.center' + local + n['id'] + 'index.md', (build / (local + n['id']).lstrip('/') / 'index.md').read_text().strip()) for n in nodes]
        require(P.llms_entries((build / (local + PREFIX).lstrip('/') / 'llms-full.txt').read_text()) == expected_llms, language + ': complete LLMS bodies/order')
        printing = build / local.lstrip('/') / '_print/docs/patroni/index.html'
        pages.append(printing)
        sections = P.content_sections(P.read_document(printing))
        expected_order = [None if source == ROOT / '_index.md' else 'pg-' + hashlib.md5((source if language == 'en' else source.with_suffix('.' + language + '.md')).relative_to(PROJECT / 'content').as_posix().encode()).hexdigest() for source in ordered]
        actual_order = [title.attrs.get('id') if (title := P.heading(section)) else None for section in sections]
        require(actual_order == expected_order, language + ': print chapter order')
        blocks = 0
        for source, section in zip(ordered, sections):
            normal = P.content_sections(P.read_document(build / (local + route(source)).lstrip('/') / 'index.html'))
            require(len(normal) == 1, route(source) + ': content section count')
            if len(normal) != 1:
                continue
            expected_blocks = P.body_blocks(normal[0])
            blocks += len(expected_blocks)
            require(expected_blocks == P.body_blocks(section, print_root=source == ROOT / '_index.md'), local + route(source) + ': complete print body')
            require(P.content_metadata(normal[0]) == P.content_metadata(section, print_title=source != ROOT / '_index.md'), local + route(source) + ': print headings/metadata')
        reports[language] = {'pages': len(nodes), 'print_blocks': blocks}
        cache = {}
        for page in pages:
            for attribute, url in L.load_document(page).links:
                destination, fragment = L.resolve_target(build, page, url)
                if destination is None:
                    continue
                require(destination.is_relative_to(build) and destination.exists(), f'{page.relative_to(build)}: missing/escaping {attribute}={url}')
                if destination.exists() and fragment and destination.suffix == '.html':
                    if destination not in cache:
                        cache[destination] = L.load_document(destination)
                    anchors = cache[destination].anchors
                    require(fragment in anchors or ('_print' in destination.parts and any(a.endswith('--' + fragment) for a in anchors)), f'{page.relative_to(build)}: missing fragment {url}')
    return errors, reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rendered-dir', type=Path)
    args = parser.parse_args()
    audit = json.loads(AUDIT.read_text())
    failures, sources = source_errors(audit)
    if args.rendered_dir and not failures:
        rendered, _ = rendered_errors(args.rendered_dir.resolve(), sources)
        failures.extend(rendered)
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1
    print('Validated Patroni: 120 current-source translation pairs, technical content and review fingerprints' + (', 144 rendered pages, anchors/navigation/search/aliases and complete Markdown/print/LLMS bodies.' if args.rendered_dir else '.'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
