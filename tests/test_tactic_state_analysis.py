"""Result-analysis regressions; no native collection or proof verdict substitution."""
import importlib.util
from concurrent.futures import Future
import signal
import errno
import json
import os
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch, Mock
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


class CaptureOutputDurability(unittest.TestCase):
    def test_nonexistent_output_on_the_workspace_filesystem_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root/"new"/"run"
            with patch.object(Path, "is_mount", return_value=True):
                self.assertEqual(RUNNER.persistent_output(output, root), output)
            self.assertFalse(output.exists())

    def test_unmounted_workspace_is_not_assumed_persistent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "PVC"):
                RUNNER.persistent_output(root/"run", root)

    def test_outside_prefix_and_symlink_escape_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base/"workspace"
            outside = base/"workspace-other"
            root.mkdir()
            outside.mkdir()
            (root/"escape").symlink_to(outside, target_is_directory=True)
            with patch.object(Path, "is_mount", return_value=True):
                for output in [base/"tmp"/"run", outside/"run", root/"escape"/"run"]:
                    with self.subTest(output=output):
                        with self.assertRaisesRegex(ValueError, "PVC"):
                            RUNNER.persistent_output(output, root)
                        self.assertFalse(output.exists())

    def test_symlink_into_the_volume_is_canonicalized_before_use(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base/"workspace"
            root.mkdir()
            (base/"alias").symlink_to(root, target_is_directory=True)
            with patch.object(Path, "is_mount", return_value=True):
                self.assertEqual(RUNNER.persistent_output(base/"alias"/"run", root),
                                 root/"run")

    def test_nested_other_device_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root/"other-mount"
            nested.mkdir()
            original = Path.stat

            def stat(path, *args, **kwargs):
                value = original(path, *args, **kwargs)
                if path == nested:
                    fields = list(value)
                    fields[2] += 1  # Simulated different device,not an actual mount.
                    return os.stat_result(fields)
                return value

            with patch.object(Path, "is_mount", return_value=True), \
                 patch.object(Path, "stat", stat):
                with self.assertRaisesRegex(ValueError, "different filesystem"):
                    RUNNER.persistent_output(nested/"run", root)

    def test_real_cli_rejects_temporary_output_without_creating_it(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as directory:
            output = Path(directory)/"not-created"
            result = subprocess.run(
                [sys.executable, "-B", str(RUN_SPEC.origin),
                 "--input", "not-read", "--out", str(output),
                 "--context", "not-read", "--module-dir", "not-read"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("PVC", result.stderr)
            self.assertNotIn("affinity", result.stderr)
            self.assertFalse(output.exists())

    def test_bad_cli_output_is_rejected_before_affinity_or_native_work(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as directory:
            output = Path(directory)/"container-output"
            argv = ["run.py", "--input", "unread-input.json.gz",
                    "--out", str(output), "--context", "unread-context.json",
                    "--module-dir", "unread-modules"]
            with patch.object(sys, "argv", argv), \
                 patch.dict(sys.modules, {"psutil": SimpleNamespace()}), \
                 patch.object(RUNNER.os, "sched_setaffinity",
                              side_effect=AssertionError("affinity before storage check")) as affinity, \
                 patch.object(RUNNER.subprocess, "Popen") as native:
                with self.assertRaises(SystemExit) as error:
                    RUNNER.main()
                self.assertEqual(error.exception.code, 2)
                affinity.assert_not_called()
                native.assert_not_called()
            self.assertFalse(output.exists())


class CaptureResourcePoint(unittest.TestCase):
    def test_g10_budget_and_discovered_cpu_ids_are_recorded_without_lab_labels(self):
        point = RUNNER.resource_point(12, None, set(range(8)), 28 * 1024**3)
        self.assertEqual(point, dict(budget_bytes=12 * 1024**3,
                                    cpu_eligibility=list(range(8)),
                                    hardware_memory_bytes=28 * 1024**3))
        chosen = RUNNER.resource_point(12, "6,7", set(range(8)), 28 * 1024**3)
        self.assertEqual(chosen["cpu_eligibility"], [6, 7])

    def test_old_lab_budget_and_nonpositive_budgets_do_not_fit_g10(self):
        for budget in [48, 0, -1]:
            with self.subTest(budget=budget), self.assertRaisesRegex(ValueError, "RSS budget"):
                RUNNER.resource_point(budget, None, set(range(8)), 28 * 1024**3)

    def test_user_12gib_cap_cannot_be_raised_even_if_host_ram_is_larger(self):
        self.assertEqual(RUNNER.MAX_BUDGET_GIB, 12)
        for budget in [13, 48]:
            with self.subTest(budget=budget), self.assertRaisesRegex(ValueError, "12GiB maximum"):
                RUNNER.resource_point(budget, None, set(range(8)), 125 * 1024**3)

    def test_old_cpu_ids_empty_and_malformed_masks_are_not_silently_relabelled(self):
        for cpus in ["8,9,10,11", "", "0,,1", "CPU0", "-1"]:
            with self.subTest(cpus=cpus), self.assertRaisesRegex(ValueError, "--cpus"):
                RUNNER.resource_point(12, cpus, set(range(8)), 28 * 1024**3)

    def test_continuation_requires_actual_matching_resource_and_host_evidence(self):
        point = dict(RUNNER.resource_point(12, None, set(range(8)), 28 * 1024**3),
                     host_boot_id="g10-boot")
        RUNNER.check_continuation_resources([dict(event="resource_point", **point)], point)
        for history in [[], [dict(event="launch", pid=123)]]:
            with self.assertRaisesRegex(ValueError, "separate fresh point"):
                RUNNER.check_continuation_resources(history, point)
        for field, old in [("budget_bytes", 48 * 1024**3),
                           ("cpu_eligibility", [8, 9, 10, 11]),
                           ("hardware_memory_bytes", 125 * 1024**3),
                           ("host_boot_id", "lab-boot")]:
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "separate fresh point"):
                RUNNER.check_continuation_resources(
                    [dict(event="resource_point", **dict(point, **{field: old}))], point)


class CaptureHostSafety(unittest.TestCase):
    def test_memory_floor_is_whole_collection_failure_not_a_candidate_verdict(self):
        RUNNER.check_host_memory(6 * 1024**3)
        with self.assertRaisesRegex(RUNNER.HostSafetyStop, "below 6GiB"):
            RUNNER.check_host_memory(6 * 1024**3 - 1)

    def test_signal_control_requires_real_retirement_for_both_owned_signal_paths(self):
        records = []
        children = [Mock(pid=101), Mock(pid=102)]
        for child in children:
            child.stdout.readline.return_value = b"ready\n"
            child.wait.return_value = -signal.SIGKILL
        processes = SimpleNamespace(Process=lambda pid: SimpleNamespace(create_time=lambda: pid + 0.5))
        with patch.object(RUNNER.subprocess, "Popen", side_effect=children), \
             patch.object(RUNNER.os, "kill") as pid_kill, \
             patch.object(RUNNER.os, "killpg") as group_kill:
            RUNNER.require_signal_control(processes, records.append)
        pid_kill.assert_called_once_with(101, signal.SIGKILL)
        group_kill.assert_called_once_with(102, signal.SIGKILL)
        self.assertEqual([(r["pid"], r["birth"], r["qualified"]) for r in records],
                         [(101, 101.5, True), (102, 102.5, True)])
        for child in children:
            child.wait.assert_called_once()
            child.stdout.close.assert_called_once()

    def test_denied_signal_retires_the_control_and_stops_before_other_work(self):
        records, child = [], Mock(pid=101)
        child.stdout.readline.return_value = b"ready\n"
        child.wait.return_value = 0
        processes = SimpleNamespace(Process=lambda pid: SimpleNamespace(create_time=lambda: 1.5))
        with patch.object(RUNNER.subprocess, "Popen", return_value=child) as spawn, \
             patch.object(RUNNER.os, "kill", side_effect=PermissionError(errno.EACCES, "denied")), \
             patch.object(RUNNER.os, "killpg") as group_kill:
            with self.assertRaisesRegex(RUNNER.HostSafetyStop, "no native startup"):
                RUNNER.require_signal_control(processes, records.append)
        self.assertEqual(spawn.call_count, 1)
        group_kill.assert_not_called()
        child.wait.assert_called_once()
        self.assertEqual(records[0]["exit_code"], 0)
        self.assertFalse(records[0]["qualified"])

    def test_missing_existing_api_credentials_cannot_be_called_ready(self):
        with patch.object(Path, "exists", return_value=False), \
             patch.object(RUNNER.urllib.request, "urlopen") as request:
            with self.assertRaisesRegex(RUNNER.HostSafetyStop, "credentials unavailable"):
                RUNNER.api_ready()
            request.assert_not_called()

    def test_api_http_failure_is_operational_and_does_not_reveal_a_token(self):
        failure = RUNNER.urllib.error.HTTPError("https://fixture/readyz", 503, "unready", {}, None)
        with patch.dict(os.environ, {"KUBERNETES_SERVICE_HOST": "127.0.0.1"}), \
             patch.object(Path, "exists", return_value=True), \
             patch.object(Path, "read_text", return_value="simulated-token"), \
             patch.object(RUNNER.ssl, "create_default_context"), \
             patch.object(RUNNER.urllib.request, "urlopen", side_effect=failure):
            with self.assertRaisesRegex(RUNNER.HostSafetyStop, "HTTP503") as error:
                RUNNER.api_ready()
        self.assertNotIn("simulated-token", str(error.exception))

    def test_pending_api_work_does_not_block_sampling_and_stalls_stop(self):
        ready, pending = Future(), Future()
        ready.set_result(None)
        executor = Mock()
        executor.submit.side_effect = [ready, pending]
        with patch.object(RUNNER, "ThreadPoolExecutor", return_value=executor), \
             patch.object(RUNNER.time, "monotonic", return_value=0):
            health = RUNNER.ApiHealth(lambda: None)
            health.start()
            health.check(1)
            health.check(2.9)  # In-flight HTTP is never synchronously awaited here.
            self.assertFalse(pending.done())
            with self.assertRaisesRegex(RUNNER.HostSafetyStop, "stalled"):
                health.check(3)
            health.close()

    def test_final_api_failure_is_not_discarded_at_successful_collection_end(self):
        ready, bad = Future(), Future()
        ready.set_result(None)
        bad.set_exception(RUNNER.HostSafetyStop("API unreachable"))
        executor = Mock()
        executor.submit.side_effect = [ready, bad]
        with patch.object(RUNNER, "ThreadPoolExecutor", return_value=executor), \
             patch.object(RUNNER.time, "monotonic", return_value=0):
            health = RUNNER.ApiHealth(lambda: None)
            health.start()
            health.check(1)
            with self.assertRaisesRegex(RUNNER.HostSafetyStop, "unreachable"):
                health.finish()
            health.close()

    def test_host_stop_keeps_the_interrupted_candidate_pending_not_failed(self):
        rows = [dict(id="stopped", mode="observe")]
        pending, retry, derived = RUNNER.continuation_plan(rows, [],
            [dict(segment=0, current=["stopped", "observe"], source_started=True,
                  exit=-9, operational="host_safety_stop")])
        self.assertEqual(pending, rows)
        self.assertEqual((retry, derived), ([], []))


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
