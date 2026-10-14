#!/usr/bin/env python3
"""Check all PgBouncer 1.26 pages against current English and reviewed files.

The semantic review is bound to exact file hashes. Structural checks protect
technical content independently; rendered checks verify the actual outputs.
Chinese prose headings retain their established localized IDs.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, urlunsplit

PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content"
ROOT = CONTENT / "docs/pgbouncer"
AUDIT = PROJECT / "data/translation-audits/pgbouncer.json"
LANGUAGES = {"en": "en-US", "zh": "zh-CN", "fr": "fr-FR", "ja": "ja-JP", "de": "de-DE", "ru": "ru-RU"}
PAGES = {"_index", "changelog", "community", "config", "download", "faq", "features", "install", "usage"}
PREFIX = "/docs/pgbouncer/"


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


R = load("pgbouncer_helpers", "pgbouncer_validation.py")
G = load("pgbouncer_structure", "check-german-parity.py")
P = R
L = load("pgbouncer_links", "check-local-links.py")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(value):
    parsed = urlsplit(value)
    if parsed.netloc and parsed.netloc not in {"doc.pg.center", "www.doc.pg.center"}:
        return value
    path = re.sub(r"^/(?:zh|fr|ja|de|ru)(?=/(?:docs|search|attribution)(?:/|$))", "", parsed.path)
    return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))


def numeric_facts(body):
    _, prose = R.fenced_blocks(body)
    prose = re.sub(r"<!--.*?-->", "", prose, flags=re.S)
    prose = re.sub(r"\{#[^}]+\}", "", prose)
    # Stop at the Markdown closing parenthesis. A whitespace-only URL regex
    # swallows following CJK prose and issue labels on the same line.
    prose = re.sub(r"https?://[^\s<>)]*", "", prose)
    prose = re.sub(r"(?<=\d)[,\u00a0\u202f ](?=\d{3}(?:\D|$))", "", prose)
    return Counter(re.findall(r"(?<!\d)\d+(?:[.,]\d+)*(?!\d)", prose))


def link_signature(body, source, language):
    _, prose = G.parse_fenced_blocks(body)
    prose = G.prose_without_comments_and_shortcodes(prose)
    prose = G.INLINE_CODE_RE.sub("`CODE`", prose)
    targets = G.markdown_inline_destinations(prose)
    targets.extend(match[2] for match in G.REFERENCE_DEFINITION_RE.finditer(prose)
                   if not match[1].startswith("^"))
    targets.extend(G.html_destinations(prose))
    remaining = G.prose_without_markdown_destinations(prose)
    remaining = G.REFERENCE_DEFINITION_RE.sub(
        lambda match: match[0] if match[1].startswith("^") else "", remaining)
    remaining = G.HTML_URL_ATTRIBUTE_RE.sub("", remaining)
    autolink = re.compile(r"<((?:https?|ftp)://[^<>\s]+|mailto:[^<>\s]+)>")
    targets.extend(autolink.findall(remaining))
    remaining = autolink.sub("", remaining)
    targets.extend(value.rstrip(".,;!?，。；") for value in re.findall(
        r"(?:https?|ftp)://[^\s<>()\"'\u3000-\u9fff]+", remaining))
    values = [normalize(R.canonical_target(value.strip("<>"), source)) for value in targets]
    if language == "zh":
        def local_fragment(value):
            parsed = urlsplit(value)
            local = (not parsed.netloc or parsed.netloc in {"doc.pg.center", "www.doc.pg.center"}) and parsed.scheme in {"", "http", "https"}
            return urlunsplit((*parsed[:4], "")) if local and (not parsed.path or parsed.path.startswith(PREFIX)) else value
        values = [local_fragment(value) for value in values]
    # Footnotes may be defined next to their translated paragraph rather than
    # at the end. Destinations and their multiplicity remain protected.
    return Counter(values)


def shared_front(front):
    return {key: value for key, value in G.front_matter_blocks(front).items()
            if key not in R.TRANSLATABLE_FRONT_KEYS}


def technical_errors(source, target, row):
    ef, eb = R.split_front_matter(source.read_text(encoding="utf-8"))
    tf, tb = R.split_front_matter(target.read_text(encoding="utf-8"))
    language = target.name.split(".")[-2]
    label = target.relative_to(PROJECT).as_posix()
    errors = []
    for name, expected, actual in (
        ("shared metadata", shared_front(ef), shared_front(tf)),
        ("heading levels/order", R.headings(eb), R.headings(tb)),
        ("fenced code", R.fenced_blocks(eb)[0], R.fenced_blocks(tb)[0]),
        ("quoted fenced code", R.blockquoted_fenced_blocks(eb), R.blockquoted_fenced_blocks(tb)),
        ("lists", G.list_signature(eb), G.list_signature(tb)),
        ("tables", G.table_signature(eb), G.table_signature(tb)),
        ("links/assets", link_signature(eb, source, language), link_signature(tb, source, language)),
    ):
        if expected != actual:
            errors.append(f"{label}: {name} differs from current English")
    missing = Counter(R.inline_literals(eb)) - Counter(R.inline_literals(tb))
    if missing:
        errors.append(f"{label}: protected inline literals missing: {dict(missing)}")
    en_numbers, translated_numbers = numeric_facts(eb), numeric_facts(tb)
    if en_numbers - translated_numbers:
        errors.append(f"{label}: numeric facts missing: {dict(en_numbers - translated_numbers)}")
    extra = dict(translated_numbers - en_numbers)
    note = row.get("additional_numeric_facts", {})
    if extra != note.get("counts", {}):
        errors.append(f"{label}: additional numeric facts differ from the exact reviewed record")
    if extra and not note.get("reason"):
        errors.append(f"{label}: additional numeric facts have no review explanation")
    diagnostics = row.get("protected_diagnostics", [])
    errors.extend(f"{label}: {error}" for error in R.diagnostic_errors(eb, tb, diagnostics))
    if source == ROOT / "changelog.md" and language == "de":
        # These original program messages use quotes rather than code spans.
        # Compare whole quoted messages so an added suffix cannot pass the
        # existing substring-count check; Markdown line wrapping is allowed.
        for literal in (
            "unclean server",
            "client disconnect while server was not ready",
            "client disconnect before everything was sent to the server",
        ):
            pattern = '"' + r"[ \t\r\n]+".join(map(re.escape, literal.split())) + '"'
            expected = len(re.findall(pattern, eb))
            if not expected or len(re.findall(pattern, tb)) != expected:
                errors.append(f"{label}: original diagnostic changed (quoted message): {literal!r}")
    errors.extend(f"{label}: {error}" for error in R.placeholder_errors(eb, tb, diagnostics))
    return errors


def source_errors(audit):
    sources = sorted(p for p in ROOT.glob("*.md") if R.is_english(p))
    errors = []
    if {p.stem for p in sources} != PAGES:
        errors.append("English PgBouncer logical page set changed")
    expected = {s.with_suffix(f".{language}.md").relative_to(PROJECT).as_posix(): s
                for s in sources for language in LANGUAGES if language != "en"}
    rows = audit.get("pages", [])
    if Counter(row.get("translation") for row in rows) != Counter(expected.keys()):
        errors.append("semantic review must cover every one of the 45 translation pairs exactly once")
    for row in rows:
        source = expected.get(row.get("translation"))
        if source is None:
            continue
        target = PROJECT / row["translation"]
        if not target.is_file():
            errors.append(f"missing translation: {row['translation']}")
            continue
        if row.get("source") != source.relative_to(PROJECT).as_posix():
            errors.append(f"{target.name}: source review path mismatch")
        if row.get("source_sha256") != sha256(source) or row.get("translation_sha256") != sha256(target):
            errors.append(f"{target.name}: semantic review fingerprint is stale")
        if row.get("semantic_review") != "pass" or not row.get("review"):
            errors.append(f"{target.name}: semantic review conclusion or evidence missing")
        errors.extend(technical_errors(source, target, row))
    expected_files = set(sources) | {PROJECT / path for path in expected}
    if set(ROOT.glob("*.md")) != expected_files:
        errors.append("PgBouncer has missing or orphan locale pages")
    for language in LANGUAGES:
        target = ROOT / ("_index.md" if language == "en" else f"_index.{language}.md")
        front, _ = R.split_front_matter(target.read_text(encoding="utf-8"))
        if "1.26.0" not in (R.front_text(front, "title") or ""):
            errors.append(f"{target.name}: version title is not 1.26.0")
        if re.findall(r"(?m)^\s*upstream_ref:\s*(\S+)", front) != ["v1.26.0", "v1.26.0"]:
            errors.append(f"{target.name}: upstream/cascade version mismatch")
    return errors, sources


def collection_nodes(build, language):
    payload = json.loads((build / ("" if language == "en" else language) / "navigation.json").read_text(encoding="utf-8"))
    result = []
    def walk(node):
        if node.get("id", "").startswith(PREFIX):
            result.append(node)
        for child in node.get("children", []):
            walk(child)
    walk(payload["root"])
    return result


def english_print_errors(build, sources):
    sections = P.content_sections(P.read_document(build / "_print/docs/pgbouncer/index.html"))
    errors, blocks = [], 0
    for source, section in zip(sources, sections):
        route = PREFIX + ("" if source.stem == "_index" else source.stem + "/")
        normal = P.content_sections(P.read_document(build / route.lstrip("/") / "index.html"))
        if len(normal) != 1:
            errors.append(route + ": English normal content section missing")
            continue
        expected = P.body_blocks(normal[0])
        actual = P.body_blocks(section, print_root=source.stem == "_index")
        blocks += len(expected)
        if expected != actual:
            errors.append(route + ": English print body differs from normal page")
        if P.content_metadata(normal[0]) != P.content_metadata(section, print_title=source.stem != "_index"):
            errors.append(route + ": English print title/lead/headings/images differ")
    if len(sections) != len(sources):
        errors.append("English print chapter count differs")
    return errors, blocks


def rendered_errors(build, sources):
    errors, reports = [], {}
    def require(condition, message):
        if not condition:
            errors.append(message)
    en_nodes = collection_nodes(build, "en")
    ids = [n["id"] for n in en_nodes]
    by_route = {PREFIX + ("" if s.stem == "_index" else s.stem + "/"): s for s in sources}
    require(Counter(ids) == Counter(by_route.keys()), "English navigation coverage/duplicates")
    ordered_sources = [by_route[route] for route in ids]
    for language, locale in LANGUAGES.items():
        local = "" if language == "en" else "/" + language
        nodes = collection_nodes(build, language)
        require([n["id"] for n in nodes] == ids, f"{language}: navigation order/coverage")
        indexes = list(build.glob(f"offline-search-index.{language}.*.json"))
        require(len(indexes) == 1, f"{language}: expected one search index")
        if len(indexes) != 1:
            continue
        rows = json.loads(indexes[0].read_text(encoding="utf-8"))
        search = {row["ref"]: row for row in rows}
        require(Counter(row["ref"] for row in rows if row["ref"].startswith(local + PREFIX)) ==
                Counter(local + route for route in ids), f"{language}: search coverage/duplicates")
        pages = []
        for node in nodes:
            route = local + node["id"]
            label = f"{language}: {route}"
            source = by_route[node["id"]]
            target = source if language == "en" else source.with_suffix(f".{language}.md")
            front, body = R.split_front_matter(target.read_text(encoding="utf-8"))
            path = build / route.lstrip("/") / "index.html"
            pages.append(path)
            doc, english = R.RenderedContent(path), R.RenderedContent(build / node["id"].lstrip("/") / "index.html")
            require(doc.canonical == ["https://doc.pg.center" + route], label + ": canonical")
            require(doc.html_languages == [locale], label + ": HTML language")
            require(([h for h, _ in doc.headings] == [h for h, _ in english.headings]) if language == "zh"
                    else doc.headings == english.headings, label + ": headings/required anchors")
            require(doc.code == english.code, label + ": rendered code/output")
            require([normalize(p) for p in doc.sidebar] == english.sidebar, label + ": sidebar order")
            require([(d, normalize(p)) for d, p in doc.pager] == english.pager, label + ": pager")
            for other, other_locale in LANGUAGES.items():
                alternate = ("" if other == "en" else "/" + other) + node["id"]
                require(doc.alternates.get(other_locale) == "https://doc.pg.center" + alternate, label + ": alternate " + other)
                if other != language:
                    require(alternate in doc.languages, label + ": language switch " + other)
            markdown = (build / route.lstrip("/") / "index.md").read_text(encoding="utf-8")
            require(body.strip() in markdown, label + ": incomplete Markdown body")
            for field in ("title", "description"):
                require(" ".join(search[route][field].split()) == " ".join((R.front_text(front, field) or "").split()), label + ": search " + field)
            if node["id"] == PREFIX + "config/":
                for parameter in ("pool_idle_timeout", "login_notify_message", "query_wait_timeout"):
                    require(parameter in search[route]["headings"], label + ": search parameter " + parameter)
            for alias in R.front_aliases(front):
                redirected = R.RenderedContent(build / (local + alias).lstrip("/") / "index.html")
                require(redirected.canonical == doc.canonical and redirected.refresh == doc.canonical, label + ": alias " + alias)
        llms = R.llms_entries((build / (local + PREFIX).lstrip("/") / "llms-full.txt").read_text(encoding="utf-8"))
        expected = [("https://doc.pg.center" + local + n["id"] + "index.md",
                     (build / (local + n["id"]).lstrip("/") / "index.md").read_text(encoding="utf-8").strip()) for n in nodes]
        require(llms == expected, language + ": complete LLMS bodies/order")
        printing = build / local.lstrip("/") / "_print/docs/pgbouncer/index.html"
        pages.append(printing)
        sections = P.content_sections(P.read_document(printing))
        section_order = [title.attrs.get("id") if (title := P.heading(section)) else None for section in sections]
        expected_order = [None if source.stem == "_index" else "pg-" + hashlib.md5(
            (source if language == "en" else source.with_suffix(f".{language}.md")).relative_to(CONTENT).as_posix().encode()).hexdigest()
            for source in ordered_sources]
        require(section_order == expected_order, language + ": print chapter order")
        if language == "en":
            failures, blocks = english_print_errors(build, ordered_sources)
            errors.extend(failures)
            reports[language] = {"pages": len(nodes), "print_blocks": blocks}
        else:
            failures, printed = P.check_print(build, ordered_sources, CONTENT, locale=language,
                                             component="pgbouncer", compare_metadata=True)
            errors.extend(f"{language}: {error}" for error in failures)
            reports[language] = {"pages": len(nodes), "print_blocks": sum(p["expected_blocks"] for p in printed)}
        cache = {}
        for page in pages:
            for attribute, url in L.load_document(page).links:
                destination, fragment = L.resolve_target(build, page, url)
                if destination is None:
                    continue
                require(destination.is_relative_to(build) and destination.exists(), f"{page.relative_to(build)}: missing/escaping {attribute}={url}")
                if destination.exists() and fragment and destination.suffix == ".html" and "third_party" not in destination.parts:
                    if destination not in cache:
                        cache[destination] = L.load_document(destination)
                    anchors = cache[destination].anchors
                    require(fragment in anchors or ("_print" in destination.parts and any(a.endswith("--" + fragment) for a in anchors)), f"{page.relative_to(build)}: missing fragment {url}")
    return errors, reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rendered-dir", type=Path)
    parser.add_argument("--report", type=Path, help="write generated results outside Git")
    args = parser.parse_args()
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    errors, sources = source_errors(audit)
    reports = {}
    if args.rendered_dir:
        failures, reports = rendered_errors(args.rendered_dir.resolve(), sources)
        errors.extend(failures)
    if args.report:
        args.report.write_text(json.dumps({"pairs": 45, "outputs": reports, "errors": errors}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if errors:
        print("PgBouncer acceptance failed:\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1
    print("Validated PgBouncer 1.26.0: 45 current-source translation pairs and exact semantic-review fingerprints" +
          (", 54 rendered pages, navigation/search/aliases, complete Markdown/print/LLMS bodies and local links." if args.rendered_dir else "."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
