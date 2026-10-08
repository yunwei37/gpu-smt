#!/usr/bin/env python3
"""Analyze stock module CLI diagnostics, cumulative scopes and paired wall costs.

Cumulative categories are exclusive same-thread elapsed wall scopes and may
overlap across threads. Displayed values have three significant digits. Category
shares are descriptive accumulated-category shares, never CPU/wall partitions.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import statistics

CATEGORY = re.compile(r"^\t(.+?) ([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)(ms|s)$")
MODULES = ["Mathlib/" + name for name in (
    "Algebra/Group/Basic.lean", "Algebra/Polynomial/Basic.lean",
    "Data/Nat/Prime.lean", "LinearAlgebra/FiniteDimensional.lean",
    "Analysis/SpecialFunctions/Trigonometric/Basic.lean",
    "MeasureTheory/Integral/IntervalIntegral.lean")]


def parse_profile(raw):
    text = raw.decode("utf-8", errors="replace")
    issues = []
    if "\ufffd" in text:
        issues.append("stderr contains invalid UTF8; raw retained")
    blocks = []
    active = None
    for line_number, line in enumerate(text.splitlines(), 1):
        if line == "cumulative profiling times:":
            active = []
            blocks.append(active)
        elif active is not None and line.startswith("\t"):
            match = CATEGORY.fullmatch(line)
            if not match:
                issues.append(dict(line=line_number, raw_line=line, error="unparsed cumulative category"))
                continue
            name, display, unit = match.groups()
            active.append(dict(category=name, displayed_value=display, unit=unit,
                               seconds=float(display) / (1000 if unit == "ms" else 1),
                               raw_line=line, significant_digits="stock display precision3"))
        else:
            active = None
    if len(blocks) > 1:
        issues.append("multiple cumulative blocks; no combining or summing across blocks")
    for block in blocks:
        names = [row["category"] for row in block]
        if len(set(names)) != len(names):
            issues.append("duplicate category within native block; no fabricated merge")
    return dict(blocks=blocks, issues=issues)


def parse_diagnostics(raw):
    records, malformed = [], []
    for line_number, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line.decode("utf-8"))
            if not isinstance(record, dict):
                raise ValueError("diagnostic is not a JSON object")
            records.append(record)
            if "severity" in record and not isinstance(record["severity"], str):
                malformed.append(dict(line=line_number, raw_hex=line.hex(), error="diagnostic severity is not a string; original object retained"))
        except Exception as error:
            malformed.append(dict(line=line_number, raw_hex=line.hex(), error=repr(error)))
    return dict(records=records, malformed=malformed,
                severity_counts=dict(Counter(row["severity"] if isinstance(row.get("severity"), str)
                                             else "unclassified_json" for row in records)))


def parse_time(raw):
    fields = {}
    unparsed = []
    # GNU time -v, LC_ALL=C. Retain every original display string and line.
    for line in raw.decode("utf-8", errors="replace").splitlines():
        if ": " in line:
            key, display = line.strip().split(": ", 1)
            fields[key] = dict(display=display, raw_line=line)
        elif line.strip():
            unparsed.append(line)
    numeric = {}
    for key, label in (("User time (seconds)", "user_cpu_seconds"),
                       ("System time (seconds)", "system_cpu_seconds"),
                       ("Maximum resident set size (kbytes)", "maxrss_kbytes"),
                       ("Exit status", "exit_status")):
        if key in fields:
            try:
                numeric[label] = float(fields[key]["display"]) if "seconds" in key else int(fields[key]["display"])
            except ValueError:
                unparsed.append(fields[key]["raw_line"])
    return dict(fields=fields, numeric=numeric, unparsed_lines=unparsed,
                scope="GNU time CPU/maxRSS diagnostic of command tree; RSS is not PSS")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    events_raw = (args.input / "events.jsonl").read_bytes()
    events, issues = [], []
    for line_number, line in enumerate(events_raw.splitlines(), 1):
        try:
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError("event is not an object")
            events.append(record)
        except Exception as error:
            issues.append(dict(file="events.jsonl", line=line_number, error=repr(error)))
    runs = [e for e in events if e.get("event") == "run"]
    shutdowns = [e for e in events if e.get("event") == "shutdown"]
    if len(runs) != 1 or len(shutdowns) != 1:
        issues.append(dict(error="run/shutdown records incomplete", runs=len(runs), shutdowns=len(shutdowns)))
    run = runs[0] if runs else {}
    expected = run.get("cells", [])
    if [e.get("sequence") for e in events] != list(range(len(events))):
        issues.append(dict(error="event sequence incomplete or reordered"))
    repeats = run.get("repeats")
    if type(repeats) is int and repeats > 0:
        declared_order = [(r, module, mode) for r in range(1, repeats + 1)
                          for module in (MODULES[:1] if run.get("preflight") else MODULES)
                          for mode in (("normal", "profile") if r % 2 else ("profile", "normal"))]
        original_order = [dict(index=i, repeat=r, module=m, mode=v) for i, (r, m, v) in enumerate(declared_order)]
        if expected != original_order:
            issues.append(dict(error="declared cells differ from fixed original workload/order"))
    else:
        issues.append(dict(error="repeat count unavailable or invalid"))
    rows, by_pair = [], defaultdict(dict)
    for file in sorted(args.input.glob("cell-*/result.json")):
        try:
            result = json.loads(file.read_bytes())
            for name, info in result.get("files", {}).items():
                path = file.parent / name
                if not path.exists() or sha(path.read_bytes()) != info.get("sha256") or path.stat().st_size != info.get("bytes"):
                    issues.append(dict(file=str(path.relative_to(args.input)), error="raw hash/size mismatch"))
            stderr = (file.parent / "stderr.bin").read_bytes()
            stdout = (file.parent / "stdout.bin").read_bytes()
            time_raw = (file.parent / "time.txt").read_bytes() if (file.parent / "time.txt").exists() else b""
            profile, diagnostic, resources = parse_profile(stderr), parse_diagnostics(stdout), parse_time(time_raw)
            admission = []
            if diagnostic["severity_counts"].get("warning"):
                admission.append("native warnings present; preserved, not silently accepted as faithful proofs")
            if diagnostic["severity_counts"].get("unclassified_json"):
                admission.append("unclassified JSON diagnostics require inspection")
            if result.get("error") or result.get("status") != "exited" or result.get("returncode") != 0:
                outcome = "system_or_process_failure"
            elif diagnostic["malformed"]:
                outcome = "malformed_stdout"
            elif diagnostic["severity_counts"].get("error"):
                outcome = "native_errors"
            elif admission:
                outcome = "completed_with_admission_warnings"
            else:
                outcome = "completed_cli_no_reported_errors"
            if result.get("source", {}).get("sha256") != result.get("source_after", {}).get("sha256"):
                issues.append(dict(index=result.get("index"), error="source changed during invocation"))
            if result.get("mode") == "profile" and not profile["blocks"]:
                admission.append("no cumulative profile block; profile collection not established")
            if result.get("mode") == "normal" and profile["blocks"]:
                admission.append("normal path unexpectedly produced cumulative profile")
            if resources["numeric"].get("exit_status") != result.get("returncode"):
                admission.append("GNU time exit receipt absent or differs from process status")
            shares = []
            if len(profile["blocks"]) == 1 and not profile["issues"]:
                block = profile["blocks"][0]
                total = sum(row["seconds"] for row in block)
                if total > 0:
                    shares = [dict(category=row["category"], accumulated_category_share=row["seconds"] / total)
                              for row in block]
            row = dict(result=result, native_diagnostics=diagnostic, profile=profile, resources=resources,
                       outcome=outcome, admission_warnings=admission,
                       stdout_sha256=sha(stdout), stderr_sha256=sha(stderr),
                       descriptive_accumulated_category_shares=shares,
                       correctness="CLI diagnostics/status retained; profile totals do not certify correctness/no-sorry fidelity")
            rows.append(row)
            key = (result["module"], result["repeat"])
            if result["mode"] in by_pair[key]:
                issues.append(dict(module=key[0], repeat=key[1], error="duplicate paired mode result"))
            by_pair[key][result["mode"]] = row
        except Exception as error:
            issues.append(dict(file=str(file.relative_to(args.input)), error=repr(error)))
    result_events = [e for e in events if e.get("event") == "result"]
    normalized_events = Counter(json.dumps({k: v for k, v in e.items()
                                if k not in ("event", "sequence", "wall_ns", "monotonic_ns")}, sort_keys=True) for e in result_events)
    if normalized_events != Counter(json.dumps(row["result"], sort_keys=True) for row in rows):
        issues.append(dict(error="raw result files and event receipts differ"))
    expected_by_index = {e["index"]: e for e in expected}
    observed_indices = [r["result"]["index"] for r in rows]
    if len(set(observed_indices)) != len(observed_indices):
        issues.append(dict(error="duplicate result index"))
    for row in rows:
        result = row["result"]
        declared = expected_by_index.get(result["index"])
        if not declared or any(result.get(k) != declared.get(k) for k in ("module", "repeat", "mode")):
            issues.append(dict(index=result["index"], error="cell identity differs from declared source matrix"))
    for module, info in run.get("sources", {}).items():
        path = args.input / "sources" / module
        if not path.exists() or sha(path.read_bytes()) != info.get("sha256"):
            issues.append(dict(module=module, error="retained source snapshot mismatch"))
    missing = sorted(set(expected_by_index) - set(observed_indices))
    if shutdowns and (shutdowns[-1].get("terminal_indices") != observed_indices or shutdowns[-1].get("missing_indices") != missing):
        issues.append(dict(error="shutdown completeness differs from raw results"))
    pairs = []
    for (module, repeat), group in sorted(by_pair.items()):
        normal, profiled = group.get("normal"), group.get("profile")
        both = bool(normal and profiled)
        nw = normal["result"].get("invocation_wall_ns") if normal else None
        pw = profiled["result"].get("invocation_wall_ns") if profiled else None
        diagnostic_equal = bool(both and not normal["native_diagnostics"]["malformed"] and
                                not profiled["native_diagnostics"]["malformed"] and
                                normal["native_diagnostics"]["records"] == profiled["native_diagnostics"]["records"])
        pairs.append(dict(module=module, repeat=repeat, normal_index=normal["result"]["index"] if normal else None,
                          profile_index=profiled["result"]["index"] if profiled else None, paired_complete=both,
                          diagnostic_identity=diagnostic_equal,
                          stdout_bytes_identity=both and normal["stdout_sha256"] == profiled["stdout_sha256"],
                          returncode_identity=both and normal["result"].get("returncode") == profiled["result"].get("returncode"),
                          normal_wall_ns=nw, profile_wall_ns=pw,
                          profile_minus_normal_wall_ns=pw - nw if nw is not None and pw is not None else None,
                          profile_over_normal_wall_ratio=pw / nw if nw and pw is not None else None,
                          normal_outcome=normal["outcome"] if normal else "missing",
                          profile_outcome=profiled["outcome"] if profiled else "missing"))
    by_module = {}
    for module in dict.fromkeys(e.get("module") for e in expected):
        selected = [p for p in pairs if p["module"] == module]
        deltas = [p["profile_minus_normal_wall_ns"] for p in selected if p["profile_minus_normal_wall_ns"] is not None]
        by_module[module] = dict(pairs=selected, wall_delta_ns=dict(n=len(deltas), values=deltas,
                                  mean=statistics.mean(deltas) if deltas else None,
                                  median=statistics.median(deltas) if deltas else None,
                                  min=min(deltas) if deltas else None, max=max(deltas) if deltas else None))
    summary = dict(input=str(args.input.resolve()), events_sha256=sha(events_raw), run_provenance=run,
                   declared_cells=len(expected), retained_cells=len(rows), missing_indices=missing,
                   terminal_complete=bool(shutdowns) and not missing,
                   outcomes=dict(Counter(r["outcome"] for r in rows)), issues=issues, paired_by_module=by_module,
                   makespan_ns=shutdowns[-1]["monotonic_ns"] - run["monotonic_ns"] if shutdowns and runs else None,
                   interpretation="profile categories are rounded exclusive same-thread elapsed scopes, potentially overlapping across threads; shares are accumulated-category descriptions, not CPU/exact wall fractions; type checking includes addDecl/auxiliary declarations; import loads compiled dependencies, not transitive proof rechecking")
    args.out.mkdir(parents=True, exist_ok=False)
    with open(args.out / "cells.jsonl", "x") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    lines = ["# Stock module profile observations", "", summary["interpretation"], "",
             "| Module | Repeat | Normal wall (s) | Profile wall (s) | Delta (s) | Diagnostic identity |", "|---|---:|---:|---:|---:|---|"]
    for pair in pairs:
        seconds = lambda value: value / 1e9 if value is not None else None
        lines.append(f"| {pair['module']} | {pair['repeat']} | {seconds(pair['normal_wall_ns'])} | {seconds(pair['profile_wall_ns'])} | {seconds(pair['profile_minus_normal_wall_ns'])} | {pair['diagnostic_identity']} |")
    lines += ["", "| Module | Repeat | Cumulative category | Original display |", "|---|---:|---|---:|"]
    for row in rows:
        if row["result"]["mode"] == "profile":
            for block in row["profile"]["blocks"]:
                for category in block:
                    lines.append(f"| {row['result']['module']} | {row['result']['repeat']} | {category['category']} | {category['displayed_value']}{category['unit']} |")
    lines += ["", "Raw display units/values, unknown categories, CPU/maxRSS, all failures and diagnostics remain in `cells.jsonl`; counts, completeness, issues and paired repeated values are in `summary.json`. RSS is not PSS. No correctness, GPU readiness, Amdahl bound or service-speed claim follows from category totals."]
    (args.out / "tables.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
