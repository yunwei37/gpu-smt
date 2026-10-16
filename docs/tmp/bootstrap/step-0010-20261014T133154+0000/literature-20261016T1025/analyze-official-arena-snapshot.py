#!/usr/bin/env python3
"""Extract published Arena facts; never run or rank a project GPU benchmark."""
import argparse
import collections
import csv
import gzip
import json
import re
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("snapshot", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    raw = args.snapshot.read_bytes()
    data = json.loads(gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw)
    args.out.mkdir(parents=True, exist_ok=True)
    selected = ("official", "sokonanoda", "mathgraph", "nanoclo",
                "nanoclo-fortran", "parse-only")
    corpora = ("mathlib", "cslib", "init")
    results = []
    for row in data["results"]:
        if row["checker"] not in selected or row["test"] not in corpora:
            continue
        result = {k: row.get(k) for k in (
            "test", "checker", "status", "correctness", "exit_code",
            "wall_time", "cpu_time", "max_rss", "instructions")}
        instructions = result["instructions"]
        result["virtual_cpu_seconds_at_6Ginstr_s"] = (
            instructions / 6_000_000_000 if instructions is not None else None)
        results.append(result)
    results.sort(key=lambda r: (corpora.index(r["test"]), selected.index(r["checker"])))
    if len(results) != len(selected) * len(corpora):
        raise ValueError("selected checker/test population is incomplete in snapshot")
    fields = list(results[0])
    with (args.out / "official-selected-results.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)
    checkers = []
    for c in data["checkers"]:
        if c["name"] not in selected:
            continue
        info = {k: c.get(k) for k in (
            "name", "url", "ref", "rev", "version", "threads", "run", "declines")}
        build = c.get("build", "")
        info["published_build_uses_pgo"] = "profile-generate" in build and "profile-use" in build
        info["published_build_uses_native_target"] = "target-cpu=native" in build
        thread_match = re.search(r'(?:"num_threads":\s*|--threads\s+)(\d+)', build + "\\n" + c.get("run", ""))
        info["configured_threads_from_command"] = int(thread_match.group(1)) if thread_match else c.get("threads")
        info["all_test_correctness_counts"] = dict(collections.Counter(
            r.get("correctness") for r in data["results"] if r["checker"] == c["name"]))
        checkers.append(info)
    tests = [{k: t.get(k) for k in (
        "name", "size", "lines", "lean_version", "lean_githash",
        "lean4export_version", "timeout", "declaration_url", "source_url",
        "outcome")} for t in data["tests"] if t["name"] in corpora]
    output = dict(
        scope="Third-party published snapshot extraction only; no project measurement, speedup, ranking across protocols or metric subtraction",
        source_url="https://arena.lean-lang.org/results.json",
        source_meta=data["meta"],
        raw_snapshot=str(args.snapshot),
        source_counts=dict(checkers=len(data["checkers"]), tests=len(data["tests"]),
                           results=len(data["results"])),
        metric_notes=dict(
            wall_time="published measured wall seconds; not the website virtual CPU column",
            cpu_time="raw reported CPU-time field; not replaced by instruction-derived time",
            virtual_cpu_seconds_at_6Ginstr_s="instructions divided by website fixed 6.0 Ginstr/s",
            max_rss="published raw maximum RSS in bytes; not PSS or GPU memory"),
        checkers=checkers, tests=tests)
    (args.out / "official-snapshot-context.json").write_text(
        json.dumps(output, indent=2) + "\n")
    print(json.dumps(dict(source_meta=data["meta"], selected_rows=len(results))))


if __name__ == "__main__":
    main()
