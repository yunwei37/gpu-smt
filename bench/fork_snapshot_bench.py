#!/usr/bin/env python3
"""Benchmark fork/COW snapshots of a pre-built stock libz3 solver state.

The baseline forks the same number of children but each child reconstructs the
entire solver context. The snapshot path constructs a shared prefix once in the
parent and then forks children that inherit it copy-on-write.

This is Linux-specific and intentionally does not modify Z3. A production
implementation should use a controlled single-threaded pre-fork phase or a
forkserver; forking arbitrary multi-threaded processes is unsafe.
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import json
import math
import os
import re
import statistics
import time
from pathlib import Path

MASK64 = (1 << 64) - 1
Z3_L_TRUE = 1
Z3_L_FALSE = -1


def percentile(values: list[float], p: float) -> float:
    xs = sorted(values)
    if not xs:
        return 0.0
    if len(xs) == 1:
        return xs[0]
    rank = (len(xs) - 1) * p
    lo = math.floor(rank)
    hi = math.ceil(rank)
    if lo == hi:
        return xs[lo]
    return xs[lo] * (hi - rank) + xs[hi] * (rank - lo)


def smaps_rollup() -> dict[str, int]:
    out: dict[str, int] = {}
    try:
        with open("/proc/self/smaps_rollup", "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(
                    r"^(Rss|Pss|Private_Clean|Private_Dirty|Shared_Clean|Shared_Dirty):\s+(\d+) kB",
                    line,
                )
                if match:
                    out[match.group(1) + "_kb"] = int(match.group(2))
    except OSError:
        pass
    return out


class Z3:
    def __init__(self, path: str | None = None):
        libname = path or ctypes.util.find_library("z3")
        if not libname:
            raise RuntimeError("libz3 not found")
        self.path = libname
        self.l = ctypes.CDLL(libname)

        P = ctypes.c_void_p
        U = ctypes.c_uint
        U64 = ctypes.c_uint64

        self.l.Z3_mk_config.restype = P
        self.l.Z3_del_config.argtypes = [P]
        self.l.Z3_mk_context.argtypes = [P]
        self.l.Z3_mk_context.restype = P
        self.l.Z3_del_context.argtypes = [P]

        self.l.Z3_mk_bv_sort.argtypes = [P, U]
        self.l.Z3_mk_bv_sort.restype = P
        self.l.Z3_mk_string_symbol.argtypes = [P, ctypes.c_char_p]
        self.l.Z3_mk_string_symbol.restype = P
        self.l.Z3_mk_const.argtypes = [P, P, P]
        self.l.Z3_mk_const.restype = P
        self.l.Z3_mk_unsigned_int64.argtypes = [P, U64, P]
        self.l.Z3_mk_unsigned_int64.restype = P
        self.l.Z3_mk_bvadd.argtypes = [P, P, P]
        self.l.Z3_mk_bvadd.restype = P
        self.l.Z3_mk_eq.argtypes = [P, P, P]
        self.l.Z3_mk_eq.restype = P

        self.l.Z3_mk_solver.argtypes = [P]
        self.l.Z3_mk_solver.restype = P
        self.l.Z3_solver_inc_ref.argtypes = [P, P]
        self.l.Z3_solver_dec_ref.argtypes = [P, P]
        self.l.Z3_solver_assert.argtypes = [P, P, P]
        self.l.Z3_solver_check.argtypes = [P, P]
        self.l.Z3_solver_check.restype = ctypes.c_int

        self.version = None
        if hasattr(self.l, "Z3_get_full_version"):
            self.l.Z3_get_full_version.restype = ctypes.c_char_p
            raw = self.l.Z3_get_full_version()
            if raw:
                self.version = raw.decode("utf-8", errors="replace")

    def new_context(self):
        cfg = self.l.Z3_mk_config()
        ctx = self.l.Z3_mk_context(cfg)
        self.l.Z3_del_config(cfg)
        return ctx


def make_base(z: Z3, n: int):
    l = z.l
    ctx = z.new_context()
    sort = l.Z3_mk_bv_sort(ctx, 64)
    xs = []
    for i in range(n + 1):
        sym = l.Z3_mk_string_symbol(ctx, f"x{i}".encode())
        xs.append(l.Z3_mk_const(ctx, sym, sort))

    solver = l.Z3_mk_solver(ctx)
    l.Z3_solver_inc_ref(ctx, solver)

    value = 1
    one = l.Z3_mk_unsigned_int64(ctx, value, sort)
    l.Z3_solver_assert(ctx, solver, l.Z3_mk_eq(ctx, xs[0], one))

    for i in range(n):
        step = (0x9E3779B97F4A7C15 + i * 0x100000001B3) & MASK64
        value = (value + step) & MASK64
        step_ast = l.Z3_mk_unsigned_int64(ctx, step, sort)
        add = l.Z3_mk_bvadd(ctx, xs[i], step_ast)
        l.Z3_solver_assert(ctx, solver, l.Z3_mk_eq(ctx, xs[i + 1], add))

    return ctx, sort, xs[-1], solver, value


def add_delta(z: Z3, ctx, sort, xlast, solver, value: int, qid: int) -> None:
    l = z.l
    offset = (qid * 0xD6E8FEB86659FD93) & MASK64
    offset_ast = l.Z3_mk_unsigned_int64(ctx, offset, sort)
    lhs = l.Z3_mk_bvadd(ctx, xlast, offset_ast)
    rhs = l.Z3_mk_unsigned_int64(
        ctx, (value + offset + (qid & 1)) & MASK64, sort
    )
    l.Z3_solver_assert(ctx, solver, l.Z3_mk_eq(ctx, lhs, rhs))


def child_send(fd: int, payload: dict) -> None:
    os.write(fd, (json.dumps(payload, separators=(",", ":")) + "\n").encode())


def launch_fresh(z: Z3, n: int, qid: int, fd: int) -> None:
    start = time.perf_counter()
    ctx, sort, xlast, solver, value = make_base(z, n)
    add_delta(z, ctx, sort, xlast, solver, value, qid)
    status = z.l.Z3_solver_check(ctx, solver)
    child_send(
        fd,
        {
            "qid": qid,
            "status": status,
            "elapsed_s": time.perf_counter() - start,
            "mem": smaps_rollup(),
        },
    )
    z.l.Z3_solver_dec_ref(ctx, solver)
    z.l.Z3_del_context(ctx)


def launch_snapshot(
    z: Z3, ctx, sort, xlast, solver, value: int, qid: int, fd: int
) -> None:
    start = time.perf_counter()
    add_delta(z, ctx, sort, xlast, solver, value, qid)
    status = z.l.Z3_solver_check(ctx, solver)
    child_send(
        fd,
        {
            "qid": qid,
            "status": status,
            "elapsed_s": time.perf_counter() - start,
            "mem": smaps_rollup(),
        },
    )


def run_children(fn, queries: list[int], width: int):
    start = time.perf_counter()
    records = []

    for base in range(0, len(queries), width):
        children = []
        for qid in queries[base : base + width]:
            read_fd, write_fd = os.pipe()
            pid = os.fork()
            if pid == 0:
                try:
                    os.close(read_fd)
                    fn(qid, write_fd)
                finally:
                    try:
                        os.close(write_fd)
                    finally:
                        os._exit(0)

            os.close(write_fd)
            children.append((pid, read_fd))

        for pid, read_fd in children:
            data = b""
            while True:
                chunk = os.read(read_fd, 65536)
                if not chunk:
                    break
                data += chunk
            os.close(read_fd)
            _, status = os.waitpid(pid, 0)
            if status != 0:
                raise RuntimeError(f"child {pid} failed: wait status {status}")
            records.append(json.loads(data.decode("utf-8")))

    return time.perf_counter() - start, records


def summarize(total_s: float, records: list[dict]) -> dict:
    latencies = [r["elapsed_s"] for r in records]
    pss = [
        r["mem"]["Pss_kb"]
        for r in records
        if r.get("mem", {}).get("Pss_kb") is not None
    ]
    return {
        "total_s": total_s,
        "throughput_qps": len(records) / total_s,
        "child_latency_ms_p50": percentile(latencies, 0.50) * 1e3,
        "child_latency_ms_p95": percentile(latencies, 0.95) * 1e3,
        "child_pss_kb_p50": percentile(pss, 0.50) if pss else None,
    }


def median_metric(runs: list[dict], key: str):
    values = [r[key] for r in runs if r[key] is not None]
    return statistics.median(values) if values else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--libz3")
    parser.add_argument("--queries", type=int, default=32)
    parser.add_argument("--prefix-sizes", default="64,256,1024")
    parser.add_argument("--widths", default="1,2,4")
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    if not hasattr(os, "fork"):
        raise RuntimeError("this benchmark requires os.fork()")

    z3 = Z3(args.libz3)
    queries = list(range(args.queries))
    expected = [Z3_L_TRUE if q % 2 == 0 else Z3_L_FALSE for q in queries]
    rows = []

    for prefix_size in [
        int(x) for x in args.prefix_sizes.split(",") if x.strip()
    ]:
        for width in [int(x) for x in args.widths.split(",") if x.strip()]:
            fresh_runs = []
            snapshot_runs = []

            for _ in range(args.repetitions):
                fresh_total, fresh_records = run_children(
                    lambda q, fd: launch_fresh(z3, prefix_size, q, fd),
                    queries,
                    width,
                )

                ctx, sort, xlast, solver, value = make_base(z3, prefix_size)
                snapshot_total, snapshot_records = run_children(
                    lambda q, fd: launch_snapshot(
                        z3, ctx, sort, xlast, solver, value, q, fd
                    ),
                    queries,
                    width,
                )
                z3.l.Z3_solver_dec_ref(ctx, solver)
                z3.l.Z3_del_context(ctx)

                fresh_records.sort(key=lambda r: r["qid"])
                snapshot_records.sort(key=lambda r: r["qid"])
                if [r["status"] for r in fresh_records] != expected:
                    raise RuntimeError("fresh semantic mismatch")
                if [r["status"] for r in snapshot_records] != expected:
                    raise RuntimeError("snapshot semantic mismatch")

                fresh_runs.append(summarize(fresh_total, fresh_records))
                snapshot_runs.append(
                    summarize(snapshot_total, snapshot_records)
                )

            fresh_total = median_metric(fresh_runs, "total_s")
            snapshot_total = median_metric(snapshot_runs, "total_s")
            row = {
                "prefix_constraints": prefix_size,
                "parallel_width": width,
                "queries": args.queries,
                "repetitions": args.repetitions,
                "fresh_total_s_median": fresh_total,
                "snapshot_total_s_median": snapshot_total,
                "speedup_total": fresh_total / snapshot_total,
                "fresh_child_latency_ms_p50": median_metric(
                    fresh_runs, "child_latency_ms_p50"
                ),
                "snapshot_child_latency_ms_p50": median_metric(
                    snapshot_runs, "child_latency_ms_p50"
                ),
                "fresh_child_pss_kb_p50": median_metric(
                    fresh_runs, "child_pss_kb_p50"
                ),
                "snapshot_child_pss_kb_p50": median_metric(
                    snapshot_runs, "child_pss_kb_p50"
                ),
            }
            rows.append(row)
            print(json.dumps(row, sort_keys=True), flush=True)

    result = {
        "config": {
            "libz3": z3.path,
            "z3_version": z3.version,
        },
        "rows": rows,
        "semantic_match": True,
        "note": (
            "Linux fork/COW experiment. Production code must control threads "
            "before fork; do not fork arbitrary multithreaded solver processes."
        ),
    }
    if args.json:
        args.json.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
