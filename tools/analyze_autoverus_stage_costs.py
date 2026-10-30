#!/usr/bin/env python3
"""Partition retained Verus --time-expanded records; never rerun verification."""
import argparse
import collections
import csv
import gzip
import json
from pathlib import Path

METRICS = ("external_s", "covered_external_s", "native_s", "rust_s", "vir_s",
           "air_excluding_smt_s", "smt_init_s", "smt_run_s", "residual_s")

def partition(cell):
    t = (cell.get("native_json") or {}).get("times-ms")
    out = {k: None for k in METRICS}
    out["external_s"] = cell["external_wall_s"]
    if t is None:
        return out
    if t["num-threads"] != 1:
        raise ValueError("This wall-clock partition requires the retained single-thread point")
    smt = t.get("smt")
    out.update(covered_external_s=cell["external_wall_s"],
               native_s=t["total"] / 1000, rust_s=t["rust"]["total"] / 1000,
               vir_s=t["verification"]["vir"]["total"] / 1000,
               air_excluding_smt_s=t["air"]["total"] / 1000,
               smt_init_s=None if smt is None else smt["smt-init"] / 1000,
               smt_run_s=None if smt is None else smt["smt-run"] / 1000)
    # When SMT fields are absent, residual retains all unreported time.
    residual_ms = t["total"] - t["rust"]["total"] - t["verification"]["vir"]["total"] - t["air"]["total"]
    if smt is not None:
        if smt["total"] != smt["smt-init"] + smt["smt-run"]:
            raise ValueError("Inconsistent SMT totals")
        residual_ms -= smt["total"]
    if residual_ms < 0:
        raise ValueError("Overlapping or inconsistent timers")
    out["residual_s"] = residual_ms / 1000
    return out

def summarize(rows):
    sums = {k: sum(r[k] for r in rows if r[k] is not None) for k in METRICS}
    return {
        "cells": len(rows), "timing_json_present": sum(r["native_s"] is not None for r in rows),
        "smt_timing_present": sum(r["smt_run_s"] is not None for r in rows),
        "returncodes": dict(collections.Counter(str(r["returncode"]) for r in rows)),
        "timeouts": sum(bool(r["timed_out"]) for r in rows), "sum": sums,
        "reported_frontend_fraction_of_native": (sums["rust_s"] + sums["vir_s"] + sums["air_excluding_smt_s"]) / sums["native_s"] if sums["native_s"] else None,
        "reported_smt_run_fraction_of_all_external": sums["smt_run_s"] / sums["external_s"],
        "reported_smt_all_fraction_of_all_external": (sums["smt_run_s"] + sums["smt_init_s"]) / sums["external_s"],
        "reported_smt_zero_cost_ratio": sums["external_s"] / (sums["external_s"] - sums["smt_init_s"] - sums["smt_run_s"]),
    }

def analyze(root, out):
    source = root / "artifacts/autoverus-native-2026-10-09/full/analysis/cells.json.gz"
    with gzip.open(source, "rt") as f:
        cells = json.load(f)
    rows = []
    for c in cells:
        row = {k: c[k] for k in ("candidate", "condition", "repetition", "context_key", "returncode", "timed_out")}
        row.update(partition(c))
        n = c.get("native_json") or {}
        v = n.get("verification-results", {})
        row["encountered_vir_error"] = v.get("encountered-vir-error")
        row["verified"] = v.get("verified")
        row["errors"] = v.get("errors")
        row["accepted_exit_zero"] = c["returncode"] == 0
        rows.append(row)
    expected = {(i, cond, rep) for i in range(3566) for cond in ("direct", "capture") for rep in range(3)}
    actual = {(r["candidate"], r["condition"], r["repetition"]) for r in rows}
    if len(rows) != len(actual) or actual != expected:
        raise ValueError("Retained matrix is not the expected complete 3566 x 2 x 3 point")
    out.mkdir(parents=True, exist_ok=True)
    with gzip.open(out / "candidate-timers.csv.gz", "wt", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    summary = {
        "source": str(source.relative_to(root)),
        "source_verus_revision": "33269ac6a0ea33a08109eefe5016c1fdd0ce9fbd",
        "timer_definition": "source/rust_verify/src/main.rs:176-303; air subtracts SMT; VIR children are nested",
        "limitations": [
            "Direct and capture are separate conditions; repetitions remain separate.",
            "Reported SMT run is host elapsed around SMT interaction, not pure Z3 CPU.",
            "Missing JSON and missing SMT fields remain unknown, not zero-time observations.",
            "Native milliseconds are rounded down; residual includes unreported work and timer quantization.",
            "Zero-cost ratio removes only reported SMT time from this replay denominator; not a global application bound.",
            "This is the historical single-CPU AutoVerus replay point, not current G10 or an LLM generation round.",
        ],
        "passes": {},
    }
    for cond in ("direct", "capture"):
        for rep in range(3):
            selected = [r for r in rows if r["condition"] == cond and r["repetition"] == rep]
            summary["passes"][f"{cond}-{rep}"] = summarize(selected)
            summary["passes"][f"{cond}-{rep}"]["accepted"] = summarize([r for r in selected if r["accepted_exit_zero"]])
            summary["passes"][f"{cond}-{rep}"]["nonaccepted"] = summarize([r for r in selected if not r["accepted_exit_zero"]])
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path("."))
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(analyze(args.root.resolve(), args.out.resolve())["passes"], indent=2))
