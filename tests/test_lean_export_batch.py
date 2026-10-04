#!/usr/bin/env python3

from pathlib import Path
import tempfile
import unittest

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bench"))

import lean_export_batch as leb  # noqa: E402


class ExpandTests(unittest.TestCase):
    def test_expand_dedups_and_preserves_order(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            (base / "b.ndjson").write_text("")
            (base / "a.ndjson").write_text("")
            files = leb.expand([str(base / "*.ndjson"), str(base / "a.ndjson")])
            self.assertEqual([Path(f).name for f in files], ["a.ndjson", "b.ndjson"])

    def test_expand_duplicate_repeats_without_reordering_dedup(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            (base / "a.ndjson").write_text("")
            (base / "b.ndjson").write_text("")
            files = leb.expand([str(base / "*.ndjson")], duplicate=3)
            self.assertEqual(
                [Path(f).name for f in files],
                ["a.ndjson", "b.ndjson"] * 3,
            )

    def test_expand_empty_when_no_match(self):
        self.assertEqual(leb.expand(["/nonexistent-dir/*.ndjson"]), [])


if __name__ == "__main__":
    unittest.main()
