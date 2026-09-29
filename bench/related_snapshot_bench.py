#!/usr/bin/env python3
"""Benchmark fork/COW fan-out on real multi-check SMT-LIB files.

For each input file, reconstruct the active context at each check-sat, find the
longest exact command prefix shared by all checks, and compare:

1. fresh-parallel: fork one child per check; each child rebuilds common+delta;
2. snapshot-parallel: build the common prefix once, then fork one child per
   check and apply only its delta.

This keeps stock libz3 unmodified. It is useful for branch-like verification
workloads in which several checks share a large prelude.
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import json
import os
from pathlib import Path
import re
import statistics
import struct
import time


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


def snapshots(path: Path) -> list[list[str]]:
    commands = [
        normalize(c)
        for c in split_commands(
            path.read_text(encoding="utf-8", errors="replace")
        )
    ]
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
            raise NotImplementedError(
                "check-sat-assuming is not supported yet"
            )
        elif kind in {
            "echo",
            "get-value",
            "get-model",
            "get-proof",
            "get-unsat-core",
            "exit",
        }:
            continue
        else:
            globals_.append(cmd)
    return queries


def common_prefix(queries: list[list[str]]) -> tuple[list[str], list[list[str]]]:
    if not queries:
        return [], []
    limit = min(len(query) for query in queries)
    shared = 0
    while shared < limit:
        item = queries[0][shared]
        if not all(query[shared] == item for query in queries[1:]):
            break
        shared += 1
    return queries[0][:shared], [query[shared:] for query in queries]


class Z3:
    def __init__(self, path: str | None = None):
        libname = path or ctypes.util.find_library("z3")
        if not libname:
            raise RuntimeError("libz3 not found")
        self.path = libname
        self.l = ctypes.CDLL(libname)
        P = ctypes.c_void_p

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

    def close(self, ctx, solver):
        self.l.Z3_solver_dec_ref(ctx, solver)
        self.l.Z3_del_context(ctx)


def solve_fresh(z3: Z3, commands: list[str]):
    ctx, solver = z3.context_solver()
    start = time.perf_counter()
    z3.l.Z3_solver_from_string(
        ctx, solver, ("\n".join(commands) + "\n").encode()
    )
    status = z3.l.Z3_solver_check(ctx, solver)
    elapsed = time.perf_counter() - start
    z3.close(ctx, solver)
    return status, elapsed


def fresh_parallel(z3: Z3, common: list[str], deltas: list[list[str]]):
    start = time.perf_counter()
    children = []
    for delta in deltas:
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        if pid == 0:
            try:
                os.close(read_fd)
                status, elapsed = solve_fresh(z3, common + delta)
                os.write(
                    write_fd,
                    struct.pack("id", status, elapsed),
                )
            finally:
                try:
                    os.close(write_fd)
                finally:
                    os._exit(0)
        os.close(write_fd)
        children.append((pid, read_fd))

    records = []
    for pid, read_fd in children:
        data = b""
        while len(data) < struct.calcsize("id"):
            chunk = os.read(read_fd, 64)
            if not chunk:
                break
            data += chunk
        os.close(read_fd)
        _, wait_status = os.waitpid(pid, 0)
        if wait_status != 0:
            raise RuntimeError(f"fresh child {pid} failed")
        records.append(struct.unpack("id", data))
    return time.perf_counter() - start, records


def snapshot_parallel(
    z3: Z3,
    common: list[str],
    deltas: list[list[str]],
):
    ctx, solver = z3.context_solver()
    if common:
        z3.l.Z3_solver_from_string(
            ctx, solver, ("\n".join(common) + "\n").encode()
        )

    start = time.perf_counter()
    children = []
    for delta in deltas:
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        if pid == 0:
            try:
                os.close(read_fd)
                child_start = time.perf_counter()
                if delta:
                    z3.l.Z3_solver_from_string(
                        ctx,
                        solver,
                        ("\n".join(delta) + "\n").encode(),
                    )
                status = z3.l.Z3_solver_check(ctx, solver)
                elapsed = time.perf_counter() - child_start
                os.write(
                    write_fd,
                    struct.pack("id", status, elapsed),
                )
            finally:
                try:
                    os.close(write_fd)
                finally:
                    os._exit(0)
        os.close(write_fd)
        children.append((pid, read_fd))

    records = []
    for pid, read_fd in children:
        data = b""
        while len(data) < struct.calcsize("id"):
            chunk = os.read(read_fd, 64)
            if not chunk:
                break
            data += chunk
        os.close(read_fd)
        _, wait_status = os.waitpid(pid, 0)
        if wait_status != 0:
            z3.close(ctx, solver)
            raise RuntimeError(f"snapshot child {pid} failed")
        records.append(struct.unpack("id", data))

    elapsed = time.perf_counter() - start
    z3.close(ctx, solver)
    return elapsed, records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--libz3")
    parser.add_argument("--repetitions", type=int, default=30)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    if not hasattr(os, "fork"):
        raise RuntimeError("this benchmark requires os.fork()")

    z3 = Z3(args.libz3)
    rows = []

    for path in args.files:
        try:
            queries = snapshots(path)
        except NotImplementedError as exc:
            rows.append(
                {
                    "file": str(path),
                    "skipped": True,
                    "reason": str(exc),
                }
            )
            continue

        if len(queries) < 2:
            rows.append(
                {
                    "file": str(path),
                    "skipped": True,
                    "reason": "need at least two check-sat queries",
                }
            )
            continue

        common, deltas = common_prefix(queries)
        fresh_times = []
        snapshot_times = []
        reference_status = None

        for _ in range(args.repetitions):
            fresh_t, fresh_records = fresh_parallel(
                z3, common, deltas
            )
            snapshot_t, snapshot_records = snapshot_parallel(
                z3, common, deltas
            )
            fresh_status = [record[0] for record in fresh_records]
            snapshot_status = [
                record[0] for record in snapshot_records
            ]
            if fresh_status != snapshot_status:
                raise RuntimeError(
                    f"semantic mismatch in {path}: "
                    f"{fresh_status} vs {snapshot_status}"
                )
            reference_status = fresh_status
            fresh_times.append(fresh_t)
            snapshot_times.append(snapshot_t)

        fresh = statistics.median(fresh_times)
        snapshot = statistics.median(snapshot_times)
        row = {
            "file": str(path),
            "queries": len(queries),
            "common_commands": len(common),
            "delta_commands": [len(delta) for delta in deltas],
            "fresh_parallel_ms_median": fresh * 1e3,
            "snapshot_parallel_ms_median": snapshot * 1e3,
            "speedup_median": fresh / snapshot,
            "statuses": reference_status,
            "repetitions": args.repetitions,
            "skipped": False,
        }
        rows.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)

    result = {
        "config": {
            "libz3": z3.path,
            "z3_version": z3.version,
        },
        "rows": rows,
        "note": (
            "Fork/COW experiment. A production implementation must use a "
            "controlled single-threaded forkserver or equivalent mechanism."
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
