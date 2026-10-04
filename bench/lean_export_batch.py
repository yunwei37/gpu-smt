#!/usr/bin/env python3
"""Measure batched independent-checking throughput for a Lean export checker.

The serving question for the Lean thread is: *can the runtime batch many
independent Lean checks while preserving accept/reject semantics?* This harness
runs a fixed job set of Lean export files (one declaration environment each)
through a checker binary with a process pool at several widths, and reports
makespan plus the accept/reject count.

It deliberately treats the checker as a black box, matching the
``backend-unmodified`` constraint: the same binary an application would invoke
is the one under test.

Example
-------

::

    python3 bench/lean_export_batch.py \
        --checker /path/to/kernel \
        --inputs '_build/tests/tutorial/*/*.ndjson' \
        --widths 1,4,8,16,24 \
        --json results-lean-batch.json

Each input file is expected to produce exit code 0 on accept for the official
kernel checker interface (``kernel <file>``). Reject/accept counts are reported
via ``--accept-marker`` (default ``Accepted``), which is matched against stdout;
for checkers that only signal via exit code, pass ``--accept-by-exit``.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import glob
import json
import subprocess
import time
from pathlib import Path


def expand(patterns: list[str], duplicate: int = 1) -> list[str]:
    files: list[str] = []
    for pat in patterns:
        files.extend(sorted(glob.glob(pat)))
    # de-duplicate while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for f in files:
        if f not in seen:
            seen.add(f)
            out.append(f)
    if duplicate > 1:
        out = out * duplicate
    return out


def run_one(checker: str, cores: str | None, path: str, timeout: float) -> dict:
    cmd = ["taskset", "-c", cores, checker, path] if cores else [checker, path]
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
        wall = time.perf_counter() - t0
        return {
            "path": path,
            "returncode": proc.returncode,
            "wall": wall,
            "stdout": proc.stdout[:4096].decode("utf-8", "replace"),
            "stderr": proc.stderr[:4096].decode("utf-8", "replace"),
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "path": path,
            "returncode": None,
            "wall": time.perf_counter() - t0,
            "stdout": "",
            "stderr": "",
            "timed_out": True,
        }


def run_width(
    files: list[str],
    checker: str,
    width: int,
    cores: str | None,
    timeout: float,
    accept_marker: str | None,
    accept_by_exit: bool,
) -> dict:
    t0 = time.perf_counter()
    results: list[dict] = []
    with cf.ThreadPoolExecutor(max_workers=width) as ex:
        for r in ex.map(lambda p: run_one(checker, cores, p, timeout), files):
            results.append(r)
    makespan = time.perf_counter() - t0

    accepted = 0
    for r in results:
        if r["timed_out"]:
            continue
        if accept_by_exit:
            accepted += int(r["returncode"] == 0)
        else:
            accepted += int((accept_marker or "Accepted") in r["stdout"])

    return {
        "width": width,
        "jobs": len(files),
        "makespan_s": makespan,
        "throughput_jobs_per_s": len(files) / makespan if makespan > 0 else 0.0,
        "accepted": accepted,
        "seconds_per_job": makespan / len(files) if files else 0.0,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--checker", required=True, help="checker binary")
    ap.add_argument(
        "--inputs",
        nargs="+",
        required=True,
        help="file/glob list of Lean export files",
    )
    ap.add_argument("--widths", default="1,4,8,16,24")
    ap.add_argument("--cores", default=None, help="taskset core list, e.g. 0-23")
    ap.add_argument("--timeout", type=float, default=3600.0)
    ap.add_argument("--accept-marker", default="Accepted")
    ap.add_argument(
        "--accept-by-exit",
        action="store_true",
        help="score accept by exit code 0 instead of an stdout marker",
    )
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument(
        "--duplicate",
        type=int,
        default=1,
        help="repeat the job set N times to model a stream of repeated candidates",
    )
    ap.add_argument("--json", required=True)
    args = ap.parse_args()

    files = expand(args.inputs, duplicate=args.duplicate)
    if not files:
        ap.error("no input files matched")
    widths = [int(w) for w in args.widths.split(",") if w.strip()]

    runs = []
    for width in widths:
        for rep in range(args.repeat):
            r = run_width(
                files,
                args.checker,
                width,
                args.cores,
                args.timeout,
                args.accept_marker,
                args.accept_by_exit,
            )
            r["repeat"] = rep
            runs.append(r)
            print(
                f"width={width:3d} rep={rep} jobs={r['jobs']} "
                f"makespan={r['makespan_s']:8.3f}s "
                f"jobs/s={r['throughput_jobs_per_s']:8.2f} "
                f"accepted={r['accepted']}",
                flush=True,
            )

    payload = {
        "checker": args.checker,
        "inputs": args.inputs,
        "cores": args.cores,
        "jobs": len(files),
        "accept_marker": None if args.accept_by_exit else args.accept_marker,
        "accept_by_exit": args.accept_by_exit,
        "runs": runs,
    }
    Path(args.json).write_text(json.dumps(payload, indent=1) + "\n")
    print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
