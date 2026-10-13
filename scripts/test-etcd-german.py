#!/usr/bin/env python3
"""Regression checks for the complete German etcd acceptance gate."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("etcd_de_gate", Path(__file__).with_name("check-etcd-german.py"))
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class EtcdGermanAcceptanceTests(unittest.TestCase):
    def test_nested_commands_and_comments_remain_protected(self):
        source = "1. Run:\n\n    ```sh\n    # example\n    etcdctl get key\n    ```\n"
        translation = source.replace("Run", "Ausführen")
        self.assertEqual(gate.fenced_blocks(source), gate.fenced_blocks(translation))
        self.assertNotEqual(gate.fenced_blocks(source), gate.fenced_blocks(translation.replace("# example", "# Beispiel")))
        self.assertNotEqual(gate.fenced_blocks(source), gate.fenced_blocks(translation.replace("get key", "del key")))
        with self.assertRaises(ValueError):
            gate.fenced_blocks("    ```sh\n    etcd\n")
        quoted = "> ```yaml\n> # duration in nanoseconds\n> interval: 600000000000\n> ```\n"
        self.assertEqual(gate.fenced_blocks(quoted), [quoted])
        self.assertNotEqual(gate.fenced_blocks(quoted), gate.fenced_blocks(quoted.replace("# duration", "# Dauer")))
        self.assertEqual(gate.fenced_blocks("```sh\netcd\n````\n"), ["```sh\netcd\n````\n"])

    def test_rendered_body_fingerprint_detects_english_and_missing_prose(self):
        with tempfile.TemporaryDirectory() as folder:
            page = Path(folder) / "index.html"
            page.write_text('<div class="td-content"><h1>Titel</h1><p>Deutsche Erklärung.</p><pre>etcdctl get key</pre></div>')
            original = gate.rendered_body(page)[0]
            page.write_text(page.read_text().replace('Deutsche Erklärung.', 'English explanation.'))
            self.assertNotEqual(original, gate.rendered_body(page)[0])
            page.write_text(page.read_text().replace('<p>English explanation.</p>', ''))
            self.assertNotEqual(original, gate.rendered_body(page)[0])

    def test_numeric_table_cells_cannot_be_swapped(self):
        source = "| count | latency |\n| 64 | 0.7 |\n| 256 | 27.1 |\n"
        translation = source.replace("count", "Anzahl").replace("latency", "Latenz")
        self.assertEqual(gate.table_numbers(source), gate.table_numbers(translation))
        changed = translation.replace("0.7", "TEMP").replace("27.1", "0.7").replace("TEMP", "27.1")
        self.assertNotEqual(gate.table_numbers(source), gate.table_numbers(changed))

    def test_print_block_boundaries_ignore_minifier_whitespace(self):
        normal = '<div class="td-content"><li><p>Ausführen:</p> <div><pre>etcd\n</pre></div></li></div>'
        compact = normal.replace('</p> <div>', '</p><div>')
        normal_section = gate.printing.content_sections(gate.printing.Document(normal))[0]
        compact_section = gate.printing.content_sections(gate.printing.Document(compact))[0]
        self.assertEqual(gate.printing.body_blocks(normal_section), gate.printing.body_blocks(compact_section))
        self.assertIn(('pre', 'etcd\n'), gate.printing.body_blocks(normal_section))

    def test_rendered_links_leads_and_print_titles_remain_bound(self):
        with tempfile.TemporaryDirectory() as folder:
            page = Path(folder) / 'index.html'
            original = '<div class="td-content"><h1>Schnellstart</h1><div class="lead">Beschreibung</div><p><a href="/de/docs/etcd/install/">Installation</a></p></div>'
            page.write_text(original)
            fingerprint = gate.rendered_body(page)[0]
            for changed in (original.replace('/install/', '/faq/'), original.replace('Beschreibung', 'Description')):
                page.write_text(changed)
                self.assertNotEqual(fingerprint, gate.rendered_body(page)[0])
            normal = gate.printing.content_sections(gate.printing.Document(original))[0]
            correct = gate.printing.content_sections(gate.printing.Document(original.replace('Schnellstart', '2.1 - Schnellstart')))[0]
            wrong = gate.printing.content_sections(gate.printing.Document(original.replace('Schnellstart', '2.1 - Quickstart')))[0]
            self.assertEqual(gate.printing.content_metadata(normal), gate.printing.content_metadata(correct, print_title=True))
            self.assertNotEqual(gate.printing.content_metadata(normal), gate.printing.content_metadata(wrong, print_title=True))

    def test_review_freshness_missing_pages_and_orphans_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            content = root / "content/docs/etcd"
            content.mkdir(parents=True)
            source = content / "_index.md"
            target = content / "_index.de.md"
            source.write_text("---\ntitle: Guide\n---\n")
            target.write_text("---\ntitle: Anleitung\n---\n")
            record = root / "review.json"
            row = {"source": "content/docs/etcd/_index.md", "source_sha256": gate.digest(source), "target_sha256": gate.digest(target), "review_status": "passed"}
            record.write_text(json.dumps({"pages": [row]}))
            with patch.object(gate, "PROJECT", root), patch.object(gate, "CONTENT", content), patch.object(gate, "RECORD", record), patch.object(gate.parity, "PROJECT", root), patch.object(gate.parity, "read_source", side_effect=lambda path, *_args, **_kwargs: (path.read_text(), None)), patch.object(sys, "argv", ["check-etcd-german.py"]), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(gate.main(), 0)
                target.write_text(target.read_text() + "Zusatz\n")
                self.assertEqual(gate.main(), 1)
                target.unlink()
                self.assertEqual(gate.main(), 1)
                target.write_text("---\ntitle: Anleitung\n---\n")
                (content / "orphan.de.md").write_text(target.read_text())
                self.assertEqual(gate.main(), 1)


if __name__ == "__main__":
    unittest.main()
