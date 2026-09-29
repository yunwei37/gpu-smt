#!/usr/bin/env python3
"""Stream-preserving Z3 stdin/stdout capture shim.

Usage:
  GPU_SMT_REAL_Z3=/usr/bin/z3 GPU_SMT_TRACE_DIR=traces \
    python tools/z3_capture.py -in

The shim forwards argv and streams stdin/stdout so interactive clients keep
working. It records the raw stdin SMT-LIB transcript plus lightweight metadata.
It does not modify solver responses.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time


def find_real_z3() -> str:
    explicit = os.environ.get("GPU_SMT_REAL_Z3") or os.environ.get("REAL_Z3")
    if explicit:
        return explicit
    found = shutil.which("z3")
    if not found:
        raise RuntimeError("Z3 not found; set GPU_SMT_REAL_Z3=/path/to/z3")
    try:
        if Path(found).resolve() == Path(__file__).resolve():
            raise RuntimeError(
                "z3 resolves to this capture shim; set GPU_SMT_REAL_Z3 to the real binary"
            )
    except OSError:
        pass
    return found


def pump_stdout(src, dst) -> None:
    while True:
        chunk = os.read(src.fileno(), 65536)
        if not chunk:
            break
        os.write(dst.fileno(), chunk)


def main() -> int:
    try:
        real_z3 = find_real_z3()
    except RuntimeError as exc:
        print(f"z3_capture: {exc}", file=sys.stderr)
        return 127

    trace_dir = Path(os.environ.get("GPU_SMT_TRACE_DIR", ".gpu-smt-traces"))
    trace_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.time_ns()
    stem = f"z3-{stamp}-{os.getpid()}"
    smt_path = trace_dir / f"{stem}.smt2"
    meta_path = trace_dir / f"{stem}.meta.json"

    start = time.perf_counter()
    proc = subprocess.Popen(
        [real_z3, *sys.argv[1:]],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=None,
        bufsize=0,
    )
    assert proc.stdin is not None
    assert proc.stdout is not None

    out_thread = threading.Thread(
        target=pump_stdout,
        args=(proc.stdout, sys.stdout.buffer),
        daemon=True,
    )
    out_thread.start()

    bytes_in = 0
    broken_pipe = False
    try:
        with smt_path.open("wb") as trace:
            while True:
                chunk = os.read(sys.stdin.fileno(), 65536)
                if not chunk:
                    break
                trace.write(chunk)
                trace.flush()
                bytes_in += len(chunk)
                try:
                    proc.stdin.write(chunk)
                    proc.stdin.flush()
                except BrokenPipeError:
                    broken_pipe = True
                    break
    finally:
        try:
            proc.stdin.close()
        except BrokenPipeError:
            broken_pipe = True

    rc = proc.wait()
    out_thread.join(timeout=5)
    elapsed = time.perf_counter() - start

    meta = {
        "real_z3": real_z3,
        "argv": sys.argv[1:],
        "pid": os.getpid(),
        "child_pid": proc.pid,
        "returncode": rc,
        "elapsed_s": elapsed,
        "stdin_bytes": bytes_in,
        "broken_pipe": broken_pipe,
        "trace": smt_path.name,
    }
    meta_path.write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
