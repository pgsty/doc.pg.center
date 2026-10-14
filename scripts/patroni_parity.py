"""Exact, current-byte Patroni notation exceptions for the legacy DE/RU gates."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
ROOT = PROJECT / 'content/docs/patroni'
AUDIT = PROJECT / 'data/translation-audits/patroni.json'


def reviewed_delta(source, source_text, target_text, language, field, expected, actual):
    """Accept only the reviewed multiset delta, with both complete-file pins.

    Executable examples, literal presence, values and structure retain their
    independent checks; this does not authorize arbitrary formatting changes.
    """
    if not source.is_relative_to(ROOT) or field not in {'inline_literal_variant', 'numeric_variant'}:
        return False
    try:
        audit = json.loads(AUDIT.read_text())
        page = audit['pages'][source.relative_to(ROOT).as_posix()]
        row = page['translations'][language]
        variant = row[field]
        return (
            audit['semantic_review']['status'] == 'complete'
            and row['semantic_review'] == 'complete'
            and page['source_sha256'] == hashlib.sha256(source_text.encode()).hexdigest()
            and row['translation_sha256'] == hashlib.sha256(target_text.encode()).hexdigest()
            and bool(variant['reason'])
            and variant['delta'] == {'missing': dict(expected - actual), 'added': dict(actual - expected)}
        )
    except (OSError, ValueError, KeyError, TypeError):
        return False
