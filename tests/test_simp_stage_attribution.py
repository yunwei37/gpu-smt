"""Diagnostic attribution tests; these never execute Lean or infer rejection."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "simp_stage_analysis", ROOT / "bench/lean-failure-profile/simp-all-profile/analyze.py")
ANALYSIS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANALYSIS)


class SimpStageAttribution(unittest.TestCase):
    def analyze(self, events):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.jsonl"
            path.write_text("".join(ANALYSIS.PREFIX + json.dumps(e) + "\n" for e in events))
            return ANALYSIS.analyze_source("candidate", path, {})

    def event(self, kind, **extra):
        return dict(event=kind, invocation_byte=10, phase="hypothesis",
                    round=1, slot=0, **extra)

    def test_return_unwind_and_unknown_remain_distinct(self):
        events = []
        for extra in [{}, {"action_completed": False}, {"action_completed": True}]:
            events.extend([self.event("begin", subject="h"),
                           self.event("end", elapsed_ns=7, **extra)])
        result = self.analyze(events)
        phase = result["observed_phases"][0]
        self.assertEqual((phase["completion_unknown"], phase["unwound_actions"],
                          phase["completed_actions"]), (1, 1, 1))
        self.assertEqual(phase["subjects"], ["h"])
        self.assertEqual((phase["elapsed_ns"], phase["max_elapsed_ns"]), (21, 7))
        self.assertEqual(result["open_phases"], [])
        self.assertEqual(result["unmatched_events"], [])
        self.assertFalse(result["certified_impossible"])

    def test_open_phase_and_repeated_hash_are_not_rejection(self):
        result = self.analyze([
            self.event("begin"),
            self.event("progress", expression_hash_hint=17, used_origins=[]),
            self.event("progress", expression_hash_hint=17, used_origins=[]),
        ])
        self.assertEqual(len(result["open_phases"]), 1)
        self.assertIsNone(result["open_phases"][0]["max_elapsed_ns"])
        self.assertFalse(result["certified_impossible"])

    def test_actual_legacy_native_records_keep_measured_counts(self):
        directory = ROOT / "artifacts/hotspot-mechanisms-2026-10-25/simp-all-profile/qualification-007"
        terminal = json.loads((directory / "terminal.json").read_text())
        old = json.loads((directory / "attribution.json").read_text())
        expected = {r["id"]: r for r in old["sources"]}
        actual_events = 0
        for row in terminal["results"]:
            result = ANALYSIS.analyze_source(row["id"], directory / (row["id"] + ".jsonl"), {})
            prior = expected[row["id"]]
            for key in ["parsed_events", "last_progress", "malformed_event_lines",
                        "unmatched_events", "certified_impossible"]:
                self.assertEqual(result[key], prior[key], row["id"])
            self.assertEqual(result["open_phases"], prior["open_phases"], row["id"])
            self.assertEqual(len(result["observed_phases"]), len(prior["observed_phases"]))
            for phase, baseline in zip(result["observed_phases"], prior["observed_phases"]):
                for key, value in baseline.items():
                    self.assertEqual(phase[key], value, (row["id"], key))
                self.assertEqual(phase["completion_unknown"], phase["ended"])
                self.assertEqual((phase["completed_actions"], phase["unwound_actions"]), (0, 0))
            actual_events += result["parsed_events"]
        self.assertEqual(actual_events, sum(x["parsed_events"] for x in old["sources"]))

    def test_missing_record_is_unavailable(self):
        result = ANALYSIS.analyze_source("missing", None, {})
        self.assertFalse(result["runtime_record_available"])
        self.assertFalse(result["certified_impossible"])


if __name__ == "__main__":
    unittest.main()
