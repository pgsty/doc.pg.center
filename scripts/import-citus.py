#!/usr/bin/env python3
"""Import a frozen Microsoft Learn Citus 14 snapshot into a new collection.

Requires BeautifulSoup and PyYAML at import time. Source snapshots live outside
the repository. Refuses to overwrite maintained content. English is authoritative;
Chinese output starts as an explicitly labelled machine draft awaiting review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup, NavigableString, Comment
import yaml

ROOT = Path(__file__).resolve().parents[1]
VIEW = 'citus-14'
BASE = 'https://learn.microsoft.com/en-us/postgresql/citus/'
GROUPS = [
    ('overview', 'Overview', '概览', 'Understand Citus, its workloads, and common questions.', '了解 Citus、适用负载与常见问题。', 'circle-info', ['what-is-citus', 'postgresql-citus-scale', 'use-cases', 'faq-citus', 'help-support']),
    ('installation', 'Installation', '安装部署', 'Start locally or deploy a cluster of PostgreSQL nodes.', '从本地体验开始，部署多节点 PostgreSQL 集群。', 'download', ['getting-started', 'single-node', 'single-node-docker', 'single-node-debian', 'single-node-rhel', 'multi-node', 'multi-node-ubuntu-debian', 'multi-node-fedora-centos-rhel', 'citus-cloud']),
    ('tutorials', 'Tutorials', '教程', 'Build multitenant, analytics, time series, and microservice applications.', '构建多租户、实时分析、时序和微服务应用。', 'graduation-cap', ['tutorial-multi-tenant', 'tutorial-analytics', 'tutorial-time-series', 'tutorial-micro-services']),
    ('modeling', 'Data modeling', '数据建模', 'Choose distribution keys and integrate your application.', '选择分布键，组织数据并集成应用程序。', 'diagram-project', ['app-type', 'data-modeling', 'integrations', 'triggers']),
    ('operations', 'Administration', '集群运维', 'Manage tables, diagnose queries, tune performance, and upgrade Citus.', '管理表、诊断查询、优化性能并升级 Citus。', 'gears', ['cluster-management', 'table-management', 'diagnostic-queries', 'performance-tuning', 'benchmark', 'upgrade-citus']),
    ('migration', 'Migration', '迁移指南', 'Move PostgreSQL schemas, queries, data, and application frameworks to Citus.', '将 PostgreSQL 模式、查询、数据与应用框架迁移到 Citus。', 'arrow-right-arrow-left', ['migrate/migration', 'migrate/migration-schema', 'migrate/migration-query', 'migrate/migration-data', 'migrate/migration-data-small', 'migrate/migration-data-big', 'migrate/migration-ruby-rails', 'migrate/migration-asp']),
    ('reference', 'SQL and API reference', 'SQL 与 API 参考', 'Look up SQL support, functions, configuration, metadata, and query execution.', '查阅 SQL 支持、函数、配置、元数据与查询执行。', 'code', ['reference', 'api', 'api-udf', 'api-guc', 'api-metadata', 'reference-ddl', 'reference-dml', 'reference-processing', 'reference-propagation', 'reference-sql', 'reference-workarounds', 'common-errors']),
    ('articles', 'Articles and blog archive', '专题与博客', 'Read the Citus technical articles retained in the upstream manual.', '阅读上游手册收录的 Citus 技术文章与博客。', 'newspaper', ['guides', 'designing-saas', 'sharding-mt-app', 'aggregation', 'efficient-rollup', 'hyperloglog-count-distinct', 'outer-joins', 'faceted-search', 'metrics-dashboard', 'semi-structured-data', 'parallel-indexing']),
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def select_version(text):
    """Learn also leaks literal moniker directives inside fenced examples."""
    selected, active = [], []
    for line in text.splitlines(keepends=True):
        match = re.fullmatch(r'\s*:::moniker range="([<>=]+)citus-(\d+)"\s*', line)
        if match:
            op, version = match[1], int(match[2])
            active.append({'=': 14 == version, '<=': 14 <= version,
                           '>=': 14 >= version, '<': 14 < version,
                           '>': 14 > version}[op])
        elif re.fullmatch(r'\s*:::moniker-end\s*', line):
            if not active:
                raise ValueError('Unmatched moniker end')
            active.pop()
        elif all(active):
            if ':::moniker' in line:
                raise ValueError('Unrecognized moniker directive: '+line)
            selected.append(line)
    if active:
        raise ValueError('Unclosed moniker block')
    return ''.join(selected)


def page(source, lang, slug):
    path = source / 'html' / lang / (slug.replace('/', '__') + '.html')
    soup = BeautifulSoup(path.read_bytes(), 'html.parser')
    metadata = {m.get('name'): m.get('content') for m in soup.find_all('meta') if m.get('name')}
    for node in soup.select('[data-moniker]'):
        if VIEW not in node.get('data-moniker', '').split():
            node.decompose()
    # FAQ answers have nested .content elements; selecting them twice duplicates
    # every answer and code block after the complete article.
    parts = [node for node in soup.select('main .content')
             if not node.find_parent(class_='content')]
    content = BeautifulSoup('<div>' + ''.join(str(p) for p in parts) + '</div>', 'html.parser').div
    # Some Learn pages publish terminal output as paragraphs. Preserve the
    # original line breaks before ordinary prose whitespace is normalized.
    for node in content.find_all('p'):
        text = node.get_text()
        if text.startswith(('┌', 'ERROR:')):
            pre, code = soup.new_tag('pre'), soup.new_tag('code')
            code['class'] = ['lang-text']
            code.string = text.strip()
            pre.append(code)
            node.replace_with(pre)
    for code in content.select('pre code'):
        if ':::moniker' in code.get_text():
            code.string = select_version(code.get_text())
    title = content.find('h1').get_text(' ', strip=True)
    for h in content.find_all('h1'):
        h.decompose()
    return content, metadata, title, path


def write(path, front, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('---\n' + yaml.safe_dump(front, allow_unicode=True, sort_keys=False, width=1000) + '---\n\n' + body.strip() + '\n')


class Converter:
    def __init__(self, slug, routes, assets, lang):
        self.slug, self.routes, self.assets, self.lang = slug, routes, assets, lang
        self.base = BASE + ('' if slug == 'index' else slug)

    def url(self, raw):
        if raw.startswith('#'):
            return raw
        absolute = urljoin(self.base, raw)
        p = urlsplit(absolute)
        path = unquote(p.path)
        logical = re.sub(r'^/(?:en-us|zh-cn)/postgresql/citus/?', '', path).rstrip('/')
        suffix = '#' + p.fragment if p.fragment else ''
        if p.netloc == 'learn.microsoft.com' and re.match(r'^/(?:en-us|zh-cn)/postgresql/citus(?:/|$)', path):
            if logical in self.routes:
                return self.routes[logical] + suffix
        # Other Learn products stay on their upstream host, including absolute paths.
        return absolute

    def children(self, node):
        return ''.join(self.render(x) for x in node.children)

    def render(self, node):
        if isinstance(node, Comment):
            return ''
        if isinstance(node, NavigableString):
            return re.sub(r'\s+', ' ', str(node))
        name = node.name
        if name in ('script', 'style', 'button'):
            return ''
        if name == 'pre':
            code = node.find('code')
            text = (code or node).get_text()
            cls = (code or node).get('class', [])
            lang = next((x.removeprefix('lang-') for x in cls if x.startswith('lang-')), 'text')
            lang = {'postgresql': 'sql', 'output': 'text'}.get(lang, lang)
            fence = '`' * max(3, max((len(x) + 1 for x in re.findall(r'`+', text)), default=3))
            return f'\n\n{fence}{lang}\n{text.rstrip(chr(10))}\n{fence}\n\n'
        if name == 'code':
            text = node.get_text()
            fence = '`' * max(1, max((len(x) + 1 for x in re.findall(r'`+', text)), default=1))
            pad = ' ' if text.startswith('`') or text.endswith('`') else ''
            return fence + pad + text + pad + fence
        if name in ('strong', 'b', 'em', 'i'):
            marker = '**' if name in ('strong', 'b') else '*'
            return marker + self.children(node).strip() + marker
        if name == 'a':
            text = self.children(node).strip()
            if not node.get('href'):
                return f'<a id="{node["id"]}"></a>' if node.get('id') else text
            return f'[{text}]({self.url(node["href"])})'
        if name == 'img':
            return '\n\n![' + node.get('alt', '').replace(']', '\\]') + '](' + self.assets[node['src']] + ')\n\n'
        if name == 'br':
            return '<br>'
        if name in ('h2', 'h3', 'h4', 'h5', 'h6'):
            return '\n\n' + '#' * int(name[1]) + ' ' + self.children(node).strip() + ' {#' + node['id'] + '}\n\n'
        if name == 'p':
            return '\n\n' + self.children(node).strip() + '\n\n'
        if name in ('ul', 'ol'):
            lines = []
            for i, li in enumerate(node.find_all('li', recursive=False)):
                prefix = '- ' if name == 'ul' else str(i + int(node.get('start', 1))) + '. '
                text = self.children(li).strip()
                lines.append(prefix + text.replace('\n', '\n' + ' ' * len(prefix)))
            return '\n\n' + '\n'.join(lines) + '\n\n'
        if name == 'table':
            rows = []
            for row in node.find_all('tr'):
                cells = []
                for cell in row.find_all(['th', 'td'], recursive=False):
                    text = self.children(cell).strip().replace('|', '\\|')
                    text = re.sub(r'\n+', '<br>', text)
                    cells.append(text)
                rows.append('| ' + ' | '.join(cells) + ' |')
            if rows:
                n = len(node.find('tr').find_all(['th', 'td'], recursive=False))
                rows.insert(1, '| ' + ' | '.join(['---'] * n) + ' |')
            return '\n\n' + '\n'.join(rows) + '\n\n'
        if name == 'div':
            kind = next((x for x in node.get('class', []) if x in ('NOTE', 'TIP', 'WARNING', 'CAUTION', 'IMPORTANT')), None)
            if kind:
                first = node.find('p', recursive=False)
                title = first.get_text(' ', strip=True) if first else ''
                if first: first.decompose()
                body = re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', '\n\n', self.children(node).strip())
                return '\n\n> [!' + kind + ']\n> ' + body.replace('\n', '\n> ') + '\n\n'
        if name == 'blockquote':
            return '\n\n> ' + self.children(node).strip().replace('\n', '\n> ') + '\n\n'
        if name == 'sup':
            return '<sup>' + self.children(node) + '</sup>'
        if node.get('id') and name == 'span':
            return '<span id="' + node['id'] + '">' + self.children(node) + '</span>'
        return self.children(node)

    def convert(self, content):
        text = self.children(content)
        # Whitespace is normalized outside fences only; SQL and output stay exact.
        parts = re.split(r'(?ms)(^`{3,}[^\n]*\n.*?^`{3,}[ \t]*$)', text)
        return ''.join(x if i % 2 else re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', '\n\n', x) for i, x in enumerate(parts)).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    dest = ROOT / 'content/citus'
    if dest.exists():
        raise SystemExit('Refusing to overwrite maintained Citus content')
    routes = {'': '/citus/', 'index': '/citus/'}
    placements = {}
    for group, en, zh, desc_en, desc_zh, icon, slugs in GROUPS:
        for i, slug in enumerate(slugs):
            key = slug.split('/')[-1]
            name = '_index' if slug in ('reference', 'guides') else key
            placements[slug] = (group, name, (i + 1) * 10)
            routes[slug] = f'/citus/{group}/' + ('' if name == '_index' else name + '/')
    manifest = dict(component='citus', edition='Citus 14', snapshot_date='2026-11-07',
                    source_url=BASE+'?view='+VIEW, source_repository='https://github.com/MicrosoftDocs/azure-databases-docs',
                    preserved_repository='https://github.com/Kiranchandratrey/azure-databases-docs',
                    preserved_commit='ff9de504fdbe2b7aa9d06411e0f0472d39dc1f14', pages=[], assets=[])
    for slug, (group, name, weight) in placements.items():
        en, meta, title, enpath = page(source, 'en', slug)
        zh, zmeta, ztitle, zhpath = page(source, 'zh', slug)
        en_heads, zh_heads = [en.select('h2,h3,h4,h5,h6'), zh.select('h2,h3,h4,h5,h6')]
        assert len(en_heads) == len(zh_heads), f'Heading mismatch: {slug}'
        for a, b in zip(en_heads, zh_heads): b['id'] = a['id']
        en_codes, zh_codes = en.find_all('pre'), zh.find_all('pre')
        assert len(en_codes) == len(zh_codes), f'Code count mismatch: {slug}'
        for a, b in zip(en_codes, zh_codes): b.replace_with(BeautifulSoup(str(a), 'html.parser'))
        image_map = {}
        bundle = bool(en.find_all('img'))
        page_dir = dest/group/(name if name != '_index' else '') if bundle else dest/group
        filename = 'index' if bundle and name != '_index' else name
        for node in en.find_all('img'):
            raw = node['src']; absolute = urljoin(BASE+slug, raw)
            image_name = Path(urlsplit(raw).path).name
            frozen = source/'assets'/group/name/image_name
            frozen.parent.mkdir(parents=True, exist_ok=True)
            if not frozen.exists():
                with urlopen(Request(absolute,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r: frozen.write_bytes(r.read())
            target = page_dir/image_name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(frozen, target)
            image_map[raw] = image_name
            for zimg in zh.find_all('img'):
                if Path(urlsplit(zimg['src']).path).name == image_name: image_map[zimg['src']] = image_name
            manifest['assets'].append(dict(source=absolute,target=str(target.relative_to(ROOT)),bytes=target.stat().st_size,sha256=digest(target.read_bytes())))
        front = dict(title=title, description=meta.get('description',title), weight=weight,
                     type='docs', upstream_source='citus', upstream_link=BASE+slug+'?view='+VIEW,
                     upstream_ref=VIEW+'; '+meta.get('git_commit_id','')[:12])
        for lang, content, title_, meta_, input_path in [('en',en,title,meta,enpath),('zh',zh,ztitle,zmeta,zhpath)]:
            fm = dict(front)
            fm.update(title=title_, description=meta_.get('description',title_))
            if lang == 'zh':
                fm['translation_status'] = 'machine-draft'
            body = Converter(slug,routes,image_map,lang).convert(content)
            if lang == 'zh':
                body = '> [!CAUTION] 机器译稿，待英文校订\n> 本页暂存上游机器译稿，英文原文为准。\n\n' + body
            out = page_dir/(filename+('.zh' if lang=='zh' else '')+'.md')
            write(out,fm,body)
            manifest['pages'].append(dict(source_url=BASE.replace('en-us','zh-cn' if lang=='zh' else 'en-us')+slug+'?view='+VIEW,
                source_path=meta_.get('source_path','citus/'+slug+'.md'), source_commit=meta_.get('git_commit_id'),
                source_updated=meta_.get('updated_at'), language=lang, target=str(out.relative_to(ROOT)),
                route=('' if lang=='en' else '/zh')+routes[slug], source_html_sha256=digest(input_path.read_bytes()),
                source_markdown_sha256=digest((source/'markdown'/lang/(slug.replace('/','__')+'.md')).read_bytes()),
                heading_ids=[h['id'] for h in en_heads], code_sha256=[digest((x.get_text().rstrip('\n')+'\n').encode()) for x in en_codes],
                status='imported' if lang=='en' else 'machine-draft'))
        print(slug, flush=True)
    for group, title, ztitle, description, zdescription, icon, slugs in GROUPS:
        for lang in ('en','zh'):
            out = dest/group/('_index'+('.zh' if lang=='zh' else '')+'.md')
            if out.exists():
                text=out.read_text(); front,body=text[4:].split('\n---\n',1);fm=yaml.safe_load(front)
            else:fm,body={},''
            fm.update(title=ztitle if lang=='zh' else title, description=zdescription if lang=='zh' else description,
                weight=(1+[g[0] for g in GROUPS].index(group))*10,type='docs',icon='fa-solid fa-'+icon,
                upstream_source='citus',upstream_link=fm.get('upstream_link',BASE+'?view='+VIEW),section_index='list')
            write(out,fm,body)
    (ROOT/'data/imports/citus.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print('Imported',len(manifest['pages']),'pages;',len(manifest['assets']),'images')


if __name__ == '__main__':
    main()
