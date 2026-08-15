#!/usr/bin/env python3
"""Check source-level parity for bilingual component documentation."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ANCHOR_RE = re.compile(r'<a id="([^"]+)"></a>')
VERSION_RE = re.compile(r"^## Version (.+)$", re.MULTILINE)
PATRONICTL_RE = re.compile(r"^### (patronictl .+)$", re.MULTILINE)
METRIC_RE = re.compile(r"^# (?:HELP|TYPE) patroni_.+$", re.MULTILINE)


def compare(label: str, english: list[str], chinese: list[str], errors: list[str]) -> None:
    if english != chinese:
        errors.append(
            f"{label} differs between English and Chinese\n"
            f"  EN: {english}\n"
            f"  ZH: {chinese}"
        )


def main() -> int:
    project_dir = Path(__file__).resolve().parent.parent
    docs_dir = project_dir / "content" / "docs"
    errors: list[str] = []

    for chinese_path in sorted(docs_dir.rglob("*.zh.md")):
        english_path = chinese_path.with_name(chinese_path.name.replace(".zh.md", ".md"))
        if not english_path.is_file():
            errors.append(f"missing English pair for {chinese_path.relative_to(project_dir)}")
            continue
        english = english_path.read_text(encoding="utf-8")
        chinese = chinese_path.read_text(encoding="utf-8")
        compare(
            f"explicit anchors in {english_path.relative_to(project_dir)}",
            ANCHOR_RE.findall(english),
            ANCHOR_RE.findall(chinese),
            errors,
        )

    patroni_dir = docs_dir / "patroni"
    english_releases = (patroni_dir / "releases.md").read_text(encoding="utf-8")
    chinese_releases = (patroni_dir / "releases.zh.md").read_text(encoding="utf-8")
    compare(
        "Patroni release versions",
        VERSION_RE.findall(english_releases),
        VERSION_RE.findall(chinese_releases),
        errors,
    )

    english_ctl = (patroni_dir / "patronictl.md").read_text(encoding="utf-8")
    chinese_ctl = (patroni_dir / "patronictl.zh.md").read_text(encoding="utf-8")
    compare(
        "patronictl command sections",
        PATRONICTL_RE.findall(english_ctl),
        PATRONICTL_RE.findall(chinese_ctl),
        errors,
    )

    english_api = (patroni_dir / "rest_api.md").read_text(encoding="utf-8")
    chinese_api = (patroni_dir / "rest_api.zh.md").read_text(encoding="utf-8")
    compare(
        "Patroni Prometheus metric declarations",
        METRIC_RE.findall(english_api),
        METRIC_RE.findall(chinese_api),
        errors,
    )

    if errors:
        print("Bilingual source validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    pair_count = sum(1 for _ in docs_dir.rglob("*.zh.md"))
    print(f"Validated source parity for {pair_count} bilingual documentation pairs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
