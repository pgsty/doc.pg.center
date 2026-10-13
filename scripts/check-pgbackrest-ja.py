#!/usr/bin/env python3
"""Validate all Japanese pgBackRest pages against current English and a build.

No pinned-source or partial mode: every English page must have a translation.
This structural/technical gate complements, but cannot replace, prose review.
"""
from __future__ import annotations
import argparse
from collections import Counter
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import sys

PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / 'content'
ROOT = CONTENT / 'docs/pgbackrest'
spec = importlib.util.spec_from_file_location('structure', PROJECT / 'scripts/check-component-translations.py')
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
spec = importlib.util.spec_from_file_location('print_check', PROJECT / 'scripts/check-pgbackrest-ja-print.py')
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
spec = importlib.util.spec_from_file_location('links', PROJECT / 'scripts/check-local-links.py')
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)
INLINE = re.compile(r'`+[^`\n]*`+')
JAPANESE = re.compile(r'[\u3040-\u30ff\u3400-\u9fff]')
FUNCTION_WORDS = set('a an the and or to of in for on with by from as is are be this that it its can will may should must not if when at into which their they them than has have had was were would'.split())
# Exact program messages appearing in explanatory paragraphs in faq.md.
ENGLISH_LITERALS = {
    'could not find WAL segment',
    'aborted backup of same type exists, will be cleaned to remove invalid files and resumed',
    "unable to find hostname 'my.backup.bucket.s3.amazonaws.com' in certificate common name or subject alternative names",
}
MONTHS = 'January February March April May June July August September October November December'.split()


def english_source(path):
    return path.suffix == '.md' and not re.search(r'\.[a-z]{2}(?:-[a-z0-9]+)?\.md$', path.name)


def local_target(source):
    return source.with_suffix('.ja.md')


def normalize_route(value):
    return re.sub(r'/ja/(?=(?:docs|search|attribution)(?:/|$))', '/', value)


def prose(body):
    return S.parse_fenced_blocks(body)[1]


def metadata(front):
    rows = []
    for line in front.splitlines():
        m = re.match(r'^(\s*)([A-Za-z_][\w]*):\s*(.*)$', line)
        if m and m[2] in {'title', 'linkTitle', 'description', 'categories'}:
            if m[3] in {'|', '>', '|-', '>-', '|+', '>+'}:
                raise ValueError('multiline translated metadata needs explicit parser support')
            line = f'{m[1]}{m[2]}: <translated>'
        rows.append(line)
    return '\n'.join(rows)


def headings(body):
    return [(len(m['marks']), m['anchor']) for line in prose(body).splitlines() if (m := S.HEADING_RE.match(line))]


def refs(body):
    return [m.groups() for line in prose(body).splitlines() if (m := S.REFERENCE_DEF_RE.match(line))]


def targets(body):
    values = S.link_targets(body, 'pgbackrest', normalize=False)
    values.extend(target for _, target in refs(body))
    return [normalize_route(x) for x in values]


def markup(body):
    return [re.sub(r'''\s+(alt|title|aria-label)=(["'])[^"']*\2''', r' \1=<translated>', normalize_route(tag)) for tag in S.HTML_TAG_RE.findall(prose(body))]


def number_facts(body):
    text = INLINE.sub('', prose(body))
    text = re.sub(r'\{#[^}]+\}|<!--.*?-->', '', text, flags=re.S)
    text = re.sub(r'\]\([^\n)]*\)', ']', text)
    text = re.sub(r'https?://\S+', '', text)
    for number, month in enumerate(MONTHS, 1):
        text = re.sub(rf'\b{month}(?= \d{{1,2}}, \d{{4}})', str(number), text)
    text = re.sub(r'(?<=\d),(?=\d{3}(?:\D|$))', '', text)
    return Counter(re.findall(r'\d+(?:\.\d+)*', text))


def numeric_errors(source, target):
    expected, actual = number_facts(source), number_facts(target)
    # Japanese may use digits for these explicitly written English counts.
    words = {'zero':0, 'one':1, 'single':1, 'another':1,
             'two':2, 'three':3, 'four':4, 'once':1, 'twice':2,
             'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10,
             'eleven':11, 'twelve':12, 'thirteen':13, 'fourteen':14,
             'fifteen':15, 'sixteen':16, 'hexadecimal':16, 'twenty':20,
             'hundred':100, 'thousand':1000, 'million':1000000, 'billion':1000000000}
    source_prose = INLINE.sub('', prose(source))
    spelled = Counter(str(words[w.lower()]) for w in re.findall(r'[A-Za-z]+', source_prose) if w.lower() in words)
    spelled['1'] += len(re.findall(r'\b(?:per (?:asynchronous run|run|execution|day|line)|each line)\b', source_prose))
    spelled['5'] += len(re.findall(r'\bfifth full backup\b', source_prose))
    # Reviewed article-based counts in the guides: once a day, last day or
    # more, and a potential benefit. These add no new numerical claim.
    spelled['1'] += len(re.findall(r'\b(?:a day|last day|a potential benefit)\b', source_prose, re.I))
    missing, extra = expected-actual, (actual-expected)-spelled
    return [f'numeric facts differ; missing={dict(missing)}, extra={dict(extra)}'] if missing or extra else []


def technical_facts(body):
    text = re.sub(r'\{#[^}]+\}', '', prose(body))
    text = re.sub(r'\]\([^\n)]*\)', ']', text)
    return Counter(re.findall(r'(?<![A-Za-z0-9_/-])--[a-z][a-z0-9-]*(?:=[A-Za-z0-9_./*-]+)?|(?<![A-Za-z0-9_:])/[A-Za-z_][A-Za-z0-9_./*-]+', text))


def english_residue(body):
    problems = []
    text = re.sub(r'<!--.*?-->', '', prose(body), flags=re.S)
    for number, raw in enumerate(text.splitlines(), 1):
        line = INLINE.sub('', raw)
        line = re.sub(r'\{#[^}]+\}|\{\{[<%].*?[>%]\}\}', '', line)
        line = re.sub(r'\]\([^\n)]*\)', ']', line)
        line = re.sub(r'https?://[^\s<>]+|</?[^>]+>', '', line)
        for literal in ENGLISH_LITERALS:
            line = line.replace(literal, '')
        words = re.findall(r'[A-Za-z]+', line)
        functions = sum(w.lower() in FUNCTION_WORDS for w in words)
        simple = line.strip(' #*:_-\t')
        if re.fullmatch(r'[A-Za-z]+(?:[ -][A-Za-z]+)*[.:]?', simple) and simple not in {'pgBackRest','PostgreSQL','FAQ','Azure Blob Storage Service','Google Cloud Storage','AWS Simple Storage Service','Secure File Transfer Protocol'}:
            problems.append((number, raw))
        elif (len(words) >= 4 and functions >= 2) or (not JAPANESE.search(line) and len(words) >= 5 and functions):
            problems.append((number, raw))
        elif re.search(r'\b(?:TODO|TBD|TRANSLATE_ME)\b|翻訳未完|翻訳予定', line):
            problems.append((number, raw))
    return problems


def compare_text(source_text, target_text, *, metrics=False):
    errors = []
    sf, sb = S.split_front_matter(source_text)
    tf, tb = S.split_front_matter(target_text)
    sp, tp = prose(sb), prose(tb)
    checks = [
        ('non-translatable metadata', metadata(sf), metadata(tf)),
        ('code/config/output blocks', S.parse_fenced_blocks(sb)[0], S.parse_fenced_blocks(tb)[0]),
        ('prose block count', len(re.split(r'\n\s*\n',sp.strip())), len(re.split(r'\n\s*\n',tp.strip()))),
        ('heading levels', [x[0] for x in headings(sb)], [x[0] for x in headings(tb)]),
        ('inline technical literals', Counter(INLINE.findall(sp)), Counter(INLINE.findall(tp))),
        ('bare options and paths', technical_facts(sb), technical_facts(tb)),
        ('table structure', S.table_signature(sb), S.table_signature(tb)),
        ('list structure', S.list_signature(sb), S.list_signature(tb)),
        ('blockquote structure', S.blockquote_signature(sb), S.blockquote_signature(tb)),
        ('HTML structure', markup(sb), markup(tb)),
        ('HTML comments', S.html_comments(sb), S.html_comments(tb)),
        ('shortcodes', re.findall(r'\{\{[%<].*?[>%]\}\}',sb), re.findall(r'\{\{[%<].*?[>%]\}\}',tb)),
        ('link/image/reference targets', Counter(targets(sb)), Counter(targets(tb))),
        ('reference identifiers', [x[0] for x in refs(sb)], [x[0] for x in refs(tb)]),
        ('footnotes', re.findall(r'\[\^[^]\n]+\]',sb), re.findall(r'\[\^[^]\n]+\]',tb)),
    ]
    if metrics:
        cells = lambda body: [line.split('|')[1].strip() for line in prose(body).splitlines() if line.startswith('|')][2:-1]
        checks.append(('metric directory names', cells(sb), cells(tb)))
    source_units=re.split(r'\n\s*\n',sp.strip())
    target_units=re.split(r'\n\s*\n',tp.strip())
    for index,(su,tu) in enumerate(zip(source_units,target_units),1):
        errors.extend(f'prose block {index}: {issue}' for issue in numeric_errors(su,tu))
        sl,tl=su.splitlines(),tu.splitlines()
        if len(sl)==len(tl) and any(re.match(r'^\s*(?:\||[-+*] )',line) for line in sl):
            for row,(sr,tr) in enumerate(zip(sl,tl),1):
                errors.extend(f'prose block {index}, row {row}: {issue}' for issue in numeric_errors(sr,tr))
        if Counter(INLINE.findall(su))!=Counter(INLINE.findall(tu)):
            errors.append(f'prose block {index}: inline technical literals differ')
        if Counter(targets(su))!=Counter(targets(tu)):
            errors.append(f'prose block {index}: link/image/reference targets differ')
    for name, expected, actual in checks:
        if expected != actual:
            detail = f'; missing={dict(expected-actual)}, extra={dict(actual-expected)}' if isinstance(expected,Counter) else ''
            errors.append(name+' differ'+detail)
    for literal in ENGLISH_LITERALS:
        if sb.count(literal)!=tb.count(literal): errors.append('program diagnostic changed: '+literal)
    literal_headings = {'OpenSSL 1.0'} & {m['title'] for line in sp.splitlines() if (m := S.HEADING_RE.match(line))}
    for line in tp.splitlines():
        if (m:=S.HEADING_RE.match(line)) and not JAPANESE.search(m['title']) and m['title'] not in literal_headings:
            errors.append('untranslated explanatory heading: '+m['title'])
    navigation_literals={'pgBackRest','FAQ'} | {p.stem for p in (ROOT/'command').glob('*.md') if english_source(p) and p.stem!='_index'}
    nav=re.search(r'^linkTitle:\s*(.+)$',tf,re.M)
    if nav and not JAPANESE.search(nav[1]):
        source_nav=re.search(r'^linkTitle:\s*(.+)$',sf,re.M)
        if nav[1].strip("\"'") not in navigation_literals or not source_nav or nav[1]!=source_nav[1]:
            errors.append('untranslated or changed linkTitle metadata')
    for sr,tr in zip(headings(sb),headings(tb)):
        if sr[1] and sr[1] != tr[1]:
            errors.append('explicit source anchor changed: '+sr[1])
        if not tr[1]:
            errors.append('Japanese heading lacks explicit English anchor')
    for key in ('title','description','categories'):
        match = re.search(rf'^{key}:\s*(.+)$',tf,re.M)
        if match and not JAPANESE.search(match[1]):
            errors.append(f'untranslated {key} metadata')
    localized_front = '\n'.join(line for line in tf.splitlines() if re.match(r'^(title|linkTitle|description|categories):', line))
    for line,value in english_residue(localized_front+'\n'+tb):
        errors.append(f'unreviewed explanatory English/placeholder near prose line {line}: {value}')
    for line in tp.splitlines():
        if re.search(r'\]\(/docs/pgbackrest/',line):
            errors.append('component link still uses English route: '+line)
    return errors


class Rendered(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.headings, self.ids, self.canonical, self.links, self.languages = [], [], [], [], []
        self.refresh = []
        self.index_sources = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'): self.ids.append(attrs['id'])
        if attrs.get('data-td-index-src'): self.index_sources.append(attrs['data-td-index-src'])
        if re.fullmatch('h[1-6]',tag) and attrs.get('id'): self.headings.append((int(tag[1]),attrs['id']))
        if tag=='link' and attrs.get('rel')=='canonical': self.canonical.append(attrs.get('href'))
        if tag=='a': self.links.append(attrs)
        if tag=='html': self.languages.append(attrs.get('lang'))
        if tag=='meta' and attrs.get('http-equiv','').lower()=='refresh': self.refresh.append(attrs.get('content','').partition('url=')[2])


def rendered(path):
    parsed = Rendered()
    parsed.feed(path.read_text())
    return parsed


def route(source):
    relative=source.relative_to(CONTENT)
    return '/'+(relative.parent if source.stem in {'index','_index'} else relative.with_suffix('')).as_posix().lower()+'/'


def navigation_errors(en, ja):
    errors=[]
    for a in ja.links:
        if ('td-shell-tree__link' in a.get('class','') or 'data-td-pager-prev' in a or 'data-td-pager-next' in a) and '/docs/pgbackrest/' in a.get('href',''):
            if not a.get('href','').startswith('/ja/docs/pgbackrest/') or 'data-fallback-language' in a:
                errors.append('sidebar/pager component link uses English fallback')
    for label, selector in [('sidebar',lambda a:'td-shell-tree__link' in a.get('class','')),('pager',lambda a:'data-td-pager-prev' in a or 'data-td-pager-next' in a)]:
        before=[normalize_route(a.get('href','')) for a in en.links if selector(a)]
        after=[normalize_route(a.get('href','')) for a in ja.links if selector(a)]
        if before!=after: errors.append(label+' order/routes differ from English')
    return errors


def compare_pair(source,target,build):
    errors=compare_text(source.read_text(),target.read_text(),metrics=source.name=='metric.md')
    url=route(source)
    en=rendered(build/url.lstrip('/')/'index.html')
    ja=rendered(build/'ja'/url.lstrip('/')/'index.html')
    if len(en.headings)!=len(headings(S.split_front_matter(source.read_text())[1])): errors.append('English rendered heading count differs from source')
    if en.headings!=ja.headings: errors.append('rendered heading IDs or order differ')
    if ja.canonical!=['https://pig.center/ja'+url]: errors.append('incorrect Japanese canonical')
    if ja.languages!=['ja-JP']: errors.append('incorrect rendered html language')
    old=rendered(build/'ja'/url.removeprefix('/docs/')/'index.html')
    if old.canonical!=ja.canonical or old.refresh!=ja.canonical: errors.append('incorrect legacy alias redirect')
    errors.extend(navigation_errors(en,ja))
    if not any(a.get('hreflang')=='en-US' and a.get('href')==url for a in ja.links): errors.append('English language switch missing')
    if not any(a.get('hreflang')=='ja-JP' and a.get('href')=='/ja'+url for a in en.links): errors.append('Japanese language switch missing')
    md=build/'ja'/url.lstrip('/')/'index.md'
    if not md.is_file() or not md.stat().st_size: errors.append('missing Markdown output')
    elif S.split_front_matter(target.read_text())[1].strip() not in md.read_text(): errors.append('Markdown output does not contain complete current Japanese body')
    return errors



def component_links(build, sources):
    """Resolve every local link/asset/fragment in this component and its print view."""
    build=build.resolve()
    pages=[build/'ja'/route(p).lstrip('/')/'index.html' for p in sources]
    pages.append(build/'ja/_print/docs/pgbackrest/index.html')
    cache={}
    errors=[]
    def document(path):
        if path not in cache: cache[path]=L.load_document(path)
        return cache[path]
    for page in pages:
        for attr,url in document(page).links:
            target,fragment=L.resolve_target(build,page,url)
            if target is None: continue
            if not target.is_relative_to(build):
                errors.append(f'{page.relative_to(build)}: site-root escape {url}')
                continue
            if L.LEGACY_COMPONENT_ROUTE.match(target.relative_to(build).as_posix()):
                errors.append(f'{page.relative_to(build)}: legacy component route {url}')
            if not target.exists():
                errors.append(f'{page.relative_to(build)}: missing {attr} target {url}')
            elif fragment and target.suffix=='.html' and 'third_party' not in target.parts:
                anchors=document(target).anchors
                print_anchor='_print' in target.parts and any(a.endswith('--'+fragment) for a in anchors)
                if fragment not in anchors and not print_anchor:
                    errors.append(f'{page.relative_to(build)}: missing fragment {url}')
    return errors


def component_outputs(build, sources):
    errors=[]
    def nodes(item):
        yield item
        for child in item.get('children',[]): yield from nodes(child)
    en=json.loads((build/'navigation.json').read_text())
    ja=json.loads((build/'ja/navigation.json').read_text())
    eroot=next(n for n in nodes(en['root']) if n['id']=='/docs/pgbackrest/')
    jroot=next(n for n in nodes(ja['root']) if n['id']=='/docs/pgbackrest/')
    if [n['id'] for n in nodes(eroot)]!=[n['id'] for n in nodes(jroot)]: errors.append('navigation.json component order/coverage differs')
    if len(list(nodes(jroot)))!=len(sources): errors.append('navigation.json does not include every page')
    for node in nodes(jroot):
        if node['url']!='https://pig.center/ja'+node['id']: errors.append('navigation.json contains incorrect locale URL: '+node['id'])
    llms=(build/'ja/docs/pgbackrest/llms-full.txt').read_text()
    printed=rendered(build/'ja/_print/docs/pgbackrest/index.html')
    expected_ids=Counter()
    for source in sources:
        body=S.split_front_matter(local_target(source).read_text())[1]
        if 'Source: https://pig.center/ja'+route(source)+'index.md' not in llms: errors.append('LLMS source missing: '+route(source))
        if body.strip() not in llms: errors.append('LLMS body incomplete: '+route(source))
        expected_ids.update(anchor for _,anchor in headings(body))
    actual_ids=Counter(anchor.split('--',1)[1] for _,anchor in printed.headings if '--' in anchor)
    if expected_ids!=actual_ids: errors.append('print bundle heading coverage differs')
    print_errors, _ = P.check_print(build, sources, CONTENT)
    errors.extend(print_errors)
    errors.extend(component_links(build, sources))
    home=rendered(build/'ja/index.html')
    if len(home.index_sources)!=1:
        errors.append('homepage must reference exactly one Japanese search index')
    else:
        entries=json.loads((build/home.index_sources[0].lstrip('/')).read_text())
        expected={'/ja'+route(source) for source in sources}
        indexed=[entry for entry in entries if '/docs/pgbackrest/' in entry.get('ref','')]
        if Counter(e['ref'] for e in indexed)!=Counter(expected): errors.append('search index page coverage or Japanese routes differ')
        for entry in indexed:
            if not JAPANESE.search(entry.get('title','')): errors.append('untranslated search title: '+entry['ref'])

    for a in home.links:
        if '/docs/pgbackrest/' in a.get('href','') and a.get('data-fallback-language'): errors.append('homepage pgBackRest link still falls back to English')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rendered-dir',required=True,type=Path,help='production Hugo output with both English and Japanese')
    parser.add_argument('--report',type=Path,help='write JSON results outside the repository')
    args=parser.parse_args()
    sources=sorted(p for p in ROOT.rglob('*.md') if english_source(p))
    expected={local_target(p) for p in sources};actual=set(ROOT.rglob('*.ja.md'))
    errors=[f'missing Japanese page: {p.relative_to(PROJECT)}' for p in sorted(expected-actual)]
    errors += [f'orphan Japanese page: {p.relative_to(PROJECT)}' for p in sorted(actual-expected)]
    pages=[]
    for source in sources:
        target=local_target(source)
        if not target.exists():continue
        try:issues=compare_pair(source,target,args.rendered_dir)
        except (OSError,ValueError) as exc:issues=[str(exc)]
        pages.append({'page':str(source.relative_to(ROOT)),'errors':issues})
        errors.extend(f'{target.relative_to(PROJECT)}: {issue}' for issue in issues)
    if expected==actual:
        try:errors.extend(component_outputs(args.rendered_dir,sources))
        except (OSError,ValueError,KeyError,StopIteration) as exc:errors.append('component outputs: '+str(exc))
    result={'component':'pgbackrest','source':'current English','expected':len(expected),'paired':len(expected&actual),'missing':len(expected-actual),'orphans':len(actual-expected),'errors':errors,'pages':pages}
    if args.report:args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    if errors:
        for error in errors:print(error,file=sys.stderr)
        print(f'Japanese pgBackRest parity FAILED: {len(errors)} errors',file=sys.stderr)
        return 1
    print(f'Validated {len(pages)}/{len(sources)} Japanese pgBackRest pages against CURRENT English: source structure, protected content, prose residue, rendered anchors, canonical routes, legacy aliases, navigation, language switches, search index, links/assets, Markdown, complete print bodies and LLMS.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
