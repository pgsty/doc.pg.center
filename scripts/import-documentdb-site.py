#!/usr/bin/env python3
"""Prepare the complete published DocumentDB /docs/ edition in a NEW directory.

Requires pinned docs sources, the website article export, and PyYAML. The old
import-documentdb.py imported only the docs repository; it misses generated
guides and website corrections. Maintained content is never overwritten here.
"""
import argparse
import hashlib
import html
import json
import posixpath
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit
import yaml

DOCS_REF = 'cf69384e6da9524cc0fc723e8ac5b6c0689af432'
WEB_REF = '90cfa088351557cd618034dfc00ab817c35a5f76'
DOCS_REPO = 'https://github.com/documentdb/docs'
WEB_REPO = 'https://github.com/documentdb/documentdb.github.io'
WEB_FILE = 'app/services/articleService.ts'
WEB_PAGE = 'app/docs/[section]/[[...slug]]/page.tsx'
NOTES_FILE = Path(__file__).resolve().parent.parent / 'data/imports/documentdb-notes.json'

# This introduction is rendered by the website page component, outside article
# Markdown. Keep its command and instructions when converting the published site.
INSTALL_PRIMER = r'''## Choose an environment, then run your first query

Install with Docker or Linux packages once. Create a working instance, then insert
and read a document using a shell, driver, or editor.

1. **Choose an install path.** Start with Docker on Linux, macOS, or Windows.
   Use Linux packages when you need a host installation.

   **Docker: recommended for evaluation and development.** With Docker installed,
   run a local instance on Linux, macOS, or Windows. Replace the credential
   placeholders before running. The port stays on loopback.

   ```bash
   docker run -dt --pull always --name documentdb \
     -p 127.0.0.1:10260:10260 \
     -e USERNAME='<YOUR_USERNAME>' \
     -e PASSWORD='<YOUR_PASSWORD>' \
     ghcr.io/documentdb/documentdb/documentdb-local:latest
   ```

   > [!NOTE]
   > The DocumentDB Local image sends usage telemetry by default. To turn it off,
   > add `-e DOCUMENTDB_USAGE_TELEMETRY=false` before the image name. See
   > [Usage telemetry](/documentdb/documentdb-local/#usage-telemetry) and the
   > [privacy statement](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md).

   Wait for the readiness banner in `docker logs documentdb` before connecting.
   See the [Docker Quick Start](/documentdb/getting-started/docker/).

   **Linux packages.** For environments without Docker, or when you need control
   over PostgreSQL, topology, services, and configuration. Install with apt or dnf
   on Ubuntu 24.04 (Noble) or EL9, then run the setup wizard. Open
   [Linux packages installation](https://documentdb.io/packages?method=packages)
   or the full [Linux Packages Quick Start](/documentdb/getting-started/packages/).

2. **Insert and read your first document.** Pick the client you prefer. Each guide
   connects to the instance you already created and verifies an insert and read.
   Sample data is optional. Start with the
   [Visual Studio Code Quick Start](/documentdb/getting-started/vscode-quickstart/),
   [Node.js Quick Start](/documentdb/getting-started/nodejs-setup/), or
   [Python Quick Start](/documentdb/getting-started/python-setup/).
{.steps}

'''


def digest(data):
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def read_page(text):
    if text.startswith('---\n'):
        _, front, body = text.split('---', 2)
        return yaml.safe_load(front) or {}, body
    return {}, text


def write_page(path, front, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('---\n' + yaml.safe_dump(front, allow_unicode=True, sort_keys=False, width=110)
                    + '---\n\n' + body.strip() + '\n')


def edition_note(text, language='en'):
    title = '编者注' if language == 'zh' else 'Edition note'
    return f'> [!NOTE] {title}\n> {text}\n\n'


def prose_chunks(body):
    fence, chunk = None, []
    for line in body.splitlines(keepends=True):
        match = re.match(r'^\s*(?:>\s*)*(`{3,}|~{3,})', line)
        if match and fence is None:
            yield False, ''.join(chunk)
            chunk, fence = [line], match[1]
        elif fence and match and match[1][0] == fence[0] and len(match[1]) >= len(fence):
            chunk.append(line)
            yield True, ''.join(chunk)
            chunk, fence = [], None
        else:
            chunk.append(line)
    if fence:
        raise ValueError('Unclosed code fence')
    yield False, ''.join(chunk)


def target(relative):
    parts = list(Path(relative).parts)
    if parts[0] == 'api-reference':
        parts[0] = 'reference'
    name = parts[-1]
    parts[-1] = ('_index.md' if name in ('index.md', '_metadata.description.md', 'readme.md')
                 else 'positional-dollar.md' if name == '$.md' else name.replace('$', '').lower())
    return Path(*parts)


def route(path):
    path = path.parent if path.name == '_index.md' else path.with_suffix('')
    return '/documentdb/' + (path.as_posix().strip('./') + '/' if str(path) != '.' else '')


def github_anchor(text):
    text = html.unescape(re.sub(r'<[^>]*>', '', text))
    text = re.sub(r'\[([^]]*)\]\([^)]*\)', r'\1', text)
    return re.sub(r'\s', '-', re.sub(r'[^\w\s-]', '', text.lower().strip()))


def website_anchor(text):
    text = re.sub(r'([a-z\d])([A-Z])', r'\1-\2', text)
    text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1-\2', text)
    return re.sub(r'[\W_]+', '-', text).strip('-').lower()


def anchors(body):
    counts, used = {}, set()
    def prose(text):
        lines = []
        for line in text.splitlines(keepends=True):
            match = re.match(r'^(#{2,6})\s+(.+?)\s*\n?$', line)
            if not match:
                lines.append(line)
                continue
            heading = match[2]
            explicit = re.search(r'\s*\{#([^}]+)\}$', heading)
            base = explicit[1] if explicit else github_anchor(heading)
            counts[base] = counts.get(base, -1) + 1
            anchor = base + (f'-{counts[base]}' if counts[base] else '')
            used.add(anchor)
            alias = website_anchor(heading)
            if len(match[1]) <= 3 and alias and alias != anchor and alias not in used:
                lines.append(f'<span id="{alias}"></span>\n\n')
                used.add(alias)
            lines.append(line if explicit else f'{match[1]} {heading} {{#{anchor}}}\n')
        return ''.join(lines)
    return ''.join(text if code else prose(text) for code, text in prose_chunks(body))


def native_blocks(body):
    def prose(text):
        text = re.sub(r'^(\s*> )\*\*(Note|Warning|Important|Caution|Tip):?\*\*:?\s*',
                      lambda m: m[1] + '[!' + m[2].upper() + ']\n' + m[1], text, flags=re.M | re.I)
        text = text.replace('[!Important]', '[!IMPORTANT]')
        out, table = [], []
        def flush():
            if not table:
                return
            out.extend(table)
            if len(table) > 2 and re.match(r'^\|\s*:?-', table[1]):
                head = [c.strip().lower() for c in table[0].strip().strip('|').split('|')]
                if head[-1] in ('description', 'purpose') and head[0] in (
                        'parameter', 'option', 'field', 'function', 'procedure', 'setting', 'guc'):
                    out.append('{.fields}\n')
                elif len(head) >= 4:
                    out.append('{.wide .expand}\n')
            table.clear()
        for line in text.splitlines(keepends=True):
            if line.startswith('|'):
                table.append(line)
            else:
                flush()
                out.append(line)
        flush()
        return ''.join(out)
    return ''.join(text if code else prose(text) for code, text in prose_chunks(body))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--website-export', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    args = parser.parse_args()
    if args.destination.exists():
        parser.error('Refusing to overwrite existing content; use a new staging directory.')
    notes = json.loads(NOTES_FILE.read_text())['pages']
    revision = subprocess.check_output(['git', '-C', str(args.source), 'rev-parse', 'HEAD'], text=True).strip()
    if revision != DOCS_REF:
        parser.error('The docs checkout must match the pinned revision.')
    files = sorted(p for p in args.source.rglob('*.md') if '.git' not in p.parts)
    articles = json.loads(args.website_export.read_text())
    if not isinstance(articles, dict) or articles.get('docs_commit') != DOCS_REF or articles.get('website_commit') != WEB_REF:
        parser.error('Export the pinned website with scripts/export-documentdb-website.mjs first.')
    page_components = articles.get('page_components', {})
    primer_command = re.search(r'```bash\n(.*?)\n   ```', INSTALL_PRIMER, re.S)[1]
    primer_command = '\n'.join(line.removeprefix('   ') for line in primer_command.splitlines())
    if (page_components.get('source') != WEB_PAGE or
            page_components.get('docker_command') != primer_command):
        parser.error('The website primer command differs from the imported command; review the export.')
    articles = articles['articles']
    virtual = {a['section'] + '/' + a['file'] + '.md': a for a in articles}
    mapping = {p.relative_to(args.source).as_posix(): target(p.relative_to(args.source)) for p in files}
    mapping.update({key: target(key) for key in virtual})
    route_map = {'/docs/': '/documentdb/'}
    for source, dest in mapping.items():
        published = '/docs/' + source.replace('api-reference/', 'reference/', 1)
        for variant in (published, published.removesuffix('.md'),
                        published.replace('/index.md', '/').replace('/_metadata.description.md', '/')):
            route_map[variant.rstrip('/') + '/'] = route(dest)
        route_map[route(dest).replace('/documentdb/', '/docs/', 1)] = route(dest)

    def url(raw, source):
        parsed = urlsplit(raw)
        if not parsed.path or (parsed.netloc and parsed.netloc not in ('documentdb.io', 'documentdb.github.io')):
            return raw
        path = unquote(parsed.path)
        if not path.startswith('/'):
            path = '/docs/' + posixpath.normpath(posixpath.join(str(Path(source).parent), path))
            path = path.replace('/docs/api-reference/', '/docs/reference/')
        mapped = route_map.get(path.rstrip('/') + '/')
        if mapped:
            return urlunsplit(('', '', mapped, parsed.query, parsed.fragment))
        return raw if parsed.netloc or parsed.scheme else urlunsplit(('https', 'documentdb.io', path, parsed.query, parsed.fragment))

    pages, records = {}, []
    for source, dest in sorted(mapping.items()):
        p = args.source / source
        raw = p.read_text() if p.exists() else ''
        front, body = read_page(raw)
        original = body
        a = virtual.get(source)
        if a:
            front, body = a['frontmatter'], a['content']
        generated = not p.exists() or (a and body.strip() != original.strip())
        front = {k: v for k, v in front.items() if k in ('title', 'description')}
        title = front.get('title') or ('DocumentDB' if source == 'readme.md' else Path(source).parent.name.replace('-', ' ').title())
        if title == 'Api Reference':
            title = 'API reference'
        front.update(title=title, type='docs', upstream_source='documentdb',
                     upstream_link=(f'{WEB_REPO}/blob/{WEB_REF}/{WEB_FILE}' if generated
                                    else f'{DOCS_REPO}/blob/{DOCS_REF}/{source}'))
        front.setdefault('description', ('MongoDB Query Language command and operator reference for DocumentDB.'
                                        if title == 'API reference' else title + ' reference for DocumentDB.'))
        if generated:
            front['upstream_ref'] = f'website {WEB_REF[:7]}; DocumentDB 1.0'
        body = re.sub(r'^# [^\n]+\n', '', body, count=1, flags=re.M)
        def links(text):
            return re.sub(r'(!?\[[^\]\n]*\]\()([^\s)]+)', lambda m: m[1] + url(m[2], source), text)
        body = ''.join(t if code else links(t) for code, t in prose_chunks(body))
        if source == 'getting-started/index.md':
            body = INSTALL_PRIMER + body.lstrip()
        if source == 'architecture/index.md':
            front['source_status'] = 'forthcoming'
            body = ('> [!NOTE] Not yet published upstream\n'
                    '> The architecture manual is not available in this source snapshot. The '
                    '[component overview](/documentdb/postgres-api/) describes the existing extensions and gateway.\n')
        if source in ('getting-started/prebuilt-packages.md', 'getting-started/vscode-extension-guide.md'):
            front['source_status'] = 'superseded'
            successor = 'packages' if 'prebuilt-packages' in source else 'vscode-quickstart'
            body = ('> [!NOTE] Superseded upstream\n> The official website now directs this page to the '
                    f'[current guide](/documentdb/getting-started/{successor}/). '
                    'The source document is retained here for existing links.\n\n' + body.lstrip())
        body = native_blocks(anchors(body))
        if source == 'linux-packages/offline.md':
            body = body.replace('```bash\n# Debian / Ubuntu',
                                '```bash {tab="Debian / Ubuntu" group="documentdb-offline-os" value="deb"}\n# Debian / Ubuntu')
            body = body.replace('```bash\n# RHEL-compatible',
                                '```bash {tab="EL / RHEL" value="rpm"}\n# RHEL-compatible')
        if source.endswith('/$datefromstring.md'):
            front['description'] = front['description'].replace('$dateDiff', '$dateFromString')
        if dest.as_posix() in notes:
            body = edition_note(notes[dest.as_posix()]['en']) + body.lstrip()
        pages[dest] = [front, body]
        records.append(dict(source=source, target='content/documentdb/' + dest.as_posix(), language='en',
                            route=route(dest), sha256=digest(raw), effective_sha256=digest(a['content'] if a else original),
                            effective_repository=WEB_REPO if generated else DOCS_REPO,
                            effective_commit=WEB_REF if generated else DOCS_REF,
                            effective_source=WEB_FILE if generated else source,
                            status=front.get('source_status', 'generated-upstream' if generated else 'imported')))
        if source == 'getting-started/index.md':
            records[-1]['additional_source'] = WEB_PAGE
            records[-1]['additional_source_sha256'] = page_components['sha256']
        if dest.as_posix() in notes:
            records[-1]['local_notes'] = 'data/imports/documentdb-notes.json#' + dest.as_posix()
    for parent in sorted({p.parent for p in pages}):
        children = [p for p in pages if p.parent == parent and p.name != '_index.md']
        children += [p for p in pages if p.name == '_index.md' and p.parent.parent == parent and p.parent != parent]
        for i, p in enumerate(sorted(children, key=lambda p: (pages[p][0]['title'].lower(), str(p)))):
            pages[p][0]['weight'] = (i + 1) * 10
    navigation_targets = set()
    for a in articles:
        for i, nav in enumerate(a['navigation']):
            r = route_map.get(nav['link'].rstrip('/') + '/')
            p = next((p for p in pages if route(p) == r), None)
            if p and p.name != '_index.md':
                pages[p][0]['weight'] = (i + 1) * 10
                navigation_targets.add(p)
    # Retained legacy guides must follow, not interleave with, the live menu.
    for p in pages:
        if p.parent == Path('getting-started') and p.name != '_index.md' and p not in navigation_targets:
            pages[p][0]['weight'] += 1000
    for i, section in enumerate(('getting-started', 'documentdb-local', 'linux-packages', 'postgres-api', 'reference', 'kubernetes-operator', 'architecture')):
        pages[Path(section) / '_index.md'][0]['weight'] = (i + 1) * 10
    pages[Path('reference/_index.md')][0]['cascade'] = {'section_index': 'list'}
    pages[Path('postgres-api/_index.md')][0]['linkTitle'] = 'PostgreSQL API'
    front, _ = pages[Path('_index.md')]
    front.update(title='DocumentDB documentation', linkTitle='DocumentDB', weight=-10,
                 description='DocumentDB 1.0: installation, operations, PostgreSQL APIs, commands, and operators.',
                 sidebar_root_for='self', sidebar_root_link_self=True, no_list=True, icon='fa-solid fa-file-code',
                 outputs=['HTML', 'RSS', 'print', 'markdown', 'LLMSFULL'],
                 cascade={'type': 'docs', 'upstream_source': 'documentdb'})
    pages[Path('_index.md')][1] = '''DocumentDB provides a PostgreSQL-based document database with BSON storage,
document operations, indexes, and a MongoDB wire protocol gateway. This edition
includes the published DocumentDB 1.0 documentation and its Simplified Chinese translation.

- [Getting started](/documentdb/getting-started/) — Docker, Linux packages, and your first query with a shell, driver, or editor.
- [DocumentDB Local](/documentdb/documentdb-local/) — Container options, persistent data, certificates, and telemetry.
- [Linux package operations](/documentdb/linux-packages/) — Secure, operate, upgrade, and install without internet access.
- [PostgreSQL API](/documentdb/postgres-api/) — Extensions, gateway, functions, and configuration parameters.
- [Command and operator reference](/documentdb/reference/) — MongoDB Query Language commands, expressions, and aggregation stages.
- [Kubernetes Operator](/documentdb/kubernetes-operator/) — Deployment prerequisites and the independently versioned operator manual.
{.cards}

> [!NOTE] Source edition
> The documentation repository is pinned at `cf69384`; website-generated guides
> and corrections are pinned at `90cfa08` (7 November 2026). The upstream
> [architecture chapter](/documentdb/architecture/) is still forthcoming.
> See [source and translation notices](/attribution/#documentdb).
'''
    if set(notes) - {p.as_posix() for p in pages}:
        parser.error('An editorial annotation points to a missing page.')
    for dest, (front, body) in pages.items():
        write_page(args.destination / dest, front, body)
    args.manifest.write_text(json.dumps(dict(component='documentdb', source_repository=DOCS_REPO, commit=DOCS_REF,
                    website_repository=WEB_REPO, website_commit=WEB_REF, snapshot_date='2026-11-07',
                    editorial_notes='data/imports/documentdb-notes.json', editorial_notes_sha256=digest(NOTES_FILE.read_bytes()),
                    docs_markdown_records=len(files), website_articles=len(articles), english_pages=len(pages),
                    pages=records, assets=[]), ensure_ascii=False, indent=2) + '\n')
    print(f'Prepared {len(pages)} English pages from {len(files)} docs records and {len(articles)} website articles.')


if __name__ == '__main__':
    main()
