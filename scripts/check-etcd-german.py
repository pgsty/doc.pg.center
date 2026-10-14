#!/usr/bin/env python3
"""Accept the complete German etcd edition against current sources and a production build.

The review record binds the separate semantic review to exact source/target
bytes. Structural checks complement that review; they do not replace it.
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
from urllib.parse import urlsplit

PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content/docs/etcd"
RECORD = PROJECT / "data/translation-audits/etcd-de.json"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, PROJECT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


parity = load_module("etcd_german_parity", "etcd_source_parity.py")
links = load_module("etcd_german_links", "check-local-links.py")
printing = load_module("etcd_german_print", "check-pgbackrest-ja-print.py")


class Document(links.DocumentParser):
    def __init__(self, path: Path):
        super().__init__()
        self.canonical = ""
        self.redirect = ""
        self.language = ""
        self.sidebar: list[str] = []
        self.pager: dict[str, str] = {}
        self.switches: list[str] = []
        self.fallbacks: list[str] = []
        self.print_pages = 0
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        values = dict(attrs)
        if tag == "html":
            self.language = values.get("lang", "")
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href", "")
        if tag == "meta" and (values.get("http-equiv") or "").lower() == "refresh":
            self.redirect = (values.get("content") or "").partition("url=")[2]
        if tag == "h1" and re.fullmatch(r"pg-[^-]+", values.get("id", "")):
            self.print_pages += 1
        if tag != "a":
            return
        href = values.get("href", "")
        classes = (values.get("class") or "").split()
        if "td-shell-tree__link" in classes:
            self.sidebar.append(href)
        for direction in ("prev", "next"):
            if f"data-td-pager-{direction}" in values:
                self.pager[direction] = href
        if "hreflang" in values:
            self.switches.append(href)
        if values.get("data-fallback-language"):
            self.fallbacks.append(href)


def route(source: Path) -> str:
    relative = source.relative_to(PROJECT / "content")
    logical = relative.parent if source.name in {"_index.md", "index.md"} else relative.with_suffix("")
    return "/" + logical.as_posix().lower().strip("/") + "/"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fenced_blocks(body: str) -> list[str]:
    """Include fences inside lists and blockquotes, preserving their raw bytes."""
    blocks: list[str] = []
    current: list[str] = []
    marker = ""
    for line in body.splitlines(keepends=True):
        if marker:
            current.append(line)
            if re.fullmatch(r"[ \t]*(?:>[ \t]*)*" + re.escape(marker[0]) + "{" + str(len(marker)) + r",}[ \t]*\n?", line):
                blocks.append("".join(current))
                marker = ""
                current = []
        else:
            match = re.match(r"^[ \t]*(?:>[ \t]*)*(`{3,}|~{3,})", line)
            if match:
                marker = match[1]
                current = [line]
    if marker:
        raise ValueError("unterminated code fence")
    return blocks


def table_numbers(body: str) -> list[list[Counter]]:
    """Keep numeric facts in their original rows and cells, not just the page."""
    for block in fenced_blocks(body):
        body = body.replace(block, "", 1)
    return [
        [Counter(parity.NUMBER_RE.findall(cell)) for cell in re.split(r"(?<!\\)\|", line)]
        for line in body.splitlines() if line.lstrip().startswith("|")
    ]


def flatten(node: dict) -> list[dict]:
    return [node] + [item for child in node.get("children", []) for item in flatten(child)]


def visible_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def rendered_body(path: Path) -> tuple[str, list[tuple[str, str]], list[str]]:
    """Bind the approved rendered prose/code, headings and content links.

    The record is established only after source review and production QA. Site
    chrome, backlinks and generated section listings do not affect the digest.
    """
    sections = printing.content_sections(printing.read_document(path))
    if len(sections) != 1:
        raise ValueError(f"{path}: expected one content section, found {len(sections)}")
    section = sections[0]
    metadata = printing.content_metadata(section)
    headings = metadata["headings"]
    hrefs = []
    def content_links(node):
        if node.classes & {"td-page-end", "td-page-meta"}:
            return
        if node.tag == "a":
            hrefs.append(node.attrs.get("href", ""))
        for child in node.children:
            if isinstance(child, printing.Node):
                content_links(child)
    content_links(section)
    payload = {"blocks": printing.body_blocks(section), "metadata": metadata, "links": hrefs}
    fingerprint = hashlib.sha256(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
    return fingerprint, headings, hrefs


def front_text(path: Path, key: str) -> str:
    blocks = parity.front_matter_blocks(parity.split_front_matter(path.read_text())[0])
    raw = blocks.get(key, "").partition(":")[2].strip()
    if raw.startswith('"'):
        return json.loads(raw)
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1].replace("''", "'")
    return raw


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rendered-dir", type=Path, help="production Hugo output; enables complete rendered acceptance")
    args = parser.parse_args()
    root = args.rendered_dir.resolve() if args.rendered_dir else None
    errors: list[str] = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    sources = sorted(path for path in CONTENT.rglob("*.md") if parity.is_english_source(path))
    targets = {path.with_suffix(".de.md") for path in sources}
    actual = set(CONTENT.rglob("*.de.md"))
    require(bool(sources), "no English etcd pages")
    require(actual == targets, f"German pairing mismatch: missing={sorted(targets - actual)}, orphan={sorted(actual - targets)}")
    try:
        record = json.loads(RECORD.read_text())
        rows = record["pages"]
        by_source = {row["source"]: row for row in rows}
    except (OSError, KeyError, ValueError) as exc:
        print(f"Cannot read semantic review record: {exc}", file=sys.stderr)
        return 1
    expected_sources = {str(path.relative_to(PROJECT)) for path in sources}
    require(len(rows) == len(by_source) == len(sources), "review page count or unique source count differs")
    require(set(by_source) == expected_sources, "review record does not cover exactly the current English pages")
    for source in sources:
        target = source.with_suffix(".de.md")
        label = str(source.relative_to(PROJECT))
        row = by_source.get(label, {})
        require(row.get("source_sha256") == digest(source), f"{label}: source changed since semantic review")
        if not target.exists():
            continue
        require(row.get("target_sha256") == digest(target), f"{label}: translation changed since semantic review")
        require(row.get("review_status") == "passed", f"{label}: semantic review incomplete")
        parity.validate_pair(source, target, root, errors, current_source=True)
        en_body = parity.split_front_matter(source.read_text())[1]
        de_body = parity.split_front_matter(target.read_text())[1]
        require(fenced_blocks(en_body) == fenced_blocks(de_body), f"{label}: code/output changed (including indented fences)")
        require(table_numbers(en_body) == table_numbers(de_body), f"{label}: numeric facts moved between table cells")

    if root:
        documents: dict[Path, Document] = {}

        def document(path: Path):
            path = path.resolve()
            if path not in documents:
                require(path.is_file(), f"missing rendered file: {path}")
                if not path.is_file():
                    return None
                documents[path] = Document(path)
            return documents[path]

        def at(path: str):
            return document(root / path.strip("/") / "index.html")

        expected_routes = {"/de" + route(source) for source in sources}
        rendered_headings = {}
        markdown_outputs = {}
        bundle = root / "de/docs/etcd/llms-full.txt"
        require(bundle.is_file(), f"missing {bundle}")
        bundle_text = bundle.read_text() if bundle.exists() else ""
        llms = root / "de/llms.txt"
        require(llms.is_file() and "/de/docs/etcd/llms-full.txt" in llms.read_text(), "German llms.txt lacks etcd bundle")
        printed = at("/de/_print/docs/etcd/")
        english_print = at("/_print/docs/etcd/")
        if printed and english_print:
            require(printed.print_pages == english_print.print_pages == len(sources) - 1, "print bundle does not contain every child page")
            print_errors, print_pages = printing.check_print(root, sources, PROJECT / "content", locale="de", component="etcd", compare_metadata=True)
            errors.extend(print_errors)
        for source in sources:
            logical = route(source)
            localized = "/de" + logical
            en, de = at(logical), at(localized)
            if not en or not de:
                continue
            require(de.language == "de-DE", f"{localized}: unexpected HTML language {de.language!r}")
            require(de.canonical == "https://doc.pg.center" + localized and not de.redirect, f"{localized}: incorrect canonical or fallback redirect")
            require(de.sidebar == ["/de" + value for value in en.sidebar], f"{localized}: sidebar order or language differs from English")
            require(len(de.sidebar) == len(sources) and set(de.sidebar) == expected_routes, f"{localized}: sidebar omits or duplicates component pages")
            require(de.pager == {key: "/de" + value for key, value in en.pager.items()}, f"{localized}: previous/next destinations differ from English")
            if localized in de.sidebar:
                position = de.sidebar.index(localized)
                expected_pager = {}
                if position:
                    expected_pager["prev"] = de.sidebar[position - 1]
                if position + 1 < len(de.sidebar):
                    expected_pager["next"] = de.sidebar[position + 1]
                require(de.pager == expected_pager, f"{localized}: pager is incomplete or not in sidebar reading order")
            require(logical in de.switches, f"{localized}: missing English language switch")
            require(localized in en.switches, f"{logical}: missing German language switch")
            require(not any("/docs/etcd/" in value for value in de.fallbacks), f"{localized}: English fallback remains")
            fingerprint, page_headings, body_hrefs = rendered_body(root / localized.strip("/") / "index.html")
            row = by_source[str(source.relative_to(PROJECT))]
            require(fingerprint == row.get("rendered_body_sha256"), f"{localized}: rendered body differs from approved source/build review")
            rendered_headings[localized] = page_headings
            require(page_headings and page_headings[0] == ("h1", front_text(source.with_suffix(".de.md"), "title")), f"{localized}: rendered title differs from current German source")
            for href in body_hrefs:
                parsed = urlsplit(href)
                if (not parsed.netloc or parsed.hostname in parity.INTERNAL_HOSTS) and parsed.path.startswith("/docs/etcd/"):
                    require(Path(parsed.path).suffix in parity.SHARED_ASSET_EXTENSIONS, f"{localized}: English component link in rendered content: {href}")
            headings = parity.heading_rows(parity.split_front_matter(source.read_text())[1])
            for anchor in parity.rendered_heading_ids(source, headings, root):
                require(anchor in de.anchors, f"{localized}: missing rendered English anchor {anchor}")
                if printed:
                    require(any(value.endswith("--" + anchor) for value in printed.anchors), f"print bundle: missing heading {anchor}")
            markdown = root / localized.strip("/") / "index.md"
            require(markdown.is_file() and markdown.stat().st_size > 0, f"{localized}: missing Markdown output")
            if markdown.is_file():
                markdown_text = markdown.read_text().strip()
                markdown_outputs[localized] = markdown_text
                de_body = parity.split_front_matter(source.with_suffix(".de.md").read_text())[1].strip()
                require(de_body in markdown_text, f"{localized}: Markdown omits or changes current German body")
                entry = "Source: https://doc.pg.center" + localized + "index.md\n================\n\n" + markdown_text
                require(bundle_text.count(entry) == 1, f"{localized}: LLMS omits, duplicates or changes the complete Markdown page")
            front = parity.split_front_matter(source.read_text())[0]
            aliases = parity.front_matter_blocks(front).get("aliases", "")
            for alias in re.findall(r"/[A-Za-z0-9_./-]+", aliases):
                old = at("/de" + alias)
                if old:
                    require(old.canonical == old.redirect == "https://doc.pg.center" + localized, f"{alias}: German legacy alias target differs")
        for locale in ("", "de/"):
            path = root / locale / "navigation.json"
            require(path.is_file(), f"missing {path}")
        if all((root / locale / "navigation.json").is_file() for locale in ("", "de/")):
            en_nodes = [node for node in flatten(json.loads((root / "navigation.json").read_text())["root"]) if node["id"].startswith("/docs/etcd/")]
            de_nodes = [node for node in flatten(json.loads((root / "de/navigation.json").read_text())["root"]) if node["id"].startswith("/docs/etcd/")]
            require([node["id"] for node in de_nodes] == [node["id"] for node in en_nodes], "navigation.json order or page set differs")
            require({urlsplit(node["url"]).path for node in de_nodes} == expected_routes, "navigation.json German routes incomplete")
            require(all(node["markdown"] == node["url"] + "index.md" for node in de_nodes), "navigation.json Markdown destinations differ")
            require(all(node["url"] == "https://doc.pg.center/de" + node["id"] for node in de_nodes), "navigation.json node IDs point to a different page")
        indexes = list(root.glob("offline-search-index.de.*.json"))
        require(len(indexes) == 1, "expected exactly one German search index")
        if len(indexes) == 1:
            entries = json.loads(indexes[0].read_text())
            found = [entry["ref"] for entry in entries if entry["ref"].startswith("/de/docs/etcd/")]
            require(set(found) == expected_routes and len(found) == len(expected_routes), "search index omits or duplicates etcd pages")
            by_route = {entry["ref"]: entry for entry in entries}
            for source in sources:
                localized = "/de" + route(source)
                entry = by_route.get(localized, {})
                target = source.with_suffix(".de.md")
                require(entry.get("title") == front_text(target, "title"), f"{localized}: search title differs from current German source")
                description = front_text(target, "description")
                if description:
                    require(entry.get("description", "") == description, f"{localized}: search description differs from current German source")
                elif parity.split_front_matter(target.read_text())[1].strip():
                    require(bool(entry.get("description", "")), f"{localized}: search omits the generated German summary")
                # The configured Hugo table of contents indexes levels 2–4;
                # API headings at levels 5–6 remain checked in HTML and print.
                expected_headings = " ".join(value for tag, value in rendered_headings.get(localized, [])[1:] if tag in {"h2", "h3", "h4"})
                require(visible_text(entry.get("headings", "")) == expected_headings, f"{localized}: search headings differ from rendered German content")
        home = at("/de/")
        if home:
            require(not any("/docs/etcd/" in value for value in home.fallbacks), "homepage falls back to English etcd")
            home_hrefs = {value for attribute, value in home.links if attribute == "href"}
            for suffix in ("", "quickstart/", "install/", "op-guide/configuration/", "op-guide/maintenance/", "learning/api/", "upgrades/upgrade_3_7/"):
                require("/de/docs/etcd/" + suffix in home_hrefs, f"homepage etcd shortcut missing: {suffix}")
        # Validate all local links/assets/fragments originating in the complete
        # German collection, its print bundle, and the homepage.
        for path, doc in list(documents.items()):
            relative = path.relative_to(root).as_posix()
            if not (relative.startswith("de/docs/etcd/") or relative in {"de/_print/docs/etcd/index.html", "de/index.html"}):
                continue
            for attribute, raw in doc.links:
                target, fragment = links.resolve_target(root, path, raw)
                if target is None:
                    continue
                require(target.is_relative_to(root), f"{relative}: link escapes root: {raw}")
                require(target.exists(), f"{relative}: missing {attribute} target: {raw}")
                generated_rss = urlsplit(raw).path in {route + "index.xml" for route in expected_routes}
                require(generated_rss or not parity.localized_shared_asset(raw), f"{relative}: localized shared asset: {raw}")
                if fragment and target.suffix == ".html" and target.exists():
                    destination = document(target)
                    valid_print = "_print" in target.parts and any(anchor.endswith("--" + fragment) for anchor in destination.anchors)
                    require(fragment in destination.anchors or valid_print, f"{relative}: missing fragment: {raw}")

    if errors:
        print("German etcd acceptance failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(sources)} current English/German etcd pairs and exact semantic-review hashes" + ("; all routes, aliases, anchors, navigation, pagers, switches, search, assets, Markdown, print and LLMS outputs passed." if root else "."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
