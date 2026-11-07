#!/usr/bin/env python3
"""Import the reviewed OrioleDB OINK edition without overwriting maintained pages.

Usage: python3 scripts/import-orioledb.py /path/to/oriole.pgsty.com
Requires PyYAML only for this one-time import. The resulting Markdown is maintained
directly; later upstream updates must be reviewed as diffs. Product landing pages,
blog posts and taxonomies belong to the source site, not this documentation tree.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('import_sites', ROOT / 'scripts/import-kernel-sites.py')
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)

ICONS = {
    'introduction': 'fa-dove', 'usage': 'fa-rocket', 'getting-started': 'fa-play',
    'configuration': 'fa-sliders', 'rewind': 'fa-clock-rotate-left',
    'decoupled-storage': 'fa-cloud', 'pg-upgrade': 'fa-arrow-up',
    'architecture': 'fa-diagram-project', 'overview': 'fa-sitemap',
    'checkpoints': 'fa-floppy-disk', 'recovery': 'fa-rotate',
    'buffering': 'fa-memory', 'concurrency': 'fa-code-branch',
    'row-level-concurrency': 'fa-lock', 'fsm': 'fa-hard-drive',
    'concurrent-index': 'fa-list', 'contributing': 'fa-code',
    'code-structure': 'fa-folder-tree', 'local-builds': 'fa-hammer',
    'docker-builds': 'fa-box', 'binary-compatibility': 'fa-puzzle-piece',
    'benchmarks': 'fa-chart-line', 'pgbench': 'fa-gauge-high',
    'tracking': 'fa-location-dot',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    dest = ROOT / 'content/orioledb'
    if dest.exists():
        raise SystemExit(f'Refusing to overwrite maintained content: {dest}')
    snapshot_path = source / 'data/source-manifest.json'
    snapshot = json.loads(snapshot_path.read_text())
    upstream_pages = {
        item[lang]: item for item in snapshot['items']
        if item['kind'] in ('docs', 'benchmarks') for lang in ('english', 'chinese')
    }
    manifest = dict(component='orioledb', source_site='https://oriole.pgsty.com/',
                    upstream_site=snapshot['authority'], snapshot_date=snapshot['snapshot_date'],
                    source_manifest_sha256=common.digest(snapshot_path.read_bytes()),
                    pages=[], assets=[])
    assets = set()
    for path in sorted([*(source / 'content/docs').rglob('*.md'),
                        *(source / 'content/benchmarks').rglob('*.md')]):
        relative = path.relative_to(source / 'content')
        lang = 'zh' if path.name.endswith('.zh.md') else 'en'
        prefix = '/zh' if lang == 'zh' else ''
        front, body = common.read_page(path)
        if relative.parts[0] == 'docs':
            target_relative = Path(*relative.parts[1:])
            if len(relative.parts) == 2:
                target_relative = Path('introduction') / ('index.zh.md' if lang == 'zh' else 'index.md')
        else:
            target_relative = relative
        target = dest / target_relative
        section = target_relative.parts[0]
        slug = target_relative.parent.name
        front.pop('sidebar_root_for', None)
        front.pop('cascade', None)
        front.pop('outputs', None)
        front.pop('aliases', None)
        front['type'] = 'docs'
        front['icon'] = 'fa-solid ' + ICONS[slug]
        front['search_keywords'] = ['OrioleDB', slug.replace('-', ' ')]
        if slug == 'getting-started' and lang == 'en':
            front['title'] = 'Getting started with OrioleDB'
        front['upstream_source'] = 'orioledb-website' if section == 'benchmarks' else 'orioledb'
        front.setdefault('upstream_link', 'https://www.orioledb.com/pgbench-benchmark'
                         if section == 'benchmarks' else 'https://www.orioledb.com/docs')
        front['upstream_notice'] = prefix + '/orioledb/attribution/'
        front['upstream_modified'] = True
        if section == 'introduction':
            front.update(title='OrioleDB 概览' if lang == 'zh' else 'OrioleDB overview',
                         linkTitle='概览' if lang == 'zh' else 'Overview', weight=10)
        if target.name.startswith('_index'):
            front['outputs'] = ['HTML', 'RSS', 'print', 'markdown']
            if section == 'benchmarks':
                front['weight'] = 50
        # Native OINK attribution also appears in Markdown and print exports.
        body = re.sub(r'\n---\n\n(?:Source:|来源：)[^\n]+\n\{\.oriole-source-note\}\s*$', '\n', body)

        def rewrite_url(raw):
            parsed = urlsplit(raw)
            if parsed.netloc or parsed.scheme or not parsed.path:
                return raw
            url = parsed.path
            if url.startswith('/images/orioledb/'):
                original = source / 'static' / url.lstrip('/')
                local = target.parent / original.name
                local.parent.mkdir(parents=True, exist_ok=True)
                if not local.exists():
                    shutil.copyfile(original, local)
                    manifest['assets'].append(dict(source=str(original.relative_to(source)),
                        target=str(local.relative_to(ROOT)), bytes=local.stat().st_size,
                        sha256=common.digest(local.read_bytes())))
                assets.add(str(original.relative_to(source)))
                url = original.name
            elif url == '/files/tracking-bench.py':
                url = '/orioledb/assets/tracking-bench.py'
            elif url == '/licenses/LICENSE-POSTGRESQL.txt':
                url = '/third_party/orioledb/LICENSE-POSTGRESQL.txt'
            else:
                logical = url.removeprefix('/zh')
                if logical.rstrip('/') == '/docs':
                    url = prefix + '/orioledb/introduction/'
                elif logical.startswith('/docs/'):
                    url = prefix + '/orioledb/' + logical.removeprefix('/docs/')
                elif logical.startswith('/benchmarks/'):
                    url = prefix + '/orioledb' + logical
                elif logical == '/about/attribution/':
                    url = prefix + '/orioledb/attribution/'
                else:
                    raise ValueError(f'Unmapped local URL in {relative}: {raw}')
            return urlunsplit(('', '', url, parsed.query, parsed.fragment))

        def rewrite_prose(text):
            text = re.sub(r'(?P<start>!?\[[^\]\n]*\]\()(?P<url>[^\s)]+)',
                          lambda m: m['start'] + rewrite_url(m['url']), text)
            text = re.sub(r'(?P<start>\b(?:href|src)=["\x27])(?P<url>[^"\x27]+)',
                          lambda m: m['start'] + rewrite_url(m['url']), text)
            return text

        chunks = list(common.prose_chunks(body))
        body = ''.join(text if code else rewrite_prose(text) for code, text in chunks)
        common.write_page(target, front, body)
        record = dict(source=str(path.relative_to(source)), target=str(target.relative_to(ROOT)),
                      language=lang, sha256=common.digest(path.read_bytes()),
                      code_sha256=[common.digest(text.encode()) for code, text in chunks if code],
                      status='imported')
        if record['source'] in upstream_pages:
            upstream = upstream_pages[record['source']]
            record.update(upstream_url=upstream['source_url'],
                          upstream_html_sha256=upstream['source_sha256'],
                          heading_ids=upstream['headings'])
        manifest['pages'].append(record)

    for original, relative in (
        ('static/files/tracking-bench.py', 'static/orioledb/assets/tracking-bench.py'),
        ('static/licenses/LICENSE-POSTGRESQL.txt', 'static/third_party/orioledb/LICENSE-POSTGRESQL.txt'),
    ):
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / original, target)
        manifest['assets'].append(dict(source=original, target=relative,
            bytes=target.stat().st_size, sha256=common.digest(target.read_bytes())))
    (ROOT / 'data/imports/orioledb.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f"OrioleDB: {len(manifest['pages'])} imported pages, {len(manifest['assets'])} assets")


if __name__ == '__main__':
    main()
