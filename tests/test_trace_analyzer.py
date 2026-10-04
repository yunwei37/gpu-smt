#!/usr/bin/env python3

from pathlib import Path
import tempfile
import unittest

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import analyze_smt_trace as ast  # noqa: E402


class TraceAnalyzerTests(unittest.TestCase):
    def test_normalization_preserves_quoted_identity(self):
        self.assertEqual(ast.normalize('(assert  (= |x  y| "a  b"))'), '(assert (= |x  y| "a  b"))')
        self.assertNotEqual(ast.normalize('(echo "a  b")'), ast.normalize('(echo "a b")'))

    def test_cross_task_reuse_excludes_same_task(self):
        import analyze_verus_jobs as jobs
        from collections import Counter
        def q(task):
            return dict(task_id=task,project='P',identity=task,context=['a'],counter=Counter(['a']),sizes={'a':3},bytes=3,digest='same')
        result=jobs.analyze([q('A'),q('A'),q('B')],16)
        self.assertEqual(result['comparable_queries'],1)
        self.assertEqual(result['exact_cross_task_hits'],1)
        self.assertEqual(result['rows'][1]['prefix_commands'],0)

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
        self.assertEqual(
            ast.command_head(ast.normalize(cmds[-1])),
            "check-sat",
        )

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
        self.assertEqual(
            sum(c.startswith("(assert") for c in qs[0]),
            1,
        )
        self.assertEqual(
            sum(c.startswith("(assert") for c in qs[1]),
            2,
        )
        self.assertEqual(
            sum(c.startswith("(assert") for c in qs[2]),
            1,
        )
        self.assertEqual(
            ast.digest_query(qs[0]),
            ast.digest_query(qs[2]),
        )

    def test_context_overlap_can_detect_reordered_commands(self):
        a = [
            "(declare-fun x () Int)",
            "(declare-fun y () Int)",
            "(assert (> x 0))",
            "(assert (> y 0))",
        ]
        b = [
            "(declare-fun y () Int)",
            "(declare-fun x () Int)",
            "(assert (> y 0))",
            "(assert (> x 1))",
        ]
        self.assertEqual(ast.lcp_len(a, b), 0)
        # Both declarations and the assertion about y occur in both contexts.
        self.assertEqual(ast.multiset_common_count(a, b), 3)

    def test_byte_overlap_counts_duplicate_commands(self):
        a = ["(assert a)", "(assert a)", "(assert b)"]
        b = ["(assert a)", "(assert a)", "(assert c)"]
        expected = 2 * (len("(assert a)") + 1)
        self.assertEqual(ast.multiset_common_count(a, b), 2)
        self.assertEqual(ast.multiset_common_bytes(a, b), expected)

    def test_scoped_declarations_are_removed_and_order_is_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "scoped.smt2"
            path.write_text("(declare-const x Int) (assert (> x 0)) (push 1) "
                            "(declare-const y Int) (assert (= y x)) (check-sat) "
                            "(get-info :all-statistics) (pop 1) (check-sat)")
            first, second = ast.snapshot_queries(path)
            self.assertEqual(first[:3], ["(declare-const x Int)", "(assert (> x 0))", "(declare-const y Int)"])
            self.assertNotIn("(declare-const y Int)", second)
            self.assertNotIn("(assert (= y x))", second)
            self.assertNotIn("(get-info :all-statistics)", second)

    def test_global_declarations_survive_pop_and_reset_clears_context(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "global.smt2"
            path.write_text("(set-option :global-decls true) (push 1) "
                            "(declare-const x Int) (pop 1) (check-sat) (reset) (check-sat)")
            first, second = ast.snapshot_queries(path)
            self.assertIn("(declare-const x Int)", first)
            self.assertEqual(second, ["(check-sat)"])


if __name__ == "__main__":
    unittest.main()
