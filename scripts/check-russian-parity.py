#!/usr/bin/env python3
"""Validate English/Russian source parity for every documentation page.

The Russian edition is translated prose, but executable examples and the
Markdown/link structure must remain derived from the English source.  This
check deliberately runs on source files so a broken translation fails before
Hugo renders it.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import posixpath
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, unquote

from russian_routes import transform_route_text

from translation_sources import describe_sources, read_source
from patroni_parity import reviewed_delta as patroni_reviewed_delta
from translation_fences import (
    load_manifest, prose_for_lint, translated_inline_labels,
    validate_fences, validate_literal_blocks,
)


PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content"
COMPONENTS = ("patroni", "pgbackrest", "pgbouncer", "pgbadger", "haproxy", "etcd")
TRANSLATABLE_FRONT_KEYS = {"title", "linkTitle", "description", "categories"}
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
REFERENCE_DEF_RE = re.compile(r"^\s*\[[^]]+\]:\s+\S+")
INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
SHORTCODE_RE = re.compile(r"\{\{[%<].*?[>%]\}\}")
HTML_TAG_RE = re.compile(r"</?[A-Za-z][^>\n]*>")
EXPLICIT_ANCHOR_RE = re.compile(
    r"\{#([A-Za-z0-9_.:-]+)\}|<a\s+(?:id|name)=[\"']([^\"']+)[\"'][^>]*>"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+.*?(?:\s+\{#[^}]+\})?\s*$")
NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:v|V)?\d+(?:\.\d+)*(?:[-+][A-Za-z0-9.-]+)?"
    r"(?:\s?(?:ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB|%))?"
    r"(?![A-Za-z0-9])"
)
ENGLISH_WORD_RE = re.compile(r"\b[a-z]{2,}\b")
CYRILLIC_RE = re.compile(r"[\u0400-\u052f]")
ENGLISH_FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "for", "on", "with",
    "by", "from", "as", "is", "are", "be", "this", "that", "it", "its", "can",
    "will", "may", "should", "must", "not", "if", "when", "at", "into", "which",
    "their", "they", "them", "than", "has", "have", "had", "was", "were", "would",
}


def is_english(path: Path) -> bool:
    return path.suffix == ".md" and not re.search(
        r"\.[a-z]{2}(?:-[a-z0-9]+)?\.md$", path.name, flags=re.IGNORECASE
    )


def russian_path(source: Path) -> Path:
    return source.with_name(source.name.removesuffix(".md") + ".ru.md")


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


def normalized_front(front: str) -> str:
    lines: list[str] = []
    scalar = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z][A-Za-z0-9_]*):(?P<rest>.*)$")
    source_lines = front.splitlines()
    index = 0
    while index < len(source_lines):
        line = source_lines[index]
        match = scalar.match(line)
        if match and match.group("key") in TRANSLATABLE_FRONT_KEYS:
            lines.append(f'{match.group("indent")}{match.group("key")}: <translated>')
            if match.group("rest").strip() in {">", "|", ">-", "|-", ">+", "|+"}:
                parent_indent = len(match.group("indent").expandtabs(2))
                index += 1
                while index < len(source_lines):
                    candidate = source_lines[index]
                    indent = len(candidate) - len(candidate.lstrip(" \t"))
                    if candidate.strip() and indent <= parent_indent:
                        break
                    index += 1
                continue
        else:
            lines.append(line)
        index += 1
    return "\n".join(lines)


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


def normalized_target(target: str) -> str:
    return transform_route_text(target, ("docs", "search", "attribution", "patroni"))


def canonical_target(target: str, source: Path) -> str:
    value = normalized_target(target)
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
        return value
    base = "/" + source.parent.relative_to(CONTENT).as_posix()
    path = posixpath.normpath(base + "/" + parsed.path)
    if parsed.path.endswith("/"):
        path += "/"
    return urlunsplit(("", "", path, parsed.query, parsed.fragment))


def link_targets(body: str, source: Path) -> list[str]:
    _, prose = fenced_blocks(body)
    prose = re.sub(r"<!--.*?-->", "", prose, flags=re.DOTALL)
    targets: list[str] = []
    targets.extend(re.findall(r"(?<=[^!])\]\(([^)\n]+)\)", " " + prose))
    targets.extend(re.findall(r"!\[[^]]*\]\(([^)\n]+)\)", prose))
    targets.extend(
        match.group(1)
        for line in prose.splitlines()
        if not re.match(r"^\s*\[\^", line)
        and (match := re.match(r"^\s*\[[^]]+\]:\s+(\S+)", line))
    )
    targets.extend(re.findall(r'\b(?:href|src|link)=["\']([^"\']+)["\']', prose))
    return [canonical_target(value, source) for value in targets]


def image_targets(body: str) -> list[str]:
    _, prose = fenced_blocks(body)
    targets = re.findall(r"!\[[^]]*\]\(([^)\n]+)\)", prose)
    targets.extend(re.findall(r'\b(?:src|poster)=["\']([^"\']+)["\']', prose))
    return targets


def headings(body: str) -> list[int]:
    _, prose = fenced_blocks(body)
    return [len(match.group(1)) for line in prose.splitlines() if (match := HEADING_RE.match(line))]


def explicit_anchors(body: str) -> list[str]:
    _, prose = fenced_blocks(body)
    return [left or right for left, right in EXPLICIT_ANCHOR_RE.findall(prose)]


def protected_inline(body: str) -> tuple[list[str], list[str], list[str], list[str]]:
    _, prose = fenced_blocks(body)
    comments = re.findall(r"<!--.*?-->", prose, flags=re.DOTALL)
    prose_without_comments = re.sub(r"<!--.*?-->", "", prose, flags=re.DOTALL)
    inline = INLINE_CODE_RE.findall(prose_without_comments)
    # Angle-bracket arguments inside backticks are code, not HTML. Their
    # exact values and multiplicities are protected by the inline-code check;
    # Russian prose may legitimately mention them in a different order.
    markup = INLINE_CODE_RE.sub("", prose_without_comments)
    shortcodes = SHORTCODE_RE.findall(markup)
    tags = []
    for tag in HTML_TAG_RE.findall(markup):
        tag = normalized_target(tag)
        tag = re.sub(
            r"\s+(alt|title|aria-label)=([\"'])[^\"']*\2",
            r" \1=<translated>",
            tag,
            flags=re.IGNORECASE,
        )
        tags.append(tag)
    references = [
        normalized_target(line)
        for line in markup.splitlines()
        if REFERENCE_DEF_RE.match(line) and not re.match(r"^\s*\[\^", line)
    ]
    return comments, inline, shortcodes, tags + references


def numeric_tokens(body: str) -> Counter[str]:
    blocks, prose = fenced_blocks(body)
    del blocks
    prose = re.sub(r"<!--.*?-->", "", prose, flags=re.DOTALL)
    prose = INLINE_CODE_RE.sub("", prose)
    prose = re.sub(r"https?://\S+", "", prose)
    prose = re.sub(r"\{#[^}]+\}", "", prose)
    prose = re.sub(r"\bдвух(?=байт)", "2 ", prose, flags=re.IGNORECASE)
    # “3rd party” is naturally spelled out in Russian, not written “3-й”.
    prose = re.sub(r"\bтретьей(?=\s+стороны\b)", "3", prose, flags=re.IGNORECASE)
    prose = re.sub(
        r"(?<=\d)[,\u00a0\u202f ](?=\d{3}(?:\D|$))",
        "",
        prose,
    )
    # Russian typography legitimately uses a decimal comma and localized unit
    # names.  Compare the digit facts themselves; protected literals, code,
    # and URLs are checked separately.
    return Counter(
        token.replace(",", ".")
        for token in re.findall(r"(?<!\d)\d+(?:[.,]\d+)*(?!\d)", prose)
    )


def residual_english(body: str) -> list[tuple[int, str]]:
    _, prose = fenced_blocks(body)
    prose = re.sub(r"<!--.*?-->", "", prose, flags=re.DOTALL)
    problems: list[tuple[int, str]] = []
    for number, line in enumerate(prose.splitlines(), 1):
        stripped = line.strip()
        if (
            not stripped
            or line.startswith(("    ", "\t"))
            or REFERENCE_DEF_RE.match(stripped)
            or stripped.startswith("<pre")
        ):
            continue
        candidate = INLINE_CODE_RE.sub("", stripped)
        candidate = re.sub(r"https?://\S+", "", candidate)
        candidate = HTML_TAG_RE.sub("", candidate)
        candidate = SHORTCODE_RE.sub("", candidate)
        candidate = re.sub(r"\{#[^}]+\}", "", candidate)
        if candidate.startswith(
            (
                "Permission to use",
                "Redistribution and use",
                "IN NO EVENT",
                "Darold SPECIFICALLY DISCLAIMS",
                "THE SOFTWARE IS PROVIDED",
                "THIS SOFTWARE IS PROVIDED",
            )
        ):
            continue
        words = ENGLISH_WORD_RE.findall(candidate.lower())
        function_words = sum(word in ENGLISH_FUNCTION_WORDS for word in words)
        cyrillic = len(CYRILLIC_RE.findall(candidate))
        if len(words) >= 10 and function_words >= 4 and cyrillic < 5:
            problems.append((number, line[:240]))
    return problems


def compare_pair(source: Path, target: Path, current_source: bool = False) -> list[str]:
    errors: list[str] = []
    label = source.relative_to(PROJECT)
    try:
        source_text, _ = read_source(source, "ru", current=current_source)
        target_text = target.read_text(encoding="utf-8")
        source_front, source_body = split_front_matter(source_text)
        target_front, target_body = split_front_matter(target_text)
        source_blocks, _ = fenced_blocks(source_body)
        target_blocks, _ = fenced_blocks(target_body)
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"{label}: {exc}"]

    source_comments, source_inline, source_shortcodes, source_markup = protected_inline(
        source_body
    )
    target_comments, target_inline, target_shortcodes, target_markup = protected_inline(
        target_body
    )
    checks = (
        ("non-translatable front matter", normalized_front(source_front), normalized_front(target_front)),
        (
            "blockquoted fenced code blocks",
            blockquoted_fenced_blocks(source_body),
            blockquoted_fenced_blocks(target_body),
        ),
        ("heading levels", headings(source_body), headings(target_body)),
        (
            "footnote identifiers",
            re.findall(r"\[\^[^]\n]+\]", source_body),
            re.findall(r"\[\^[^]\n]+\]", target_body),
        ),
        ("HTML comments", source_comments, target_comments),
        ("shortcodes", source_shortcodes, target_shortcodes),
        ("HTML/reference structure", source_markup, target_markup),
        ("image targets", image_targets(source_body), image_targets(target_body)),
        ("link targets", link_targets(source_body, source), link_targets(target_body, source)),
        ("numeric literals", numeric_tokens(source_body), numeric_tokens(target_body)),
    )
    for name, expected, actual in checks:
        if expected != actual:
            errors.append(f"{label}: {name} changed")
    # Imported HAProxy text fences also contain parameter descriptions and
    # explanatory tables. Only individually reviewed, hash-pinned pairs may
    # differ; commands, output and every unregistered fence remain immutable.
    validate_fences(source, source_blocks, target_blocks, errors, language="ru")
    validate_literal_blocks(source, target_text, errors, language="ru")
    validate_indented_explanations(source, source_body, target_body, errors)

    missing_inline = translated_inline_labels(source, Counter(source_inline), "ru") - Counter(target_inline)
    if missing_inline:
        errors.append(f"{label}: protected inline code missing: {list(missing_inline)[:8]}")

    source_anchors = explicit_anchors(source_body)
    target_anchors = explicit_anchors(target_body)
    missing_anchors = [anchor for anchor in source_anchors if anchor not in target_anchors]
    if missing_anchors:
        errors.append(f"{label}: explicit anchors missing in Russian: {missing_anchors[:8]}")

    untranslated = residual_english(prose_for_lint(source, target_body, language="ru"))
    for number, line in untranslated[:5]:
        errors.append(f"{label}: probable untranslated English near body line {number}: {line}")
    if len(untranslated) > 5:
        errors.append(f"{label}: {len(untranslated) - 5} more probable untranslated lines")
    return errors


def strict_structure(source: Path, target: Path, current_source: bool) -> list[str]:
    """Extra whole-page checks for a collection being fully brought up to date."""
    source_text, _ = read_source(source, "ru", current=current_source)
    _, source_body = split_front_matter(source_text)
    target_text = target.read_text(encoding="utf-8")
    _, target_body = split_front_matter(target_text)

    def signature(body: str) -> tuple:
        _, prose = fenced_blocks(body)
        lists = []
        tables = []
        quotes = []
        previous_blank = True
        ordered_indents = set()
        for line in prose.splitlines():
            match = re.match(r"^(\s*)([-+*]|\d+[.)])\s+", line)
            if match:
                indent, marker = len(match[1].expandtabs(4)), match[2]
                # An ordered list can interrupt a paragraph only at 1.
                # Wrapped prose such as "RFC\n4492)" or "early\n2015."
                # is not an additional Markdown list item.
                if marker in "-+*" or previous_blank or marker[:-1] == "1" or indent in ordered_indents:
                    lists.append((indent, marker))
                    if marker not in "-+*":
                        ordered_indents.add(indent)
            elif line.strip() and not line.startswith((" ", "\t")):
                ordered_indents.clear()
            if line.lstrip().startswith("|"):
                tables.append(len(re.findall(r"(?<!\\)\|", line)))
            match = re.match(r"^\s*(>+)\s*(\[![A-Z]+\])?", line)
            if match:
                quotes.append((len(match[1]), match[2]))
            previous_blank = not line.strip()
        return lists, tables, quotes, Counter(INLINE_CODE_RE.findall(prose))

    errors = []
    label = source.relative_to(PROJECT)
    source_signature = list(signature(source_body))
    source_signature[-1] = translated_inline_labels(source, source_signature[-1], "ru")
    for name, expected, actual in zip(
        ("list markers/nesting", "table shape", "blockquote/admonition structure", "exact inline literals"),
        source_signature, signature(target_body),
    ):
        if name == 'exact inline literals' and patroni_reviewed_delta(
            source, source_text, target_text, 'ru', 'inline_literal_variant', expected, actual
        ):
            continue
        if expected != actual:
            errors.append(f"{label}: {name} changed")
    _, prose = fenced_blocks(target_body)
    _, lint_prose = fenced_blocks(prose_for_lint(source, target_body, language="ru"))
    if re.search(r"__PGSQL_|⟦P\d+⟧|\b(?:TODO|FIXME|TRANSLATE_ME)\b", lint_prose):
        errors.append(f"{label}: unresolved translation placeholder")
    component = source.relative_to(CONTENT).parts[1] if source.is_relative_to(CONTENT / "docs") else None
    if component and re.search(rf"\]\(/docs/{re.escape(component)}/[^)]*?(?:/|/#[^)]*)\)", prose):
        errors.append(f"{label}: component link still uses the English route")
    return errors


class RenderedContent(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.headings: list[tuple[str, str]] = []
        self.code: list[str] = []
        self.in_pre = False
        self.sidebar: list[str] = []
        self.pager: list[tuple[str, str]] = []
        self.languages: list[str] = []
        self.canonical: list[str] = []
        self.refresh: list[str] = []
        self.html_languages: list[str] = []
        self.alternates: dict[str, str] = {}
        self.ids: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.link_contexts: list[tuple[str, str, dict[str, str]]] = []
        self.link_attributes: list[dict[str, str]] = []
        self.assets: list[str] = []
        self._translation_notices: list[bool] = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div":
            self._translation_notices.append("td-page-meta__translation" in attrs.get("class", "").split())
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if attrs.get("name"):
            self.ids.append(attrs["name"])
        if tag == "html":
            self.html_languages.append(attrs.get("lang", ""))
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href", ""))
        if tag == "link" and attrs.get("rel") == "alternate":
            self.alternates[attrs.get("hreflang", "")] = attrs.get("href", "")
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.refresh.append(re.split(r"url=", attrs.get("content", ""), flags=re.I)[-1])
        if tag in {"a", "link"} and attrs.get("href") is not None:
            self.links.append(("href", attrs["href"]))
            context = dict(attrs)
            context.pop("_translation_notice", None)
            if tag == "a" and any(self._translation_notices):
                context["_translation_notice"] = "true"
            self.link_contexts.append((tag, "href", context))
        if tag == "a":
            self.link_attributes.append(attrs)
        if tag in {"img", "script", "iframe", "source"} and attrs.get("src"):
            self.links.append(("src", attrs["src"]))
            self.link_contexts.append((tag, "src", attrs))
            self.assets.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.assets.append(attrs.get("href", ""))
        if re.fullmatch(r"h[1-6]", tag) and attrs.get("id"):
            self.headings.append((tag, attrs["id"]))
        classes = attrs.get("class", "").split()
        href = attrs.get("href", "")
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
        if tag == "div" and self._translation_notices:
            self._translation_notices.pop()
        if tag == "pre":
            self.in_pre = False

    def handle_data(self, data):
        if self.in_pre:
            self.code[-1] += data


def indented_fragments(body: str, *, split_at_fences: bool = False) -> list[str]:
    """Find indented text candidates; rendered <pre> checks distinguish code.

    HAProxy's import also indents a few explanatory paragraphs. Their exact
    hashes are reviewed explicitly, just like explanatory text fences.
    """
    blocks, _ = fenced_blocks(body)
    for block in blocks:
        boundary = "\nFENCED_BLOCK_BOUNDARY\n" if split_at_fences else "\n"
        body = body.replace(block, boundary, 1)
    chunks = []
    current = []
    for line in body.splitlines():
        if line.startswith("    "):
            current.append(line[4:])
        elif not line.strip() and current:
            current.append("")
        else:
            if current:
                chunks.append("\n".join(current).rstrip("\n"))
                current = []
    if current:
        chunks.append("\n".join(current).rstrip("\n"))
    return chunks


def text_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_indented_explanations(source: Path, english: str, russian: str, errors: list[str]) -> set[tuple[str, str]]:
    entries = load_manifest(source, "ru").get("indented_prose", [])
    en_chunks = {text_digest(value): value for value in indented_fragments(english)}
    ru_chunks = {text_digest(value): value for value in indented_fragments(russian)}
    reviewed = set()
    for entry in entries:
        en = en_chunks.get(entry.get("source_sha256"))
        ru = ru_chunks.get(entry.get("target_sha256"))
        if en is None or ru is None or not entry.get("reason"):
            errors.append(f"{source.relative_to(PROJECT)}: stale or unexplained indented-prose review")
            continue
        if Counter(re.findall(r"\d+(?:[.,]\d+)*", en)) != Counter(re.findall(r"\d+(?:[.,]\d+)*", ru)):
            errors.append(f"{source.relative_to(PROJECT)}: numeric facts changed in indented explanation")
        for literal in entry.get("protected_literals", []):
            if not literal or not en.count(literal) or en.count(literal) != ru.count(literal):
                errors.append(f"{source.relative_to(PROJECT)}: literal changed in indented explanation: {literal!r}")
        for line in entry.get("protected_lines", []):
            if line not in en.splitlines() or en.splitlines().count(line) != ru.splitlines().count(line):
                errors.append(f"{source.relative_to(PROJECT)}: output changed in indented explanation: {line!r}")
        reviewed.add((en, ru))
    return reviewed


def reviewed_rendered_fences(source: Path, target: Path) -> set[tuple[str, str]]:
    """Exact permitted <pre> differences, validated separately at source level."""
    entries = load_manifest(source, "ru").get("fences", [])
    source_body = split_front_matter(source.read_text(encoding="utf-8"))[1]
    target_body = split_front_matter(target.read_text(encoding="utf-8"))[1]
    source_blocks, _ = fenced_blocks(source_body)
    target_blocks, _ = fenced_blocks(target_body)
    review_errors = []
    validate_fences(source, source_blocks, target_blocks, review_errors, language="ru")
    result = validate_indented_explanations(source, source_body, target_body, review_errors)
    if review_errors:
        return set()
    # The source audit historically joins indented prose across a removed
    # fence. Hugo renders a separate <pre> on each side. Admit only exact
    # segments belonging to the same already validated source/target pair.
    source_indented = indented_fragments(source_body, split_at_fences=True)
    target_indented = indented_fragments(target_body, split_at_fences=True)
    if len(source_indented) == len(target_indented):
        validated_parents = set(result)
        for en, ru in zip(source_indented, target_indented):
            if any(en in parent_en and ru in parent_ru for parent_en, parent_ru in validated_parents):
                result.add((en, ru))
    for entry in entries:
        index = entry["index"] - 1
        if 0 <= index < min(len(source_blocks), len(target_blocks)):
            contents = lambda block: "".join(block.splitlines(keepends=True)[1:-1]).rstrip("\n")
            result.add((contents(source_blocks[index]), contents(target_blocks[index])))
    return result


def rendered_code_matches(english: list[str], russian: list[str], reviewed: set[tuple[str, str]]) -> bool:
    return len(english) == len(russian) and all(
        en == ru or (en.rstrip("\n"), ru.rstrip("\n")) in reviewed
        for en, ru in zip(english, russian)
    )


def compare_rendered(source: Path, target: Path, root: Path) -> list[str]:
    if source.name.startswith("_div_"):
        return []
    route = logical_path(source)
    label = source.relative_to(PROJECT)
    try:
        english = RenderedContent(root / route / "index.html")
        russian = RenderedContent(root / "ru" / route / "index.html")
    except OSError as exc:
        return [f"{label}: {exc}"]
    errors = []
    url = "/" + route.as_posix().lower() + "/"
    localized = "/ru" + url
    if russian.canonical != ["https://doc.pg.center" + localized]:
        errors.append(f"{label}: Russian canonical route changed")
    if russian.html_languages != ["ru-RU"]:
        errors.append(f"{label}: Russian HTML language changed")
    if russian.alternates.get("en-US") != "https://doc.pg.center" + url:
        errors.append(f"{label}: English alternate is not the same page")
    if english.alternates.get("ru-RU") != "https://doc.pg.center" + localized:
        errors.append(f"{label}: English page lacks the same-page Russian alternate")
    source_front, _ = split_front_matter(source.read_text(encoding="utf-8"))
    for alias in front_aliases(source_front):
        alias_path = root / "ru" / alias.lstrip("/") / "index.html"
        try:
            redirected = RenderedContent(alias_path)
            if redirected.canonical != russian.canonical or redirected.refresh != russian.canonical:
                errors.append(f"{label}: legacy alias does not redirect to the Russian canonical: {alias}")
        except OSError:
            errors.append(f"{label}: missing Russian alias: {alias}")
    if english.headings != russian.headings:
        errors.append(f"{label}: rendered heading sequence/English IDs changed")
    # Rendered <pre> includes fenced AND indented code and raw HTML output.
    if not rendered_code_matches(english.code, russian.code, reviewed_rendered_fences(source, target)):
        errors.append(f"{label}: rendered code/output changed")
    _, target_body = split_front_matter(target.read_text(encoding="utf-8"))
    source_ids = [identifier for _, identifier in english.headings]
    target_ids = heading_anchor_ids(target_body)
    if source_ids != target_ids:
        errors.append(f"{label}: source headings must explicitly retain every rendered English ID")
    return errors


def front_aliases(front: str) -> list[str]:
    match = re.search(r"(?m)^aliases:\s*\[([^]]*)\]", front)
    if match:
        return [value.strip().strip("\"'") for value in match[1].split(",") if value.strip()]
    match = re.search(r"(?m)^aliases:\s*\n((?:[ \t]+.*\n?)+)", front)
    return re.findall(r"(?m)^\s*-\s*([^\s#]+)", match[1]) if match else []


def load_check_helper(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def logical_path(source: Path) -> Path:
    """Both branch (_index) and leaf (index) bundles use their parent route."""
    relative = source.relative_to(CONTENT)
    route = relative.parent if source.stem in {"_index", "index"} else relative.with_suffix("")
    return Path(route.as_posix().lower())


def heading_anchor_ids(body: str) -> list[str | None]:
    # Use the shared Markdown parser so Setext headings receive the same
    # explicit-ID requirement as ATX headings.
    parser = load_check_helper("russian_markdown_headings", "check-german-parity.py")
    return [heading.anchor for heading in parser.heading_rows(body)]


def weighted_tree(node: dict, weights: dict[str, int]) -> tuple:
    """Compare hierarchy while permitting translated title order at weight ties."""
    children = node.get("children", [])
    ordered_weights = [weights[child["id"]] for child in children]
    assert ordered_weights == sorted(ordered_weights), "navigation sibling weights are not ordered"
    return node["id"], tuple(sorted((weighted_tree(child, weights) for child in children), key=lambda item: item[0]))


def llms_entries(text: str) -> list[tuple[str, str]]:
    """Read complete sections, so a source marker cannot hide a missing body."""
    markers = list(re.finditer(r"(?m)^={16}\nSource: ([^\n]+)\n={16}\n", text))
    return [(match[1], text[match.end():markers[index + 1].start() if index + 1 < len(markers) else len(text)].strip())
            for index, match in enumerate(markers)]


def check_full_agent_outputs(root: Path, ordered_nodes: list[dict]) -> list[str]:
    component_route = ordered_nodes[0]["id"]
    llms = llms_entries((root / "ru" / component_route.lstrip("/") / "llms-full.txt").read_text(encoding="utf-8"))
    expected = [("https://doc.pg.center/ru" + node["id"] + "index.md",
                 (root / "ru" / node["id"].lstrip("/") / "index.md").read_text(encoding="utf-8").strip())
                for node in ordered_nodes]
    errors = []
    if [item[0] for item in llms] != [item[0] for item in expected]:
        errors.append("LLMS section order, duplicate entries or page coverage differs from navigation.json")
    for (actual_url, actual_body), (expected_url, expected_body) in zip(llms, expected):
        if actual_url == expected_url and actual_body != expected_body:
            errors.append(f"incomplete or changed LLMS Markdown body: {expected_url}")
    return errors


def check_semantic_review(component: str, sources: list[Path]) -> list[str]:
    """Bind the completed HAProxy review to the exact delivered source files."""
    if component != "haproxy":
        return []
    path = PROJECT / "data/translation-audits/haproxy-ru.json"
    try:
        audit = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"haproxy: completed page-level semantic review unavailable: {exc}"]
    expected = {source.relative_to(PROJECT).as_posix(): source for source in sources}
    rows = audit.get("pages", [])
    actual = [row.get("source") for row in rows]
    errors = []
    if Counter(actual) != Counter(expected.keys()):
        errors.append("haproxy: semantic review must cover every current page and divider exactly once")
    for row in rows:
        source = expected.get(row.get("source"))
        if source is None:
            continue
        target = russian_path(source)
        if not target.is_file():
            continue
        if row.get("source_sha256") != hashlib.sha256(source.read_bytes()).hexdigest():
            errors.append(f"{row['source']}: semantic review source hash is stale")
        if row.get("target_sha256") != hashlib.sha256(target.read_bytes()).hexdigest():
            errors.append(f"{row['source']}: semantic review target hash is stale")
        review = row.get("semantic_review", {})
        if row.get("change") not in {"added", "corrected", "unchanged", "divider"}:
            errors.append(f"{row['source']}: semantic review change classification missing or invalid")
        if review.get("status") != "complete" or not review.get("method") or not review.get("note"):
            errors.append(f"{row['source']}: complete semantic review method/conclusion missing")
        if row.get("change") in {"added", "corrected"} and review.get("separate_review") != "complete":
            errors.append(f"{row['source']}: separate review of added/changed prose missing")
    return errors


def check_collection_links(component: str, root: Path, pages: list[Path]) -> list[str]:
    helper = load_check_helper("russian_local_links", "check-local-links.py")
    parsed = {}
    errors = []
    root = root.resolve()
    for page in pages:
        page = page.resolve()
        document = RenderedContent(page)
        canonical_path = urlsplit(document.canonical[0]).path if document.canonical else ""
        english_path = canonical_path.removeprefix("/ru") if canonical_path.startswith(f"/ru/docs/{component}/") else ""
        for tag, attribute, attrs in document.link_contexts:
            raw = attrs[attribute]
            destination, fragment = helper.resolve_target(root, page, raw)
            if destination is None:
                continue
            if not destination.is_relative_to(root) or not destination.is_file():
                errors.append(f"{page.relative_to(root)}: missing/escaping {attribute}={raw!r}")
                continue
            path = urlsplit(raw).path
            resolved_path = destination.relative_to(root).as_posix()
            if resolved_path.startswith(f"docs/{component}/") and destination.suffix in {".html", ".md"}:
                # Same-page language controls, alternate metadata and the
                # theme's translation-source notice may point to English. An
                # ordinary prose link is still a component fallback, even if
                # a real switch or source notice shares its URL.
                classes = set(attrs.get("class", "").split())
                same_page = (path == english_path and not urlsplit(raw).fragment
                             and not urlsplit(raw).query)
                is_switch = same_page and attrs.get("hreflang") == "en-US" and (
                    (tag == "link" and attrs.get("rel") == "alternate") or
                    (tag == "a" and bool(classes & {
                        "td-language-selector__item", "td-language-selector__trigger"})))
                is_source_notice = same_page and tag == "a" and attrs.get("_translation_notice") == "true"
                if not (is_switch or is_source_notice):
                    errors.append(f"{page.relative_to(root)}: component English fallback: {raw}")
            if raw in document.assets and resolved_path.startswith("ru/") and not resolved_path.startswith("ru/docs/"):
                errors.append(f"{page.relative_to(root)}: shared asset acquired a locale prefix: {raw}")
            if fragment and destination.suffix == ".html" and "third_party" not in destination.parts:
                if destination not in parsed:
                    parsed[destination] = helper.load_document(destination)
                anchors = parsed[destination].anchors
                print_fragment = "_print" in destination.parts and any(a.endswith("--" + fragment) for a in anchors)
                if fragment not in anchors and not print_fragment:
                    errors.append(f"{page.relative_to(root)}: missing fragment #{unquote(fragment)}: {raw}")
    return errors


def compare_collection_outputs(component: str, root: Path) -> list[str]:
    """Verify full navigation and alternate outputs for a complete collection."""
    prefix = f"/docs/{component}/"

    def nodes(language: str) -> list[dict]:
        path = root / language / "navigation.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        result = []

        def walk(node):
            if node.get("id", "").startswith(prefix):
                result.append(node)
            for child in node.get("children", []):
                walk(child)

        walk(payload["root"])
        return result

    errors = []
    try:
        english, russian = nodes(""), nodes("ru")
        assert english, "English navigation collection missing"
        expected_routes = set()
        for source in (CONTENT / "docs" / component).rglob("*.md"):
            if not is_english(source) or source.name.startswith("_div_"):
                continue
            route = logical_path(source)
            expected_routes.add("/" + route.as_posix().lower() + "/")
        assert len(english) == len(expected_routes) and {n["id"] for n in english} == expected_routes, "navigation does not cover every English logical page exactly once"
        if component != "etcd":
            assert [n["id"] for n in english] == [n["id"] for n in russian], "navigation.json page order/coverage differs"
        llms = (root / f"ru/docs/{component}/llms-full.txt").read_text(encoding="utf-8")
        search_files = list(root.glob("offline-search-index.ru.*.json"))
        assert len(search_files) == 1, "expected one Russian search index"
        search_rows = json.loads(search_files[0].read_text(encoding="utf-8"))
        expected_search = Counter("/ru" + node["id"] for node in russian)
        actual_search = Counter(row["ref"] for row in search_rows if row["ref"].startswith("/ru" + prefix))
        assert expected_search == actual_search, "search routes, duplicates or page coverage differs"
        search = {row["ref"]: row for row in search_rows}
        sources_by_route = {}
        for source in (CONTENT / "docs" / component).rglob("*.md"):
            if is_english(source) and not source.name.startswith("_div_"):
                logical = logical_path(source)
                sources_by_route["/" + logical.as_posix().lower() + "/"] = source
        if component == "etcd":
            weights = {}
            for logical, source in sources_by_route.items():
                front, _ = split_front_matter(source.read_text())
                match = re.search(r"(?m)^weight:\s*(-?\d+)", front)
                weights[logical] = int(match[1]) if match else 0
            assert weighted_tree(english[0], weights) == weighted_tree(russian[0], weights), "navigation hierarchy/coverage differs"
        russian_routes = ["/ru" + node["id"] for node in russian]
        rendered_pages = []
        for node in russian:
            route = "/ru" + node["id"]
            assert urlsplit(node["url"]).path == route, f"navigation fallback: {route}"
            assert urlsplit(node["markdown"]).path == route + "index.md", f"Markdown navigation: {route}"
            assert (root / route.lstrip("/") / "index.md").is_file(), f"Markdown missing: {route}"
            target = russian_path(sources_by_route[node["id"]])
            target_front, target_body = split_front_matter(target.read_text(encoding="utf-8"))
            markdown = (root / route.lstrip("/") / "index.md").read_text(encoding="utf-8")
            assert target_body.strip() in markdown, f"incomplete source Markdown body: {route}"
            assert f"Source: https://doc.pg.center{route}index.md" in llms, f"LLMS entry missing: {route}"
            assert route in search, f"search entry missing: {route}"
            assert CYRILLIC_RE.search(search[route]["description"]), f"search description not localized: {route}"
            for field in ("title", "description"):
                value = front_text(target_front, field)
                if value is not None:
                    assert " ".join(search[route][field].split()) == " ".join(value.split()), f"search {field} differs from source metadata: {route}"
            en = RenderedContent(root / node["id"].lstrip("/") / "index.html")
            ru = RenderedContent(root / route.lstrip("/") / "index.html")
            if component == "etcd":
                assert ru.sidebar == russian_routes, f"sidebar differs from localized navigation: {route}"
                position = russian_routes.index(route)
                expected_pager = []
                if position:
                    expected_pager.append(("prev", russian_routes[position - 1]))
                if position + 1 < len(russian_routes):
                    expected_pager.append(("next", russian_routes[position + 1]))
                assert ru.pager == expected_pager, f"pager differs from localized reading order: {route}"
            else:
                assert en.sidebar == [normalized_target(p) for p in ru.sidebar], f"sidebar order differs: {route}"
                assert en.pager == [(d, normalized_target(p)) for d, p in ru.pager], f"pager differs: {route}"
            assert node["id"] in ru.languages, f"English language switch missing: {route}"
            assert route in en.languages, f"Russian language switch missing: {route}"
            assert not any(p.startswith(prefix) for p in ru.sidebar), f"sidebar fallback: {route}"
            assert not any(a.get("data-fallback-language") and prefix in a.get("href", "") for a in ru.link_attributes), f"component fallback marker remains: {route}"
            rendered_pages.append(root / route.lstrip("/") / "index.html")
        errors.extend(f"{component}: {error}" for error in check_full_agent_outputs(root, russian))
        en_print = RenderedContent(root / f"_print/docs/{component}/index.html")
        ru_print = RenderedContent(root / f"ru/_print/docs/{component}/index.html")
        def print_headings(document):
            return [(level, re.sub(r"^pg-[a-f0-9]+", "page", identifier))
                    for level, identifier in document.headings]
        if component == "etcd":
            assert Counter(print_headings(en_print)) == Counter(print_headings(ru_print)), "print page/heading coverage differs"
        else:
            assert print_headings(en_print) == print_headings(ru_print), "print page/heading sequence differs"
        reviewed = set()
        for source in (CONTENT / "docs" / component).rglob("*.md"):
            if is_english(source) and russian_path(source).is_file():
                reviewed.update(reviewed_rendered_fences(source, russian_path(source)))
        if component == "etcd":
            # Each page's exact code order is already checked by compare_rendered;
            # complete per-page print bodies and chapter order are checked below.
            assert Counter(en_print.code) == Counter(ru_print.code), "print code/output coverage differs"
        else:
            assert rendered_code_matches(en_print.code, ru_print.code, reviewed), "print code/output differs"
        printing = load_check_helper("russian_print_body", "check-pgbackrest-ja-print.py")
        print_sources = [sources_by_route[node["id"]] for node in russian]
        print_errors, print_reports = printing.check_print(
            root, print_sources, CONTENT, locale="ru", component=component, compare_metadata=True)
        errors.extend(f"{component}: {error}" for error in print_errors)
        sections = printing.content_sections(printing.read_document(root / f"ru/_print/docs/{component}/index.html"))
        section_order = [title.attrs.get("id") if (title := printing.heading(section)) else None for section in sections]
        expected_order = [None if node["id"] == prefix else "pg-" + hashlib.md5(
            russian_path(sources_by_route[node["id"]]).relative_to(CONTENT).as_posix().encode()).hexdigest()
            for node in russian]
        assert section_order == expected_order, "print chapter order differs from navigation.json"
        rendered_pages.append(root / f"ru/_print/docs/{component}/index.html")
        errors.extend(check_collection_links(component, root, rendered_pages))
        if not errors:
            print(f"Validated Russian {component} production outputs: {len(russian)} pages, "
                  f"{sum(report['expected_blocks'] for report in print_reports)} complete print body blocks, "
                  "canonical/aliases, English anchors, sidebar/pager, language switches, search, "
                  "links/assets, complete Markdown/LLMS bodies and navigation order.")
    except (OSError, ValueError, KeyError, AssertionError) as exc:
        errors.append(f"{component}: rendered collection: {exc}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate English/Russian source parity."
    )
    parser.add_argument(
        "--current-source", action="store_true",
        help="compare older translations with current English instead of their pinned source version",
    )
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="validate every existing Russian pair without requiring all English pages to be translated",
    )
    parser.add_argument("--component", action="append", choices=COMPONENTS,
                        help="limit validation to a component; repeat to select several")
    parser.add_argument("--strict", action="store_true",
                        help="also check complete list/table/quote structure, exact literals and placeholders")
    parser.add_argument("--rendered-dir", type=Path,
                        help="production build used to verify English heading IDs and all code blocks")
    parser.add_argument("--report", type=Path,
                        help="optional full JSON validation report; keep generated reports outside Git")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    roots = [CONTENT / "docs" / name for name in args.component] if args.component else [CONTENT]
    english = sorted({path for root in roots for path in root.rglob("*.md") if is_english(path)})
    russian = sorted({path for root in roots for path in root.rglob("*.ru.md")})
    expected = {russian_path(path) for path in english}
    actual = set(russian)
    errors: list[str] = []

    if not args.allow_partial:
        for missing in sorted(expected - actual):
            errors.append(f"missing Russian page: {missing.relative_to(PROJECT)}")
    for extra in sorted(actual - expected):
        errors.append(f"Russian page has no English source: {extra.relative_to(PROJECT)}")
    for source in english:
        target = russian_path(source)
        if target.is_file():
            errors.extend(compare_pair(source, target, args.current_source))
            if args.strict:
                errors.extend(strict_structure(source, target, args.current_source))
            if args.rendered_dir:
                errors.extend(compare_rendered(source, target, args.rendered_dir))
    if args.component and args.strict and args.current_source and not args.allow_partial:
        for component in args.component:
            errors.extend(check_semantic_review(component, [source for source in english
                          if source.is_relative_to(CONTENT / "docs" / component)]))
    if args.component and args.rendered_dir and not args.allow_partial:
        for component in args.component:
            errors.extend(compare_collection_outputs(component, args.rendered_dir))

    if args.report:
        args.report.write_text(json.dumps({
            "language": "ru", "components": args.component or list(COMPONENTS),
            "source": describe_sources("ru", current=args.current_source),
            "allow_partial": args.allow_partial, "strict": args.strict,
            "expected_pairs": len(expected), "paired": len(actual & expected),
            "missing": [str(path.relative_to(PROJECT)) for path in sorted(expected - actual)],
            "orphans": [str(path.relative_to(PROJECT)) for path in sorted(actual - expected)],
            "rendered_dir": str(args.rendered_dir) if args.rendered_dir else None,
            "errors": errors,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if errors:
        print("Russian source validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    pair_count = len(actual & expected)
    scope = "existing " if args.allow_partial else ""
    print(
        f"Validated {scope}English/Russian parity for {pair_count} documentation pairs "
        f"against {describe_sources('ru', current=args.current_source)}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
