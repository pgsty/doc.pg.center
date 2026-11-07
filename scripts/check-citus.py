#!/usr/bin/env python3
"""Check Citus import coverage, version selection, examples, and retained rights."""
from __future__ import annotations

import hashlib
import json
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def code_blocks(text: str) -> list[str]:
    """Include examples in callouts and indented lists as well as normal fences."""
    blocks, lines, active = [], [], None
    for line in text.splitlines():
        if active:
            prefix, fence = active
            if re.fullmatch(re.escape(prefix + fence) + r"\s*", line):
                blocks.append("\n".join(lines).rstrip("\n") + "\n")
                lines, active = [], None
            else:
                lines.append(line[len(prefix):] if line.startswith(prefix) else line)
        else:
            match = re.match(r"^([ \t]*(?:> ?)*)(`{3,}|~{3,})[^`]*$", line)
            if match:
                active = match[1], match[2]
    assert active is None, "Unclosed code block"
    return blocks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--public', type=Path, help='Also validate rendered exports and notices')
    args = parser.parse_args()
    manifest = json.loads((ROOT / "data/imports/citus.json").read_text())
    entries = manifest["pages"]
    assert len(entries) == 118, "Review upstream inventory changes explicitly"
    imported, english_codes = set(), 0
    for entry in entries:
        target = ROOT / entry["target"]
        assert target not in imported, f"Duplicate import target: {target}"
        imported.add(target)
        text = target.read_text()
        front, body = text[4:].split("\n---\n", 1)
        assert ":::moniker" not in body, f"Unresolved version directive: {target}"
        ids = re.findall(r"(?m)^#{2,6} .*?\{#([^}]+)\}\s*$", body)
        assert ids == entry["heading_ids"], f"Source anchors changed: {target}"
        assert len(ids) == len(set(ids)), f"Duplicate heading anchors: {target}"
        hashes = [digest(code.encode()) for code in code_blocks(body)]
        assert hashes == entry["code_sha256"], f"Source examples changed: {target}"
        if entry["language"] == "en":
            english_codes += len(hashes)
        if entry["status"] == "machine-draft":
            assert "translation_status: machine-draft" in front and "机器译稿" in body, target
        elif entry["language"] == "zh":
            assert "translation_status: translated" in front, target
            assert "机器译稿，待英文校订" not in body, target
            basis = entry["translation_basis"]
            assert digest((ROOT / basis["target"]).read_bytes()) == basis["sha256"], f"English changed since translation review: {target}"
        assert digest(target.read_bytes()) == entry["maintained_sha256"], f"Refresh maintained content provenance: {target}"
        if "source_pre_code_sha256" in entry:
            recovered = entry["recovered_paragraph_output_sha256"]
            assert [h for h in hashes if h not in recovered] == entry["source_pre_code_sha256"], target
            assert all(h in hashes for h in recovered), target
        assert re.fullmatch(r"[a-f0-9]{40}", entry["source_commit"]), target
        for key in ("source_html_sha256", "source_markdown_sha256"):
            assert re.fullmatch(r"[a-f0-9]{64}", entry[key]), target

    for asset in manifest["assets"] + manifest["license_files"]:
        target = ROOT / asset["target"]
        assert digest(target.read_bytes()) == asset["sha256"], f"Retained asset changed: {target}"
    for suffix in ("", ".zh"):
        for slug in ("single-node-debian", "single-node-rhel"):
            text = (ROOT / f"content/citus/installation/{slug}{suffix}.md").read_text()
            assert re.search(r"^## 1\. .*PostgreSQL 18", text, re.M), slug
    pages = list((ROOT / 'content/citus').rglob('*.md'))
    assert len(pages) == 134, 'Expected 67 maintained pages per language'
    if args.public:
        from collection_registry import source_route
        for source in pages:
            route = source_route(source)
            exported = (args.public / route.strip('/') / 'index.md').read_text()
            for required in ('Microsoft', 'CC BY 4.0', 'learn.microsoft.com', '/citus/attribution/'):
                assert required in exported, f'Missing export credit {required}: {route}'
        for prefix in ('', 'zh/'):
            bundle = (args.public / prefix / 'citus/llms-full.txt').read_text()
            assert bundle.count('\nSource: https://doc.pg.center/') == 67, f'Incomplete Citus export: {prefix}'
            assert bundle.count('Microsoft') >= 67, f'Missing bundle notices: {prefix}'
            printed = (args.public / prefix / '_print/citus/index.html').read_text()
            assert 'Microsoft' in printed and 'CC BY 4.0' in printed, f'Missing print credits: {prefix}'
    print(f"Validated Citus: 59 source pages per language, {english_codes} exact examples per edition, "
          f"{len(manifest['assets'])} images, source anchors, version selection, and retained licenses.")


if __name__ == "__main__":
    main()
