#!/usr/bin/env python3
"""Analyze reuse opportunities in captured SMT-LIB traces.

The analyzer reconstructs assertion contexts at each check-sat/check-sat-assuming
point and reports several conservative syntactic reuse metrics:

* exact duplicate queries;
* ordered common-prefix sharing;
* order-insensitive exact-command context overlap;
* byte-weighted context overlap;
* estimated command transitions to a nearby reusable context.

These metrics intentionally do not attempt semantic equivalence. The purpose is
first to determine whether a stateful runtime has enough obvious structure to
exploit before implementing expensive canonicalization or solver changes.
"""

from __future__ import annotations

import argparse
from collections import Counter
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
    # Quoted symbols and string literals are part of the input identity.
    # Collapsing their whitespace would create false exact-reuse matches.
    out = []
    quoted = None
    escaped = False
    pending_space = False
    for ch in cmd.strip():
        if quoted:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\" and quoted == '"':
                escaped = True
            elif ch == quoted:
                quoted = None
        elif ch.isspace():
            pending_space = True
        else:
            if pending_space and out:
                out.append(' ')
            pending_space = False
            out.append(ch)
            if ch in ('"', '|'):
                quoted = ch
    return ''.join(out)


def command_head(cmd: str) -> str:
    match = re.match(r"\(\s*([^\s()]+)", cmd)
    return match.group(1) if match else ""


def int_arg(cmd: str, default: int = 1) -> int:
    match = re.match(r"\(\s*[^\s()]+\s+([0-9]+)", cmd)
    return int(match.group(1)) if match else default


def snapshot_queries(path: Path) -> list[list[str]]:
    commands = [
        normalize(c)
        for c in split_commands(
            path.read_text(encoding="utf-8", errors="replace")
        )
    ]

    # Keep the observed command order. Declarations are scoped by push/pop
    # unless :global-decls is enabled; options remain global. Treating every
    # declaration as global inflated reuse on real multi-query Verus sessions.
    active: list[tuple[str, int | None, bool]] = []
    depth = 0
    global_decls = False
    queries: list[list[str]] = []

    for cmd in commands:
        head = command_head(cmd)
        if head == "assert":
            active.append((cmd, depth, True))
        elif head == "push":
            depth += int_arg(cmd)
        elif head == "pop":
            depth = max(0, depth - int_arg(cmd))
            active = [r for r in active if r[1] is None or r[1] <= depth]
        elif head == "reset":
            active = []
            depth = 0
            global_decls = False
        elif head == "reset-assertions":
            active = [r for r in active if not r[2] and (r[1] is None or r[1] == 0)]
            depth = 0
        elif head in {"check-sat", "check-sat-assuming"}:
            queries.append([r[0] for r in active] + [cmd])
        elif head in {
            "get-info",
            "get-option",
            "get-model",
            "get-proof",
            "get-unsat-core",
            "get-value",
            "echo",
            "exit",
        }:
            continue
        else:
            if head == "set-option" and ":global-decls" in cmd:
                global_decls = bool(re.search(r":global-decls\s+true", cmd))
            scoped = head.startswith("declare-") or head.startswith("define-")
            active.append((cmd, depth if scoped and not global_decls else None, False))

    return queries


def digest_query(cmds: list[str]) -> str:
    h = hashlib.sha256()
    for cmd in cmds:
        h.update(cmd.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def query_context(cmds: list[str]) -> list[str]:
    if cmds and command_head(cmds[-1]) in {"check-sat", "check-sat-assuming"}:
        return cmds[:-1]
    return cmds


def lcp_len(a: list[str], b: list[str]) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


def multiset_common_count(a: list[str], b: list[str]) -> int:
    return sum((Counter(a) & Counter(b)).values())


def multiset_common_bytes(a: list[str], b: list[str]) -> int:
    common = Counter(a) & Counter(b)
    return sum((len(cmd) + 1) * count for cmd, count in common.items())


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


def distribution(values: list[float]) -> dict[str, float]:
    return {
        "mean": (sum(values) / len(values)) if values else 0.0,
        "p50": percentile(values, 0.50),
        "p95": percentile(values, 0.95),
        "p99": percentile(values, 0.99),
    }


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
        path
        for path in args.trace_dir.rglob("*")
        if path.is_file() and path.suffix in {".smt2", ".smt"}
    )
    all_queries: list[tuple[str, list[str]]] = []
    per_file: dict[str, int] = {}

    for path in paths:
        queries = snapshot_queries(path)
        per_file[str(path)] = len(queries)
        for query in queries:
            all_queries.append((str(path), query))

    seen: set[str] = set()
    exact_hits = 0
    prefix_fractions: list[float] = []
    nearest_prefix_commands: list[int] = []
    overlap_fractions: list[float] = []
    byte_overlap_fractions: list[float] = []
    transition_commands: list[float] = []

    for i, (_source, query) in enumerate(all_queries):
        digest = digest_query(query)
        if digest in seen:
            exact_hits += 1
        seen.add(digest)

        context = query_context(query)
        best_prefix = 0
        best_common = 0
        best_common_bytes = 0
        best_transition = len(context)

        start = max(0, i - max(args.window, 0))
        for j in range(start, i):
            previous = query_context(all_queries[j][1])
            prefix = lcp_len(context, previous)
            common = multiset_common_count(context, previous)
            common_bytes = multiset_common_bytes(context, previous)
            transition = (
                len(context) - common + len(previous) - common
            )

            best_prefix = max(best_prefix, prefix)

            candidate = (common, common_bytes, -transition)
            incumbent = (
                best_common,
                best_common_bytes,
                -best_transition,
            )
            if candidate > incumbent:
                best_common = common
                best_common_bytes = common_bytes
                best_transition = transition

        nearest_prefix_commands.append(best_prefix)
        prefix_fractions.append(
            (best_prefix / len(context)) if context else 0.0
        )
        overlap_fractions.append(
            (best_common / len(context)) if context else 0.0
        )
        total_bytes = sum(len(cmd) + 1 for cmd in context)
        byte_overlap_fractions.append(
            (best_common_bytes / total_bytes) if total_bytes else 0.0
        )
        transition_commands.append(float(best_transition))

    sizes = [len(query_context(q)) for _src, q in all_queries]
    result = {
        "files": len(paths),
        "queries": len(all_queries),
        "unique_queries": len(seen),
        "exact_duplicate_queries": exact_hits,
        "exact_duplicate_fraction": (
            exact_hits / len(all_queries) if all_queries else 0.0
        ),
        "commands_per_query": distribution([float(x) for x in sizes]),
        "nearest_recent_prefix_fraction": distribution(prefix_fractions),
        "nearest_recent_prefix_commands": distribution(
            [float(x) for x in nearest_prefix_commands]
        ),
        "nearest_recent_context_overlap_fraction": distribution(
            overlap_fractions
        ),
        "nearest_recent_context_byte_overlap_fraction": distribution(
            byte_overlap_fractions
        ),
        "nearest_recent_transition_commands": distribution(
            transition_commands
        ),
        "window": args.window,
        "per_file_queries": per_file,
        "notes": [
            "Prefix similarity is exact and order-sensitive.",
            (
                "Context overlap is exact normalized-command multiset overlap; "
                "it is order-insensitive but not semantic equivalence."
            ),
            (
                "Transition commands approximate edits to the nearest recent "
                "context; a runtime still has to preserve scopes and backend "
                "semantics."
            ),
            (
                "These conservative metrics are intended to falsify/validate "
                "the reuse hypothesis before implementing solver changes."
            ),
        ],
    }

    encoded = json.dumps(result, indent=2, sort_keys=True)
    print(encoded)
    if args.json is not None:
        args.json.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
