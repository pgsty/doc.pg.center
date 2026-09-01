#!/usr/bin/env python3
"""Translate the authoritative English Markdown tree into German.

The mature Chinese translator already contains the repository-specific Markdown
protector, atomic cache, chunking, heading-anchor alignment, and numeric-fidelity
checks. This driver reuses those language-neutral parts while supplying German
prompts, terminology, routes, filenames, and validation.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content"
STYLE_GUIDE = PROJECT / "TRANSLATION_DE.md"
HELPER_PATH = PROJECT / "scripts" / "translate-component-docs.py"
CHECKER_PATH = PROJECT / "scripts" / "check-german-parity.py"
DEFAULT_CACHE = PROJECT / ".hugo_cache" / "translation-cache-de.json"
DEFAULT_MODEL = "qwen3:30b-a3b-instruct-2507-q4_K_M"
COMPONENTS = ("patroni", "pgbackrest", "pgbouncer", "pgbadger", "haproxy", "etcd")
LOCALIZED_SUFFIX_RE = re.compile(r"\.[a-z]{2}(?:-[a-z0-9]+)?\.md$", re.IGNORECASE)
PROTECTED_NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    r"[vV]?\d+(?:\.\d+)+(?:[-+][A-Za-z0-9.-]+)?"
    r"|\d{4}-\d{2}-\d{2}"
    r"|\d+(?:\.\d+)?[kKmMgGtTpP](?:i?[bB])?"
    r"|\d{4,}"
    r")(?![A-Za-z0-9_])"
)
TRANSLATABLE_META = {"title", "linkTitle", "description"}
CATEGORY_MAP = {
    "Concept": "Konzept",
    "Task": "Aufgabe",
    "Reference": "Referenz",
    "Tutorial": "Tutorial",
}

INDENTED_LITERAL_RANGES: dict[str, tuple[tuple[int, int], ...]] = {
    "haproxy/acls-and-samples.md": ((1722, 1727),),
    "haproxy/configuration-logging.md": (
        (1825, 1827), (1832, 1834), (1850, 1852), (1861, 1862),
        (1868, 1869), (1876, 1877), (1882, 1884),
    ),
    "haproxy/fastcgi.md": ((271, 272), (280, 282)),
    "haproxy/global.md": ((1546, 1546),),
    "haproxy/other-sections.md": ((1520, 1528),),
    "haproxy/proxies.md": (
        (3264, 3265), (3747, 3784), (7113, 7117), (7388, 7392),
        (9246, 9259), (9417, 9433), (9559, 9574), (10877, 10878),
        (11517, 11518), (12497, 12498),
    ),
    "haproxy/security.md": ((123, 127),),
    "haproxy/statistics-and-monitoring.md": ((2209, 2213),),
    "haproxy/stick-tables-and-peers.md": ((580, 581),),
    "patroni/citus.md": (
        (57, 68), (72, 87), (97, 140),
        (144, 157), (171, 184), (194, 199),
    ),
    "patroni/config/yaml.md": ((126, 134),),
    "patroni/readme.md": ((54, 56), (64, 64), (66, 66)),
}


def load_base_translator():
    spec = importlib.util.spec_from_file_location("pgsql_translate_component_docs", HELPER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load translation helper: {HELPER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


base = load_base_translator()
shared_normalize_model_output = base.normalize_model_output
shared_translate_front_matter = base.translate_front_matter
shared_translate_text = base.translate_text


def load_german_checker():
    spec = importlib.util.spec_from_file_location("pgsql_check_german_parity", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load German parity checker: {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


german_checker = load_german_checker()


def glossary_entries() -> list[tuple[str, str]]:
    guide = STYLE_GUIDE.read_text(encoding="utf-8")
    try:
        table = guide.split("## Required terminology", 1)[1].split("\n## ", 1)[0]
    except IndexError as exc:
        raise RuntimeError("TRANSLATION_DE.md has no required terminology section") from exc
    entries: list[tuple[str, str]] = []
    for line in table.splitlines():
        if not line.startswith("|") or line.startswith("| ---") or "English" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 2:
            entries.append((cells[0], cells[1]))
    return entries


GLOSSARY = glossary_entries()


def selected_glossary(source: str) -> str:
    source_lower = re.sub(r"\s+", " ", source.lower())
    selected: list[str] = []
    for english, german in GLOSSARY:
        candidates = [
            re.sub(r"\s*\([^)]*\)\s*", "", candidate).strip()
            for candidate in english.lower().split("/")
        ]
        if any(candidate and candidate in source_lower for candidate in candidates):
            selected.append(f"{english} => {german}")
    return "; ".join(selected)


def german_system_prompt(component: str, source: str, mode: str) -> str:
    glossary = selected_glossary(source)
    if mode == "scalar":
        return f"""Du bist ein erfahrener deutscher Redakteur für technische Dokumentation. Übersetze die folgende kurze Metadatenphrase aus der offiziellen {component}-Dokumentation vollständig, präzise, idiomatisch und knapp ins Deutsche.
Gib ausschließlich die deutsche Phrase aus: keinen YAML-Schlüssel, keine Anführungszeichen, keine Einleitung und keine Erklärung. Produktnamen, Kapitelnummern, Befehle, Konfigurationsschlüssel, API-Namen, Abkürzungen, Versionen, Zahlen und Platzhalter müssen exakt erhalten bleiben. Schreibe Zahlen weiterhin als Ziffern.
Verbindliche Terminologie: {glossary or 'siehe TRANSLATION_DE.md'}"""
    return f"""Du bist ein erfahrener deutscher Redakteur für technische Dokumentation und übersetzt das offizielle {component}-Handbuch aus dem Englischen.

Anforderungen:
1. Übersetze sämtliche natürliche Sprache vollständig in präzises, idiomatisches, professionelles Deutsch. Nichts auslassen, zusammenfassen, erklären oder hinzufügen.
2. Markdown-Struktur, Zeilen- und Listenebenen, Tabellenform, Hervorhebungen und Blockquotes exakt erhalten. Jeder geschützte Platzhalter muss unverändert und genau einmal erscheinen. Platzhalter samt zugehörigem Linktext dürfen als Einheit verschoben werden, wenn die deutsche Wortstellung dies erfordert.
3. Befehle, Konfigurationsschlüssel, API/RPC-/Nachrichten-/Feldnamen, Umgebungsvariablen, Dateinamen, Pfade, Metriken, Protokolle, Produktnamen und Abkürzungen unverändert lassen.
4. Natürliche Sprache in Überschriften und Linktexten übersetzen; Kapitelnummern unverändert lassen.
5. Normative Stärke exakt bewahren: must=muss, should=sollte, may/can=kann. Negationen, Bedingungen, Standardwerte, veraltete Funktionen, Warnungen, Reihenfolge, Zahlen, Versionen und Einheiten niemals verändern.
6. Alle Zahlen als dieselben Ziffern wie im Ausgangstext schreiben; Zahlen niemals ausschreiben oder neu formatieren.
7. Nur das übersetzte Fragment ausgeben: keine Anführungszeichen, Codeblöcke, Einleitung oder Erläuterung hinzufügen.
8. Natürliches, kompaktes Standarddeutsch für erfahrene Linux-, Netzwerk-, Datenbank- und Distributed-Systems-Anwender verwenden. Anweisungen einheitlich als formelle Imperative mit „Sie“ oder unpersönlich formulieren; niemals „du“ verwenden.

Verbindliche Terminologie: {glossary or 'siehe TRANSLATION_DE.md'}"""


def german_post_ollama(model: str, prompt: str, *, timeout: int = 600) -> str:
    if model.startswith("translategemma"):
        marker = "\n\n待翻译片段：\n"
        if marker not in prompt:
            raise RuntimeError("cannot locate protected source fragment for TranslateGemma")
        source_fragment = prompt.rsplit(marker, 1)[1]
        prompt = (
            "You are a professional English (en) to German (de-DE) translator. "
            "Your goal is to accurately convey the meaning and nuances of the original "
            "English text while adhering to German grammar, vocabulary, and cultural "
            "sensitivities.\nProduce only the German translation, without any additional "
            "explanations or commentary. Please translate the following English text "
            "into German:\n\n\n"
            + source_fragment
        )
    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "keep_alive": "30m",
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "repeat_penalty": 1.0,
                "num_ctx": 32768,
                "num_predict": 8192,
            },
        }
    ).encode("utf-8")
    if model.startswith("translategemma"):
        endpoint = os.environ.get(
            "GERMAN_OLLAMA_URL", "http://127.0.0.1:11434/api/generate"
        )
    elif model == DEFAULT_MODEL:
        endpoint = os.environ.get(
            "OLLAMA_30B_URL",
            os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate"),
        )
    elif model == os.environ.get("GERMAN_FALLBACK_MODEL"):
        endpoint = os.environ.get(
            "GERMAN_FALLBACK_OLLAMA_URL",
            os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate"),
        )
    else:
        endpoint = os.environ.get(
            "OLLAMA_URL", "http://127.0.0.1:11434/api/generate"
        )
    request = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc
    translated = result.get("response")
    if not isinstance(translated, str) or not translated.strip():
        raise RuntimeError(f"Ollama returned no translation: {result}")
    return translated


def normalize_german_output(value: str) -> str:
    value = value.replace("\u00a0", " ")
    value = re.sub(r"(!?)\[\s+(?=[^]\n]+\])", r"\1[", value)
    value = re.sub(r"\s+\](?=(?:\(|\[))", "]", value)
    value = re.sub(r"(?<!`)``([^`\n]+)``(?!`)", r"`\1`", value)

    def move_heading_anchor(match: re.Match[str]) -> str:
        title = f"{match.group('before')} {match.group('after')}".strip()
        title = re.sub(r"\s{2,}", " ", title)
        return f"{match.group('prefix')}{title} {match.group('anchor')}"

    value = re.sub(
        r"(?m)^(?P<prefix>\s*#{1,6}\s+)(?P<before>.*?)\s*"
        r"(?P<anchor>\{#[A-Za-z0-9_.:-]+\})(?P<after>.*?)\s*$",
        move_heading_anchor,
        value,
    )
    value = re.sub(r"[ \t]+\n", "\n", value)
    return value


def translate_german_text(
    source: str,
    *,
    component: str,
    model: str,
    cache,
    mode: str = "markdown",
    retries: int = 4,
) -> str:
    fallback_model = os.environ.get("GERMAN_FALLBACK_MODEL", DEFAULT_MODEL)

    def translate_with_fallback() -> str:
        if (
            fallback_model != DEFAULT_MODEL
            and not os.environ.get("GERMAN_SKIP_30B_PROBE")
        ):
            try:
                return shared_translate_text(
                    source,
                    component=component,
                    model=DEFAULT_MODEL,
                    cache=cache,
                    mode=mode,
                    retries=1,
                )
            except RuntimeError:
                pass
        return shared_translate_text(
            source,
            component=component,
            model=fallback_model,
            cache=cache,
            mode=mode,
            retries=retries,
        )

    if not model.startswith("translategemma"):
        return shared_translate_text(
            source,
            component=component,
            model=model,
            cache=cache,
            mode=mode,
            retries=retries,
        )
    probe = GermanProtector()
    probe.protect(source)
    if len(probe.values) > 6:
        return translate_with_fallback()
    failure_key = base.hashlib.sha256(
        (f"german-primary-failure\0{base.CACHE_SCHEMA_VERSION}\0{model}\0{mode}\0" + source).encode(
            "utf-8"
        )
    ).hexdigest()
    if cache.get(failure_key) == "1":
        return translate_with_fallback()
    try:
        return shared_translate_text(
            source,
            component=component,
            model=model,
            cache=cache,
            mode=mode,
            retries=1,
        )
    except RuntimeError as exc:
        cache.put(failure_key, "1")
        print(
            f"TranslateGemma fragment fallback to {fallback_model}: {exc}",
            file=sys.stderr,
            flush=True,
        )
        return translate_with_fallback()


def normalize_german_model_output(source: str, translated: str) -> str:
    value = shared_normalize_model_output(source, translated)
    source_core = source.lstrip("\n")
    source_indent_match = re.match(r"^[ \t]+", source_core)
    if source_indent_match:
        leading_newlines = len(value) - len(value.lstrip("\n"))
        target_core = value[leading_newlines:]
        target_indent_match = re.match(r"^[ \t]*", target_core)
        target_indent = target_indent_match.group(0) if target_indent_match else ""
        source_indent = source_indent_match.group(0)
        if len(target_indent.expandtabs(4)) < len(source_indent.expandtabs(4)):
            value = (
                value[:leading_newlines]
                + source_indent
                + target_core[len(target_indent) :]
            )
    # Some models mirror the right bracket when placeholders appear as Markdown
    # link boundaries. The identifier itself is still unambiguous.
    value = re.sub(r"[⟦⟧]P(\d{4})[⟦⟧]", r"⟦P\1⟧", value)
    return re.sub(
        r"<x-([a-z]+)\s*/\s*>",
        lambda match: f'<x-{match.group(1).lower()}/>',
        value,
        flags=re.IGNORECASE,
    )


def translate_german_front_matter(
    front: str,
    *,
    component: str,
    scalar_model: str,
    fallback_model: str,
    cache,
) -> str:
    translated_front = shared_translate_front_matter(
        front,
        component=component,
        scalar_model=scalar_model,
        fallback_model=fallback_model,
        cache=cache,
    )
    block_re = re.compile(
        r"^(?P<key>title|linkTitle|description):\s*(?P<indicator>[>|][+-]?)\n"
        r"(?P<body>(?:[ \t]+.*(?:\n|$))*)",
        flags=re.MULTILINE,
    )
    for match in reversed(list(block_re.finditer(front))):
        body_lines = [line for line in match.group("body").splitlines() if line.strip()]
        if not body_lines:
            continue
        indent_match = re.match(r"^[ \t]+", body_lines[0])
        indent = indent_match.group(0) if indent_match else "  "
        source_value = " ".join(line.strip() for line in body_lines)
        translated_value = base.translate_scalar_preserving_prefix(
            source_value,
            component=component,
            model=scalar_model,
            cache=cache,
            fallback_model=fallback_model,
        )
        current_matches = list(block_re.finditer(translated_front))
        current = next(
            item
            for item in current_matches
            if item.group("key") == match.group("key")
            and item.group("indicator") == match.group("indicator")
        )
        replacement = (
            f'{match.group("key")}: {match.group("indicator")}\n'
            f"{indent}{translated_value}\n"
        )
        translated_front = (
            translated_front[: current.start()]
            + replacement
            + translated_front[current.end() :]
        )
    return translated_front.rstrip("\n")


def validate_german_fragment_structure(source: str, translated: str) -> None:
    """Reject structural rewrites and changes to explicitly written numbers.

    The Chinese helper contains extensive Han-specific number normalization.
    German naturally translates ``5 minutes`` to ``5 Minuten``, so this driver
    validates the numeric literal itself while allowing the surrounding unit
    word to be localized.
    """

    def table_signature(value: str) -> list[int]:
        return [
            len(re.findall(r"(?<!\\)\|", line))
            for line in value.splitlines()
            if line.lstrip().startswith("|")
        ]

    if table_signature(source) != table_signature(translated):
        raise ValueError("Markdown table shape changed")

    heading_re = re.compile(r"(?m)^\s*(#{1,6})\s+")
    if [len(value) for value in heading_re.findall(source)] != [
        len(value) for value in heading_re.findall(translated)
    ]:
        raise ValueError("Markdown heading levels changed")

    def marker_count(value: str, pattern: str) -> int:
        return sum(
            bool(re.match(pattern, line))
            for line in value.splitlines()
            if line.strip()
        )

    if marker_count(source, r"^\s*[-+*]\s+") != marker_count(
        translated, r"^\s*[-+*]\s+"
    ):
        raise ValueError("unordered list marker count changed")

    def list_signature(value: str) -> list[tuple[int, str]]:
        signature: list[tuple[int, str]] = []
        for line in value.splitlines():
            match = re.match(r"^(\s*)([-+*]|\d{1,3}[.)])\s+", line)
            if not match:
                continue
            indent = len(match.group(1).expandtabs(4))
            if indent <= 1:
                indent = 0
            marker = match.group(2)
            signature.append((indent, "unordered" if marker in "-+*" else marker))
        return signature

    if list_signature(source) != list_signature(translated):
        raise ValueError("Markdown list marker sequence or nesting changed")

    definition_re = re.compile(r"(?m)^(\s*):([ \t]+)")
    if definition_re.findall(source) != definition_re.findall(translated):
        raise ValueError("Markdown definition-list markers changed")

    source_lines = [line for line in source.splitlines() if line.strip()]
    target_lines = [line for line in translated.splitlines() if line.strip()]
    source_is_quote = bool(source_lines) and all(
        re.match(r"^\s*>\s?", line) for line in source_lines
    )
    target_is_quote = bool(target_lines) and all(
        re.match(r"^\s*>\s?", line) for line in target_lines
    )
    if source_is_quote != target_is_quote:
        raise ValueError("blockquote structure changed")

    number_re = re.compile(
        r"(?<![A-Za-z0-9_])(?:"
        r"[vV]?\d+(?:[.,]\d+)+(?:[-+](?=[a-z0-9])[A-Za-z0-9.-]*[A-Za-z0-9])?"
        r"|\d+"
        r")"
        r"(?![A-Za-z0-9_])"
    )
    source_numbers = Counter(number_re.findall(source))
    target_numbers = Counter(number_re.findall(translated))
    if source_numbers != target_numbers:
        raise ValueError(
            "numeric literals changed "
            f"source={list(source_numbers.elements())!r} "
            f"translated={list(target_numbers.elements())!r}"
        )

    acronym_re = re.compile(r"\b[A-Z][A-Z0-9_]{1,}\b")
    ignored_acronyms = {"FAQ", "MANUALLY", "OS", "UNIX"}
    source_acronyms = {
        value for value in acronym_re.findall(source) if value not in ignored_acronyms
    }
    target_acronyms = {
        value for value in acronym_re.findall(translated) if value not in ignored_acronyms
    }
    missing_acronyms = source_acronyms - target_acronyms
    if missing_acronyms:
        raise ValueError(
            "technical acronyms missing "
            f"source={sorted(source_acronyms)!r} "
            f"translated={sorted(target_acronyms)!r}"
        )


def localize_internal_links(document: str, _component: str) -> str:
    """Route document links through /de while leaving shared assets untouched."""
    roots = "|".join(map(re.escape, COMPONENTS))
    component_pattern = re.compile(rf"(?<![A-Za-z0-9_:/])/(?P<root>{roots})/")
    site_pattern = re.compile(r"(?<![A-Za-z0-9_:/])/(?P<root>attribution|search)/")
    asset_pattern = re.compile(
        rf"/de/(?P<root>{roots})/(?P<asset>[^\s)\]>'\"]+\."
        r"(?:png|gif|svg|webp|jpg|jpeg|json|txt|xml|yaml|yml|pdf|zip|tar|gz))",
        flags=re.IGNORECASE,
    )
    lines = document.splitlines(keepends=True)
    output: list[str] = []
    fence_marker = ""
    in_comment = False
    for line in lines:
        stripped = line.rstrip("\n")
        if fence_marker:
            output.append(line)
            if stripped.lstrip().startswith(fence_marker):
                fence_marker = ""
            continue
        fence = base.FENCE_RE.match(stripped)
        if fence:
            fence_marker = fence.group(1)
            output.append(line)
            continue
        if in_comment:
            output.append(line)
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line:
            output.append(line)
            if "-->" not in line:
                in_comment = True
            continue
        localized = component_pattern.sub(r"/de/\g<root>/", line)
        localized = site_pattern.sub(r"/de/\g<root>/", localized)
        localized = asset_pattern.sub(r"/\g<root>/\g<asset>", localized)
        output.append(localized)
    return "".join(output)


def rendered_heading_ids(source: Path, expected_levels: list[int] | None = None) -> list[str]:
    relative = source.relative_to(CONTENT)
    route = relative.parent if source.name in {"_index.md", "index.md"} else relative.with_suffix("")
    rendered_path = PROJECT / "public" / route / "index.html"
    if not rendered_path.is_file():
        return []
    document = rendered_path.read_text(encoding="utf-8", errors="replace")
    rendered = [
        (int(level), base.html.unescape(quoted or bare))
        for level, quoted, bare in re.findall(
            r'<h([1-6])[^>]*\sid=(?:"([^"]+)"|([^\s>]+))', document
        )
    ]
    if expected_levels is not None and len(rendered) != len(expected_levels):
        for start in range(0, len(rendered) - len(expected_levels) + 1):
            window = rendered[start : start + len(expected_levels)]
            if [level for level, _ in window] == expected_levels:
                return [value for _, value in window]
    return [value for _, value in rendered]


def translate_german_body(
    body: str,
    *,
    source: Path,
    component: str,
    model: str,
    scalar_model: str,
    cache,
    max_chars: int,
) -> str:
    """Translate compatible prose atoms in batches to reduce model round trips."""
    del scalar_model  # Headings are translated with their surrounding prose.
    source_document = source.read_text(encoding="utf-8")
    source_front, _ = base.split_front_matter(source_document)
    file_line_offset = len(source_front.splitlines()) + 2
    source_relative = str(source.relative_to(CONTENT))
    body = base.add_heading_anchors(body, source)
    lines = body.splitlines(keepends=True)
    flags = base.verbatim_ranges(lines)
    output: list[str] = []
    pending: list[str] = []
    pending_size = 0

    def flush_pending() -> None:
        nonlocal pending, pending_size
        if pending:
            output.append(
                base.translate_text(
                    "".join(pending),
                    component=component,
                    model=model,
                    cache=cache,
                )
            )
        pending = []
        pending_size = 0

    def queue(atom: str) -> None:
        nonlocal pending_size
        if pending and pending_size + len(atom) > max_chars:
            flush_pending()
        pending.append(atom)
        pending_size += len(atom)
        if pending_size >= max_chars:
            flush_pending()

    def is_literal_atom(atom: str, file_start_line: int) -> bool:
        nonblank = [line for line in atom.splitlines() if line.strip()]
        if not nonblank:
            return False
        atom_line_numbers = [
            file_start_line + index
            for index, line in enumerate(atom.splitlines())
            if line.strip()
        ]
        for range_start, range_end in INDENTED_LITERAL_RANGES.get(source_relative, ()):
            if atom_line_numbers and all(
                range_start <= line_number <= range_end
                for line_number in atom_line_numbers
            ):
                return True
        first_line = nonblank[0].lstrip()
        quote_lines = [
            line.lstrip()[1:].strip()
            for line in atom.splitlines()
            if line.lstrip().startswith(">")
        ]
        literal_quote = bool(quote_lines) and all(
            not content or re.fullmatch(r"`.*`", content)
            for content in quote_lines
        )
        config_prefix = re.match(
            r"^(?:frontend|backend|listen|defaults|global|fcgi-app|cache|peers|ring|resolvers|userlist|stick-table|table|shards|acl|http-request|http-response|tcp-request|tcp-response|http-check|tcp-check|use_backend|default_backend)\b",
            first_line,
        )
        all_indented = all(
            line.startswith(("    ", "\t"))
            and not re.match(r"^\s*(?:>|[-+*]\s+|\d+[.)]\s+)", line)
            for line in nonblank
        )
        indented_code = all_indented and bool(
            re.match(
                r"^(?:[$#>]|>>>|\+[-+| ]|\d{4}-\d{2}-\d{2}[ T]|"
                r"[A-Za-z_][A-Za-z0-9_.-]*\s*=|[{}\[\]])",
                first_line,
            )
        )
        command_output = re.search(
            r"(?:Active Internet connections|Proto\s+Recv-Q|PID/Program name|"
            r"HAProxy version .*Copyright|Build options:|Default settings:|"
            r"Encrypted password support|Available polling systems:|Total: \d+)",
            atom,
        )
        return bool(config_prefix or indented_code or literal_quote or command_output)

    def split_long_atom(atom: str) -> list[str]:
        if len(atom) <= max_chars:
            return [atom]
        atom_lines = atom.splitlines(keepends=True)
        logical_blocks: list[str] = []
        current: list[str] = []
        saw_boundary = False
        for line in atom_lines:
            boundary = bool(
                re.match(r"^\s*(?:[-+*]|\d{1,3}[.)])\s+", line)
                or line.lstrip().startswith("|")
            )
            if boundary and current:
                logical_blocks.append("".join(current))
                current = []
                saw_boundary = True
            current.append(line)
        if current:
            logical_blocks.append("".join(current))
        if not saw_boundary:
            return [atom]

        pieces: list[str] = []
        pending_blocks: list[str] = []
        pending_length = 0
        for block in logical_blocks:
            if pending_blocks and pending_length + len(block) > max_chars:
                pieces.append("".join(pending_blocks))
                pending_blocks = []
                pending_length = 0
            pending_blocks.append(block)
            pending_length += len(block)
        if pending_blocks:
            pieces.append("".join(pending_blocks))
        return pieces

    index = 0
    while index < len(lines):
        if flags[index]:
            flush_pending()
            start = index
            while index < len(lines) and flags[index]:
                index += 1
            output.append("".join(lines[start:index]))
            continue

        start = index
        while index < len(lines) and not flags[index]:
            index += 1
            if not lines[index - 1].strip():
                break
        atom = "".join(lines[start:index])
        if re.fullmatch(r"\s*(?:-{3,}|\*{3,}|_{3,})\s*", atom):
            flush_pending()
            output.append(atom)
            continue
        if not atom.strip() or not base.ASCII_WORD_RE.search(atom):
            queue(atom)
            continue
        if atom.strip("\n") in base.MANUAL_TRANSLATIONS:
            flush_pending()
            output.append(
                base.translate_text(
                    atom,
                    component=component,
                    model=model,
                    cache=cache,
                )
            )
            continue
        if component == "etcd" and re.search(
            r"</?(?:table|thead|tbody|tr|th|td|p|ul|li|pre|strong|a)\b",
            atom,
            flags=re.IGNORECASE,
        ):
            flush_pending()
            output.append(
                base.translate_html_fragment(
                    atom,
                    component=component,
                    model=model,
                    cache=cache,
                )
            )
            continue
        nonblank_atom = [line for line in atom.splitlines() if line.strip()]
        first_atom_line = nonblank_atom[0].lstrip() if nonblank_atom else ""
        definition_atom = first_atom_line.startswith(":")
        short_term_atom = (
            len(nonblank_atom) == 1
            and len(first_atom_line) <= 160
            and not re.match(r"(?:#{1,6}|[-+*]|\d{1,3}[.)]|\|)", first_atom_line)
            and not first_atom_line.endswith((".", ":", ";", "!", "?"))
        )
        if definition_atom or short_term_atom:
            flush_pending()
            output.append(
                base.translate_text(
                    atom,
                    component=component,
                    model=model,
                    cache=cache,
                )
            )
            continue
        if is_literal_atom(atom, file_line_offset + start + 1):
            flush_pending()
            output.append(atom)
            continue
        for piece in split_long_atom(atom):
            queue(piece)

    flush_pending()
    translated = "".join(output)
    # A model can preserve both constructs yet remove the blank line between a
    # translated heading and the first Markdown table row at a chunk boundary.
    translated = re.sub(
        r"(?m)^(#{1,6}[^\n]*?\{#[A-Za-z0-9_.:-]+\})(?=[ \t]*\S)",
        r"\1\n\n",
        translated,
    )
    inline_span_re = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
    source_lines = body.splitlines(keepends=True)
    source_flags = base.verbatim_ranges(source_lines)
    allowed_inline = Counter(
        literal
        for index, line in enumerate(source_lines)
        if not source_flags[index]
        for literal in inline_span_re.findall(line)
    )
    used_inline: Counter[str] = Counter()
    translated_lines = translated.splitlines(keepends=True)
    translated_flags = base.verbatim_ranges(translated_lines)

    def drop_added_inline(match: re.Match[str]) -> str:
        literal = match.group(1)
        if used_inline[literal] < allowed_inline[literal]:
            used_inline[literal] += 1
            return match.group(0)
        return literal

    translated = "".join(
        line if translated_flags[index] else inline_span_re.sub(drop_added_inline, line)
        for index, line in enumerate(translated_lines)
    )
    return localize_internal_links(translated, component)


def legal_passthroughs() -> dict[str, str]:
    """Keep the pgBadger PostgreSQL License clauses verbatim."""
    source = (CONTENT / "pgbadger" / "license.md").read_text(encoding="utf-8")
    body = source.split("## PostgreSQL License {#postgresql-license}\n", 1)[1]
    legal = body.split("\n## Authors and design credits", 1)[0]
    return {
        paragraph.strip(): paragraph.strip()
        for paragraph in legal.split("\n\n")
        if paragraph.strip()
    }


base.STYLE_GUIDE = STYLE_GUIDE
class GermanProtector(base.Protector):
    """Protect collapsed reference links before the shared protector runs."""

    TERMINOLOGY = (
        (r"\bSHA256\b", "SHA256-Prüfsumme"),
        (r"\bEOL\b", "Zeilenende (EOL)"),
        (r"\bDC\b", "Rechenzentrum (DC)"),
        (r"\bsingle-member cluster\b", "Ein-Mitglied-Cluster"),
        (r"\bmulti-machine cluster\b", "Cluster mit mehreren Rechnern"),
        (r"\bmixed-version cluster\b", "Cluster mit gemischten Versionen"),
        (r"\bhigh availability\b", "Hochverfügbarkeit"),
        (r"\bautomatic failover\b", "automatisches Failover"),
        (r"\bdistributed configuration store\b", "verteilter Konfigurationsspeicher"),
        (r"\bconnection pools\b", "Verbindungspools"),
        (r"\bconnection pool\b", "Verbindungspool"),
        (r"\bconnection pooling\b", "Verbindungs-Pooling"),
        (r"\btransaction pooling\b", "Transaktions-Pooling"),
        (r"\bsession pooling\b", "Session-Pooling"),
        (r"\bprepared statements\b", "vorbereitete Anweisungen"),
        (r"\bprepared statement\b", "vorbereitete Anweisung"),
        (r"\bpoint-in-time recovery\b", "Point-in-Time-Recovery"),
        (r"\bwrite-ahead logs\b", "Write-Ahead-Logs"),
        (r"\bwrite-ahead log\b", "Write-Ahead-Log"),
        (r"\brolling upgrade\b", "Rolling Upgrade"),
        (r"\bkey-value stores\b", "Schlüssel-Wert-Speicher"),
        (r"\bkey-value store\b", "Schlüssel-Wert-Speicher"),
        (r"\bload balancers\b", "Load-Balancer"),
        (r"\bload balancer\b", "Load-Balancer"),
        (r"\bload balancing\b", "Lastverteilung"),
        (r"\breverse proxies\b", "Reverse-Proxys"),
        (r"\breverse proxy\b", "Reverse-Proxy"),
        (r"\bhealth checks\b", "Health Checks"),
        (r"\bhealth check\b", "Health Check"),
        (r"\bgraceful shutdown\b", "geordnetes Herunterfahren"),
        (r"\bgraceful reload\b", "unterbrechungsfreies Neuladen"),
        (r"\baccess control lists\b", "Zugriffskontrolllisten"),
        (r"\baccess control list\b", "Zugriffskontrollliste"),
        (r"\bstick tables\b", "Stick Tables"),
        (r"\bstick table\b", "Stick Table"),
        (r"\bsample fetches\b", "Sample-Abrufe"),
        (r"\bsample fetch\b", "Sample-Abruf"),
        (r"\brate limits\b", "Ratenbegrenzungen"),
        (r"\brate limit\b", "Ratenbegrenzung"),
        (r"\bfile descriptors\b", "Dateideskriptoren"),
        (r"\bfile descriptor\b", "Dateideskriptor"),
        (r"\bUnix sockets\b", "Unix-Sockets"),
        (r"\bUnix socket\b", "Unix-Socket"),
        (r"\bcommand line\b", "Befehlszeile"),
        (r"\buser guides\b", "Benutzerhandbücher"),
        (r"\buser guide\b", "Benutzerhandbuch"),
        (r"\brelease notes\b", "Versionshinweise"),
    )

    @staticmethod
    def temporary_marker(index: int) -> str:
        return f"@@xq{base.alpha_index(index).lower()}@@"

    @staticmethod
    def external_marker(index: int) -> str:
        return f"<x-{base.alpha_index(index).lower()}/>"

    def token(self, value: str) -> str:
        token = self.temporary_marker(len(self.values))
        self.values.append(value)
        return token

    def restore(self, text: str) -> str:
        for index, value in enumerate(self.values):
            token = self.external_marker(index)
            count = text.count(token)
            repeatable = bool(
                re.fullmatch(r"--?[A-Za-z0-9][A-Za-z0-9_.-]*(?:=[^\s,;]+)?", value)
            )
            if count < 1 or (count > 1 and not repeatable):
                raise ValueError(f"placeholder {token} occurred {count} times")
            text = text.replace(token, value)
        if re.search(r"<x-[a-z]+\s*/>", text):
            raise ValueError("translation contains an unknown placeholder")
        return text

    def protect(self, text: str) -> str:
        text = re.sub(
            r"(?m)^(\s*:[ \t]+)",
            lambda match: self.token(match.group(1)),
            text,
        )
        collapsed_reference_re = re.compile(
            r"(?P<image>!?)\[(?P<label>[^]\n]+)\]\[\]"
        )
        text = collapsed_reference_re.sub(
            lambda match: (
                self.token(f'{match.group("image")}[')
                + match.group("label")
                + self.token(f'][{match.group("label")}]')
            ),
            text,
        )
        text = super().protect(text)
        for pattern, german in self.TERMINOLOGY:
            text = re.sub(pattern, german, text, flags=re.IGNORECASE)
        text = PROTECTED_NUMBER_RE.sub(
            lambda match: self.token(match.group(0)),
            text,
        )
        for index in range(len(self.values)):
            text = text.replace(self.temporary_marker(index), self.external_marker(index))
        return text


base.CACHE_SCHEMA_VERSION = "de-10"
base.MANUAL_TRANSLATIONS = legal_passthroughs()
base.CATEGORY_MAP = CATEGORY_MAP
base.TRANSLATABLE_META = TRANSLATABLE_META
base.system_prompt = german_system_prompt
base.post_ollama = german_post_ollama
base.normalize_model_output = normalize_german_model_output
base.normalize_chinese_spacing = normalize_german_output
base.localize_internal_links = localize_internal_links
base.rendered_heading_ids = rendered_heading_ids
base.validate_fragment_structure = validate_german_fragment_structure
base.Protector = GermanProtector
base.translate_front_matter = translate_german_front_matter
base.translate_body = translate_german_body
base.translate_text = translate_german_text


def split_fenced_blocks(body: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    marker = ""
    for line in body.splitlines(keepends=True):
        match = base.FENCE_RE.match(line.rstrip("\n"))
        if not marker and match:
            marker = match.group(1)
            current = [line]
        elif marker:
            current.append(line)
            if line.lstrip().startswith(marker):
                blocks.append("".join(current))
                current = []
                marker = ""
    if marker:
        raise RuntimeError("unterminated Markdown fence")
    return blocks


def front_value(front: str, key: str) -> list[str]:
    return re.findall(rf"^{re.escape(key)}:\s*(.*)$", front, flags=re.MULTILINE)


def normalized_reference_definitions(body: str) -> list[str]:
    definitions: list[str] = []
    for line in body.splitlines():
        if not base.REFERENCE_DEF_RE.match(line):
            continue
        definitions.append(re.sub(r"/de/(?=(?:" + "|".join(COMPONENTS) + r")/)", "/", line))
    return definitions


def markdown_destinations(body: str) -> Counter[str]:
    destinations: list[str] = []
    for target in re.findall(r"!?\[[^\]]*\]\(([^)\n]+)\)", body):
        target = re.sub(r"^/de/(?=(?:" + "|".join(COMPONENTS) + r"|attribution|search)/)", "/", target)
        destinations.append(target)
    return Counter(destinations)


def reference_link_signature(body: str) -> list[str]:
    signature: list[str] = []
    for match in re.finditer(r"!?\[([^]\n]*)\]\[([^]\n]*)\]", body):
        signature.append((match.group(2) or match.group(1)).casefold())
    return signature


def validate_pair(source_text: str, translated_text: str, source: Path) -> None:
    source_front, source_body = base.split_front_matter(source_text)
    target_front, target_body = base.split_front_matter(translated_text)
    for key in ("weight", "icon", "module", "upstream_link", "upstream_name", "upstream_ref", "aliases", "outputs"):
        if front_value(source_front, key) != front_value(target_front, key):
            raise RuntimeError(f"front matter {key} changed")
    if split_fenced_blocks(source_body) != split_fenced_blocks(target_body):
        raise RuntimeError("fenced code or literal output changed")
    if normalized_reference_definitions(source_body) != normalized_reference_definitions(target_body):
        raise RuntimeError("reference definitions changed")
    source_comments = re.findall(r"<!--.*?-->", source_body, flags=re.DOTALL)
    target_comments = re.findall(r"<!--.*?-->", target_body, flags=re.DOTALL)
    if source_comments != target_comments:
        raise RuntimeError("HTML comments changed")
    source_shortcodes = re.findall(r"\{\{[%<].*?[>%]\}\}", source_body)
    target_shortcodes = re.findall(r"\{\{[%<].*?[>%]\}\}", target_body)
    if source_shortcodes != target_shortcodes:
        raise RuntimeError("shortcodes changed")
    footnote_re = re.compile(r"\[\^[^\]\n]+\]")
    if footnote_re.findall(source_body) != footnote_re.findall(target_body):
        raise RuntimeError("footnote references changed")
    if markdown_destinations(source_body) != markdown_destinations(target_body):
        raise RuntimeError("Markdown link or asset targets changed")
    if reference_link_signature(source_body) != reference_link_signature(target_body):
        raise RuntimeError("reference-link structure or identifiers changed")


def target_for(source: Path) -> Path:
    return source.with_name(source.name.removesuffix(".md") + ".de.md")


def component_for(source: Path) -> str:
    relative = source.relative_to(CONTENT)
    return relative.parts[0] if len(relative.parts) > 1 else "site"


def translate_file(
    source: Path,
    *,
    model: str,
    scalar_model: str,
    cache,
    max_chars: int,
    force: bool,
    dry_run: bool,
) -> Path:
    target = target_for(source)
    if target.exists() and not force:
        print(f"skip existing {target.relative_to(PROJECT)}", flush=True)
        return target
    source_text = source.read_text(encoding="utf-8")
    front, body = base.split_front_matter(source_text)
    component = component_for(source)
    translated_front = base.translate_front_matter(
        front,
        component=component,
        scalar_model=scalar_model,
        fallback_model=model,
        cache=cache,
    )
    translated_body = base.translate_body(
        body,
        source=source,
        component=component,
        model=model,
        scalar_model=scalar_model,
        cache=cache,
        max_chars=max_chars,
    )
    translated_text = f"---\n{translated_front}\n---\n{translated_body}"
    validate_pair(source_text, translated_text, source)
    if dry_run:
        print(translated_text)
        return target
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(translated_text, encoding="utf-8")
    strict_errors: list[str] = []
    rendered_root = PROJECT / "public"
    german_checker.validate_pair(
        source.resolve(),
        temporary.resolve(),
        rendered_root.resolve() if rendered_root.is_dir() else None,
        strict_errors,
    )
    if strict_errors:
        temporary.unlink(missing_ok=True)
        raise RuntimeError("; ".join(strict_errors))
    os.replace(temporary, target)
    print(f"wrote {target.relative_to(PROJECT)}", flush=True)
    return target


def is_english_source(path: Path) -> bool:
    return path.suffix == ".md" and not LOCALIZED_SUFFIX_RE.search(path.name)


def discover_sources(requested: list[str], components: list[str]) -> list[Path]:
    if requested:
        sources: list[Path] = []
        for value in requested:
            path = Path(value)
            if not path.is_absolute():
                path = PROJECT / path
            path = path.resolve()
            if not path.is_file() or not is_english_source(path):
                raise RuntimeError(f"not an English Markdown source: {value}")
            try:
                path.relative_to(CONTENT.resolve())
            except ValueError as exc:
                raise RuntimeError(f"source is outside content/: {value}") from exc
            sources.append(path)
        return sorted(set(sources), key=lambda path: (path.stat().st_size, str(path)))

    sources = [path for path in CONTENT.rglob("*.md") if is_english_source(path)]
    if components:
        allowed = set(components)
        sources = [
            path
            for path in sources
            if (component_for(path) in allowed or ("site" in allowed and component_for(path) == "site"))
        ]
    return sorted(sources, key=lambda path: (path.stat().st_size, str(path)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--component", action="append", choices=("site",) + COMPONENTS, default=[])
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--scalar-model")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--max-chars", type=int, default=10000)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_chars < 500:
        raise RuntimeError("--max-chars must be at least 500")
    scalar_model = args.scalar_model or args.model
    sources = discover_sources(args.paths, args.component)
    if args.limit is not None:
        sources = sources[: args.limit]
    cache = base.Cache.load(args.cache)
    print(
        f"translating {len(sources)} English files to German with {args.model}; "
        f"scalar model={scalar_model}; cache entries={len(cache.entries)}",
        flush=True,
    )
    for index, source in enumerate(sources, 1):
        print(f"[{index}/{len(sources)}] {source.relative_to(PROJECT)}", flush=True)
        translate_file(
            source,
            model=args.model,
            scalar_model=scalar_model,
            cache=cache,
            max_chars=args.max_chars,
            force=args.force,
            dry_run=args.dry_run,
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
    except Exception as exc:
        print(f"German translation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
