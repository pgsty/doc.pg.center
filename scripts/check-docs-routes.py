#!/usr/bin/env python3
"""Check top-level component routes, aliases, and published discovery outputs."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

PROJECT = Path(__file__).resolve().parent.parent
COMPONENTS = ("patroni", "pgbackrest", "pgbouncer", "pgbadger", "haproxy", "etcd")
LOCALES = ("en", "zh", "fr", "ja", "de", "ru")
REMOVED_DOCS_ROUTE = re.compile(r"^/(?:(?:zh|fr|ja|de|ru)/)?(?:_print/)?docs(?:/|$)")


class Head(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.canonical = ""
        self.redirect = ""
        self.alternates: set[str] = set()
        with path.open(encoding="utf-8") as document:
            # Canonical and refresh metadata live in the head, even on the
            # large manuals. Avoid parsing their full bodies a second time.
            head = ""
            while "</head>" not in head:
                chunk = document.read(4096)
                if not chunk:
                    break
                head += chunk
            self.feed(head.split("</head>", 1)[0])

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href", "")
        if tag == "link" and values.get("rel") == "alternate" and values.get("hreflang"):
            self.alternates.add(urlsplit(values.get("href", "")).path)
        if tag == "meta" and (values.get("http-equiv") or "").lower() == "refresh":
            self.redirect = (values.get("content") or "").partition("url=")[2]


def navigation_routes(node: dict) -> set[str]:
    routes = {urlsplit(node["url"]).path}
    for child in node.get("children", []):
        routes.update(navigation_routes(child))
    return routes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_dir", type=Path)
    args = parser.parse_args()
    root = args.public_dir.resolve()
    checked: dict[str, Head] = {}
    aliases_checked = 0
    pages_checked = 0
    expected = {language: set() for language in LOCALES}
    llms = {}

    def head(route: str) -> Head:
        if route not in checked:
            path = root / unquote(route).strip("/") / "index.html"
            assert path.is_file(), f"Missing route: {route}"
            checked[route] = Head(path)
        return checked[route]

    for language in LOCALES:
        prefix = "" if language == "en" else f"/{language}"
        for removed in (f"{prefix}/docs", f"{prefix}/_print/docs"):
            assert not (root / removed.lstrip("/")).exists(), f"Removed route still published: {removed}"
        llms[language] = (root / prefix.lstrip("/") / "llms.txt").read_text()

    content = PROJECT / "content"
    sources = sorted(source for component in COMPONENTS for source in (content / component).rglob("*.md"))
    for source in sources:
        if source.name.startswith("_div_"):
            continue
        relative = source.relative_to(content)
        stem = source.stem
        language = stem.rsplit(".", 1)[-1] if "." in stem else "en"
        if language != "en":
            stem = stem.rsplit(".", 1)[0]
        route_path = relative.parent if stem in {"_index", "index"} else relative.with_name(stem)
        logical = "/" + route_path.as_posix().lower().strip("/") + "/"
        prefix = "" if language == "en" else f"/{language}"
        canonical = f"{prefix}{logical}"
        metadata = head(canonical)
        assert metadata.canonical == f"https://doc.pg.center{canonical}", canonical
        assert not metadata.redirect, canonical
        alternates = {("" if lang == "en" else f"/{lang}") + logical for lang in LOCALES}
        assert metadata.alternates == alternates, f"Incorrect language alternates: {canonical}"
        assert (root / canonical.strip("/") / "index.md").is_file(), canonical
        assert f"](https://doc.pg.center{canonical}index.md)" in llms[language], f"Missing llms.txt entry: {canonical}"
        expected[language].add(canonical)
        front = source.read_text(encoding="utf-8").split("\n---\n", 1)[0]
        block = re.search(r"^aliases:.*(?:\n[ \t]+-[^\n]*)*", front, re.M)
        aliases = re.findall(r"/[A-Za-z0-9_./-]+", block[0]) if block else []
        assert len(aliases) == len(set(aliases)), f"Duplicate aliases: {source}"
        for alias in aliases:
            old = prefix + alias
            assert not REMOVED_DOCS_ROUTE.match(old), f"Removed prefix in alias: {source}"
            assert old != canonical, f"Self redirect: {source}"
            assert urlsplit(head(old).canonical).path == canonical, old
            assert urlsplit(head(old).redirect).path == canonical, old
            aliases_checked += 1
        if stem == "_index" and len(relative.parts) == 2:
            component = relative.parts[0]
            for output in ("index.xml", "llms-full.txt"):
                artifact = root / canonical.strip("/") / output
                assert artifact.is_file() and artifact.stat().st_size, artifact
            printed = root / f"{prefix}/_print/{component}/index.html".lstrip("/")
            assert printed.is_file(), printed
            assert canonical + "llms-full.txt" in llms[language], canonical
        pages_checked += 1

    sitemap_routes = {
        urlsplit(loc.text).path
        for sitemap in root.rglob("sitemap.xml")
        for loc in ElementTree.parse(sitemap).findall(".//{*}url/{*}loc")
    }
    for route in sitemap_routes:
        assert not REMOVED_DOCS_ROUTE.match(route), f"Removed route in sitemap: {route}"
        head(route)

    for language in LOCALES:
        prefix = "" if language == "en" else language + "/"
        navigation = json.loads((root / prefix / "navigation.json").read_text())
        routes = navigation_routes(navigation["root"])
        assert expected[language] <= routes, f"Missing {language} navigation routes: {expected[language] - routes}"
        top_sections = {
            urlsplit(node["url"]).path
            for node in navigation["root"].get("children", []) if node["kind"] == "section"
        }
        assert top_sections == {f"/{prefix}{component}/" for component in COMPONENTS}, top_sections
        indexes = list(root.glob(f"offline-search-index.{language}.*.json"))
        assert len(indexes) == 1, f"Expected one {language} search index"
        search_routes = {doc["ref"] for doc in json.loads(indexes[0].read_text())}
        assert expected[language] <= search_routes, f"Missing {language} search routes: {expected[language] - search_routes}"
        assert expected[language] <= sitemap_routes, f"Missing {language} sitemap routes: {expected[language] - sitemap_routes}"
        for route in routes | search_routes:
            assert not REMOVED_DOCS_ROUTE.match(route), f"Removed route in discovery output: {route}"
            head(route)

    resources_checked = 0
    for component in COMPONENTS:
        for resource in (content / component).rglob("*"):
            if resource.is_file() and resource.suffix != ".md":
                target = root / resource.relative_to(content)
                assert target.is_file() and target.read_bytes() == resource.read_bytes(), target
                resources_checked += 1

    print(f"Validated {pages_checked} top-level documentation pages, {aliases_checked} chapter aliases, "
          f"{resources_checked} resources, language alternates, navigation, search, sitemaps, and component outputs.")


if __name__ == "__main__":
    main()
