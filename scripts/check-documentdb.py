#!/usr/bin/env python3
"""Validate the paired DocumentDB edition and its upstream migration inventory.

Checks protected examples, links, heading aliases, native block structure, and
translation freshness. These structural checks do not certify semantic quality.
"""

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content/documentdb"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_page(path):
    text = path.read_text()
    if not text.startswith("---\n") or "\n---\n" not in text:
        raise ValueError(f"Invalid front matter: {path}")
    return text[4:].split("\n---\n", 1)


def pieces(body):
    """Fences in normal prose, nested callouts, and indented list items."""
    fence, pending = None, []
    for line in body.splitlines(keepends=True):
        bare = re.sub(r"^(?:[ \t]*>[ \t]?)*", "", line).lstrip()
        marker = re.match(r"(`{3,}|~{3,})", bare)
        if fence is None and marker:
            yield False, "".join(pending)
            pending, fence = [line], marker[1]
        elif fence and re.fullmatch(re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", bare):
            pending.append(line)
            yield True, "".join(pending)
            pending, fence = [], None
        else:
            pending.append(line)
    if fence:
        raise ValueError("Unclosed code fence")
    yield False, "".join(pending)


def structure(body):
    parts = list(pieces(body))
    prose = "".join(part for code, part in parts if not code)
    # Multisets allow Chinese word order without silently dropping a literal.
    inline = Counter(re.findall(r"(`+)([^`\n]+)\1", prose))
    links = Counter(re.findall(r"\]\(([^\s)]+)", prose))
    html_ids = re.findall(r'<span id="([^"]+)"></span>', prose)
    headings = re.findall(r"^\s*(#{1,6})\s+.*?\{#([^}]+)\}", prose, re.M)
    all_headings = re.findall(r"^\s*#{1,6}\s+.+", prose, re.M)
    if len(headings) != len(all_headings):
        raise ValueError("A heading lacks an explicit stable ID")
    table_rows = [len(re.findall(r"(?<!\\)\|", line)) for line in prose.splitlines()
                  if line.lstrip().startswith("|")]
    attrs = Counter(re.findall(r"\{\.[^}]+\}", prose))
    callouts = Counter(re.findall(r"\[!([A-Z]+)\]", prose))
    return {
        "code blocks": [part for code, part in parts if code],
        "inline literals": inline,
        "links": links,
        "heading IDs": headings,
        "heading aliases": html_ids,
        "table row widths": table_rows,
        "native block attributes": attrs,
        "callout types": callouts,
    }


def main():
    manifest = json.loads((ROOT / "data/imports/documentdb.json").read_text())
    records = manifest["pages"]
    errors = []
    sources = {p for p in CONTENT.rglob("*.md") if not p.name.endswith(".zh.md")}
    targets = {ROOT / r["target"] for r in records}
    if len(targets) != len(records) or targets != sources:
        errors.append("DocumentDB provenance must cover every English page exactly once")
    if len(records) != manifest.get("english_pages"):
        errors.append("DocumentDB page count differs from the recorded migration scope")
    if manifest.get("chinese_pages") != len(records):
        errors.append("DocumentDB Chinese coverage differs from the English migration scope")
    notes_file = ROOT / "data/imports/documentdb-notes.json"
    notes = json.loads(notes_file.read_text())["pages"]
    if (manifest.get("editorial_notes") != notes_file.relative_to(ROOT).as_posix()
            or manifest.get("editorial_notes_sha256") != digest(notes_file)):
        errors.append("DocumentDB editorial note provenance is stale")
    for record in records:
        en = ROOT / record["target"]
        zh = en.with_suffix(".zh.md")
        if not zh.exists():
            errors.append(f"Missing Chinese peer: {zh.relative_to(ROOT)}")
            continue
        if record.get("target_sha256") != digest(en):
            errors.append(f"English provenance hash is stale: {en.relative_to(ROOT)}")
        translation = record.get("translation", {})
        if (translation.get("target") != zh.relative_to(ROOT).as_posix()
                or translation.get("sha256") != digest(zh)
                or translation.get("source_sha256") != digest(en)
                or translation.get("route") != "/zh" + record["route"]):
            errors.append(f"Chinese provenance hash is stale: {zh.relative_to(ROOT)}")
        try:
            ef, eb = split_page(en)
            zf, zb = split_page(zh)
            note = notes.get(en.relative_to(CONTENT).as_posix())
            if note:
                for body, language in ((eb, "en"), (zb, "zh")):
                    if note[language] not in body:
                        errors.append(f"{en.relative_to(ROOT)}: missing {language} editorial note")
            left, right = structure(eb), structure(zb)
            for key in left:
                if left[key] != right[key]:
                    errors.append(f"{zh.relative_to(ROOT)}: {key} differ from English")
            if re.search(r"^translation_status:\s*(?:placeholder|machine-draft)\s*$", zf, re.M):
                errors.append(f"Unfinished translation: {zh.relative_to(ROOT)}")
            source_hash = re.search(r"^translation_source_sha256:\s*([a-f0-9]{64})$", zf, re.M)
            if not source_hash or source_hash[1] != digest(en):
                errors.append(f"Chinese source hash is stale: {zh.relative_to(ROOT)}")
            for field in ("upstream_link", "source_status"):
                pattern = rf"^{field}:\s*(.+)$"
                if re.findall(pattern, ef, re.M) != re.findall(pattern, zf, re.M):
                    errors.append(f"{zh.relative_to(ROOT)}: inconsistent {field}")
            prose = "".join(s for code, s in pieces(zb) if not code)
            if re.search(r"ZXQ\d+ZXQ", prose):
                errors.append(f"Unresolved translation token: {zh.relative_to(ROOT)}")
            if re.search(r"\]\(/(?:zh/)?docs/", prose):
                errors.append(f"Obsolete /docs/ route: {zh.relative_to(ROOT)}")
            if not re.search(r"[\u4e00-\u9fff]", prose):
                errors.append(f"Chinese prose is missing: {zh.relative_to(ROOT)}")
        except ValueError as exc:
            errors.append(f"{zh.relative_to(ROOT)}: {exc}")
    orphans = [p for p in CONTENT.rglob("*.zh.md") if p.with_name(p.name.replace(".zh.md", ".md")) not in sources]
    errors.extend(f"Orphan Chinese page: {p.relative_to(ROOT)}" for p in orphans)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(records)} DocumentDB English/Chinese pairs, provenance, protected examples, and stable anchors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
