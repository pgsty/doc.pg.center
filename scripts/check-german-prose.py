#!/usr/bin/env python3
"""Find probable untranslated English prose in German Markdown pages.

This is deliberately a conservative lint, not a language detector.  It scans
visible prose, compares it with the sibling English source when available, and
requires grammatical evidence before reporting a line.  Literal material that
is expected to remain in English (code, commands, diagnostics, and original
licence text) is excluded.

With no arguments, every ``*.de.md`` file below ``content`` is checked.  Files
and directories may be supplied explicitly::

    scripts/check-german-prose.py
    scripts/check-german-prose.py content/pgbouncer content/search.de.md

Exit status is 1 when findings are reported, 2 for invalid input/read errors,
and 0 otherwise.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content"

TRANSLATABLE_FRONT_MATTER = frozenset(
    {"title", "linkTitle", "description", "categories"}
)

FENCE_OPEN_RE = re.compile(r"^\s*(?P<run>`{3,}|~{3,})(?:[^\r\n]*)$")
FRONT_KEY_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):(?P<value>.*)$")
REFERENCE_DEFINITION_RE = re.compile(
    r"^ {0,3}\[[^\]\n]+\]:[ \t]*(?:\S+|$)", re.IGNORECASE
)
SHORTCODE_RE = re.compile(r"\{\{[<%].*?[>%]\}\}")
HTML_TAG_RE = re.compile(r"</?[A-Za-z][A-Za-z0-9:-]*(?:\s[^<>]*?)?/?>")
RAW_URL_RE = re.compile(
    r"(?:(?:https?|ftp)://|mailto:|www\.)[^\s<>\])}]+", re.IGNORECASE
)
AUTOLINK_RE = re.compile(r"<(?:https?://|ftp://|mailto:)[^<>]+>", re.IGNORECASE)
HEADING_ATTRIBUTE_RE = re.compile(r"[ \t]*\{[^{}]*#[^{}]+\}[ \t]*$")
WORD_RE = re.compile(r"[A-Za-z\u00c0-\u024f]+(?:['\u2019][A-Za-z\u00c0-\u024f]+)?")

# Words shared by English and German (notably "in", "an", "was", and
# "will") are intentionally absent.  They are weak language evidence.
ENGLISH_FUNCTION_WORDS = frozenset(
    {
        "a",
        "about",
        "above",
        "after",
        "all",
        "although",
        "among",
        "and",
        "any",
        "are",
        "as",
        "at",
        "because",
        "been",
        "before",
        "being",
        "below",
        "between",
        "both",
        "but",
        "by",
        "can",
        "cannot",
        "could",
        "did",
        "do",
        "does",
        "each",
        "either",
        "else",
        "even",
        "every",
        "for",
        "from",
        "had",
        "has",
        "have",
        "he",
        "her",
        "here",
        "hers",
        "him",
        "his",
        "how",
        "if",
        "into",
        "is",
        "it",
        "its",
        "itself",
        "may",
        "might",
        "must",
        "neither",
        "no",
        "nor",
        "not",
        "of",
        "on",
        "only",
        "onto",
        "or",
        "our",
        "ours",
        "over",
        "shall",
        "she",
        "should",
        "since",
        "some",
        "such",
        "than",
        "that",
        "the",
        "their",
        "theirs",
        "them",
        "themselves",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "through",
        "thus",
        "to",
        "under",
        "until",
        "up",
        "upon",
        "us",
        "we",
        "were",
        "what",
        "when",
        "where",
        "whether",
        "which",
        "while",
        "who",
        "whom",
        "whose",
        "why",
        "with",
        "without",
        "would",
        "you",
        "your",
        "yours",
    }
)

GERMAN_FUNCTION_WORDS = frozenset(
    {
        "aber",
        "alle",
        "allem",
        "allen",
        "aller",
        "alles",
        "als",
        "also",
        "am",
        "an",
        "auch",
        "auf",
        "aus",
        "bei",
        "beim",
        "beide",
        "beiden",
        "beziehungsweise",
        "bis",
        "da",
        "dabei",
        "dadurch",
        "damit",
        "dann",
        "das",
        "dass",
        "dem",
        "den",
        "denn",
        "der",
        "des",
        "deshalb",
        "die",
        "dies",
        "diese",
        "diesem",
        "diesen",
        "dieser",
        "dieses",
        "doch",
        "durch",
        "dürfen",
        "ein",
        "eine",
        "einem",
        "einen",
        "einer",
        "eines",
        "entweder",
        "er",
        "es",
        "für",
        "gegen",
        "hat",
        "haben",
        "hinter",
        "ich",
        "ihm",
        "ihn",
        "ihnen",
        "ihr",
        "ihre",
        "ihrem",
        "ihren",
        "ihrer",
        "ihres",
        "im",
        "in",
        "indem",
        "ins",
        "ist",
        "jede",
        "jedem",
        "jeden",
        "jeder",
        "jedes",
        "jedoch",
        "kann",
        "kein",
        "keine",
        "keinem",
        "keinen",
        "keiner",
        "keines",
        "können",
        "man",
        "mehr",
        "mein",
        "mit",
        "muss",
        "müssen",
        "nach",
        "neben",
        "nicht",
        "noch",
        "nur",
        "ob",
        "oder",
        "ohne",
        "sein",
        "seine",
        "seinem",
        "seinen",
        "seiner",
        "seines",
        "seit",
        "selbst",
        "sich",
        "sie",
        "sind",
        "so",
        "sobald",
        "sodass",
        "sollen",
        "sondern",
        "sowie",
        "über",
        "um",
        "und",
        "unter",
        "uns",
        "unser",
        "vom",
        "von",
        "vor",
        "war",
        "waren",
        "weil",
        "welche",
        "welchem",
        "welchen",
        "welcher",
        "welches",
        "wenn",
        "werden",
        "wie",
        "wird",
        "wo",
        "wurde",
        "wurden",
        "zu",
        "zum",
        "zur",
        "zwischen",
    }
)

ENGLISH_BIGRAMS = frozenset(
    {
        ("as", "a"),
        ("as", "the"),
        ("at", "the"),
        ("by", "the"),
        ("can", "be"),
        ("could", "be"),
        ("does", "not"),
        ("for", "a"),
        ("for", "the"),
        ("from", "the"),
        ("has", "been"),
        ("have", "been"),
        ("in", "a"),
        ("in", "the"),
        ("is", "a"),
        ("is", "not"),
        ("of", "a"),
        ("of", "the"),
        ("on", "the"),
        ("should", "be"),
        ("that", "the"),
        ("the", "following"),
        ("there", "is"),
        ("this", "is"),
        ("to", "a"),
        ("to", "be"),
        ("to", "the"),
        ("will", "be"),
        ("with", "a"),
        ("with", "the"),
        ("would", "be"),
    }
)

# These words help catch unchanged English headings that naturally contain few
# function words.  Two cues are required unless ordinary English grammar is
# present, keeping product and protocol names quiet.
ENGLISH_DOCUMENT_CUES = frozenset(
    {
        "advanced",
        "asked",
        "authentication",
        "architecture",
        "command",
        "commands",
        "configuration",
        "configuring",
        "download",
        "example",
        "examples",
        "faq",
        "features",
        "format",
        "formats",
        "frequently",
        "getting",
        "guide",
        "guides",
        "installation",
        "installing",
        "introduction",
        "logging",
        "monitoring",
        "options",
        "output",
        "overview",
        "parallel",
        "processing",
        "question",
        "questions",
        "reference",
        "release",
        "releases",
        "report",
        "reports",
        "requirement",
        "requirements",
        "sample",
        "samples",
        "setup",
        "started",
        "support",
        "task",
        "tasks",
        "troubleshooting",
        "usage",
    }
)

LEGAL_FILE_PARTS = frozenset(
    {"copying", "copyright", "legal", "licence", "license", "notice"}
)
LEGAL_STRONG_RE = re.compile(
    r"\b(?:"
    r"all rights reserved|as is|copyright \(c\)|in no event shall|"
    r"permission (?:is hereby granted|to use)|redistribution and use|"
    r"the software (?:is provided|provided hereunder)|"
    r"without (?:fee|a written agreement)|"
    r"warrant(?:y|ies) of merchantability"
    r")\b",
    re.IGNORECASE,
)
LEGAL_TERMS_RE = re.compile(
    r"\b(?:copyright|damages|disclaims?|fitness|hereby|liable|liability|"
    r"licen[cs]e[ds]?|merchantability|permission|redistribut(?:e|ion)|"
    r"warrant(?:y|ies))\b",
    re.IGNORECASE,
)

LOG_OR_ERROR_RE = re.compile(
    r"^(?:"
    r"(?:DEBUG|DETAIL|ERROR|FATAL|HINT|INFO|LOG|NOTICE|PANIC|TRACE|WARNING|WARN)"
    r"(?:\[[^]]+\])?\s*[:\-]|"
    r"(?:error|exception|failure|fatal|panic|warning)\s*[:\-]|"
    r"(?:cannot|could not|no such|unable to)\b|"
    r"traceback \(most recent call last\)"
    r")",
    re.IGNORECASE,
)
TIMESTAMPED_LOG_RE = re.compile(
    r"^(?:\d{4}-\d{2}-\d{2}[ T]|\d{2}:\d{2}:\d{2}(?:[.,]\d+)?)"
    r".*\b(?:DEBUG|ERROR|FATAL|INFO|LOG|PANIC|WARN(?:ING)?)\b",
    re.IGNORECASE,
)
CLI_OPTION_RE = re.compile(r"^-{1,2}[A-Za-z0-9][A-Za-z0-9_-]*(?:\s*\||\s|$)")
PROMPT_RE = re.compile(r"^(?:\$|>>>|\.\.\.|[A-Za-z0-9_.@:/~-]+[$#])\s+\S")
ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*\s*(?::=|=)\s*\S")
SQL_LITERAL_RE = re.compile(
    r"^(?:ALTER|BEGIN|CALL|COMMIT|COPY|CREATE|DELETE|DROP|GRANT|INSERT|"
    r"REINDEX|REVOKE|ROLLBACK|SELECT|SET|SHOW|TRUNCATE|UPDATE|VACUUM)\b"
)


@dataclass(frozen=True)
class Candidate:
    line: int
    raw: str
    visible: str
    front_matter: bool = False


@dataclass(frozen=True)
class LanguageEvidence:
    words: tuple[str, ...]
    english: int
    german: int
    bigrams: int
    cues: int


@dataclass(frozen=True)
class SourceProfile:
    lines: frozenset[str]
    legal_lines: frozenset[str]


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    reason: str
    summary: str


def strip_inline_code(value: str) -> str:
    """Remove Markdown code spans without assuming a one-backtick delimiter."""
    output: list[str] = []
    position = 0
    while position < len(value):
        if value[position] != "`":
            output.append(value[position])
            position += 1
            continue
        end_of_run = position + 1
        while end_of_run < len(value) and value[end_of_run] == "`":
            end_of_run += 1
        delimiter = value[position:end_of_run]
        closing = value.find(delimiter, end_of_run)
        if closing < 0:
            # An unmatched backtick is punctuation, not permission to discard
            # the rest of a potentially untranslated sentence.
            output.append(delimiter)
            position = end_of_run
            continue
        output.append(" ")
        position = closing + len(delimiter)
    return "".join(output)


def remove_markdown_destinations(value: str) -> str:
    """Keep link labels while removing balanced inline-link destinations."""
    output: list[str] = []
    position = 0
    while True:
        start = value.find("](", position)
        if start < 0:
            output.append(value[position:])
            break
        output.append(value[position : start + 1])
        cursor = start + 2
        depth = 1
        escaped = False
        angle = False
        while cursor < len(value):
            character = value[cursor]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == "<" and depth == 1:
                angle = True
            elif character == ">" and angle:
                angle = False
            elif not angle and character == "(":
                depth += 1
            elif not angle and character == ")":
                depth -= 1
                if depth == 0:
                    break
            cursor += 1
        if depth:
            # Malformed Markdown: keep the label and discard only the obvious
            # destination prefix so a URL cannot dominate language evidence.
            output.append(value[start + 1 :])
            break
        position = cursor + 1
    return "".join(output)


def clean_visible_text(value: str) -> str:
    """Reduce one Markdown line to user-visible prose for language scoring."""
    value = SHORTCODE_RE.sub(" ", value)
    value = strip_inline_code(value)
    value = AUTOLINK_RE.sub(" ", value)
    value = remove_markdown_destinations(value)
    value = re.sub(r"!?\[([^]\n]*)\]\[[^]\n]*\]", r"\1", value)
    value = RAW_URL_RE.sub(" ", value)
    value = HTML_TAG_RE.sub(" ", value)
    value = HEADING_ATTRIBUTE_RE.sub("", value)

    # Remove blockquote, heading, list, and checkbox syntax.  Repeat the quote
    # removal because nested blockquotes are common in imported manuals.
    value = re.sub(r"^\s*(?:>\s*)+", "", value)
    value = re.sub(r"^\s{0,3}#{1,6}(?:\s+|$)", "", value)
    value = re.sub(r"^\s{0,3}(?:[-+*]|\d{1,3}[.)])\s+", "", value)
    value = re.sub(r"^\s*\[[ xX]\]\s+", "", value)
    value = re.sub(r"\s+#+\s*$", "", value)

    value = html.unescape(value)
    value = re.sub(r"[*_~]", " ", value)
    value = re.sub(r"\\([\\`*{}\[\]()#+.!|>-])", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(' \t\r\n|"')


def normalize_visible(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"\s+", " ", value).strip()


def without_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """Remove comments from a line while preserving prose on either side."""
    output: list[str] = []
    position = 0
    while position < len(line):
        if in_comment:
            closing = line.find("-->", position)
            if closing < 0:
                return "".join(output), True
            position = closing + 3
            in_comment = False
            continue
        opening = line.find("<!--", position)
        if opening < 0:
            output.append(line[position:])
            break
        output.append(line[position:opening])
        position = opening + 4
        in_comment = True
    return "".join(output), in_comment


def without_raw_literal_html(line: str, raw_tag: str | None) -> tuple[str, str | None]:
    """Remove raw HTML code/pre/script/style blocks, including inline blocks."""
    output: list[str] = []
    position = 0
    while position < len(line):
        if raw_tag is not None:
            closing = re.search(rf"</{re.escape(raw_tag)}\s*>", line[position:], re.I)
            if closing is None:
                return "".join(output), raw_tag
            position += closing.end()
            raw_tag = None
            continue
        opening = re.search(r"<(pre|code|script|style)\b[^>]*>", line[position:], re.I)
        if opening is None:
            output.append(line[position:])
            break
        output.append(line[position : position + opening.start()])
        raw_tag = opening.group(1).casefold()
        position += opening.end()
    return "".join(output), raw_tag


def front_matter_end(lines: list[str]) -> int | None:
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return index
    return None


def candidate_lines(document: str) -> list[Candidate]:
    lines = document.splitlines()
    candidates: list[Candidate] = []
    end = front_matter_end(lines)

    if end is not None:
        active_key: str | None = None
        for index in range(1, end):
            line = lines[index]
            key_match = FRONT_KEY_RE.match(line)
            if key_match:
                active_key = key_match.group("key")
                if active_key not in TRANSLATABLE_FRONT_MATTER:
                    continue
                scalar = key_match.group("value").strip()
                if scalar in {"|", "|-", "|+", ">", ">-", ">+"}:
                    continue
                visible = clean_visible_text(scalar)
            elif active_key in TRANSLATABLE_FRONT_MATTER and line.startswith(
                (" ", "\t")
            ):
                visible = clean_visible_text(line.strip())
            else:
                continue
            if visible:
                candidates.append(Candidate(index + 1, line, visible, True))

    body_start = end + 1 if end is not None else 0
    fence_character = ""
    fence_length = 0
    in_comment = False
    raw_tag: str | None = None

    for index in range(body_start, len(lines)):
        raw = lines[index]
        if fence_character:
            if re.fullmatch(
                rf"\s*{re.escape(fence_character)}{{{fence_length},}}[ \t]*",
                raw,
            ):
                fence_character = ""
                fence_length = 0
            continue

        line, in_comment = without_html_comments(raw, in_comment)
        line, raw_tag = without_raw_literal_html(line, raw_tag)
        if not line.strip():
            continue

        # Fence markers inside comments or raw <pre>/<code> blocks are data,
        # not Markdown delimiters, so look for them only after those constructs
        # have been removed.
        fence = FENCE_OPEN_RE.match(line)
        if fence:
            run = fence.group("run")
            fence_character = run[0]
            fence_length = len(run)
            continue

        if REFERENCE_DEFINITION_RE.match(line):
            continue
        if re.fullmatch(r"\s*(?:[-*_]\s*){3,}", line):
            continue
        if re.fullmatch(r"\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*", line):
            continue

        visible = clean_visible_text(line)
        if visible:
            candidates.append(Candidate(index + 1, raw, visible))

    return candidates


def language_evidence(value: str) -> LanguageEvidence:
    words = tuple(word.casefold() for word in WORD_RE.findall(value))
    english = sum(word in ENGLISH_FUNCTION_WORDS for word in words)
    german = sum(word in GERMAN_FUNCTION_WORDS for word in words)
    bigrams = sum(pair in ENGLISH_BIGRAMS for pair in zip(words, words[1:]))
    cues = sum(word in ENGLISH_DOCUMENT_CUES for word in words)
    return LanguageEvidence(words, english, german, bigrams, cues)


def legalish_path(path: Path) -> bool:
    parts = {
        token
        for part in path.parts
        for token in re.split(r"[^a-z]+", part.casefold())
        if token
    }
    return bool(parts & LEGAL_FILE_PARTS)


def is_legal_original(value: str, path: Path) -> bool:
    if LEGAL_STRONG_RE.search(value):
        return True
    if not legalish_path(path):
        return False
    terms = {match.group(0).casefold() for match in LEGAL_TERMS_RE.finditer(value)}
    letters = [character for character in value if character.isalpha()]
    uppercase = sum(character.isupper() for character in letters)
    return len(terms) >= 3 or (
        bool(terms) and len(letters) >= 20 and uppercase / len(letters) >= 0.8
    )


def is_literal_line(candidate: Candidate) -> bool:
    """Recognize unfenced commands, log messages, and error output."""
    if candidate.front_matter:
        return False
    value = candidate.visible.strip()
    if not value:
        return True
    if candidate.raw.startswith(("    ", "\t")) and re.match(
        r"^\s*[A-Za-z0-9_./-]+\s+(?:--?[A-Za-z0-9]|-[A-Za-z])",
        candidate.raw,
    ):
        return True
    if CLI_OPTION_RE.match(value) or PROMPT_RE.match(value):
        return True
    if ASSIGNMENT_RE.match(value):
        return True
    if LOG_OR_ERROR_RE.match(value) or TIMESTAMPED_LOG_RE.match(value):
        return True
    if SQL_LITERAL_RE.match(value) and (
        value.endswith(";") or re.search(r"\b(?:FROM|INTO|TABLE|VALUES|WHERE)\b", value)
    ):
        return True
    if re.match(r"^(?:Usage|Synopsis):\s+\S", value, re.IGNORECASE):
        return True
    return False


def source_profile(path: Path) -> SourceProfile:
    english = path.with_name(path.name[: -len(".de.md")] + ".md")
    if not english.is_file():
        return SourceProfile(frozenset(), frozenset())
    document = english.read_text(encoding="utf-8")
    candidates = candidate_lines(document)
    lines = {
        normalize_visible(candidate.visible)
        for candidate in candidates
        if not is_literal_line(candidate)
    }

    legal_lines: set[str] = set()
    paragraph: list[Candidate] = []
    previous = -2

    def keep_legal_paragraph() -> None:
        if not paragraph:
            return
        combined = " ".join(item.visible for item in paragraph)
        if is_legal_original(combined, english):
            legal_lines.update(normalize_visible(item.visible) for item in paragraph)

    for candidate in candidates:
        if candidate.front_matter:
            continue
        if candidate.line != previous + 1:
            keep_legal_paragraph()
            paragraph = []
        paragraph.append(candidate)
        previous = candidate.line
    keep_legal_paragraph()

    return SourceProfile(frozenset(lines), frozenset(legal_lines))


def assess(candidate: Candidate, path: Path, source: SourceProfile) -> str | None:
    if is_literal_line(candidate):
        return None
    normalized = normalize_visible(candidate.visible)
    if not normalized or normalized in source.legal_lines:
        return None
    if is_legal_original(candidate.visible, path):
        return None

    evidence = language_evidence(candidate.visible)
    word_count = len(evidence.words)
    if word_count < 2:
        return None

    identical = normalized in source.lines
    if identical:
        grammatical = (
            word_count >= 5
            and evidence.english >= 2
            and evidence.english >= evidence.german + 1
        )
        heading_like = (
            word_count >= 2 and evidence.cues >= 2 and evidence.german == 0
        ) or (
            word_count >= 3
            and evidence.cues >= 1
            and evidence.english >= 1
            and evidence.english >= evidence.german
        )
        long_english = (
            word_count >= 9
            and evidence.english >= 2
            and evidence.bigrams >= 1
            and evidence.english >= evidence.german + 1
        )
        if grammatical or heading_like or long_english:
            return "identical-source"

    # Without exact-source support, insist on several independent signs of an
    # English clause.  German prose often contains English technical nouns;
    # nouns alone cannot satisfy these conditions.
    if (
        word_count >= 8
        and evidence.english >= 3
        and evidence.bigrams >= 1
        and evidence.english >= evidence.german + 2
    ):
        return "english-heavy"
    if word_count >= 8 and evidence.english >= 4 and evidence.german == 0:
        return "english-heavy"
    if (
        word_count >= 12
        and evidence.english >= 4
        and evidence.english >= evidence.german + 2
    ):
        return "english-heavy"
    return None


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PROJECT))
    except ValueError:
        return str(path)


def summary(value: str, limit: int = 180) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "\u2026"


def collect_files(arguments: list[str]) -> tuple[list[Path], list[str]]:
    inputs = [Path(argument) for argument in arguments] if arguments else [CONTENT]
    files: set[Path] = set()
    errors: list[str] = []
    for supplied in inputs:
        path = supplied if supplied.is_absolute() else Path.cwd() / supplied
        if path.is_dir():
            files.update(
                candidate.resolve()
                for candidate in path.rglob("*")
                if candidate.is_file() and candidate.name.casefold().endswith(".de.md")
            )
        elif path.is_file():
            if not path.name.casefold().endswith(".de.md"):
                errors.append(f"not a German Markdown page: {supplied}")
            else:
                files.add(path.resolve())
        else:
            errors.append(f"path does not exist: {supplied}")
    return sorted(files), errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        help="German Markdown files or directories (default: content)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files, errors = collect_files(args.paths)
    if not files and not errors:
        errors.append("no *.de.md files found")
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    for path in files:
        try:
            document = path.read_text(encoding="utf-8")
            profile = source_profile(path)
        except (OSError, UnicodeError) as exc:
            print(f"error: {display_path(path)}: {exc}", file=sys.stderr)
            return 2
        for candidate in candidate_lines(document):
            reason = assess(candidate, path, profile)
            if reason is not None:
                findings.append(
                    Finding(
                        path,
                        candidate.line,
                        reason,
                        summary(candidate.visible),
                    )
                )

    for finding in findings:
        print(
            f"{display_path(finding.path)}:{finding.line}: "
            f"[{finding.reason}] {finding.summary}"
        )
    if findings:
        print(
            f"Found {len(findings)} probable untranslated line(s) "
            f"in {len(files)} German file(s).",
            file=sys.stderr,
        )
        return 1

    print(
        f"No probable untranslated English prose found in {len(files)} German file(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
