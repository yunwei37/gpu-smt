"""Accounting controls only; fixture durations are not native performance data."""
import copy
import gzip
import importlib.util
import json
import tempfile
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "warm_resource_compare", Path(__file__).parents[1] / "bench/lean-warm-resource/compare.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture():
    library, repl = "/project/libnative.so", "/native/repl"
    candidates = [dict(id=i, code=f"import Init\n-- {i}", timeout_ms=300000,
                       task_id=i, reuse=False) for i in ["a", "b"]]
    batch = dict(mode="all", candidates=candidates)
    warm_payloads = [{"env": 9}, {"env": 9, "messages": [{"severity": "error", "data": "failed"}]}]
    engine_payloads = [dict(p, env=0, ast=[]) for p in warm_payloads]
    warm_results, engine_results, attempts = [], [], {}
    for n, i in enumerate(["a", "b"]):
        warm_status, status = ("valid", "accepted") if n == 0 else ("lean_error", "rejected")
        warm_results.append(dict(id=i, status=warm_status, result=dict(response=warm_payloads[n])))
        attempts[i] = [dict(wall_seconds=12)]
        events = [{"stage": "prepared_ready", "detail": json.dumps(
            {"prepared_context": {"native_library": library}})}] if n == 0 else []
        engine_results.append(dict(
            id=i, outcome=dict(status=status, response=engine_payloads[n]),
            attempts=[dict(elapsed_seconds=7, backend_events=events)],
            cached=False, coalesced=False))
    resources = dict(cpus=[8, 9, 10, 11], memory_bytes=48 << 30)
    return dict(
        manifest=dict(**resources, fixed_process_AS_cap=False,
                      native_library=library, warm_repl=repl),
        input=batch, warm=dict(original_candidates=candidates, results=warm_results, attempts=attempts),
        warm_terminal=dict(
            state="complete", native_survivors=[], returned=2, physical_attempts=2,
            memory=dict(error=None, peak_sampled_native_repl_count=4),
            resources=dict(**resources, per_process_AS=None, maximum_native_workers=4),
            native_library=library, source_repl=repl, source_context=dict(project="/project"),
            whole_seconds=14, preparation_seconds=2),
        engine=dict(batch=batch, results=engine_results, resources=dict(**resources, cores_per_worker=1),
                    backend='lean-repl|"/native/repl"|[]|"/project"|fixture', lifecycle_seconds=9),
        warm_libraries=[dict(pid=n, birth=1, mapped=True, native_library=library) for n in range(4)],
        warm_exit=dict(exit=0, external_seconds=15),
        engine_exit=dict(exit=0, external_seconds=10),
        terminal=dict(state="qualification-pair-complete"))


class WarmResourceCompare(unittest.TestCase):
    def test_alias_resolution_accepts_only_the_exact_canonical_executable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real = root / "retained"
            real.mkdir()
            (real / "repl").write_bytes(b"native fixture")
            (root / "alias").symlink_to(real, target_is_directory=True)
            requested = str(root / "alias" / "repl")
            resolution = module.executable_resolution(requested)
            self.assertEqual(resolution["resolved"], str(real / "repl"))
            self.assertTrue(resolution["same_file"])
            point = fixture()
            point["manifest"]["warm_repl"] = requested
            point["warm_terminal"]["source_repl"] = requested
            point["executable_resolution"] = resolution
            point["engine"]["backend"] = 'lean-repl|' + json.dumps(str(real / "repl")) + '|[]|"/project"|fixture'
            self.assertEqual(module.compare(point)["executable_resolution"], resolution)
            point["engine"]["backend"] = 'lean-repl|' + json.dumps(str(real / "repl") + "-backup") + '|[]|"/project"|fixture'
            with self.assertRaisesRegex(ValueError, "native fallback"):
                module.compare(point)
            point["executable_resolution"]["requested"] = "/another/alias"
            with self.assertRaisesRegex(ValueError, "alias receipt"):
                module.compare(point)

    def test_missing_executable_alias_never_becomes_an_identity_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                module.executable_resolution(str(Path(tmp) / "missing"))

    def test_archived_compressed_point_replays_without_native_files(self):
        point = fixture()
        paths = {
            "manifest": "manifest.json", "input": "input24.json",
            "warm": "warm/results.json", "warm_terminal": "warm/terminal.json",
            "engine": "engine.stdout", "warm_exit": "warm-exit.json",
            "engine_exit": "engine-exit.json", "terminal": "terminal.json",
            "warm_libraries": "warm/native-library-readiness.json",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, path in paths.items():
                p = root / (path + ".gz")
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(gzip.compress(json.dumps(point[name]).encode(), mtime=0))
            self.assertEqual(module.compare(module.read_point(root)), module.compare(point))

    def test_only_external_complete_clocks_determine_the_descriptive_ratio(self):
        value = module.compare(fixture())
        self.assertEqual(value["descriptive_external_elapsed_ratio"], 1.5)
        self.assertEqual(value["warm_admitted_envelope_seconds_sum"], 24)
        self.assertEqual(value["engine_native_attempt_seconds_sum"], 14)
        self.assertNotEqual(value["descriptive_external_elapsed_ratio"], 24 / 14)
        self.assertFalse(value["resource_layer_gain_established"])
        self.assertIsNone(value["engine_preparation_seconds"])

    def test_equal_accepted_counts_with_changed_ids_are_not_parity(self):
        point = fixture()
        point["engine"]["results"][0]["outcome"]["status"] = "rejected"
        point["engine"]["results"][1]["outcome"]["status"] = "accepted"
        value = module.compare(point)
        self.assertEqual(value["accepted_set_only_warm"], ["a"])
        self.assertEqual(value["accepted_set_only_engine"], ["b"])
        self.assertEqual(len(value["changed_statuses"]), 2)

    def test_wire_normalization_never_hides_diagnostic_changes(self):
        point = fixture()
        value = module.compare(point)
        self.assertEqual(value["raw_native_payload_changed_ids"], ["a", "b"])
        self.assertEqual(value["top_level_env_and_empty_ast_normalized_payload_changed_ids"], [])
        point["engine"]["results"][1]["outcome"]["response"]["messages"] = [
            dict(severity="error", data="different ?m.17", pos=dict(line=20, column=2))]
        value = module.compare(point)
        self.assertEqual(value["top_level_env_and_empty_ast_normalized_payload_changed_ids"], ["b"])

    def test_operational_failure_stays_distinct_from_native_rejection(self):
        point = fixture()
        point["engine"]["results"][1]["outcome"] = dict(status="backend_error", response=None)
        value = module.compare(point)
        self.assertEqual(value["changed_statuses"][0]["warm"], "rejected")
        self.assertEqual(value["changed_statuses"][0]["engine"], "backend_error")
        self.assertEqual(value["missing_engine_native_payload_ids"], ["b"])

    def test_missing_or_changed_resource_library_and_source_evidence_is_refused(self):
        variants = []
        point = fixture()
        point["warm_terminal"]["resources"]["per_process_AS"] = 24 << 30
        variants.append(point)
        point = fixture()
        point["engine"]["resources"]["cpus"] = [8, 9]
        variants.append(point)
        point = fixture()
        point["warm_terminal"]["native_library"] = "/other.so"
        variants.append(point)
        point = fixture()
        point["warm_libraries"] = []
        variants.append(point)
        point = fixture()
        point["engine"]["results"][0]["attempts"][0]["backend_events"] = []
        variants.append(point)
        point = fixture()
        point["engine"]["batch"] = copy.deepcopy(point["input"])
        point["engine"]["batch"]["candidates"][0]["timeout_ms"] += 1
        variants.append(point)
        point = fixture()
        point["warm"]["original_candidates"] = copy.deepcopy(point["input"]["candidates"])
        point["warm"]["original_candidates"][0]["code"] += "\n"
        variants.append(point)
        for n, point in enumerate(variants):
            with self.subTest(n=n), self.assertRaises(ValueError):
                module.compare(point)

    def test_partial_failed_duplicate_or_unknown_results_are_refused(self):
        variants = []
        point = fixture()
        point["terminal"]["state"] = "in-progress"
        variants.append(point)
        point = fixture()
        point["warm_terminal"]["native_survivors"] = [dict(pid=1)]
        variants.append(point)
        point = fixture()
        point["warm"]["results"][1]["id"] = "a"
        variants.append(point)
        point = fixture()
        point["engine_exit"]["exit"] = 1
        variants.append(point)
        point = fixture()
        point["warm"]["results"][0]["status"] = "unknown"
        variants.append(point)
        point = fixture()
        point["engine"]["results"][0]["cached"] = True
        variants.append(point)
        for n, point in enumerate(variants):
            with self.subTest(n=n), self.assertRaises(ValueError):
                module.compare(point)


if __name__ == "__main__":
    unittest.main()
