#!/usr/bin/env python3

from pathlib import Path
import tempfile
import unittest

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import analyze_smt_trace as ast  # noqa: E402


class TraceAnalyzerTests(unittest.TestCase):
    def test_split_commands_handles_comments_and_strings(self):
        text = """
        ; comment
        (set-logic QF_BV)
        (declare-fun |x(y)| () String)
        (assert (= |x(y)| "a(b)c"))
        (check-sat)
        """
        cmds = ast.split_commands(text)
        self.assertEqual(len(cmds), 4)
        self.assertEqual(ast.command_head(ast.normalize(cmds[-1])), "check-sat")

    def test_push_pop_reconstructs_active_assertions(self):
        text = """
        (set-logic QF_BV)
        (declare-fun x () (_ BitVec 8))
        (assert (= x #x01))
        (check-sat)
        (push 1)
        (assert (= x #x02))
        (check-sat)
        (pop 1)
        (check-sat)
        """
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "trace.smt2"
            p.write_text(text, encoding="utf-8")
            qs = ast.snapshot_queries(p)

        self.assertEqual(len(qs), 3)
        self.assertEqual(sum(c.startswith("(assert") for c in qs[0]), 1)
        self.assertEqual(sum(c.startswith("(assert") for c in qs[1]), 2)
        self.assertEqual(sum(c.startswith("(assert") for c in qs[2]), 1)
        self.assertEqual(ast.digest_query(qs[0]), ast.digest_query(qs[2]))


if __name__ == "__main__":
    unittest.main()
