#!/usr/bin/env python3
"""Validate every German HAProxy page and its production-rendered outputs."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

PROJECT = Path(__file__).resolve().parent.parent


def helper(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


parity = helper("haproxy_de_parity", "check-german-parity.py")
links = helper("haproxy_de_links", "check-local-links.py")
# This shared comparator accepts a locale/component and checks entire ordered
# prose, table, list, code and metadata bodies; its Japanese entry point is tested.
printing = helper("haproxy_de_print", "check-pgbackrest-ja-print.py")
from translation_fences import load_manifest, sha256, validate_fences

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids, self.content_ids, self.links, self.headings, self.pre = [], [], [], [], []
        self.canonical, self.language, self.sidebar, self.previous, self.next = [], [], [], [], []
        self.alternates, self.search, self.current_pre = {}, "", None
        self.dividers, self.current_divider = [], None
        self.feed(text)

    def in_content(self):
        return any("td-content" in data.get("class", "").split() for _, data in self.stack)

    def handle_starttag(self, tag, attrs):
        data = {key: value or "" for key, value in attrs}
        classes = data.get("class", "").split()
        if data.get("id"):
            self.ids.append(data["id"])
            if self.in_content():
                self.content_ids.append(data["id"])
        if tag == "html":
            self.language.append(data.get("lang"))
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical.append(data.get("href"))
        if tag == "link" and data.get("rel") == "alternate":
            self.alternates[data.get("hreflang")] = data.get("href")
        if tag == "a":
            self.links.append(data)
            if "td-shell-tree__link" in classes:
                self.sidebar.append(data.get("href"))
            if "data-td-pager-prev" in data:
                self.previous.append(data.get("href"))
            if "data-td-pager-next" in data:
                self.next.append(data.get("href"))
        if data.get("data-td-index-src"):
            self.search = data["data-td-index-src"]
        if self.in_content() and re.fullmatch(r"h[2-6]", tag):
            self.headings.append((tag, data.get("id", "")))
        if tag == "pre" and self.in_content():
            self.current_pre = []
        if "td-shell-tree__heading-label" in classes:
            self.current_divider = []
        if tag not in VOID:
            self.stack.append((tag, data))

    def handle_endtag(self, tag):
        if tag == "pre" and self.current_pre is not None:
            self.pre.append("".join(self.current_pre))
            self.current_pre = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                if "td-shell-tree__heading-label" in self.stack[index][1].get("class", "").split():
                    self.dividers.append(" ".join("".join(self.current_divider or []).split()))
                    self.current_divider = None
                del self.stack[index:]
                break

    def handle_data(self, text):
        if self.current_pre is not None:
            self.current_pre.append(text)
        if self.current_divider is not None:
            self.current_divider.append(text)


def route(source, german=False):
    root = "/de/docs/haproxy/" if german else "/docs/haproxy/"
    return root if source.name == "_index.md" else root + source.stem + "/"


def front_text(front, key):
    value = parity.front_matter_blocks(front).get(key, "").partition(":")[2].strip()
    if value.startswith('"'):
        return json.loads(value)
    return value.strip("'")


def aliases(front):
    match = re.search(r"(?m)^aliases:\s*\[([^]]*)\]", front)
    if match:
        return [value.strip().strip("\"'") for value in match.group(1).split(",") if value.strip()]
    match = re.search(r"(?m)^aliases:\s*\n((?:[ \t]+.*\n)+)", front)
    return re.findall(r"(?m)^\s*-\s*(\S+)", match.group(1)) if match else []


def approved_pre_pairs(source, english, german, errors):
    """Permit only exact registered explanations; real code stays byte exact."""
    validate_fences(source, english, german, errors)
    reviewed = {entry["index"] for entry in load_manifest(source, "de").get("fences", [])}
    # HTMLParser already decodes the rendered HTML once. Entity-like strings
    # inside a literal example must not be decoded a second time.
    inner = lambda value: "\n".join(value.splitlines()[1:-1]).strip()
    return {(inner(en), inner(de)) for index, (en, de) in enumerate(zip(english, german), 1) if index in reviewed}


def validate_pre(source, english, german, permitted_fences, errors):
    """Check indented explanations independently of fenced Markdown blocks."""
    entries = load_manifest(source, "de").get("rendered_explanations", [])
    reviews, used = {}, set()
    label = source.name
    for entry in entries:
        index = entry.get("index")
        if not isinstance(index, int) or not 1 <= index <= len(english) or index in reviews:
            errors.append(f"{label}: invalid or duplicate rendered explanation index {index!r}")
            continue
        reviews[index] = entry
    if len(english) != len(german):
        errors.append(f"{label}: preformatted block count")
    for index, (en, de) in enumerate(zip(english, german), 1):
        if en == de or (en.strip(), de.strip()) in permitted_fences:
            continue
        review = reviews.get(index)
        prefix = f"{label}: rendered block {index}"
        if review is None:
            errors.append(f"{prefix}: changed without an exact explanation review")
            continue
        used.add(index)
        if review.get("classification") not in {"argument-description", "table-labels", "mixed-explanation", "explanation-label"} or not review.get("review"):
            errors.append(f"{prefix}: explanation classification or semantic review is missing")
        if review.get("source_sha256") != sha256(en):
            errors.append(f"{prefix}: reviewed English explanation changed")
        if review.get("target_sha256") != sha256(de):
            errors.append(f"{prefix}: German explanation differs from the reviewed translation")
        if parity.number_facts("", en) != parity.number_facts("", de):
            errors.append(f"{prefix}: numeric facts changed")
        for line in review.get("protected_lines", []):
            if not line or en.splitlines().count(line) == 0 or en.splitlines().count(line) != de.splitlines().count(line):
                errors.append(f"{prefix}: protected code/output line changed: {line!r}")
        for label_prefix in review.get("protected_prefixes", []):
            count = lambda text: sum(line.lstrip().startswith(label_prefix) for line in text.splitlines())
            if not label_prefix or not count(en) or count(en) != count(de):
                errors.append(f"{prefix}: protected table/list label changed: {label_prefix!r}")
        normalized_en, normalized_de = " ".join(en.split()), " ".join(de.split())
        for literal in review.get("protected_literals", []):
            if not literal or normalized_en.count(literal) == 0 or normalized_en.count(literal) != normalized_de.count(literal):
                errors.append(f"{prefix}: protected technical literal changed: {literal!r}")
    for index in reviews.keys() - used:
        errors.append(f"{label}: unused/stale rendered explanation review {index}")
    return len(used)


def review_record_errors(sources, record):
    """A semantic signoff applies only to the exact source/target pair reviewed."""
    errors = []
    paths = [str(p.relative_to(PROJECT)) for p in sources]
    rows = record.get("pages", [])
    if Counter(row.get("source") for row in rows) != Counter(paths):
        errors.append("semantic review: missing, duplicate or orphan page records")
    indexed = {row.get("source"): row for row in rows}
    for source, path in zip(sources, paths):
        row = indexed.get(path, {})
        target = source.with_suffix(".de.md")
        for key, file in (("source_sha256", source), ("target_sha256", target)):
            if not file.is_file() or row.get(key) != hashlib.sha256(file.read_bytes()).hexdigest():
                errors.append(f"{path}: semantic review {key} is absent or stale")
        if row.get("semantic_review", {}).get("status") != "passed":
            errors.append(f"{path}: separate semantic/navigation review is missing")
    return errors


def check(build):
    source_root = PROJECT / "content/docs/haproxy"
    all_sources = sorted(p for p in source_root.glob("*.md") if parity.is_english_source(p))
    expected = {p.with_suffix(".de.md") for p in all_sources}
    actual = set(source_root.glob("*.de.md"))
    errors = [f"missing German page: {p}" for p in sorted(expected - actual)]
    errors += [f"orphan German page: {p}" for p in sorted(actual - expected)]
    reading = sorted((p for p in all_sources if not p.name.startswith("_")), key=lambda p: int(re.search(r"(?m)^weight:\s*(\d+)", p.read_text()).group(1)))
    # Hugo emits the section introduction first, regardless of its own weight.
    sources = [source_root / "_index.md"] + reading
    sidebar = ["/de/docs/haproxy/"] + [route(p, True) for p in reading]
    report = {"scope": "all current English/German HAProxy pages", "source_pairs": len(all_sources), "pages": [], "errors": errors}
    review_file = PROJECT / "data/translation-audits/haproxy-de.json"
    if review_file.is_file():
        errors.extend(review_record_errors(all_sources, json.loads(review_file.read_text())))
    else:
        errors.append("page-by-page German HAProxy semantic review record is missing")
    loaded, link_documents, search_indexes = {}, {}, {}

    def require(ok, message):
        if not ok:
            errors.append(message)

    def load(path):
        if path not in loaded:
            loaded[path] = Page(path.read_text())
        return loaded[path]

    def document(path):
        if path not in link_documents:
            link_documents[path] = links.load_document(path)
        return link_documents[path]

    def check_links(path):
        for attribute, url in document(path).links:
            target, fragment = links.resolve_target(build, path, url)
            if target is None:
                continue
            if not target.is_relative_to(build):
                errors.append(f"{path}: site-root escape {url}")
                continue
            require(target.exists(), f"{path}: missing {attribute} target {url}")
            if fragment and target.is_file() and target.suffix == ".html" and "third_party" not in target.parts:
                anchors = document(target).anchors
                print_anchor = "_print" in target.parts and any(a.endswith("--" + fragment) for a in anchors)
                require(fragment in anchors or print_anchor, f"{path}: missing fragment {url}")

    homepage = build / "de/index.html"
    if homepage.is_file():
        home = load(homepage)
        require(home.language == ["de-DE"], "German homepage: HTML language")
        for destination in ("/de/docs/haproxy/", "/de/docs/haproxy/proxies/", "/de/docs/haproxy/acls-and-samples/", "/de/docs/haproxy/statistics-and-monitoring/"):
            require(any(a.get("href") == destination and not a.get("data-fallback-language") for a in home.links), f"German homepage: missing localized entry {destination}")
        require(not any("/docs/haproxy/" in a.get("href", "") and a.get("data-fallback-language") for a in home.links), "German homepage: HAProxy English fallback")
    else:
        errors.append("German homepage missing")

    require(len(all_sources) == 38 and len(sources) == 35 and len(reading) == 34, "HAProxy source page/divider count changed")
    divider_titles = [front_text(parity.split_front_matter(p.with_suffix(".de.md").read_text())[0], "title") for p in sorted((p for p in all_sources if p.name.startswith("_div_")), key=lambda p: int(re.search(r"(?m)^weight:\s*(\d+)", p.read_text()).group(1))) if p.with_suffix(".de.md").is_file()]
    for source in all_sources:
        target = source.with_suffix(".de.md")
        if not target.is_file():
            continue
        parity.validate_pair(source, target, build, errors, current_source=True)
        if source.name.startswith("_div_"):
            require(not (build / "de/docs/haproxy" / source.stem / "index.html").exists(), f"{source.name}: divider became a reading page")
            continue
        destination = route(source, True)
        html_path = build / destination.lstrip("/") / "index.html"
        markdown_path = html_path.with_name("index.md")
        english_path = build / route(source).lstrip("/") / "index.html"
        if not all(p.is_file() for p in (html_path, markdown_path, english_path)):
            errors.append(f"{source.name}: missing German HTML/Markdown or English HTML")
            continue
        page, english = load(html_path), load(english_path)
        require(page.language == ["de-DE"], f"{source.name}: HTML language")
        require(page.canonical == ["https://doc.pg.center" + destination], f"{source.name}: canonical")
        require(page.alternates.get("en-US") == "https://doc.pg.center" + route(source), f"{source.name}: English alternate")
        require(english.alternates.get("de-DE") == "https://doc.pg.center" + destination, f"{source.name}: reciprocal German alternate")
        require(any(a.get("hreflang") == "en-US" and a.get("href") == route(source) for a in page.links), f"{source.name}: visible English language switch")
        require(any(a.get("hreflang") == "de-DE" and a.get("href") == destination for a in english.links), f"{source.name}: visible German language switch")
        require(page.headings == english.headings, f"{source.name}: rendered heading IDs/order")
        stable_ids = lambda values: [re.sub(r"^td-code-[0-9a-f]{8}-fence-", "td-code-LOCALE-fence-", value) for value in values]
        require(stable_ids(page.content_ids) == stable_ids(english.content_ids), f"{source.name}: rendered body IDs/order")
        require(not [value for value, count in Counter(page.ids).items() if count > 1], f"{source.name}: duplicate IDs")
        require(page.sidebar == sidebar, f"{source.name}: sidebar routes/order")
        require(page.dividers == divider_titles, f"{source.name}: localized divider labels/order")
        require(not any(a.get("data-fallback-language") and "/docs/haproxy/" in a.get("href", "") for a in page.links), f"{source.name}: HAProxy English fallback")
        index = reading.index(source) if source in reading else -1
        previous = ([route(reading[index - 1], True)] if index else ["/de/docs/haproxy/"]) if index >= 0 else []
        following = [route(reading[index + 1], True)] if index + 1 < len(reading) else []
        require(page.previous == previous and page.next == following, f"{source.name}: weighted German pager")
        front, body = parity.split_front_matter(target.read_text())
        _, en_body = parity.split_front_matter(source.read_text())
        en_fences = parity.parse_fenced_blocks(en_body)[0]
        de_fences = parity.parse_fenced_blocks(body)[0]
        permitted = approved_pre_pairs(source, en_fences, de_fences, errors)
        rendered_explanations = validate_pre(source, english.pre, page.pre, permitted, errors)
        require(body.strip() in markdown_path.read_text(), f"{source.name}: incomplete Markdown body")
        for alias in aliases(front):
            old = build / "de" / alias.strip("/") / "index.html"
            require(old.is_file() and "https://doc.pg.center" + destination in old.read_text(), f"{source.name}: legacy alias {alias}")
        raw = html_path.read_text()
        require("Copyright 2000-2026 Willy Tarreau" in raw, f"{source.name}: copyright")
        require("https://www.gnu.org/licenses/old-licenses/gpl-2.0.html" in raw, f"{source.name}: GPLv2 attribution")
        check_links(html_path)
        search_path = build / page.search.lstrip("/")
        require(bool(page.search) and search_path.is_file(), f"{source.name}: missing search index")
        if page.search and search_path.is_file():
            if search_path not in search_indexes:
                search_indexes[search_path] = json.loads(search_path.read_text())
            entries = [entry for entry in search_indexes[search_path] if entry.get("ref") == destination]
            require(len(entries) == 1, f"{source.name}: search entry count")
            if len(entries) == 1:
                for key in ("title", "description"):
                    require(entries[0].get(key) == front_text(front, key), f"{source.name}: search {key}")
                require(bool(entries[0].get("excerpt")), f"{source.name}: empty search excerpt")
        report["pages"].append({"route": destination, "anchors": len(page.content_ids), "headings": len(page.headings), "rendered_code_blocks": len(page.pre), "reviewed_indented_explanations": rendered_explanations})

    navigation = build / "de/navigation.json"
    if navigation.is_file():
        payload = json.loads(navigation.read_text())
        try:
            docs = next(p for p in payload["root"]["children"] if p["id"] == "/docs/")
            component = next(p for p in docs["children"] if p["id"] == "/docs/haproxy/")
            require([p["url"] for p in component["children"]] == ["https://doc.pg.center" + route(p, True) for p in reading], "navigation.json: reading routes/order")
            for node, source in zip([component] + component["children"], sources):
                front = parity.split_front_matter(source.with_suffix(".de.md").read_text())[0]
                require(node["title"] == (front_text(front, "linkTitle") or front_text(front, "title")), f"navigation.json: title for {source.name}")
                require(node["markdown"] == "https://doc.pg.center" + route(source, True) + "index.md", f"navigation.json: Markdown for {source.name}")
        except (KeyError, StopIteration, OSError) as exc:
            errors.append(f"navigation.json: incomplete German HAProxy navigation: {exc}")
    else:
        errors.append("German navigation.json missing")
    llms = build / "de/docs/haproxy/llms-full.txt"
    if llms.is_file():
        bundle = llms.read_text()
        require(re.findall(r"(?m)^Source: (.+)$", bundle) == ["https://doc.pg.center" + route(p, True) + "index.md" for p in sources], "llms-full.txt: missing, duplicate or reordered sources")
        for source in sources:
            target = source.with_suffix(".de.md")
            if target.is_file():
                body = parity.split_front_matter(target.read_text())[1]
                require(body.strip() in bundle, f"llms-full.txt: incomplete body for {source.name}")
    else:
        errors.append("German llms-full.txt missing")
    printed = build / "de/_print/docs/haproxy/index.html"
    if printed.is_file():
        print_errors, print_pages = printing.check_print(build, sources, PROJECT / "content", locale="de", component="haproxy", compare_metadata=True)
        errors.extend(print_errors)
        report["print_pages"] = print_pages
        check_links(printed)
    else:
        errors.append("German print output missing")
    for name in ("LICENSE", "GPL-2.0"):
        license_file = build / "third_party/haproxy" / name
        require(license_file.is_file() and license_file.read_bytes() == (PROJECT / "sources/haproxy/upstream" / name).read_bytes(), f"shared HAProxy {name} missing or changed")
    for entries in search_indexes.values():
        require(Counter(e["ref"] for e in entries if e.get("ref", "").startswith("/de/docs/haproxy/")) == Counter(route(p, True) for p in sources), "search: HAProxy route coverage")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rendered-dir", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = check(args.rendered_dir.resolve())
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    for error in report["errors"]:
        print(error)
    if report["errors"]:
        print(f"German HAProxy rendered check failed: {len(report['errors'])} errors.")
        return 1
    print(f"German HAProxy rendered check passed: {report['source_pairs']} source pairs, {len(report['pages'])} complete routes, navigation, aliases, search, Markdown, print, LLMS, attribution and assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
