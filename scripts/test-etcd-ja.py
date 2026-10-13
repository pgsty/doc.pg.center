#!/usr/bin/env python3
"""Mutation tests for the Japanese etcd source and rendered acceptance gates.

Use a complete production build with --rendered-dir. All mutations are confined
to mocked reads/enumeration; repository sources and build outputs stay intact.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch


PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / "content/docs/etcd"
MANIFEST = PROJECT / "data/translation-reviews/etcd.ja.json"
RENDERED = None


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, PROJECT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parity = load_module("test_etcd_ja_parity", "check-japanese-parity.py")
rendered = load_module("test_etcd_ja_rendered", "check-etcd-ja-rendered.py")


@contextlib.contextmanager
def changed_reads(replacements):
    original = Path.read_text

    def read(path, *args, **kwargs):
        if path in replacements:
            return replacements[path]
        return original(path, *args, **kwargs)

    with patch.object(Path, "read_text", read):
        yield


def run_main(module, arguments):
    output = io.StringIO()
    with patch.object(sys, "argv", [module.__file__, *arguments]), \
            contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        status = module.main()
    return status, output.getvalue()


class SourceAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text())
        cls.reviews = {entry["path"]: entry for entry in cls.manifest["pages"]}

    def pair_errors(self, relative, transform=None, review_changes=None):
        source = CONTENT / relative
        target = source.with_suffix(".ja.md")
        original = target.read_text()
        changed = transform(original) if transform else original
        if transform:
            self.assertNotEqual(original, changed, "mutation no longer matches its fixture")
        review = copy.deepcopy(self.reviews[relative])
        # A mutation must fail its content check, not merely a stale review hash.
        review["translation_sha256"] = parity.digest(changed)
        review.update(review_changes or {})
        with changed_reads({target: changed}):
            errors = parity.validate_pair(source, target, RENDERED, review)
        return errors

    def reject(self, relative, before, after, diagnostic):
        def transform(text):
            self.assertIn(before, text)
            return text.replace(before, after, 1)

        errors = self.pair_errors(relative, transform)
        self.assertFalse(any("does not match" in error for error in errors), errors)
        self.assertTrue(any(diagnostic in error for error in errors), errors)

    def source_main(self):
        return run_main(parity, [
            "--component", "etcd", "--rendered-dir", str(RENDERED),
            "--review-manifest", str(MANIFEST),
        ])

    def test_current_source_and_review_manifest_pass(self):
        status, output = self.source_main()
        self.assertEqual(status, 0, output)

    def test_english_directory_metadata_is_rejected(self):
        relative = "op-guide/_index.md"
        english = (CONTENT / relative).read_text()
        errors = self.pair_errors(relative, lambda _: english)
        for field in ("title", "description", "categories"):
            self.assertIn(f"unlocalized display metadata: {field}", errors)
        self.assertFalse(any("does not match" in error for error in errors), errors)

    def test_protected_metadata_cannot_change(self):
        self.reject("op-guide/_index.md", "weight: 4000", "weight: 4001",
                    "protected metadata changed: weight")

    def test_commands_outputs_and_quoted_comments_cannot_change(self):
        cases = [
            ("op-guide/recovery.md", "snapshot save snapshot.db\n",
             "snapshot restore snapshot.db\n"),
            ("op-guide/recovery.md", "| 7ef846e |", "| deadbee |"),
            ("op-guide/maintenance.md", "# compact up to revision 3",
             "# リビジョン3までコンパクションする"),
            ("op-guide/configuration.md", "> # Correct: 10 minutes in nanoseconds",
             "> # 10分をナノ秒で指定"),
        ]
        for relative, before, after in cases:
            with self.subTest(page=relative, literal=before):
                self.reject(relative, before, after, "fenced code/configuration/output changed")

    def test_inline_technical_literals_cannot_change(self):
        self.reject("op-guide/recovery.md", "`--bump-revision`", "`--bump-revisions`",
                    "inline technical literals changed")

    def test_storage_table_field_spelling_is_protected(self):
        self.reject("learning/persistent-storage-files.md", "authRevision", "authRevisoin",
                    "storage HTML table bucket/key/type identifiers changed")

    def test_public_english_anchors_cannot_change(self):
        self.reject("op-guide/recovery.md", "{#snapshotting-the-keyspace}",
                    "{#snapshotting-the-wrong-keyspace}",
                    "English rendered heading IDs not preserved")

    def test_signed_numeric_values_cannot_change(self):
        cases = [
            ("benchmarks/etcd-2-2-0-rc-benchmarks.md", "(-5%)", "(+5%)"),
            ("upgrades/upgrade_3_2.md", "TTL=-1", "TTL=1"),
        ]
        for relative, before, after in cases:
            with self.subTest(page=relative):
                self.reject(relative, before, after, "numeric facts need review")

    def test_numeric_table_values_cannot_move_between_cells(self):
        relative = "benchmarks/etcd-2-2-0-rc-benchmarks.md"

        def swap(text):
            first, second = "2804 (-5%)", "17816 (+0%)"
            self.assertEqual(text.count(first), 1)
            self.assertEqual(text.count(second), 1)
            return text.replace(first, "REGRESSION_CELL").replace(second, first).replace(
                "REGRESSION_CELL", second)

        errors = self.pair_errors(relative, swap)
        self.assertTrue(any("numeric table value missing/moved" in error for error in errors), errors)
        self.assertFalse(any("numeric facts need review" in error for error in errors), errors)
        self.assertFalse(any("does not match" in error for error in errors), errors)

    def test_review_hashes_bind_both_current_files(self):
        source = CONTENT / "op-guide/_index.md"
        target = source.with_suffix(".ja.md")
        review = self.reviews["op-guide/_index.md"]
        for path, diagnostic in [
            (source, "semantic review does not match CURRENT English source"),
            (target, "semantic review does not match current Japanese translation"),
        ]:
            with self.subTest(path=path.name):
                with changed_reads({path: path.read_text() + "\n"}):
                    errors = parity.validate_pair(source, target, RENDERED, review)
                self.assertEqual(errors, [diagnostic])

    def test_review_status_notes_and_reviewer_are_required(self):
        for field, value in [("status", "draft"), ("notes", []), ("reviewer", "")]:
            with self.subTest(field=field):
                errors = self.pair_errors("op-guide/_index.md", review_changes={field: value})
                self.assertIn("separate whole-page semantic review is missing", errors)

    def test_missing_translation_is_rejected(self):
        missing = CONTENT / "op-guide/_index.ja.md"
        original_glob, original_exists = Path.rglob, Path.exists

        def glob(path, pattern, *args, **kwargs):
            values = original_glob(path, pattern, *args, **kwargs)
            return (value for value in values if value != missing)

        def exists(path):
            return False if path == missing else original_exists(path)

        with patch.object(Path, "rglob", glob), patch.object(Path, "exists", exists):
            status, output = self.source_main()
        self.assertEqual(status, 1, output)
        self.assertIn("missing translation: op-guide/_index.md", output)

    def test_orphan_translation_is_rejected(self):
        original_glob = Path.rglob
        orphan = CONTENT / "__regression_orphan.ja.md"

        def glob(path, pattern, *args, **kwargs):
            values = list(original_glob(path, pattern, *args, **kwargs))
            if path == CONTENT and pattern in {"*.md", "*.ja.md"}:
                values.append(orphan)
            return iter(values)

        with patch.object(Path, "rglob", glob):
            status, output = self.source_main()
        self.assertEqual(status, 1, output)
        self.assertIn("orphan translation: __regression_orphan.md", output)

    def test_missing_semantic_review_is_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["pages"] = [entry for entry in manifest["pages"]
                             if entry["path"] != "op-guide/_index.md"]
        with changed_reads({MANIFEST: json.dumps(manifest, ensure_ascii=False)}):
            status, output = self.source_main()
        self.assertEqual(status, 1, output)
        self.assertIn("review manifest must cover each current English page exactly once", output)
        self.assertIn("op-guide/_index.md: no separate semantic review", output)


class RenderedAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.print_path = RENDERED / "ja/_print/docs/etcd/index.html"
        cls.printed = cls.print_path.read_text()

    def rendered_main(self, printed=None):
        replacements = {} if printed is None else {self.print_path: printed}
        with changed_reads(replacements):
            return run_main(rendered, ["--rendered-dir", str(RENDERED)])

    def test_current_production_build_passes(self):
        status, output = self.rendered_main()
        self.assertEqual(status, 0, output)

    def test_print_paragraph_loss_is_rejected(self):
        # Select actual source prose, avoiding print navigation and page chrome.
        source = CONTENT / "op-guide/failures.md"
        individual = RENDERED / rendered.route(source, True).lstrip("/") / "index.html"
        paragraphs = re.findall(r"<p(?:\s[^>]*)?>[^<]{40,}</p>", individual.read_text())
        self.assertTrue(paragraphs, "rendered prose fixture is missing")
        paragraph = next((value for value in paragraphs if value in self.printed), None)
        self.assertIsNotNone(paragraph, "print fixture lacks the individual page paragraph")
        changed = self.printed.replace(paragraph, "", 1)
        status, output = self.rendered_main(changed)
        self.assertEqual(status, 1, output)
        self.assertIn("print: full body missing or changed: /ja/docs/etcd/op-guide/failures/", output)

    def test_print_image_loss_is_rejected(self):
        changed, count = re.subn(r"<img\b[^>]*>", "", self.printed)
        self.assertGreater(count, 0, "rendered image fixture is missing")
        # Removing images leaves body text and preformatted output unchanged.
        self.assertEqual(rendered.Page(self.printed).bodies, rendered.Page(changed).bodies)
        status, output = self.rendered_main(changed)
        self.assertEqual(status, 1, output)
        self.assertIn("print: images or localized alt text differ from individual pages", output)

    def test_print_fragment_typo_is_rejected(self):
        match = re.search(r"\bhref=(?P<quote>[\"']?)(?P<href>#pg-[^\"'\s>]+)(?P=quote)",
                          self.printed)
        self.assertIsNotNone(match, "print fragment link fixture is missing")
        broken = "#regression-missing-print-anchor"
        original = rendered.Page(self.printed)
        self.assertNotIn(broken[1:], original.ids)
        changed = self.printed[:match.start("href")] + broken + self.printed[match.end("href"):]
        changed_page = rendered.Page(changed)
        self.assertEqual(original.bodies, changed_page.bodies)
        self.assertEqual(original.ids, changed_page.ids)
        status, output = self.rendered_main(changed)
        self.assertEqual(status, 1, output)
        self.assertIn("print: broken internal anchor", output)


def main():
    global RENDERED
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rendered-dir", required=True, type=Path)
    args = parser.parse_args()
    RENDERED = args.rendered_dir.resolve()
    if not RENDERED.is_dir():
        parser.error(f"rendered directory does not exist: {RENDERED}")
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
