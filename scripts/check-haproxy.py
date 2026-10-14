#!/usr/bin/env python3
"""Check all six HAProxy editions and complete production outputs.

Fingerprints bind the publication review to the delivered text; automated
checks do not substitute for semantic review. Unregistered code changes fail.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit
import pgbouncer_validation as v
from translation_fences import load_manifest, validate_fences

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'content'
DOCS = CONTENT / 'docs/haproxy'
LOCALES = {'en':'en-US','zh':'zh-CN','fr':'fr-FR','ja':'ja-JP','de':'de-DE','ru':'ru-RU'}

def helper(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

component = helper('haproxy_component', 'check-component-translations.py')
render = helper('haproxy_render', 'check-haproxy-de-rendered.py')
links = helper('haproxy_links', 'check-local-links.py')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def unfenced_sample_types(document):
    """Read literal return types in sample signatures left outside code fences."""
    _, body = v.split_front_matter(document)
    _, prose = component.parse_fenced_blocks(body)
    # Some declarations place a deprecated alias on the same line. Parse
    # consecutive declarations, without treating prose labels or references
    # inside sentences as signatures or crossing paragraph breaks.
    signature = re.compile(r'([a-z][a-z0-9_.]*(?:\([^\n)]*\))?)[ \t]*:[ \t]*([^\W\d]\w*)')
    result = []
    for line in prose.splitlines():
        rest = line.lstrip(' \t')
        while match := signature.match(rest):
            result.append(match.groups())
            rest = rest[match.end():].lstrip(' \t')
    return result

def route(source, language):
    prefix = '' if language == 'en' else '/' + language
    return prefix + '/docs/haproxy/' + ('' if source.name == '_index.md' else source.stem + '/')

def source_witness(directory):
    """Render current .Content independently of normal/print page templates.

    Both production outputs can omit the same paragraph and still agree. This
    temporary Hugo output renders only source content, with the same Markdown
    settings and render hooks. No generated files enter the checkout.
    """
    content = directory/'content'
    layouts = directory/'layouts'
    shutil.copytree(CONTENT, content)
    shutil.copytree(ROOT/'layouts', layouts)
    for path in (content/'docs/haproxy').glob('_index*.md'):
        path.write_text(re.sub(r'^outputs:.*$', 'outputs: [SOURCEHTML]', path.read_text(), flags=re.M))
    for kind in ('home', 'page', 'section'):
        (layouts/f'{kind}.sourcehtml.html').write_text('<section class="td-content">{{ .Content }}</section>')
    config = directory/'config.json'
    config.write_text(json.dumps({
        'contentDir':str(content), 'layoutDir':str(layouts),
        'outputs':{kind:['SOURCEHTML'] for kind in ('home','page','section')},
        'outputFormats':{'SOURCEHTML':{'mediaType':'text/html','baseName':'__source','isHTML':True,'permalinkable':False}},
        'disableAliases':True, 'disableKinds':['taxonomy','term','RSS','sitemap','robotsTXT'],
        'build':{'writeStats':False},
    }))
    output = directory/'public'
    environment = dict(os.environ, HUGO_RESOURCEDIR=str(directory/'resources'))
    result = subprocess.run(['hugo','--source',str(ROOT),'--config',str(ROOT/'hugo.yaml')+','+str(config),
        '--destination',str(output),'--cacheDir',str(directory/'cache'),'--minify','--panicOnWarning'],
        cwd=ROOT, env=environment, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError('Independent source rendering failed:\n'+result.stdout+result.stderr)
    return output

def visible_headings(section):
    result=[]
    def visit(node):
        if node.tag=='header' or node.classes & v.SKIP_CLASSES:return
        if node is not section and 'td-content' in node.classes:return
        if re.fullmatch(r'h[2-6]',node.tag) and not re.fullmatch(r'pg-[0-9a-f]{32}',node.attrs.get('id','')):
            result.append((node.tag,re.sub(r'\s+',' ',node.text()).strip()))
        for child in node.children:
            if isinstance(child,v.Node):visit(child)
    visit(section)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rendered-dir', type=Path)
    parser.add_argument('--report', type=Path, help='optional detailed report outside Git')
    args = parser.parse_args()
    errors, pairs = [], []
    def require(ok, message):
        if not ok: errors.append(message)
    sources = sorted(p for p in DOCS.glob('*.md') if v.is_english(p))
    published = [DOCS/'_index.md'] + sorted((p for p in sources if not p.name.startswith('_')), key=lambda p:int(v.front_text(v.split_front_matter(p.read_text())[0], 'weight')))
    require(len(sources)==38 and len(published)==35, 'HAProxy must contain 35 pages and 3 dividers')
    ledger_path = ROOT/'data/translation-audits/haproxy.json'
    ledger = json.loads(ledger_path.read_text()) if ledger_path.is_file() else {}
    snapshot = json.loads((ROOT/'sources/haproxy/SNAPSHOT.json').read_text())
    require(ledger.get('edition')==snapshot['documentation_version'] and ledger.get('upstream_commit')==snapshot['documentation_commit'], 'publication ledger must use the pinned current English snapshot')
    require(ledger.get('stable_release')==snapshot['stable_release'] and ledger.get('stable_tag')==snapshot['stable_tag'], 'publication ledger stable release/tag differs from the pinned snapshot')
    require(ledger.get('upstream_ref')==snapshot['documentation_ref'], 'publication ledger documentation ref differs from the pinned snapshot')
    require((ROOT/'sources/haproxy/upstream/VERSION').read_text().strip()==snapshot['stable_release'], 'pinned upstream release identity differs from snapshot metadata')
    require(snapshot['stable_tag']=='v'+snapshot['stable_release'], 'snapshot stable tag must identify the actual stable release')
    expected_inputs={'intro.txt','configuration.txt','management.txt','LICENSE','GPL-2.0','VERSION','VERDATE'}
    require(len(snapshot['files'])==7 and {entry['file'] for entry in snapshot['files']}==expected_inputs, 'snapshot must include all seven original input files exactly once')
    for entry in snapshot['files']:
        require(digest(ROOT/'sources/haproxy/upstream'/entry['file'])==entry['sha256'], f'pinned upstream checksum changed: {entry["file"]}')
    for name in ('LICENSE','GPL-2.0'):
        require((ROOT/'sources/haproxy/upstream'/name).read_bytes()==(ROOT/'static/third_party/haproxy'/name).read_bytes(), f'published HAProxy license changed: {name}')
    records = ledger.get('pairs', [])
    indexed = {(p.get('source'),p.get('language')):p for p in records}
    expected = {(str(p.relative_to(ROOT)),language) for p in sources for language in LOCALES if language!='en'}
    require(len(records)==len(indexed) and set(indexed)==expected, 'publication ledger must contain all 190 translation pairs exactly once')
    for source in sources:
        source_fences = v.fenced_blocks(v.split_front_matter(source.read_text())[1])[0]
        expected_types = Counter((name, kind) for name, kind in unfenced_sample_types(source.read_text()) if kind in {'integer','boolean','bool','string','binary','ip'})
        typed_names = {name for name, _ in expected_types}
        required = {r['index'] for r in load_manifest(source,'de').get('fences',[])}
        for language in list(LOCALES)[1:]:
            target = source.with_suffix('.'+language+'.md')
            require(target.is_file(), f'missing translation: {target}')
            if not target.is_file(): continue
            actual_types = Counter((name, kind) for name, kind in unfenced_sample_types(target.read_text()) if name in typed_names)
            require(actual_types==expected_types, f'{target.name}: unfenced sample return type signatures differ from English')
            record = indexed.get((str(source.relative_to(ROOT)),language),{})
            require(record.get('documentation_version')==snapshot['documentation_version'], f'{target.name}: publication pair documentation version differs from the pinned snapshot')
            require(record.get('source_sha256')==digest(source) and record.get('target_sha256')==digest(target), f'{target.name}: publication review fingerprints stale')
            require(record.get('target')==str(target.relative_to(ROOT)), f'{target.name}: publication target path mismatch')
            require(bool(record.get('review_scope','').strip()), f'{target.name}: missing publication review scope')
            target_fences = v.fenced_blocks(v.split_front_matter(target.read_text())[1])[0]
            if language!='ja':validate_fences(source,source_fences,target_fences,errors,language=language)
            if language in ('zh','fr'):
                component.validate_pair(source,target,errors,language=language)
                actual = {r['index'] for r in load_manifest(source,language).get('fences',[])}
                require(required<=actual, f'{target.name}: missing explanatory-fence translations {sorted(required-actual)}')
            pairs.append({'source':str(source.relative_to(ROOT)),'language':language,'source_sha256':digest(source),'target_sha256':digest(target)})
    # Keep the existing locale-specific numeric, literal and semantic-review
    # checks mandatory, including Japanese's separately classified explanations.
    locale_gates = []
    for filename, flags in (
        ('check-german-parity.py', ['--component','haproxy','--current-source']),
        ('check-russian-parity.py', ['--component','haproxy','--current-source','--strict']),
        ('check-haproxy-ja.py', ['--require-review']),
    ):
        result = subprocess.run([sys.executable, str(ROOT/'scripts'/filename), *flags], cwd=ROOT, text=True, capture_output=True)
        locale_gates.append({'check':filename,'exit_code':result.returncode,'output':result.stdout+result.stderr})
        require(result.returncode==0, f'{filename}: locale-specific review gate failed\n{result.stdout}{result.stderr}')
    if args.rendered_dir:
        witness_temp = tempfile.TemporaryDirectory(prefix='doc-pg-center-haproxy-witness-')
        witness = source_witness(Path(witness_temp.name))
        build=args.rendered_dir.resolve(); page_cache={}; link_cache={}; search_cache={}
        def page(path):
            if path not in page_cache:page_cache[path]=render.Page(path.read_text())
            return page_cache[path]
        def link_document(path):
            if path not in link_cache:link_cache[path]=links.load_document(path)
            return link_cache[path]
        def check_links(path):
            for attr,url in link_document(path).links:
                destination,fragment=links.resolve_target(build,path,url)
                if destination is None:continue
                require(destination.is_relative_to(build) and destination.exists(),f'{path}: broken {attr} {url}')
                if fragment and destination.is_file() and destination.suffix=='.html':
                    ids=link_document(destination).anchors
                    require(fragment in ids or ('_print' in destination.parts and any(x.endswith('--'+fragment) for x in ids)),f'{path}: broken fragment {url}')
        def walk(node):
            yield node
            for child in node.get('children',[]):yield from walk(child)
        for language,html_language in LOCALES.items():
            prefix=Path() if language=='en' else Path(language)
            routes=[route(p,language) for p in published]
            navigation=json.loads((build/prefix/'navigation.json').read_text())
            actual=[urlsplit(n['url']).path for n in walk(navigation['root']) if n.get('id','').startswith('/docs/haproxy/')]
            require(actual==routes,f'{language}: complete ordered navigation')
            llms=v.llms_entries((build/prefix/'docs/haproxy/llms-full.txt').read_text())
            require([urlsplit(url).path for url,_ in llms]==[r+'index.md' for r in routes],f'{language}: complete ordered LLMS entries')
            print_path=build/prefix/'_print/docs/haproxy/index.html'
            print_sections=v.content_sections(v.read_document(print_path));print_index={};print_roots=[]
            for section in print_sections:
                title=v.heading(section);key=title.attrs.get('id') if title else None
                if key:require(key not in print_index,f'{language}: duplicate print section');print_index[key]=section
                else:print_roots.append(section)
            require(len(print_sections)==35 and len(print_roots)==1,f'{language}: complete print section count')
            for index,source in enumerate(published):
                url=routes[index];output=build/url.lstrip('/')/'index.html'
                require(output.is_file(),f'{language}: missing page {url}')
                if not output.is_file():continue
                current=page(output);english=page(build/route(source,'en').lstrip('/')/'index.html')
                require(current.language==[html_language] and current.canonical==['https://doc.pg.center'+url],f'{url}: HTML language/canonical')
                require(current.sidebar==routes,f'{url}: sidebar order')
                require(current.previous+current.next==[routes[x] for x in (index-1,index+1) if 0<=x<35],f'{url}: pager order')
                require(current.headings==english.headings,f'{url}: stable English heading anchors')
                require(not any(a.get('data-fallback-language') and '/docs/haproxy/' in a.get('href','') for a in current.links),f'{url}: unexpected English fallback')
                for other in LOCALES:
                    if other==language:continue
                    require(any(urlsplit(a.get('href','')).path==route(source,other) for a in current.links if 'td-language-selector__item' in a.get('class','').split()),f'{url}: same-page {other} language switch')
                target=source if language=='en' else source.with_suffix('.'+language+'.md')
                front,body=v.split_front_matter(target.read_text());markdown=(output.parent/'index.md').read_text()
                require(markdown.count(body.strip())==1,f'{url}: complete Markdown body')
                if index<len(llms):require(llms[index][1].count(body.strip())==1,f'{url}: complete LLMS body')
                key='pg-'+hashlib.md5(target.relative_to(CONTENT).as_posix().encode()).hexdigest()
                printed=print_roots[0] if index==0 and print_roots else print_index.get(key);normal=v.content_sections(v.read_document(output))
                require(printed is not None and len(normal)==1 and v.body_blocks(normal[0])==v.body_blocks(printed,print_root=index==0),f'{url}: complete ordered print body')
                title=v.front_text(front,'title')
                if len(normal)==1:
                    titles=[re.sub(r'\s+',' ',node.text()).strip() for node in normal[0].walk() if node.tag=='h1']
                    require(titles==[title],f'{url}: localized HTML page title differs from front matter')
                if printed is not None:
                    print_titles=[re.sub(r'\s+',' ',node.text()).strip() for node in printed.walk() if node.tag=='h1']
                    if index:print_titles=[re.sub(r'^\d+(?:\.\d+)*\s+-\s+','',value) for value in print_titles]
                    require(print_titles==[title],f'{url}: localized print page title differs from front matter')
                expected_path=witness/url.lstrip('/')/'__source.html'
                require(expected_path.is_file(), f'{url}: missing independent source render')
                if expected_path.is_file():
                    expected_content=v.content_sections(v.read_document(expected_path))
                    require(len(expected_content)==1 and len(normal)==1 and v.body_blocks(expected_content[0])==v.body_blocks(normal[0]), f'{url}: HTML body differs from independently rendered source')
                    if len(expected_content)==len(normal)==1:
                        require(visible_headings(expected_content[0])==visible_headings(normal[0]), f'{url}: HTML heading text differs from source')
                        if printed is not None:require(visible_headings(expected_content[0])==visible_headings(printed), f'{url}: print heading text differs from source')
                # Preserve each literal fence, including whitespace, in order.
                cursor=0
                for fence in v.fenced_blocks(body)[0]:
                    literal=''.join(fence.splitlines(keepends=True)[1:-1]).rstrip('\n')
                    match=next((i for i in range(cursor,len(current.pre)) if current.pre[i].rstrip('\n')==literal),None)
                    require(match is not None,f'{url}: missing or changed rendered fence after pre {cursor}')
                    if match is not None:cursor=match+1
                search_path=build/current.search.lstrip('/')
                require(search_path.is_file(),f'{url}: missing search index')
                if search_path.is_file():
                    if search_path not in search_cache:search_cache[search_path]=json.loads(search_path.read_text())
                    matches=[r for r in search_cache[search_path] if urlsplit(r.get('ref',r.get('url',''))).path==url]
                    require(len(matches)==1 and matches[0].get('title')==v.front_text(front,'title'),f'{url}: localized search entry')
                for alias in v.front_aliases(front):
                    alias_path=build/prefix/alias.lstrip('/')/'index.html'
                    require(alias_path.is_file() and 'https://doc.pg.center'+url in alias_path.read_text(),f'{url}: legacy alias {alias}')
                check_links(output)
            check_links(print_path)
        witness_temp.cleanup()
    for pair in pairs:
        source=ROOT/pair['source'];target=source.with_suffix('.'+pair['language']+'.md')
        require(digest(source)==pair['source_sha256'] and digest(target)==pair['target_sha256'], f'{target.name}: content changed during validation')
    report={'component':'haproxy','source_pairs':len(pairs),'published_pages':210,'rendered':bool(args.rendered_dir),'locale_gates':locale_gates,'errors':errors,'pairs':pairs}
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    for error in errors[:80]:print(error,file=sys.stderr)
    if errors:print(f'HAProxy publication gate failed: {len(errors)} errors.',file=sys.stderr);return 1
    print(f'HAProxy publication gate passed: {len(pairs)} current translation pairs'+(', 210 pages and complete outputs.' if args.rendered_dir else '.'))
    return 0

if __name__=='__main__':raise SystemExit(main())
