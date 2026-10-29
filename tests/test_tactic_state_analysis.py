"""Result-analysis regressions; no native collection or proof verdict substitution."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "state_analysis", ROOT/"bench/lean-failure-profile/state-reuse/analyze.py")
ANALYSIS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANALYSIS)

RUN_SPEC = importlib.util.spec_from_file_location(
    "state_runner", ROOT/"bench/lean-failure-profile/state-reuse/run.py")
RUNNER = importlib.util.module_from_spec(RUN_SPEC)
RUN_SPEC.loader.exec_module(RUNNER)


def source(event, identity="candidate", mode="observe", **fields):
    return dict(event=event, id=identity, mode=mode, **fields)


def begin(call, key=0):
    return dict(event="begin", call=call, key=key, kind="nlinarith",
                capture_ns=10, goal_generation_indexes=[7])


def end(call, outcome="native_error"):
    return dict(event="end", call=call, key=0, outcome=outcome, elapsed_ns=100)


def completed(identity="candidate", mode="observe", **fields):
    return source("candidate_end", identity, mode, native_error=True,
                  diagnostics=fields.pop("diagnostics", []), **fields)


def raw_text(events):
    return "".join((ANALYSIS.PREFIX if "call" in row else "")+json.dumps(row)+"\n"
                   for row in events)


class TacticStateAnalysis(unittest.TestCase):
    def analyze(self, events, **kwargs):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"raw.log"
            path.write_text(raw_text(events))
            return ANALYSIS.analyze_raw(path, **kwargs)

    def test_native_exit_is_operational_only_after_source_begin(self):
        current = ("source", "observe")
        self.assertEqual(RUNNER.native_exit_kind(current, True, None), "native_process_failure")
        self.assertIsNone(RUNNER.native_exit_kind(current, False, None))
        self.assertIsNone(RUNNER.native_exit_kind(None, True, None))
        self.assertEqual(RUNNER.native_exit_kind(current, True, "timeout"), "timeout")
        self.assertEqual(RUNNER.native_exit_kind(current, True, "resource_preempted"),
                         "resource_preempted")

    def test_continuation_retains_resource_queue_and_classifies_unreported_exit(self):
        rows = [dict(id=i, mode="original") for i in ["done", "resource", "timeout", "panic", "pending"]]
        history = [completed("done", "original", segment=0),
                   source("operational_end", "resource", "original", segment=1,
                          status="resource_preempted", exclusive_retry=False),
                   source("operational_end", "timeout", "original", segment=2,
                          status="timeout", exclusive_retry=False)]
        retired = [dict(event="retired", segment=3, exit=1,
                        current=["panic", "original"], source_started=True)]
        pending, retry, derived = RUNNER.continuation_plan(rows, history, retired)
        self.assertEqual([r["id"] for r in pending], ["pending"])
        self.assertEqual([r["id"] for r in retry], ["resource"])
        row, = derived
        self.assertEqual(row["status"], "native_process_failure")
        self.assertTrue(row["derived_from_prior_retirement"])
        self.assertIsNone(row["transport_wall_seconds"])

    def test_continuation_refuses_prior_exit_without_source_begin(self):
        with self.assertRaises(ValueError):
            RUNNER.continuation_plan([dict(id="x", mode="original")], [],
                [dict(segment=0, exit=1, current=["x", "original"], source_started=False)])

    def test_actual_failed_prefix_restores_only_unfinished_cells_and_five_retries(self):
        import gzip
        directory = ROOT/"artifacts/hotspot-mechanisms-2026-10-25/state-reuse-native-20261029/populations/partial-20261029T1233"
        rows = json.loads(gzip.decompress((directory/"input.json.gz").read_bytes()))["candidates"]
        history = [json.loads(s) for s in ANALYSIS.lines(directory/"run/results.jsonl.gz")]
        lifecycle = [json.loads(s) for s in ANALYSIS.lines(directory/"run/lifecycle.jsonl.gz")]
        retired = []
        for old in lifecycle:
            if old["event"] != "retired":
                continue
            if old.get("current") and not old.get("operational"):
                raw = directory/("run/segment-%04d/raw.log.gz" % old["segment"])
                starts = []
                for line in ANALYSIS.lines(raw):
                    if line.startswith("{"):
                        value = json.loads(line)
                        if value.get("event") == "candidate_begin":
                            starts.append([value["id"], value["mode"]])
                old = dict(old, source_started=old["current"] in starts)
            retired.append(old)
        pending, retry, derived = RUNNER.continuation_plan(rows, history, retired)
        self.assertEqual((len(rows), len(history), len(pending), len(retry), len(derived)),
                         (8031, 2640, 5390, 5, 1))
        self.assertEqual(derived[0]["id"], "proofnet-5879")
        self.assertNotIn(("proofnet-5879", "original"),
                         {(r["id"], r["mode"]) for r in pending})

    def test_derived_prior_attempt_is_explicit_not_an_unresolved_exit_or_tactic_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            row = source("operational_end", "panic", "original", segment=19,
                         status="native_process_failure", exclusive_retry=False,
                         derived_from_prior_retirement=True, transport_wall_seconds=None)
            old = dict(event="retired", segment=19, exit=1,
                       current=["panic", "original"], operational=None)
            (path/"results.jsonl").write_text(json.dumps(row)+"\n")
            (path/"lifecycle.jsonl").write_text(json.dumps(old)+"\n")
            result = ANALYSIS.analyze_collection(path)
            self.assertEqual(len(result["derived_prior_attempts"]), 1)
            self.assertEqual(result["unresolved_native_exits"], [])
            self.assertEqual(result["repeated_ordinary_error_occurrences"], 0)
            self.assertEqual(result["final_outcomes"],
                             [{"mode": "original", "status": "native_process_failure", "count": 1}])

    def test_retained_native_positive_and_changed_inputs(self):
        directory = ROOT/"docs/tmp/build-and-evaluate/step-0131-20261029T091211+0000/experiment-001"
        result = ANALYSIS.analyze_raw(
            directory/"input-generation-qualification/command-4.log.gz")
        self.assertEqual(result["native_sources"], 30)
        self.assertEqual(result["completed_observations"], 10)
        self.assertEqual(result["repeated_ordinary_error_occurrences"], 1)
        self.assertEqual(result["cross_source_repeated_ordinary_errors"], 1)
        self.assertEqual(result["within_source_repeated_ordinary_errors"], 0)
        row, = result["repeats"]
        self.assertEqual(row["prior_source"], ("arith-failure-a", "observe"))
        self.assertEqual(row["source"], ("arith-failure-b", "observe"))
        self.assertEqual(row["outcome"], "native_error")
        self.assertEqual(result["errors"], [])
        self.assertFalse(result["complete_replay_certification"])
        self.assertIsNone(result["complete_state_hit_count"])

    def test_retained_rejected_source_really_reaches_arithmetic_failure(self):
        directory = ROOT/"artifacts/hotspot-mechanisms-2026-10-25/state-reuse-native-20261029/qualification/real-preflight"
        result = ANALYSIS.analyze_collection(directory)
        self.assertEqual(result["final_cells_returned"], 6)
        segment = result["segments"][0]
        self.assertEqual(segment["completed_observations"], 4)
        cost = segment["observed_cost_by_kind"]["nlinarith"]
        self.assertEqual(cost["completed"], 1)
        self.assertEqual(cost["outcomes"], {"native_error": 1})
        self.assertEqual(segment["completed_observe_source_coverage"]["sources_with_runtime_observations"], 2)

    def test_retained_unresolved_local_is_unreached_not_unsupported_hit(self):
        directory = ROOT/"artifacts/hotspot-mechanisms-2026-10-25/state-reuse-native-20261029/qualification/input-generation-preflight"
        result = ANALYSIS.analyze_collection(directory)["segments"][0]
        coverage = result["completed_observe_source_coverage"]
        self.assertEqual(coverage["sources"], 5)
        self.assertEqual(coverage["sources_with_runtime_observations"], 4)
        self.assertEqual(coverage["wrapped_but_unreached_sources"], ["unresolved-local"])
        self.assertEqual(coverage["wrapped_but_unreached_outer_units"], 1)
        self.assertEqual(result["unsupported_inputs"], 0)
        self.assertEqual(result["input_eligibility_counts"], {"observed_input_only": 5})
        kinds = result["observed_cost_by_kind"].values()
        self.assertEqual(sum(k["completed"] for k in kinds), result["completed_observations"])
        self.assertAlmostEqual(sum(k["completed_action_ns"] for k in kinds)/1e9,
                               result["observed_action_seconds"])

    def test_repeated_runtime_calls_are_not_subtracted_from_syntax_units(self):
        result = self.analyze([
            source("candidate_begin", "unreached"),
            completed("unreached", wrapped_outer_units=2),
            source("candidate_begin", "repeated"), begin(0), end(0), begin(1), end(1),
            completed("repeated", wrapped_outer_units=1),
            source("candidate_begin", "no-wrapper"),
            completed("no-wrapper", wrapped_outer_units=0),
        ])
        coverage = result["completed_observe_source_coverage"]
        self.assertEqual(coverage["sources"], 3)
        self.assertEqual(coverage["wrapped_but_unreached_sources"], ["unreached"])
        self.assertEqual(coverage["wrapped_but_unreached_outer_units"], 2)
        self.assertEqual(coverage["sources_with_zero_wrapped_outer_units"], 1)
        self.assertEqual(result["observed_cost_by_kind"]["nlinarith"]["begins"], 2)

    def test_unsupported_and_open_calls_keep_their_kind_cost_denominator(self):
        unsupported = dict(begin(0, None), eligibility="unresolved_target")
        opened = dict(begin(1), eligibility="observed_input_only")
        result = self.analyze([source("candidate_begin"), unsupported, end(0),
                               opened, completed(wrapped_outer_units=2)])
        self.assertEqual(result["input_eligibility_counts"],
                         {"unresolved_target": 1, "observed_input_only": 1})
        cost = result["observed_cost_by_kind"]["nlinarith"]
        self.assertEqual((cost["begins"], cost["completed"], cost["open"]), (2, 1, 1))
        self.assertEqual((cost["capture_ns"], cost["completed_action_ns"]), (20, 100))
        self.assertEqual(cost["unsupported_inputs"], 1)
        self.assertEqual(result["repeated_ordinary_error_occurrences"], 0)

    def test_return_resource_limit_and_open_call_are_not_reusable_errors(self):
        result = self.analyze([
            source("candidate_begin"), begin(0), end(0, "returned"),
            begin(1), end(1, "heartbeat_limit"), begin(2),
            completed(),
        ])
        self.assertEqual(result["repeated_ordinary_error_occurrences"], 0)
        self.assertEqual(result["outcomes"], {"returned": 1, "heartbeat_limit": 1})
        self.assertEqual(result["open_observations"], [2])

    def test_prior_must_finish_before_repeated_call_starts(self):
        result = self.analyze([
            source("candidate_begin"), begin(0), begin(1), end(1), end(0), completed()])
        self.assertEqual(result["completed_input_match_occurrences"], 0)

    def test_outcome_unstable_key_gets_no_failure_cost_credit(self):
        result = self.analyze([
            source("candidate_begin"), begin(0), end(0), begin(1), end(1, "returned"),
            begin(2), end(2), completed()])
        self.assertEqual(result["unstable_input_keys"], [0])
        self.assertEqual(result["repeated_ordinary_error_occurrences"], 0)
        self.assertEqual(result["observed_repeated_error_wall_seconds"], 0)

    def test_wrapped_allocation_diagnostic_is_conservatively_excluded(self):
        result = self.analyze([
            source("candidate_begin"), begin(0), end(0), begin(1), end(1),
            completed(diagnostics=[{"severity": "error", "text": "nested error: bad_alloc"}])])
        self.assertEqual(result["excluded_operational_or_limit_calls"], 2)
        self.assertEqual(result["repeated_ordinary_error_occurrences"], 0)

    def test_observer_without_completed_source_is_unknown_not_a_hit(self):
        result = self.analyze([source("candidate_begin"), begin(0), end(0),
                               begin(1), end(1)])
        self.assertEqual(result["repeated_ordinary_error_occurrences"], 0)
        self.assertEqual(result["excluded_operational_or_limit_calls"], 2)

    def test_retained_real_watchdog_injection_preserves_all_attempts(self):
        directory = ROOT/"artifacts/hotspot-mechanisms-2026-10-25/state-reuse-native-20261029/qualification/safe-injection"
        result = ANALYSIS.analyze_collection(directory)
        self.assertTrue(result["collection_complete"])
        self.assertEqual(result["final_cells_returned"], 2)
        self.assertEqual(result["watchdog_events"], 4)
        self.assertEqual(result["exclusive_retry_attempts"], 2)
        self.assertEqual(result["attempt_outcomes"],
                         [{"mode": "observe", "status": "resource_preempted", "count": 4}])
        self.assertEqual(result["final_outcomes"],
                         [{"mode": "observe", "status": "resource_preempted", "count": 2}])
        self.assertEqual(result["repeated_ordinary_error_occurrences"], 0)

    def test_complete_marker_without_all_planned_cells_remains_incomplete(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            row = completed(segment=0, exclusive_retry=False)
            (path/"results.jsonl").write_text(json.dumps(row)+"\n")
            (path/"terminal.json").write_text(json.dumps({"state": "complete", "planned": 2}))
            (path/"client-exit.json").write_text(json.dumps({"state": "returned", "error": None}))
            self.assertFalse(ANALYSIS.analyze_collection(path)["collection_complete"])

    def test_process_local_key_ids_do_not_join_between_segments(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            rows = []
            for index in range(2):
                name = "candidate-"+str(index)
                segment = path/("segment-%04d" % index)
                segment.mkdir()
                row = completed(name, segment=index, exclusive_retry=False)
                rows.append(row)
                (segment/"raw.log").write_text(raw_text([
                    source("candidate_begin", name), begin(0), end(0), row]))
            (path/"results.jsonl").write_text("".join(json.dumps(r)+"\n" for r in rows))
            result = ANALYSIS.analyze_collection(path)
            self.assertFalse(result["collection_complete"])
            self.assertEqual(len(result["segments"]), 2)
            self.assertEqual(result["repeated_ordinary_error_occurrences"], 0)

    def test_late_native_completion_does_not_erase_timeout(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            segment = path/"segment-0000"
            segment.mkdir()
            native = completed(segment=0, exclusive_retry=False)
            (segment/"raw.log").write_text(raw_text([
                source("candidate_begin"), begin(0), end(0), begin(1), end(1), native]))
            late = dict(native, event="late_candidate_end")
            timeout = source("operational_end", status="timeout", segment=0,
                             exclusive_retry=False)
            (path/"results.jsonl").write_text(json.dumps(late)+"\n"+json.dumps(timeout)+"\n")
            result = ANALYSIS.analyze_collection(path)
            self.assertEqual(result["late_native_completions"], 1)
            self.assertEqual(result["segments"][0]["completed_observe_source_coverage"]["sources"], 0)
            self.assertEqual(result["final_outcomes"],
                             [{"mode": "observe", "status": "timeout", "count": 1}])
            self.assertEqual(result["repeated_ordinary_error_occurrences"], 0)

    def test_equal_error_flags_do_not_hide_diagnostic_or_limit_differences(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            a = completed(mode="original", segment=0, exclusive_retry=False,
                          diagnostics=[{"text": "ordinary strategy failed", "severity": "error"}])
            b = completed(mode="observe", segment=0, exclusive_retry=False,
                          diagnostics=[{"text": "maximum recursion depth", "severity": "error"}])
            (path/"results.jsonl").write_text(json.dumps(a)+"\n"+json.dumps(b)+"\n")
            result = ANALYSIS.analyze_collection(path)
            self.assertEqual(len(result["paired_status_differences"]), 1)
            self.assertEqual(len(result["paired_raw_diagnostic_differences"]), 1)
            self.assertIsNone(result["end_to_end_speedup"])


if __name__ == "__main__":
    unittest.main()
