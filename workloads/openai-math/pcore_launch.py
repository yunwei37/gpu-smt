#!/usr/bin/env python3
"""Launch a W timed task without joining the shared P-core wait queue.

M/O priority is an operator instruction, not inferred from an empty wait queue.
Do not invoke this launcher until their current profile/calibration/replay work
has completed. Inspection never acquires the shared lock.
"""
import argparse
import errno
import fcntl
import json
import os
from pathlib import Path
import re

LOCK = Path("/workspaces/.agent-state/gpu-smt-captures/pcore.lock")
TEMPORARY_FAILURE = 75
LOCK_ID = re.compile(r"^([0-9a-fA-F]+):([0-9a-fA-F]+):([0-9]+)$")


def waiting_pids(lock_path, locks_text):
    """Read only arrow-marked waiters for this exact device and inode."""
    st = lock_path.stat()
    identity = (os.major(st.st_dev), os.minor(st.st_dev), st.st_ino)
    waiting = []
    for line in locks_text.splitlines():
        fields = line.split()
        if "->" not in fields:
            continue
        for i, field in enumerate(fields):
            match = LOCK_ID.fullmatch(field)
            if not match:
                continue
            actual = (int(match[1], 16), int(match[2], 16), int(match[3]))
            if actual == identity:
                if i == 0:
                    raise ValueError("missing waiter PID in /proc/locks")
                waiting.append(int(fields[i - 1]))
            break
    return sorted(set(waiting))


def try_acquire(lock_path, read_locks=lambda: Path("/proc/locks").read_text()):
    """Return (fd, reason, waiters); never block or enqueue for this lock."""
    waiting = waiting_pids(lock_path, read_locks())
    if waiting:
        return None, "deferred_existing_waiters", waiting
    fd = os.open(lock_path, os.O_RDWR)  # Existing shared lock; do not create one.
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            if error.errno in (errno.EACCES, errno.EAGAIN):
                os.close(fd)
                return None, "deferred_lock_held", []
            raise
        # Another lane may have started waiting between the first check and take.
        waiting = waiting_pids(lock_path, read_locks())
        if waiting:
            os.close(fd)
            return None, "deferred_waiter_arrived", waiting
        return fd, "acquired_without_waiting", []
    except BaseException:
        os.close(fd)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inspect", action="store_true",
                        help="read waiting PIDs only; acquire no lock and run nothing")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if args.inspect:
        if command:
            parser.error("--inspect accepts no command")
        waiting = waiting_pids(LOCK, Path("/proc/locks").read_text())
        print(json.dumps(dict(status="inspection_only", waiting_pids=waiting,
                              acquired=False, launched=False,
                              other_lanes_completed="not_inferred")))
        return TEMPORARY_FAILURE if waiting else 0
    if not command:
        parser.error("a timed command is required")
    fd, reason, waiting = try_acquire(LOCK)
    if fd is None:
        print(json.dumps(dict(status=reason, waiting_pids=waiting,
                              acquired=False, launched=False)), flush=True)
        return TEMPORARY_FAILURE
    os.set_inheritable(fd, True)
    try:
        os.execvp("taskset", ["taskset", "-c", "0-7", *command])
    finally:
        os.close(fd)


if __name__ == "__main__":
    raise SystemExit(main())
