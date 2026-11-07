#!/usr/bin/env python3
"""Import an existing OINK edition into a component (one-time, no overwrites).

Requires PyYAML only for importing, never for normal builds. The maintained
Markdown is authoritative after import. Run with --help for the input contract.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_page(path):
    text = path.read_text()
    _, front, body = text.split('---', 2)
    return yaml.safe_load(front) or {}, body


def write_page(path, front, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('---\n' + yaml.safe_dump(front, allow_unicode=True, sort_keys=False, width=110)
                    + '---\n' + body.rstrip() + '\n')


def prose_chunks(body):
    """Yield fenced examples verbatim; rewrite destinations only in prose."""
    fence = None
    chunk = []
    for line in body.splitlines(keepends=True):
        match = re.match(r'^\s*(?:>\s*)*(`{3,}|~{3,})', line)
        if match and fence is None:
            yield False, ''.join(chunk)
            chunk = [line]
            fence = match[1]
        elif fence and match and match[1][0] == fence[0] and len(match[1]) >= len(fence):
            chunk.append(line)
            yield True, ''.join(chunk)
            chunk, fence = [], None
        else:
            chunk.append(line)
    yield bool(fence), ''.join(chunk)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('component')
    parser.add_argument('--name', required=True)
    parser.add_argument('--upstream', required=True, help='Fallback source URL for generated indexes')
    parser.add_argument('--weight', type=int, default=80)
    args = parser.parse_args()
    source = args.source.resolve()
    component = args.component
    dest = ROOT / 'content' / component
    if dest.exists():
        raise SystemExit(f'Refusing to overwrite maintained content: {dest}')
    config = yaml.safe_load(next(source.glob('hugo.y*')).read_text())
    default = config.get('defaultContentLanguage', 'en')
    host = urlsplit(config['baseURL']).netloc
    pages = []
    routes = {}
    for path in sorted((source / 'content').rglob('*.md')):
        relative = path.relative_to(source / 'content')
        if len(relative.parts) == 1:
            continue  # product landing pages are replaced by the manual root
        front, body = read_page(path)
        lang = next((lang for lang in ('en', 'zh') if path.name.endswith('.' + lang + '.md')), default)
        stem = re.sub(r'\.(en|zh)$', '', path.stem)
        branch_index = stem == 'index' and any(path.parent.glob('_index*.md'))
        logical = relative.parent if stem in ('index', '_index') and not branch_index else relative.with_name(stem)
        old_path = '/' + logical.as_posix().strip('/') + '/'
        old_route = ('' if lang == default else '/' + lang) + old_path
        parts = list(relative.parts)
        if parts[0] == 'docs':
            parts.pop(0)
        elif parts[0] == 'about':
            parts[0] = 'site'  # IvorySQL has its own upstream docs/about tree
        if branch_index:
            stem = 'overview'
        parts[-1] = stem + ('.zh.md' if lang == 'zh' else '.md')
        target = dest.joinpath(*parts)
        logical_target = target.relative_to(ROOT / 'content')
        logical_target = logical_target.parent if stem in ('index', '_index') else logical_target.with_name(stem)
        new_route = ('' if lang == 'en' else '/zh') + '/' + logical_target.as_posix() + '/'
        item = dict(source=path, target=target, lang=lang, front=front, body=body,
                    old_route=old_route, new_route=new_route)
        pages.append(item)
        for alias in [old_route, old_route.rstrip('/'), *front.get('aliases', [])]:
            routes[alias] = new_route
        for name in (str(relative), str(relative).replace('.en.md', '.md').replace('.zh.md', '.md')):
            routes[('' if lang == default else '/' + lang) + '/' + name] = new_route
    # The original home is now the collection root.
    for lang in ('en', 'zh'):
        routes['/' if lang == default else '/' + lang + '/'] = ('' if lang == 'en' else '/zh') + '/' + component + '/'
    assets = {}
    for path in sorted((source / 'static').rglob('*')):
        if not path.is_file() or path.name.startswith('.') or path.name.startswith('favicon'):
            continue
        relative = path.relative_to(source / 'static')
        target = ROOT / 'static' / component / 'assets' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        assets['/' + relative.as_posix()] = '/' + component + '/assets/' + relative.as_posix()

    def rewrite_url(raw, item, source_metadata=False):
        parsed = urlsplit(raw)
        if parsed.scheme and parsed.scheme not in ('https', 'http'):
            return raw
        if parsed.netloc and parsed.netloc != host:
            return raw
        if not parsed.path:
            return raw
        absolute = urlsplit(urljoin('https://' + host + item['old_route'], raw))
        path = unquote(absolute.path)
        target = assets.get(path) or routes.get(path) or routes.get(path.rstrip('/') + '/')
        # A relative resource may have been written against the Markdown file.
        if not target and not parsed.path.startswith('/'):
            rel = '/' + posixpath.normpath(posixpath.join(str(item['source'].relative_to(source / 'content').parent), parsed.path))
            target = assets.get(rel) or routes.get(rel)
        if not target:
            if path.startswith('/docs/') or path.startswith('/en/docs/') or path.startswith('/zh/docs/'):
                logical = re.sub(r'^/(?:en/|zh/)?docs/', '', path)
                target = ('/zh' if path.startswith('/zh/') or (default == 'zh' and not path.startswith('/en/')) else '') + '/' + component + '/' + logical
            else:
                return raw
        return urlunsplit(('', '', target, parsed.query, parsed.fragment))

    manifest = dict(component=component, source_site=config['baseURL'], pages=[], assets=[])
    for item in pages:
        front, body = item['front'], item['body']
        for key in ('aliases', 'url', 'menus', 'menu', 'body_class', 'theme_color', 'theme_color_dark',
                    'footer_style', 'github_repo', 'github_branch', 'path_base_for_github_subdir', 'translationKey'):
            front.pop(key, None)
        def clean(value):
            if isinstance(value, dict):
                return {k: clean(v) for k, v in value.items() if k not in ('body_class', 'theme_color', 'theme_color_dark', 'footer_style')}
            if isinstance(value, list):
                return [clean(v) for v in value]
            if isinstance(value, str) and (value.startswith('/') or value.startswith(config['baseURL'])):
                return rewrite_url(value, item)
            return value
        front = clean(front)
        upstream = front.get('upstream_source', component)
        if component == 'pgedge' and upstream in ('spock', 'lolor', 'safesession', 'snowflake'):
            upstream = component + '-' + upstream
        elif component in ('ivorysql', 'percona', 'babelfish'):
            upstream = component
        front['upstream_source'] = upstream
        if not front.get('upstream_link'):
            front['upstream_link'] = args.upstream
        front['type'] = 'docs'
        # Keep the host site's appearance, navbar, and independent collection tree.
        if item['target'].parent == dest and item['target'].name.startswith('_index'):
            front.update(title=args.name + (' 文档' if item['lang'] == 'zh' else ' documentation'),
                         linkTitle=args.name, weight=args.weight, sidebar_root_for='self',
                         sidebar_root_link_self=True, outputs=['HTML', 'RSS', 'print', 'markdown', 'LLMSFULL'])
            front.setdefault('cascade', {}).update(type='docs', upstream_source=component)
            front.setdefault('description', args.name)
        elif front.get('sidebar_root_for') == 'self':
            front['sidebar_root_menu'] = False
        def rewrite_prose(text):
            text = re.sub(r'(?P<start>!?\[[^\]\n]*\]\()(?P<url>[^\s)]+)',
                          lambda m: m['start'] + rewrite_url(m['url'], item), text)
            text = re.sub(r'(?P<start>\b(?:href|src|poster)=["\x27])(?P<url>[^"\x27]+)',
                          lambda m: m['start'] + rewrite_url(m['url'], item), text)
            text = re.sub(r'(?m)^(\[[^\]]+\]:\s*)(\S+)', lambda m: m[1] + rewrite_url(m[2], item), text)
            return text
        body = ''.join(text if code else rewrite_prose(text) for code, text in prose_chunks(body))
        body = re.sub(r'\{\{< upstream-export >\}\}', '', body)
        # Existing guide-only stubs must never masquerade as finished translations.
        if item['lang'] == 'zh' and ('本页是 AgensGraph 2.18.6.1 的中文导读' in body or '上游尚未提供此页的中文译文' in body):
            front['translation_status'] = 'placeholder'
            english = item['new_route'].removeprefix('/zh')
            body = '\n> [!NOTE] 译文待补\n> 本页中文正文尚未完成，请阅读' + f'<a href="{english}" hreflang="en" lang="en">英文原文</a>。\n'
        write_page(item['target'], front, body)
        manifest['pages'].append(dict(source=str(item['source'].relative_to(source)),
            target=str(item['target'].relative_to(ROOT)), language=item['lang'], old_route=item['old_route'],
            route=item['new_route'], sha256=digest(item['source'].read_bytes()),
            code_sha256=[digest(text.encode()) for code, text in prose_chunks(body) if code],
            status=front.get('translation_status', 'imported')))
    for old, new in assets.items():
        path=ROOT / 'static' / new.lstrip('/')
        manifest['assets'].append(dict(source='static'+old, target='static'+new,
                                       bytes=path.stat().st_size, sha256=digest(path.read_bytes())))
    record = ROOT / 'data' / 'imports' / (component + '.json')
    record.parent.mkdir(exist_ok=True)
    record.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'{component}: {len(pages)} pages, {len(assets)} assets')


if __name__ == '__main__':
    main()
