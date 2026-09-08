#!/usr/bin/env python3
"""Translate the six component documentation collections into Russian.

The English Markdown is authoritative.  This helper reuses the placeholder
protector and cache implementation from ``translate-component-docs.py``, then
adds Russian prompts, terminology, route localization, fail-closed structural
validation, and atomic ``*.ru.md`` writes.  It never reads a Chinese page as a
source and never writes a ``*.zh.md`` target.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType


PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content" / "docs"
STYLE_GUIDE = PROJECT / "RUSSIAN_TRANSLATION.md"
BASE_TRANSLATOR = Path(__file__).with_name("translate-component-docs.py")
DEFAULT_CACHE = PROJECT / ".hugo_cache" / "russian-translation-cache.json"
DEFAULT_MODEL = "qwen3:30b-a3b-instruct-2507-q4_K_M"
DEFAULT_SCALAR_MODEL = DEFAULT_MODEL
CACHE_SCHEMA_VERSION = "1"

SUPPORTED_COMPONENTS = (
    "patroni",
    "pgbackrest",
    "pgbouncer",
    "pgbadger",
    "haproxy",
    "etcd",
)
COMPONENT_DISPLAY_NAMES = {
    "patroni": "Patroni",
    "pgbackrest": "pgBackRest",
    "pgbouncer": "PgBouncer",
    "pgbadger": "pgBadger",
    "haproxy": "HAProxy",
    "etcd": "etcd",
}
TRANSLATABLE_META = {"title", "linkTitle", "description"}
CATEGORY_MAP = {
    "Concept": "Концепция",
    "Task": "Задача",
    "Reference": "Справочник",
    "Tutorial": "Руководство",
}


def load_base_translator() -> ModuleType:
    """Load the existing helper despite the hyphen in its file name."""

    spec = importlib.util.spec_from_file_location(
        "_pgsql_component_translation_base", BASE_TRANSLATOR
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load base translator: {BASE_TRANSLATOR}")
    module = importlib.util.module_from_spec(spec)
    # dataclasses resolves annotations through sys.modules during import.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BASE = load_base_translator()
Cache = BASE.Cache
HEADING_RE = BASE.HEADING_RE
FENCE_RE = BASE.FENCE_RE
REFERENCE_DEF_RE = BASE.REFERENCE_DEF_RE
ANCHOR_ONLY_RE = BASE.ANCHOR_ONLY_RE
NUMBER_TOKEN_RE = BASE.NUMBER_TOKEN_RE
ASCII_WORD_RE = BASE.ASCII_WORD_RE

CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
HAN_RE = re.compile(r"[\u3400-\u9fff]")
MIXED_SCRIPT_RE = re.compile(r"[A-Za-z][А-Яа-яЁё]|[А-Яа-яЁё][A-Za-z]")
LANGUAGE_SUFFIX_RE = re.compile(r"\.[a-z]{2}(?:-[a-z]{2})?\.md$", re.IGNORECASE)
LEGAL_START_RE = re.compile(
    r"^(?:"
    r"Copyright(?:\s|\()|"
    r"Permission (?:is hereby granted|to use)|"
    r"Redistribution and use|"
    r"THE SOFTWARE IS PROVIDED|"
    r"THIS SOFTWARE IS PROVIDED|"
    r"IN NO EVENT|"
    r"(?:[A-Za-z][A-Za-z .'-]+ )?SPECIFICALLY DISCLAIMS|"
    r"Neither the name|"
    r"Except as contained|"
    r"[A-Z][A-Z ,'-]{18,}(?:DISCLAIM|WARRANT|LIAB|DAMAGE)"
    r")"
)
HTML_PROSE_RE = re.compile(
    r"</?(?:table|thead|tbody|tr|th|td|p|ul|ol|li|dl|dt|dd|pre|strong|em|a|span)\b",
    flags=re.IGNORECASE,
)
RAW_CONFIG_PREFIX_RE = re.compile(
    r"^(?:"
    r"frontend|backend|listen|defaults|global|fcgi-app|cache|peers|ring|"
            r"resolvers|userlist|stick-table|table|shards|acl|http-request|"
            r"http-response|tcp-request|tcp-response|http-check|tcp-check|"
            r"use_backend|default_backend"
    r")\b"
)
RAW_OUTPUT_RE = re.compile(
    r"(?:"
    r"Active Internet connections|Proto\s+Recv-Q|PID/Program name|"
    r"HAProxy version .*Copyright|Build options:|Default settings:|"
    r"Encrypted password support|Available polling systems:|Total: \d+|"
    r"^\s*(?:\$|#|>>>|\.\.\.)\s+\S"
    r")",
    flags=re.MULTILINE,
)

# These are names or literal values, not untranslated prose.  Other English
# words must produce Cyrillic output or the fragment is rejected.
NON_PROSE_WORDS = {
    "acl",
    "api",
    "ascii",
    "aws",
    "ca",
    "cli",
    "cpu",
    "crc",
    "dcs",
    "dns",
    "docker",
    "etcd",
    "etcdctl",
    "etcdutl",
    "Etcdv3",
    "false",
    "freebsd",
    "github",
    "grpc",
    "haproxy",
    "html",
    "http",
    "https",
    "json",
    "kubernetes",
    "linux",
    "macos",
    "mvcc",
    "nginx",
    "null",
    "off",
    "on",
    "openssl",
    "patroni",
    "pgbackrest",
    "pgbadger",
    "pgbouncer",
    "postgresql",
    "prometheus",
    "python",
    "quic",
    "raft",
    "rc",
    "rpc",
    "sni",
    "spoe",
    "sql",
    "ssh",
    "tcp",
    "tls",
    "true",
    "ttl",
    "udp",
    "unix",
    "url",
    "utf",
    "v",
    "wal",
    "windows",
    "yaml",
}
NONTRANSLATABLE_SCALARS = {
    "Barman",
    "bbolt",
    "C",
    "C++",
    "Citus",
    "Clojure",
    "Consul",
    "Docker",
    "Elixir",
    "Erlang",
    "Go",
    "Gradle",
    "Grafana",
    "Haskell",
    "Java",
    "JSON",
    "Kubernetes",
    "Linux",
    "Lua",
    "Nim",
    "Perl",
    "PHP",
    "Prometheus",
    "Psycopg",
    "Python",
    "R",
    "Ruby",
    "Rust",
    "Scala",
    "Swagger",
    "Tcl",
    "ZooKeeper",
    "Patroni",
    "patroni_barman config-switch",
    "pgBackRest",
    "PgBouncer",
    "pgBadger",
    "HAProxy",
    "etcd",
    "etcdctl",
    "etcdutl",
    "Etcdv3",
    "PostgreSQL",
    "MIT License",
    "ISC License",
    "PostgreSQL License",
    "Apache License 2.0",
    "GNU General Public License version 2",
}
ENGLISH_FUNCTION_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "below", "by", "can",
    "each", "for", "from", "has", "have", "if", "in", "into", "is", "it",
    "may", "must", "not", "of", "on", "or", "should", "that", "the", "their",
    "this", "to", "was", "were", "will", "with", "would",
}


def default_endpoint() -> str:
    host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
    if host.endswith("/api/generate"):
        return host
    return host + "/api/generate"


@dataclass(frozen=True)
class GenerationOptions:
    endpoint: str
    timeout: int
    temperature: float
    top_p: float
    repeat_penalty: float
    num_ctx: int
    num_predict: int
    keep_alive: str
    retries: int

    def cache_signature(self) -> str:
        # The endpoint and timeout do not affect the generated text.
        return json.dumps(
            {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "repeat_penalty": self.repeat_penalty,
                "num_ctx": self.num_ctx,
                "num_predict": self.num_predict,
            },
            sort_keys=True,
        )


class RussianProtector(BASE.Protector):
    """Extend the proven Markdown protector with common config identifiers."""

    def protect(self, text: str) -> str:
        text = super().protect(text)
        # Do not let the extra ASCII patterns match the ``P0001`` portion of
        # placeholders already emitted by the base protector.  Private-use
        # characters are safe here because they live only for this method.
        existing = re.findall(r"⟦P\d{4}⟧", text)
        shields = {
            token: chr(0xE000 + index) for index, token in enumerate(dict.fromkeys(existing))
        }
        for token, shield in shields.items():
            text = text.replace(token, shield)
        # Apply the extra rules in one pass.  Separate substitution passes
        # would see and re-protect placeholders emitted by an earlier pass.
        extra_literals = re.compile(
            r"(?:"
            # image alt identifiers and fixture names may begin with digits
            + r"\b\d+[A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b|"
            # numeric facts, versions, and units must stay byte-for-byte
            + r"(?<![A-Za-z0-9_])\d+(?:\.\d+)?\s?(?:ns|us|ms|s|min|h|d|B|kB|KB|MB|GB|TB|KiB|MiB|GiB|%)(?![A-Za-z0-9])|"
            + r"(?<![A-Za-z0-9_])(?:v|V)?\d+(?:\.\d+)+(?:[-+](?:[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)*)?)?(?![A-Za-z0-9])|"
            + NUMBER_TOKEN_RE.pattern
            + r"|"
            # snake_case settings, fields, and metrics
            r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b|"
            # dotted settings and file-like identifiers
            r"\b[A-Za-z][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)+\b|"
            # function calls
            r"\b[A-Za-z_][A-Za-z0-9_]*(?=\(\))|"
            # upper-case commands and protocol constants
            r"\b(?:SIG[A-Z0-9]+|[A-Z][A-Z0-9_-]{2,})\b"
            r")"
        )
        text = self.substitute(extra_literals, text)
        for token, shield in shields.items():
            text = text.replace(shield, token)
        return text


def guide_section(heading: str) -> str:
    guide = STYLE_GUIDE.read_text(encoding="utf-8")
    marker = f"## {heading}"
    try:
        return guide.split(marker, 1)[1].split("\n## ", 1)[0]
    except IndexError as exc:
        raise RuntimeError(f"missing glossary section {marker!r}") from exc


def glossary_entries(component: str) -> list[tuple[str, str]]:
    headings = [
        "Common terminology",
        f"{COMPONENT_DISPLAY_NAMES[component]} terminology",
    ]
    entries: list[tuple[str, str]] = []
    for heading in headings:
        for line in guide_section(heading).splitlines():
            if not line.startswith("|") or line.startswith("| ---"):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) < 2 or cells[0] == "English":
                continue
            entries.append((cells[0], cells[1]))
    return entries


def parse_glossary(component: str, source: str) -> str:
    source_lower = source.lower()
    selected: list[str] = []
    for english_term, russian_term in glossary_entries(component):
        candidates = [
            re.sub(r"\s*\([^)]*\)\s*", "", candidate).strip()
            for candidate in english_term.lower().split("/")
        ]
        for candidate in candidates:
            if candidate and re.search(
                rf"(?<![a-z0-9]){re.escape(candidate)}(?:s|es|ed|ing)?(?![a-z0-9])",
                source_lower,
            ):
                selected.append(f"{english_term} => {russian_term}")
                break
    return "\n".join(f"- {entry}" for entry in selected) or "- no glossary terms selected"


def system_prompt(component: str, source: str, mode: str) -> str:
    display = COMPONENT_DISPLAY_NAMES[component]
    scalar_note = (
        "Return one metadata phrase on one line. Do not return a YAML key or quotes."
        if mode == "scalar"
        else "Preserve the Markdown line, list, table, and blockquote structure."
    )
    return f"""You are a senior Russian technical editor translating the official {display} documentation from English into Russian.

Requirements:
1. Translate every natural-language word in the supplied fragment into accurate, idiomatic, concise professional Russian. Do not summarize, omit, merge, or add information.
2. {scalar_note}
3. Every placeholder of the form ⟦Pdddd⟧ is immutable and must occur exactly once, in the original order. Never invent a placeholder.
4. Keep product spelling, commands, options, configuration keys and values, API/RPC/message/field names, environment variables, metrics, file names, paths, protocol identifiers, versions, numbers, and units unchanged.
5. Preserve negation and normative strength: must=должен/обязательно, should=следует/рекомендуется, may/can=может/можно.
6. Translate link labels and visible explanatory HTML text, but never alter a URL, anchor, shortcode, footnote identifier, or HTML tag.
7. Use Russian punctuation and a neutral operator-oriented style. Keep established Latin abbreviations such as API, CLI, CPU, DCS, DNS, HTTP, Raft, RPC, SQL, TCP, TLS, TTL, and WAL.
8. Output only the translated fragment, with no preface, explanation, quotation wrapper, or code fence.

Mandatory terminology for this fragment:
{parse_glossary(component, source)}"""


def post_ollama(model: str, prompt: str, options: GenerationOptions) -> str:
    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "keep_alive": options.keep_alive,
            "options": {
                "temperature": options.temperature,
                "top_p": options.top_p,
                "repeat_penalty": options.repeat_penalty,
                "num_ctx": options.num_ctx,
                "num_predict": options.num_predict,
            },
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        options.endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=options.timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Ollama request failed at {options.endpoint}: {exc}") from exc
    translated = result.get("response")
    if not isinstance(translated, str) or not translated.strip():
        raise RuntimeError(f"Ollama returned no translation: {result}")
    return translated


def normalize_brand_spelling(value: str) -> str:
    brands = (
        (r"\bpgbackrest\b", "pgBackRest"),
        (r"\bpgbouncer\b", "PgBouncer"),
        (r"\bpgbadger\b", "pgBadger"),
        (r"\bhaproxy\b", "HAProxy"),
        (r"\bpostgresql\b", "PostgreSQL"),
        (r"\bopenssl\b", "OpenSSL"),
        (r"\bpatroni\b", "Patroni"),
        (r"\betcdctl\b", "etcdctl"),
        (r"\betcd\b", "etcd"),
    )
    parts = re.split(r"(⟦P\d{4}⟧)", value)
    for index, part in enumerate(parts):
        if re.fullmatch(r"⟦P\d{4}⟧", part):
            continue
        for pattern, spelling in brands:
            part = re.sub(pattern, spelling, part, flags=re.IGNORECASE)
        parts[index] = part
    return "".join(parts)


def cache_key(
    model: str,
    component: str,
    mode: str,
    prompt: str,
    source: str,
    options: GenerationOptions,
) -> str:
    style_digest = hashlib.sha256(STYLE_GUIDE.read_bytes()).hexdigest()
    payload = "\0".join(
        (
            CACHE_SCHEMA_VERSION,
            model,
            component,
            mode,
            style_digest,
            options.cache_signature(),
            prompt,
            source,
        )
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def meaningful_english_words(protected: str) -> list[str]:
    without_placeholders = re.sub(r"⟦P\d{4}⟧", " ", protected)
    words = re.findall(r"[A-Za-z][A-Za-z-]*", without_placeholders)
    meaningful: list[str] = []
    for word in words:
        normalized = word.strip("-").lower()
        if not normalized or normalized in NON_PROSE_WORDS:
            continue
        if word.isupper() or re.search(r"\d", word):
            continue
        meaningful.append(word)
    return meaningful


def table_signature(value: str) -> list[int]:
    return [
        len(re.findall(r"(?<!\\)\|", line))
        for line in value.splitlines()
        if line.lstrip().startswith("|")
    ]


def list_signature(value: str) -> list[tuple[int, str]]:
    signature: list[tuple[int, str]] = []
    active_ordered_indents: set[int] = set()
    for line in value.splitlines():
        match = re.match(r"^(\s*)([-+*]|\d{1,3}[.)])\s+", line)
        if not match:
            if line.strip() and not line.startswith((" ", "\t", ">")):
                active_ordered_indents.clear()
            continue
        indent = len(match.group(1).expandtabs(4))
        if indent <= 1:
            indent = 0
        marker = match.group(2)
        if marker in "-+*":
            signature.append((indent, "unordered"))
        elif int(marker[:-1]) == 1 or indent in active_ordered_indents:
            signature.append((indent, marker))
            active_ordered_indents.add(indent)
    return signature


def blockquote_signature(value: str) -> list[tuple[int, str]]:
    signature: list[tuple[int, str]] = []
    for line in value.splitlines():
        match = re.match(r"^\s*(>+)\s?(.*)$", line)
        if not match:
            continue
        admonition = re.match(r"\[!([A-Za-z]+)\]", match.group(2))
        signature.append(
            (len(match.group(1)), admonition.group(1).upper() if admonition else "")
        )
    return signature


def protected_literal_counter(value: str) -> Counter[str]:
    protector = RussianProtector()
    protector.protect(value)
    return Counter(protector.values)


def number_counter(value: str) -> Counter[str]:
    # Compare numeric facts independently of Russian ordinal suffixes and
    # decimal typography.  Technical units and full versions are additionally
    # protected byte-for-byte by RussianProtector.
    value = re.sub(
        r"(?<=\d)[,\u00a0\u202f ](?=\d{3}(?:\D|$))",
        "",
        value,
    )
    return Counter(
        token.replace(",", ".")
        for token in re.findall(r"(?<!\d)\d+(?:[.,]\d+)*(?!\d)", value)
    )


def validate_fragment_structure(source: str, translated: str) -> None:
    if table_signature(source) != table_signature(translated):
        raise ValueError("Markdown table shape changed")
    if list_signature(source) != list_signature(translated):
        raise ValueError("Markdown list marker sequence or nesting changed")
    if blockquote_signature(source) != blockquote_signature(translated):
        raise ValueError("blockquote or admonition structure changed")
    if number_counter(source) != number_counter(translated):
        raise ValueError(
            "numbers, versions, or units changed "
            f"source={sorted(number_counter(source).elements())!r} "
            f"translated={sorted(number_counter(translated).elements())!r}"
        )
    if protected_literal_counter(source) - protected_literal_counter(translated):
        missing = protected_literal_counter(source) - protected_literal_counter(translated)
        raise ValueError(
            f"protected literals changed missing={dict(missing)!r}"
        )
    marker_re = re.compile(r"(?<!\\)(?:\*\*|__|~~)")
    if Counter(marker_re.findall(source)) != Counter(marker_re.findall(translated)):
        raise ValueError("Markdown emphasis markers changed")


def validate_russian_output(
    source: str, translated: str, protected: str, mode: str
) -> None:
    words = meaningful_english_words(protected)
    if words and not CYRILLIC_RE.search(translated) and (mode == "scalar" or len(words) > 1):
        raise ValueError(
            "translation appears to contain no Russian text; "
            f"English prose candidates={words[:8]!r}"
        )
    if (
        source.strip() == translated.strip()
        and words
        and (mode == "scalar" or len(words) > 1)
    ):
        raise ValueError("translation is identical to English source")
    if HAN_RE.search(translated):
        raise ValueError("Russian translation contains Han characters")
    if MIXED_SCRIPT_RE.search(translated):
        raise ValueError("Russian translation contains a mixed Latin/Cyrillic word")
    if re.search(r"&&|\)\s*&|&\s*\(", translated):
        raise ValueError("Russian translation contains suspicious generated punctuation")

    target_protected = RussianProtector().protect(translated)
    residual = meaningful_english_words(target_protected)
    function_words = sum(word.lower() in ENGLISH_FUNCTION_WORDS for word in residual)
    if len(residual) >= 6 and function_words >= 2:
        raise ValueError(
            "translation retains probable English prose: " + repr(residual[:12])
        )


def translate_text(
    source: str,
    *,
    component: str,
    model: str,
    cache: Cache,
    options: GenerationOptions,
    mode: str = "markdown",
) -> str:
    if not ASCII_WORD_RE.search(source):
        return source

    protector = RussianProtector()
    protected = protector.protect(source)
    if not meaningful_english_words(protected):
        return protector.restore(protected)

    instruction = system_prompt(component, source, mode)
    placeholders = re.findall(r"⟦P\d{4}⟧", protected)
    if placeholders:
        instruction += (
            "\nThe immutable placeholders, in order, are: " + ", ".join(placeholders)
        )
    else:
        instruction += "\nThis fragment has no placeholders; do not add any."
    prompt = f"{instruction}\n\nSOURCE FRAGMENT:\n{protected}"
    key = cache_key(model, component, mode, prompt, source, options)

    errors: list[str] = []
    cached = cache.get(key)
    if cached is not None:
        try:
            validate_fragment_structure(source, cached)
            validate_russian_output(source, cached, protected, mode)
            return cached
        except ValueError as exc:
            errors.append(f"cached translation: {exc}")

    attempt_prompt = prompt
    attempt_limit = 1 if os.environ.get("TRANSLATION_DEBUG") else options.retries
    for attempt in range(1, attempt_limit + 1):
        raw = ""
        try:
            raw = post_ollama(model, attempt_prompt, options)
            normalized = BASE.normalize_model_output(protected, raw)
            source_indent = re.match(r"^([ \t]+)(?=\S)", protected)
            if source_indent and normalized:
                indent = source_indent.group(1)
                normalized = indent + normalized.lstrip(" \t")
            normalized = normalize_brand_spelling(normalized)
            restored = protector.restore(normalized)
            if mode == "scalar":
                restored = restored.strip().strip('"').strip("'")
                if "\n" in restored:
                    raise ValueError("scalar translation contains a newline")
            validate_fragment_structure(source, restored)
            validate_russian_output(source, restored, protected, mode)
            cache.put(key, restored)
            return restored
        except (RuntimeError, ValueError) as exc:
            if os.environ.get("TRANSLATION_DEBUG"):
                print(f"debug attempt {attempt} raw output: {raw!r}", file=sys.stderr)
            errors.append(f"attempt {attempt}: {exc}")
            attempt_prompt = (
                prompt
                + "\n\nThe previous answer failed validation: "
                + str(exc)
                + ". Translate again without adding, deleting, reordering, or "
                + "duplicating any placeholder, literal, number, list item, or table cell."
            )
            if attempt < attempt_limit:
                time.sleep(min(attempt, 3))
    raise RuntimeError("; ".join(errors))


def translate_html_fragment(
    fragment: str,
    *,
    component: str,
    model: str,
    cache: Cache,
    options: GenerationOptions,
) -> str:
    """Translate visible raw-HTML prose while preserving preformatted text."""

    output: list[str] = []
    in_pre = False
    for line in fragment.splitlines(keepends=True):
        lower = line.lower()
        if in_pre or "<pre" in lower:
            output.append(line)
            if "</pre>" in lower:
                in_pre = False
            elif "<pre" in lower:
                in_pre = True
            continue
        content = line[:-1] if line.endswith("\n") else line
        newline = "\n" if line.endswith("\n") else ""
        leading_match = re.match(r"^[ \t]*", content)
        leading = leading_match.group(0) if leading_match else ""
        core = content[len(leading) :]
        visible = re.sub(r"</?[A-Za-z][^>\n]*>", "", core)
        if not ASCII_WORD_RE.search(visible):
            output.append(line)
            continue
        translated = translate_text(
            core + newline,
            component=component,
            model=model,
            cache=cache,
            options=options,
        )
        output.append(leading + translated)
    return "".join(output)


def translate_scalar_preserving_prefix(
    value: str,
    *,
    component: str,
    model: str,
    cache: Cache,
    options: GenerationOptions,
    fallback_model: str | None = None,
) -> str:
    number_match = re.match(r"^(\d+(?:\.\d+)*\.\s+)(.+)$", value)
    prefix, prose = number_match.groups() if number_match else ("", value)
    brand_names = "|".join(re.escape(name) for name in COMPONENT_DISPLAY_NAMES.values())
    brand_match = re.match(
        rf"^((?:{brand_names})(?:\s+[vV]?\d+(?:\.\d+){{1,3}})?\s+)(.+)$",
        prose,
    )
    if brand_match:
        brand_prefix, prose = brand_match.groups()
        prefix += brand_prefix
    if prose in NONTRANSLATABLE_SCALARS or re.fullmatch(
        r"[a-z][a-z0-9]*(?:[-_.][A-Za-z0-9]+)+", prose
    ):
        return prefix + prose
    try:
        translated = translate_text(
            prose,
            component=component,
            model=model,
            cache=cache,
            options=options,
            mode="scalar",
        )
    except RuntimeError:
        if not fallback_model or fallback_model == model:
            raise
        translated = translate_text(
            prose,
            component=component,
            model=fallback_model,
            cache=cache,
            options=options,
            mode="scalar",
        )
    return prefix + translated


def add_heading_anchors(body: str, source: Path) -> str:
    """Pin every translated heading to its rendered English Hugo ID."""

    lines = body.splitlines(keepends=True)
    flags = BASE.verbatim_ranges(lines)
    headings = [
        line
        for index, line in enumerate(lines)
        if not flags[index] and HEADING_RE.match(line.rstrip("\n"))
    ]
    if not headings:
        return body
    matches = [HEADING_RE.match(line.rstrip("\n")) for line in headings]
    if all(match and match.group("anchor") for match in matches):
        return body
    expected_levels = [len(match.group("marks")) for match in matches if match]
    heading_ids = BASE.rendered_heading_ids(source, expected_levels)
    if len(heading_ids) != len(headings):
        raise RuntimeError(
            f"cannot align rendered heading IDs for {source.relative_to(PROJECT)}: "
            f"source={len(headings)}, rendered={len(heading_ids)}. "
            "Run an English Hugo build before translating."
        )

    output: list[str] = []
    heading_index = 0
    for index, line in enumerate(lines):
        newline = "\n" if line.endswith("\n") else ""
        content = line[:-1] if newline else line
        match = None if flags[index] else HEADING_RE.match(content)
        if not match:
            output.append(line)
            continue
        anchor = match.group("anchor") or f" {{#{heading_ids[heading_index]}}}"
        output.append(
            f'{match.group("marks")}{match.group("space")}{match.group("title")}'
            f"{anchor}{newline}"
        )
        heading_index += 1
    return "".join(output)


def translate_front_matter(
    front: str,
    *,
    component: str,
    scalar_model: str,
    fallback_model: str,
    cache: Cache,
    options: GenerationOptions,
) -> str:
    lines = front.splitlines()
    output: list[str] = []
    scalar_re = re.compile(
        r"^(?P<indent>\s*)(?P<key>[A-Za-z][A-Za-z0-9_]*):\s*(?P<value>.*)$"
    )
    index = 0
    while index < len(lines):
        line = lines[index]
        match = scalar_re.match(line)
        if not match:
            output.append(line)
            index += 1
            continue
        indent = match.group("indent")
        key = match.group("key")
        raw = match.group("value")
        if key == "categories":
            localized = raw
            for english, russian in CATEGORY_MAP.items():
                localized = re.sub(rf"\b{english}\b", russian, localized)
            output.append(f"{indent}{key}: {localized}")
            index += 1
            continue
        if key not in TRANSLATABLE_META or not raw:
            output.append(line)
            index += 1
            continue

        if raw in {">", "|", ">-", "|-", ">+", "|+"}:
            block: list[str] = []
            next_index = index + 1
            parent_indent = len(indent.expandtabs(2))
            while next_index < len(lines):
                candidate = lines[next_index]
                candidate_indent = len(candidate) - len(candidate.lstrip(" \t"))
                if candidate.strip() and candidate_indent <= parent_indent:
                    break
                block.append(candidate)
                next_index += 1
            prose = " ".join(part.strip() for part in block if part.strip())
            if not prose:
                output.append(line)
                output.extend(block)
                index = next_index
                continue
            translated = translate_scalar_preserving_prefix(
                prose,
                component=component,
                model=scalar_model,
                cache=cache,
                options=options,
                fallback_model=fallback_model,
            )
            child_indent = re.match(r"^\s*", block[0]).group(0) if block else indent + "  "
            output.append(line)
            output.append(child_indent + translated)
            index = next_index
            continue

        quote = (
            raw[0]
            if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {'"', "'"}
            else ""
        )
        value = raw[1:-1] if quote else raw
        translated = translate_scalar_preserving_prefix(
            value,
            component=component,
            model=scalar_model,
            cache=cache,
            options=options,
            fallback_model=fallback_model,
        )
        output.append(f"{indent}{key}: {BASE.quote_yaml(translated, quote)}")
        index += 1
    return "\n".join(output)


def legal_verbatim_ranges(lines: list[str], flags: list[bool]) -> list[bool]:
    """Protect contiguous legal paragraphs in otherwise translatable pages."""

    result = list(flags)
    index = 0
    while index < len(lines):
        if result[index] or not LEGAL_START_RE.match(lines[index].strip()):
            index += 1
            continue
        while index < len(lines) and lines[index].strip():
            result[index] = True
            index += 1
    return result


def blockquoted_fence_ranges(lines: list[str], flags: list[bool]) -> list[bool]:
    """Protect fenced examples whose fence is nested inside a blockquote."""

    result = list(flags)
    index = 0
    opening_re = re.compile(r"^\s*>+\s*(`{3,}|~{3,})")
    while index < len(lines):
        opening = opening_re.match(lines[index])
        if not opening:
            index += 1
            continue
        marker = opening.group(1)
        result[index] = True
        index += 1
        closing_re = re.compile(rf"^\s*>+\s*{re.escape(marker)}\s*$")
        while index < len(lines):
            result[index] = True
            if closing_re.match(lines[index].rstrip("\n")):
                index += 1
                break
            index += 1
        else:
            raise RuntimeError("unterminated blockquoted Markdown fence")
    return result


def fragment_is_verbatim(fragment: str) -> bool:
    nonblank = [line for line in fragment.splitlines() if line.strip()]
    if not nonblank:
        return True
    first_line = nonblank[0].lstrip()
    quote_lines = [
        line.lstrip()[1:].strip()
        for line in fragment.splitlines()
        if line.lstrip().startswith(">")
    ]
    literal_quote = bool(quote_lines) and all(
        not content or re.fullmatch(r"`.*`", content) for content in quote_lines
    )
    literal_rule_item = len(nonblank) == 1 and bool(
        re.fullmatch(r"\s*-\s+\*\*-\s+[^*]+\*\*\s*", nonblank[0])
    )
    all_indented = all(line.startswith(("    ", "\t")) for line in nonblank)
    indented_code = all_indented and (
        any(
            re.match(
                r"^\s*(?:[$#>%]\s|\d{4}[-/]\d{2}[-/]\d{2}\b|[A-Za-z_][A-Za-z0-9_.-]*\s*(?:=|\{))",
                line,
            )
            for line in nonblank
        )
        or any(re.match(r"^\s*[{}]\s*$", line) for line in nonblank)
    )
    indented_table_output = all_indented and any(
        re.match(r"^\s*(?:\+[-+]|\+\s+Citus cluster:|\||[^\s]+@[^:]+:.*\$)", line)
        for line in nonblank
    )
    raw_config = bool(RAW_CONFIG_PREFIX_RE.match(first_line))
    return bool(
        indented_code
        or indented_table_output
        or literal_rule_item
        or raw_config
        or literal_quote
        or RAW_OUTPUT_RE.search(fragment)
    )


def translate_body(
    body: str,
    *,
    component: str,
    model: str,
    scalar_model: str,
    cache: Cache,
    options: GenerationOptions,
    max_chars: int,
) -> str:
    lines = body.splitlines(keepends=True)
    flags = BASE.verbatim_ranges(lines)
    flags = blockquoted_fence_ranges(lines, flags)
    flags = legal_verbatim_ranges(lines, flags)
    output: list[str] = []
    buffer: list[str] = []
    buffer_size = 0

    def flush() -> None:
        nonlocal buffer, buffer_size
        if not buffer:
            return
        fragment = "".join(buffer)
        if fragment_is_verbatim(fragment):
            output.append(fragment)
        elif HTML_PROSE_RE.search(fragment):
            output.append(
                translate_html_fragment(
                    fragment,
                    component=component,
                    model=model,
                    cache=cache,
                    options=options,
                )
            )
        else:
            output.append(
                translate_text(
                    fragment,
                    component=component,
                    model=model,
                    cache=cache,
                    options=options,
                )
            )
        buffer = []
        buffer_size = 0

    for index, line in enumerate(lines):
        if flags[index]:
            flush()
            output.append(line)
            continue
        newline = "\n" if line.endswith("\n") else ""
        content = line[:-1] if newline else line
        list_boundary = re.match(r"^\s*(?:[-+*]|\d{1,3}[.)])\s+", content)
        buffered_list = any(
            re.match(r"^\s*(?:[-+*]|\d{1,3}[.)])\s+", candidate)
            for candidate in buffer
        )
        if buffer and list_boundary and (
            buffer_size >= max_chars or (max_chars <= 700 and buffered_list)
        ):
            # Long option/reference lists often have no blank lines.  Split at
            # an item boundary so each item keeps its indentation while the
            # model sees a manageable number of protected literals.  The
            # low-limit mode intentionally isolates every item for difficult
            # option matrices with many technical placeholders.
            flush()
        italic_heading = re.match(r"^(\s*)\*(?!\s)(.+)\*\s*$", content)
        if italic_heading:
            flush()
            translated_italic = translate_scalar_preserving_prefix(
                italic_heading.group(2),
                component=component,
                model=scalar_model,
                cache=cache,
                options=options,
                fallback_model=model,
            )
            output.append(f"{italic_heading.group(1)}*{translated_italic}*{newline}")
            continue
        heading = HEADING_RE.match(content)
        if heading:
            flush()
            translated_title = translate_scalar_preserving_prefix(
                heading.group("title"),
                component=component,
                model=scalar_model,
                cache=cache,
                options=options,
                fallback_model=model,
            )
            output.append(
                f'{heading.group("marks")}{heading.group("space")}{translated_title}'
                f'{heading.group("anchor") or ""}{newline}'
            )
            continue
        if not line.strip():
            buffer.append(line)
            flush()
            continue
        # Do not split raw HTML constructs, whose <pre> state may span lines.
        if (
            buffer
            and buffer_size + len(line) > max_chars
            and not HTML_PROSE_RE.search("".join(buffer))
        ):
            flush()
        buffer.append(line)
        buffer_size += len(line)
    flush()
    return localize_internal_links("".join(output))


def localize_internal_links(document: str) -> str:
    """Prefix Russian documentation routes without changing shared assets."""

    route_names = tuple(f"docs/{name}" for name in SUPPORTED_COMPONENTS) + ("attribution", "search")
    routes = "|".join(re.escape(route) for route in route_names)
    pattern = re.compile(
        rf"(?<![A-Za-z0-9_:/])/(?P<route>{routes})(?P<tail>/|(?=[#?)\"']))"
    )
    asset_re = re.compile(
        rf"/ru/(?P<route>{routes})/(?P<asset>[^\s)>'\"]+\."
        r"(?:png|jpe?g|gif|webp|avif|svg|ico|pdf|zip|tar|gz|json|txt|csv|"
        r"ya?ml|toml|ini|conf))",
        flags=re.IGNORECASE,
    )
    lines = document.splitlines(keepends=True)
    indented_flags = [False] * len(lines)
    index = 0
    while index < len(lines):
        previous_blank = index == 0 or not lines[index - 1].strip()
        nested_list = re.match(
            r"^\s*(?:[-+*]|\d{1,3}[.)])\s+", lines[index]
        )
        if (
            not previous_blank
            or not lines[index].startswith(("    ", "\t"))
            or nested_list
        ):
            index += 1
            continue
        while index < len(lines) and (
            not lines[index].strip() or lines[index].startswith(("    ", "\t"))
        ):
            indented_flags[index] = True
            index += 1

    output: list[str] = []
    fence_marker = ""
    in_comment = False
    in_pre = False
    inline_literal_re = re.compile(
        r"(`+[^`\n]*`+|<(?:code|kbd)\b[^>\n]*>.*?</(?:code|kbd)>)",
        flags=re.IGNORECASE,
    )
    for index, line in enumerate(lines):
        stripped = line.rstrip("\n")
        if fence_marker:
            output.append(line)
            if stripped.lstrip().startswith(fence_marker):
                fence_marker = ""
            continue
        fence = FENCE_RE.match(stripped)
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
        lower = line.lower()
        if in_pre or "<pre" in lower:
            output.append(line)
            if "</pre>" in lower:
                in_pre = False
            elif "<pre" in lower:
                in_pre = True
            continue
        if indented_flags[index]:
            output.append(line)
            continue
        parts = inline_literal_re.split(line)
        for part_index in range(0, len(parts), 2):
            parts[part_index] = pattern.sub(
                lambda match: f'/ru/{match.group("route")}{match.group("tail")}',
                parts[part_index],
            )
            parts[part_index] = asset_re.sub(
                lambda match: f'/{match.group("route")}/{match.group("asset")}',
                parts[part_index],
            )
        output.append("".join(parts))
    return "".join(output)


def normalize_localized_routes(document: str) -> str:
    """Reverse localized routes for source/target structural comparison."""

    routes = "|".join(
        re.escape(route) for route in tuple(f"docs/{name}" for name in SUPPORTED_COMPONENTS) + ("attribution", "search")
    )
    pattern = re.compile(rf"/ru/(?P<route>{routes})(?=/|[#?)\"'])")
    # Reuse the same literal-awareness as localization by temporarily swapping
    # the forward route marker for a sentinel that the localizer cannot match.
    sentinel = "\ue100RU_ROUTE\ue101"
    protected = pattern.sub(lambda match: sentinel + match.group("route"), document)
    # The sentinel replacement above is intentionally global; restore routes
    # inside literals before normalizing prose so code remains byte-for-byte.
    lines = protected.splitlines(keepends=True)
    original_lines = document.splitlines(keepends=True)
    output: list[str] = []
    fence_marker = ""
    in_comment = False
    in_pre = False
    inline_literal_re = re.compile(
        r"(`+[^`\n]*`+|<(?:code|kbd)\b[^>\n]*>.*?</(?:code|kbd)>)",
        flags=re.IGNORECASE,
    )
    indented_flags = [False] * len(lines)
    index = 0
    while index < len(lines):
        previous_blank = index == 0 or not lines[index - 1].strip()
        if not previous_blank or not lines[index].startswith(("    ", "\t")):
            index += 1
            continue
        while index < len(lines) and (
            not lines[index].strip() or lines[index].startswith(("    ", "\t"))
        ):
            indented_flags[index] = True
            index += 1
    for index, (line, original) in enumerate(zip(lines, original_lines, strict=True)):
        stripped = original.rstrip("\n")
        if fence_marker:
            output.append(original)
            if stripped.lstrip().startswith(fence_marker):
                fence_marker = ""
            continue
        fence = FENCE_RE.match(stripped)
        if fence:
            fence_marker = fence.group(1)
            output.append(original)
            continue
        if in_comment:
            output.append(original)
            if "-->" in original:
                in_comment = False
            continue
        if "<!--" in original:
            output.append(original)
            if "-->" not in original:
                in_comment = True
            continue
        lower = original.lower()
        if in_pre or "<pre" in lower:
            output.append(original)
            if "</pre>" in lower:
                in_pre = False
            elif "<pre" in lower:
                in_pre = True
            continue
        if indented_flags[index]:
            output.append(original)
            continue
        parts = inline_literal_re.split(line)
        for part_index in range(1, len(parts), 2):
            # Inline literals are copied from the original rather than reverse
            # localized, matching localize_internal_links() exactly.
            original_parts = inline_literal_re.split(original)
            if part_index < len(original_parts):
                parts[part_index] = original_parts[part_index]
        output.append(
            "".join(parts).replace(sentinel, "/")
        )
    return "".join(output)


def parse_fenced_blocks(body: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    marker = ""
    for line in body.splitlines(keepends=True):
        if marker:
            current.append(line)
            if line.lstrip().startswith(marker):
                blocks.append("".join(current))
                current = []
                marker = ""
            continue
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            current = [line]
    if marker:
        raise RuntimeError("unterminated Markdown fence")
    return blocks


def parse_blockquoted_fenced_blocks(body: str) -> list[str]:
    lines = body.splitlines(keepends=True)
    blocks: list[str] = []
    index = 0
    opening_re = re.compile(r"^\s*>+\s*(`{3,}|~{3,})")
    while index < len(lines):
        opening = opening_re.match(lines[index])
        if not opening:
            index += 1
            continue
        marker = opening.group(1)
        block = [lines[index]]
        index += 1
        closing_re = re.compile(rf"^\s*>+\s*{re.escape(marker)}\s*$")
        while index < len(lines):
            block.append(lines[index])
            if closing_re.match(lines[index].rstrip("\n")):
                index += 1
                break
            index += 1
        else:
            raise RuntimeError("unterminated blockquoted Markdown fence")
        blocks.append("".join(block))
    return blocks


def indented_code_blocks(body: str) -> list[str]:
    """Extract top-level indented code introduced after a blank line."""

    lines = body.splitlines(keepends=True)
    blocks: list[str] = []
    index = 0
    while index < len(lines):
        previous_blank = index == 0 or not lines[index - 1].strip()
        if not previous_blank or not lines[index].startswith(("    ", "\t")):
            index += 1
            continue
        block: list[str] = []
        while index < len(lines) and (
            not lines[index].strip() or lines[index].startswith(("    ", "\t"))
        ):
            block.append(lines[index])
            index += 1
        if any(
            re.match(r"^\s*(?:[-+*]|\d{1,3}[.)])\s+", line)
            for line in block
            if line.strip()
        ):
            continue
        candidate = "".join(block).rstrip("\n") + "\n"
        if not fragment_is_verbatim(candidate):
            continue
        blocks.append(candidate)
    return blocks


def link_targets(body: str) -> list[str]:
    prose = body
    for block in parse_fenced_blocks(body):
        prose = prose.replace(block, "")
    targets: list[str] = []
    targets.extend(re.findall(r"(?<=[^!])\]\(([^)\n]+)\)", " " + prose))
    targets.extend(re.findall(r"!\[[^]]*\]\(([^)\n]+)\)", prose))
    targets.extend(
        match.group(1)
        for line in prose.splitlines()
        if (match := re.match(r"^\s*\[[^]]+\]:\s+(\S+)", line))
    )
    targets.extend(re.findall(r'\b(?:href|src|link)=["\']([^"\']+)["\']', prose))
    return targets


def heading_signature(body: str) -> list[tuple[str, str | None]]:
    lines = body.splitlines(keepends=True)
    flags = BASE.verbatim_ranges(lines)
    rows: list[tuple[str, str | None]] = []
    for index, line in enumerate(lines):
        if flags[index]:
            continue
        match = HEADING_RE.match(line.rstrip("\n"))
        if match:
            anchor = match.group("anchor")
            rows.append((match.group("marks"), anchor.strip() if anchor else None))
    return rows


def mask_translatable_front_matter(front: str) -> str:
    lines = front.splitlines()
    output: list[str] = []
    scalar_re = re.compile(
        r"^(?P<indent>\s*)(?P<key>[A-Za-z][A-Za-z0-9_]*):\s*(?P<value>.*)$"
    )
    index = 0
    while index < len(lines):
        line = lines[index]
        match = scalar_re.match(line)
        if not match or match.group("key") not in TRANSLATABLE_META | {"categories"}:
            output.append(line)
            index += 1
            continue
        output.append(f'{match.group("indent")}{match.group("key")}: <localized>')
        if match.group("value") in {">", "|", ">-", "|-", ">+", "|+"}:
            parent_indent = len(match.group("indent").expandtabs(2))
            index += 1
            while index < len(lines):
                candidate = lines[index]
                candidate_indent = len(candidate) - len(candidate.lstrip(" \t"))
                if candidate.strip() and candidate_indent <= parent_indent:
                    break
                index += 1
            continue
        index += 1
    return "\n".join(output)


def legal_fragments(body: str) -> list[str]:
    lines = body.splitlines(keepends=True)
    fragments: list[str] = []
    index = 0
    while index < len(lines):
        if not LEGAL_START_RE.match(lines[index].strip()):
            index += 1
            continue
        paragraph: list[str] = []
        while index < len(lines) and lines[index].strip():
            paragraph.append(lines[index])
            index += 1
        fragments.append("".join(paragraph))
    return fragments


def validate_pair(
    source_text: str,
    translated_text: str,
    source: Path,
    anchored_source_body: str,
) -> None:
    source_front, _ = BASE.split_front_matter(source_text)
    target_front, target_body = BASE.split_front_matter(translated_text)
    if mask_translatable_front_matter(source_front) != mask_translatable_front_matter(
        target_front
    ):
        raise RuntimeError("immutable YAML front matter changed")

    normalized_target = normalize_localized_routes(target_body)
    if parse_fenced_blocks(anchored_source_body) != parse_fenced_blocks(normalized_target):
        raise RuntimeError("fenced code blocks changed")
    if parse_blockquoted_fenced_blocks(
        anchored_source_body
    ) != parse_blockquoted_fenced_blocks(normalized_target):
        raise RuntimeError("blockquoted fenced code blocks changed")
    if indented_code_blocks(anchored_source_body) != indented_code_blocks(
        normalized_target
    ):
        raise RuntimeError("indented code blocks changed")
    if re.findall(r"<!--.*?-->", anchored_source_body, flags=re.DOTALL) != re.findall(
        r"<!--.*?-->", normalized_target, flags=re.DOTALL
    ):
        raise RuntimeError("HTML comments changed")
    if heading_signature(anchored_source_body) != heading_signature(normalized_target):
        raise RuntimeError("heading levels or anchors changed")
    if link_targets(anchored_source_body) != link_targets(normalized_target):
        raise RuntimeError("link targets changed")
    if legal_fragments(anchored_source_body) != legal_fragments(normalized_target):
        raise RuntimeError("legal text changed")
    try:
        validate_fragment_structure(anchored_source_body, normalized_target)
    except ValueError as exc:
        raise RuntimeError(f"document structure changed: {exc}") from exc

    source_refs = [
        line for line in anchored_source_body.splitlines() if REFERENCE_DEF_RE.match(line)
    ]
    target_refs = [
        line for line in normalized_target.splitlines() if REFERENCE_DEF_RE.match(line)
    ]
    if source_refs != target_refs:
        raise RuntimeError("reference definitions changed")

    target_path = source.with_name(source.name.removesuffix(".md") + ".ru.md")
    if target_path.name.endswith(".zh.md"):
        raise RuntimeError("refusing to construct a Chinese target")


def translate_file(
    source: Path,
    *,
    component: str,
    model: str,
    scalar_model: str,
    cache: Cache,
    options: GenerationOptions,
    max_chars: int,
    force: bool,
    dry_run: bool,
) -> Path:
    target = source.with_name(source.name.removesuffix(".md") + ".ru.md")
    if target.exists() and not force:
        print(f"skip existing {target.relative_to(PROJECT)}", flush=True)
        return target
    source_text = source.read_text(encoding="utf-8")
    front, body = BASE.split_front_matter(source_text)
    anchored_body = add_heading_anchors(body, source)
    translated_front = translate_front_matter(
        front,
        component=component,
        scalar_model=scalar_model,
        fallback_model=model,
        cache=cache,
        options=options,
    )
    translated_body = translate_body(
        anchored_body,
        component=component,
        model=model,
        scalar_model=scalar_model,
        cache=cache,
        options=options,
        max_chars=max_chars,
    )
    translated_text = f"---\n{translated_front}\n---\n{translated_body}"
    validate_pair(source_text, translated_text, source, anchored_body)
    if dry_run:
        print(f"<!-- dry-run target: {target.relative_to(PROJECT)} -->")
        print(translated_text)
        return target

    temporary = target.with_name(f".{target.name}.tmp-{os.getpid()}")
    try:
        temporary.write_text(translated_text, encoding="utf-8")
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    print(f"wrote {target.relative_to(PROJECT)}", flush=True)
    return target


def source_component(path: Path) -> str:
    try:
        relative = path.resolve().relative_to(CONTENT.resolve())
    except ValueError as exc:
        raise RuntimeError(f"source is outside content/docs/: {path}") from exc
    if not relative.parts or relative.parts[0] not in SUPPORTED_COMPONENTS:
        raise RuntimeError(f"source is outside the six component collections: {path}")
    return relative.parts[0]


def is_english_source(path: Path) -> bool:
    return path.suffix == ".md" and not LANGUAGE_SUFFIX_RE.search(path.name)


def discover_sources(component: str, requested: list[str]) -> list[Path]:
    if requested:
        sources: list[Path] = []
        for value in requested:
            path = Path(value)
            if not path.is_absolute():
                path = PROJECT / path
            path = path.resolve()
            if not path.is_file():
                raise RuntimeError(f"source does not exist: {value}")
            if not is_english_source(path):
                raise RuntimeError(f"not an English Markdown source: {value}")
            detected = source_component(path)
            if component != "all" and detected != component:
                raise RuntimeError(
                    f"source belongs to {detected}, not requested component {component}: {value}"
                )
            sources.append(path)
        return sorted(set(sources))

    components = SUPPORTED_COMPONENTS if component == "all" else (component,)
    sources = [
        path.resolve()
        for selected in components
        for path in (CONTENT / selected).rglob("*.md")
        if is_english_source(path)
    ]
    order = {name: index for index, name in enumerate(SUPPORTED_COMPONENTS)}
    return sorted(
        sources,
        key=lambda path: (order[source_component(path)], path.stat().st_size, str(path)),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Translate English component Markdown to validated *.ru.md pages."
    )
    parser.add_argument("component", choices=SUPPORTED_COMPONENTS + ("all",))
    parser.add_argument(
        "paths",
        nargs="*",
        help="optional English Markdown paths inside the selected component",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--scalar-model", default=DEFAULT_SCALAR_MODEL)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--endpoint", default=default_endpoint())
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--repeat-penalty", type=float, default=1.0)
    parser.add_argument("--num-ctx", type=int, default=32768)
    parser.add_argument("--num-predict", type=int, default=8192)
    parser.add_argument("--keep-alive", default="30m")
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--max-chars", type=int, default=5000)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list-sources", action="store_true")
    parser.add_argument("--limit", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not STYLE_GUIDE.is_file():
        raise RuntimeError(f"missing Russian translation guide: {STYLE_GUIDE}")
    if args.max_chars < 500:
        raise RuntimeError("--max-chars must be at least 500")
    if args.retries < 1:
        raise RuntimeError("--retries must be at least 1")
    if args.timeout < 1 or args.num_ctx < 1 or args.num_predict < 1:
        raise RuntimeError("timeout and model token limits must be positive")
    sources = discover_sources(args.component, args.paths)
    if args.limit is not None:
        if args.limit < 0:
            raise RuntimeError("--limit cannot be negative")
        sources = sources[: args.limit]
    if args.list_sources:
        for source in sources:
            target = source.with_name(source.name.removesuffix(".md") + ".ru.md")
            print(f"{source.relative_to(PROJECT)} -> {target.relative_to(PROJECT)}")
        return 0

    options = GenerationOptions(
        endpoint=args.endpoint,
        timeout=args.timeout,
        temperature=args.temperature,
        top_p=args.top_p,
        repeat_penalty=args.repeat_penalty,
        num_ctx=args.num_ctx,
        num_predict=args.num_predict,
        keep_alive=args.keep_alive,
        retries=args.retries,
    )
    cache = Cache.load(args.cache)
    print(
        f"translating {len(sources)} files for {args.component} with {args.model}; "
        f"scalar model={args.scalar_model}; cache entries={len(cache.entries)}",
        flush=True,
    )
    for index, source in enumerate(sources, 1):
        component = source_component(source)
        print(f"[{index}/{len(sources)}] {source.relative_to(PROJECT)}", flush=True)
        translate_file(
            source,
            component=component,
            model=args.model,
            scalar_model=args.scalar_model,
            cache=cache,
            options=options,
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
    except Exception as exc:  # Fail closed; partial targets are never renamed.
        print(f"Russian translation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
