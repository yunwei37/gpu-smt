"""Finite baseline resource-queue contracts; no native proofs or timings."""
import asyncio
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "warm_resource_runner", ROOT / "bench/lean-warm-resource/run.py")
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class WarmResourceQueue(unittest.IsolatedAsyncioTestCase):
    async def test_deferred_retry_does_not_block_the_ordinary_frontier(self):
        peer_started = asyncio.Event()
        release_peer = asyncio.Event()
        smalls_done = asyncio.Event()
        preempted = []
        completed = []
        active = set()
        peak = 0

        async def execute(candidate):
            nonlocal peak
            active.add(candidate)
            peak = max(peak, len(active))
            try:
                if candidate == "heavy":
                    await peer_started.wait()
                    preempted.append(candidate)
                elif candidate == "peer":
                    peer_started.set()
                    await release_peer.wait()
                else:
                    self.assertIn("peer", active)
                    self.assertEqual(preempted, ["heavy"])
                    completed.append(candidate)
                    if completed == ["small-a", "small-b"]:
                        smalls_done.set()
            finally:
                active.remove(candidate)

        async def close_idle():
            self.fail("ordinary progress must not retire a live peer")

        task = asyncio.create_task(RUNNER._run_first_attempts(
            ["heavy", "peer", "small-a", "small-b"], execute,
            lambda: True, close_idle, 2))
        try:
            # Progress is ordered by actual callbacks, not a speed comparison.
            await asyncio.wait_for(smalls_done.wait(), 2)
            self.assertFalse(task.done(), "held peer was not actually active")
        finally:
            release_peer.set()
            await task
        self.assertEqual(peak, 2)
        self.assertEqual(completed, ["small-a", "small-b"])
        self.assertEqual(preempted, ["heavy"])
        self.assertFalse(active)

    async def test_actual_pressure_retires_idle_state_before_first_admission(self):
        admitted = False
        events = []

        async def close_idle():
            nonlocal admitted
            events.append("retire-idle")
            admitted = True

        async def execute(candidate):
            self.assertTrue(admitted)
            events.append(candidate)

        await RUNNER._run_first_attempts(
            ["one", "two"], execute, lambda: admitted, close_idle, 2)
        self.assertEqual(events, ["retire-idle", "one", "two"])

    async def test_cancellation_awaits_all_ordinary_task_cleanup(self):
        both_started = asyncio.Event()
        started = set()
        retired = set()
        hold = asyncio.Event()

        async def execute(candidate):
            started.add(candidate)
            if len(started) == 2:
                both_started.set()
            try:
                await hold.wait()
            finally:
                # Retirement can contain real asynchronous operations.
                await asyncio.sleep(0)
                retired.add(candidate)

        async def close_idle():
            self.fail("fixture has no idle pressure")

        task = asyncio.create_task(RUNNER._run_first_attempts(
            ["one", "two", "not-started"], execute,
            lambda: True, close_idle, 2))
        await asyncio.wait_for(both_started.wait(), 2)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(started, {"one", "two"})
        self.assertEqual(retired, started)


if __name__ == "__main__":
    unittest.main()
