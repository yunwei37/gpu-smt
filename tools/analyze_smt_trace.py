#!/usr/bin/env python3
"""Analyze reuse opportunities in captured SMT-LIB traces.

The analyzer reconstructs assertion contexts at each check-sat/check-sat-assuming
point, then measures exact duplicates and nearest-recent common-prefix sharing.
It is intentionally conservative and syntactic: semantic equivalence and
commutative reordering are not inferred.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re


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
                if depth > 0:
                    buf.append(" ")
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


def command_head(cmd: str) -> str:
    m = re.match(r"\(\s*([^\s()]+)", cmd)
    return m.group(1) if m else ""


def int_arg(cmd: str, default: int = 1) -> int:
    m = re.match(r"\(\s*[^\s()]+\s+([0-9]+)", cmd)
    return int(m.group(1)) if m else default


def snapshot_queries(path: Path) -> list[list[str]]:
    commands = [
        normalize(c)
        for c in split_commands(path.read_text(encoding="utf-8", errors="replace"))
    ]

    global_cmds: list[str] = []
    assertions: list[str] = []
    stack: list[int] = []
    queries: list[list[str]] = []

    for cmd in commands:
        head = command_head(cmd)
        if head == "assert":
            assertions.append(cmd)
        elif head == "push":
            n = int_arg(cmd)
            for _ in range(n):
                stack.append(len(assertions))
        elif head == "pop":
            n = int_arg(cmd)
            for _ in range(n):
                if not stack:
                    break
                assertions = assertions[: stack.pop()]
        elif head in {"check-sat", "check-sat-assuming"}:
            queries.append(global_cmds + assertions + [cmd])
        elif head in {"get-model", "get-proof", "get-unsat-core", "get-value", "exit"}:
            continue
        else:
            # Conservatively treat declarations/options/definitions as global.
            global_cmds.append(cmd)

    return queries


def digest_query(cmds: list[str]) -> str:
    h = hashlib.sha256()
    for cmd in cmds:
        h.update(cmd.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def lcp_len(a: list[str], b: list[str]) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace_dir", type=Path)
    parser.add_argument(
        "--window",
        type=int,
        default=256,
        help="nearest-recent query search window",
    )
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    paths = sorted(
        p
        for p in args.trace_dir.rglob("*")
        if p.is_file() and p.suffix in {".smt2", ".smt"}
    )
    all_queries: list[tuple[str, list[str]]] = []
    per_file: dict[str, int] = {}

    for path in paths:
        qs = snapshot_queries(path)
        per_file[str(path)] = len(qs)
        for q in qs:
            all_queries.append((str(path), q))

    seen: set[str] = set()
    exact_hits = 0
    prefix_fractions: list[float] = []
    nearest_prefix_commands: list[int] = []

    for i, (_source, query) in enumerate(all_queries):
        d = digest_query(query)
        if d in seen:
            exact_hits += 1
        seen.add(d)

        best = 0
        start = max(0, i - max(args.window, 0))
        for j in range(start, i):
            best = max(best, lcp_len(query, all_queries[j][1]))
        nearest_prefix_commands.append(best)
        prefix_fractions.append((best / len(query)) if query else 0.0)

    sizes = [len(q) for _src, q in all_queries]
    result = {
        "files": len(paths),
        "queries": len(all_queries),
        "unique_queries": len(seen),
        "exact_duplicate_queries": exact_hits,
        "exact_duplicate_fraction": (
            exact_hits / len(all_queries) if all_queries else 0.0
        ),
        "commands_per_query": {
            "mean": (sum(sizes) / len(sizes)) if sizes else 0.0,
            "p50": percentile([float(x) for x in sizes], 0.50),
            "p95": percentile([float(x) for x in sizes], 0.95),
            "p99": percentile([float(x) for x in sizes], 0.99),
        },
        "nearest_recent_prefix_fraction": {
            "mean": (
                sum(prefix_fractions) / len(prefix_fractions)
                if prefix_fractions
                else 0.0
            ),
            "p50": percentile(prefix_fractions, 0.50),
            "p95": percentile(prefix_fractions, 0.95),
            "p99": percentile(prefix_fractions, 0.99),
        },
        "nearest_recent_prefix_commands": {
            "mean": (
                sum(nearest_prefix_commands) / len(nearest_prefix_commands)
                if nearest_prefix_commands
                else 0.0
            ),
            "p50": percentile(
                [float(x) for x in nearest_prefix_commands], 0.50
            ),
            "p95": percentile(
                [float(x) for x in nearest_prefix_commands], 0.95
            ),
            "p99": percentile(
                [float(x) for x in nearest_prefix_commands], 0.99
            ),
        },
        "window": args.window,
        "per_file_queries": per_file,
        "notes": [
            "Similarity is syntactic and command-order sensitive.",
            "Scoped declarations and unusual SMT-LIB command patterns may not be reconstructed exactly.",
            "The metric is intended to falsify/validate the reuse hypothesis before implementing a runtime.",
        ],
    }

    encoded = json.dumps(result, indent=2, sort_keys=True)
    print(encoded)
    if args.json is not None:
        args.json.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
