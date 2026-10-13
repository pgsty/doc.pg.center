#!/usr/bin/env python3
"""Verify all Japanese etcd routes and derived outputs in a production build."""

from __future__ import annotations

import argparse
from collections import Counter
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

PROJECT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("etcd_ja", PROJECT / "scripts/check-japanese-parity.py")
parity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parity)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids, self.headings, self.links, self.assets = [], [], [], []
        self.canonical, self.sidebar, self.previous, self.next = [], [], [], []
        self.alternates = {}
        self.search = ""
        self.pre, self.current_pre = [], None
        self.bodies = []
        self.content_images = []
        self.feed(text)

    def in_content(self):
        return any("td-content" in attrs.get("class", "").split() for _, attrs in self.stack)

    def handle_starttag(self, tag, attrs):
        data = {key: value or "" for key, value in attrs}
        if "td-content" in data.get("class", "").split():
            self.bodies.append([])
        if data.get("id"):
            self.ids.append(data["id"])
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical.append(data.get("href", ""))
        if tag == "link" and data.get("rel") == "alternate":
            self.alternates[data.get("hreflang", "")] = data.get("href", "")
        if tag == "a":
            self.links.append(data)
            if "td-shell-tree__link" in data.get("class", "").split():
                self.sidebar.append(data.get("href", ""))
            if "data-td-pager-prev" in data:
                self.previous.append(data.get("href", ""))
            if "data-td-pager-next" in data:
                self.next.append(data.get("href", ""))
        if tag in {"img", "script", "source"} and data.get("src"):
            self.assets.append(data["src"])
        if self.in_content() and tag in {"img", "source"}:
            self.content_images.append((tag, data.get("src", ""), data.get("srcset", ""), data.get("alt", "")))
        if tag == "link" and data.get("rel") == "stylesheet":
            self.assets.append(data.get("href", ""))
        if data.get("data-td-index-src"):
            self.search = data["data-td-index-src"]
        if self.in_content() and re.fullmatch(r"h[1-6]", tag) and data.get("id"):
            self.headings.append((tag, data["id"]))
        if tag == "pre" and self.in_content():
            self.current_pre = []
        if tag not in VOID:
            self.stack.append((tag, data))

    def handle_endtag(self, tag):
        if tag == "pre" and self.current_pre is not None:
            self.pre.append("".join(self.current_pre))
            self.current_pre = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, value):
        if self.current_pre is not None:
            self.current_pre.append(value)
        excluded = {"td-page-heading", "lead", "td-article-meta", "td-page-end",
                    "td-page-notice", "td-section-index", "title"}
        if self.in_content() and not any(
            excluded.intersection(attrs.get("class", "").split())
            or (tag == "h1" and re.fullmatch(r"pg-[a-f0-9]{32}", attrs.get("id", "")))
            for tag, attrs in self.stack
        ):
            self.bodies[-1].append(value)


def route(source: Path, japanese=False):
    path = source.relative_to(PROJECT / "content").with_suffix("")
    if path.name in {"_index", "index"}:
        path = path.parent
    return ("/ja/" if japanese else "/") + path.as_posix().lower() + "/"


def flatten(node):
    yield node
    for child in node.get("children", []):
        yield from flatten(child)


def component_navigation(path):
    payload = json.loads(path.read_text())
    return next(node for node in flatten(payload["root"]) if node["id"] == "/docs/etcd/")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rendered-dir", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.rendered_dir.resolve()
    source_root = PROJECT / "content/docs/etcd"
    sources = sorted(p for p in source_root.rglob("*.md") if not parity.LOCALE.search(p.name))
    errors, records, loaded = [], [], {}
    def check(condition, message):
        if not condition:
            errors.append(message)
    def load(path):
        if path not in loaded:
            loaded[path] = Page(path.read_text())
        return loaded[path]
    bundle_path = root / "ja/docs/etcd/llms-full.txt"
    bundle = bundle_path.read_text() if bundle_path.is_file() else ""
    en_tree = component_navigation(root / "navigation.json")
    ja_tree = component_navigation(root / "ja/navigation.json")
    en_nav, ja_nav = list(flatten(en_tree)), list(flatten(ja_tree))
    ja_order = [urlsplit(p["url"]).path for p in ja_nav]
    weights = {}
    for source in sources:
        front, _ = parity.structure.split_front_matter(source.read_text())
        weights[route(source)] = parity.structure.front_value(front, "weight")

    def check_tree(en, ja):
        en_children, ja_children = en.get("children", []), ja.get("children", [])
        en_ids, ja_ids = [p["id"] for p in en_children], [p["id"] for p in ja_children]
        check(Counter(en_ids) == Counter(ja_ids), f"navigation: {en['id']} child hierarchy")
        # Hugo ByWeight breaks equal weights using localized titles. Preserve
        # all source weights and hierarchy while allowing only those ties.
        check([weights.get(x) for x in en_ids] == [weights.get(x) for x in ja_ids],
              f"navigation: {en['id']} weighted order")
        translated = {p["id"]: p for p in ja_children}
        for child in en_children:
            if child["id"] in translated:
                check_tree(child, translated[child["id"]])
    check_tree(en_tree, ja_tree)
    all_pre = Counter()
    all_images = Counter()
    for source in sources:
        label = source.relative_to(source_root).as_posix()
        destination = route(source, True)
        html_path = root / destination.lstrip("/") / "index.html"
        md_path = html_path.with_name("index.md")
        target = source.with_suffix(".ja.md")
        if not all(p.is_file() for p in (html_path, md_path, target)):
            errors.append(f"{label}: missing Japanese source, HTML or Markdown")
            continue
        page = load(html_path)
        english = load(root / route(source).lstrip("/") / "index.html")
        check(page.canonical == ["https://pig.center" + destination], f"{label}: canonical route")
        check(page.alternates.get("en-US") == "https://pig.center" + route(source), f"{label}: English language alternate")
        check(english.alternates.get("ja-JP") == "https://pig.center" + destination, f"{label}: Japanese language alternate")
        check(page.headings == english.headings, f"{label}: rendered headings/anchors")
        check(not [key for key, n in Counter(page.ids).items() if n > 1], f"{label}: duplicate rendered IDs")
        check(page.sidebar == ja_order, f"{label}: sidebar differs from Japanese navigation order")
        if destination in ja_order:
            position = ja_order.index(destination)
            check(page.previous == ja_order[max(0, position - 1):position], f"{label}: previous page")
            check(page.next == ja_order[position + 1:position + 2], f"{label}: next page")
        check(page.pre == english.pre, f"{label}: rendered code/output changed")
        all_pre.update(page.pre)
        all_images.update(page.content_images)
        front, body = parity.structure.split_front_matter(target.read_text())
        check(body.strip() in md_path.read_text(), f"{label}: full Japanese body missing from Markdown")
        check(body.strip() in bundle, f"{label}: full Japanese body missing from LLMS")
        check("Copyright 2013-present etcd Authors" in html_path.read_text(), f"{label}: upstream attribution")
        check("creativecommons.org/licenses/by/4.0" in html_path.read_text(), f"{label}: CC-BY-4.0 attribution")
        match = re.search(r"^aliases:\s*\[([^]]*)\]", front, re.M)
        for alias in match[1].split(",") if match else []:
            legacy = root / "ja" / alias.strip(' \"\x27/').lower() / "index.html"
            check(legacy.is_file() and "https://pig.center" + destination in legacy.read_text(),
                  f"{label}: legacy alias {alias}")
        for link in page.links:
            href = link.get("href", "")
            parsed = urlsplit(href)
            if parsed.netloc and parsed.netloc != "pig.center":
                continue
            check(not (link.get("data-fallback-language") and "/docs/etcd/" in parsed.path),
                  f"{label}: English fallback remains: {href}")
            path = parsed.path or destination
            if path.startswith("/ja/docs/etcd/"):
                output = root / path.lstrip("/")
                if path.endswith("/"):
                    output /= "index.html"
                elif not output.suffix:
                    output /= "index.html"
                check(output.is_file(), f"{label}: missing internal target {href}")
                if parsed.fragment and output.is_file() and output.suffix == ".html":
                    check(unquote(parsed.fragment) in load(output).ids, f"{label}: broken anchor {href}")
        for asset in page.assets:
            parsed = urlsplit(asset)
            if not parsed.netloc and parsed.path.startswith("/"):
                check((root / parsed.path.lstrip("/")).is_file(), f"{label}: missing shared asset {asset}")
        search = root / page.search.lstrip("/")
        check(bool(page.search) and search.is_file(), f"{label}: Japanese search index missing")
        if search.is_file():
            entries = json.loads(search.read_text())
            check(any(item.get("ref") == destination for item in entries), f"{label}: page absent from Japanese search")
        records.append({"path": label, "route": destination, "headings": len(page.headings),
                        "preformatted_blocks": len(page.pre), "body_characters": len(body)})

    expected_routes = {route(p, True) for p in sources}
    try:
        check(Counter(p["id"] for p in en_nav) == Counter(p["id"] for p in ja_nav),
              "navigation: missing or duplicate logical pages")
        check({urlsplit(p["url"]).path for p in ja_nav} == expected_routes, "navigation: incomplete Japanese route set")
        english_nodes = {p["id"]: p for p in en_nav}
        for ja in ja_nav:
            en = english_nodes.get(ja["id"], {})
            for key in ("url", "markdown"):
                check(parity.normalize_routes(ja[key]) == en.get(key), f"navigation: {ja['id']} {key}")
        expected_llms = [p["markdown"] for p in ja_nav]
        check(re.findall(r"^Source: (.+)$", bundle, re.M) == expected_llms,
              "LLMS: missing, duplicate or reordered source pages")
    except (OSError, KeyError, StopIteration) as exc:
        errors.append(f"navigation/LLMS: {exc}")
    printed = root / "ja/_print/docs/etcd/index.html"
    if printed.is_file():
        print_page = load(printed)
        for link in print_page.links:
            destination = urlsplit(link.get("href", ""))
            if not destination.scheme and not destination.netloc and not destination.path and destination.fragment:
                check(unquote(destination.fragment) in print_page.ids,
                      f"print: broken internal anchor #{destination.fragment}")
        page_ids = [key for key in print_page.ids if re.fullmatch(r"pg-[a-f0-9]{32}", key)]
        check(len(page_ids) == len(sources) - 1, "print: incomplete child page set")
        check(Counter(print_page.pre) == all_pre, "print: preformatted content differs from all individual pages")
        check(Counter(print_page.content_images) == all_images,
              "print: images or localized alt text differ from individual pages")
        check(len(print_page.bodies) == len(sources), "print: incomplete page body set")
        compact = lambda parts: re.sub(r"\s+", "", "".join(parts))
        for destination, printed_body in zip(ja_order, print_page.bodies):
            original = load(root / destination.lstrip("/") / "index.html")
            check(len(original.bodies) == 1 and compact(original.bodies[0]) in compact(printed_body),
                  f"print: full body missing or changed: {destination}")
            for _, anchor in original.headings:
                check(any(key.endswith("--" + anchor) for key in print_page.ids),
                      f"print: missing namespaced heading {destination}#{anchor}")
        for source in sources:
            target = source.with_suffix(".ja.md")
            if target.is_file():
                front, _ = parity.structure.split_front_matter(target.read_text())
                raw = parity.structure.front_value(front, "title")[0]
                title = json.loads(raw) if raw.startswith('"') else raw.strip("'")
                check(title in printed.read_text(), f"print: missing title {title}")
    else:
        errors.append("print: missing Japanese component bundle")
    assets = [p for p in source_root.rglob("*") if p.is_file() and p.suffix != ".md"]
    for asset in assets:
        relative = asset.relative_to(PROJECT / "content")
        published = root / relative
        check(published.is_file() and published.read_bytes() == asset.read_bytes(), f"shared resource changed: {relative}")
        check(not (root / "ja" / relative).exists(), f"duplicated Japanese shared resource: {relative}")
    homepage = root / "ja/index.html"
    if homepage.is_file():
        home_links = load(homepage).links
        for suffix in ("", "quickstart/", "install/", "op-guide/configuration/",
                       "op-guide/maintenance/", "learning/api/", "upgrades/upgrade_3_7/"):
            check(any(link.get("href") == "/ja/docs/etcd/" + suffix for link in home_links),
                  f"homepage: missing Japanese etcd entry {suffix}")
        check(not any("/docs/etcd/" in link.get("href", "") and link.get("data-fallback-language")
                      for link in home_links), "homepage: etcd English fallback remains")
    else:
        errors.append("homepage: Japanese route missing")
    report = {"component": "etcd", "language": "ja", "pages": records,
              "shared_resources": len(assets), "errors": errors}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    for error in errors:
        print(error)
    if errors:
        print(f"Japanese etcd rendered validation failed: {len(errors)} errors.")
        return 1
    print(f"Validated {len(records)} Japanese etcd rendered pages, aliases, anchors, navigation, "
          f"pager, language switches, search, Markdown, print, LLMS and {len(assets)} shared resources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
