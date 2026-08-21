#!/usr/bin/env python3
"""Validate HAProxy and etcd source/translation structure and completeness."""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content"
COMPONENTS = ("haproxy", "etcd")

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(
    r"^(?P<marks>#{1,6})\s+(?P<title>.*?)(?:\s+\{#(?P<anchor>[^}]+)\})?\s*$"
)
REFERENCE_DEF_RE = re.compile(r"^\s*\[([^]]+)\]:\s+(\S+)(?:\s+.*)?$")
INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
FOOTNOTE_RE = re.compile(r"\[\^[^\]\n]+\]")
HTML_TAG_RE = re.compile(
    r"</?(?:a|abbr|b|blockquote|br|code|dd|div|dl|dt|em|h[1-6]|hr|i|img|kbd|li|ol|p|pre|span|strong|sub|sup|table|tbody|td|th|thead|tr|ul)\b[^>\n]*>",
    flags=re.IGNORECASE,
)
NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    r"(?:v|V)?\d+(?:\.\d+)+(?:[-+][A-Za-z0-9.-]+)?"
    r"|\d+(?:\.\d+)?(?:\s?(?:ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB|纳秒|微秒|毫秒|秒|分钟|小时|天|字节|%))?"
    r")(?![A-Za-z0-9])"
)
ENGLISH_WORD_RE = re.compile(r"\b[a-z]{2,}\b")
ENGLISH_FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "for", "on", "with",
    "by", "from", "as", "is", "are", "be", "this", "that", "it", "its", "can",
    "will", "may", "should", "must", "not", "if", "when", "at", "into", "which",
    "their", "they", "them", "than", "has", "have", "had", "was", "were", "would",
}


def split_front_matter(document: str) -> tuple[str, str]:
    if not document.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    end = document.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML front matter")
    return document[4:end], document[end + 5 :]


def front_value(front: str, key: str) -> list[str]:
    return re.findall(rf"^{re.escape(key)}:\s*(.*)$", front, flags=re.MULTILINE)


def parse_fenced_blocks(body: str) -> tuple[list[str], str]:
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


def html_comments(body: str) -> list[str]:
    return re.findall(r"<!--.*?-->", body, flags=re.DOTALL)


def normalize_localized_target(value: str, component: str) -> str:
    return value.replace(f"/zh/{component}/", f"/{component}/")


def link_targets(body: str, component: str, *, normalize: bool = True) -> list[str]:
    _, prose = parse_fenced_blocks(body)
    targets: list[str] = []
    targets.extend(re.findall(r"(?<=[^!])\]\(([^)\n]+)\)", " " + prose))
    targets.extend(re.findall(r"!\[[^]]*\]\(([^)\n]+)\)", prose))
    targets.extend(value for _, value in REFERENCE_DEF_RE.findall(prose))
    targets.extend(re.findall(r'\b(?:href|src|link)=["\']([^"\']+)["\']', prose))
    if normalize:
        return [normalize_localized_target(value, component) for value in targets]
    return targets


def heading_rows(body: str) -> list[tuple[str, str | None]]:
    _, prose = parse_fenced_blocks(body)
    rows: list[tuple[str, str | None]] = []
    for line in prose.splitlines():
        match = HEADING_RE.match(line)
        if match:
            rows.append((match.group("marks"), match.group("anchor")))
    return rows


def list_signature(body: str) -> list[tuple[int, str]]:
    _, prose = parse_fenced_blocks(body)
    rows: list[tuple[int, str]] = []
    active_ordered_indents: set[int] = set()
    for line in prose.splitlines():
        match = re.match(r"^(\s*)([-+*]|\d{1,2}[.)])\s+", line)
        if match:
            indent = len(match.group(1).expandtabs(4))
            if indent <= 1:
                indent = 0
            marker = match.group(2)
            if marker in "-+*":
                rows.append((indent, "unordered"))
            elif int(marker[:-1]) == 1 or indent in active_ordered_indents:
                rows.append((indent, marker))
                active_ordered_indents.add(indent)
            continue
        if line.strip() and not line.startswith((" ", "\t", ">")):
            active_ordered_indents.clear()
    return rows


def table_signature(body: str) -> list[int]:
    _, prose = parse_fenced_blocks(body)
    return [
        len(re.findall(r"(?<!\\)\|", line))
        for line in prose.splitlines()
        if line.lstrip().startswith("|")
    ]


def technical_list_labels(body: str) -> list[str]:
    _, prose = parse_fenced_blocks(body)
    labels: list[str] = []
    pattern = re.compile(
        r"^\s*[-+*]\s+"
        r"([A-Z][A-Za-z0-9_]*(?:,\s*[A-Z][A-Za-z0-9_]*)*)"
        r"\s+-\s+"
    )
    for line in prose.splitlines():
        match = pattern.match(line)
        if match:
            labels.append(match.group(1))
    return labels


def technical_table_cells_preserved(source_body: str, target_body: str) -> bool:
    def rows(body: str) -> list[list[str]]:
        _, prose = parse_fenced_blocks(body)
        return [
            [cell.strip() for cell in line.split("|")[1:-1]]
            for line in prose.splitlines()
            if line.lstrip().startswith("|")
        ]

    source_rows = rows(source_body)
    target_rows = rows(target_body)
    if len(source_rows) != len(target_rows):
        return False
    headers = {"Method", "Request", "Response", "Type", "Description", "Field", "Name", "Value", "Action"}
    technical = re.compile(r"^\(?[A-Za-z_][A-Za-z0-9_.]*\)?$")
    for source_cells, target_cells in zip(source_rows, target_rows, strict=True):
        if len(source_cells) != len(target_cells):
            return False
        for source_cell, target_cell in zip(source_cells, target_cells, strict=True):
            if technical.fullmatch(source_cell) and source_cell not in headers:
                if source_cell != target_cell:
                    return False
    return True


def blockquote_signature(body: str) -> list[tuple[str, int]]:
    _, prose = parse_fenced_blocks(body)
    blocks: list[tuple[str, int]] = []
    tag = ""
    depth = 0
    in_quote = False
    for line in prose.splitlines():
        match = re.match(r"^\s*(>+)\s?(.*)$", line)
        if match:
            in_quote = True
            depth = max(depth, len(match.group(1)))
            admonition = re.match(r"\[!([A-Za-z]+)\]", match.group(2))
            if admonition:
                tag = admonition.group(1).upper()
        elif in_quote:
            blocks.append((tag, depth))
            tag = ""
            depth = 0
            in_quote = False
    if in_quote:
        blocks.append((tag, depth))
    return blocks


def rendered_heading_ids(source: Path, expected_levels: list[int] | None = None) -> list[str]:
    relative = source.relative_to(CONTENT)
    if source.name in {"_index.md", "index.md"}:
        route = relative.parent
    else:
        route = relative.with_suffix("")
    rendered = PROJECT / "public" / route / "index.html"
    if not rendered.is_file():
        raise ValueError(f"missing rendered English page used for anchors: {rendered}")
    document = rendered.read_text(encoding="utf-8", errors="replace")
    rendered = [
        (int(level), html.unescape(value))
        for level, value in re.findall(r'<h([1-6])[^>]*\sid="([^"]+)"', document)
    ]
    if expected_levels is not None and len(rendered) != len(expected_levels):
        for start in range(0, len(rendered) - len(expected_levels) + 1):
            window = rendered[start : start + len(expected_levels)]
            if [level for level, _ in window] == expected_levels:
                return [value for _, value in window]
    return [value for _, value in rendered]


def residual_english(body: str, *, include_indented: bool = False) -> list[tuple[int, str]]:
    _, prose = parse_fenced_blocks(body)
    prose = re.sub(r"<!--.*?-->", "", prose, flags=re.DOTALL)
    prose = re.sub(r"<pre\b.*?</pre>", "", prose, flags=re.DOTALL | re.IGNORECASE)
    problems: list[tuple[int, str]] = []
    for number, line in enumerate(prose.splitlines(), 1):
        stripped = line.strip()
        if (
            not stripped
            or (not include_indented and line.startswith(("    ", "\t")))
            or REFERENCE_DEF_RE.match(stripped)
        ):
            continue
        stripped = INLINE_CODE_RE.sub("", stripped)
        stripped = re.sub(r"https?://\S+", "", stripped)
        stripped = re.sub(r"</?[A-Za-z][^>]*>", "", stripped)
        stripped = re.sub(r"\{\{[%<].*?[>%]\}\}", "", stripped)
        stripped = re.sub(r"\{#[^}]+\}", "", stripped)
        words = ENGLISH_WORD_RE.findall(stripped.lower())
        function_words = sum(word in ENGLISH_FUNCTION_WORDS for word in words)
        han = len(re.findall(r"[\u3400-\u9fff]", stripped))
        # Eight lowercase words with several grammatical words is almost always
        # untranslated prose, while API signatures and keyword matrices do not match.
        if len(words) >= 8 and function_words >= 3 and han < len(words):
            problems.append((number, line[:240]))
    return problems


def normalize_numbers(value: str) -> Counter[str]:
    value = re.sub(r"([\u3400-\u9fff])(?=\d)", r"\1 ", value)
    value = re.sub(r"(?<=\d)([\u3400-\u9fff])", r" \1", value)
    cluster_chinese_numbers = {"单": 1, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    value = re.sub(
        r"(?<![任每某])([单一二两三四五六七八九十])(?=成员|节点|服务器)",
        lambda match: str(cluster_chinese_numbers[match.group(1)]),
        value,
    )
    value = re.sub(r"\betcd(\d+(?:\.\d+)+)", r"etcd \1", value, flags=re.IGNORECASE)
    value = re.sub(r"\bNote(\d+)\b", r"Note \1", value, flags=re.IGNORECASE)
    value = re.sub(r"\bPython(\d+(?:\.\d+)+)", r"Python \1", value, flags=re.IGNORECASE)
    value = re.sub(r"\bday-2\b", "day-two", value, flags=re.IGNORECASE)
    cluster_number_words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
    value = re.sub(
        r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\s+(?=(?:(?:disconnected|active|voting|non-voting|new|healthy|unhealthy)\s+)?(?:members?|followers?|leaders?|nodes?)\b)",
        lambda match: str(cluster_number_words[match.group(1).lower()]) + " ",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(r"\bHTTP/?(\d+(?:\.\d+)*)", r"HTTP \1", value, flags=re.IGNORECASE)
    value = re.sub(r"\bend-2-end\b", "end-to-end", value, flags=re.IGNORECASE)
    value = re.sub(r"(?<!\w)(\d+(?:\.\d+)?)x\b", r"\1", value, flags=re.IGNORECASE)
    value = re.sub(
        r"(?<!\w)(\d+(?:\.\d+)?)\s*(kb|mb|gb|tb)\b",
        lambda match: match.group(1) + {"kb": "kB", "mb": "MB", "gb": "GB", "tb": "TB"}[match.group(2).lower()],
        value,
        flags=re.IGNORECASE,
    )
    hardware_numbers = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
    value = re.sub(
        r"\b(\d+)x\s+(?:dedicated\s+)?(?=(?:local\s+)?(?:SSDs?|disks?|CPUs?)\b)",
        r"\1 ",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:dedicated\s+)?(?=(?:local\s+)?(?:SSDs?|disks?|CPUs?)\b)",
        lambda match: str(hardware_numbers[match.group(1).lower()]) + " ",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(r"\{#[^}]+\}", "", value)
    value = re.sub(r"\b([1-5]\d\d)s\b", r"\1 responses", value)
    value = re.sub(r"\bRFC\s*(\d+)\b", r"RFC \1", value, flags=re.IGNORECASE)
    value = re.sub(
        r"\b(TLS|SSL)v?(\d+(?:\.\d+)+)",
        r"\1 \2",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"(?<!\w)(\d+)\s+first\s+bytes\b",
        r"\1B first",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"(?<!\w)(\d+)\s+to\s+(\d+)\s+extra\s+bytes\b",
        r"\1 to \2B extra",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"\badds\s+(\d+)\s+bytes([^.]{0,100}?)\band\s+(\d+)\s+for\b",
        lambda match: f"adds {match.group(1)}B{match.group(2)} and {match.group(3)}B for",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(r"\b0-?rtt\b", "ZERORTT", value, flags=re.IGNORECASE)
    value = re.sub(
        r"(\d+)\s+segments?\s+of\s+(\d+)\s+each",
        r"\1 segments of \2B each",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"(?<!\w)(\d+(?:\.\d+)?)\s*-\s*(ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB|%)\b",
        r"\1\2",
        value,
    )
    value = re.sub(
        r"(?<!\w)(\d+(?:\.\d+)?)\s*[-~～]\s*(\d+(?:\.\d+)?)\s*(ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB|%)",
        r"\1\3-\2\3",
        value,
    )
    months = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12,
    }
    value = re.sub(
        r"\b(" + "|".join(months) + r")\b",
        lambda match: str(months[match.group(1)]),
        value,
    )
    value = re.sub(r"\bzero\b", "0", value, flags=re.IGNORECASE)
    value = re.sub(
        r"\ba\s+(?=seconds?|minutes?|hours?|days?\b)",
        "1 ",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"(?<!\w)(\d+(?:\.\d+)?)\s+or\s+more\s+(seconds?|milliseconds?|minutes?|hours?|days?|bytes?)\b",
        r"\1 \2 or more",
        value,
        flags=re.IGNORECASE,
    )
    chinese_unit_numbers = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    def chinese_tens(match: re.Match[str]) -> str:
        raw = match.group(1)
        before, _, after = raw.partition("十")
        tens = chinese_unit_numbers.get(before, 1) if before else 1
        ones = chinese_unit_numbers.get(after, 0) if after else 0
        return str(tens * 10 + ones)
    value = re.sub(
        r"([一二三四五六七八九]?十[一二三四五六七八九]?)(?=纳秒|微秒|毫秒|秒|分钟|小时|天|字节)",
        chinese_tens,
        value,
    )
    value = re.sub(
        r"([一二两三四五六七八九十])\s*(?=纳秒|微秒|毫秒|秒|分钟|小时|天|字节)",
        lambda match: str(chinese_unit_numbers[match.group(1)]),
        value,
    )
    value = re.sub(r"\bpower\s+of\s+two\b", "power of 2", value, flags=re.IGNORECASE)
    value = re.sub(
        r"(\d+)\s+bytes(\s+[^.]{0,120}?\bor\s+)(\d+)(\s+when\b)",
        r"\1 bytes\2\3B\4",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"\bbetween\s+one\s+and\s+two\b",
        "between 1 and 2",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"\bbetween\s+once\s+to\s+twice\b",
        "between 1 and 2 times",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"(\d+(?:\.\d+)?)\s*(纳秒|微秒|毫秒|秒|分钟|小时|天|字节)\s*(或|和|与|、)\s*(\d+(?:\.\d+)?)\s*\2",
        r"\1 \3 \4 \2",
        value,
    )
    unit_words = {
        "nanoseconds": "ns", "nanosecond": "ns",
        "microseconds": "us", "microsecond": "us",
        "milliseconds": "ms", "millisecond": "ms",
        "seconds": "s", "second": "s",
        "minutes": "min", "minute": "min",
        "hours": "h", "hour": "h",
        "days": "d", "day": "d",
        "bytes": "B", "byte": "B",
    }
    small_number_words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
    value = re.sub(
        r"\b(one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)\s+(?=(?:" + "|".join(unit_words) + r"|ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB)\b)",
        lambda match: str(small_number_words[match.group(1).lower()]) + " ",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"(\d+(?:\.\d+)?)\s+(nanoseconds?|microseconds?|milliseconds?|seconds?|minutes?|hours?|days?|bytes?)\s+(or|and)\s+(\d+(?:\.\d+)?)\s+\2",
        r"\1 \3 \4 \2",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"\bbetween\s+(\d+(?:\.\d+)?)\s+(?:and|to)\s+(\d+(?:\.\d+)?)(ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB|%)\b",
        lambda match: f"between {match.group(1)}{match.group(3)} and {match.group(2)}{match.group(3)}",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"(?<!\w)(\d+(?:\.\d+)?)\s*-?\s*(" + "|".join(unit_words) + r")\b",
        lambda match: match.group(1) + unit_words[match.group(2).lower()],
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"(\bstarting\s+(?:at|from)\s+)one\b",
        r"\g<1>1",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"(\b(?:incremented|decremented)\s+)once\b",
        r"\g<1>1",
        value,
        flags=re.IGNORECASE,
    )
    def scaled(match: re.Match[str]) -> str:
        multipliers = {
            "thousand": Decimal(1_000),
            "million": Decimal(1_000_000),
            "billion": Decimal(1_000_000_000),
            "万": Decimal(10_000),
            "亿": Decimal(100_000_000),
        }
        number = Decimal(match.group(1)) * multipliers[match.group(2).lower()]
        rendered = format(number, "f")
        return rendered.rstrip("0").rstrip(".") if "." in rendered else rendered

    value = re.sub(
        r"\b(?:a|one)\s+(\d+)(?:st|nd|rd|th)\s+of\b",
        lambda match: f"1/{match.group(1)}",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(r"(?<!\w)(\d+)(?:st|nd|rd|th)\b", r"\1", value)
    bit_words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8}
    value = re.sub(
        r"\b(one|two|three|four|five|six|seven|eight)\s+(?=bits?\b)",
        lambda match: str(bit_words[match.group(1).lower()]) + " ",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"\b(one|two|three|four|five|six|seven|eight)\s+((?:upper|lower|high|low)\s+)(?=bits?\b)",
        lambda match: str(bit_words[match.group(1).lower()]) + " " + match.group(2),
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(
        r"\b(one|two|three|four|five|six|seven|eight)\s+((?:upper|lower|high|low)\s+)(?=(?:are|were)\b)",
        lambda match: str(bit_words[match.group(1).lower()]) + " " + match.group(2),
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(r"(?<!\w)(\d+)\s*-?\s*bits?\b", r"\1", value, flags=re.IGNORECASE)
    value = re.sub(r"(?<![\w.])(\d+(?:\.\d+)?)\s*-?\s*(thousand|million|billion|万|亿)(?![A-Za-z])", scaled, value, flags=re.IGNORECASE)
    unit_aliases = {"纳秒": "ns", "微秒": "us", "毫秒": "ms", "秒": "s", "分钟": "min", "小时": "h", "天": "d", "字节": "B"}
    tokens = []
    for token in NUMBER_RE.findall(value):
        token = token.replace(" ", "")
        if token.endswith("KB"):
            token = token[:-2] + "kB"
        if re.fullmatch(r"[vV]\d+(?:\.\d+)+(?:[-+][A-Za-z0-9.-]+)?", token):
            token = token[1:]
        for localized, canonical in unit_aliases.items():
            if token.endswith(localized):
                token = token[: -len(localized)] + canonical
                break
        tokens.append(token)
    return Counter(tokens)


def validate_pair(source: Path, target: Path, errors: list[str]) -> None:
    label = str(source.relative_to(PROJECT))
    try:
        english = source.read_text(encoding="utf-8")
        chinese = target.read_text(encoding="utf-8")
        en_front, en_body = split_front_matter(english)
        zh_front, zh_body = split_front_matter(chinese)
        en_blocks, en_prose = parse_fenced_blocks(en_body)
        zh_blocks, zh_prose = parse_fenced_blocks(zh_body)
    except (OSError, ValueError) as exc:
        errors.append(f"{label}: {exc}")
        return

    for key in ("weight", "icon", "module", "upstream_link", "upstream_name", "upstream_ref"):
        if front_value(en_front, key) != front_value(zh_front, key):
            errors.append(f"{label}: front matter {key} changed")

    if en_blocks != zh_blocks:
        errors.append(f"{label}: fenced code or literal output changed")
    if html_comments(en_body) != html_comments(zh_body):
        errors.append(f"{label}: HTML comments changed")
    if HTML_TAG_RE.findall(en_prose) != HTML_TAG_RE.findall(zh_prose):
        errors.append(f"{label}: HTML tag sequence changed")
    if FOOTNOTE_RE.findall(en_prose) != FOOTNOTE_RE.findall(zh_prose):
        errors.append(f"{label}: footnote references changed")
    if list_signature(en_body) != list_signature(zh_body):
        errors.append(f"{label}: Markdown list marker sequence changed")
    if table_signature(en_body) != table_signature(zh_body):
        errors.append(f"{label}: Markdown table shape changed")
    if (
        source == CONTENT / "etcd" / "learning" / "api.md"
        and technical_list_labels(en_body) != technical_list_labels(zh_body)
    ):
        errors.append(f"{label}: API or field labels changed")
    if (
        source == CONTENT / "etcd" / "dev-guide" / "api_reference_v3.md"
        and not technical_table_cells_preserved(en_body, zh_body)
    ):
        errors.append(f"{label}: generated API table identifiers changed")
    if blockquote_signature(en_body) != blockquote_signature(zh_body):
        errors.append(f"{label}: blockquote structure changed")
    source_inline = [
        literal
        for literal in INLINE_CODE_RE.findall(en_prose)
        if re.search(r"[A-Za-z0-9_/.-]", literal.strip("`"))
    ]
    missing_inline = Counter(source_inline) - Counter(INLINE_CODE_RE.findall(zh_prose))
    if missing_inline:
        errors.append(f"{label}: inline code literals missing: {list(missing_inline.elements())[:12]}")

    component = source.relative_to(CONTENT).parts[0]
    if link_targets(en_body, component) != link_targets(zh_body, component):
        errors.append(f"{label}: link or asset targets changed")
    localized_assets = [
        target
        for target in link_targets(zh_body, component, normalize=False)
        if re.match(
            rf"^/zh/{re.escape(component)}/.*\.(?:png|gif|svg|json|txt)(?:[?#].*)?$",
            target,
            flags=re.IGNORECASE,
        )
    ]
    if localized_assets:
        errors.append(f"{label}: shared asset paths must not have a language prefix")

    en_headings = heading_rows(en_body)
    zh_headings = heading_rows(zh_body)
    if [level for level, _ in en_headings] != [level for level, _ in zh_headings]:
        errors.append(f"{label}: heading level sequence changed")
    else:
        if component == "haproxy":
            expected_ids = [anchor for _, anchor in en_headings]
        else:
            try:
                expected_ids = rendered_heading_ids(
                    source, [len(level) for level, _ in en_headings]
                )
            except ValueError as exc:
                errors.append(f"{label}: {exc}")
                expected_ids = []
        actual_ids = [anchor for _, anchor in zh_headings]
        if expected_ids != actual_ids:
            errors.append(f"{label}: translated heading anchors do not preserve English IDs")

    residual = residual_english(zh_body, include_indented=component == "etcd")
    for line_number, excerpt in residual[:8]:
        errors.append(f"{label}:{line_number}: probable untranslated prose: {excerpt}")
    if len(residual) > 8:
        errors.append(f"{label}: {len(residual) - 8} more probable untranslated prose lines")

    forbidden = {
        "etcd": (
            "领导人", "领导者节点", "主节点", "租赁契约", "多数派人数",
            "观察者", "身份验证", "本文件", "您",
        ),
        "haproxy": (
            "样品提取", "样本获取", "棍表", "黏性表", "后端计算机",
            "前端计算机", "故障排除", "选项家族", "TLS 门票", "OCSP 信封",
            "身份验证", "您",
        ),
    }
    for phrase in forbidden[component]:
        if phrase in chinese:
            errors.append(f"{label}: forbidden inconsistent term {phrase!r}")
    if component == "etcd" and re.search(r"学习者(?!成员)", chinese):
        errors.append(f"{label}: learner must be translated as '学习者成员'")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("components", nargs="*", choices=COMPONENTS, default=list(COMPONENTS))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    pair_count = 0
    for component in args.components:
        for source in sorted(
            path
            for path in (CONTENT / component).rglob("*.md")
            if not path.name.endswith(".zh.md")
        ):
            target = source.with_name(source.stem + ".zh.md")
            if not target.is_file():
                errors.append(f"missing translation: {target.relative_to(PROJECT)}")
                continue
            pair_count += 1
            validate_pair(source, target, errors)

    if errors:
        print("Component translation validation failed:", file=sys.stderr)
        for error in errors[:300]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 300:
            print(f"- ... {len(errors) - 300} more", file=sys.stderr)
        return 1
    print(f"Validated {pair_count} HAProxy/etcd translation pairs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
