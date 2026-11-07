#!/usr/bin/env python3
"""Import documentdb/docs cf69384 into a new content/documentdb tree.

Pass the downloaded repository directory. Requires PyYAML at import time.
Never rerun over maintained content; subsequent updates are reviewed diffs.
"""
import hashlib
import importlib.util
import json
import posixpath
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
REF = 'cf69384e6da9524cc0fc723e8ac5b6c0689af432'
REPO = 'https://github.com/documentdb/docs'
spec = importlib.util.spec_from_file_location('import_sites', ROOT / 'scripts/import-kernel-sites.py')
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)
source = Path(sys.argv[1]).resolve()
dest = ROOT / 'content/documentdb'
if dest.exists():
    raise SystemExit('Refusing to overwrite maintained DocumentDB content')


def target(relative):
    parts = list(relative.parts)
    if parts[0] == 'api-reference':
        parts[0] = 'reference'
    name = parts[-1]
    if name in ('index.md', '_metadata.description.md', 'readme.md'):
        parts[-1] = '_index.md'
    else:
        parts[-1] = name.replace('$', '').lower() if name != '$.md' else 'positional-dollar.md'
    return Path(*parts)


files = sorted(source.rglob('*.md'))
mapping = {str(p.relative_to(source)): target(p.relative_to(source)) for p in files}
route = lambda p: '/documentdb/' + (str(p.parent) if p.name == '_index.md' else str(p.with_suffix(''))).strip('.') .strip('/') + '/'


def url(raw, relative):
    parsed = urlsplit(raw)
    if not parsed.path:
        return raw
    if parsed.netloc and parsed.netloc not in ('documentdb.io', 'documentdb.github.io'):
        return raw
    path = unquote(parsed.path)
    if parsed.netloc or path.startswith('/'):
        if not path.startswith('/docs/'):
            return raw
        key = path.removeprefix('/docs/').replace('reference/', 'api-reference/', 1)
        key = key.rstrip('/')
        candidates = [key + '.md', key + '/index.md', key + '/_metadata.description.md']
    else:
        key = posixpath.normpath(posixpath.join(str(relative.parent), path))
        candidates = [key, key.rstrip('/') + '/index.md', key.rstrip('/') + '/_metadata.description.md']
    match = next((mapping[k] for k in candidates if k in mapping), None)
    if match is None:
        return raw
    return route(match).replace('//', '/') + ('?' + parsed.query if parsed.query else '') + ('#' + parsed.fragment if parsed.fragment else '')


records=[]
for p in files:
    relative=p.relative_to(source)
    text=p.read_text()
    if text.startswith('---\n'):
        front, body=common.read_page(p)
    else:
        front,body={},text
    title=front.get('title') or ('DocumentDB' if relative.name == 'readme.md' else relative.parent.name.replace('-', ' ').title())
    front={k:v for k,v in front.items() if k in ('title','description')}
    front.update(title=title, type='docs', upstream_source='documentdb',
                 upstream_link=f'{REPO}/blob/{REF}/{relative.as_posix()}')
    front.setdefault('description',title + ' — DocumentDB documentation.')
    # API headings and syntax remain intact; the page shell supplies the H1.
    body=re.sub(r'^# [^\n]+\n', '',body,count=1,flags=re.M)
    def prose(text):
        return re.sub(r'(!?\[[^\]\n]*\]\()([^\s)]+)',lambda m:m[1]+url(m[2],relative),text)
    body=''.join(t if code else prose(t) for code,t in common.prose_chunks(body))
    if str(relative)=='architecture/index.md':
        front['source_status']='forthcoming'
        body='\n> [!NOTE] Not yet published upstream\n> The architecture manual is not available in this source snapshot. The [component overview](/documentdb/postgres-api/) describes the existing extensions and gateway.\n'
    output=dest/mapping[str(relative)]
    common.write_page(output,front,'\n'+body.lstrip())
    records.append(dict(source=str(relative),target=str(output.relative_to(ROOT)),language='en',
                        route=route(mapping[str(relative)]).replace('//','/'),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status=front.get('source_status','imported')))

# Every category gets the native OINK section index, including empty upstream
# categories. It contains links to its actual children, never guessed coverage.
for directory in sorted({p.parent for p in dest.rglob('*.md')}):
    cursor=directory
    while cursor.is_relative_to(dest):
        index=cursor/'_index.md'
        if not index.exists():
            common.write_page(index,dict(title=cursor.name.replace('-',' ').title(),description='DocumentDB reference topics.',type='docs',
                upstream_source='documentdb',upstream_link=f'{REPO}/tree/{REF}/api-reference'), '\n')
        if cursor==dest:break
        cursor=cursor.parent

for group in ('getting-started','postgres-api','documentdb-local','kubernetes-operator','architecture'):
    nav=source/group/'navigation.yml'
    if not nav.exists():continue
    for i,entry in enumerate(yaml.safe_load(nav.read_text()) or []):
        key=group+'/'+entry.get('link','')
        if key not in mapping:continue
        p=dest/mapping[key];fm,body=common.read_page(p);fm['weight']=(i+1)*10;common.write_page(p,fm,body)

root=dest/'_index.md';front,body=common.read_page(root)
front.update(title='DocumentDB documentation',linkTitle='DocumentDB',weight=150,sidebar_root_for='self',sidebar_root_link_self=True,
             outputs=['HTML','RSS','print','markdown','LLMSFULL'],cascade={'type':'docs','upstream_source':'documentdb'})
body='''
DocumentDB provides a PostgreSQL-based document database with BSON storage,
document operations, indexes, and a MongoDB protocol gateway. This collection
preserves the official documentation at commit `cf69384` (DocumentDB 1.0).

- [Getting started](/documentdb/getting-started/)
- [Command and operator reference](/documentdb/reference/)
- [PostgreSQL extensions and gateway](/documentdb/postgres-api/)
- [DocumentDB Local](/documentdb/documentdb-local/)
- [Kubernetes operator](/documentdb/kubernetes-operator/)
{.cards}

The upstream architecture chapter is still forthcoming. The Chinese edition
currently includes an introduction and the translated component overview;
the remaining manuals are available in English.
'''
common.write_page(root,front,body)
(ROOT/'data/imports/documentdb.json').write_text(json.dumps(dict(component='documentdb',source_repository=REPO,commit=REF,pages=records,assets=[]),ensure_ascii=False,indent=2)+'\n')
print(f'DocumentDB: {len(records)} upstream Markdown records')
