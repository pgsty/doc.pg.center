#!/usr/bin/env python3
"""Regressions for real PgBouncer literals and folded search metadata."""

import importlib.util
import json
import os
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "pgbouncer_helpers", Path(__file__).with_name("pgbouncer_validation.py")
)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
SOURCE = checker.CONTENT / "docs/pgbouncer/changelog.md"
AUDIT = json.loads((checker.CONTENT.parent / "data/translation-audits/pgbouncer.json").read_text())
DIAGNOSTICS = next(row["protected_diagnostics"] for row in AUDIT["pages"] if row["translation"].endswith("changelog.ru.md"))
gate_spec = importlib.util.spec_from_file_location(
    "pgbouncer_gate", Path(__file__).with_name("check-pgbouncer.py")
)
gate = importlib.util.module_from_spec(gate_spec)
sys.modules[gate_spec.name] = gate
gate_spec.loader.exec_module(gate)


class PgBouncerParityTests(unittest.TestCase):
    def test_folded_description_is_not_the_yaml_indicator(self):
        for indicator in (">", ">-", ">+", "|", "|-", "|+"):
            front = f"title: Test\ndescription: {indicator}\n  Первая строка\n  вторая строка\nweight: 30\n"
            self.assertEqual(checker.front_text(front, "description"),
                             "Первая строка вторая строка")

    def test_quoted_and_plain_metadata_remain_exact(self):
        self.assertEqual(checker.front_text('title: "SHOW USERS"', "title"), "SHOW USERS")
        self.assertEqual(checker.front_text("title: 'User''s pool'", "title"), "User's pool")
        self.assertEqual(checker.front_text("title: PgBouncer 1.26.0", "title"), "PgBouncer 1.26.0")
        self.assertIsNone(checker.front_text("title: Test", "description"))

    def check_body(self, body):
        _, source_body = checker.split_front_matter(SOURCE.read_text(encoding="utf-8"))
        return checker.placeholder_errors(source_body, body, DIAGNOSTICS)

    def test_real_historical_fixme_diagnostic_is_accepted(self):
        target = SOURCE.with_suffix(".ru.md")
        _, body = checker.split_front_matter(target.read_text(encoding="utf-8"))
        self.assertFalse(any("placeholder" in error for error in self.check_body(body)))

    def test_new_placeholder_is_still_rejected(self):
        target = SOURCE.with_suffix(".ru.md")
        _, body = checker.split_front_matter(target.read_text(encoding="utf-8"))
        for token in ("FIXME", "TODO", "TRANSLATE_ME"):
            errors = self.check_body(body + "\n" + token + ": перевод не завершён.\n")
            self.assertTrue(any("placeholder" in error for error in errors), errors)

    def test_changed_historical_diagnostic_cannot_use_the_exception(self):
        target = SOURCE.with_suffix(".ru.md")
        _, body = checker.split_front_matter(target.read_text(encoding="utf-8"))
        changed = body.replace("FIXME: query end, but query_start == 0",
                               "FIXME: query end, but query_start == 1")
        errors = self.check_body(changed)
        self.assertTrue(any("placeholder" in error for error in errors), errors)
        _, source_body = checker.split_front_matter(SOURCE.read_text(encoding="utf-8"))
        self.assertTrue(checker.diagnostic_errors(source_body, changed, DIAGNOSTICS))

    def test_autolink_and_bare_url_changes_are_rejected(self):
        for wrapper in ("<{}>", "{}"):
            first = gate.link_signature(wrapper.format("https://example.org/first"), SOURCE, "zh")
            second = gate.link_signature(wrapper.format("https://example.org/second"), SOURCE, "zh")
            self.assertTrue(first)
            self.assertNotEqual(first, second)

    def test_explicit_and_bare_links_preserve_multiplicity(self):
        signature = gate.link_signature("[one](https://example.org/path) https://example.org/path.", SOURCE, "fr")
        self.assertEqual(signature["https://example.org/path"], 2)

    def test_only_local_chinese_prose_fragments_are_normalized(self):
        for root in ("https://example.org", "https://example.org/docs/pgbouncer/config/"):
            self.assertNotEqual(gate.link_signature(f"[x]({root}#one)", SOURCE, "zh"),
                                gate.link_signature(f"[x]({root}#two)", SOURCE, "zh"))
        self.assertEqual(gate.link_signature("[x](/docs/pgbouncer/config/#one)", SOURCE, "zh"),
                         gate.link_signature("[x](/zh/docs/pgbouncer/config/#二)", SOURCE, "zh"))

    def test_english_print_paragraph_loss_is_rejected(self):
        build = Path(os.environ.get("PGBOUNCER_RENDERED_DIR", ""))
        printing = build / "_print/docs/pgbouncer/index.html"
        if not printing.is_file():
            self.skipTest("set PGBOUNCER_RENDERED_DIR to test the production print bundle")
        sources = [gate.ROOT / ("_index.md" if n["id"] == gate.PREFIX else n["id"].removeprefix(gate.PREFIX).strip("/") + ".md")
                   for n in gate.collection_nodes(build, "en")]
        original = Path.read_text
        def read_text(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            if path == printing:
                changed, count = re.subn(r"<p>This manual is based on.*?</p>", "", text, count=1, flags=re.S)
                self.assertEqual(count, 1)
                return changed
            return text
        with patch.object(Path, "read_text", read_text):
            errors, _ = gate.english_print_errors(build, sources)
        self.assertTrue(any("print body" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
