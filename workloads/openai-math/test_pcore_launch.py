#!/usr/bin/env python3
"""Untimed E-core controls for W's nonqueueing P-lock launcher."""
import errno
import fcntl
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "pcore_launch", Path(__file__).with_name("pcore_launch.py"))
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LockLaunchTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(
            dir="/workspaces/.agent-state/gpu-smt-captures/workloads")
        self.path = Path(self.directory.name) / "control.lock"
        self.path.touch()
        st = self.path.stat()
        self.identity = f"{os.major(st.st_dev):02x}:{os.minor(st.st_dev):02x}:{st.st_ino}"

    def tearDown(self):
        self.directory.cleanup()

    def test_arrow_waiter_exact_identity(self):
        text = (f"3: FLOCK ADVISORY WRITE 1 {self.identity} 0 EOF\n"
                f"3: -> FLOCK ADVISORY WRITE 11027 {self.identity} 0 EOF\n"
                f"3:  -> FLOCK ADVISORY WRITE 38309 {self.identity} 0 EOF\n"
                "4: -> FLOCK ADVISORY WRITE 999 00:00:12 0 EOF\n")
        self.assertEqual(launcher.waiting_pids(self.path, text), [11027, 38309])

    def test_same_inode_different_device_is_not_ours(self):
        inode = self.path.stat().st_ino
        self.assertEqual(launcher.waiting_pids(
            self.path, f"1: -> FLOCK ADVISORY WRITE 123 ffff:ffff:{inode} 0 EOF\n"), [])

    def test_waiters_defer_before_acquisition(self):
        text = f"3: -> FLOCK ADVISORY WRITE 11027 {self.identity} 0 EOF\n"
        fd, reason, waiting = launcher.try_acquire(self.path, lambda: text)
        self.assertIsNone(fd)
        self.assertEqual((reason, waiting), ("deferred_existing_waiters", [11027]))
        with self.path.open("r+") as probe:
            fcntl.flock(probe.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

    def test_waiter_arriving_after_take_releases_lock(self):
        texts = iter(["", f"3: -> FLOCK ADVISORY WRITE 11027 {self.identity} 0 EOF\n"])
        fd, reason, waiting = launcher.try_acquire(self.path, lambda: next(texts))
        self.assertIsNone(fd)
        self.assertEqual(reason, "deferred_waiter_arrived")
        with self.path.open("r+") as probe:
            fcntl.flock(probe.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

    def test_free_control_lock_acquires_and_excludes_another_open(self):
        fd, reason, waiting = launcher.try_acquire(self.path, lambda: "")
        self.assertEqual(reason, "acquired_without_waiting")
        try:
            with self.path.open("r+") as other:
                with self.assertRaises(OSError) as caught:
                    fcntl.flock(other.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.assertIn(caught.exception.errno, (errno.EACCES, errno.EAGAIN))
        finally:
            os.close(fd)

    def test_real_owned_holder_returns_without_enqueuing(self):
        child = subprocess.Popen(
            [sys.executable, "-u", "-c",
             "import fcntl,sys; f=open(sys.argv[1],'r+'); "
             "fcntl.flock(f,fcntl.LOCK_EX); print('held',flush=True); sys.stdin.read()",
             str(self.path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True)
        try:
            self.assertEqual(child.stdout.readline().strip(), "held")
            fd, reason, waiting = launcher.try_acquire(self.path)
            self.assertIsNone(fd)
            self.assertEqual(reason, "deferred_lock_held")
            self.assertNotIn(os.getpid(), launcher.waiting_pids(
                self.path, Path("/proc/locks").read_text()))
        finally:
            child.stdin.close()  # Natural exit; no timed/native task or signal.
            child.wait(timeout=5)
            child.stdout.close()
            child.stderr.close()


if __name__ == "__main__":
    unittest.main()
