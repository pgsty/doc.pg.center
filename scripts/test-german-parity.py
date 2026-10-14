#!/usr/bin/env python3
"""Regression tests for complete component acceptance and protected literals."""

import contextlib
from collections import Counter
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "german_parity", Path(__file__).with_name("check-german-parity.py")
)
checker = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = checker
spec.loader.exec_module(checker)
import translation_fences as fences


class GermanParityTests(unittest.TestCase):
    def test_release_separators_after_references_are_not_setext_headings(self):
        for definition in (
            "[#1034]: https://github.com/pgbouncer/pgbouncer/pull/1034",
            "[libusual/#41]: https://github.com/libusual/libusual/pull/41",
        ):
            body = definition + "\n--------\n\n## Release {#release}\n"
            self.assertEqual(checker.heading_rows(body), [checker.Heading(2, "Release", "release", 4)])

    def test_release_separators_after_list_items_are_not_setext_headings(self):
        for item in ("* Updated CI", "- Fixed a bug", "+ Updated docs", "1. Fixed a bug", "2) Updated CI"):
            body = item + "\n--------\n\n## Release {#release}\n"
            self.assertEqual(checker.heading_rows(body), [checker.Heading(2, "Release", "release", 4)])

    def test_legitimate_setext_headings_still_require_their_exact_anchors(self):
        body = "Overview {#overview}\n========\n\n*Details* {#details}\n--------\n"
        self.assertEqual(checker.heading_rows(body), [
            checker.Heading(1, "Overview", "overview", 1),
            checker.Heading(2, "*Details*", "details", 4),
        ])
        self.assertEqual(checker.heading_rows("Details\n--------\n")[0].anchor, None)
        self.assertNotEqual(checker.heading_rows(body), checker.heading_rows(body.replace("#details", "#other")))
        nested = checker.heading_rows("* Details {#details}\n  --------\n")
        self.assertEqual([(row.level, row.anchor) for row in nested], [(2, "details")])

    def test_localized_shortcut_references_preserve_their_ids(self):
        definitions = "\n\n[Homebrew can run on Linux]: <https://example.com>\n"
        english = "[Homebrew can run on Linux]" + definitions
        german = "[Homebrew läuft unter Linux][Homebrew can run on Linux]" + definitions
        self.assertEqual(checker.reference_link_signature(english), ["homebrew can run on linux"])
        self.assertEqual(checker.reference_link_signature(english), checker.reference_link_signature(german))
        self.assertEqual(checker.reference_link_signature(definitions), [])
        self.assertEqual(checker.reference_link_signature("`[Homebrew can run on Linux]`" + definitions), [])
        self.assertEqual(checker.reference_link_signature("[Homebrew can run on Linux](https://example.com)" + definitions), [])

    def test_etcd_exclusivity_emphasis_is_not_a_sql_keyword(self):
        self.assertEqual(checker.uppercase_technical_literals("ONLY used for TLS. ONLY be used for HTTP."), {"TLS", "HTTP"})
        self.assertEqual(checker.uppercase_technical_literals("MVCC for testing ONLY!"), {"MVCC"})
        self.assertEqual(checker.uppercase_technical_literals("SELECT ONLY"), {"SELECT", "ONLY"})
        self.assertEqual(checker.uppercase_technical_literals("CRC takes in consideration ALL records"), {"CRC"})
        self.assertEqual(checker.uppercase_technical_literals("SELECT ALL"), {"SELECT", "ALL"})

    def test_rendered_routes_are_lowercase_on_case_sensitive_filesystems(self):
        source = checker.CONTENT / "docs/etcd/triage/PRs.md"
        self.assertEqual(checker.rendered_page(source, Path("/build")), Path("/build/docs/etcd/triage/prs/index.html"))

    def test_inline_concept_translation_is_page_scoped_and_keeps_api_literals(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "content/docs/etcd/learning/api.md"
            source.parent.mkdir(parents=True)
            target = source.with_suffix(".de.md")
            source.write_text("---\ntitle: Guide\n---\nUse `Revision` for a `time travel query`.\n")
            target.write_text("---\ntitle: Anleitung\n---\n`Revision` für eine `Zeitreiseabfrage` verwenden.\n")
            with patch.object(checker, "PROJECT", root), patch.object(checker, "read_source", side_effect=lambda path, *_args, **_kwargs: (path.read_text(), None)), patch("translation_fences.PROJECT", root.resolve()):
                errors = []
                checker.validate_pair(source, target, None, errors, current_source=True)
                self.assertEqual(errors, [])
                target.write_text(target.read_text().replace("`Revision`", "`Version`"))
                errors = []
                checker.validate_pair(source, target, None, errors, current_source=True)
                self.assertTrue(any("inline code literals changed" in error for error in errors))
                target.write_text(target.read_text().replace("`Version`", "`Revision`"))
                other = source.with_name("other.md")
                other.write_text(source.read_text())
                errors = []
                checker.validate_pair(other, target, None, errors, current_source=True)
                self.assertTrue(any("inline code literals changed" in error for error in errors))

    def test_failsafe_emphasis_is_prose_not_a_technical_literal(self):
        self.assertEqual(checker.uppercase_technical_literals(
            "Why MUST the current primary see ALL other members? DCS REST API\n"
            "ALL other cluster members\n## F.A.Q.\n"
        ), {"DCS", "REST", "API"})
        self.assertEqual(checker.uppercase_technical_literals("SELECT ALL"), {"SELECT", "ALL"})

    def test_html_alternative_text_is_translatable_but_asset_is_protected(self):
        english = '<img src="/shared.png" width="128" alt="image" title="Overview" />'
        german = '<img src="/shared.png" width="128" alt="Bild" title="Überblick" />'
        self.assertEqual(checker.normalized_html_tags(english), checker.normalized_html_tags(german))
        self.assertNotEqual(checker.normalized_html_tags(english), checker.normalized_html_tags(german.replace('128', '256')))
        self.assertNotEqual(checker.normalized_html_tags(english), checker.normalized_html_tags(german.replace('/shared.png', '/de/shared.png')))
        self.assertNotEqual(checker.normalized_html_tags(english), checker.normalized_html_tags(german.replace(' alt="Bild"', '')))

    def test_translatable_warning_labels_keep_following_acronyms(self):
        text = "**NOTE TO PACKAGERS**: TLS and WAL. **IMPORTANT NOTE**: CPU.\nCAUTION:\nPITR"
        self.assertEqual(checker.uppercase_technical_literals(text), {"TLS", "WAL", "CPU", "PITR"})
        self.assertEqual(checker.uppercase_technical_literals("NOTE TABLESPACES"), {"NOTE", "TABLESPACES"})

    def test_total_label_is_not_a_technical_token(self):
        self.assertEqual(checker.uppercase_technical_literals("| TOTAL | 1/1 |"), set())
        self.assertEqual(checker.uppercase_technical_literals("TOTAL is a field"), {"TOTAL"})

    def test_warning_emphasis_and_clock_suffix_are_prose(self):
        self.assertEqual(checker.uppercase_technical_literals("WARNING:\n**DROP IT** WAL\nIMPORTANT:\n6:30 AM"), {"WAL"})
        self.assertEqual(checker.uppercase_technical_literals("DROP AM PM"), {"DROP", "AM", "PM"})

    def test_haproxy_ring_warning_and_negation_are_exact_prose_contexts(self):
        text = (
            "WARNING: there are stability and security implications in using this feature. TLS\n"
            "The information present in this ring are structured and are NOT directly readable using a text\neditor.\n"
        )
        self.assertEqual(checker.uppercase_technical_literals(text), {"TLS"})
        for text in ("WARNING: different warning", "NOT readable", "SELECT NOT NULL", "SQL OR NOT"):
            self.assertTrue({"WARNING", "NOT"} & checker.uppercase_technical_literals(text), text)

    def test_numeric_units_ordinals_and_versions_remain_protected(self):
        english = "Timeout 30s; the 256th portion; version 3.4.4; count 2.\n"
        german = "Zeitüberschreitung 30 Sekunden; der 256. Anteil; Version 3.4.4; Anzahl 2.\n"
        self.assertEqual(checker.number_facts("", english), checker.number_facts("", german))
        self.assertEqual(checker.version_facts("", english), checker.version_facts("", german))
        for old, new in (("30", "31"), ("256", "255"), ("3.4.4", "3.4.5")):
            self.assertNotEqual(checker.number_facts("", english), checker.number_facts("", german.replace(old, new)))

    def test_narrow_space_integer_grouping_preserves_the_numeric_value(self):
        english = "Less than once in 25,000,000 cases; 1,000 or 123,456."
        german = "Weniger als einmal in 25\u202f000\u202f000 Fällen; 1\u202f000 oder 123\u202f456."
        self.assertEqual(checker.number_facts("", english), checker.number_facts("", german))
        self.assertNotEqual(checker.number_facts("", english), checker.number_facts("", german.replace("25\u202f000\u202f000", "25\u202f000\u202f001")))
        self.assertNotEqual(checker.number_facts("", "25,000,000"), checker.number_facts("", "25\u202f00\u202f000"))

    def test_narrow_space_normalization_does_not_consume_decimals_versions_or_identifiers(self):
        for value in (
            "1.25\u202f000", "25\u202f000.5", "25\u202f000,5", "v25\u202f000",
            "id_25\u202f000", "build-25\u202f000", "25\u202f000-build",
            "1234\u202f000", "25\u202f000\u202f00", "version 3.4.6; decimal 2.50",
        ):
            with self.subTest(value=value):
                self.assertEqual(checker.number_facts("", value), Counter(checker.NUMBER_RE.findall(value)))
        self.assertEqual(checker.version_facts("", "version 3.4.6"), {"3.4.6": 1})
        self.assertNotEqual(checker.version_facts("", "version 3.4.6"), checker.version_facts("", "version 3.4.7"))

    def test_number_grouping_does_not_waive_inline_literal_protection(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "content/docs/example/guide.md"
            source.parent.mkdir(parents=True)
            target = source.with_suffix(".de.md")
            source.write_text("---\ntitle: Guide\n---\nUse `25,000,000`.\n")
            target.write_text("---\ntitle: Anleitung\n---\n`25\u202f000\u202f000` verwenden.\n")
            with patch.object(checker, "PROJECT", root), patch.object(checker, "read_source", side_effect=lambda path, *_args, **_kwargs: (path.read_text(), None)), patch("translation_fences.PROJECT", root.resolve()):
                errors = []
                checker.validate_pair(source, target, None, errors, current_source=True)
            self.assertTrue(any("inline code literals changed" in error for error in errors))
            self.assertFalse(any("numeric facts changed" in error for error in errors))

    def test_acme_third_party_wording_does_not_waive_real_ordinals(self):
        english = "dataplaneAPI or another 3rd party tool to talk to a DNS provider API. Renew after 7 days and 12 hours."
        german = "dataplaneAPI oder ein anderes Drittanbieterwerkzeug zur Kommunikation mit einer DNS-Anbieter-API. Nach 7 Tagen und 12 Stunden erneuern."
        self.assertEqual(checker.number_facts("", english), checker.number_facts("", german))
        self.assertNotEqual(checker.number_facts("", english), checker.number_facts("", german.replace("12", "24")))
        self.assertEqual(checker.number_facts("", "another 3rd party tool"), {"3": 1})
        self.assertEqual(checker.number_facts("", "the 3rd server"), {"3": 1})

    def test_docs_routes_and_shared_assets(self):
        self.assertTrue(checker.unlocalized_document_route("/docs/pgbackrest/faq/#question"))
        self.assertFalse(checker.unlocalized_document_route("/de/docs/pgbackrest/faq/"))
        self.assertFalse(checker.unlocalized_document_route("https://example.org/docs/pgbackrest/"))
        self.assertFalse(checker.unlocalized_document_route("/docs/pgbackrest/chart.svg"))
        self.assertTrue(checker.localized_shared_asset("/de/docs/pgbackrest/chart.svg"))
        self.assertFalse(checker.localized_shared_asset("/docs/pgbackrest/chart.svg"))

    def test_component_gate_requires_all_pages_and_rejects_orphans(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            component = root / "content/docs/pgbackrest"
            component.mkdir(parents=True)
            source = "---\ntitle: Example\n---\n"
            (component / "_index.md").write_text(source)
            unrelated = root / "content/docs/patroni"
            unrelated.mkdir()
            (unrelated / "_index.md").write_text(source)
            args = ["check-german-parity.py", "--component", "pgbackrest", "--current-source"]
            with patch.object(checker, "PROJECT", root), patch.object(checker, "CONTENT", root / "content"), patch("translation_fences.PROJECT", root.resolve()), patch.object(sys, "argv", args), patch.object(checker, "read_source", side_effect=lambda source, *_args, **_kwargs: (source.read_text(), None)):
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(checker.main(), 1)
                    (component / "_index.de.md").write_text(source.replace("Example", "Beispiel"))
                    self.assertEqual(checker.main(), 0)
                    (component / "orphan.de.md").write_text(source)
                    self.assertEqual(checker.main(), 1)


class ReviewedFenceTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.source = self.root / "content/docs/haproxy/example.md"
        self.source.parent.mkdir(parents=True)
        self.registry = self.root / "data/translation-fences"
        for attribute, value in (("PROJECT", self.root), ("REGISTRY", self.registry)):
            patcher = patch.object(fences, attribute, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def write_review(self, english, german, **extra):
        self.source.write_text(english)
        review = {
            "index": 1, "classification": "argument-description",
            "source_sha256": fences.sha256(english), "target_sha256": fences.sha256(german),
            "review": "Separate bilingual comparison.",
        }
        review.update(extra)
        self.payload = {
            "source": str(self.source.relative_to(self.root)), "language": "de", "fences": [review],
        }
        self.save()

    def save(self):
        import json
        path = fences.manifest_path(self.source, "de")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.payload))

    def errors(self, english, german):
        errors = []
        fences.validate_fences(self.source, [english], [german], errors)
        return errors

    def test_exact_review_accepts_only_the_reviewed_bilingual_pair(self):
        en, de = "```text\n<name> is required; default 30.\n```", "```text\n<name> ist erforderlich; Standardwert 30.\n```"
        self.write_review(en, de)
        self.assertEqual(self.errors(en, de), [])
        self.assertTrue(any("English explanation changed" in e for e in self.errors(en.replace("required", "optional"), de)))
        self.assertTrue(any("reviewed translation" in e for e in self.errors(en, de.replace("erforderlich", "optional"))))

    def test_unregistered_fence_is_byte_protected(self):
        en = "```text\nThis output is literal.\n```"
        self.source.write_text(en)
        self.assertEqual(self.errors(en, en), [])
        self.assertTrue(any("without a prose review" in e for e in self.errors(en, en.replace("output", "Ausgabe"))))

    def test_stale_index_and_manifest_identity_fail(self):
        en, de = "```text\nExplanation\n```", "```text\nErklärung\n```"
        self.write_review(en, de)
        self.payload["fences"][0]["index"] = 2
        self.save()
        self.assertTrue(any("invalid or duplicate" in e for e in self.errors(en, de)))
        self.payload["source"] = "content/docs/haproxy/other.md"
        self.save()
        self.assertTrue(any("source path mismatch" in e for e in self.errors(en, de)))
        self.payload["source"] = str(self.source.relative_to(self.root))
        self.payload["language"] = "ru"
        self.save()
        self.assertTrue(any("language mismatch" in e for e in self.errors(en, de)))

    def test_protected_lines_literals_placeholders_and_numbers_survive_fresh_hashes(self):
        en = "```text\nshow info\n<name> is required at 30; field Stot.\n```"
        de = "```text\nshow info\n<name> ist bei 30 erforderlich; Feld Stot.\n```"
        self.write_review(en, de, protected_lines=["show info"], protected_literals=["Stot"])
        self.assertEqual(self.errors(en, de), [])
        for old, new, error in (("show info", "show stat", "code/output line"), ("Stot", "Other", "protected literal"), ("<name>", "<id>", "placeholder"), ("30", "31", "numeric literal")):
            broken = de.replace(old, new)
            self.payload["fences"][0]["target_sha256"] = fences.sha256(broken)
            self.save()
            self.assertTrue(any(error in e for e in self.errors(en, broken)), (old, self.errors(en, broken)))

    def test_lint_exposes_explanations_but_masks_exact_output_lines(self):
        en, de = "```text\nshow info\nThe default is 30.\n```", "```text\nshow info\nDer Standardwert ist 30.\n```"
        self.write_review(en, de, protected_lines=["show info"])
        text = fences.prose_for_lint(self.source, de)
        self.assertIn("Der Standardwert ist 30.", text)
        self.assertNotIn("show info", text)
        self.assertEqual(text.count("\n"), de.count("\n"))

    def test_exact_importer_prose_label_is_page_scoped(self):
        self.source = self.source.with_name("starting.md")
        en, de = "```haproxy\n- the version\n```", "```haproxy\n- die Version\n```"
        self.write_review(en, de, classification="explanation-label")
        self.assertEqual(self.errors(en, de), [])
        inline = checker.Counter({"`- the version`": 1, "`version`": 1})
        self.assertEqual(fences.translated_inline_labels(self.source, inline), {"`- die Version`": 1, "`version`": 1})
        self.source = self.source.with_name("example.md")
        self.write_review(en, de, classification="explanation-label")
        self.assertTrue(any("only explanatory text" in e for e in self.errors(en, de)))
        self.assertEqual(fences.translated_inline_labels(self.source, inline), inline)

    def test_shell_keylog_description_table_is_exact_and_page_scoped(self):
        self.source = self.source.with_name("global.md")
        en = "```shell\n$HAPROXY_KEYLOG_FC_LOG_FMT   frontend (client-facing) connection keys\n$HAPROXY_KEYLOG_BC_LOG_FMT   backend (server-facing) connection keys\n```"
        de = "```shell\n$HAPROXY_KEYLOG_FC_LOG_FMT   Schlüssel der Frontend-Verbindung\n$HAPROXY_KEYLOG_BC_LOG_FMT   Schlüssel der Backend-Verbindung\n```"
        self.write_review(en, de, classification="table-labels", protected_literals=["$HAPROXY_KEYLOG_FC_LOG_FMT", "$HAPROXY_KEYLOG_BC_LOG_FMT"])
        self.assertEqual(self.errors(en, de), [])
        changed = de.replace("FC_LOG", "FC_OTHER")
        self.payload["fences"][0]["target_sha256"] = fences.sha256(changed)
        self.save()
        self.assertTrue(any("only explanatory text" in e for e in self.errors(en, changed)))
        self.source = self.source.with_name("example.md")
        self.write_review(en, de, classification="table-labels")
        self.assertTrue(any("only explanatory text" in e for e in self.errors(en, de)))

    def test_unfenced_literal_suffix_and_snippet_occurrences_are_protected(self):
        text = "Example show info\n# literal output\n\nkey key\n"
        self.source.write_text(text)
        block, snippet = "show info\n# literal output\n", "key"
        self.payload = {
            "source": str(self.source.relative_to(self.root)), "language": "de", "fences": [],
            "literal_blocks": [{"lines": [1, 2], "start_column": 9, "classification": "program-output", "source_sha256": fences.sha256(block)}],
            "literal_snippets": [{"text": snippet, "classification": "configuration", "source_sha256": fences.sha256(snippet)}],
        }
        self.save()
        target = text.replace("Example", "Beispiel")
        errors = []
        fences.validate_literal_blocks(self.source, target, errors)
        self.assertEqual(errors, [])
        for changed in (target.replace("show info", "show stat"), target.replace("key key", "key")):
            errors = []
            fences.validate_literal_blocks(self.source, changed, errors)
            self.assertTrue(any("unfenced code or output changed" in e for e in errors))
        self.source.write_text(text.replace("# literal output", "# changed output"))
        errors = []
        fences.validate_literal_blocks(self.source, target, errors)
        self.assertTrue(any("reviewed unfenced literal changed" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
