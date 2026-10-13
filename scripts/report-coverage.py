#!/usr/bin/env python3
"""Report localized page availability relative to English content routes."""

from __future__ import annotations

from pathlib import Path
import sys


CONTENT = Path(__file__).resolve().parent.parent / "content"
LANGUAGES = ("en", "zh", "fr", "ja", "de", "ru")
COMPONENTS = {
    "patroni": "Patroni",
    "pgbackrest": "pgBackRest",
    "pgbouncer": "PgBouncer",
    "pgbadger": "pgBadger",
    "haproxy": "HAProxy",
    "etcd": "etcd",
}


def english_path(path: Path) -> Path:
    """Map a localized file to its default-language source path."""
    for language in LANGUAGES[1:]:
        if path.name.endswith(f".{language}.md"):
            return path.with_name(path.name.removesuffix(f".{language}.md") + ".md")
    return path


def counts(sources: list[Path]) -> list[int]:
    return [
        sum(
            (source if language == "en" else source.with_suffix(f".{language}.md")).is_file()
            for source in sources
        )
        for language in LANGUAGES
    ]


def row(label: str, sources: list[Path]) -> str:
    total = len(sources)
    cells = []
    for count in counts(sources):
        percent = f"{100 * count / total:.1f}".removesuffix(".0") if total else "0"
        cells.append(f"{count} ({percent}%)")
    return "| " + " | ".join([label, *cells]) + " |"


def main() -> int:
    # _index files are published directory pages; _div files only label sidebars.
    files = sorted(path for path in CONTENT.rglob("*.md") if not path.name.startswith("_div_"))
    orphans = [path for path in files if not english_path(path).is_file()]
    if orphans:
        for path in orphans:
            print(f"Missing English source: {path.relative_to(CONTENT)}", file=sys.stderr)
        return 1

    sources = [path for path in files if english_path(path) == path]
    groups = {
        name: [path for path in sources if path.is_relative_to(CONTENT / "docs" / name)]
        for name in COMPONENTS
    }
    component_sources = [path for group in groups.values() for path in group]
    component_set = set(component_sources)
    site_sources = [path for path in sources if path not in component_set]

    print("| Collection | EN | ZH | FR | JA | DE | RU |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, label in COMPONENTS.items():
        print(row(label, groups[name]))
    print(row("**Component total**", component_sources))
    print(row("Site pages", site_sources))
    print(row("**All publishable pages**", sources))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
