#!/usr/bin/env python3
"""Generate verbatim pgBadger reference pages from the pinned source snapshot."""

from __future__ import annotations

import re
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent
SOURCE = PROJECT / "sources" / "pgbadger" / "upstream"
CONTENT = PROJECT / "content" / "docs" / "pgbadger"
COMMIT = "a1ad95a035a0c2d246fe632eb1c361d4bde0ddae"
SOURCE_URL = f"https://github.com/darold/pgbadger/tree/{COMMIT}"


def normalize_source_markdown(text: str) -> str:
    return (
        text.replace(r"\_", "_")
        .replace(r"\[", "[")
        .replace(r"\]", "]")
        .replace(r"\--", "--")
        .strip()
    )


def fence_indented_blocks(text: str) -> str:
    """Turn POD-generated four-space blocks into explicit text fences."""
    lines = text.splitlines()
    output: list[str] = []
    block: list[str] = []

    def flush() -> None:
        nonlocal block
        while block and not block[-1]:
            block.pop()
        if block:
            output.extend(["```text", *block, "```"])
        block = []

    for index, line in enumerate(lines):
        next_indented = index + 1 < len(lines) and lines[index + 1].startswith("    ")
        if line.startswith("    "):
            block.append(line[4:])
        elif block and not line and next_indented:
            block.append("")
        else:
            flush()
            output.append(line)
    flush()
    return "\n".join(output).strip()


def read_readme_section(name: str) -> str:
    readme = (SOURCE / "README.md").read_text(encoding="utf-8")
    match = re.search(
        rf"^### {re.escape(name)}\s*$\n(.*?)(?=^### [A-Z][A-Z ]+\s*$|\Z)",
        readme,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise RuntimeError(f"README section not found: {name}")
    return fence_indented_blocks(normalize_source_markdown(match.group(1)))


def write_command_reference() -> None:
    body = read_readme_section("SYNOPSIS")
    common = f"""
> Source: [pgBadger `README.md`]({SOURCE_URL}/README.md) at commit [`{COMMIT[:7]}`](https://github.com/darold/pgbadger/commit/{COMMIT}).

## Usage and options {{#usage-and-options}}

{body}
""".strip()

    english = f"""---
title: "Command-Line Reference"
linkTitle: "Command Line"
weight: 30
description: "Complete pgBadger command syntax, options, remote input, return codes, and examples"
icon: fa-solid fa-terminal
module: [PGBADGER]
categories: [Reference]
---

This page preserves the command reference generated from the pinned upstream source. Option names and help text remain verbatim so they can be compared directly with `pgbadger --help`.

{common}
"""

    chinese = f"""---
title: "命令行参考"
linkTitle: "命令行"
weight: 30
description: "完整的 pgBadger 命令语法、选项、远程输入、返回码与示例"
icon: fa-solid fa-terminal
module: [PGBADGER]
categories: [参考]
---

本页保留固定上游源码生成的完整命令参考。为了能与 `pgbadger --help` 逐项核对，参数名、帮助文字和命令示例均保留英文原文。

{common.replace('## Usage and options {#usage-and-options}', '## 用法与选项 {#usage-and-options}')}
"""

    CONTENT.mkdir(parents=True, exist_ok=True)
    (CONTENT / "command-line.md").write_text(english, encoding="utf-8")
    (CONTENT / "command-line.zh.md").write_text(chinese, encoding="utf-8")


def changelog_entries() -> dict[int, list[tuple[str, str, str]]]:
    changelog = (SOURCE / "ChangeLog").read_text(encoding="utf-8")
    starts = list(
        re.finditer(
            r"^(\d{4}-\d{2}-\d{2}) - v(\d+\.\d+)\s*$",
            changelog,
            flags=re.MULTILINE,
        )
    )
    result: dict[int, list[tuple[str, str, str]]] = {major: [] for major in range(9, 14)}
    for index, match in enumerate(starts):
        version = match.group(2)
        major = int(version.split(".", 1)[0])
        if major not in result:
            continue
        end = starts[index + 1].start() if index + 1 < len(starts) else len(changelog)
        body = normalize_source_markdown(changelog[match.end() : end])
        result[major].append((version, match.group(1), body))
    return result


def write_release_pages() -> None:
    release_dir = CONTENT / "releases"
    release_dir.mkdir(parents=True, exist_ok=True)
    entries = changelog_entries()
    weights = {13: 10, 12: 20, 11: 30, 10: 40, 9: 50}

    for major in range(13, 8, -1):
        sections: list[str] = []
        for version, date, body in entries[major]:
            sections.append(f"## v{version} · {date} {{#v{version.replace('.', '-')}}}\n\n{body}")
        release_text = "\n\n".join(sections)
        common = f"""
> Source: [upstream `ChangeLog`]({SOURCE_URL}/ChangeLog) at commit [`{COMMIT[:7]}`](https://github.com/darold/pgbadger/commit/{COMMIT}).

{release_text}
""".strip()

        english = f"""---
title: "pgBadger {major}.x Release Notes"
linkTitle: "{major}.x"
weight: {weights[major]}
description: "Complete upstream release notes for the pgBadger {major}.x series"
icon: fa-solid fa-code-branch
module: [PGBADGER]
categories: [Release]
---

These entries preserve the complete upstream change record for pgBadger {major}.x, newest first.

{common}
"""

        chinese = f"""---
title: "pgBadger {major}.x 版本记录"
linkTitle: "{major}.x"
weight: {weights[major]}
description: "pgBadger {major}.x 系列的完整上游版本记录"
icon: fa-solid fa-code-branch
module: [PGBADGER]
categories: [版本发布]
---

本页按从新到旧的顺序保留 pgBadger {major}.x 的完整上游变更记录。为确保版本、参数、提交者致谢和兼容性描述不被转述改变，正文保留英文原文。

{common}
"""

        (release_dir / f"{major}.md").write_text(english, encoding="utf-8")
        (release_dir / f"{major}.zh.md").write_text(chinese, encoding="utf-8")


def main() -> None:
    write_command_reference()
    write_release_pages()
    print("Generated pgBadger command reference and release-history pages.")


if __name__ == "__main__":
    main()
