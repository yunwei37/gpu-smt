import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bench"))
from lean_persistent_bench import decision


class DecisionTests(unittest.TestCase):
    def test_process_failure_cannot_count_as_acceptance(self):
        self.assertEqual(decision(dict(timed_out=False, returncode=-9, stdout="Accepted 1 declarations.")), "error")

    def test_acceptance_requires_success_and_official_marker(self):
        self.assertEqual(decision(dict(timed_out=False, returncode=0, stdout="Accepted 1 declarations.\n")), "accepted")
        self.assertEqual(decision(dict(timed_out=False, returncode=0, stdout="Not Accepted")), "error")

    def test_timeout_and_decline_are_not_proof_rejection(self):
        self.assertEqual(decision(dict(timed_out=True, returncode=None, stdout="")), "timeout")
        self.assertEqual(decision(dict(timed_out=False, returncode=2, stdout="")), "error")
        self.assertEqual(decision(dict(timed_out=False, returncode=1, stdout="")), "rejected")
