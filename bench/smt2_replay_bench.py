#!/usr/bin/env python3
"""Replay real SMT-LIB workloads through stock libz3.

For files containing multiple check-sat commands, compare:
  * fresh: rebuild a solver from the full active context for each query;
  * incremental: replay the original command stream into one solver and retain
    state across push/pop boundaries.

This benchmark currently supports check-sat. Files using check-sat-assuming are
reported but skipped unless converted to explicit assertions by the caller.
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import json
import math
import re
import statistics
import time
from pathlib import Path


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


def split_commands(text: str) -> list[str]:
    commands: list[str] = []
    buf: list[str] = []
    depth = 0
    in_string = False
    in_bar = False
    in_comment = False
    escape = False

    for ch in text:
        if in_comment:
            if ch == "\n":
                in_comment = False
            continue
        if not in_string and not in_bar and ch == ";":
            in_comment = True
            continue
        if in_string:
            buf.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if in_bar:
            buf.append(ch)
            if ch == "|":
                in_bar = False
            continue
        if ch == '"':
            in_string = True
            buf.append(ch)
            continue
        if ch == "|":
            in_bar = True
            buf.append(ch)
            continue
        if ch == "(":
            if depth == 0:
                buf = []
            depth += 1
            buf.append(ch)
        elif ch == ")" and depth > 0:
            depth -= 1
            buf.append(ch)
            if depth == 0:
                cmd = "".join(buf).strip()
                if cmd:
                    commands.append(cmd)
                buf = []
        elif depth > 0:
            buf.append(ch)
    return commands


def normalize(cmd: str) -> str:
    return re.sub(r"\s+", " ", cmd).strip()


def head(cmd: str) -> str:
    match = re.match(r"\(\s*([^\s()]+)", cmd)
    return match.group(1) if match else ""


def int_arg(cmd: str, default: int = 1) -> int:
    match = re.match(r"\(\s*[^\s()]+\s+([0-9]+)", cmd)
    return int(match.group(1)) if match else default


def query_snapshots(commands: list[str]) -> list[list[str]]:
    globals_: list[str] = []
    assertions: list[str] = []
    stack: list[int] = []
    queries: list[list[str]] = []

    for cmd in commands:
        kind = head(cmd)
        if kind == "assert":
            assertions.append(cmd)
        elif kind == "push":
            for _ in range(int_arg(cmd)):
                stack.append(len(assertions))
        elif kind == "pop":
            for _ in range(int_arg(cmd)):
                if not stack:
                    raise RuntimeError("unbalanced pop")
                assertions = assertions[: stack.pop()]
        elif kind == "check-sat":
            queries.append(globals_ + assertions)
        elif kind == "check-sat-assuming":
            raise NotImplementedError("check-sat-assuming is not supported yet")
        elif kind in {
            "get-model",
            "get-value",
            "get-proof",
            "get-unsat-core",
            "echo",
            "exit",
        }:
            continue
        else:
            globals_.append(cmd)

    return queries


class Z3:
    def __init__(self, path: str | None = None):
        libname = path or ctypes.util.find_library("z3")
        if not libname:
            raise RuntimeError("libz3 not found")
        self.path = libname
        self.l = ctypes.CDLL(libname)
        P = ctypes.c_void_p
        U = ctypes.c_uint

        self.l.Z3_mk_config.restype = P
        self.l.Z3_del_config.argtypes = [P]
        self.l.Z3_mk_context.argtypes = [P]
        self.l.Z3_mk_context.restype = P
        self.l.Z3_del_context.argtypes = [P]
        self.l.Z3_mk_solver.argtypes = [P]
        self.l.Z3_mk_solver.restype = P
        self.l.Z3_solver_inc_ref.argtypes = [P, P]
        self.l.Z3_solver_dec_ref.argtypes = [P, P]
        self.l.Z3_solver_from_string.argtypes = [P, P, ctypes.c_char_p]
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

    def context_solver(self):
        cfg = self.l.Z3_mk_config()
        ctx = self.l.Z3_mk_context(cfg)
        self.l.Z3_del_config(cfg)
        solver = self.l.Z3_mk_solver(ctx)
        self.l.Z3_solver_inc_ref(ctx, solver)
        return ctx, solver

    def close(self, ctx, solver) -> None:
        self.l.Z3_solver_dec_ref(ctx, solver)
        self.l.Z3_del_context(ctx)


def run_fresh(z3: Z3, snapshots: list[list[str]], repetitions: int):
    elapsed = []
    statuses = None

    for _ in range(repetitions):
        run_statuses = []
        start = time.perf_counter()
        for query in snapshots:
            ctx, solver = z3.context_solver()
            z3.l.Z3_solver_from_string(
                ctx, solver, ("\n".join(query) + "\n").encode()
            )
            run_statuses.append(z3.l.Z3_solver_check(ctx, solver))
            z3.close(ctx, solver)
        elapsed.append(time.perf_counter() - start)
        statuses = run_statuses

    return elapsed, statuses


def run_incremental(z3: Z3, commands: list[str], repetitions: int):
    e2e_elapsed = []
    warm_elapsed = []
    statuses = None

    for _ in range(repetitions):
        e2e_start = time.perf_counter()
        ctx, solver = z3.context_solver()
        warm_start = time.perf_counter()
        run_statuses = []

        for cmd in commands:
            kind = head(cmd)
            if kind == "push":
                for _ in range(int_arg(cmd)):
                    z3.l.Z3_solver_push(ctx, solver)
            elif kind == "pop":
                z3.l.Z3_solver_pop(ctx, solver, int_arg(cmd))
            elif kind == "check-sat":
                run_statuses.append(z3.l.Z3_solver_check(ctx, solver))
            elif kind == "check-sat-assuming":
                z3.close(ctx, solver)
                raise NotImplementedError(
                    "check-sat-assuming is not supported yet"
                )
            elif kind in {
                "get-model",
                "get-value",
                "get-proof",
                "get-unsat-core",
                "echo",
                "exit",
            }:
                continue
            else:
                z3.l.Z3_solver_from_string(ctx, solver, cmd.encode())

        warm_elapsed.append(time.perf_counter() - warm_start)
        e2e_elapsed.append(time.perf_counter() - e2e_start)
        statuses = run_statuses
        z3.close(ctx, solver)

    return e2e_elapsed, warm_elapsed, statuses


def summarize(values: list[float]) -> dict:
    return {
        "median_ms": statistics.median(values) * 1e3,
        "p95_ms": percentile(values, 0.95) * 1e3,
        "min_ms": min(values) * 1e3,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--libz3")
    parser.add_argument("--repetitions", type=int, default=20)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    z3 = Z3(args.libz3)
    rows = []

    for path in args.files:
        commands = [
            normalize(c)
            for c in split_commands(
                path.read_text(encoding="utf-8", errors="replace")
            )
        ]
        try:
            snapshots = query_snapshots(commands)
        except NotImplementedError as exc:
            rows.append(
                {
                    "file": str(path),
                    "skipped": True,
                    "reason": str(exc),
                }
            )
            continue

        if not snapshots:
            rows.append(
                {
                    "file": str(path),
                    "skipped": True,
                    "reason": "no check-sat commands",
                }
            )
            continue

        fresh_times, fresh_statuses = run_fresh(
            z3, snapshots, args.repetitions
        )
        incremental_e2e_times, incremental_warm_times, incremental_statuses = (
            run_incremental(z3, commands, args.repetitions)
        )

        if fresh_statuses != incremental_statuses:
            raise RuntimeError(
                f"semantic mismatch in {path}: "
                f"{fresh_statuses} vs {incremental_statuses}"
            )

        fresh = summarize(fresh_times)
        incremental_e2e = summarize(incremental_e2e_times)
        incremental_warm = summarize(incremental_warm_times)
        row = {
            "file": str(path),
            "commands": len(commands),
            "queries": len(snapshots),
            "statuses": fresh_statuses,
            "fresh": fresh,
            "incremental_e2e": incremental_e2e,
            "incremental_warm": incremental_warm,
            "speedup_e2e_median": (
                fresh["median_ms"] / incremental_e2e["median_ms"]
            ),
            "speedup_warm_median": (
                fresh["median_ms"] / incremental_warm["median_ms"]
            ),
            "skipped": False,
        }
        rows.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)

    result = {
        "config": {
            "libz3": z3.path,
            "z3_version": z3.version,
            "repetitions": args.repetitions,
        },
        "rows": rows,
    }
    if args.json:
        args.json.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
