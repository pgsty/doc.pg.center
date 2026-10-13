"""PgBouncer source and rendered-output helpers using only the standard library.

Kept with the PgBouncer gate so its committed tests do not depend on unrelated
translation work in progress. Code fences, original diagnostics, metadata and
complete print bodies are checked independently of the semantic fingerprints.
"""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
import re
from typing import Iterable
from urllib.parse import urlsplit, urlunsplit

CONTENT = Path(__file__).resolve().parent.parent / "content"
TRANSLATABLE_FRONT_KEYS = {"title", "linkTitle", "description", "categories"}
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
HEADING_RE = re.compile(r"^(#{1,6})\s+.*?(?:\s+\{#[^}]+\})?\s*$")


def is_english(path: Path) -> bool:
    return path.suffix == ".md" and not re.search(
        r"\.[a-z]{2}(?:-[a-z0-9]+)?\.md$", path.name, flags=re.IGNORECASE
    )


def split_front_matter(document: str) -> tuple[str, str]:
    if not document.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    end = document.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML front matter")
    return document[4:end], document[end + 5 :]


def front_text(front: str, key: str) -> str | None:
    """Read the top-level text scalars used by search metadata.

    Hugo folds ``>`` descriptions before emitting JSON. Comparing the literal
    YAML indicator with that description rejects valid translated metadata.
    Whitespace is normalized at the comparison boundary, as in rendered HTML.
    """
    lines = front.splitlines()
    for index, line in enumerate(lines):
        match = re.match(rf"^{re.escape(key)}:[ \t]*(.*)$", line)
        if not match:
            continue
        value = match[1].strip()
        if value in {">", ">-", ">+", "|", "|-", "|+"}:
            body = []
            for following in lines[index + 1:]:
                if following.strip() and not following.startswith((" ", "\t")):
                    break
                body.append(following.strip())
            return " ".join(" ".join(body).split())
        if value.startswith('"'):
            return json.loads(value)
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1].replace("''", "'")
        return value
    return None


def fenced_blocks(body: str) -> tuple[list[str], str]:
    lines = body.splitlines(keepends=True)
    blocks: list[str] = []
    prose: list[str] = []
    current: list[str] = []
    marker = ""
    for line in lines:
        match = FENCE_RE.match(line)
        if marker:
            current.append(line)
            if line.lstrip().startswith(marker):
                blocks.append("".join(current))
                current = []
                marker = ""
            continue
        if match:
            marker = match.group(1)
            current = [line]
        else:
            prose.append(line)
    if marker:
        raise ValueError("unterminated code fence")
    return blocks, "".join(prose)


def blockquoted_fenced_blocks(body: str) -> list[str]:
    lines = body.splitlines(keepends=True)
    blocks: list[str] = []
    index = 0
    opening_re = re.compile(r"^\s*>+\s*(`{3,}|~{3,})")
    while index < len(lines):
        opening = opening_re.match(lines[index])
        if not opening:
            index += 1
            continue
        marker = opening.group(1)
        block = [lines[index]]
        index += 1
        closing_re = re.compile(rf"^\s*>+\s*{re.escape(marker)}\s*$")
        while index < len(lines):
            block.append(lines[index])
            if closing_re.match(lines[index].rstrip("\n")):
                index += 1
                break
            index += 1
        else:
            raise ValueError("unterminated blockquoted code fence")
        blocks.append("".join(block))
    return blocks


def headings(body: str) -> list[int]:
    _, prose = fenced_blocks(body)
    return [len(match.group(1)) for line in prose.splitlines() if (match := HEADING_RE.match(line))]


def front_aliases(front: str) -> list[str]:
    match = re.search(r"(?m)^aliases:\s*\[([^]]*)\]", front)
    if match:
        return [value.strip().strip("\"'") for value in match[1].split(",") if value.strip()]
    match = re.search(r"(?m)^aliases:\s*\n((?:[ \t]+.*\n?)+)", front)
    return re.findall(r"(?m)^\s*-\s*([^\s#]+)", match[1]) if match else []


def llms_entries(text: str) -> list[tuple[str, str]]:
    """Read complete sections, so a source marker cannot hide a missing body."""
    markers = list(re.finditer(r"(?m)^={16}\nSource: ([^\n]+)\n={16}\n", text))
    return [(match[1], text[match.end():markers[index + 1].start() if index + 1 < len(markers) else len(text)].strip())
            for index, match in enumerate(markers)]


def canonical_target(target: str, source: Path) -> str:
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
        return target
    base = "/" + source.parent.relative_to(CONTENT).as_posix()
    path = posixpath.normpath(base + "/" + parsed.path)
    if parsed.path.endswith("/"):
        path += "/"
    return urlunsplit(("", "", path, parsed.query, parsed.fragment))


def inline_literals(body: str) -> list[str]:
    _, prose = fenced_blocks(body)
    prose = re.sub(r"<!--.*?-->", "", prose, flags=re.S)
    return INLINE_CODE_RE.findall(prose)


def diagnostic_errors(source_body: str, target_body: str, diagnostics: list[str]) -> list[str]:
    english = " ".join(source_body.replace("\\_", "_").split())
    translated = " ".join(target_body.replace("\\_", "_").split())
    errors = []
    for literal in diagnostics:
        literal = " ".join(literal.split())
        if not literal or not english.count(literal) or translated.count(literal) != english.count(literal):
            errors.append(f"original diagnostic changed: {literal!r}")
    return errors


def placeholder_errors(source_body: str, target_body: str, diagnostics: list[str]) -> list[str]:
    pattern = re.compile(r"__PGSQL_|⟦P\d+⟧|\b(?:TODO|FIXME|TRANSLATE_ME)\b")
    _, prose = fenced_blocks(target_body)
    lint = " ".join(re.sub(r"<!--.*?-->", "", prose, flags=re.S).split())
    english = " ".join(source_body.split())
    for literal in diagnostics:
        literal = " ".join(literal.split())
        if pattern.search(literal) and english.count(literal) and lint.count(literal) == english.count(literal):
            lint = lint.replace(literal, "")
    return ["unresolved translation placeholder"] if pattern.search(lint) else []


class RenderedContent(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.headings, self.code, self.sidebar, self.pager = [], [], [], []
        self.languages, self.canonical, self.refresh, self.html_languages = [], [], [], []
        self.alternates = {}
        self.in_pre = False
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.html_languages.append(attrs.get("lang", ""))
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href", ""))
        if tag == "link" and attrs.get("rel") == "alternate":
            self.alternates[attrs.get("hreflang", "")] = attrs.get("href", "")
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.refresh.append(re.split(r"url=", attrs.get("content", ""), flags=re.I)[-1])
        if re.fullmatch(r"h[1-6]", tag) and attrs.get("id"):
            self.headings.append((tag, attrs["id"]))
        classes, href = attrs.get("class", "").split(), attrs.get("href", "")
        if tag == "a" and "td-shell-tree__link" in classes and "/docs/" in href:
            self.sidebar.append(href)
        for direction in ("prev", "next"):
            if f"td-pager__link--{direction}" in classes:
                self.pager.append((direction, href))
        if "td-language-selector__item" in classes:
            self.languages.append(href)
        if tag == "pre":
            self.in_pre = True
            self.code.append("")

    def handle_endtag(self, tag):
        if tag == "pre":
            self.in_pre = False

    def handle_data(self, data):
        if self.in_pre:
            self.code[-1] += data



VOID = frozenset('area base br col embed hr img input link meta param source track wbr'.split())


BODY_TAGS = frozenset({'p', 'li', 'pre', 'td', 'th'})


BLOCK_TAGS = frozenset({'p', 'div', 'pre', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'blockquote'})


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
                *, locale='zh', component='pgbouncer', compare_metadata=False) -> tuple[list[str], list[dict]]:
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
