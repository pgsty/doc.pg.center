#!/usr/bin/env python3
"""Check language coverage and upstream attribution without historical review files."""

from pathlib import Path
import re
import sys

PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content"
LANGUAGES = ("en", "zh", "fr", "ja", "de", "ru", "ar", "es")
COMPONENTS = ("patroni", "pgbackrest", "pgbouncer", "pgbadger", "haproxy", "etcd", "cloudberry")
# Collections that are not yet published in every language. Their Chinese pages
# may be title-only placeholders marked `translation_status: placeholder`.
COMPONENT_LANGUAGES = {"cloudberry": ("en", "zh")}
PLACEHOLDER = re.compile(r'^translation_status: "?placeholder"?$', re.M)


def languages_for(path: Path) -> tuple[str, ...]:
    relative = path.relative_to(CONTENT).parts
    if len(relative) > 1 and relative[0] in COMPONENT_LANGUAGES:
        return COMPONENT_LANGUAGES[relative[0]]
    return LANGUAGES


def english_route(source: Path) -> str:
    relative = source.relative_to(CONTENT)
    stem = relative.name.removesuffix(".md")
    route = relative.parent if stem in ("_index", "index") else relative.with_name(stem)
    return "/" + route.as_posix().strip("/") + "/"


def english_path(path: Path) -> Path:
    for language in LANGUAGES[1:]:
        suffix = f".{language}.md"
        if path.name.endswith(suffix):
            return path.with_name(path.name.removesuffix(suffix) + ".md")
    return path


def main() -> int:
    errors = []
    pages = {path: path.read_text(encoding="utf-8") for path in CONTENT.rglob("*.md")}
    sources = [path for path in pages if english_path(path) == path]
    registry = (PROJECT / "data/upstreams.yaml").read_text(encoding="utf-8")
    if (CONTENT / "docs").exists():
        errors.append("Documentation must live in top-level component sections, not content/docs")
    for component in COMPONENTS:
        if not re.search(rf"^{component}:$", registry, re.M):
            errors.append(f"Missing upstream registry entry: {component}")
        for language in COMPONENT_LANGUAGES.get(component, LANGUAGES):
            suffix = ".md" if language == "en" else f".{language}.md"
            index = CONTENT / component / ("_index" + suffix)
            if f"upstream_source: {component}" not in pages.get(index, ""):
                errors.append(f"Missing component attribution: {index.relative_to(PROJECT)}")
            front = pages.get(index, "").split("\n---\n", 1)[0]
            if not re.search(r"^type: docs$", front, re.M):
                errors.append(f"Missing docs layout: {index.relative_to(PROJECT)}")
            if not re.search(r"^sidebar_root_for: self$", front, re.M):
                errors.append(f"Missing independent sidebar: {index.relative_to(PROJECT)}")

    for path, text in pages.items():
        source = english_path(path)
        if source not in pages:
            errors.append(f"Missing English source for {path.relative_to(PROJECT)}")
        if not text.startswith("---\n") or "\n---\n" not in text:
            errors.append(f"Missing YAML front matter: {path.relative_to(PROJECT)}")
        relative = path.relative_to(CONTENT).parts
        if len(relative) < 2:
            continue
        if relative[0] not in COMPONENTS:
            errors.append(f"Unregistered documentation component: {relative[0]}")
        front = text.split("\n---\n", 1)[0]
        link = re.search(r"^upstream_link:\s*(.+)$", front, re.M)
        original = re.search(r"^upstream_link:\s*(.+)$", pages.get(source, "").split("\n---\n", 1)[0], re.M)
        if not link or not original or link[1] != original[1]:
            errors.append(f"Missing or inconsistent upstream link: {path.relative_to(PROJECT)}")
        if PLACEHOLDER.search(front):
            if source == path:
                errors.append(f"English source marked as a placeholder: {path.relative_to(PROJECT)}")
            elif f'<a href="{english_route(source)}" hreflang="en" lang="en">' not in text:
                errors.append(f"Placeholder does not link its English page: {path.relative_to(PROJECT)}")

    for source in sources:
        expected = languages_for(source)
        for language in LANGUAGES[1:]:
            translated = source.with_suffix(f".{language}.md")
            if language in expected and translated not in pages:
                errors.append(f"Missing translation: {translated.relative_to(PROJECT)}")
            if language not in expected and translated in pages:
                errors.append(f"Unregistered language edition: {translated.relative_to(PROJECT)}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    published = sum(not path.name.startswith("_div_") for path in pages)
    placeholders = sum(bool(PLACEHOLDER.search(text.split("\n---\n", 1)[0])) for text in pages.values())
    print(f"Validated {published} publishable source pages ({placeholders} translation placeholders) "
          f"across {len(COMPONENTS)} documentation collections.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
