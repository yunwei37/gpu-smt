"""Test archived RSS association; no verifier or model executes."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "profile_memory", ROOT / "bench/lean-failure-profile/memory_attribution.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def event(time, source="a", phase="body", kind="sample", active=True):
    return dict(time_ns=time, event=kind, sampler_error=0, threads=[
        dict(source_id=source, phase=phase, active=[{}] if active else [])])


def rss(time, birth=1, value=30):
    return dict(time_ns=time, total_rss_bytes=999999, processes=[
        dict(pid=7, birth=birth, rss=value, native_repl=True)])


class ProfileMemoryAttribution(unittest.TestCase):
    def test_body_time_birth_and_HTTP_are_all_required(self):
        runs = {7: [(0, 100, "a")]}
        matches, dropped = M.associate(rss(20), rss(30, value=45),
                                      runs, {7: {1}}, {"a": [(0, 100)]})
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["sampled_rss_bytes"], 45)  # never aggregate
        for before, after, births, envelope in [
            (rss(20), rss(30, birth=2), {7: {1, 2}}, {"a": [(0, 100)]}),
            (rss(20), rss(30), {7: {1, 2}}, {"a": [(0, 100)]}),
            (rss(20), rss(30), {7: {1}}, {"a": [(0, 29)]}),
            (rss(-1), rss(30), {7: {1}}, {"a": [(0, 100)]}),
        ]:
            matches, dropped = M.associate(before, after, runs, births, envelope)
            self.assertEqual(matches, [])
            self.assertEqual(sum(dropped.values()), 1)

    def test_source_boundary_breaks_even_if_same_tag_reappears(self):
        runs = M.body_runs([event(0), event(40),
            event(50, kind="source_boundary"), event(60), event(100)], {"a"})
        self.assertEqual(runs, [(0, 40, "a"), (60, 100, "a")])
        matches, _ = M.associate(rss(30), rss(70), {7: runs},
                                 {7: {1}}, {"a": [(0, 100)]})
        self.assertEqual(matches, [])

    def test_idle_header_and_conflicting_thread_are_not_body_ownership(self):
        for e in [event(1, active=False), event(1, phase="header"),
                  event(1, source="unknown")]:
            self.assertIsNone(M.owner(e, {"a"}))
        e = event(1)
        e["threads"] += event(1, source="b")["threads"]
        self.assertIsNone(M.owner(e, {"a", "b"}))

    def test_censored_gzip_prefix_is_retained_without_tail_extrapolation(self):
        import json
        rows = [event(10), event(20)]
        raw = "".join(json.dumps(row) + "\n" for row in rows).encode()
        compressor = zlib.compressobj(wbits=31)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prefix.jsonl.gz"
            path.write_bytes(compressor.compress(raw) + compressor.flush(zlib.Z_SYNC_FLUSH))
            events = list(M._PROFILE.snapshots(path))
        self.assertFalse(events[-1]["_stream_closed"])
        self.assertEqual(M.body_runs(events, {"a"}), [(10, 20, "a")])
        matches, _ = M.associate(rss(19), rss(21), {7: [(10, 20, "a")]},
                                 {7: {1}}, {"a": [(0, 100)]})
        self.assertEqual(matches, [])


if __name__ == "__main__":
    unittest.main()
