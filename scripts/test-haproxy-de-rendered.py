#!/usr/bin/env python3
"""Exercise stale reviews and rendered code/prose boundaries for German HAProxy."""

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("haproxy_de_rendered", Path(__file__).with_name("check-haproxy-de-rendered.py"))
checker = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = checker
spec.loader.exec_module(checker)
import translation_fences as fences


class RenderedAcceptanceTests(unittest.TestCase):
    def test_semantic_reviews_expire_when_either_page_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            source = root / "content/docs/haproxy/example.md"
            source.parent.mkdir(parents=True)
            target = source.with_suffix(".de.md")
            source.write_text("The server must use TLS.\n")
            target.write_text("Der Server muss TLS verwenden.\n")
            row = {"source": str(source.relative_to(root)), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "target_sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "semantic_review": {"status": "passed"}}
            with patch.object(checker, "PROJECT", root):
                self.assertEqual(checker.review_record_errors([source], {"pages": [row]}), [])
                target.write_text("Der Server kann TLS verwenden.\n")
                self.assertTrue(any("target_sha256" in e for e in checker.review_record_errors([source], {"pages": [row]})))
                source.write_text("The server may use TLS.\n")
                self.assertTrue(any("source_sha256" in e for e in checker.review_record_errors([source], {"pages": [row]})))
                self.assertTrue(any("missing, duplicate or orphan" in e for e in checker.review_record_errors([source], {"pages": [row, row]})))
                unsigned = dict(row, semantic_review={"status": "draft"})
                self.assertTrue(any("separate semantic" in e for e in checker.review_record_errors([source], {"pages": [unsigned]})))

    def test_rendered_literal_exceptions_require_exact_reviewed_fence_hashes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            source = root / "content/docs/haproxy/example.md"
            source.parent.mkdir(parents=True)
            en, de = "```text\n<name> is required.\n```", "```text\n<name> ist erforderlich.\n```"
            source.write_text(en)
            registry = root / "data/translation-fences"
            with patch.object(fences, "PROJECT", root), patch.object(fences, "REGISTRY", registry):
                errors = []
                self.assertEqual(checker.approved_pre_pairs(source, [en], [de], errors), set())
                self.assertTrue(errors)
                manifest = {"source": str(source.relative_to(root)), "language": "de", "fences": [{"index": 1, "classification": "argument-description", "source_sha256": fences.sha256(en), "target_sha256": fences.sha256(de)}]}
                file = fences.manifest_path(source, "de")
                file.parent.mkdir(parents=True)
                file.write_text(json.dumps(manifest))
                errors = []
                self.assertEqual(checker.approved_pre_pairs(source, [en], [de], errors), {("<name> is required.", "<name> ist erforderlich.")})
                self.assertEqual(errors, [])
                errors = []
                checker.approved_pre_pairs(source, [en], [de.replace("erforderlich", "optional")], errors)
                self.assertTrue(any("reviewed translation" in e for e in errors))

    def test_body_anchors_and_pre_text_are_distinct_from_page_chrome(self):
        page = checker.Page('<html lang="de-DE"><body><nav id="outside"><pre>chrome</pre></nav><main class="td-content"><h2 id="english-id">Deutsch</h2><a id="entry"></a><pre><code>show info\n&lt;name&gt;\n</code></pre></main><span class="td-shell-tree__heading-label"><span>Verwaltungshandbuch</span></span></body></html>')
        self.assertEqual(page.content_ids, ["english-id", "entry"])
        self.assertEqual(page.pre, ["show info\n<name>\n"])
        self.assertEqual(page.dividers, ["Verwaltungshandbuch"])
        self.assertEqual(page.language, ["de-DE"])

    def test_indented_explanation_reviews_are_exact_and_cannot_hide_literals(self):
        source = Path("example.md")
        en = '  fill    Keep the existing hostname.\n\n>>> show info\n  Server: HAProxy\nWait 5 ms.\n'
        de = '  fill    Den vorhandenen Hostnamen beibehalten.\n\n>>> show info\n  Server: HAProxy\n5 ms warten.\n'
        review = {"index": 1, "classification": "mixed-explanation", "source_sha256": fences.sha256(en), "target_sha256": fences.sha256(de), "protected_lines": [">>> show info", "  Server: HAProxy"], "protected_prefixes": ["fill    "], "protected_literals": ["show info"], "review": "Compared hostname preservation, exact command/output and delay."}
        with patch.object(checker, "load_manifest", return_value={"rendered_explanations": [review]}):
            errors = []
            self.assertEqual(checker.validate_pre(source, [en], [de], set(), errors), 1)
            self.assertEqual(errors, [])
            for changed, expected in ((de.replace("5 ms", "6 ms"), "numeric facts"), (de.replace("show info", "show sess"), "protected code/output"), (de.replace("fill    ", "keep    "), "table/list label")):
                # Refreshing a prose hash still cannot waive technical content.
                review["target_sha256"] = fences.sha256(changed)
                errors = []
                checker.validate_pre(source, [en], [changed], set(), errors)
                self.assertTrue(any(expected in e for e in errors), errors)
            errors = []
            checker.validate_pre(source, [en], [de], set(), errors)
            self.assertTrue(any("reviewed translation" in e for e in errors))
            errors = []
            checker.validate_pre(source, [en + "More text.\n"], [de], set(), errors)
            self.assertTrue(any("English explanation changed" in e for e in errors))

    def test_unregistered_duplicate_and_unused_indented_reviews_fail(self):
        source = Path("example.md")
        en, de = 'The server must use TLS.\n', 'Der Server muss TLS verwenden.\n'
        review = {"index": 1, "classification": "mixed-explanation", "source_sha256": fences.sha256(en), "target_sha256": fences.sha256(de), "review": "Compared mandatory TLS."}
        for payload, targets, expected in (({}, [de], "without an exact"), ({"rendered_explanations": [review, review]}, [de], "duplicate"), ({"rendered_explanations": [review]}, [en], "unused/stale"), ({"rendered_explanations": [dict(review, index=2)]}, [de], "invalid"), ({"rendered_explanations": [review]}, [], "block count")):
            with patch.object(checker, "load_manifest", return_value=payload):
                errors = []
                checker.validate_pre(source, [en], targets, set(), errors)
                self.assertTrue(any(expected in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
