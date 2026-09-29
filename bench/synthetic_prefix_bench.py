#!/usr/bin/env python3
"""Synthetic benchmark for cross-query SMT prefix reuse.

This is intentionally a smoke test, not paper evidence. It compares:
  1. cold: one stock Z3 process per query;
  2. incremental: one stock Z3 process with a common prefix and push/pop deltas.

The generated QF_BV queries are semantically identical across both modes.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import time

MASK64 = (1 << 64) - 1


def bv64(value: int) -> str:
    return f"#x{value & MASK64:016x}"


def build_common_prefix(prefix_constraints: int) -> tuple[str, int]:
    if prefix_constraints < 1:
        raise ValueError("prefix_constraints must be >= 1")

    lines = ["(set-logic QF_BV)"]
    for i in range(prefix_constraints + 1):
        lines.append(f"(declare-fun x{i} () (_ BitVec 64))")

    value = 1
    lines.append(f"(assert (= x0 {bv64(value)}))")
    for i in range(prefix_constraints):
        step = (0x9E3779B97F4A7C15 + i * 0x100000001B3) & MASK64
        value = (value + step) & MASK64
        lines.append(f"(assert (= x{i + 1} (bvadd x{i} {bv64(step)})))")

    return "\n".join(lines) + "\n", value


def build_delta(prefix_constraints: int, expected: int, query_id: int) -> tuple[str, str]:
    # Give each query different syntax while preserving deterministic SAT/UNSAT
    # behavior. Even query ids are SAT; odd ids are UNSAT.
    offset = (query_id * 0xD6E8FEB86659FD93) & MASK64
    lhs = f"(bvadd x{prefix_constraints} {bv64(offset)})"
    rhs_value = (expected + offset + (query_id & 1)) & MASK64
    expected_status = "sat" if (query_id & 1) == 0 else "unsat"
    return f"(assert (= {lhs} {bv64(rhs_value)}))\n", expected_status


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    rank = (len(xs) - 1) * p
    lo = math.floor(rank)
    hi = math.ceil(rank)
    if lo == hi:
        return xs[lo]
    return xs[lo] * (hi - rank) + xs[hi] * (rank - lo)


def summarize(latencies_s: list[float], total_s: float) -> dict[str, float]:
    n = len(latencies_s)
    return {
        "queries": n,
        "total_s": total_s,
        "throughput_qps": (n / total_s) if total_s > 0 else 0.0,
        "latency_ms_mean": statistics.fmean(latencies_s) * 1e3 if n else 0.0,
        "latency_ms_p50": percentile(latencies_s, 0.50) * 1e3,
        "latency_ms_p95": percentile(latencies_s, 0.95) * 1e3,
        "latency_ms_p99": percentile(latencies_s, 0.99) * 1e3,
    }


def parse_status(stdout: str) -> str:
    for line in stdout.splitlines():
        token = line.strip()
        if token in {"sat", "unsat", "unknown"}:
            return token
    raise RuntimeError(f"could not find solver status in output: {stdout!r}")


def run_cold(
    z3: str,
    common: str,
    deltas: list[tuple[str, str]],
    dump_dir: Path | None,
) -> tuple[list[str], dict[str, float]]:
    statuses: list[str] = []
    latencies: list[float] = []
    total_start = time.perf_counter()

    for qid, (delta, _expected) in enumerate(deltas):
        payload = common + delta + "(check-sat)\n(exit)\n"
        if dump_dir is not None:
            (dump_dir / f"cold-{qid:05d}.smt2").write_text(payload, encoding="utf-8")

        start = time.perf_counter()
        proc = subprocess.run(
            [z3, "-in", "-smt2"],
            input=payload,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        latencies.append(time.perf_counter() - start)
        if proc.returncode != 0:
            raise RuntimeError(f"z3 failed for query {qid}: {proc.stderr}")
        statuses.append(parse_status(proc.stdout))

    total_s = time.perf_counter() - total_start
    return statuses, summarize(latencies, total_s)


def run_incremental(
    z3: str,
    common: str,
    deltas: list[tuple[str, str]],
) -> tuple[list[str], dict[str, float]]:
    proc = subprocess.Popen(
        [z3, "-in", "-smt2"],
        text=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
    )
    assert proc.stdin is not None
    assert proc.stdout is not None

    statuses: list[str] = []
    latencies: list[float] = []
    total_start = time.perf_counter()

    try:
        proc.stdin.write(common)
        proc.stdin.flush()

        for qid, (delta, _expected) in enumerate(deltas):
            start = time.perf_counter()
            proc.stdin.write("(push 1)\n")
            proc.stdin.write(delta)
            proc.stdin.write("(check-sat)\n")
            proc.stdin.flush()

            line = proc.stdout.readline()
            if line == "":
                stderr = proc.stderr.read() if proc.stderr is not None else ""
                raise RuntimeError(f"z3 terminated while reading query {qid}: {stderr}")
            status = line.strip()
            if status not in {"sat", "unsat", "unknown"}:
                raise RuntimeError(f"unexpected z3 output for query {qid}: {line!r}")
            statuses.append(status)

            proc.stdin.write("(pop 1)\n")
            proc.stdin.flush()
            latencies.append(time.perf_counter() - start)

        proc.stdin.write("(exit)\n")
        proc.stdin.flush()
        proc.stdin.close()
        rc = proc.wait(timeout=30)
        if rc != 0:
            stderr = proc.stderr.read() if proc.stderr is not None else ""
            raise RuntimeError(f"incremental z3 exited with {rc}: {stderr}")
    finally:
        if proc.poll() is None:
            proc.kill()

    total_s = time.perf_counter() - total_start
    return statuses, summarize(latencies, total_s)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--z3", default=os.environ.get("Z3", "z3"))
    parser.add_argument("--queries", type=int, default=32)
    parser.add_argument("--prefix-constraints", type=int, default=512)
    parser.add_argument("--dump-dir", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    z3 = shutil.which(args.z3) if os.path.sep not in args.z3 else args.z3
    if not z3 or not Path(z3).exists():
        print(f"error: Z3 not found: {args.z3}", file=sys.stderr)
        return 2
    if args.queries < 1:
        parser.error("--queries must be >= 1")

    if args.dump_dir is not None:
        args.dump_dir.mkdir(parents=True, exist_ok=True)

    common, expected = build_common_prefix(args.prefix_constraints)
    deltas = [
        build_delta(args.prefix_constraints, expected, i)
        for i in range(args.queries)
    ]
    expected_statuses = [status for _delta, status in deltas]

    cold_statuses, cold = run_cold(z3, common, deltas, args.dump_dir)
    incr_statuses, incremental = run_incremental(z3, common, deltas)

    if cold_statuses != expected_statuses:
        raise RuntimeError(
            f"cold results differ from expected: {cold_statuses} vs {expected_statuses}"
        )
    if incr_statuses != expected_statuses:
        raise RuntimeError(
            f"incremental results differ from expected: {incr_statuses} vs {expected_statuses}"
        )

    result = {
        "config": {
            "z3": z3,
            "queries": args.queries,
            "prefix_constraints": args.prefix_constraints,
        },
        "cold": cold,
        "incremental": incremental,
        "speedup_total": (
            cold["total_s"] / incremental["total_s"]
            if incremental["total_s"] > 0
            else None
        ),
        "semantic_match": True,
        "statuses": {
            "sat": cold_statuses.count("sat"),
            "unsat": cold_statuses.count("unsat"),
            "unknown": cold_statuses.count("unknown"),
        },
    }

    encoded = json.dumps(result, indent=2, sort_keys=True)
    print(encoded)
    if args.json is not None:
        args.json.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
