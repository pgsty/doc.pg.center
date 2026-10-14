#!/usr/bin/env python3
"""Validate pgBadger translations, protected literals and publication routes.

Semantic review is recorded separately. This gate detects missing pages,
changed commands, unreviewed explanatory fences and broken rendered links.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

from translation_fences import validate_fences, validate_literal_blocks

PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content/docs/pgbadger"
LANGUAGES = {"en": "en-US", "zh": "zh-CN", "fr": "fr-FR", "ja": "ja-JP", "de": "de-DE", "ru": "ru-RU"}
LOCALE = re.compile(r"\.(?:zh|fr|ja|de|ru)\.md$")
INLINE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
NUMERIC_REVIEWS = PROJECT / "data/translation-checks/pgbadger-numbers.json"
SEMANTIC_REVIEW = PROJECT / "data/translation-audits/pgbadger.json"
READER_POLICY = re.compile(
    r"翻译政策|翻译说明|译者(?:注|说明)?|(?:说明|正文|选项).*?(?:已译|译为)|"
    r"(?:保留|保持)(?:英文)?原文|文档快照说明|"
    r"\btranslator(?:s|'s)?\b|translation polic(?:y|ies)|translated edition|"
    r"This page (?:preserves|translates)|This pig\.center edition|documentation snapshot|"
    r"These entries preserve|Cette (?:page|édition)|traduction(?:s)?|"
    r"Diese (?:Seite|Ausgabe)|Übersetz(?:ung|ungen|t)|"
    r"翻訳|原文どおり|英語の原文|このページは|"
    r"Эта страница содержит|Эта редакция|перевод (?:справочника|документации)|пояснения переведены",
    re.I,
)


def validate_reader_prose(path: Path, body: str, errors: list[str]) -> None:
    """Keep editing/translation instructions out of reader-facing prose."""
    _, prose = fenced(body)
    for line in prose.splitlines():
        # WITH -> CTE and Russian 'перевод строки' describe program behavior.
        if "WITH" in line and "CTE" in line:
            continue
        if READER_POLICY.search(line) or "{#documentation-snapshot}" in line:
            errors.append(f"{path.name}: reader prose contains translation/editorial policy")


def numeric_facts(body: str) -> Counter:
    return Counter(value.replace(",", ".") for value in re.findall(
        r"\d+(?:[.,]\d+)*", unicodedata.normalize("NFKC", body)
    ))


def digest(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def validate_numbers(source: Path, target: Path, english: str, translated: str, reviews: dict, errors: list[str]) -> None:
    expected, actual = numeric_facts(english), numeric_facts(translated)
    # Versions, ISO dates and decimal technical values never use a prose-number
    # exception. A formatting change such as 9.5 -> 9,5 is normalized first.
    compound = lambda body: Counter(value.replace(",", ".") for value in re.findall(
        r"\d+(?:[.,]\d+)+|\d{4}-\d{2}-\d{2}", unicodedata.normalize("NFKC", body)
    ))
    label = str(target.relative_to(PROJECT))
    if compound(english) != compound(translated):
        errors.append(f"{label}: changed version, date or decimal fact")
    if expected == actual:
        return
    review = reviews.get(label, {})
    if not (
        review.get("source") == str(source.relative_to(PROJECT))
        and review.get("source_body_sha256") == digest(english)
        and review.get("target_body_sha256") == digest(translated)
        and review.get("missing") == dict(expected - actual)
        and review.get("extra") == dict(actual - expected)
        and review.get("reason")
    ):
        errors.append(f"{label}: numeric notation differs without a current exact review")


def split(document: str) -> tuple[str, str]:
    if not document.startswith("---\n") or "\n---\n" not in document[4:]:
        raise ValueError("missing or unterminated YAML front matter")
    return tuple(document[4:].split("\n---\n", 1))


def fenced(body: str) -> tuple[list[str], str]:
    blocks, prose, current = [], [], []
    marker = ""
    for line in body.splitlines(keepends=True):
        if marker:
            current.append(line)
            if re.fullmatch(r" {0,3}" + re.escape(marker[0]) + "{" + str(len(marker)) + r",}\s*", line):
                blocks.append("".join(current))
                marker, current = "", []
        elif match := re.match(r" {0,3}(`{3,}|~{3,})", line):
            marker, current = match[1], [line]
        else:
            prose.append(line)
    if marker:
        raise ValueError("unterminated code fence")
    return blocks, "".join(prose)


def headings(body: str) -> list[tuple[int, str]]:
    return [(len(m[1]), m[2] or "") for m in re.finditer(r"^(#{1,6})\s+.*?(?:\s+\{#([^}]+)\})?\s*$", body, re.M)]


def list_rows(body: str) -> list[tuple[int, str]]:
    return [(len(m[1]), "unordered" if m[2] in "-+*" else m[2])
            for m in re.finditer(r"^( *)([-+*]|[0-9]+[.)])\s+", body, re.M)]


def table_rows(body: str) -> list[int]:
    return [len(re.findall(r"(?<!\\)\|", line))
            for line in body.splitlines() if line.lstrip().startswith("|")]


def normalize_url(value: str) -> str:
    return re.sub(r"^/(?:zh|fr|ja|de|ru)/(?=docs/pgbadger(?:/|$))", "/", value)


def urls(prose: str) -> Counter:
    return Counter(normalize_url(x) for x in re.findall(r"\]\(([^\s)]+)(?:\s+[^)]*)?\)", prose))


def field(front: str, name: str) -> str:
    match = re.search(r"^" + re.escape(name) + r":\s*(.*?)\s*$", front, re.M)
    return match[1].strip('"\'') if match else ""


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.canonical = ""
        self.language = ""
        self.alternates: dict[str, str] = {}
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "html":
            self.language = a.get("lang", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href", "")
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.alternates[a["hreflang"]] = a.get("href", "")
        if tag in {"a", "link"} and a.get("href"):
            self.links.append(a["href"])
        if tag in {"img", "script", "iframe", "source"} and a.get("src"):
            self.links.append(a["src"])

    def handle_data(self, data: str) -> None:
        self.text.append(data)


@lru_cache(maxsize=None)
def document(path: Path) -> Document:
    result = Document()
    result.feed(path.read_text(encoding="utf-8"))
    return result


def check_links(root: Path, source: Path, doc: Document, errors: list[str]) -> None:
    for url in doc.links:
        parsed = urlsplit(url)
        if parsed.scheme not in {"", "http", "https"}:
            continue
        if parsed.netloc and parsed.netloc not in {"doc.pg.center", "www.doc.pg.center"}:
            continue
        path = unquote(parsed.path)
        target = (root / path.lstrip("/") if path.startswith("/") else source.parent / path) if path else source
        target = target.resolve()
        if not target.is_relative_to(root):
            errors.append(f"{source.relative_to(root)}: link escapes output root: {url}")
            continue
        if target.is_dir() or path.endswith("/"):
            target /= "index.html"
        elif not target.exists() and not target.suffix:
            target /= "index.html"
        if not target.is_file():
            errors.append(f"{source.relative_to(root)}: missing target: {url}")
        elif parsed.fragment and target.suffix == ".html" and "third_party" not in target.parts:
            fragment = unquote(parsed.fragment)
            ids = document(target).ids
            if fragment not in ids and not ("_print" in target.parts and any(i.endswith("--" + fragment) for i in ids)):
                errors.append(f"{source.relative_to(root)}: missing fragment: {url}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rendered-dir", type=Path)
    parser.add_argument("--report", type=Path, help="optional generated JSON report outside Git")
    args = parser.parse_args()
    if args.report and args.report.resolve().is_relative_to(PROJECT.resolve()):
        parser.error("generated reports must be outside the source repository")
    errors: list[str] = []
    reviews = json.loads(NUMERIC_REVIEWS.read_text()) if NUMERIC_REVIEWS.is_file() else {}
    semantic = json.loads(SEMANTIC_REVIEW.read_text()) if SEMANTIC_REVIEW.is_file() else None
    fingerprints = {entry["path"]: entry["sha256"] for entry in semantic.get("files", [])} if semantic else {}
    search: dict[str, dict] = {}
    if args.rendered_dir:
        for language in LANGUAGES:
            indices = list(args.rendered_dir.glob(f"offline-search-index.{language}.*.json"))
            if len(indices) != 1:
                errors.append(f"{language}: expected one current offline search index")
            else:
                search[language] = {entry["ref"]: entry for entry in json.loads(indices[0].read_text())}
    sources = sorted(p for p in CONTENT.rglob("*.md") if not LOCALE.search(p.name))
    if len(sources) != 16 or len(list(CONTENT.rglob("*.md"))) != 96:
        errors.append("expected 16 logical pages and 96 physical pages")
    rendered_count = 0
    for source in sources:
        try:
            ef, eb = split(source.read_text())
            blocks, prose = fenced(eb)
            for language in LANGUAGES:
                target = source if language == "en" else source.with_name(source.stem + "." + language + ".md")
                label = str(target.relative_to(PROJECT))
                if not target.is_file():
                    errors.append(f"{label}: missing translation")
                    continue
                tf, tb = split(target.read_text())
                if semantic and fingerprints.get(label) != digest(target.read_text()):
                    errors.append(f"{label}: file differs from the final semantic review")
                translated, translated_prose = fenced(tb)
                validate_reader_prose(target, tb, errors)
                if source.name == "license.md":
                    notice = re.search(r"Copyright \(c\).*?MODIFICATIONS\.", tb, re.S)
                    normalize_notice = lambda text: " ".join(text.split()).replace("“", '"').replace("”", '"')
                    original = (PROJECT / "sources/pgbadger/upstream/LICENSE").read_text()
                    if not notice or normalize_notice(notice[0]) != normalize_notice(original):
                        errors.append(f"{label}: changed upstream license notice")
                if language != "en":
                    validate_numbers(source, target, eb, tb, reviews, errors)
                    for name in ("weight", "upstream_link", "aliases", "icon", "module", "search_keywords", "search_boost"):
                        if normalize_url(field(ef, name)) != normalize_url(field(tf, name)):
                            errors.append(f"{label}: metadata differs: {name}")
                    for name, expected, actual in (
                        ("heading levels and explicit anchors", headings(prose), headings(translated_prose)),
                        ("link destinations", urls(prose), urls(translated_prose)),
                        ("list structure", list_rows(prose), list_rows(translated_prose)),
                        ("table structure", table_rows(prose), table_rows(translated_prose)),
                    ):
                        if expected != actual:
                            errors.append(f"{label}: changed {name}")
                    # Translations may add code styling to source literals that
                    # were plain text, but existing source code spans remain exact.
                    expected_inline = Counter(m[2] for m in INLINE.finditer(prose))
                    actual_inline = Counter(m[2] for m in INLINE.finditer(translated_prose))
                    if expected_inline - actual_inline:
                        errors.append(f"{label}: missing or changed inline literals")
                    validate_fences(source, blocks, translated, errors, language=language)
                    validate_literal_blocks(source, target.read_text(), errors, language=language)
                    # Explanatory fences are reviewed by exact hashes. Also protect
                    # option spellings and PostgreSQL prefix placeholders everywhere.
                    for name, pattern in (("long options", r"(?<![\w-])--[A-Za-z][A-Za-z_-]*"), ("prefix placeholders", r"%[A-Za-z]")):
                        if Counter(re.findall(pattern, eb)) != Counter(re.findall(pattern, tb)):
                            errors.append(f"{label}: changed {name}")
                    if "2919-05" in tb or r"\`jsonlog\`" in tb:
                        errors.append(f"{label}: upstream erratum reintroduced")
                    lint_prose = prose
                    if source.name == "license.md":
                        # Retain the exact upstream notice separately from
                        # translated licensing and attribution explanations.
                        lint_prose = re.sub(
                            r"^## [^\n]*\{#postgresql-license\}.*?(?=^## [^\n]*\{#credits\})",
                            "", prose, flags=re.M | re.S,
                        )
                    for paragraph in re.split(r"\n\s*\n", lint_prose):
                        phrase = " ".join(paragraph.split())
                        if len(phrase) >= 90 and phrase in " ".join(translated_prose.split()) and re.search(r"\b(?:the|this|these|that|with|from)\b", phrase, re.I):
                            errors.append(f"{label}: untranslated English paragraph: {phrase[:100]}")
                if args.rendered_dir:
                    root = args.rendered_dir.resolve()
                    relative = source.relative_to(CONTENT)
                    slug = relative.parent if relative.name == "_index.md" else relative.with_suffix("")
                    route = ("/" if language == "en" else f"/{language}/") + "docs/pgbadger/" + (slug.as_posix().strip(".") + "/" if slug.as_posix() != "." else "")
                    output = root / route.lstrip("/") / "index.html"
                    if not output.is_file():
                        errors.append(f"{label}: missing rendered page: {route}")
                        continue
                    doc = document(output)
                    search_entry = search.get(language, {}).get(route)
                    expected_keywords = field(tf, "search_keywords").strip("[]").split(", ")
                    expected_keywords = [word for word in expected_keywords if word]
                    if not search_entry or not set(expected_keywords).issubset(search_entry.get("keywords", [])):
                        errors.append(f"{label}: page or technical keywords missing from local search")
                    markdown = output.with_name("index.md")
                    if not markdown.is_file() or tb.strip() not in markdown.read_text():
                        errors.append(f"{label}: incomplete Markdown publication body")
                    bundle = root / ("" if language == "en" else language) / "docs/pgbadger/llms-full.txt"
                    if bundle.is_file() and markdown.is_file():
                        marker = f"Source: https://doc.pg.center{route}index.md"
                        if marker not in bundle.read_text() or markdown.read_text().strip() not in bundle.read_text():
                            errors.append(f"{label}: incomplete LLMS publication body")
                    if doc.language != LANGUAGES[language] or doc.canonical != "https://doc.pg.center" + route:
                        errors.append(f"{label}: wrong HTML language or canonical URL")
                    for lang, locale in LANGUAGES.items():
                        alternate = ("/" if lang == "en" else f"/{lang}/") + "docs/pgbadger/" + (slug.as_posix().strip(".") + "/" if slug.as_posix() != "." else "")
                        if doc.alternates.get(locale) != "https://doc.pg.center" + alternate:
                            errors.append(f"{label}: wrong hreflang route: {locale}")
                    for _, anchor in headings(translated_prose):
                        if anchor and anchor not in doc.ids:
                            errors.append(f"{label}: unrendered heading anchor: {anchor}")
                    check_links(root, output, doc, errors)
                    rendered_count += 1
        except (ValueError, OSError) as exc:
            errors.append(f"{source.relative_to(PROJECT)}: {exc}")
    if args.rendered_dir:
        root = args.rendered_dir.resolve()
        for language in LANGUAGES:
            prefix = Path() if language == "en" else Path(language)
            for path in (prefix / "_print/docs/pgbadger/index.html", prefix / "docs/pgbadger/llms-full.txt", prefix / "docs/pgbadger/index.md"):
                if not (root / path).is_file():
                    errors.append(f"missing publication output: {path}")
    report = {"status": "failed" if errors else "passed", "logical_pages": len(sources), "languages": list(LANGUAGES), "rendered_pages": rendered_count, "errors": errors}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    if errors:
        print("pgBadger publication validation failed:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated pgBadger: 16 pages × 6 languages; {rendered_count} rendered pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
