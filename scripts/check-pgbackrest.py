#!/usr/bin/env python3
"""Check all pgBackRest translations against current English and a production build.

Technical checks and exact review fingerprints are independent. They do not
claim that a structural check can establish translation quality by itself.
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
from urllib.parse import unquote, urlsplit, urlunsplit

PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / 'content'
ROOT = CONTENT / 'docs/pgbackrest'
AUDIT = PROJECT / 'data/translation-audits/pgbackrest.json'
PREFIX = '/docs/pgbackrest/'
LANGUAGES = {'en': 'en-US', 'zh': 'zh-CN', 'fr': 'fr-FR', 'ja': 'ja-JP', 'de': 'de-DE', 'ru': 'ru-RU'}
STABLE_TAG = 'release/2.59.3'
STABLE_COMMIT = '46cdca625a73403cad4774d97354a1fac1e91e51'
SECURITY_CHECK_SHA256 = '6589a3d180c75756c206691cf323d0dde8c0af8e10f8110a5da8f80f45b305cd'


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


P = load('pgbackrest_output_helpers', 'pgbouncer_validation.py')
G = load('pgbackrest_structure', 'check-german-parity.py')
J = load('pgbackrest_japanese', 'check-pgbackrest-ja.py')
L = load('pgbackrest_links', 'check-local-links.py')


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def route(source):
    relative = source.relative_to(CONTENT)
    path = relative.parent if source.stem == '_index' else relative.with_suffix('')
    return '/' + path.as_posix() + '/'


def normalize(value):
    parsed = urlsplit(value)
    if parsed.netloc and parsed.netloc not in {'doc.pg.center', 'www.doc.pg.center'}:
        return value
    path = re.sub(r'^/(?:zh|fr|ja|de|ru)(?=/(?:docs|search|attribution)(?:/|$))', '', parsed.path)
    return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))


def units(body):
    return [line for line in P.fenced_blocks(body)[1].splitlines() if line.strip()]


def links(body, source, *, chinese=False):
    result = []
    for value in J.S.link_targets(body, 'pgbackrest', normalize=False):
        value = normalize(P.canonical_target(value, source))
        parsed = urlsplit(value)
        if parsed.scheme in {'http', 'https'} and parsed.netloc and not parsed.path:
            value = urlunsplit((parsed.scheme, parsed.netloc, '/', parsed.query, parsed.fragment))
            parsed = urlsplit(value)
        # Chinese keeps its established localized anchors. Their semantic
        # destination is compared through the actual rendered heading map.
        if chinese and not parsed.netloc and (not parsed.path or parsed.path.startswith(PREFIX)):
            value = urlunsplit((*parsed[:4], ''))
        result.append(value)
    return Counter(result)


def fingerprint_errors(source, target, row):
    if row.get('source_sha256') != sha256(source) or row.get('translation_sha256') != sha256(target):
        return [f'{target.name}: review fingerprint is stale']
    return []


MONTHS = [
    'January janvier Januar января', 'February février Februar февраля',
    'March mars März марта', 'April avril April апреля', 'May mai Mai мая',
    'June juin Juni июня', 'July juillet Juli июля', 'August août August августа',
    'September septembre September сентября', 'October octobre Oktober октября',
    'November novembre November ноября', 'December décembre Dezember декабря',
]
WORDS = dict(zip('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen'.split(), range(17)))
WORDS.update({'single': 1, 'another': 1, 'once': 1, 'twice': 2, 'fifth': 5,
              'hexadecimal': 16, 'twenty': 20, 'hundred': 100, 'thousand': 1000,
              'million': 1000000, 'billion': 1000000000})


def numbers(text):
    text = re.sub(r'\{#[^}]+\}|<!--.*?-->', '', text)
    text = G.prose_without_markdown_destinations(text)
    text = re.sub(r'https?://[^\s<>)]*', '', text)
    for month, spellings in enumerate(MONTHS, 1):
        for spelling in set(spellings.split()):
            # Only date contexts: do not reinterpret the modal verb "may".
            text = re.sub(rf'\b{spelling}(?= \d{{1,2}}, \d{{4}})', str(month), text)
            text = re.sub(rf'(?<=\d)(?:er|\.)?\s+{spelling}(?=\s+\d{{4}})', ' ' + str(month), text)
    text = re.sub(r'(?<=\d)[,\u00a0\u202f](?=\d{3}(?:\D|$))', '', text)
    return Counter(re.findall(r'\d+(?:\.\d+)*', text))


def numeric_delta(english, target):
    en, tr = numbers(english), numbers(target)
    spelled = Counter(str(WORDS[w.lower()]) for w in re.findall(r'[A-Za-z]+', english) if w.lower() in WORDS)
    spelled['1'] += len(re.findall(r'\b(?:per (?:asynchronous run|run|execution|day|line)|each line|a day|last day|a potential benefit)\b', english, re.I))
    if english == 'Function/line coverage is complete with no exceptions.':
        spelled['100'] += 1  # "complete" is expressed as 100% in Chinese.
    return {'missing': dict(en - tr), 'extra': dict((tr - en) - spelled)}


def literal_missing(english, target):
    # Chinese adds code formatting and can replace a repeated identifier with
    # a pronoun. Protect the literal's presence in each aligned prose unit.
    translated = {literal.strip('`') for literal in J.INLINE.findall(target)}
    prose = J.INLINE.sub('', target)
    missing = set()
    for quoted in J.INLINE.findall(english):
        literal = quoted.strip('`')
        # Grouped commands retain their individual tokens. An option name may
        # be shown with its CLI prefix, e.g. `repo` option -> `--repo`.
        prefix = r'(?:--)?' if not literal.startswith('-') and re.search(re.escape(quoted) + r' option\b', english) else ''
        token = prefix + re.escape(literal)
        if (literal not in translated
                and not any(re.search(r'(?<![A-Za-z0-9_./-])' + token + r'(?![A-Za-z0-9_./-])', code) for code in translated)
                and not re.search(r'(?<![A-Za-z0-9_-])' + token + r'(?![A-Za-z0-9_-])', prose)):
            missing.add(literal)
    return sorted(missing)


def technical_errors(source, target, row):
    sf, sb = P.split_front_matter(source.read_text())
    tf, tb = P.split_front_matter(target.read_text())
    language = target.name.split('.')[-2]
    errors = []
    for label, before, after in (
        ('shared metadata', J.metadata(sf), J.metadata(tf)),
        ('code/config/output', P.fenced_blocks(sb)[0], P.fenced_blocks(tb)[0]),
        ('quoted code/config/output', P.blockquoted_fenced_blocks(sb), P.blockquoted_fenced_blocks(tb)),
        ('heading structure', P.headings(sb), P.headings(tb)),
        ('list structure', G.list_signature(sb), G.list_signature(tb)),
        ('table structure', G.table_signature(sb), G.table_signature(tb)),
        ('link/image/reference destinations', links(sb, source, chinese=language == 'zh'), links(tb, source, chinese=language == 'zh')),
        ('HTML/shortcode structure', [normalize(x) for x in J.markup(sb)], [normalize(x) for x in J.markup(tb)]),
        ('shortcodes', re.findall(r'\{\{[<%].*?[>%]\}\}', sb), re.findall(r'\{\{[<%].*?[>%]\}\}', tb)),
    ):
        if before != after:
            errors.append(label + ' differs')
    eu, tu = units(sb), units(tb)
    if len(eu) != len(tu):
        errors.append(f'prose unit coverage differs: {len(eu)} / {len(tu)}')
    exceptions = {e['unit']: e for e in row.get('reviewed_variants', [])}
    used = set()
    for number, (en, tr) in enumerate(zip(eu, tu), 1):
        delta = numeric_delta(en, tr)
        missing = literal_missing(en, tr)
        if delta['missing'] or delta['extra'] or missing:
            observed = {'numbers': delta, 'literals': missing}
            exception = exceptions.get(number, {})
            if exception.get('difference') != observed or not exception.get('reason'):
                errors.append(f'prose unit {number}: unreviewed technical difference {observed}')
            else:
                used.add(number)
        if re.search(r'__PGSQL_|⟦P\d+⟧|\b(?:TODO|TBD|FIXME|TRANSLATE_ME)\b', tr) and tr != en:
            errors.append(f'prose unit {number}: unresolved placeholder')
    if used != set(exceptions):
        errors.append('obsolete technical-difference exception')
    for literal in J.ENGLISH_LITERALS:
        if sb.count(literal) != tb.count(literal):
            errors.append('original diagnostic changed: ' + literal)
    if source.name == 'metric.md':
        en_cells = [x.split('|')[1:-1] for x in eu if x.startswith('|')][2:]
        tr_cells = [x.split('|')[1:-1] for x in tu if x.startswith('|')][2:]
        if [[v.strip() for v in r] for r in en_cells[:-1]] != [[v.strip() for v in r] for r in tr_cells[:-1]]:
            errors.append('metric directory/numeric table changed')
    if language != 'zh' and any(not anchor for _, anchor in J.headings(tb)):
        errors.append('missing explicit English heading anchor')
    if re.search(r'\]\(/docs/pgbackrest/', P.fenced_blocks(tb)[1]):
        errors.append('component link still points to English')
    return [f'{target.relative_to(PROJECT)}: {e}' for e in errors]


def source_errors(audit):
    sources = sorted(p for p in ROOT.rglob('*.md') if P.is_english(p))
    expected = {s.with_suffix(f'.{lang}.md').relative_to(PROJECT).as_posix(): s
                for s in sources for lang in LANGUAGES if lang != 'en'}
    rows = audit.get('pages', [])
    errors = []
    if (audit.get('source', {}).get('tag') != STABLE_TAG
            or audit.get('source', {}).get('commit') != STABLE_COMMIT):
        errors.append('review must identify the verified stable release tag and commit')
    security = (ROOT / 'news.md').read_text().split('## pgBackRest 2.59.3 Released')[0]
    code = re.search(r'```bash\n(.*?)\n```', security, re.S)
    if not code or hashlib.sha256(code[1].encode()).hexdigest() != SECURITY_CHECK_SHA256:
        errors.append('security advisory check differs from the stable-tag script')
    for name in ('user-guide', 'user-guide-rhel'):
        for language in LANGUAGES:
            path = ROOT / (name + ('' if language == 'en' else '.' + language) + '.md')
            if '2.59.2' in path.read_text() or 'Output suppressed for testing' in path.read_text():
                errors.append(f'{path.name}: stale or suppressed release example')
    if len(sources) != 29 or Counter(r.get('translation') for r in rows) != Counter(expected.keys()):
        errors.append('review record must cover all 145 current-source translation pairs exactly once')
    if set(ROOT.rglob('*.md')) != set(sources) | {PROJECT / p for p in expected}:
        errors.append('missing or orphan translated pages')
    for row in rows:
        source = expected.get(row.get('translation'))
        if source is None:
            continue
        target = PROJECT / row['translation']
        if not target.is_file():
            errors.append(f'missing {target}')
            continue
        if row.get('source') != source.relative_to(PROJECT).as_posix():
            errors.append(f'{target.name}: wrong review source')
        errors.extend(fingerprint_errors(source, target, row))
        if not row.get('review_scope'):
            errors.append(f'{target.name}: review scope is not recorded')
        errors.extend(technical_errors(source, target, row))
    for language in LANGUAGES:
        path = ROOT / ('_index.md' if language == 'en' else f'_index.{language}.md')
        front, _ = P.split_front_matter(path.read_text())
        if '2.59.3' not in (P.front_text(front, 'title') or ''):
            errors.append(f'{path.name}: incorrect documentation version')
        if re.findall(r'(?m)^\s*upstream_ref:\s*(\S+)', front) != ['v2.59.3', 'v2.59.3']:
            errors.append(f'{path.name}: upstream/cascade version mismatch')
        attribution = PROJECT / ('content/attribution' + ('' if language == 'en' else '.' + language) + '.md')
        row = next((line for line in attribution.read_text().splitlines() if line.startswith('|') and '/docs/pgbackrest/' in line), '')
        if 'v2.59.3' not in row or 'v2.59.2' in row or 'v2.59.1' in row:
            errors.append(f'{attribution.name}: stale attribution version')
    registry = (PROJECT / 'data/upstreams.yaml').read_text().split('\npgbackrest:\n', 1)[-1]
    registry = re.split(r'\n\S', registry, maxsplit=1)[0]
    if not re.search(r'(?m)^  ref: v2\.59\.3$', registry):
        errors.append('upstream registry version mismatch')
    if json.loads((PROJECT / 'data/translation-sources.json').read_text()).get('pgbackrest', {}).get('languages'):
        errors.append('pgBackRest still uses an obsolete source pin')
    return errors, sources


def collection_nodes(build, language):
    payload = json.loads((build / ('' if language == 'en' else language) / 'navigation.json').read_text())
    result = []
    def walk(node):
        if node.get('id', '').startswith(PREFIX): result.append(node)
        for child in node.get('children', []): walk(child)
    walk(payload['root'])
    return result


def rendered_errors(build, sources):
    errors, reports = [], {}
    def require(condition, message):
        if not condition: errors.append(message)
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
        home = J.rendered(build / local.lstrip('/') / 'index.html')
        require(len(home.index_sources) == 1, language + ': referenced search index')
        if len(home.index_sources) != 1: continue
        rows = json.loads((build / home.index_sources[0].lstrip('/')).read_text())
        search = {r['ref']: r for r in rows}
        require(Counter(r['ref'] for r in rows if r['ref'].startswith(local + PREFIX)) == Counter(local + url for url in ids), language + ': search coverage/duplicates')
        pages, docs = [], {}
        for node in nodes:
            url = local + node['id']; source = by_route[node['id']]
            target = source if language == 'en' else source.with_suffix(f'.{language}.md')
            front, body = P.split_front_matter(target.read_text())
            page = build / url.lstrip('/') / 'index.html'; pages.append(page)
            doc = P.RenderedContent(page); docs[node['id']] = doc; en = english[node['id']]
            require(doc.canonical == ['https://doc.pg.center' + url], url + ': canonical')
            require(doc.html_languages == [locale], url + ': HTML language')
            require(([h for h, _ in doc.headings] == [h for h, _ in en.headings]) if language == 'zh' else doc.headings == en.headings, url + ': headings/anchors')
            require(doc.code == en.code, url + ': rendered code/output')
            require(doc.sidebar == [local + href for href in en.sidebar], url + ': sidebar order/locale')
            require(doc.pager == [(direction, local + href) for direction, href in en.pager], url + ': pager order/locale')
            for other, other_locale in LANGUAGES.items():
                alternate = ('' if other == 'en' else '/' + other) + node['id']
                require(doc.alternates.get(other_locale) == 'https://doc.pg.center' + alternate, url + ': alternate ' + other)
                if other != language: require(alternate in doc.languages, url + ': switch ' + other)
            markdown = (build / url.lstrip('/') / 'index.md').read_text()
            require(body.strip() in markdown, url + ': incomplete Markdown body')
            for field in ('title', 'description'):
                require(' '.join(search.get(url, {}).get(field, '').split()) == ' '.join((P.front_text(front, field) or '').split()), url + ': search ' + field)
            if node['id'] == PREFIX + 'configuration/':
                for parameter in ('repo-retention-full', 'archive-push-queue-max', 'repo-s3-key'):
                    require(parameter in search.get(url, {}).get('headings', ''), url + ': searchable parameter ' + parameter)
            require(node['url'] == 'https://doc.pg.center' + url and node['markdown'] == node['url'] + 'index.md', url + ': navigation output URL')
            for alias in P.front_aliases(front):
                redirected = P.RenderedContent(build / (local + alias).lstrip('/') / 'index.html')
                require(redirected.canonical == doc.canonical and redirected.refresh == doc.canonical, url + ': alias ' + alias)
        if language == 'zh':
            heading_maps = {url: {tr[1]: en[1] for en, tr in zip(english[url].headings, docs[url].headings)} for url in ids}
            for source in sources:
                _, sb = P.split_front_matter(source.read_text())
                _, tb = P.split_front_matter(source.with_suffix('.zh.md').read_text())
                translated = Counter()
                for value, count in links(tb, source).items():
                    parsed = urlsplit(value)
                    if not parsed.netloc and parsed.fragment:
                        page_route = parsed.path or route(source)
                        if page_route in heading_maps:
                            anchor = unquote(parsed.fragment)
                            mapped = heading_maps[page_route].get(anchor, anchor)
                            value = urlunsplit((*parsed[:4], mapped))
                    translated[value] += count
                require(links(sb, source) == translated, route(source) + ': Chinese link points to a different source section')
        llms = P.llms_entries((build / (local + PREFIX).lstrip('/') / 'llms-full.txt').read_text())
        expected = [('https://doc.pg.center' + local + n['id'] + 'index.md', (build / (local + n['id']).lstrip('/') / 'index.md').read_text().strip()) for n in nodes]
        require(llms == expected, language + ': complete LLMS bodies/order')
        printing = build / local.lstrip('/') / '_print/docs/pgbackrest/index.html'; pages.append(printing)
        sections = P.content_sections(P.read_document(printing))
        expected_order = [None if source == ROOT / '_index.md' else 'pg-' + hashlib.md5((source if language == 'en' else source.with_suffix(f'.{language}.md')).relative_to(CONTENT).as_posix().encode()).hexdigest() for source in ordered]
        actual_order = [title.attrs.get('id') if (title := P.heading(section)) else None for section in sections]
        require(actual_order == expected_order, language + ': print chapter order')
        blocks = 0
        for source, section in zip(ordered, sections):
            normal = P.content_sections(P.read_document(build / (local + route(source)).lstrip('/') / 'index.html'))
            require(len(normal) == 1, route(source) + ': normal content section count')
            if len(normal) != 1: continue
            expected_blocks = P.body_blocks(normal[0]); blocks += len(expected_blocks)
            require(expected_blocks == P.body_blocks(section, print_root=source == ROOT / '_index.md'), local + route(source) + ': complete print body')
            require(P.content_metadata(normal[0]) == P.content_metadata(section, print_title=source != ROOT / '_index.md'), local + route(source) + ': print headings/metadata')
        reports[language] = {'pages': len(nodes), 'print_blocks': blocks}
        cache = {}
        for page in pages:
            for attribute, url in L.load_document(page).links:
                destination, fragment = L.resolve_target(build, page, url)
                if destination is None: continue
                require(destination.is_relative_to(build) and destination.exists(), f'{page.relative_to(build)}: missing/escaping {attribute}={url}')
                if destination.exists() and fragment and destination.suffix == '.html' and 'third_party' not in destination.parts:
                    if destination not in cache: cache[destination] = L.load_document(destination)
                    anchors = cache[destination].anchors
                    require(fragment in anchors or ('_print' in destination.parts and any(a.endswith('--' + fragment) for a in anchors)), f'{page.relative_to(build)}: missing fragment {url}')
    return errors, reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rendered-dir', type=Path)
    parser.add_argument('--report', type=Path, help='write generated evidence outside Git')
    args = parser.parse_args()
    audit = json.loads(AUDIT.read_text())
    errors, sources = source_errors(audit)
    outputs = {}
    if args.rendered_dir:
        failures, outputs = rendered_errors(args.rendered_dir.resolve(), sources)
        errors.extend(failures)
    if args.report: args.report.write_text(json.dumps({'pairs': len(sources) * 5, 'outputs': outputs, 'errors': errors}, ensure_ascii=False, indent=2) + '\n')
    if errors:
        print('pgBackRest publication checks failed:\n- ' + '\n- '.join(errors), file=sys.stderr)
        return 1
    print('Validated pgBackRest 2.59.3: 145 current-source translation pairs and exact review fingerprints' + (', 174 rendered pages, navigation/search/aliases, code, links/assets and complete Markdown/print/LLMS bodies.' if args.rendered_dir else '.'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
