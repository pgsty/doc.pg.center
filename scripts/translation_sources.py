"""Read the English snapshot an explicitly versioned translation was based on.

Keep snapshots in Git history instead of duplicating large manuals. Missing
history or a changed translation version is an error, never a skipped check.
"""

from __future__ import annotations

import json
import re
import subprocess
from functools import lru_cache
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=1)
def snapshots() -> dict:
    return json.loads((PROJECT / "data/translation-sources.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def historical_source(revision: str, relative: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError(f"translation source must use a full Git commit: {revision!r}")
    result = subprocess.run(
        ["git", "show", f"{revision}:{relative}"],
        cwd=PROJECT, capture_output=True, text=True, encoding="utf-8", check=False,
    )
    if result.returncode:
        raise ValueError(
            f"cannot read translation source {revision}:{relative}; "
            "fetch the repository history (CI uses fetch-depth: 0)"
        )
    return result.stdout


def read_source(source: Path, language: str, *, current: bool = False) -> tuple[str, str | None]:
    relative = source.relative_to(PROJECT)
    parts = relative.parts
    snapshot = (
        snapshots().get(parts[2])
        if not current and len(parts) >= 4 and parts[:2] == ("content", "docs")
        else None
    )
    if not snapshot or language not in snapshot["languages"]:
        return source.read_text(encoding="utf-8"), None

    component = parts[2]
    revision = snapshot["revision"]
    version = snapshot["version"]
    root = Path("content/docs") / component / "_index.md"
    translated_root = PROJECT / root.with_name(f"_index.{language}.md")
    version_pattern = rf"^title:.*(?<![\d.]){re.escape(version)}(?![\d.])"
    for label, document in (
        (str(translated_root.relative_to(PROJECT)), translated_root.read_text(encoding="utf-8")),
        (f"{revision}:{root}", historical_source(revision, root.as_posix())),
    ):
        front = document.split("\n---\n", 1)[0]
        if not re.search(version_pattern, front, re.MULTILINE):
            raise ValueError(f"{label}: expected snapshot version {version}; update translation-sources.json")
    return historical_source(revision, relative.as_posix()), revision


def describe_sources(language: str, *, current: bool = False) -> str:
    if current:
        return "current English sources only"
    pinned = [
        f"{component} {entry['version']} at {entry['revision'][:7]}"
        for component, entry in snapshots().items()
        if language in entry["languages"]
    ]
    return "current English sources; pinned snapshots: " + (", ".join(pinned) or "none")
