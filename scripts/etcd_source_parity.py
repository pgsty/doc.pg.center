#!/usr/bin/env python3
"""Strict current-source primitives used by the etcd German acceptance gate.

Derived from the shared parity checker, with exact literal/numeric comparison
and the existing single page-specific prose-label exception. This module has
no CLI and does not consume foreign component review approvals.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from translation_sources import describe_sources, read_source


PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content"
EXPECTED_ENGLISH_PAGES = 219
COMPONENTS = (
    "patroni",
    "pgbackrest",
    "pgbouncer",
    "pgbadger",
    "haproxy",
    "etcd",
)
LOCALIZED_ROUTES = frozenset(("docs", "attribution", "search"))

# A locale suffix is a BCP-47-like final filename component.  Checking the
# final component, rather than merely excluding .zh.md and .de.md, prevents a
# newly added locale (for example .ru.md or .pt-BR.md) from becoming an English
# source by accident.
LOCALE_SUFFIX_RE = re.compile(
    r"\.[A-Za-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})*\.md$",
    flags=re.IGNORECASE,
)
TRANSLATABLE_FRONT_MATTER = frozenset(
    {"title", "linkTitle", "description", "categories"}
)
SHARED_ASSET_EXTENSIONS = frozenset(
    {
        ".avif",
        ".bz2",
        ".conf",
        ".csv",
        ".gif",
        ".gz",
        ".ico",
        ".jpeg",
        ".jpg",
        ".json",
        ".log",
        ".pdf",
        ".png",
        ".svg",
        ".tar",
        ".tgz",
        ".toml",
        ".tsv",
        ".txt",
        ".webp",
        ".xml",
        ".xz",
        ".yaml",
        ".yml",
        ".zip",
    }
)
INTERNAL_HOSTS = frozenset({"pig.center", "www.pig.center"})

FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(?:[^\r\n]*)$")
ATX_HEADING_RE = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$")
SETEXT_UNDERLINE_RE = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")
TRAILING_ATTRIBUTE_RE = re.compile(r"[ \t]*\{([^{}]*)\}[ \t]*$")
ATTRIBUTE_ID_RE = re.compile(r"(?:^|\s)#([^\s.]+)")
COMMENT_RE = re.compile(r"<!--.*?-->", flags=re.DOTALL)
SHORTCODE_RE = re.compile(r"\{\{[<%].*?[>%]\}\}", flags=re.DOTALL)
INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
THEMATIC_BREAK_RE = re.compile(
    r"^ {0,3}(?P<run>(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$"
)
FOOTNOTE_RE = re.compile(r"\[\^([^\]\n]+)\]")
FOOTNOTE_DEFINITION_RE = re.compile(r"^ {0,3}\[\^([^\]\n]+)\]:", re.MULTILINE)
REFERENCE_DEFINITION_RE = re.compile(
    r"^ {0,3}\[([^\]^\n][^\]\n]*)\]:[ \t]*(\S+)(?:[ \t]+(.*))?$",
    flags=re.MULTILINE,
)
REFERENCE_LINK_RE = re.compile(r"!?\[([^\]\n]*)\]\[([^\]\n]*)\]")
HTML_TAG_RE = re.compile(
    r"</?[A-Za-z][A-Za-z0-9:-]*(?:\s[^<>]*?)?/?>",
    flags=re.DOTALL,
)
HTML_URL_ATTRIBUTE_RE = re.compile(
    r"\b(href|src)\s*=\s*([\"'])(.*?)\2",
    flags=re.IGNORECASE | re.DOTALL,
)
NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")
VERSION_RE = re.compile(
    r"(?<![A-Za-z0-9_])[vV]?\d+(?:\.\d+)+"
    r"(?:[-+](?=[a-z0-9])[A-Za-z0-9][A-Za-z0-9.-]*)?"
)
RAW_URL_RE = re.compile(r"(?:(?:https?|ftp)://|mailto:)[^\s<>]+", re.IGNORECASE)
UPPERCASE_ATOM_RE = re.compile(
    r"(?<![A-Za-z])[A-Z]{2,}[A-Z0-9]*(?:s)?(?![A-Za-z0-9])"
)
UPPERCASE_COMPOUND_RE = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"[A-Z]{2,}[A-Z0-9]*(?:[+./_-][A-Z0-9]+)+(?:s)?"
    r"(?![A-Za-z0-9_])"
)
UPPERCASE_SINGLE_LETTER_COMPOUND_RE = re.compile(
    r"(?<![A-Za-z0-9_])[A-Z](?:[/.][A-Z])+(?:\.)?(?![A-Za-z0-9_])"
)
# These abbreviations may naturally be expanded in German prose.  All other
# uppercase technical tokens present in English must still occur in German.
UPPERCASE_LITERAL_EXCEPTIONS = frozenset({"FAQ", "F.A.Q.", "MANUALLY", "OS", "UNIX", "MUST", "SHOULD", "MAY"})
RAW_HTML_HEADING_TAG_RE = re.compile(
    r"</?(?:a|abbr|b|blockquote|br|code|dd|details|div|dl|dt|em|h[1-6]|hr|i|img|kbd|li|ol|p|pre|span|strong|sub|summary|sup|table|tbody|td|th|thead|tr|ul)\b[^>]*>",
    flags=re.IGNORECASE,
)


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    anchor: str | None
    line: int


def relative(path: Path) -> str:
    return str(path.relative_to(PROJECT))


def is_english_source(path: Path) -> bool:
    return path.suffix.lower() == ".md" and not LOCALE_SUFFIX_RE.search(path.name)


def german_target(source: Path) -> Path:
    return source.with_name(source.name.removesuffix(".md") + ".de.md")


def split_front_matter(document: str) -> tuple[str, str]:
    if not document.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    end = document.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML front matter")
    return document[4:end], document[end + 5 :]


def front_matter_blocks(front: str) -> dict[str, str]:
    """Return top-level YAML fields without requiring a PyYAML dependency."""
    blocks: dict[str, list[str]] = {}
    current: str | None = None
    preamble: list[str] = []
    for line in front.splitlines(keepends=True):
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$", line)
        if match:
            current = match.group(1)
            if current in blocks:
                raise ValueError(f"duplicate front matter key {current!r}")
            blocks[current] = [line]
        elif current is None:
            preamble.append(line)
        else:
            blocks[current].append(line)
    if preamble and any(line.strip() and not line.lstrip().startswith("#") for line in preamble):
        raise ValueError("content before the first front matter key")
    if preamble:
        blocks["__preamble__"] = preamble
    return {key: "".join(value) for key, value in blocks.items()}


def masked(value: str) -> str:
    """Blank a construct while retaining its line count."""
    return "".join("\n" if line.endswith("\n") else "" for line in value.splitlines(True))


def parse_fenced_blocks(body: str) -> tuple[list[str], str]:
    lines = body.splitlines(keepends=True)
    blocks: list[str] = []
    prose: list[str] = []
    block: list[str] = []
    marker = ""
    minimum = 0
    for line in lines:
        logical = line.rstrip("\r\n")
        if marker:
            block.append(line)
            if re.fullmatch(
                rf" {{0,3}}{re.escape(marker)}{{{minimum},}}[ \t]*", logical
            ):
                blocks.append("".join(block))
                prose.extend(masked(part) for part in block)
                block = []
                marker = ""
                minimum = 0
            continue
        match = FENCE_OPEN_RE.match(logical)
        if match:
            opener = match.group(1)
            marker = opener[0]
            minimum = len(opener)
            block = [line]
        else:
            prose.append(line)
    if marker:
        raise ValueError("unterminated fenced code block")
    return blocks, "".join(prose)


def prose_without_comments_and_shortcodes(prose: str) -> str:
    prose = COMMENT_RE.sub(lambda match: masked(match.group(0)), prose)
    return SHORTCODE_RE.sub(lambda match: masked(match.group(0)), prose)


def heading_parts(raw: str) -> tuple[str, str | None]:
    raw = re.sub(r"[ \t]+#+[ \t]*$", "", raw)
    attribute = TRAILING_ATTRIBUTE_RE.search(raw)
    anchor: str | None = None
    if attribute:
        identifier = ATTRIBUTE_ID_RE.search(attribute.group(1))
        if identifier:
            anchor = identifier.group(1)
        raw = raw[: attribute.start()]
    return raw.strip(), anchor


def heading_rows(body: str) -> list[Heading]:
    _, prose = parse_fenced_blocks(body)
    prose = prose_without_comments_and_shortcodes(prose)
    lines = prose.splitlines()
    rows: list[Heading] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        atx = ATX_HEADING_RE.match(line)
        if atx:
            title, anchor = heading_parts(atx.group(2))
            rows.append(Heading(len(atx.group(1)), title, anchor, index + 1))
            index += 1
            continue
        if index + 1 < len(lines) and line.strip():
            setext = SETEXT_UNDERLINE_RE.match(lines[index + 1])
            if setext:
                title, anchor = heading_parts(line)
                level = 1 if setext.group(1).startswith("=") else 2
                rows.append(Heading(level, title, anchor, index + 1))
                index += 2
                continue
        index += 1
    return rows


def plain_heading_text(title: str) -> str:
    title = html.unescape(title)
    title = re.sub(r"!?\[([^]\n]*)\]\([^)]*\)", r"\1", title)
    title = re.sub(r"!?\[([^]\n]*)\]\[[^]\n]*\]", r"\1", title)
    title = re.sub(r"`+([^`\n]*)`+", r"\1", title)
    return RAW_HTML_HEADING_TAG_RE.sub("", title)


def inferred_heading_ids(headings: list[Heading]) -> list[str]:
    """Mirror the Goldmark IDs used by the repository's current Hugo build."""
    seen: Counter[str] = Counter()
    identifiers: list[str] = []
    for heading in headings:
        if heading.anchor is not None:
            identifiers.append(heading.anchor)
            continue
        plain = plain_heading_text(heading.title).lower()
        base = "".join(
            "-" if character.isspace() else character
            for character in plain
            if character.isspace()
            or character.isalnum()
            or character in {"-", "_"}
        ).strip("-")
        occurrence = seen[base]
        seen[base] += 1
        identifiers.append(base if occurrence == 0 else f"{base}-{occurrence}")
    return identifiers


class RenderedHeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.content_depth = 0
        self.found_content = False
        self.rows: list[tuple[int, str]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if (
            tag == "div"
            and self.content_depth == 0
            and "td-content" in (attributes.get("class") or "").split()
        ):
            self.content_depth = 1
            self.found_content = True
            return
        if not self.content_depth:
            return
        if tag == "div":
            self.content_depth += 1
        if re.fullmatch(r"h[1-6]", tag) and attributes.get("id"):
            self.rows.append((int(tag[1]), html.unescape(attributes["id"] or "")))

    def handle_endtag(self, tag: str) -> None:
        if self.content_depth and tag == "div":
            self.content_depth -= 1


def rendered_page(source: Path, rendered_root: Path) -> Path:
    source_relative = source.relative_to(CONTENT)
    if source.name in {"_index.md", "index.md"}:
        route = source_relative.parent
    else:
        route = source_relative.with_suffix("")
    return rendered_root.joinpath(*(part.lower() for part in route.parts), "index.html")


def rendered_heading_ids(
    source: Path, headings: list[Heading], rendered_root: Path
) -> list[str]:
    # Landing/search layouts intentionally do not use the normal .td-content
    # wrapper.  With no Markdown headings there are no implicit IDs to align.
    if not headings:
        return []
    rendered = rendered_page(source, rendered_root)
    if not rendered.is_file():
        raise ValueError(f"missing rendered English page: {rendered}")
    parser = RenderedHeadingParser()
    parser.feed(rendered.read_text(encoding="utf-8", errors="replace"))
    if not parser.found_content:
        raise ValueError(f"rendered page has no .td-content container: {rendered}")
    levels = [heading.level for heading in headings]
    rendered_levels = [level for level, _ in parser.rows]
    if rendered_levels != levels:
        raise ValueError(
            "rendered English heading levels do not align with Markdown "
            f"(Markdown={levels!r}, HTML={rendered_levels!r})"
        )
    identifiers = [identifier for _, identifier in parser.rows]
    for heading, identifier in zip(headings, identifiers, strict=True):
        if heading.anchor is not None and identifier != heading.anchor:
            raise ValueError(
                f"rendered ID {identifier!r} does not match explicit English "
                f"anchor {heading.anchor!r} on line {heading.line}"
            )
    return identifiers


def list_signature(body: str) -> list[tuple[int, str]]:
    _, prose = parse_fenced_blocks(body)
    prose = prose_without_comments_and_shortcodes(prose)
    rows: list[tuple[int, str]] = []
    for line in prose.splitlines():
        match = re.match(r"^(\s*)([-+*]|\d{1,3}[.)])\s+", line)
        if not match:
            continue
        indent = len(match.group(1).expandtabs(4))
        if indent <= 1:
            indent = 0
        marker = match.group(2)
        rows.append((indent, "unordered" if marker in "-+*" else marker))
    return rows


def thematic_break_signature(body: str) -> list[str]:
    """Return the ordered Markdown thematic-break marker sequence.

    Front matter is already removed by the caller.  Fenced code, comments,
    and shortcodes are blanked before scanning.  An unspaced hyphen run below
    ordinary text is a Setext heading underline, not a thematic break.
    """
    _, prose = parse_fenced_blocks(body)
    prose = prose_without_comments_and_shortcodes(prose)
    lines = prose.splitlines()
    signature: list[str] = []
    for index, line in enumerate(lines):
        match = THEMATIC_BREAK_RE.fullmatch(line)
        if not match:
            continue
        run = match.group("run")
        marker = next(character for character in run if character in "*-_")
        if (
            marker == "-"
            and SETEXT_UNDERLINE_RE.fullmatch(line)
            and index > 0
            and lines[index - 1].strip()
            and not ATX_HEADING_RE.match(lines[index - 1])
            and not re.match(r"^\s*(?:>|[-+*]\s|\d{1,3}[.)]\s)", lines[index - 1])
        ):
            continue
        signature.append(marker)
    return signature


def table_signature(body: str) -> list[tuple[int, int]]:
    _, prose = parse_fenced_blocks(body)
    prose = prose_without_comments_and_shortcodes(prose)
    return [
        (
            len(line) - len(line.lstrip(" \t")),
            len(re.findall(r"(?<!\\)\|", line)),
        )
        for line in prose.splitlines()
        if line.lstrip().startswith("|")
    ]


def blockquote_signature(body: str) -> list[tuple[int, tuple[str, ...]]]:
    _, prose = parse_fenced_blocks(body)
    prose = prose_without_comments_and_shortcodes(prose)
    blocks: list[tuple[int, tuple[str, ...]]] = []
    depth = 0
    admonitions: list[str] = []
    active = False
    for line in prose.splitlines():
        quote = re.match(r"^\s*(>+)\s?(.*)$", line)
        if quote:
            active = True
            depth = max(depth, len(quote.group(1)))
            admonition = re.match(r"\[!([A-Za-z]+)\]", quote.group(2))
            if admonition:
                admonitions.append(admonition.group(1).upper())
        elif active and line.strip():
            blocks.append((depth, tuple(admonitions)))
            depth = 0
            admonitions = []
            active = False
    if active:
        blocks.append((depth, tuple(admonitions)))
    return blocks


def url_path(target: str) -> tuple[str, bool]:
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    parsed = urlsplit(target)
    if parsed.scheme in {"http", "https"} or parsed.netloc:
        if parsed.netloc.casefold() not in INTERNAL_HOSTS:
            return parsed.path, False
        return parsed.path, True
    if parsed.scheme:
        return parsed.path, False
    return parsed.path, True


def normalize_german_target(target: str) -> str:
    """Remove the German prefix only where a documentation route expects it."""
    target = target.strip()
    wrapped = target.startswith("<") and target.endswith(">")
    raw = target[1:-1] if wrapped else target
    parsed = urlsplit(raw)
    path = parsed.path
    match = re.match(r"^/de/([^/]+)(?=/|$)", path, flags=re.IGNORECASE)
    patroni_alias = match and match.group(1).casefold() == 'patroni' and url_path(raw)[1]
    if match and (match.group(1).casefold() in LOCALIZED_ROUTES or patroni_alias):
        path = path[3:]
        normalized = parsed._replace(path=path).geturl()
    else:
        normalized = raw
    return f"<{normalized}>" if wrapped else normalized


def is_shared_asset(target: str) -> bool:
    path, _ = url_path(target)
    return Path(path).suffix.casefold() in SHARED_ASSET_EXTENSIONS


def localized_shared_asset(target: str) -> bool:
    path, internal = url_path(target)
    if not internal or not is_shared_asset(target):
        return False
    match = re.match(r"^/de/(?:docs/)?([^/]+)(?=/|$)", path, flags=re.IGNORECASE)
    return bool(match and match.group(1).casefold() in COMPONENTS)


def unlocalized_document_route(target: str) -> bool:
    path, internal = url_path(target)
    if not internal or is_shared_asset(target):
        return False
    match = re.match(r"^/(?:docs/)?([^/]+)(?=/|$)", path)
    return bool(match and match.group(1).casefold() in COMPONENTS)


def markdown_inline_destinations(prose: str) -> list[str]:
    """Read destinations after ](, including balanced parentheses in URLs."""
    destinations: list[str] = []
    index = 0
    while True:
        start = prose.find("](", index)
        if start < 0:
            break
        cursor = start + 2
        depth = 1
        escaped = False
        angle = False
        while cursor < len(prose):
            character = prose[cursor]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == "<" and depth == 1:
                angle = True
            elif character == ">" and angle:
                angle = False
            elif not angle and character == "(":
                depth += 1
            elif not angle and character == ")":
                depth -= 1
                if depth == 0:
                    break
            cursor += 1
        if depth:
            index = start + 2
            continue
        inside = prose[start + 2 : cursor].strip()
        if inside.startswith("<"):
            end = inside.find(">")
            destination = inside[: end + 1] if end >= 0 else inside
        else:
            match = re.match(r"(?:\\.|[^\s])+", inside)
            destination = match.group(0) if match else ""
        if destination:
            destinations.append(destination)
        index = cursor + 1
    return destinations


def prose_without_markdown_destinations(prose: str) -> str:
    """Remove inline-link destinations while retaining their visible labels."""
    output: list[str] = []
    position = 0
    while True:
        start = prose.find("](", position)
        if start < 0:
            output.append(prose[position:])
            break
        output.append(prose[position : start + 1])
        cursor = start + 2
        depth = 1
        escaped = False
        angle = False
        while cursor < len(prose):
            character = prose[cursor]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == "<" and depth == 1:
                angle = True
            elif character == ">" and angle:
                angle = False
            elif not angle and character == "(":
                depth += 1
            elif not angle and character == ")":
                depth -= 1
                if depth == 0:
                    break
            cursor += 1
        if depth:
            output.append(prose[start + 1 :])
            break
        position = cursor + 1
    return "".join(output)


def canonical_uppercase_literal(value: str) -> str:
    # German compounds commonly attach the lowercase plural suffix in forms
    # such as URLs or APIs.  Presence of the underlying abbreviation is what
    # this check is intended to protect.
    if len(value) > 1 and value.endswith("s") and value[-2].isupper():
        return value[:-1]
    return value


def uppercase_technical_literals(body: str) -> set[str]:
    """Collect visible uppercase technical literals from translated prose."""
    _, prose = parse_fenced_blocks(body)
    prose = COMMENT_RE.sub("", prose)
    prose = SHORTCODE_RE.sub("", prose)
    prose = INLINE_CODE_RE.sub("", prose)
    prose = REFERENCE_DEFINITION_RE.sub("", prose)
    prose = prose_without_markdown_destinations(prose)
    prose = HTML_TAG_RE.sub("", prose)
    prose = RAW_URL_RE.sub("", prose)
    prose = re.sub(r"\{[^{}]*#[^{}]+\}", "", prose)
    # Warning labels are translatable prose, not protocol/API abbreviations.
    # Match the actual label syntax, so NOTE or TABLESPACES elsewhere remains
    # protected, as do any technical tokens following the label.
    prose = re.sub(
        r"\*\*(?:NOTE TO PACKAGERS|IMPORTANT NOTE|"
        r"IMPORTANT BUG FIX FOR TABLESPACES|NOTE:?|CAUTION:?)\*\*:?(?=\s|$)",
        "", prose,
    )
    prose = re.sub(r"(?m)^\s*(?:>\s*)?(?:NOTE|CAUTION|WARNING|IMPORTANT):\s*$", "", prose)
    prose = prose.replace("**DROP IT**", "")
    # Clock suffixes are localized as morgens/abends, while bare AM/PM tokens
    # remain protected. Numeric equality is checked separately.
    prose = re.sub(r"\b(\d{1,2}:\d{2})\s+(?:AM|PM)\b", r"\1", prose)
    prose = re.sub(r"(?m)^(\s*\|)\s*TOTAL\s*(?=\|)", r"\1", prose)
    # Emphasized ordinary words in the failsafe explanation are translatable.
    # ALL outside these phrases (for example a SQL keyword) remains protected.
    prose = re.sub(r"\bMUST(?= the current primary)", "", prose)
    prose = re.sub(r"\bALL(?= other (?:cluster )?members)", "", prose)
    prose = re.sub(r"\*\*MUST\*\*(?= disable any other sources)", "", prose)
    prose = re.sub(r"\bAKA(?=\s+\))", "", prose)
    # PgBouncer's release notes emphasize an ordinary adjective here.
    # A standalone VERY in SQL, output, or another context stays protected.
    prose = re.sub(r"\bVERY(?= outdated\b)", "", prose)
    # These historical PgBouncer phrases use ordinary emphasis, warning
    # labels, or database abbreviations, not API/SQL identifiers. Limit each
    # exception to its prose context; the same tokens elsewhere are checked.
    prose = re.sub(r"(?m)^(\s*\*\s+)\[SECURITY\](?=\s+Remove invalid assignment)", r"\1", prose)
    prose = re.sub(r"\bSNAFU(?=: c-ares versions)", "", prose)
    prose = re.sub(r"\bDBs(?= that are paused\.)", "", prose)
    prose = re.sub(r"(?<=seems )OK(?=\.)", "", prose)
    prose = re.sub(r"(?<=packet boundary )ASAP(?=\.)", "", prose)
    # etcd emphasizes exclusivity in ordinary sentences. Keep ONLY protected
    # outside these grammatical uses, including SQL such as SELECT ONLY.
    prose = re.sub(r"\bONLY(?= (?:be )?used for\b)", "", prose)
    prose = re.sub(r"(?<=for testing )ONLY(?=!)", "", prose)
    prose = re.sub(r"(?<=CRC takes in consideration )ALL(?= records\b)", "", prose)
    # HAProxy prose emphasizes these ordinary quantifiers/conjunctions. Match
    # their complete context; bare logic operators and enum values stay exact.
    prose = re.sub(r"(?<=when )ALL(?= health checks (?:fail|succeed)\b)", "", prose)
    prose = re.sub(r"(?<=keepalive )OR(?= any property ID\b)", "", prose)
    prose = re.sub(r"(?<=reason_code )OR(?= any property ID\b)", "", prose)
    prose = re.sub(r"(?m)^(- a )METHOD(?= : GET$)", r"\1", prose)
    prose = prose.replace("OTHER CAVEATS AND NOTES:", "")
    prose = re.sub(r"(?m)^NOTE:(?= Don't forget to set the \"protection\" rules to ensure HAProxy)", "", prose)
    prose = re.sub(r"(?<=\()IE(?= a Host header\))", "", prose)
    prose = re.sub(r"(?m)^IMPORTANT NOTE:(?= historically in HTTP/1\.x, the vast majority of requests sent by browsers use the)", "", prose)
    prose = re.sub(r"CAUTION!(?= Except under very specific conditions, it is normally not correct to use this field as a)", "", prose)
    prose = re.sub(r"THIS MUST NOT BE USED FOR (?=HTTPS\b)", "", prose)
    prose = re.sub(r"(?<=strongly recommended )NOT(?= to use this option, unless absolutely needed)", "", prose)
    prose = re.sub(r"(?<=If the variable exists, it is )NOT(?=\s+overwritten\.)", "", prose)
    prose = re.sub(r"(?<=this option does )NOT(?= make HAProxy present the client's IP to\s+the server when establishing the connection\.)", "", prose)
    prose = re.sub(r"(?m)^WARNING:(?= there are stability and security implications in using this feature\.)", "", prose)
    prose = re.sub(
        r"(The information present in this ring are structured and are )NOT(?= directly readable using a text\s+editor\b)",
        r"\1", prose,
    )

    literals = {
        canonical_uppercase_literal(value)
        for pattern in (
            UPPERCASE_ATOM_RE,
            UPPERCASE_COMPOUND_RE,
            UPPERCASE_SINGLE_LETTER_COMPOUND_RE,
        )
        for value in pattern.findall(prose)
    }
    return literals - UPPERCASE_LITERAL_EXCEPTIONS


def html_destinations(prose: str) -> list[str]:
    return [match.group(3) for match in HTML_URL_ATTRIBUTE_RE.finditer(prose)]


def link_targets(body: str) -> list[str]:
    _, prose = parse_fenced_blocks(body)
    prose = prose_without_comments_and_shortcodes(prose)
    # A code span may contain Markdown-looking syntax.  Its literal is checked
    # separately and must not create a false link target here.
    prose_without_code = INLINE_CODE_RE.sub("`CODE`", prose)
    targets = markdown_inline_destinations(prose_without_code)
    targets.extend(
        match.group(2) for match in REFERENCE_DEFINITION_RE.finditer(prose_without_code)
    )
    targets.extend(html_destinations(prose_without_code))
    return targets


def normalized_reference_definitions(body: str) -> list[tuple[str, str, str]]:
    _, prose = parse_fenced_blocks(body)
    prose = prose_without_comments_and_shortcodes(prose)
    return [
        (
            match.group(1).casefold(),
            normalize_german_target(match.group(2)),
            match.group(3) or "",
        )
        for match in REFERENCE_DEFINITION_RE.finditer(prose)
    ]


def reference_link_signature(body: str) -> list[str]:
    """Return effective IDs for full, collapsed, and defined shortcut links.

    A translated shortcut needs an explicit ID (``[deutscher Text][English]``).
    Counting only full/collapsed links would incorrectly flag that required
    localization as an added reference, while overlooking lost shortcuts.
    """
    _, prose = parse_fenced_blocks(body)
    prose = prose_without_comments_and_shortcodes(prose)
    definitions = {
        match.group(1).casefold()
        for match in REFERENCE_DEFINITION_RE.finditer(prose)
    }
    prose = REFERENCE_DEFINITION_RE.sub("", prose)
    prose = INLINE_CODE_RE.sub("`CODE`", prose)
    references = re.compile(
        r"!?\[([^\]\n]*)\]\[([^\]\n]*)\]"
        r"|!?\[([^\]\n]+)\](?![\[(:])"
    )
    return [
        (match.group(2) or match.group(1) or match.group(3)).casefold()
        for match in references.finditer(prose)
        if match.group(3) is None or match.group(3).casefold() in definitions
    ]


def normalized_html_tags(prose: str) -> list[str]:
    prose = INLINE_CODE_RE.sub("", prose)

    def normalize_attributes(match: re.Match[str]) -> str:
        quote = match.group(2)
        target = normalize_german_target(match.group(3))
        return f"{match.group(1)}={quote}{target}{quote}"

    return [
        re.sub(
            r"\b(alt|title)\s*=\s*([\"'])(.*?)\2",
            lambda match: f"{match.group(1)}={match.group(2)}TRANSLATABLE{match.group(2)}",
            HTML_URL_ATTRIBUTE_RE.sub(normalize_attributes, tag),
            flags=re.IGNORECASE | re.DOTALL,
        )
        for tag in HTML_TAG_RE.findall(prose)
    ]


def number_facts(front: str, body: str) -> Counter[str]:
    # Explicit target anchors are intentionally added for implicit English
    # headings and may themselves contain digits.  They are routing metadata,
    # not translated factual content.
    value = front + "\n" + body
    value = re.sub(r"\{[^{}]*#[^{}]+\}", "", value)
    value = re.sub(r"&#(?:x[0-9A-Fa-f]+|\d+);", "", value)
    # This exact ACME sentence uses "3rd party" as the lexical concept
    # Drittanbieter, not a numeric fact. Other ordinals and all operational
    # values, including the adjacent renewal formula/intervals, stay checked.
    value = re.sub(
        r"(?<=dataplaneAPI or another )3rd(?= party tool to talk to a DNS provider API\.)",
        "", value,
    )
    return Counter(NUMBER_RE.findall(value))


def version_facts(front: str, body: str) -> Counter[str]:
    value = front + "\n" + body
    value = re.sub(r"\{[^{}]*#[^{}]+\}", "", value)
    return Counter(VERSION_RE.findall(value))


def counter_delta(source: Counter[str], target: Counter[str]) -> str:
    missing = list((source - target).elements())[:12]
    added = list((target - source).elements())[:12]
    return f"missing={missing!r}, added={added!r}"


def compare(
    label: str, source_value: object, target_value: object, errors: list[str]
) -> None:
    if source_value != target_value:
        errors.append(label)


def validate_pair(
    source: Path,
    target: Path,
    rendered_root: Path | None,
    errors: list[str],
    current_source: bool = False,
) -> None:
    label = relative(source)
    try:
        english, source_revision = read_source(source, "de", current=current_source)
        german = target.read_text(encoding="utf-8")
        en_front, en_body = split_front_matter(english)
        de_front, de_body = split_front_matter(german)
        en_front_blocks = front_matter_blocks(en_front)
        de_front_blocks = front_matter_blocks(de_front)
        en_fences, en_prose = parse_fenced_blocks(en_body)
        de_fences, de_prose = parse_fenced_blocks(de_body)
    except (OSError, ValueError) as exc:
        errors.append(f"{label}: {exc}")
        return

    if en_front_blocks.keys() != de_front_blocks.keys():
        missing = sorted(en_front_blocks.keys() - de_front_blocks.keys())
        added = sorted(de_front_blocks.keys() - en_front_blocks.keys())
        errors.append(
            f"{label}: front matter key set changed (missing={missing!r}, added={added!r})"
        )
    for key in sorted(en_front_blocks.keys() & de_front_blocks.keys()):
        if key not in TRANSLATABLE_FRONT_MATTER and (
            en_front_blocks[key] != de_front_blocks[key]
        ):
            errors.append(f"{label}: non-translatable front matter {key!r} changed")

    compare(f"{label}: fenced code blocks changed", en_fences, de_fences, errors)

    en_comments = COMMENT_RE.findall(en_prose)
    de_comments = COMMENT_RE.findall(de_prose)
    compare(f"{label}: HTML comments changed", en_comments, de_comments, errors)

    en_without_comments = COMMENT_RE.sub("", en_prose)
    de_without_comments = COMMENT_RE.sub("", de_prose)
    compare(
        f"{label}: Hugo shortcodes changed",
        SHORTCODE_RE.findall(en_without_comments),
        SHORTCODE_RE.findall(de_without_comments),
        errors,
    )
    en_markup = SHORTCODE_RE.sub("", en_without_comments)
    de_markup = SHORTCODE_RE.sub("", de_without_comments)
    compare(
        f"{label}: HTML tag sequence or attributes changed",
        normalized_html_tags(en_markup),
        normalized_html_tags(de_markup),
        errors,
    )

    en_inline = Counter(INLINE_CODE_RE.findall(en_markup))
    # This backtick span names a prose concept, not a query/API literal.
    # Require its reviewed German translation only on this exact source page;
    # every other inline span, including Revision and API fields, stays exact.
    if label == "content/docs/etcd/learning/api.md":
        count = en_inline.pop("`time travel query`", 0)
        if count:
            en_inline["`Zeitreiseabfrage`"] += count
    de_inline = Counter(INLINE_CODE_RE.findall(de_markup))
    compare(f"{label}: inline code literals changed", en_inline, de_inline, errors)
    compare(
        f"{label}: footnote references changed",
        Counter(FOOTNOTE_RE.findall(en_markup)),
        Counter(FOOTNOTE_RE.findall(de_markup)),
        errors,
    )
    compare(
        f"{label}: footnote definition order changed",
        FOOTNOTE_DEFINITION_RE.findall(en_markup),
        FOOTNOTE_DEFINITION_RE.findall(de_markup),
        errors,
    )
    compare(
        f"{label}: reference definitions changed",
        normalized_reference_definitions(en_body),
        normalized_reference_definitions(de_body),
        errors,
    )
    compare(
        f"{label}: reference-link identifiers changed",
        reference_link_signature(en_body),
        reference_link_signature(de_body),
        errors,
    )
    missing_uppercase = sorted(
        uppercase_technical_literals(en_body) - uppercase_technical_literals(de_body)
    )
    if missing_uppercase:
        errors.append(
            f"{label}: uppercase technical literals missing from German: "
            f"{missing_uppercase[:20]!r}"
        )

    en_headings = heading_rows(en_body)
    de_headings = heading_rows(de_body)
    en_levels = [heading.level for heading in en_headings]
    de_levels = [heading.level for heading in de_headings]
    if en_levels != de_levels:
        errors.append(
            f"{label}: heading level sequence changed "
            f"(EN={en_levels!r}, DE={de_levels!r})"
        )
    else:
        try:
            expected_ids = (
                rendered_heading_ids(source, en_headings, rendered_root)
                if rendered_root is not None and source_revision is None
                else inferred_heading_ids(en_headings)
            )
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            expected_ids = []
        actual_ids = [heading.anchor for heading in de_headings]
        if expected_ids and actual_ids != expected_ids:
            for index, (heading, expected, actual) in enumerate(
                zip(de_headings, expected_ids, actual_ids, strict=True), 1
            ):
                if actual != expected:
                    errors.append(
                        f"{label}:{heading.line}: German heading {index} must preserve "
                        f"English anchor {expected!r}, found {actual!r}"
                    )
                    break

    compare(
        f"{label}: Markdown list marker sequence or nesting changed",
        list_signature(en_body),
        list_signature(de_body),
        errors,
    )
    compare(
        f"{label}: Markdown thematic break sequence changed",
        thematic_break_signature(en_body),
        thematic_break_signature(de_body),
        errors,
    )
    compare(
        f"{label}: Markdown table shape changed",
        table_signature(en_body),
        table_signature(de_body),
        errors,
    )
    compare(
        f"{label}: blockquote structure or admonition type changed",
        blockquote_signature(en_body),
        blockquote_signature(de_body),
        errors,
    )

    en_targets = [normalize_german_target(value) for value in link_targets(en_body)]
    de_targets_raw = link_targets(de_body)
    de_targets = [normalize_german_target(value) for value in de_targets_raw]
    if en_targets != de_targets:
        errors.append(f"{label}: link or asset destination sequence changed")
    prefixed_assets = sorted({value for value in de_targets_raw if localized_shared_asset(value)})
    if prefixed_assets:
        errors.append(
            f"{label}: shared assets must not use a /de prefix: {prefixed_assets[:12]!r}"
        )
    bare_component_routes = sorted(
        {value for value in de_targets_raw if unlocalized_document_route(value)}
    )
    if bare_component_routes:
        errors.append(
            f"{label}: German document links must use /de/docs/<component>/ routes: "
            f"{bare_component_routes[:12]!r}"
        )

    en_numbers = number_facts(en_front, en_body)
    de_numbers = number_facts(de_front, de_body)
    if en_numbers != de_numbers:
        errors.append(
            f"{label}: numeric facts changed ({counter_delta(en_numbers, de_numbers)})"
        )
    en_versions = version_facts(en_front, en_body)
    de_versions = version_facts(de_front, de_body)
    if en_versions != de_versions:
        errors.append(
            f"{label}: version facts changed ({counter_delta(en_versions, de_versions)})"
        )
