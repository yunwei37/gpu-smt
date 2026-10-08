#!/usr/bin/env python3
"""Capture Goedel step2's fresh native transport without its global killall.

This measures the whole lake/REPL invocation, including imports, elaboration and
checks. It does not separate these stages or measure proof-check latency. Source
list order is admission order; events record actual launch/result observations.
No response interpretation is required: opaque native fields remain in stdout.
"""
import argparse
import concurrent.futures
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import select
import shutil
import signal
import subprocess
import sys
import threading
import time
import traceback


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def durable_bytes(path, data):
    with open(path, "xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codes", type=Path, required=True)
    parser.add_argument("--lake", required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=300)
    args = parser.parse_args()
    if args.workers < 1 or not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("workers and timeout must be positive and finite")
    codes_bytes = args.codes.read_bytes()
    codes = json.loads(codes_bytes)
    if not isinstance(codes, list) or any(
        not isinstance(row, dict) or not isinstance(row.get("code"), str)
        for row in codes
    ):
        parser.error("codes must be the official list of objects with string code fields")
    workspace = args.workspace.resolve(strict=True)
    lake_found = shutil.which(args.lake)
    if not lake_found:
        parser.error("lake executable does not exist or is not executable")
    # Retain a symlink launcher path (elan dispatch may depend on argv[0]).
    lake = os.path.abspath(lake_found)
    command = [lake, "exe", "repl"]
    args.out.mkdir(parents=True, exist_ok=False)
    durable_bytes(args.out / "codes.original.json", codes_bytes)
    stop = threading.Event()
    signals = []
    lock = threading.Lock()
    old_handlers = {}
    completed = []
    started = set()

    def on_signal(number, _frame):
        signals.append({"signal": number, "wall_ns": time.time_ns(),
                        "monotonic_ns": time.monotonic_ns()})
        stop.set()

    for number in (signal.SIGINT, signal.SIGTERM):
        old_handlers[number] = signal.signal(number, on_signal)

    with open(args.out / "events.jsonl", "x", encoding="utf-8") as events:
        sequence = 0

        def event(kind, **fields):
            nonlocal sequence
            with lock:
                record = dict(event=kind, sequence=sequence, wall_ns=time.time_ns(),
                              monotonic_ns=time.monotonic_ns(), **fields)
                sequence += 1
                events.write(json.dumps(record, ensure_ascii=False) + "\n")
                events.flush()
                os.fsync(events.fileno())

        provenance = {}
        source_root = Path(__file__).resolve().parent.parent / "artifacts/lean-candidate-source-2026-10-07/goedel"
        for label, path in [("lake", Path(lake)), ("capture", Path(__file__)),
                            ("official_step2", source_root / "eval/step2_compile.py"),
                            ("official_verifier", source_root / "prover/lean/verifier.py"),
                            ("toolchain", workspace / "lean-toolchain"),
                            ("manifest", workspace / "lake-manifest.json"),
                            ("lakefile", workspace / "lakefile.lean"),
                            ("repl_binary", workspace / ".lake/build/bin/repl"),
                            ("package_repl_binary", workspace / ".lake/packages/REPL/.lake/build/bin/repl")]:
            provenance[label] = {"path": str(path), "resolved": str(path.resolve()),
                                 "sha256": sha256(path) if path.is_file() else None}
        event("run", command=command, cwd=str(workspace), workers=args.workers,
              timeout_seconds=args.timeout, codes_path=str(args.codes.resolve()),
              codes_sha256=hashlib.sha256(codes_bytes).hexdigest(), count=len(codes),
              provenance=provenance, python=sys.version, platform=platform.platform(),
              affinity=sorted(os.sched_getaffinity(0)),
              environment={key: os.environ.get(key) for key in
                           ("PATH", "LEAN_PATH", "LEAN_SYSROOT", "ELAN_HOME", "ELAN_TOOLCHAIN",
                            "OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS")},
              adaptation="owned new-session process groups; no global monitor; disk raw output",
              completion_observation="Linux pidfd exit readiness; no fixed process polling delay",
              timing_scope="whole invocation; native import/elaboration/check stages not separated")
        for index in range(len(codes)):
            event("admitted", source_index=index)

        def capture(index):
            if stop.is_set():
                event("not_launched", source_index=index, reason="supervisor_signal")
                return
            folder = args.out / f"request-{index:08d}"
            folder.mkdir()
            # Exact original JSON key order/default separators and CRLF blank delimiter.
            payload = json.dumps(dict(cmd=codes[index]["code"], allTactics=False,
                                      ast=False, tactics=False, premises=False),
                                 ensure_ascii=False).encode("utf-8") + b"\r\n\r\n"
            durable_bytes(folder / "stdin.bin", payload)
            proc = None
            pidfd = None
            status = "launch_error"
            error = None
            begin = time.monotonic_ns()
            process_end = None
            try:
                with open(folder / "stdin.bin", "rb") as stdin, \
                     open(folder / "stdout.bin", "xb") as stdout, \
                     open(folder / "stderr.bin", "xb") as stderr:
                    event("launch_intent", source_index=index, command=command,
                          cwd=str(workspace), stdin_sha256=hashlib.sha256(payload).hexdigest(),
                          affinity=sorted(os.sched_getaffinity(0)))
                    begin = time.monotonic_ns()
                    proc = subprocess.Popen(command, cwd=workspace, stdin=stdin,
                                            stdout=stdout, stderr=stderr, start_new_session=True)
                    # Native exit readiness avoids adding up to50ms of polling
                    # delay only to the fresh path. Failure is a capture error,
                    # not a silent fallback to a differently timed protocol.
                    pidfd = os.pidfd_open(proc.pid)
                    with lock:
                        started.add(index)
                    event("launched", source_index=index, pid=proc.pid, pgid=proc.pid)
                    deadline = begin + int(args.timeout * 1e9)
                    status = "exited"
                    while proc.poll() is None:
                        if stop.is_set() or time.monotonic_ns() >= deadline:
                            status = "interrupted" if stop.is_set() else "timeout"
                            break
                        select.select([pidfd], [], [],
                                      min(0.05, max(0, (deadline - time.monotonic_ns()) / 1e9)))
                    # Kill remaining owned descendants even when the launcher already exited.
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    proc.wait()
                    process_end = time.monotonic_ns()
                    for stream in (stdout, stderr):
                        stream.flush()
                        os.fsync(stream.fileno())
            except Exception:
                error = traceback.format_exc()
                if proc is not None:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    proc.wait()
            finally:
                if pidfd is not None:
                    os.close(pidfd)
            result = dict(source_index=index, status=status,
                          returncode=proc.returncode if proc else None,
                          capture_elapsed_ns=time.monotonic_ns() - begin,
                          invocation_elapsed_ns=process_end - begin if process_end else None,
                          error=error,
                          files={name: {"bytes": (folder / name).stat().st_size,
                                        "sha256": sha256(folder / name)}
                                 for name in ("stdin.bin", "stdout.bin", "stderr.bin")
                                 if (folder / name).exists()})
            # Raw bytes are persisted before any optional downstream normalization.
            durable_bytes(folder / "result.json", json.dumps(result, indent=2).encode())
            event("result", **result)
            with lock:
                completed.append(index)

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
                futures = [pool.submit(capture, index) for index in range(len(codes))]
                try:
                    for future in concurrent.futures.as_completed(futures):
                        future.result()
                except BaseException:
                    stop.set()
                    raise
        except BaseException:
            stop.set()
            event("supervisor_error", error=traceback.format_exc())
            raise
        finally:
            event("shutdown", signals=signals, launched_indices=sorted(started),
                  result_indices=sorted(completed),
                  missing_result_indices=sorted(set(range(len(codes))) - set(completed)))
            for number, handler in old_handlers.items():
                signal.signal(number, handler)
    return 128 + signals[0]["signal"] if signals else 0


if __name__ == "__main__":
    sys.exit(main())
