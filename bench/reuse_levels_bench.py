#!/usr/bin/env python3
"""Decompose the benefit of reuse into AST reuse vs live solver-state reuse.

Three execution paths use stock libz3:

1. cold: new Z3 context, ASTs, and solver for every query;
2. ast-reuse: one Z3 context and one shared AST prefix, but a fresh solver for
   every query;
3. live: one context, one AST prefix, and one persistent solver using push/pop.

This helps distinguish parser/term-construction savings from the additional
benefit of retaining solver-internal state.
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import json
import math
from pathlib import Path
import statistics
import time

MASK64 = (1 << 64) - 1


def percentile(values: list[float], p: float) -> float:
    values = sorted(values)
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    rank = (len(values) - 1) * p
    lo = math.floor(rank)
    hi = math.ceil(rank)
    if lo == hi:
        return values[lo]
    return values[lo] * (hi - rank) + values[hi] * (rank - lo)


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

        signatures = [
            ("Z3_mk_config", P, []),
            ("Z3_mk_context", P, [P]),
            ("Z3_mk_bv_sort", P, [P, U]),
            ("Z3_mk_string_symbol", P, [P, ctypes.c_char_p]),
            ("Z3_mk_const", P, [P, P, P]),
            ("Z3_mk_unsigned_int64", P, [P, U64, P]),
            ("Z3_mk_bvadd", P, [P, P, P]),
            ("Z3_mk_eq", P, [P, P, P]),
            ("Z3_mk_solver", P, [P]),
        ]
        for name, restype, argtypes in signatures:
            fn = getattr(self.l, name)
            fn.restype = restype
            fn.argtypes = argtypes

        self.l.Z3_del_config.argtypes = [P]
        self.l.Z3_del_context.argtypes = [P]
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

    def context(self):
        cfg = self.l.Z3_mk_config()
        ctx = self.l.Z3_mk_context(cfg)
        self.l.Z3_del_config(cfg)
        return ctx


def build_terms(z3: Z3, ctx, constraints: int):
    l = z3.l
    sort = l.Z3_mk_bv_sort(ctx, 64)
    xs = [
        l.Z3_mk_const(
            ctx,
            l.Z3_mk_string_symbol(ctx, f"x{i}".encode()),
            sort,
        )
        for i in range(constraints + 1)
    ]

    value = 1
    formulas = [
        l.Z3_mk_eq(
            ctx,
            xs[0],
            l.Z3_mk_unsigned_int64(ctx, value, sort),
        )
    ]
    for i in range(constraints):
        step = (0x9E3779B97F4A7C15 + i * 0x100000001B3) & MASK64
        value = (value + step) & MASK64
        formulas.append(
            l.Z3_mk_eq(
                ctx,
                xs[i + 1],
                l.Z3_mk_bvadd(
                    ctx,
                    xs[i],
                    l.Z3_mk_unsigned_int64(ctx, step, sort),
                ),
            )
        )
    return sort, xs[-1], formulas, value


def make_solver(z3: Z3, ctx, formulas):
    solver = z3.l.Z3_mk_solver(ctx)
    z3.l.Z3_solver_inc_ref(ctx, solver)
    for formula in formulas:
        z3.l.Z3_solver_assert(ctx, solver, formula)
    return solver


def add_delta(z3: Z3, ctx, sort, xlast, solver, expected: int, qid: int):
    offset = (qid * 0xD6E8FEB86659FD93) & MASK64
    lhs = z3.l.Z3_mk_bvadd(
        ctx,
        xlast,
        z3.l.Z3_mk_unsigned_int64(ctx, offset, sort),
    )
    rhs = z3.l.Z3_mk_unsigned_int64(
        ctx,
        (expected + offset + (qid & 1)) & MASK64,
        sort,
    )
    z3.l.Z3_solver_assert(
        ctx,
        solver,
        z3.l.Z3_mk_eq(ctx, lhs, rhs),
    )


def run_cold(z3: Z3, constraints: int, queries: int):
    statuses = []
    start = time.perf_counter()
    for qid in range(queries):
        ctx = z3.context()
        sort, xlast, formulas, expected = build_terms(
            z3, ctx, constraints
        )
        solver = make_solver(z3, ctx, formulas)
        add_delta(z3, ctx, sort, xlast, solver, expected, qid)
        statuses.append(z3.l.Z3_solver_check(ctx, solver))
        z3.l.Z3_solver_dec_ref(ctx, solver)
        z3.l.Z3_del_context(ctx)
    return time.perf_counter() - start, statuses


def run_ast_reuse(z3: Z3, constraints: int, queries: int):
    ctx = z3.context()
    sort, xlast, formulas, expected = build_terms(z3, ctx, constraints)
    statuses = []
    start = time.perf_counter()
    for qid in range(queries):
        solver = make_solver(z3, ctx, formulas)
        add_delta(z3, ctx, sort, xlast, solver, expected, qid)
        statuses.append(z3.l.Z3_solver_check(ctx, solver))
        z3.l.Z3_solver_dec_ref(ctx, solver)
    elapsed = time.perf_counter() - start
    z3.l.Z3_del_context(ctx)
    return elapsed, statuses


def run_live(z3: Z3, constraints: int, queries: int):
    ctx = z3.context()
    sort, xlast, formulas, expected = build_terms(z3, ctx, constraints)
    solver = make_solver(z3, ctx, formulas)
    statuses = []
    start = time.perf_counter()
    for qid in range(queries):
        z3.l.Z3_solver_push(ctx, solver)
        add_delta(z3, ctx, sort, xlast, solver, expected, qid)
        statuses.append(z3.l.Z3_solver_check(ctx, solver))
        z3.l.Z3_solver_pop(ctx, solver, 1)
    elapsed = time.perf_counter() - start
    z3.l.Z3_solver_dec_ref(ctx, solver)
    z3.l.Z3_del_context(ctx)
    return elapsed, statuses


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--libz3")
    parser.add_argument("--queries", type=int, default=32)
    parser.add_argument("--prefix-sizes", default="16,64,256,1024")
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    z3 = Z3(args.libz3)
    rows = []

    for constraints in [
        int(x) for x in args.prefix_sizes.split(",") if x.strip()
    ]:
        samples = {"cold": [], "ast_reuse": [], "live": []}
        reference_status = None

        for _ in range(args.repetitions):
            cold_t, cold_s = run_cold(z3, constraints, args.queries)
            ast_t, ast_s = run_ast_reuse(
                z3, constraints, args.queries
            )
            live_t, live_s = run_live(z3, constraints, args.queries)

            if not (cold_s == ast_s == live_s):
                raise RuntimeError("semantic mismatch between reuse levels")
            reference_status = cold_s
            samples["cold"].append(cold_t)
            samples["ast_reuse"].append(ast_t)
            samples["live"].append(live_t)

        cold = statistics.median(samples["cold"])
        ast = statistics.median(samples["ast_reuse"])
        live = statistics.median(samples["live"])

        row = {
            "prefix_constraints": constraints,
            "queries": args.queries,
            "repetitions": args.repetitions,
            "cold_total_ms_median": cold * 1e3,
            "ast_reuse_total_ms_median": ast * 1e3,
            "live_total_ms_median": live * 1e3,
            "cold_over_ast": cold / ast,
            "ast_over_live": ast / live,
            "cold_over_live": cold / live,
            "statuses": {
                "sat": reference_status.count(1),
                "unsat": reference_status.count(-1),
                "unknown": reference_status.count(0),
            },
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
    }
    if args.json:
        args.json.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
