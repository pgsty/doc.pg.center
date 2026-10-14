"""Check explicitly reviewed translations of prose stored in text fences.

HAProxy's imported manuals use some text fences for parameter explanations and
ASCII table labels, as well as for actual code and output. Only an exact,
reviewed source/translation pair may differ. All unregistered fences remain
byte-for-byte protected. The registry is source metadata, not a blanket waiver.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
REGISTRY = PROJECT / "data" / "translation-fences"
CLASSIFICATIONS = {"argument-description", "table-labels", "mixed-explanation", "explanation-label"}

# These five prose labels were imported as both inline code and haproxy fences.
# They are not command-line options, program output, or copyable configuration.
# Keep the exception tied to the exact source page and exact bilingual wording.
PROSE_LABELS = {
    "haproxy/configuration-basics.md": {
        "#    hash as a comment start": "#    Raute als Kommentarbeginn",
    },
    "haproxy/starting.md": {
        "- the version": "- die Version",
        "- the release date": "- das Veröffentlichungsdatum",
        "- build options": "- Build-Optionen",
        "- libraries versions": "- Bibliotheksversionen",
        "- Available polling systems will affect the process's scalability when":
            "- Die verfügbaren Abfragesysteme beeinflussen die Skalierbarkeit des Prozesses, wenn",
    },
    "haproxy/other-sections.md": {
        "- The feature is limited to the http-01, dns-01 or dns-persist-01 challenges":
            "- Die Funktion ist auf die Challenges http-01, dns-01 oder dns-persist-01 beschränkt",
        "- It is possible to start without an existing certificate on the disk. To do":
            "- Der Start ist ohne vorhandenes Zertifikat auf dem Datenträger möglich. Dazu",
        "- The current HAProxy architecture is a non-blocking model, access to the disk":
            "- Die aktuelle HAProxy-Architektur arbeitet nicht blockierend; der Zugriff auf den Datenträger",
    },
}

# These are explanatory labels misclassified as code by the upstream importer,
# not configuration comments. Language-specific, exact pairs prevent this from
# becoming an exemption for arbitrary code or inline literals.
RUSSIAN_PROSE_LABELS = {
    "haproxy/other-sections.md": {
        "- The feature is limited to the http-01, dns-01 or dns-persist-01 challenges":
            "- Возможность ограничена проверками http-01, dns-01 и dns-persist-01",
        "- It is possible to start without an existing certificate on the disk. To do":
            "- Можно запуститься без готового сертификата на диске. Для этого",
        "- The current HAProxy architecture is a non-blocking model, access to the disk":
            "- Текущая архитектура HAProxy неблокирующая; обращение к диску",
    },
    "haproxy/configuration-basics.md": {
        "#    hash as a comment start": "#    решётка как начало комментария",
    },
    "haproxy/starting.md": {
        "- the version": "- версия",
        "- the release date": "- дата выпуска",
        "- build options": "- параметры сборки",
        "- libraries versions": "- версии библиотек",
        "- Available polling systems will affect the process's scalability when":
            "- Доступные механизмы опроса влияют на масштабируемость процесса при",
    },
}

FRENCH_PROSE_LABELS = {
    "haproxy/configuration-basics.md": {"#    hash as a comment start": "#    dièse comme début de commentaire"},
    "haproxy/starting.md": {
        "- the version": "- la version",
        "- the release date": "- la date de publication",
        "- build options": "- les options de compilation",
        "- libraries versions": "- les versions des bibliothèques",
        "- Available polling systems will affect the process's scalability when":
            "- Les mécanismes de scrutation disponibles influent sur la capacité de montée en charge du processus lorsque",
    },
    "haproxy/other-sections.md": {
        "- The feature is limited to the http-01, dns-01 or dns-persist-01 challenges":
            "- Cette fonctionnalité est limitée aux challenges http-01, dns-01 ou dns-persist-01",
        "- It is possible to start without an existing certificate on the disk. To do":
            "- Il est possible de démarrer sans certificat existant sur le disque. Pour cela",
        "- The current HAProxy architecture is a non-blocking model, access to the disk":
            "- L'architecture actuelle de HAProxy est non bloquante ; l'accès au disque",
    },
}

CHINESE_PROSE_LABELS = {
    "haproxy/configuration-basics.md": {"#    hash as a comment start": "#    将井号作为注释的开始"},
    "haproxy/starting.md": {
        "- the version": "- 版本",
        "- the release date": "- 发布日期",
        "- build options": "- 构建选项",
        "- libraries versions": "- 库版本",
        "- Available polling systems will affect the process's scalability when":
            "- 可用的轮询系统在以下情况下会影响进程的可扩展性",
    },
    "haproxy/other-sections.md": {
        "- The feature is limited to the http-01, dns-01 or dns-persist-01 challenges":
            "- 此功能仅支持 http-01、dns-01 或 dns-persist-01 验证",
        "- It is possible to start without an existing certificate on the disk. To do":
            "- 可以在磁盘上没有现有证书的情况下启动。为此",
        "- The current HAProxy architecture is a non-blocking model, access to the disk":
            "- HAProxy 当前采用非阻塞架构，访问磁盘",
    },
    "haproxy/statistics-and-monitoring.md": {
        "set server <backend>/<server> ssl [ on | off ]  (deprecated)":
            "set server <backend>/<server> ssl [ on | off ]  （已弃用）",
    },
}


def prose_labels(source: Path, language: str = "de") -> dict[str, str]:
    try:
        relative = source.resolve().relative_to(PROJECT / "content" / "docs")
    except ValueError:
        return {}
    registry = {"de": PROSE_LABELS, "ru": RUSSIAN_PROSE_LABELS, "fr": FRENCH_PROSE_LABELS, "zh": CHINESE_PROSE_LABELS}.get(language, {})
    return registry.get(relative.as_posix(), {})


def translated_inline_labels(source: Path, inline: Counter[str], language: str = "de") -> Counter[str]:
    result = inline.copy()
    for english, german in prose_labels(source, language).items():
        count = result.pop(f"`{english}`", 0)
        if count:
            result[f"`{german}`"] += count
    return result


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def manifest_path(source: Path, language: str) -> Path | None:
    try:
        relative = source.resolve().relative_to(PROJECT / "content" / "docs")
    except ValueError:
        return None
    if len(relative.parts) < 2:
        return None
    return REGISTRY / f"{relative.parts[0]}.{language}" / relative.with_suffix(".json").relative_to(relative.parts[0])


def load_manifest(source: Path, language: str) -> dict:
    path = manifest_path(source, language)
    if path is None or not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("source") != str(source.resolve().relative_to(PROJECT)):
        raise ValueError(f"{path}: source path mismatch")
    if payload.get("language") != language:
        raise ValueError(f"{path}: language mismatch")
    if not isinstance(payload.get("fences"), list):
        raise ValueError(f"{path}: missing fence review list")
    return payload


def literal_blocks(source: Path, payload: dict) -> list[str]:
    """Read reviewed unfenced code/output, including snippets inside prose."""
    lines = source.read_text(encoding="utf-8").splitlines(keepends=True)
    blocks = []
    for entry in payload.get("literal_blocks", []):
        start, end = entry.get("lines", [None, None])
        if not isinstance(start, int) or not isinstance(end, int) or not 1 <= start <= end <= len(lines):
            raise ValueError(f"{source}: invalid reviewed literal line range")
        column = entry.get("start_column", 1)
        if not isinstance(column, int) or not 1 <= column <= len(lines[start - 1]):
            raise ValueError(f"{source}: invalid reviewed literal start column")
        # A translated label such as "Example " can precede a literal on the
        # same line in imported manuals. Protect the exact suffix and all
        # following lines, leaving only that explicitly excluded label as prose.
        block = lines[start - 1][column - 1:] + "".join(lines[start:end])
        if entry.get("classification") not in {"program-output", "configuration", "command", "source-code"}:
            raise ValueError(f"{source}: invalid unfenced literal classification")
        if entry.get("source_sha256") != sha256(block):
            raise ValueError(f"{source}: reviewed unfenced literal changed at line {start}")
        blocks.append(block)
    document = "".join(lines)
    for entry in payload.get("literal_snippets", []):
        snippet = entry.get("text")
        if not isinstance(snippet, str) or not snippet or snippet not in document:
            raise ValueError(f"{source}: reviewed literal snippet is absent from English")
        if entry.get("classification") not in {"program-output", "configuration", "command", "source-code"}:
            raise ValueError(f"{source}: invalid literal snippet classification")
        if entry.get("source_sha256") != sha256(snippet):
            raise ValueError(f"{source}: reviewed literal snippet hash changed")
        blocks.append(snippet)
    return blocks


def validate_literal_blocks(source: Path, target_document: str, errors: list[str], language: str = "de") -> None:
    try:
        blocks = literal_blocks(source, load_manifest(source, language))
    except (OSError, ValueError, TypeError) as exc:
        errors.append(str(exc))
        return
    english = source.read_text(encoding="utf-8")
    for block in blocks:
        if target_document.count(block) != english.count(block):
            errors.append(f"{source}: reviewed unfenced code or output changed: {block.splitlines()[0]!r}")


def prose_for_lint(source: Path, document: str, language: str = "de") -> str:
    """Expose reviewed explanation fences to prose lint without shifting lines."""
    payload = load_manifest(source, language)
    for block in literal_blocks(source, payload):
        document = document.replace(block, "\n" * block.count("\n"))
    reviews = {entry["index"]: entry for entry in payload.get("fences", [])}
    for english, german in prose_labels(source, language).items():
        for label in (english, german):
            document = document.replace(f"**`{label}`**", f"**{label}**")
    if not reviews:
        return document
    output = []
    marker = ""
    minimum = 0
    index = 0
    for line in document.splitlines(keepends=True):
        if marker:
            if re.fullmatch(rf" {{0,3}}{re.escape(marker)}{{{minimum},}}[ \t]*\n?", line):
                output.append(("\n" if line.endswith("\n") else "") if index in reviews else line)
                marker = ""
            else:
                review = reviews.get(index)
                if review:
                    if line.rstrip("\r\n") in review.get("protected_lines", []):
                        line = "\n" if line.endswith("\n") else ""
                    else:
                        for literal in review.get("protected_literals", []):
                            line = line.replace(literal, " " * len(literal))
                output.append(line)
            continue
        match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if match:
            index += 1
            marker, minimum = match.group(1)[0], len(match.group(1))
            output.append(("\n" if line.endswith("\n") else "") if index in reviews else line)
        else:
            output.append(line)
    return "".join(output)


def validate_fences(
    source: Path,
    english: list[str],
    translated: list[str],
    errors: list[str],
    *,
    language: str = "de",
) -> None:
    label = str(source.resolve().relative_to(PROJECT))
    try:
        payload = load_manifest(source, language)
    except (OSError, ValueError, TypeError) as exc:
        errors.append(f"{label}: invalid explanatory-fence registry: {exc}")
        return
    entries = payload.get("fences", [])
    reviews = {}
    for entry in entries:
        index = entry.get("index")
        if not isinstance(index, int) or index < 1 or index > len(english) or index in reviews:
            errors.append(f"{label}: invalid or duplicate reviewed fence index {index!r}")
            continue
        reviews[index] = entry
    if len(english) != len(translated):
        errors.append(f"{label}: fenced block count changed")
    for index, (en, target) in enumerate(zip(english, translated), 1):
        review = reviews.get(index)
        prefix = f"{label}: fence {index}"
        if review is None:
            if en != target:
                errors.append(f"{prefix}: fenced code or literal output changed without a prose review")
            continue
        if review.get("classification") not in CLASSIFICATIONS:
            errors.append(f"{prefix}: unknown explanatory-fence classification")
        if language in {"zh", "fr"} and source.parent.name == "haproxy" and not isinstance(review.get("review"), str):
            errors.append(f"{prefix}: missing bilingual explanation review")
        elif language in {"zh", "fr"} and source.parent.name == "haproxy" and not review["review"].strip():
            errors.append(f"{prefix}: empty bilingual explanation review")
        if review.get("source_sha256") != sha256(en):
            errors.append(f"{prefix}: reviewed English explanation changed; review required")
        if review.get("target_sha256") != sha256(target):
            errors.append(f"{prefix}: {language} explanation differs from the reviewed translation")
        en_lines, target_lines = en.splitlines(), target.splitlines()
        if en_lines[0] != target_lines[0] or en_lines[-1] != target_lines[-1]:
            errors.append(f"{prefix}: fence markers or language changed")
        is_label = (
            review.get("classification") == "explanation-label"
            and en_lines[0].strip() == "```haproxy"
            and len(en_lines) == len(target_lines) == 3
            and prose_labels(source, language).get(en_lines[1]) == target_lines[1]
        )
        is_mixed_code = (
            review.get("classification") == "mixed-explanation"
            and en_lines[0].strip() in {"```shell", "```haproxy"}
            and bool(review.get("protected_lines"))
        )
        # The upstream importer labels this two-row environment-variable
        # description table as shell. It contains no executable commands.
        # Admit only these exact English rows and preserve the variable column.
        keylog_rows = [
            "$HAPROXY_KEYLOG_FC_LOG_FMT   frontend (client-facing) connection keys",
            "$HAPROXY_KEYLOG_BC_LOG_FMT   backend (server-facing) connection keys",
        ]
        is_keylog_table = (
            source.parent.name == "haproxy"
            and source.name == "global.md"
            and review.get("classification") == "table-labels"
            and en_lines[0].strip() == "```shell"
            and en_lines[1:-1] == keylog_rows
            and len(target_lines) == 4
            and [line.split(maxsplit=1)[0] if line.strip() else "" for line in target_lines[1:-1]]
            == [line.split(maxsplit=1)[0] for line in keylog_rows]
        )
        if en_lines[0].strip() != "```text" and not is_label and not is_mixed_code and not is_keylog_table:
            errors.append(f"{prefix}: only explanatory text fences may be registered")
        en_body, target_body = "\n".join(en_lines[1:-1]), "\n".join(target_lines[1:-1])
        for name, pattern in (
            ("placeholder", r"<[^<>\n]+>"),
            ("inline literal", r"`+[^`\n]*`+"),
            ("numeric literal", r"\d+(?:[.,]\d+)*"),
        ):
            if Counter(re.findall(pattern, en_body)) != Counter(re.findall(pattern, target_body)):
                errors.append(f"{prefix}: protected {name} changed")
        for literal in review.get("protected_literals", []):
            if not isinstance(literal, str) or not literal or not en_body.count(literal):
                errors.append(f"{prefix}: invalid protected literal {literal!r}")
            elif en_body.count(literal) != target_body.count(literal):
                errors.append(f"{prefix}: protected literal {literal!r} changed")
        for line in review.get("protected_lines", []):
            if not isinstance(line, str) or line not in en_lines:
                errors.append(f"{prefix}: invalid protected source line {line!r}")
            elif en_lines.count(line) != target_lines.count(line):
                errors.append(f"{prefix}: protected code/output line changed: {line!r}")
