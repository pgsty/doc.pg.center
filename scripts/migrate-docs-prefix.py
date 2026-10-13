#!/usr/bin/env python3
"""One-time content/ -> content/docs/ migration; preview by default, --write to apply.

Rewrite Markdown link destinations, local site URLs, and navigation data without
touching upstream URLs or fenced code. Keep old HTML routes as Hugo aliases;
aliases omit the locale because Hugo adds it. Already-moved trees are a no-op.
Generator and validation code changes accompany this script in the migration.
"""

from __future__ import annotations

import argparse
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

PROJECT = Path(__file__).resolve().parent.parent
COMPONENTS = ("patroni", "pgbackrest", "pgbouncer", "pgbadger", "haproxy", "etcd")
LOCALES = ("zh", "fr", "ja", "de", "ru")
ROOT_RE = re.compile(r"^/(?P<locale>(?:zh|fr|ja|de|ru)/)?(?P<root>" + "|".join(COMPONENTS) + r")(?=/|$)")
LINK_RE = re.compile(
    r"(?P<prefix>\]\(\s*<?|(?:href|src)=[\"']|^\s*\[(?!\^)[^]\n]+\]:\s*<?)"
    r"(?P<url>[^\s<>\"')]+)", re.MULTILINE
)
SITE_URL_RE = re.compile(r"https?://(?:www\.)?pig\.center/[^\s<>\"')`\]]*")
ALIAS_RE = re.compile(r"^aliases:.*(?:\n[ \t]+-[^\n]*)*\n", re.MULTILINE)


def prefix_url(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.netloc and parsed.netloc not in {"pig.center", "www.pig.center"}:
        return url
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return url
    path = ROOT_RE.sub(lambda m: "/" + (m["locale"] or "") + "docs/" + m["root"], parsed.path)
    return urlunsplit(parsed._replace(path=path))


def page_route(path: Path) -> tuple[str, str]:
    relative = path.relative_to(PROJECT / "content")
    stem = relative.stem
    locale = ""
    if stem.rsplit(".", 1)[-1] in LOCALES:
        stem, locale = stem.rsplit(".", 1)
    route = relative.parent if stem in {"_index", "index"} else relative.with_name(stem)
    return "/" + route.as_posix().lower().strip("/") + "/", locale


def rewrite_markdown(text: str, source: Path) -> str:
    front, body = text.split("\n---\n", 1)
    relative = source.relative_to(PROJECT / "content")
    moved = relative.parts[0] in COMPONENTS
    if moved and not source.name.startswith("_div_"):
        old_route, _ = page_route(source)
        canonical = prefix_url(old_route)
        block = ALIAS_RE.search(front + "\n")
        aliases = re.findall(r"/[A-Za-z0-9_./-]+", block[0]) if block else []
        aliases = list(dict.fromkeys([*aliases, old_route]))
        aliases = [alias for alias in aliases if alias != canonical]
        if block and block[0].startswith("aliases:\n"):
            replacement = "aliases:\n" + "".join(f"  - {alias}\n" for alias in aliases)
        else:
            replacement = "aliases: [" + ", ".join(aliases) + "]\n"
        if block:
            front = ALIAS_RE.sub(lambda _: replacement, front + "\n").rstrip("\n")
        else:
            front += "\n" + replacement.rstrip("\n")

    def target(match: re.Match) -> str:
        url = match["url"]
        parsed = urlsplit(url)
        if moved and parsed.path and not parsed.scheme and not parsed.netloc and not parsed.path.startswith("/"):
            # Hugo resolves relative page links against the source directory.
            logical = posixpath.normpath("/" + relative.parent.as_posix() + "/" + parsed.path)
            if parsed.path.endswith("/"):
                logical += "/"
            url = urlunsplit(parsed._replace(path=logical))
            _, locale = page_route(source)
            if locale and not Path(parsed.path).suffix:
                url = "/" + locale + url
        return match["prefix"] + prefix_url(url)

    lines = []
    fence = ""
    for line in body.splitlines(keepends=True):
        marker = re.match(r"^\s*(?:>\s*)*(`{3,}|~{3,})", line)
        if marker:
            if not fence:
                fence = marker[1]
            elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = ""
            lines.append(line)
        elif fence:
            lines.append(line)
        else:
            line = LINK_RE.sub(target, line)
            lines.append(SITE_URL_RE.sub(lambda m: prefix_url(m[0]), line))
    return front + "\n---\n" + "".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    roots = [PROJECT / "content" / name for name in COMPONENTS]
    if not any(path.exists() for path in roots):
        print("Component trees already live under content/docs; nothing to migrate.")
        return
    if not all(path.is_dir() for path in roots):
        parser.error("expected all six original component directories")
    if any((PROJECT / "content/docs" / name).exists() for name in COMPONENTS):
        parser.error("refusing to overwrite an existing content/docs component")
    updates = {}
    for path in (PROJECT / "content").rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        updated = rewrite_markdown(text, path)
        if text != updated:
            updates[path] = updated
    for path in [PROJECT / "hugo.yaml", *(PROJECT / "data").rglob("*.yaml")]:
        text = path.read_text(encoding="utf-8")
        updated = re.sub(
            r"(?P<key>\b(?:url|pageRef):\s*)(?P<url>[^\s,}]+)",
            lambda m: m["key"] + prefix_url("/" + m["url"] if m["url"].split("/")[0] in COMPONENTS else m["url"]),
            text,
        )
        if text != updated:
            updates[path] = updated
    for path, text in updates.items():
        if args.write:
            path.write_text(text, encoding="utf-8")
    if args.write:
        (PROJECT / "content/docs").mkdir(exist_ok=True)
        for path in roots:
            path.rename(PROJECT / "content/docs" / path.name)
    print(f"{'Updated' if args.write else 'Would update'} {len(updates)} files and move six component directories.")


if __name__ == "__main__":
    main()
