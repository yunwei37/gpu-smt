#!/usr/bin/env python3
"""Measure fresh-vs-reused solver state through the stock libz3 C API.

This benchmark does not require the z3 CLI or Python z3 bindings. It loads
libz3 with ctypes and compares rebuilding a QF_BV solver for every query
against one persistent solver with push/pop deltas.

This is a synthetic upper-bound experiment, not paper evidence.
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import json
import math
import statistics
import time
from pathlib import Path

MASK64 = (1 << 64) - 1
Z3_L_TRUE = 1
Z3_L_FALSE = -1
Z3_L_UNDEF = 0


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


def summary(latencies: list[float], total: float) -> dict[str, float]:
    return {
        "total_s": total,
        "throughput_qps": len(latencies) / total,
        "latency_ms_mean": statistics.fmean(latencies) * 1e3,
        "latency_ms_p50": percentile(latencies, 0.50) * 1e3,
        "latency_ms_p95": percentile(latencies, 0.95) * 1e3,
        "latency_ms_p99": percentile(latencies, 0.99) * 1e3,
    }


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
        self.l.Z3_solver_push.argtypes = [P, P]
        self.l.Z3_solver_pop.argtypes = [P, P, U]
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


def make_base(z: Z3, ctx, n: int):
    l = z.l
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
        eq = l.Z3_mk_eq(ctx, xs[i + 1], add)
        l.Z3_solver_assert(ctx, solver, eq)

    return sort, xs, solver, value


def add_delta(
    z: Z3,
    ctx,
    sort,
    xlast,
    solver,
    expected: int,
    query_id: int,
) -> None:
    l = z.l
    offset = (query_id * 0xD6E8FEB86659FD93) & MASK64
    offset_ast = l.Z3_mk_unsigned_int64(ctx, offset, sort)
    lhs = l.Z3_mk_bvadd(ctx, xlast, offset_ast)
    rhs_value = (expected + offset + (query_id & 1)) & MASK64
    rhs = l.Z3_mk_unsigned_int64(ctx, rhs_value, sort)
    l.Z3_solver_assert(ctx, solver, l.Z3_mk_eq(ctx, lhs, rhs))


def status_name(value: int) -> str:
    return {
        Z3_L_TRUE: "sat",
        Z3_L_FALSE: "unsat",
        Z3_L_UNDEF: "unknown",
    }.get(value, f"bad:{value}")


def run_fresh(z: Z3, n: int, queries: int):
    latencies = []
    statuses = []
    total_start = time.perf_counter()

    for query_id in range(queries):
        start = time.perf_counter()
        ctx = z.new_context()
        sort, xs, solver, expected = make_base(z, ctx, n)
        add_delta(z, ctx, sort, xs[-1], solver, expected, query_id)
        statuses.append(status_name(z.l.Z3_solver_check(ctx, solver)))
        z.l.Z3_solver_dec_ref(ctx, solver)
        z.l.Z3_del_context(ctx)
        latencies.append(time.perf_counter() - start)

    total = time.perf_counter() - total_start
    return statuses, summary(latencies, total)


def run_reuse(z: Z3, n: int, queries: int):
    total_start = time.perf_counter()
    ctx = z.new_context()
    sort, xs, solver, expected = make_base(z, ctx, n)

    latencies = []
    statuses = []

    for query_id in range(queries):
        start = time.perf_counter()
        z.l.Z3_solver_push(ctx, solver)
        add_delta(z, ctx, sort, xs[-1], solver, expected, query_id)
        statuses.append(status_name(z.l.Z3_solver_check(ctx, solver)))
        z.l.Z3_solver_pop(ctx, solver, 1)
        latencies.append(time.perf_counter() - start)

    z.l.Z3_solver_dec_ref(ctx, solver)
    z.l.Z3_del_context(ctx)
    total = time.perf_counter() - total_start
    return statuses, summary(latencies, total)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--libz3")
    parser.add_argument("--queries", type=int, default=64)
    parser.add_argument("--prefix-constraints", type=int, default=512)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    z3 = Z3(args.libz3)
    expected = [
        "sat" if i % 2 == 0 else "unsat"
        for i in range(args.queries)
    ]

    fresh_status, fresh = run_fresh(
        z3,
        args.prefix_constraints,
        args.queries,
    )
    reuse_status, reuse = run_reuse(
        z3,
        args.prefix_constraints,
        args.queries,
    )

    if fresh_status != expected or reuse_status != expected:
        raise RuntimeError(
            {
                "fresh": fresh_status,
                "reuse": reuse_status,
                "expected": expected,
            }
        )

    result = {
        "config": {
            "libz3": z3.path,
            "z3_version": z3.version,
            "queries": args.queries,
            "prefix_constraints": args.prefix_constraints,
        },
        "fresh": fresh,
        "reuse": reuse,
        "speedup_total": fresh["total_s"] / reuse["total_s"],
        "semantic_match": True,
    }

    encoded = json.dumps(result, indent=2, sort_keys=True)
    print(encoded)
    if args.json:
        args.json.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
