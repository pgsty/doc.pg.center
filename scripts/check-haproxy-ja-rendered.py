#!/usr/bin/env python3
"""Verify the complete Japanese HAProxy component in a production Hugo build."""

from __future__ import annotations

import argparse
from collections import Counter
import html
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


PROJECT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("japanese_parity", PROJECT / "scripts/check-haproxy-ja.py")
assert spec and spec.loader
parity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parity)
print_spec = importlib.util.spec_from_file_location("print_body_parity", PROJECT / "scripts/check-pgbackrest-ja-print.py")
assert print_spec and print_spec.loader
print_parity = importlib.util.module_from_spec(print_spec)
print_spec.loader.exec_module(print_parity)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self, text: str) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict]] = []
        self.ids: list[str] = []
        self.content_ids: list[str] = []
        self.links: list[dict] = []
        self.assets: list[str] = []
        self.canonical: list[str] = []
        self.alternates: dict[str, str] = {}
        self.sidebar: list[str] = []
        self.previous: list[str] = []
        self.next: list[str] = []
        self.search = ""
        self.body_text: list[str] = []
        self.headings: list[tuple[str, str]] = []
        self.pre: list[str] = []
        self.current_pre: list[str] | None = None
        self.feed(text)

    def in_content(self) -> bool:
        return any("td-content" in d.get("class", "").split() for _, d in self.stack)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if data.get("id"):
            self.ids.append(data["id"])
            if self.in_content():
                self.content_ids.append(data["id"])
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
        if tag == "link" and data.get("rel") == "stylesheet":
            self.assets.append(data.get("href", ""))
        if data.get("data-td-index-src"):
            self.search = data["data-td-index-src"]
        if self.in_content() and re.fullmatch(r"h[2-6]", tag):
            self.headings.append((tag, data.get("id", "")))
        if tag == "pre" and self.in_content():
            self.current_pre = []
        if tag not in VOID:
            self.stack.append((tag, data))

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre" and self.current_pre is not None:
            self.pre.append("".join(self.current_pre))
            self.current_pre = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, text: str) -> None:
        if self.in_content():
            self.body_text.append(text)
        if self.current_pre is not None:
            self.current_pre.append(text)


def route(source: Path, japanese: bool = False) -> str:
    root = "/ja/docs/haproxy/" if japanese else "/docs/haproxy/"
    return root if source.name == "_index.md" else root + source.stem + "/"


def aliases(front: str) -> list[str]:
    match = re.search(r"(?m)^aliases:\s*\[([^]]*)\]", front)
    if match:
        return [value.strip().strip('\"\'') for value in match.group(1).split(",") if value.strip()]
    match = re.search(r"(?m)^aliases:\s*\n((?:[ \t]+.*\n)+)", front)
    return re.findall(r"(?m)^\s*-\s*(\S+)", match.group(1)) if match else []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.build.resolve()
    source_root = PROJECT / "content/docs/haproxy"
    sources = sorted((p for p in source_root.glob("*.md") if parity.english(p) and not p.name.startswith("_div_")), key=lambda p: int(re.search(r"(?m)^weight:\s*(\d+)", p.read_text()).group(1)))
    reading = [p for p in sources if p.name != "_index.md"]
    sidebar = ["/ja/docs/haproxy/"] + [route(p, True) for p in reading]
    errors: list[str] = []
    report: dict = {"scope": "all current English HAProxy published routes", "pages": [], "errors": errors}
    loaded: dict[Path, Page] = {}
    exceptions = parity.Audit("haproxy").exceptions
    rendered_reviews_used: set[int] = set()

    def load(path: Path) -> Page:
        if path not in loaded:
            loaded[path] = Page(path.read_text())
        return loaded[path]

    def check(ok: bool, message: str) -> None:
        if not ok:
            errors.append(message)

    for source in sources:
        label = source.name
        destination = route(source, True)
        html_path = root / destination.lstrip("/") / "index.html"
        markdown_path = html_path.with_name("index.md")
        if not html_path.is_file() or not markdown_path.is_file():
            errors.append(f"{label}: missing Japanese HTML or Markdown output")
            continue
        page = load(html_path)
        english = load(root / route(source).lstrip("/") / "index.html")
        check(page.canonical == ["https://doc.pg.center" + destination], f"{label}: canonical route")
        check(page.alternates.get("en-US") == "https://doc.pg.center" + route(source), f"{label}: English language alternate")
        check(english.alternates.get("ja-JP") == "https://doc.pg.center" + destination, f"{label}: Japanese language alternate missing from English")
        check(page.headings == english.headings, f"{label}: rendered heading IDs or order changed")
        # OINK namespaces code-copy/viewport controls by localized page identity.
        # Their fence numbers must agree; public heading/entry IDs stay exact.
        stable_ids = lambda values: [re.sub(r"^td-code-[0-9a-f]{8}-fence-", "td-code-LOCALE-fence-", value) for value in values]
        check(stable_ids(page.content_ids) == stable_ids(english.content_ids), f"{label}: rendered body anchor IDs or order changed")
        check(not [value for value, count in Counter(page.ids).items() if count > 1], f"{label}: duplicate rendered IDs")
        check(page.sidebar == sidebar, f"{label}: sidebar does not contain all 35 weighted Japanese routes")
        check(not any(link.get("data-fallback-language") and "/docs/haproxy/" in link.get("href", "") for link in page.links), f"{label}: HAProxy English fallback remains")
        if source in reading:
            index = reading.index(source)
            previous = [route(reading[index - 1], True)] if index else ["/ja/docs/haproxy/"]
            following = [route(reading[index + 1], True)] if index + 1 < len(reading) else []
            check(page.previous == previous, f"{label}: previous page is not its weighted Japanese neighbor")
            check(page.next == following, f"{label}: next page is not its weighted Japanese neighbor")
        else:
            check(page.previous == [] and page.next == [route(reading[0], True)], f"{label}: root pager must lead to the first Japanese reading page")
        target = source.with_suffix(".ja.md")
        if not target.is_file():
            errors.append(f"{label}: missing Japanese Markdown source")
            continue
        front, body = parity.structure.split_front_matter(target.read_text())
        _, en_body = parity.structure.split_front_matter(source.read_text())
        en_fences, _ = parity.structure.parse_fenced_blocks(en_body)
        ja_fences, _ = parity.structure.parse_fenced_blocks(body)
        permitted = set()
        for number, (en, ja) in enumerate(zip(en_fences, ja_fences), 1):
            if any(
                (entry.get("path"), entry.get("section"), entry.get("check"))
                == ("haproxy/" + label, f"fence-{number:04d}", "fenced code/configuration/output")
                and entry.get("source_sha256") == parity.digest(en)
                and entry.get("target_sha256") == parity.digest(ja)
                for entry in exceptions
            ):
                inner = lambda value: html.unescape("\n".join(value.splitlines()[1:-1])).strip()
                permitted.add((inner(en), inner(ja)))
        check(len(english.pre) == len(page.pre), f"{label}: rendered preformatted block count changed")
        for number, (en, ja) in enumerate(zip(english.pre, page.pre), 1):
            if en != ja and (en.strip(), ja.strip()) not in permitted:
                matching = [index for index, entry in enumerate(exceptions) if (
                    (entry.get("path"), entry.get("section"), entry.get("check"))
                    == ("haproxy/" + label, f"rendered-pre-{number:04d}", "rendered explanatory block")
                    and entry.get("source_sha256") == parity.digest(en)
                    and entry.get("target_sha256") == parity.digest(ja)
                    and entry.get("reason")
                )]
                rendered_reviews_used.update(matching)
                check(bool(matching), f"{label}: rendered code/output {number} differs without a matching explanation review")
        md = markdown_path.read_text()
        check(body.strip() in md, f"{label}: Markdown output does not contain the full Japanese body")
        content_text = "".join(page.body_text)
        check("Copyright 2000-2026 Willy Tarreau" in html_path.read_text(), f"{label}: upstream copyright missing")
        check("https://www.gnu.org/licenses/old-licenses/gpl-2.0.html" in html_path.read_text(), f"{label}: GPLv2 attribution missing")
        for alias in aliases(front):
            path = root / "ja" / alias.strip("/") / "index.html"
            check(path.is_file() and f"https://doc.pg.center{destination}" in path.read_text(), f"{label}: legacy alias {alias}")
        for link in page.links:
            href = link.get("href", "")
            parsed = urlsplit(href)
            if parsed.netloc and parsed.netloc != "doc.pg.center":
                continue
            path = parsed.path or destination
            if path.startswith("/ja/docs/haproxy/"):
                output = root / path.lstrip("/")
                if path.endswith("/"):
                    output /= "index.html"
                check(output.is_file(), f"{label}: missing internal destination {href}")
                if parsed.fragment and output.is_file() and output.suffix == ".html":
                    check(unquote(parsed.fragment) in load(output).ids, f"{label}: broken anchor {href}")
        for asset in page.assets:
            parsed = urlsplit(asset)
            if not parsed.netloc and parsed.path.startswith("/"):
                check((root / parsed.path.lstrip("/")).is_file(), f"{label}: missing asset {asset}")
        check(bool(page.search) and (root / page.search.lstrip("/")).is_file(), f"{label}: search index missing")
        if page.search and (root / page.search.lstrip("/")).is_file():
            entries = json.loads((root / page.search.lstrip("/")).read_text())
            check(any(item.get("ref") == destination for item in entries), f"{label}: missing from Japanese search index")
        report["pages"].append({"route": destination, "anchors": len(page.content_ids), "headings": len(page.headings), "rendered_code_blocks": len(page.pre), "body_characters": len(content_text)})

    for index, entry in enumerate(exceptions):
        if entry.get("check") == "rendered explanatory block" and index not in rendered_reviews_used:
            errors.append(f"unused/stale rendered review: {entry.get('path')}#{entry.get('section')}")

    navigation = root / "ja/navigation.json"
    if navigation.is_file():
        payload = json.loads(navigation.read_text())
        try:
            docs = next(p for p in payload["root"]["children"] if p["id"] == "/docs/")
            component = next(p for p in docs["children"] if p["id"] == "/docs/haproxy/")
            check([p["url"] for p in component["children"]] == ["https://doc.pg.center" + route(p, True) for p in reading], "navigation.json: missing or reordered Japanese reading pages")
        except (KeyError, StopIteration):
            errors.append("navigation.json: Japanese HAProxy root missing")
    else:
        errors.append("navigation.json missing")
    llms = root / "ja/docs/haproxy/llms-full.txt"
    if llms.is_file():
        bundle = llms.read_text()
        actual = re.findall(r"(?m)^Source: (.+)$", bundle)
        expected = ["https://doc.pg.center/ja/docs/haproxy/index.md"] + ["https://doc.pg.center" + route(p, True) + "index.md" for p in reading]
        check(actual == expected, "llms-full.txt: missing, duplicate or reordered Japanese page bodies")
        for source in sources:
            target = source.with_suffix(".ja.md")
            if target.is_file():
                _, body = parity.structure.split_front_matter(target.read_text())
                check(body.strip() in bundle, f"llms-full.txt: missing full Japanese body for {source.name}")
    else:
        errors.append("Japanese llms-full.txt missing")
    printed = root / "ja/_print/docs/haproxy/index.html"
    if printed.is_file():
        text = printed.read_text()
        for source in sources:
            target = source.with_suffix(".ja.md")
            if not target.is_file():
                continue
            front, _ = parity.structure.split_front_matter(target.read_text())
            title = parity.structure.front_value(front, "title")[0].strip('\"\'')
            check(title in text, f"print: missing title {title}")
        try:
            print_errors, print_pages = print_parity.check_print(root, sources, PROJECT / "content", locale="ja", component="haproxy", compare_metadata=True)
            errors.extend(print_errors)
            report["print_pages"] = print_pages
        except (OSError, ValueError) as exc:
            errors.append(f"print: {exc}")
    else:
        errors.append("Japanese print output missing")
    for name in ("LICENSE", "GPL-2.0"):
        license_file = root / "third_party/haproxy" / name
        check(license_file.is_file() and license_file.read_bytes() == (PROJECT / "sources/haproxy/upstream" / name).read_bytes(), f"shared HAProxy {name} missing or changed")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    for error in errors:
        print(error)
    if errors:
        print(f"Japanese HAProxy rendered check failed: {len(errors)} errors.")
        return 1
    print(f"Japanese HAProxy rendered check passed: {len(sources)} complete routes, navigation, aliases, search, Markdown, print, LLMS, attribution and assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
