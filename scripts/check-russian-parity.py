#!/usr/bin/env python3
"""Validate English/Russian source parity for every documentation page.

The Russian edition is translated prose, but executable examples and the
Markdown/link structure must remain derived from the English source.  This
check deliberately runs on source files so a broken translation fails before
Hugo renders it.
"""

from __future__ import annotations

import argparse
import re
import sys
import posixpath
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from translation_sources import describe_sources, read_source


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
    value = target
    for component in COMPONENTS:
        value = value.replace(f"/ru/docs/{component}/", f"/docs/{component}/")
    value = re.sub(r"^/ru/(?=(?:docs|search|attribution)(?:/|$))", "/", value)
    return value


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
    shortcodes = SHORTCODE_RE.findall(prose_without_comments)
    tags = []
    for tag in HTML_TAG_RE.findall(prose_without_comments):
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
        for line in prose_without_comments.splitlines()
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
        ("fenced code blocks", source_blocks, target_blocks),
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

    missing_inline = Counter(source_inline) - Counter(target_inline)
    if missing_inline:
        errors.append(f"{label}: protected inline code missing: {list(missing_inline)[:8]}")

    source_anchors = explicit_anchors(source_body)
    target_anchors = explicit_anchors(target_body)
    missing_anchors = [anchor for anchor in source_anchors if anchor not in target_anchors]
    if missing_anchors:
        errors.append(f"{label}: explicit anchors missing in Russian: {missing_anchors[:8]}")

    untranslated = residual_english(target_body)
    for number, line in untranslated[:5]:
        errors.append(f"{label}: probable untranslated English near body line {number}: {line}")
    if len(untranslated) > 5:
        errors.append(f"{label}: {len(untranslated) - 5} more probable untranslated lines")
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    english = sorted(path for path in CONTENT.rglob("*.md") if is_english(path))
    russian = sorted(CONTENT.rglob("*.ru.md"))
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

    if errors:
        print("Russian source validation failed:", file=sys.stderr)
        for error in errors[:300]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 300:
            print(f"- ... {len(errors) - 300} more", file=sys.stderr)
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
