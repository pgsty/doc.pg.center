#!/usr/bin/env python3
"""Check canonical documentation URLs, legacy aliases, and component outputs."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

PROJECT = Path(__file__).resolve().parent.parent
COMPONENTS = ("patroni", "pgbackrest", "pgbouncer", "pgbadger", "haproxy", "etcd")
LOCALES = ("en", "zh", "fr", "ja", "de", "ru")


class Head(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.canonical = ""
        self.redirect = ""
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
        if tag == "meta" and (values.get("http-equiv") or "").lower() == "refresh":
            self.redirect = (values.get("content") or "").partition("url=")[2]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_dir", type=Path)
    args = parser.parse_args()
    root = args.public_dir.resolve()
    checked: dict[str, Head] = {}
    aliases_checked = 0
    pages_checked = 0

    def head(route: str) -> Head:
        if route not in checked:
            path = root / route.strip("/") / "index.html"
            assert path.is_file(), f"Missing route: {route}"
            checked[route] = Head(path)
        return checked[route]

    for language in LOCALES:
        prefix = "" if language == "en" else f"/{language}"
        route = f"{prefix}/docs/"
        assert urlsplit(head(route).canonical).path == route, route
        assert not head(route).redirect, route

    for source in (PROJECT / "content/docs").rglob("*.md"):
        if source.name.startswith("_div_"):
            continue
        relative = source.relative_to(PROJECT / "content/docs")
        if len(relative.parts) == 1:
            continue
        stem = source.stem
        language = stem.rsplit(".", 1)[-1] if "." in stem else "en"
        if language != "en":
            stem = stem.rsplit(".", 1)[0]
        route_path = relative.parent if stem in {"_index", "index"} else relative.with_name(stem)
        logical = "/" + route_path.as_posix().lower().strip("/") + "/"
        prefix = "" if language == "en" else f"/{language}"
        canonical = f"{prefix}/docs{logical}"
        assert urlsplit(head(canonical).canonical).path == canonical, canonical
        assert not head(canonical).redirect, canonical
        assert (root / canonical.strip("/") / "index.md").is_file(), canonical
        front = source.read_text(encoding="utf-8").split("\n---\n", 1)[0]
        block = re.search(r"^aliases:.*(?:\n[ \t]+-[^\n]*)*", front, re.M)
        aliases = re.findall(r"/[A-Za-z0-9_./-]+", block[0]) if block else []
        assert logical in aliases, f"Missing old URL alias: {source}"
        for alias in aliases:
            old = prefix + alias
            assert old != canonical, f"Self redirect: {source}"
            assert urlsplit(head(old).canonical).path == canonical, old
            assert urlsplit(head(old).redirect).path == canonical, old
            aliases_checked += 1
        if stem == "_index" and len(relative.parts) == 2:
            component = relative.parts[0]
            for output in ("index.xml", "llms-full.txt"):
                artifact = root / canonical.strip("/") / output
                assert artifact.is_file() and artifact.stat().st_size, artifact
            printed = root / f"{prefix}/_print/docs/{component}/index.html".lstrip("/")
            assert printed.is_file(), printed
            llms = root / f"{prefix}/llms.txt".lstrip("/")
            assert canonical + "llms-full.txt" in llms.read_text(), llms
        pages_checked += 1

    print(f"Validated {pages_checked} documentation pages, {aliases_checked} legacy aliases, six locale indexes, and component outputs.")


if __name__ == "__main__":
    main()
