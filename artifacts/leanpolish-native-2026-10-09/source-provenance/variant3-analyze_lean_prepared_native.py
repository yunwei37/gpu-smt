#!/usr/bin/env python3
"""Recompute completion, complete-response parity and OS/resource summaries."""
import argparse
import collections
import json
from pathlib import Path
import re


def canonical(result):
    result = dict(result)
    # Fingerprint iteration order is not an observation; declaration identity
    # and each type/value hash are. Diagnostics remain strictly ordered.
    if "local_declaration_fingerprints" in result:
        result["local_declaration_fingerprints"] = sorted(result["local_declaration_fingerprints"], key=lambda d: d["name"])
    if "local_sorry_declarations" in result:
        result["local_sorry_declarations"] = sorted(result["local_sorry_declarations"])
    return result


def analyze(path, controls):
    jobs = [json.loads(x) for x in (path / "selected-jobs.jsonl").read_text().splitlines()]
    expected = {j["index"] for j in jobs}
    job_map = {j["index"]: j for j in jobs}
    cells, responses, preparations = [], {}, {}
    expected_cells = None
    config_file = path / "run-configuration.json"
    if config_file.exists():
        config = json.loads(config_file.read_text())
        expected_cells = {f"rep{rep}-{mode}-p{workers}" for rep in range(config["repetitions"])
                          for mode in config["modes"] for workers in config["workers"]}
    for cell in sorted(path.glob("rep*-*-p*")):
        match = re.fullmatch(r"rep(\d+)-(\w+)-p(\d+)", cell.name)
        if not match:
            continue
        rep, mode, workers = int(match[1]), match[2], int(match[3])
        receipt = json.loads((cell / "receipt.json").read_text())
        data = {int(p.stem): json.loads(p.read_text()) for p in (cell / "responses").glob("*.json")}
        responses[(rep, mode, workers)] = data
        prepared = {}
        for line in (cell / "stdout.bin").read_text(errors="replace").splitlines():
            try:
                record = json.loads(line)
                if "preparation" in record:
                    prepared[record["preparation"]] = record["result"]
            except json.JSONDecodeError:
                pass  # Entire original stdout is retained; no invented response.
        preparations[(rep, mode, workers)] = prepared
        fields = {}
        for line in (cell / "time.txt").read_text().splitlines():
            for label, key in (("User time (seconds)", "user_s"), ("System time (seconds)", "system_s"),
                               ("Maximum resident set size (kbytes)", "individual_maxrss_kib")):
                if label + ":" in line:
                    fields[key] = float(line.split(label + ":", 1)[1].strip())
        pss, thread_count = 0, 0
        for line in (cell / "resource-samples.jsonl").read_text().splitlines():
            sample = json.loads(line)
            pss = max(pss, sample["fleet_pss_kib"])
            thread_count = max(thread_count, sum(p["threads"] for p in sample["processes"]))
        outcomes = collections.Counter("exception" if "exception" in r["result"] else
                                       "accepted" if r["result"].get("accepted") else "rejected_or_incomplete"
                                       for r in data.values())
        groups = {}
        for index, record in data.items():
            job = job_map.get(index)
            if job is None:
                continue
            for group in (job["span_group"], "kind:" + job["syntax_kind"]):
                summary = groups.setdefault(group, {"responses": 0, "cache_hits": 0, "accepted": 0,
                                                     "exceptions": 0, "summed_service_ms": 0.0})
                summary["responses"] += 1
                summary["cache_hits"] += record["cached"]
                summary["accepted"] += bool(record["result"].get("accepted"))
                summary["exceptions"] += "exception" in record["result"]
                # At parallelism this sum overlaps and includes dispatch waiting;
                # it is neither CPU time nor an arrival-latency distribution.
                summary["summed_service_ms"] += (record["end_ns"] - record["start_ns"]) / 1e6
        cells.append({"cell": cell.name, "exitcode": receipt["exitcode"], "expected": len(expected),
                      "observed": len(data), "missing": sorted(expected - data.keys()),
                      "extra": sorted(data.keys() - expected), "wall_s": receipt["wall_ns"] / 1e9,
                      "throughput_jobs_s": len(data) / (receipt["wall_ns"] / 1e9),
                      "sampled_peak_fleet_pss_kib": pss, "sampled_max_live_threads": thread_count,
                      "cache_hits": sum(r["cached"] for r in data.values()), "outcomes": dict(outcomes),
                      "source_groups": groups, **fields})
    comparisons = []
    for rep, mode, workers in sorted(responses):
        if mode != "logical" or (rep, "fork", workers) not in responses:
            continue
        a, b = responses[(rep, mode, workers)], responses[(rep, "fork", workers)]
        common = expected & a.keys() & b.keys()
        differences = [i for i in sorted(common) if canonical(a[i]["result"]) != canonical(b[i]["result"])]
        comparisons.append({"rep": rep, "workers": workers, "paired": len(common),
                            "missing_pairs": sorted(expected - common), "different_indices": differences})
    control_results = []
    missing_control_receipts = []
    if controls:
        selected_controls = json.loads((controls / "selected-controls.json").read_text())
        missing_control_receipts = [c["id"] for c in selected_controls if not (controls / c["id"] / "receipt.json").exists()]
        for cell in sorted(controls.iterdir()):
            if not cell.is_dir():
                continue
            if not (cell / "receipt.json").exists():
                continue
            receipt = json.loads((cell / "receipt.json").read_text())
            diag, unparsed = [], []
            for line in (cell / "stdout.bin").read_text(errors="replace").splitlines():
                try:
                    diag.append(json.loads(line))
                except json.JSONDecodeError:
                    unparsed.append(line)
            # Lean's stock CLI uses Message.toJson, also used by the adapter.
            # Same source-relative filename/cwd: no text/position normalization.
            for key, rs in responses.items():
                result = (preparations[key].get(receipt["base"]) if receipt["kind"] == "original"
                          else rs.get(receipt["index"], {}).get("result"))
                if result is None:
                    continue
                control_results.append({"control": cell.name, "cell": f"rep{key[0]}-{key[1]}-p{key[2]}",
                                        "stock_exitcode": receipt["exitcode"], "unparsed_stdout": unparsed,
                                        "diagnostics_equal": result.get("diagnostics") == diag,
                                        "native_has_errors": result.get("has_errors"),
                                        "stock_has_errors": any(d.get("severity") == "error" for d in diag),
                                        "native_accepted": result.get("accepted")})
    observed_cells = {c["cell"] for c in cells}
    return {"cells": cells, "comparisons": comparisons, "stock_controls": control_results,
            "missing_expected_cells": sorted(expected_cells - observed_cells) if expected_cells is not None else None,
            "missing_control_receipts": missing_control_receipts}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True)
    ap.add_argument("--controls", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    summary = analyze(args.run, args.controls)
    args.out.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"cells": len(summary["cells"]), "paired": sum(x["paired"] for x in summary["comparisons"]),
                      "different": sum(len(x["different_indices"]) for x in summary["comparisons"]),
                      "missing": sum(len(x["missing_pairs"]) for x in summary["comparisons"]),
                      "stock_controls": len(summary["stock_controls"])}, indent=2))


if __name__ == "__main__":
    main()
