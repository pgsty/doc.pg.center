#!/usr/bin/env python3
"""Check every Japanese page against CURRENT English and a recorded prose review.

The review manifest binds the separate semantic review to both file hashes.
Exact, explained exceptions cover numeric notation, English prose detection and
one source-authored natural-language quotation marked up as inline code.
Executable content and structural checks cannot be waived.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import sys

PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content" / "docs"
spec = importlib.util.spec_from_file_location(
    "component_structure", PROJECT / "scripts/etcd_structure.py"
)
structure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(structure)
LOCALE = re.compile(r"\.[A-Za-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})*\.md$")
NATURAL_FIELDS = {"title", "linkTitle", "description", "categories"}
JAPANESE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
SHORTCODE = re.compile(r"\{\{[<%].*?[>%]\}\}", re.S)
TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9:-]*(?:\s[^<>]*?)?/?>", re.S)
URL = re.compile(r"(?:https?|ftp)://[^\s<>\]\)]+")
INLINE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.S)
UNITS = {
    "nanoseconds": "ns", "nanosecond": "ns", "ナノ秒": "ns",
    "microseconds": "us", "microsecond": "us", "マイクロ秒": "us",
    "milliseconds": "ms", "millisecond": "ms", "ミリ秒": "ms",
    "seconds": "s", "second": "s", "秒": "s",
    "minutes": "min", "minute": "min", "分": "min",
    "hours": "h", "hour": "h", "時間": "h",
    "days": "d", "day": "d", "日": "d",
    "bytes": "B", "byte": "B", "バイト": "B",
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def fenced(body: str) -> tuple[list[str], str]:
    """Retain literal fences, including indented and blockquoted examples."""
    blocks, outside, current = [], [], []
    marker = ""
    for line in body.splitlines(keepends=True):
        clean = re.sub(r"^(?:\s*>[ \t]?)+", "", line)
        if marker:
            current.append(line)
            if re.fullmatch(r"\s*" + re.escape(marker[0]) + "{" + str(len(marker)) + r",}\s*", clean):
                blocks.append("".join(current))
                current, marker = [], ""
        elif match := re.match(r"\s*(`{3,}|~{3,})", clean):
            marker, current = match[1], [line]
        else:
            outside.append(line)
    if marker:
        raise ValueError("unterminated code fence")
    return blocks, "".join(outside)


# The shared structural helpers use this neutral parser, not language rules.
structure.parse_fenced_blocks = fenced


def headings(body: str) -> list[tuple[str, str | None]]:
    _, value = fenced(body)
    lines = value.splitlines()
    result = []
    for index, line in enumerate(lines):
        if match := structure.HEADING_RE.match(line):
            result.append((match["marks"], match["anchor"]))
        elif (index and re.fullmatch(r" {0,3}(?:=+|-+)\s*", line)
              and lines[index - 1].strip()
              and not re.match(r"\s*[#>*|]", lines[index - 1])):
            anchor = re.search(r"\{#([^}]+)\}\s*$", lines[index - 1])
            result.append(("#" if line.lstrip().startswith("=") else "##",
                           anchor[1] if anchor else None))
    return result


def normalize_routes(value: str) -> str:
    return re.sub(r"/ja/(?=docs/etcd(?:/|\b))", "/", value)


def front_blocks(front: str) -> dict[str, str]:
    result = {}
    key = ""
    for line in front.splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):", line)
        if match:
            key = match[1]
            if key in result:
                raise ValueError(f"duplicate metadata field: {key}")
            result[key] = []
        if key:
            result[key].append(line)
    return {key: "\n".join(lines).rstrip() for key, lines in result.items()}


def prose(body: str) -> str:
    _, body = structure.parse_fenced_blocks(body)
    body = re.sub(r"<!--.*?-->|<pre\b.*?</pre>|<code\b.*?</code>", "", body,
                  flags=re.S | re.I)
    body = INLINE.sub("", body)
    body = re.sub(r"^\s*\[[^\]\n]+\]:[^\n]*$", "", body, flags=re.M)
    body = re.sub(r"\]\([^\n)]*\)", "]", body)
    body = re.sub(r"\]\[[^\]\n]*\]", "]", body)
    body = SHORTCODE.sub("", body)
    body = URL.sub("", body)
    body = TAG.sub("", body)
    body = re.sub(r"\{#[^}]+\}", "", body)
    return html.unescape(body)


def numbers(body: str) -> Counter:
    # Historical task GIF alt text is a recording filename, not a numeric fact.
    # Descriptive/numbered figure alt text still participates in this check.
    body = re.sub(r"!\[\d{2}_etcd[^\]]*_\d{10,}\]", "![]", body)
    value = prose(body)
    for word, unit in UNITS.items():
        suffix = r"(?![A-Za-z割断散岐類])" if word == "分" else r"(?![A-Za-z])"
        value = re.sub(r"(\d)\s*" + word + suffix, r"\1" + unit, value)
    # Only notation changes are normalized. English number words, dates and
    # idioms require a page-specific, hash-bound semantic review when needed.
    return Counter(re.sub(r"^0+(?=\d)", "", token.replace(",", "").replace(" ", "")) for token in re.findall(
        r"(?:(?<![0-9A-Za-z])[-+])?\d+(?:[.,]\d+)*(?:\s*(?:GiB|MiB|KiB|GB|MB|KB|kB|TB|Gbps|Mbps|ns|us|ms|min|s|h|d|B|%)(?![A-Za-z]))?",
        value))


def english_candidates(body: str) -> list[str]:
    candidates = []
    for line in prose(body).splitlines():
        words = re.findall(r"\b[a-z]+\b", line.lower())
        grammar = sum(len(w) > 1 and w in structure.ENGLISH_FUNCTION_WORDS for w in words)
        if len(words) >= 4 and grammar >= 2:
            candidates.append(line.strip())
    return candidates


def refs(body: str) -> list[tuple[str, str]]:
    _, value = structure.parse_fenced_blocks(body)
    value = re.sub(r"^(?:\s*>[ \t]?)+", "", value, flags=re.M)
    return [(m[1].casefold(), normalize_routes(m[2])) for line in value.splitlines()
            if (m := structure.REFERENCE_DEF_RE.match(line))]


def reference_uses(body: str) -> Counter:
    _, value = structure.parse_fenced_blocks(body)
    definitions = {key for key, _ in refs(body)}
    value = re.sub(r"^(?:[ \t]*>[ \t]?)+", "", value, flags=re.M)
    value = re.sub(r"^\s*\[[^\]\n]+\]:[^\n]*$", "", value, flags=re.M)
    uses = []
    def full(match):
        uses.append((match[2] or match[1]).casefold())
        return ""
    value = re.sub(r"!?\[([^\]]*)\]\[([^\]\n]*)\]", full, value)
    value = re.sub(r"!?\[[^\]\n]*\]\([^\n)]*\)", "", value)
    for label in re.findall(r"\[([^\]\n]+)\]", value):
        if label.casefold() in definitions:
            uses.append(label.casefold())
    return Counter(uses)


def html_tags(value: str) -> list[str]:
    return [re.sub(r'\b(?:alt|title)=("[^"]*"|\x27[^\x27]*\x27)',
                   'localized=""', normalize_routes(tag)) for tag in TAG.findall(value)]


def raw_identifiers(body: str) -> Counter:
    value = prose(body)
    return Counter(re.findall(
        r"(?<![A-Za-z0-9_])(?:--[A-Za-z][A-Za-z0-9_.-]*|"
        r"[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+)(?![A-Za-z0-9_])", value))


def table_cells(body: str) -> list[list[str]]:
    return [re.split(r"(?<!\\)\|", line.strip())[1:-1]
            for line in fenced(body)[1].splitlines() if line.lstrip().startswith("|")]


def storage_table_identifiers(body: str) -> list[Counter]:
    """Protect the unquoted bucket/key/type labels in the HTML storage tables."""
    result = []
    for cell in re.findall(r"<td\b[^>]*>(.*?)</td>", body, re.S):
        plain = html.unescape(TAG.sub("", cell)).strip()
        if re.fullmatch(r'["\x27]?[A-Za-z][A-Za-z0-9_.-]*["\x27]?', plain):
            result.append(Counter([plain]))
        else:
            result.append(Counter(re.findall(
                r"(?<![A-Za-z0-9_])(?:[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+|"
                r"[a-zA-Z]*[a-z][A-Z][A-Za-z0-9]*|(?:u?int|float)\d+)(?![A-Za-z0-9_])", plain)))
    return result


def validate_pair(source: Path, target: Path, rendered: Path,
                  review: dict | None = None) -> list[str]:
    errors = []
    source_text, target_text = source.read_text(), target.read_text()
    en_front, en_body = structure.split_front_matter(source_text)
    ja_front, ja_body = structure.split_front_matter(target_text)
    en_blocks, en_prose = structure.parse_fenced_blocks(en_body)
    ja_blocks, ja_prose = structure.parse_fenced_blocks(ja_body)
    exceptions = (review or {}).get("exceptions", [])
    used = set()
    def equal(label, a, b):
        if a != b:
            errors.append(label)
    en_meta, ja_meta = front_blocks(en_front), front_blocks(ja_front)
    equal("metadata keys changed", set(en_meta), set(ja_meta))
    for key in en_meta.keys() & ja_meta.keys() - NATURAL_FIELDS:
        equal(f"protected metadata changed: {key}", en_meta[key], ja_meta[key])
    for key in ("title", "linkTitle", "description"):
        if key in ja_meta and not ja_meta[key].split(":", 1)[1].strip(' "\x27'):
            errors.append(f"empty translated metadata: {key}")
    technical_metadata = {
        ("etcd/_index.md", "linkTitle"): "etcd 3.7",
        ("etcd/learning/api.md", "title"): "etcd API",
    }
    for key in NATURAL_FIELDS & ja_meta.keys():
        value = ja_meta[key].split(":", 1)[1].strip(' "\x27')
        if not JAPANESE.search(value) and technical_metadata.get(
            (source.relative_to(CONTENT).as_posix(), key)
        ) != value:
            errors.append(f"unlocalized display metadata: {key}")
    equal("fenced code/configuration/output changed", en_blocks, ja_blocks)
    equal("HTML comments changed", structure.html_comments(en_body), structure.html_comments(ja_body))
    equal("HTML tags/attributes changed", html_tags(en_prose), html_tags(ja_prose))
    equal("HTML code/pre literals changed",
          re.findall(r"<(?:pre|code)\b.*?</(?:pre|code)>", en_prose, re.S),
          re.findall(r"<(?:pre|code)\b.*?</(?:pre|code)>", ja_prose, re.S))
    en_inline = Counter(m[0] for m in INLINE.finditer(en_prose))
    ja_inline = Counter(m[0] for m in INLINE.finditer(ja_prose))
    for i, entry in enumerate(exceptions):
        if entry.get("check") != "inline-prose":
            continue
        original, translated = entry.get("source", ""), entry.get("target", "")
        # This paper quotation describes linearizability in natural language;
        # it is neither a command nor an API identifier despite its backticks.
        if (source.relative_to(CONTENT).as_posix() == "etcd/learning/api_guarantees.md"
                and digest(original) == "edf7fcc619d7fcf33b07990ee4d280c26ecdc515f03c2d147cddccbfaebb0907"
                and en_inline[original] == ja_inline[translated] == 1
                and translated.startswith("`") and translated.endswith("`")
                and JAPANESE.search(translated) and entry.get("reason")):
            en_inline.subtract([original])
            ja_inline.subtract([translated])
            used.add(i)
    equal("inline technical literals changed", +en_inline, +ja_inline)
    missing_identifiers = raw_identifiers(en_body) - raw_identifiers(ja_body)
    if missing_identifiers:
        errors.append(f"unquoted option/field/metric identifiers missing: {dict(missing_identifiers)}")
    for label, extract in (
        ("list structure", structure.list_signature),
        ("table structure", structure.table_signature),
        ("blockquote/admonitions", structure.blockquote_signature),
        ("footnotes", structure.FOOTNOTE_RE.findall),
        ("shortcodes", lambda s: [normalize_routes(x) for x in SHORTCODE.findall(s)]),
        ("reference definitions", refs), ("reference usages", reference_uses),
    ):
        equal(label + " changed", extract(en_body), extract(ja_body))
    # Japanese syntax may reorder links in a sentence, but may not drop,
    # duplicate, redirect or localize a shared resource.
    en_links = structure.link_targets(en_body, "etcd", normalize=False)
    ja_links = structure.link_targets(ja_body, "etcd", normalize=False)
    equal("link/image/HTML targets changed", Counter(en_links),
          Counter(normalize_routes(x) for x in ja_links))
    for link in ja_links:
        if re.match(r"/ja/docs/etcd/.*\.[A-Za-z0-9]+(?:[?#].*)?$", link):
            errors.append(f"shared asset localized: {link}")
        if re.match(r"/docs/etcd/", link) and not re.search(r"\.[A-Za-z0-9]+(?:[?#].*)?$", link):
            errors.append(f"English component route: {link}")
    en_headings, ja_headings = headings(en_body), headings(ja_body)
    equal("heading levels changed", [x[0] for x in en_headings], [x[0] for x in ja_headings])
    structure.RENDERED_ROOT = rendered
    ids = structure.rendered_heading_ids(source, [len(x[0]) for x in en_headings])
    equal("English rendered heading IDs not preserved", ids, [x[1] for x in ja_headings])
    if source.name == "api_reference_v3.md" and not structure.technical_table_cells_preserved(en_body, ja_body):
        errors.append("API/RPC/field/type table identifiers changed")
    for row, (en_cells, ja_cells) in enumerate(zip(table_cells(en_body), table_cells(ja_body)), 1):
        for column, (en_cell, ja_cell) in enumerate(zip(en_cells, ja_cells), 1):
            # Word-to-digit additions are reviewed separately; an existing
            # numeric value or inline identifier may never move to another cell.
            if numbers(en_cell) - numbers(ja_cell):
                errors.append(f"numeric table value missing/moved: row {row}, column {column}")
            equal(f"inline table literal changed: row {row}, column {column}",
                  Counter(m[0] for m in INLINE.finditer(en_cell)),
                  Counter(m[0] for m in INLINE.finditer(ja_cell)))
    if source.relative_to(CONTENT).as_posix() == "etcd/learning/api.md":
        equal("API/field list labels changed", structure.technical_list_labels(en_body),
              structure.technical_list_labels(ja_body))
    if source.relative_to(CONTENT).as_posix() == "etcd/learning/persistent-storage-files.md":
        equal("storage HTML table bucket/key/type identifiers changed",
              storage_table_identifiers(en_body), storage_table_identifiers(ja_body))
    if prose(en_body).strip() and not JAPANESE.search(prose(ja_body)):
        errors.append("nonempty English body lacks Japanese prose")
    if re.search(r"\b(?:TODO|TBD|lorem ipsum)\b|翻訳中|翻訳予定|待翻译", prose(ja_body), re.I):
        errors.append("unresolved prose placeholder")

    en_natural = "\n".join(en_meta[key] for key in sorted(NATURAL_FIELDS) if key in en_meta)
    ja_natural = "\n".join(ja_meta[key] for key in sorted(NATURAL_FIELDS) if key in ja_meta)
    en_numbers, ja_numbers = numbers(en_natural + "\n" + en_body), numbers(ja_natural + "\n" + ja_body)
    if en_numbers != ja_numbers:
        missing, extra = dict(en_numbers - ja_numbers), dict(ja_numbers - en_numbers)
        for i, entry in enumerate(exceptions):
            if (entry.get("check") == "numbers" and entry.get("source_only") == missing
                    and entry.get("target_only") == extra and entry.get("reason")):
                used.add(i)
                break
        else:
            errors.append(f"numeric facts need review: source_only={missing}; target_only={extra}")
    for line in english_candidates(ja_natural + "\n" + ja_body):
        for i, entry in enumerate(exceptions):
            if entry.get("check") == "english" and entry.get("text") == line and entry.get("reason"):
                used.add(i)
                break
        else:
            errors.append(f"English prose needs review: {line}")
    if review is not None:
        for i, entry in enumerate(exceptions):
            if i not in used:
                errors.append(f"unused or invalid review exception: {entry}")
        if review.get("source_sha256") != digest(source_text):
            errors.append("semantic review does not match CURRENT English source")
        if review.get("translation_sha256") != digest(target_text):
            errors.append("semantic review does not match current Japanese translation")
        if review.get("status") != "reviewed" or not review.get("notes") or not review.get("reviewer"):
            errors.append("separate whole-page semantic review is missing")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--component", required=True, choices=("etcd",))
    parser.add_argument("--rendered-dir", required=True, type=Path)
    parser.add_argument("--review-manifest", type=Path,
                        default=PROJECT / "data/translation-reviews/etcd.ja.json")
    args = parser.parse_args()
    root = CONTENT / args.component
    sources = sorted(p for p in root.rglob("*.md") if not LOCALE.search(p.name))
    targets = {p.relative_to(root).as_posix().replace(".ja.md", ".md")
               for p in root.rglob("*.ja.md")}
    expected = {p.relative_to(root).as_posix() for p in sources}
    errors = [f"missing translation: {p}" for p in sorted(expected - targets)]
    errors += [f"orphan translation: {p}" for p in sorted(targets - expected)]
    try:
        manifest = json.loads(args.review_manifest.read_text())
        if manifest.get("component") != args.component or manifest.get("language") != "ja":
            raise ValueError("review scope does not match component/language")
        entries = manifest["pages"]
        reviews = {entry["path"]: entry for entry in entries}
        if len(reviews) != len(entries) or set(reviews) != expected:
            errors.append("review manifest must cover each current English page exactly once")
    except (OSError, ValueError, KeyError) as exc:
        errors.append(f"review manifest: {exc}")
        reviews = {}
    for source in sources:
        name = source.relative_to(root).as_posix()
        target = source.with_suffix(".ja.md")
        if not target.exists():
            continue
        review = reviews.get(name)
        if review is None:
            errors.append(f"{name}: no separate semantic review")
        try:
            errors.extend(f"{name}: {issue}" for issue in
                          validate_pair(source, target, args.rendered_dir, review))
        except (ValueError, OSError) as exc:
            errors.append(f"{name}: {exc}")
    if errors:
        print("Japanese current-source validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(sources)} current English/Japanese {args.component} pairs; "
          "no missing/orphan pages, structural errors or unexplained review exceptions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
