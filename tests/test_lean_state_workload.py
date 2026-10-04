import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'bench'))
from lean_repl_workload import classify
from lean_dag_pack import pack
from verus_session_replay import decisions


class SMTStatusTests(unittest.TestCase):
    def test_unknown_is_preserved_in_query_order(self):
        self.assertEqual(decisions('unsat\n(:reason-unknown "unknown")\nunknown\nsat\n'),
                         ['unsat','unknown','sat'])

    def test_protocol_error_is_not_a_semantic_rejection(self):
        with self.assertRaisesRegex(RuntimeError,'protocol error'):
            decisions('(error "unknown constant")\n')


class ProofStatusTests(unittest.TestCase):
    def test_incomplete_proof_is_distinct_from_type_error(self):
        for quote in ["'", '`']:
            self.assertEqual(classify({'env':0,'messages':[{'severity':'warning',
                'data':f'declaration uses {quote}sorry{quote}'}]}), 'incomplete')
        self.assertEqual(classify({'env':1,'messages':[{'severity':'error','data':'type mismatch'}]}), 'rejected')
        self.assertEqual(classify({'env':2,'sorries':[{'goal':'False'}]}), 'incomplete')
        self.assertEqual(classify({'env':3}), 'accepted')


class DAGValidationTests(unittest.TestCase):
    def test_forward_reference_cannot_enter_gpu_schedule(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/'bad.ndjson';out=Path(d)/'bad.dag'
            src.write_text(json.dumps({'ie':0,'app':{'fn':0,'arg':1}})+'\n')
            with self.assertRaisesRegex(ValueError,'forward'):
                pack(src,out)

    def test_sparse_indices_are_explicitly_unsupported(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/'sparse.ndjson';out=Path(d)/'sparse.dag'
            src.write_text(json.dumps({'ie':1,'sort':0})+'\n')
            with self.assertRaisesRegex(ValueError,'dense'):
                pack(src,out)
