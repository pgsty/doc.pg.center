#!/usr/bin/env python3
"""Regression checks for publication gates and translation-safe generation."""
from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import translation_fences as fences

ROOT = Path(__file__).resolve().parent.parent


def module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


gate = module("pgbadger_gate", "check-pgbadger.py")
generator = module("pgbadger_generator", "generate-pgbadger-reference.py")


class PublicationRegressionTests(unittest.TestCase):
    def test_reader_prose_rejects_translation_policy(self):
        for body in (
            "This page preserves the command reference; the explanations are translated.",
            "本页选项说明已译为中文，参数保持原文。",
            "Cette page traduit la référence de commande.",
            "Diese Ausgabe enthält Übersetzungen.",
            "このページはコマンドリファレンスの翻訳です。",
            "Эта страница содержит перевод справочника команд.",
        ):
            with self.subTest(body=body):
                errors = []
                gate.validate_reader_prose(gate.CONTENT / "command-line.md", body, errors)
                self.assertTrue(errors)

    def test_reader_prose_keeps_technical_language_and_original_license(self):
        body = "Translate action WITH into CTE.\nУдалён перевод строки.\nKeep server messages in English."
        errors = []
        gate.validate_reader_prose(gate.CONTENT / "releases/11.md", body, errors)
        self.assertEqual(errors, [])

    def test_report_path_cannot_overwrite_repository_source(self):
        with patch.object(gate.sys, "argv", ["check", "--report", str(gate.CONTENT / "command-line.md")]), patch.object(gate.sys, "stderr", io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                gate.main()
            self.assertEqual(error.exception.code, 2)

    def test_missing_translation_is_rejected_without_removing_real_file(self):
        missing = gate.CONTENT / "download.fr.md"
        original = Path.is_file
        stderr = io.StringIO()
        def exists(path):
            return False if path == missing else original(path)
        with patch.object(Path, "is_file", exists), patch.object(gate.sys, "argv", ["check"]), patch.object(gate.sys, "stderr", stderr):
            self.assertEqual(gate.main(), 1)
        self.assertIn("download.fr.md: missing translation", stderr.getvalue())

    def test_option_typo_in_history_is_rejected(self):
        target = gate.CONTENT / "releases/10.fr.md"
        original = Path.read_text
        stderr = io.StringIO()
        def read(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            if path == target:
                front, body = text.split("\n---\n", 1)
                return front + "\n---\n" + body.replace("--job_per_file", "--job_pir_file")
            return text
        with patch.object(Path, "read_text", read), patch.object(gate.sys, "argv", ["check"]), patch.object(gate.sys, "stderr", stderr):
            self.assertEqual(gate.main(), 1)
        self.assertIn("releases/10.fr.md: changed long options", stderr.getvalue())

    def test_versions_and_release_dates_cannot_be_waived(self):
        source = gate.CONTENT / "releases/13.md"
        target = gate.CONTENT / "releases/13.fr.md"
        for english, translated in (("2025-12-29", "2028-12-29"), ("PgBouncer 1.21", "PgBouncer 1.22")):
            errors = []
            # Even an exact prose-number waiver cannot admit a changed version.
            review = {str(target.relative_to(ROOT)): {
                "source": str(source.relative_to(ROOT)),
                "source_body_sha256": gate.digest(english),
                "target_body_sha256": gate.digest(translated),
                "missing": dict(gate.numeric_facts(english) - gate.numeric_facts(translated)),
                "extra": dict(gate.numeric_facts(translated) - gate.numeric_facts(english)),
                "reason": "test attempted waiver",
            }}
            gate.validate_numbers(source, target, english, translated, review, errors)
            self.assertTrue(any("version, date or decimal" in error for error in errors))

    def test_numeric_notation_review_is_bound_to_both_bodies(self):
        source = gate.CONTENT / "sample-reports.md"
        target = gate.CONTENT / "sample-reports.zh.md"
        english, translated = "May 2022", "2022年5月"
        review = {str(target.relative_to(ROOT)): {
            "source": str(source.relative_to(ROOT)),
            "source_body_sha256": gate.digest(english),
            "target_body_sha256": gate.digest(translated),
            "missing": {}, "extra": {"5": 1}, "reason": "May to 5月",
        }}
        errors = []
        gate.validate_numbers(source, target, english, translated, review, errors)
        self.assertEqual(errors, [])
        gate.validate_numbers(source, target, english, "2022年6月", review, errors)
        self.assertTrue(errors)

    def test_decimal_separator_is_not_a_fact_change(self):
        source, target = gate.CONTENT / "parallel-processing.md", gate.CONTENT / "parallel-processing.fr.md"
        errors = []
        gate.validate_numbers(source, target, "9.5 GB", "9,5 Go", {}, errors)
        self.assertEqual(errors, [])

    def test_historical_option_name_keeps_underscore(self):
        self.assertEqual(generator.reference_keywords("--job_per_file"), "[--job_per_file, job_per_file]")

    def test_search_keywords_include_cli_query_tokens(self):
        self.assertEqual(generator.reference_keywords("--ssh-sudo"), "[--ssh-sudo, ssh, ssh-sudo, sudo]")

    def test_unterminated_fence_is_rejected(self):
        with self.assertRaises(ValueError):
            gate.fenced("```console\npgbadger log\n")

    def test_generator_preserves_translation_and_detects_stale_english(self):
        with tempfile.TemporaryDirectory(prefix="pgbadger-generator-test-") as tmp:
            content = Path(tmp).resolve()
            translated = content / "command-line.zh.md"
            translated.write_text("reviewed translation sentinel")
            with patch.object(generator, "CONTENT", content), patch.object(generator, "PROJECT", content), patch.object(generator, "CHECK_ONLY", False):
                generator.write_command_reference()
                generator.write_release_pages()
                self.assertEqual(translated.read_text(), "reviewed translation sentinel")
                self.assertEqual(len(list(content.rglob("*.md"))), 7)
                generator.CHECK_ONLY = True
                generator.write_command_reference()
                (content / "command-line.md").write_text("stale source")
                with self.assertRaises(RuntimeError):
                    generator.write_command_reference()
                self.assertEqual(translated.read_text(), "reviewed translation sentinel")

    def test_commands_and_stale_fence_reviews_are_blocked(self):
        with tempfile.TemporaryDirectory(prefix="pgbadger-fence-test-") as tmp:
            root = Path(tmp).resolve()
            source = root / "content/docs/pgbadger/command-line.md"
            source.parent.mkdir(parents=True)
            english = "```text\n--jobs N : parse 8 files\n```\n"
            translated = "```text\n--jobs N : 解析8个文件\n```\n"
            source.write_text(english)
            registry = root / "data/translation-fences"
            manifest = registry / "pgbadger.zh/command-line.json"
            manifest.parent.mkdir(parents=True)
            entry = {
                "index": 1, "classification": "argument-description",
                "source_sha256": fences.sha256(english),
                "target_sha256": fences.sha256(translated),
                "protected_literals": ["--jobs N"],
            }
            with patch.object(fences, "PROJECT", root), patch.object(fences, "REGISTRY", registry):
                errors = []
                fences.validate_fences(source, [english], [translated], errors, language="zh")
                self.assertTrue(errors, "an unregistered literal fence must not change")
                manifest.write_text(json.dumps({"source": str(source.relative_to(root)), "language": "zh", "fences": [entry]}))
                errors = []
                fences.validate_fences(source, [english], [translated], errors, language="zh")
                self.assertEqual(errors, [])
                changed = translated.replace("--jobs N", "--Jobs N")
                entry["target_sha256"] = fences.sha256(changed)
                manifest.write_text(json.dumps({"source": str(source.relative_to(root)), "language": "zh", "fences": [entry]}))
                errors = []
                fences.validate_fences(source, [english], [changed], errors, language="zh")
                self.assertTrue(any("protected literal" in error for error in errors))
                errors = []
                fences.validate_fences(source, [english.replace("8", "9")], [changed], errors, language="zh")
                self.assertTrue(any("English explanation changed" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
