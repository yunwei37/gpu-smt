#!/usr/bin/env python3
"""Inspect prepared-header diversity using the actual service splitter.

This is an offline cohort/admission analysis, not a cost or cache-benefit metric.
"""
import argparse
import collections
import gzip
import importlib.util
import json
from pathlib import Path
import re
import sys
import zipfile


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--split-module", type=Path, required=True)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--archive", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    spec = importlib.util.spec_from_file_location("actual_service_split", args.split_module)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    headers = collections.Counter()
    ids = set()
    attempts = 0
    with args.input.open() as f:
        for line in f:
            row = json.loads(line)
            headers[module.split_snippet(row["code"]).header] += 1
            if row.get("proof_id") is not None:
                ids.add(row["proof_id"])
            attempts += 1
    result = dict(input=str(args.input), splitter=str(args.split_module),
                  attempts=attempts, headers=dict(headers),
                  scope="actual service header keys; not preparation cost, ready work or saved time")
    if args.archive:
        reuse = collections.Counter()
        prep = collections.Counter()
        ansi = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
        reused = re.compile(r"INFO\s+\[[0-9a-f]{8}\]\s+Reusing \(started\) REPL for (Proof_\d+)")
        prepared = re.compile(r"INFO\s+\[[0-9a-f]{8}\]\s+Running snippet (Proof_\d+)-header:")
        with zipfile.ZipFile(args.archive) as z:
            members = [n for n in z.namelist() if n.endswith("/server.stdout.gz")]
            if len(members) != 1:
                raise ValueError("expected one original captured server stdout")
            with z.open(members[0]) as raw, gzip.GzipFile(fileobj=raw) as f:
                for b in f:
                    line = ansi.sub("", b.decode(errors="replace"))
                    a, b = reused.search(line), prepared.search(line)
                    if a:
                        reuse[a[1]] += 1
                    if b:
                        prep[b[1]] += 1
        result["archive"] = str(args.archive)
        result["events"] = dict(reused_started=sum(reuse.values()),
            reused_unique=len(reuse), prepared=sum(prep.values()), prepared_unique=len(prep),
            repeated_reuse_ids=sum(v > 1 for v in reuse.values()),
            repeated_prep_ids=sum(v > 1 for v in prep.values()),
            overlap_ids=sorted(set(reuse) & set(prep)),
            unobserved_ids=sorted(ids - set(reuse) - set(prep)),
            extra_ids=sorted((set(reuse) | set(prep)) - ids),
            reused_ids=sorted(reuse), prepared_ids=sorted(prep))
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "events"}))
    if "events" in result:
        print(json.dumps({k: v for k, v in result["events"].items()
                          if k not in ["reused_ids", "prepared_ids"]}))


if __name__ == "__main__":
    main()
