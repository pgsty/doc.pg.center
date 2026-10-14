#!/usr/bin/env python3
"""Mutation tests for the current-source Japanese HAProxy acceptance gate."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("haproxy_ja", Path(__file__).with_name("check-haproxy-ja.py"))
assert spec and spec.loader
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

EN = '''---
title: "Timeout"
description: "A timeout example"
weight: 10
aliases: [/haproxy/test/]
---
## Timeout {#timeout}

The default is 10 seconds. Use `timeout connect`.

```text
timeout connect 10s
```

[Cache](/docs/haproxy/cache/#6-cache)
'''
JA = '''---
title: "タイムアウト"
description: "タイムアウトの例"
weight: 10
aliases: [/haproxy/test/]
---
## タイムアウト {#timeout}

デフォルトは10秒です。`timeout connect`を使用します。

```text
timeout connect 10s
```

[キャッシュ](/ja/docs/haproxy/cache/#6-cache)
'''


class AcceptanceTests(unittest.TestCase):
    def errors(self, target=JA):
        with tempfile.TemporaryDirectory(prefix="haproxy-ja-test-") as directory:
            root = Path(directory)
            component = root / "haproxy"
            component.mkdir()
            source, translated = component / "test.md", component / "test.ja.md"
            source.write_text(EN)
            translated.write_text(target)
            audit = check.Audit()
            audit.exceptions = []
            with patch.object(check, "DOCS", root):
                check.validate_pair(source, translated, audit)
            return audit.errors

    def test_accepts_translated_units_and_local_routes(self):
        self.assertEqual(self.errors(), [])

    def test_rejects_changed_metadata(self):
        self.assertTrue(any("protected metadata" in error for error in self.errors(JA.replace("weight: 10", "weight: 11"))))

    def test_rejects_changed_code(self):
        self.assertTrue(any("fenced code/configuration/output" in error for error in self.errors(JA.replace("connect 10s", "connect 11s"))))

    def test_rejects_changed_default_and_unit(self):
        errors = self.errors(JA.replace("10秒", "11ミリ秒"))
        self.assertTrue(any("numeric facts" in error for error in errors))
        self.assertTrue(any("numeric units" in error for error in errors))

    def test_rejects_changed_public_anchor(self):
        self.assertTrue(any("heading levels and English IDs" in error for error in self.errors(JA.replace("{#timeout}", "{#time-out}"))))

    def test_rejects_english_fallback(self):
        self.assertTrue(any("component link still uses English" in error for error in self.errors(JA.replace("/ja/docs/", "/docs/"))))

    def test_rejects_untranslated_explanation(self):
        target = JA.replace("デフォルトは10秒です。`timeout connect`を使用します。", "The default is 10 seconds. Use `timeout connect`.")
        self.assertTrue(any("English prose" in error for error in self.errors(target)))

    def test_hyphenated_terms_are_not_negative_defaults(self):
        self.assertEqual(check.numeric_tokens("non-100 response; layer-1"), check.numeric_tokens("100以外のレスポンス、レイヤー1"))
        self.assertNotEqual(check.numeric_tokens("default -1"), check.numeric_tokens("デフォルト1"))
        self.assertEqual(check.quantity_tokens("a 4-byte hash"), check.quantity_tokens("4バイトのハッシュ"))
        self.assertEqual(check.quantity_tokens("the 28 lowest bits"), check.quantity_tokens("下位28ビット"))
        self.assertEqual(check.quantity_tokens("3 or more seconds"), check.quantity_tokens("3秒以上"))
        self.assertEqual(check.numeric_tokens("2^30 ~= 1.07 billion"), check.numeric_tokens("2^30 ~= 10.7億"))
        self.assertNotEqual(check.numeric_tokens("1.07 billion"), check.numeric_tokens("1.07億"))

    def test_rejects_changed_bare_url(self):
        self.assertNotEqual(check.absolute_urls("See <https://example.org/v1/>."), check.absolute_urls("<https://example.org/v2/>を参照。"))
        self.assertEqual(check.absolute_urls("See https://example.org/v1/."), check.absolute_urls("https://example.org/v1/を参照。"))

    def test_reviewed_prose_cannot_change_protected_argument(self):
        source = '```text\n<timeout> is the time in seconds.\n```\n'
        target = '```text\n<delay>は秒単位の時間です。\n```\n'
        path, section = "haproxy/test.md", "fence-0001"
        audit = check.Audit()
        audit.exceptions = [{
            "path": path, "section": section, "check": "fenced code/configuration/output",
            "source_sha256": check.digest(source), "target_sha256": check.digest(target),
            "reason": "Only explanatory prose is translatable.", "classification": "explanatory prose",
            "protected_literals": ["<timeout>"], "protected_lines": [],
        }]
        check.validate_explanatory_fence(source, target, path, section, audit)
        self.assertTrue(any("protected literal/line changed" in error for error in audit.errors))
        self.assertTrue(any("fenced argument placeholders" in error for error in audit.errors))

    def test_review_hash_cannot_authorize_later_changes(self):
        source, target = "English", "日本語"
        audit = check.Audit()
        audit.exceptions = [{
            "path": "haproxy/test.md", "section": "preamble", "check": "English prose",
            "source_sha256": check.digest(source), "target_sha256": check.digest(target),
            "reason": "Precisely reviewed exception.",
        }]
        audit.compare("English prose", source, target + " changed", ["untranslated prose"], [], "haproxy/test.md", "preamble")
        self.assertEqual(len(audit.errors), 1)


if __name__ == "__main__":
    unittest.main()
