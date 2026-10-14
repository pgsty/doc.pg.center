#!/usr/bin/env python3
"""Verify all Japanese HAProxy pages against current working-tree English.

This is a structural and technical-content gate, separate from semantic review.
Every exception names an exact section/check and both reviewed text hashes.
"""
from __future__ import annotations

import argparse
from collections import Counter
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

PROJECT = Path(__file__).resolve().parent.parent
DOCS = PROJECT / "content/docs"
ROOT = DOCS / "haproxy"
spec = importlib.util.spec_from_file_location("component_structure", PROJECT / "scripts/check-component-translations.py")
assert spec and spec.loader
structure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(structure)
JAPANESE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
ANCHOR = re.compile(r'^<a\s+id="([^"]+)"\s*></a>\s*$')
NATURAL_FIELDS = {"title", "linkTitle", "description", "categories", "summary"}
NUMBER = re.compile(r"(?:(?<![A-Za-z0-9_])[-+])?\d+(?:,\d{3})*(?:\.\d+)*")
PLACEHOLDER = re.compile(r"__PGSQL_[A-Z0-9_]+__|\b(?:TODO_TRANSLATE|TRANSLATION_PENDING)\b")
UNITS = {
    "nanoseconds": "ns", "nanosecond": "ns", "ナノ秒": "ns",
    "microseconds": "us", "microsecond": "us", "マイクロ秒": "us",
    "milliseconds": "ms", "millisecond": "ms", "ミリ秒": "ms",
    "seconds": "s", "second": "s", "秒": "s",
    "minutes": "min", "minute": "min", "分": "min",
    "hours": "h", "hour": "h", "時間": "h",
    "days": "d", "day": "d", "日": "d",
    "bytes": "B", "byte": "B", "バイト": "B",
    "bits": "bit", "bit": "bit", "ビット": "bit",
    "percent": "%", "パーセント": "%", "％": "%", "KB": "kB",
}
for unit in ("ns", "us", "ms", "s", "min", "h", "d", "B", "kB", "MB", "GB", "TB", "KiB", "MiB", "GiB", "TiB", "bps", "kbps", "Mbps", "Gbps", "Hz", "kHz", "MHz", "GHz", "%"):
    UNITS[unit] = unit
QUANTITY = re.compile(r"((?:(?<![A-Za-z0-9_])[-+])?\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:-\s*)?(" + "|".join(re.escape(unit) for unit in sorted(UNITS, key=len, reverse=True)) + r")(?![A-Za-z])")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def english(path: Path) -> bool:
    return not path.name.endswith(tuple(f".{language}.md" for language in ("zh", "fr", "ja", "de", "ru")))


def normalize_links(text: str) -> str:
    return text.replace("/ja/docs/haproxy/", "/docs/haproxy/")


def metadata_structure(front: str) -> list[str]:
    result, skipping = [], False
    for line in front.splitlines():
        key = re.match(r"^([A-Za-z_][\w-]*):", line)
        if key:
            skipping = key.group(1) in NATURAL_FIELDS
            if skipping:
                result.append(key.group(1) + ": <localized>")
        if not skipping and line.strip():
            result.append(line)
    return result


def sections(body: str) -> dict[str, str]:
    result, current, marker = {"preamble": []}, "preamble", ""
    for line in body.splitlines(keepends=True):
        if marker:
            result[current].append(line)
            if line.lstrip().startswith(marker):
                marker = ""
            continue
        fence = structure.FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
        else:
            heading, anchor = structure.HEADING_RE.match(line), ANCHOR.match(line)
            key = heading.group("anchor") if heading else (anchor.group(1) if anchor else None)
            if key:
                if key in result:
                    raise ValueError(f"duplicate section ID: {key}")
                current, result[key] = key, []
        result[current].append(line)
    return {key: "".join(lines) for key, lines in result.items()}


def prose_text(body: str) -> str:
    _, prose = structure.parse_fenced_blocks(body)
    return re.sub(r"<!--.*?-->", "", prose, flags=re.S)


def visible_text(body: str) -> str:
    text = structure.INLINE_CODE_RE.sub("", prose_text(body))
    text = re.sub(r"\]\([^\n)]*\)", "]", text)
    return re.sub(r"<[^>\n]*>|https?://\S+|\{#[^}]+\}", "", text)


def numeric_tokens(body: str) -> Counter[str]:
    text = visible_text(body)
    scales = {"thousand": 1000, "million": 1000000, "billion": 1000000000, "千": 1000, "万": 10000, "億": 100000000}
    text = re.sub(r"(\d+(?:\.\d+)?)\s*(thousand|million|billion|千|万|億)", lambda m: format((Decimal(m[1]) * scales[m[2]]).normalize(), "f"), text)
    text = re.sub(r"(?<=\d)[-–〜～](?=\d)", " ", text)
    return Counter(token.replace(",", "") for token in NUMBER.findall(text))


def quantity_tokens(body: str) -> Counter[str]:
    text = re.sub(r"(?<=\d)[-–〜～](?=\d)", " ", visible_text(body))
    text = re.sub(r"(\d+)\s+(?:lowest|highest)\s+(bits?|bytes?)\b", r"\1 \2", text)
    text = re.sub(r"(\d+)\s+or\s+(?:more|less)\s+", r"\1 ", text)
    # In Japanese fractions such as 256分の一, 分 is not a minute unit.
    text = re.sub(r"(\d+)\s*分(?=の)", r"\1 fraction", text)
    return Counter(number.replace(",", "") + UNITS[unit] for number, unit in QUANTITY.findall(text))


def absolute_urls(body: str) -> Counter[str]:
    pattern = r'''\b(?:https?|ftp)://[^\s<>`"'\u3000-\u30ff\u3400-\u9fff]+'''
    return Counter(value.rstrip(".,;:!?)]}") for value in re.findall(pattern, normalize_links(body)))


def paragraph_count(body: str) -> int:
    prose = re.sub(r"(?m)^#{1,6} .*?$|^<a\b[^\n]*$", "", prose_text(body))
    return sum(bool(block.strip()) for block in re.split(r"\n\s*\n", prose))


def english_residuals(body: str) -> list[str]:
    result = []
    for line in visible_text(body).splitlines():
        text = line.strip()
        if not text or structure.REFERENCE_DEF_RE.match(text):
            continue
        words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
        grammar = sum(word.lower() in structure.ENGLISH_FUNCTION_WORDS for word in words)
        if (len(words) >= 4 and grammar >= 2 and not JAPANESE.search(text)) or re.fullmatch(r"[\s#>*_:.-]*(?:Examples?|Notes?|Warning|See also|where|Arguments|Default value|Description|Usage|Options)[\s:*.：-]*", text, re.I):
            result.append(line)
    return result


class Audit:
    def __init__(self, component: str = "haproxy") -> None:
        path = PROJECT / "data/translation-checks" / f"{component}-ja.json"
        self.exceptions = json.loads(path.read_text()).get("exceptions", []) if path.exists() else []
        self.used, self.errors, self.pages = set(), [], []

    def exception(self, check: str, source: str, target: str, path: str, section: str):
        for index, entry in enumerate(self.exceptions):
            if (entry.get("path"), entry.get("section"), entry.get("check")) == (path, section, check) and entry.get("reason") and entry.get("source_sha256") == digest(source) and entry.get("target_sha256") == digest(target):
                return index, entry
        return None

    def compare(self, check: str, source: str, target: str, actual, expected, path: str, section: str = "page") -> None:
        if actual == expected:
            return
        exception = self.exception(check, source, target, path, section)
        if exception:
            self.used.add(exception[0])
            return
        if isinstance(actual, Counter) and isinstance(expected, Counter):
            detail = f"missing={dict(expected - actual)}, extra={dict(actual - expected)}"
        elif check == "English prose":
            detail = repr(actual)
        else:
            detail = f"expected={str(expected)[:180]}, actual={str(actual)[:180]}"
        self.errors.append(f"{path}#{section}: {check}; {detail}")


def validate_explanatory_fence(source: str, target: str, path: str, section: str, audit: Audit) -> None:
    """A prose exception never permits changes to the protected parts of a block."""
    exception = audit.exception("fenced code/configuration/output", source, target, path, section)
    if not exception:
        return
    entry = exception[1]
    if entry.get("classification") not in {"explanatory prose", "mixed table", "explanatory prose/mixed table"}:
        audit.errors.append(f"{path}#{section}: explanation exception needs a specific prose/table classification")
    source_lines, target_lines = source.splitlines(), target.splitlines()
    if (source_lines[0], source_lines[-1]) != (target_lines[0], target_lines[-1]):
        audit.errors.append(f"{path}#{section}: explanatory fence markers/language changed")
    en, ja = "\n".join(source_lines[1:-1]), "\n".join(target_lines[1:-1])
    for field in ("protected_literals", "protected_lines"):
        values = entry.get(field)
        if not isinstance(values, list) or any(not isinstance(value, str) or not value for value in values):
            audit.errors.append(f"{path}#{section}: {field} must be an explicit string list")
            continue
        for value in values:
            if field == "protected_lines":
                before, after = source_lines.count(value), target_lines.count(value)
            else:
                before, after = source.count(value), target.count(value)
            if not before or before != after:
                audit.errors.append(f"{path}#{section}: protected literal/line changed: {value!r}")
    for name, pattern in (
        ("argument placeholders", r"<[A-Za-z_][A-Za-z0-9_.:/+*-]*>"),
        ("inline literals", r"`+[^`\n]*`+"),
        ("quoted literals", r'"[^"\n]*"'),
    ):
        audit.compare("fenced " + name, source, target, Counter(re.findall(pattern, ja)), Counter(re.findall(pattern, en)), path, section)
    for name, actual, expected in (
        ("numeric facts", numeric_tokens(ja), numeric_tokens(en)),
        ("numeric units", quantity_tokens(ja), quantity_tokens(en)),
    ):
        audit.compare("fenced " + name, source, target, actual, expected, path, section)
    # Program output and actual code lines explicitly reviewed above are allowed
    # to remain English. Narrative in the remainder still needs translation.
    reviewed_lines = set(entry.get("protected_lines", []))
    prose = "\n".join(line for line in target_lines[1:-1] if line not in reviewed_lines)
    prose = re.sub(r'"[^"\n]*"', "", prose)
    audit.compare("fenced English prose", source, target, english_residuals(prose), [], path, section)


def validate_pair(source: Path, target: Path, audit: Audit) -> None:
    path = str(source.relative_to(DOCS))
    en_text, ja_text = source.read_text(), target.read_text()
    en_front, en_body = structure.split_front_matter(en_text)
    ja_front, ja_body = structure.split_front_matter(ja_text)
    compare = lambda name, actual, expected: audit.compare(name, en_text, ja_text, actual, expected, path)
    compare("protected metadata", metadata_structure(ja_front), metadata_structure(en_front))
    for key in NATURAL_FIELDS:
        en_values, ja_values = structure.front_value(en_front, key), structure.front_value(ja_front, key)
        compare(f"{key} field count", len(ja_values), len(en_values))
        if key in {"description", "summary"} and ja_values and not JAPANESE.search(" ".join(ja_values)):
            audit.errors.append(f"{path}: {key} has no Japanese prose")
    en_blocks, en_prose = structure.parse_fenced_blocks(en_body)
    ja_blocks, ja_prose = structure.parse_fenced_blocks(ja_body)
    compare("fenced block count", len(ja_blocks), len(en_blocks))
    for number, (en, ja) in enumerate(zip(en_blocks, ja_blocks), 1):
        audit.compare("fenced code/configuration/output", en, ja, ja, en, path, f"fence-{number:04d}")
        if en != ja:
            validate_explanatory_fence(en, ja, path, f"fence-{number:04d}", audit)
    checks = (
        ("HTML comments", structure.html_comments(ja_body), structure.html_comments(en_body)),
        ("HTML tags", structure.HTML_TAG_RE.findall(normalize_links(ja_prose)), structure.HTML_TAG_RE.findall(en_prose)),
        ("heading levels and English IDs", structure.heading_rows(ja_body), structure.heading_rows(en_body)),
        ("list sequence and indentation", structure.list_signature(ja_body), structure.list_signature(en_body)),
        ("table rows and columns", structure.table_signature(ja_body), structure.table_signature(en_body)),
        ("blockquote/admonition structure", structure.blockquote_signature(ja_body), structure.blockquote_signature(en_body)),
        ("footnote references", structure.FOOTNOTE_RE.findall(ja_prose), structure.FOOTNOTE_RE.findall(en_prose)),
        ("shortcodes", re.findall(r"\{\{[%<].*?[>%]\}\}", ja_body, re.S), re.findall(r"\{\{[%<].*?[>%]\}\}", en_body, re.S)),
        ("link and asset targets", Counter(structure.link_targets(normalize_links(ja_body), "haproxy", normalize=False)), Counter(structure.link_targets(en_body, "haproxy", normalize=False))),
        ("absolute URL literals", absolute_urls(ja_body), absolute_urls(en_body)),
        ("reference definitions", [line for line in normalize_links(ja_body).splitlines() if structure.REFERENCE_DEF_RE.match(line)], [line for line in en_body.splitlines() if structure.REFERENCE_DEF_RE.match(line)]),
        ("translation placeholders", PLACEHOLDER.findall(ja_prose), []),
    )
    for name, actual, expected in checks:
        compare(name, actual, expected)
    if any(anchor is None for _, anchor in structure.heading_rows(en_body)):
        audit.errors.append(f"{path}: implicit source heading ID needs production-rendered verification")
    for destination in structure.link_targets(ja_body, "haproxy", normalize=False):
        if re.match(r"^/docs/haproxy/(?:[^.]*)(?:#.*)?$", destination):
            audit.errors.append(f"{path}: component link still uses English: {destination}")
        if re.match(r"^/ja/(?:third_party|img|images)/", destination):
            audit.errors.append(f"{path}: shared asset has a language prefix: {destination}")
    en_sections, ja_sections = sections(en_body), sections(ja_body)
    compare("section/entry ID sequence", list(ja_sections), list(en_sections))
    for section, en in en_sections.items():
        if section not in ja_sections:
            continue
        ja = ja_sections[section]
        for name, actual, expected in (
            ("inline technical literals", Counter(structure.INLINE_CODE_RE.findall(prose_text(ja))), Counter(structure.INLINE_CODE_RE.findall(prose_text(en)))),
            ("numeric facts", numeric_tokens(ja), numeric_tokens(en)),
            ("numeric units", quantity_tokens(ja), quantity_tokens(en)),
            ("paragraph structure", paragraph_count(ja), paragraph_count(en)),
            ("English prose", english_residuals(ja), []),
        ):
            audit.compare(name, en, ja, actual, expected, path, section)
    audit.pages.append({"path": path, "source_sha256": digest(en_text), "target_sha256": digest(ja_text), "sections": len(en_sections), "code_blocks": len(en_blocks), "unchanged_fences": [number for number, (en, ja) in enumerate(zip(en_blocks, ja_blocks), 1) if en == ja], "divider": source.name.startswith("_div_")})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", action="append", help="check only these English filenames (diagnostic subset, not component acceptance)")
    parser.add_argument("--report", type=Path, help="save full results outside the repository")
    parser.add_argument("--require-review", action="store_true", help="also require a complete separate semantic review tied to the exact source and translation")
    args = parser.parse_args()
    audit = Audit()
    sources = sorted(path for path in ROOT.glob("*.md") if english(path))
    if args.page:
        known = {source.name for source in sources}
        audit.errors.extend(f"unknown source: {name}" for name in set(args.page) - known)
        sources = [source for source in sources if source.name in args.page]
    else:
        for target in ROOT.glob("*.ja.md"):
            if not target.with_name(target.name.removesuffix(".ja.md") + ".md").is_file():
                audit.errors.append(f"orphan Japanese page: {target}")
    for source in sources:
        target = source.with_suffix(".ja.md")
        if not target.is_file():
            audit.errors.append(f"missing Japanese page: {target.relative_to(PROJECT)}")
            continue
        try:
            validate_pair(source, target, audit)
        except (OSError, ValueError) as exc:
            audit.errors.append(f"{source.name}: {exc}")
    for index, entry in enumerate(audit.exceptions):
        if index not in audit.used and entry.get("check") != "rendered explanatory block" and any(page["path"] == entry.get("path") for page in audit.pages):
            audit.errors.append(f"unused/stale review exception: {entry.get('path')}#{entry.get('section')} {entry.get('check')}")
    if args.require_review:
        review_path = PROJECT / "data/translation-audits/haproxy-ja.json"
        review = json.loads(review_path.read_text()) if review_path.is_file() else {}
        rows = review.get("pages", [])
        records = {item.get("path"): item for item in rows}
        if len(records) != len(rows):
            audit.errors.append("duplicate semantic review records")
        for page in audit.pages:
            record = records.get(page["path"], {})
            if not (
                record.get("status") == "reviewed"
                and record.get("method") == "separate full source-target comparison"
                and record.get("notes")
                and record.get("source_sha256") == page["source_sha256"]
                and record.get("target_sha256") == page["target_sha256"]
            ):
                audit.errors.append(f"{page['path']}: missing or stale complete semantic review")
            fences = record.get("fences", {})
            verbatim, explanatory = fences.get("verbatim", []), fences.get("explanatory", [])
            if sorted(verbatim + explanatory) != list(range(1, page["code_blocks"] + 1)):
                audit.errors.append(f"{page['path']}: every fenced block must be individually classified as verbatim content or translatable explanation")
            elif sorted(verbatim) != page["unchanged_fences"]:
                audit.errors.append(f"{page['path']}: untranslated explanation or changed protected block in the reviewed fence inventory")
    scope = "selected pages" if args.page else "complete component"
    result = {"source": "current working-tree English", "scope": scope, "component": "haproxy", "semantic_review_required": args.require_review, "pages": audit.pages, "errors": audit.errors}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for error in audit.errors:
        print(error, file=sys.stderr)
    if audit.errors:
        print(f"HAProxy Japanese current-source check failed: {len(audit.errors)} errors.", file=sys.stderr)
        return 1
    published = sum(not page["divider"] for page in audit.pages)
    print(f"HAProxy Japanese current-source check passed ({scope}): {published} published pages, {len(audit.pages) - published} navigation dividers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
