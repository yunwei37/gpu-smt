#!/usr/bin/env python3
"""Recompute native probe decision coverage/errors from retained raw files."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("root", type=Path)
    args = ap.parse_args()
    rows = [json.loads(s) for s in (args.root / "decisions.jsonl").read_text().splitlines()]
    refs = {r["index"]: r for r in rows if r["mode"] == "executable" and r["repeat"] == 0}
    groups = defaultdict(list)
    for row in rows: groups[row["repeat"], row["mode"]].append(row)
    for (repeat, mode), members in sorted(groups.items()):
        counts = Counter()
        differences, short, errors = [], [], []
        for row in members:
            # Relocatable: stored paths contain the original run prefix.
            path = args.root / Path(row["output"]).relative_to(Path(row["output"]).parents[1 if mode != "branch" else 2])
            raw = path.read_text()
            decisions = re.findall(r"^(sat|unsat|unknown)\s*$", raw, re.M)
            counts.update(decisions)
            if len(decisions) != row["expected_checks"]: short.append(row["index"])
            if decisions != refs[row["index"]]["decisions"]: differences.append(row["index"])
            if "(error " in raw: errors.append(row["index"])
        print(json.dumps(dict(repeat=repeat, mode=mode, streams=len(members),
             counts=dict(counts), differing_streams=differences,
             incomplete_streams=short, streams_with_error_output=errors)))
    changed = sorted({r["index"] for r in rows if r["decisions"] != refs[r["index"]]["decisions"]})
    print("Differing source identities:")
    for index in changed:
        row = refs[index]
        print(index, row["trace"])
    processes = [json.loads(s) for s in (args.root / "processes.jsonl").read_text().splitlines()]
    failures = [r for r in processes if r["returncode"]]
    print("Process rows:", len(processes), "nonzero:", len(failures))
    print("Library driver nonzero counts:", dict(Counter((r["repeat"], r["mode"]) for r in failures)))


if __name__ == "__main__": main()
