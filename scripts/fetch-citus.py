#!/usr/bin/env python3
"""Download the bilingual Citus 14 source inventory outside the repository.

Usage: python3 scripts/fetch-citus.py /path/outside/repository/citus-snapshot
Existing files are retained, so a partial download can be resumed. Use a new
directory for a new snapshot. Import with scripts/import-citus.py only once;
subsequent changes belong in the maintained Markdown, after reviewing the diff.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
VIEW = "citus-14"


def download(url: str, destination: Path) -> bytes:
    if destination.is_file():
        return destination.read_bytes()
    destination.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=45) as response:
                data = response.read()
            if not data:
                raise ValueError(f"Empty response: {url}")
            destination.write_bytes(data)
            return data
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)
    raise AssertionError("unreachable")


def slugs_from_toc(toc: dict) -> set[str]:
    slugs = {"index"}

    def walk(items):
        for item in items:
            if item.get("monikers") and VIEW not in item["monikers"]:
                continue
            href = item.get("href", "")
            if href and href != "./":
                if ":" in href or href.startswith("/") or ".." in href.split("/"):
                    raise ValueError(f"Unexpected source route: {href}")
                slugs.add(href)
            walk(item.get("children", []))

    walk(toc["items"])
    return slugs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    destination = args.destination.expanduser().resolve()
    if destination == ROOT or ROOT in destination.parents:
        parser.error("Source downloads must be outside the repository")
    inventories = {}
    for language, locale in (("en", "en-us"), ("zh", "zh-cn")):
        data = download(f"https://learn.microsoft.com/{locale}/postgresql/citus/toc.json?view={VIEW}",
                        destination / f"toc-{language}.json")
        inventories[language] = slugs_from_toc(json.loads(data))
    if inventories["en"] != inventories["zh"]:
        raise SystemExit("English and Chinese source inventories differ; review before import")

    def fetch(task):
        language, slug, kind = task
        locale = "en-us" if language == "en" else "zh-cn"
        url = f"https://learn.microsoft.com/{locale}/postgresql/citus/" + ("" if slug == "index" else slug) + f"?view={VIEW}"
        if kind == "md":
            url += "&accept=text/markdown"
        target = destination / ("markdown" if kind == "md" else "html") / language / (slug.replace("/", "__") + "." + kind)
        data = download(url, target)
        return dict(language=language, slug=slug, kind=kind, url=url,
                    file=str(target.relative_to(destination)), bytes=len(data),
                    sha256=hashlib.sha256(data).hexdigest())

    tasks = [(language, slug, kind) for language in ("en", "zh")
             for slug in sorted(inventories[language]) for kind in ("html", "md")]
    records = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(fetch, task) for task in tasks]
        for future in as_completed(futures):
            records.append(future.result())
    (destination / "downloads.json").write_text(json.dumps(
        sorted(records, key=lambda item: (item["slug"], item["language"], item["kind"])),
        ensure_ascii=False, indent=2) + "\n")
    print(f"Retained {len(records)} snapshots for {len(inventories['en'])} source pages per language in {destination}")


if __name__ == "__main__":
    main()
