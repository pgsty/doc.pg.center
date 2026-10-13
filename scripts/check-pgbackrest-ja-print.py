#!/usr/bin/env python3
"""Compare Japanese per-page rendered body blocks with the pgBackRest print bundle.

Uses Python's standard library only. This helper reads an existing Hugo build and
never modifies repository or build files. Integrators can call check_print().
"""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from typing import Iterable

VOID = frozenset('area base br col embed hr img input link meta param source track wbr'.split())
BODY_TAGS = frozenset({'p', 'li', 'pre', 'td', 'th'})
BLOCK_TAGS = frozenset({'p', 'div', 'pre', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'blockquote'})
# Page chrome and generated metadata are outside the source Markdown body.
SKIP_CLASSES = frozenset({'lead', 'td-page-heading', 'td-article-meta', 'td-page-notice',
                          'td-section-index', 'td-page-end'})


class Node:
    def __init__(self, tag: str, attrs: dict[str, str | None] | None = None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children: list['Node | str'] = []

    @property
    def classes(self) -> set[str]:
        return set((self.attrs.get('class') or '').split())

    def walk(self) -> Iterable['Node']:
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def text(self, *, separate_blocks=False) -> str:
        parts = []
        for child in self.children:
            if isinstance(child, Node):
                value = child.text(separate_blocks=separate_blocks)
                if separate_blocks and child.tag in BLOCK_TAGS:
                    value = '\n' + value + '\n'
                parts.append(value)
            else:
                parts.append(child)
        return ''.join(parts)


class Document(HTMLParser):
    def __init__(self, html: str):
        super().__init__(convert_charrefs=True)
        self.root = Node('#document')
        self.stack = [self.root]
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, dict(attrs)))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for pos in range(len(self.stack) - 1, 0, -1):
            if self.stack[pos].tag == tag:
                del self.stack[pos:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def read_document(path: Path) -> Document:
    return Document(path.read_text(encoding='utf-8'))


def content_sections(document: Document) -> list[Node]:
    return [node for node in document.root.walk() if 'td-content' in node.classes]


def heading(section: Node) -> Node | None:
    return next((n for n in section.walk() if n.tag == 'h1'), None)


def generated_print_toc(node: Node) -> bool:
    """Recognize only the root print view's generated chapter navigation list."""
    if node.tag != 'ul':
        return False
    links = [n.attrs.get('href', '') for n in node.walk() if n.tag == 'a']
    return bool(links) and all(re.fullmatch(r'#pg-[0-9a-f]{32}', link or '') for link in links)


def body_blocks(section: Node, *, print_root=False) -> list[tuple[str, str]]:
    """Ordered p/li/pre/td/th signatures, excluding generated page metadata.

    Prose whitespace is collapsed because HTML minification may alter it. Code
    block whitespace is preserved after CRLF normalization. Nested selected
    elements are kept individually, so list/table structure remains observable.
    """
    result = []
    skip_root_toc = None
    if print_root:
        # The root print TOC is a direct child before the first source heading.
        for child in section.children:
            if not isinstance(child, Node):
                continue
            if re.fullmatch(r'h[2-6]', child.tag) or child.tag == 'hr':
                break
            if generated_print_toc(child):
                skip_root_toc = child
                break

    def visit(node: Node):
        if node is skip_root_toc or node.tag == 'header' or node.classes & SKIP_CLASSES:
            return
        if node is not section and 'td-content' in node.classes:
            return
        if node.tag in BODY_TAGS:
            value = node.text(separate_blocks=node.tag != 'pre').replace('\r\n', '\n').replace('\r', '\n')
            if node.tag != 'pre':
                value = re.sub(r'\s+', ' ', value).strip()
            result.append((node.tag, value))
        for child in node.children:
            if isinstance(child, Node):
                visit(child)

    visit(section)
    return result


def content_metadata(section: Node, *, print_title=False) -> dict:
    """Visible titles/leads and source images, separate from generated chrome."""
    normalize = lambda value: re.sub(r'\s+', ' ', value).strip()
    nodes = list(section.walk())
    headings = [(node.tag, normalize(node.text())) for node in nodes if re.fullmatch(r'h[1-6]', node.tag)]
    if print_title and headings:
        tag, text = headings[0]
        headings[0] = (tag, re.sub(r'^\d+(?:\.\d+)*\s+-\s+', '', text))
    return {
        'headings': headings,
        'leads': [normalize(node.text()) for node in nodes if 'lead' in node.classes],
        'images': [tuple(node.attrs.get(key, '') for key in ('src', 'alt', 'title', 'width', 'height')) for node in nodes if node.tag == 'img'],
    }


def route(source: Path, content_root: Path) -> str:
    rel = source.relative_to(content_root)
    logical = rel.parent if source.stem in {'index', '_index'} else rel.with_suffix('')
    return '/' + logical.as_posix().lower() + '/'


def check_print(build: Path, sources: Iterable[Path], content_root: Path,
                *, locale='ja', component='pgbackrest', compare_metadata=False) -> tuple[list[str], list[dict]]:
    """Return (errors, page_reports) for current English source paths."""
    sources = list(sources)
    bundle = build / locale / '_print' / 'docs' / component / 'index.html'
    sections = content_sections(read_document(bundle))
    indexed = {}
    roots = []
    errors = []
    for section in sections:
        title = heading(section)
        key = title.attrs.get('id') if title else None
        if key:
            if key in indexed:
                errors.append('duplicate print section ID: ' + key)
            indexed[key] = section
        else:
            roots.append(section)
    if len(roots) != 1:
        errors.append(f'expected exactly one root print section, found {len(roots)}')
    if len(sections) != len(sources):
        errors.append(f'print section count differs: expected {len(sources)}, actual {len(sections)}')
    used = set()
    reports = []
    for source in sources:
        page_route = route(source, content_root)
        is_root = page_route == f'/docs/{component}/'
        target_rel = source.with_suffix(f'.{locale}.md').relative_to(content_root).as_posix()
        section_id = 'pg-' + hashlib.md5(target_rel.encode()).hexdigest()
        printed = roots[0] if is_root and len(roots) == 1 else indexed.get(section_id)
        if printed is None:
            errors.append(f'{page_route}: missing print section {section_id}')
            continue
        used.add(id(printed))
        page_sections = content_sections(read_document(build / locale / page_route.lstrip('/') / 'index.html'))
        if len(page_sections) != 1:
            errors.append(f'{page_route}: expected one normal td-content section, found {len(page_sections)}')
            continue
        expected = body_blocks(page_sections[0])
        actual = body_blocks(printed, print_root=is_root)
        if compare_metadata and content_metadata(page_sections[0]) != content_metadata(printed, print_title=not is_root):
            errors.append(f'{page_route}: print headings, lead description or images differ from the normal page')
        report = {'route': page_route, 'print_section': section_id if not is_root else 'root',
                  'expected_blocks': len(expected), 'actual_blocks': len(actual), 'match': expected == actual}
        reports.append(report)
        if expected != actual:
            first = next((i for i, pair in enumerate(zip(expected, actual)) if pair[0] != pair[1]), min(len(expected), len(actual)))
            def sample(rows):
                return repr(rows[first])[:260] if first < len(rows) else '<missing>'
            errors.append(f'{page_route}: print body differs at block {first + 1}; expected {len(expected)} blocks, actual {len(actual)}; expected {sample(expected)}, actual {sample(actual)}')
    if len(used) != len(sections):
        errors.append(f'unmatched print sections: {len(sections) - len(used)}')
    return errors, reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rendered-dir', required=True, type=Path)
    parser.add_argument('--project-dir', type=Path, default=Path.cwd())
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    content = args.project_dir.resolve() / 'content'
    sources = sorted(p for p in (content / 'docs/pgbackrest').rglob('*.md')
                     if not re.search(r'\.[a-z]{2}(?:-[a-z0-9]+)?\.md$', p.name))
    try:
        errors, pages = check_print(args.rendered_dir, sources, content)
    except (OSError, ValueError) as exc:
        errors, pages = [str(exc)], []
    result = {'pages': pages, 'errors': errors}
    if args.report:
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for error in errors:
        print(error)
    print(f'Print body comparison: {len(pages)} pages; {sum(p["expected_blocks"] for p in pages)} blocks; {len(errors)} errors')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
