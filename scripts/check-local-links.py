#!/usr/bin/env python3
"""Validate internal HTML links and fragments in a rendered Hugo site."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


INTERNAL_HOSTS = {"pgsql.cc", "www.pgsql.cc"}
SKIP_SCHEMES = {"data", "javascript", "mailto", "tel"}
LEGACY_COMPONENT_ROUTE = re.compile(
    r"^(?:(?:zh|fr|ja|de|ru)/)?(?:_print/)?"
    r"(?:patroni|pgbackrest|pgbouncer|pgbadger|haproxy|etcd)(?:/|$)"
)


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: set[str] = set()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        for key in ("id", "name"):
            value = attributes.get(key)
            if value:
                self.anchors.add(value)
        if tag in {"a", "link"} and attributes.get("href") is not None:
            self.links.append(("href", attributes["href"] or ""))
        if tag in {"img", "script", "iframe", "source"} and attributes.get("src") is not None:
            self.links.append(("src", attributes["src"] or ""))


def load_document(path: Path) -> DocumentParser:
    parser = DocumentParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def resolve_target(root: Path, source: Path, raw_url: str) -> tuple[Path | None, str]:
    parsed = urlsplit(raw_url.strip())
    if parsed.scheme in SKIP_SCHEMES:
        return None, ""
    if parsed.scheme in {"http", "https"} and parsed.netloc not in INTERNAL_HOSTS:
        return None, ""
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return None, ""
    if parsed.netloc and parsed.netloc not in INTERNAL_HOSTS:
        return None, ""

    url_path = unquote(parsed.path)
    if not url_path:
        target = source
    elif url_path.startswith("/"):
        target = root / url_path.lstrip("/")
    else:
        target = source.parent / url_path

    target = target.resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return target, unquote(parsed.fragment)

    if url_path.endswith("/") or target.is_dir():
        target = target / "index.html"
    elif not target.exists() and not target.suffix:
        pretty_target = target / "index.html"
        if pretty_target.exists():
            target = pretty_target
    return target, unquote(parsed.fragment)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("public_dir", type=Path)
    args = parser.parse_args()
    root = args.public_dir.resolve()
    if not root.is_dir():
        parser.error(f"rendered directory does not exist: {root}")

    documents = {path.resolve(): load_document(path) for path in root.rglob("*.html")}
    errors: list[str] = []

    for source, document in documents.items():
        source_rel = source.relative_to(root)
        for attribute, raw_url in document.links:
            target, fragment = resolve_target(root, source, raw_url)
            if target is None:
                continue
            try:
                target_rel = target.relative_to(root)
            except ValueError:
                errors.append(f"{source_rel}: {attribute} escapes site root: {raw_url}")
                continue
            if LEGACY_COMPONENT_ROUTE.match(target_rel.as_posix()):
                errors.append(f"{source_rel}: component link lacks /docs prefix: {raw_url!r}")
            if not target.exists():
                errors.append(f"{source_rel}: missing {target_rel} from {attribute}={raw_url!r}")
                continue
            if fragment and target.suffix == ".html" and "third_party" not in target.parts:
                target_document = documents.get(target)
                if target_document is None:
                    target_document = load_document(target)
                # OINK print bundles namespace every source-page heading as
                # ``pg-<page-hash>--<anchor>`` so duplicate headings from
                # different pages remain valid in one HTML document. A local
                # ``#anchor`` link inside the bundle therefore resolves to a
                # namespaced anchor even though the literal ID is no longer
                # present.
                print_fragment = "_print" in target.parts and any(
                    anchor.endswith(f"--{fragment}")
                    for anchor in target_document.anchors
                )
                if fragment not in target_document.anchors and not print_fragment:
                    errors.append(
                        f"{source_rel}: missing fragment #{fragment} in {target_rel} from {attribute}={raw_url!r}"
                    )

    if errors:
        print("Internal link validation failed:", file=sys.stderr)
        for error in errors[:200]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 200:
            print(f"- ... {len(errors) - 200} more", file=sys.stderr)
        return 1

    print(f"Validated internal links across {len(documents)} rendered HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
