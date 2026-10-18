"""Secondary analysis of closed E1080 observations; not a causal replay or GPU bound."""
from pathlib import Path
import collections
import gzip
import json
import math

A = Path(__file__).resolve().parent


def read_rows(path):
    good, bad = [], []
    with gzip.open(path, "rt") as stream:
        for line_no, line in enumerate(stream, 1):
            try:
                good.append(json.loads(line))
            except json.JSONDecodeError as exc:
                bad.append({"line": line_no, "error": str(exc)})
    return good, bad


def quantiles(values):
    xs = sorted(values)
    return {"n": len(xs), **{
        key: xs[max(0, math.ceil(q * len(xs)) - 1)]
        for key, q in [("p50", .5), ("p90", .9), ("p99", .99), ("max", 1)]
    }} if xs else {"n": 0}


def union_seconds(intervals):
    total, right = 0, None
    for left, end in sorted(intervals):
        assert end >= left
        if right is None or left > right:
            total += end - left
        else:
            total += max(0, end - right)
        right = max(end, right) if right is not None else end
    return total / 1e9


def main():
    result = json.loads((A / "full1000-result.json").read_text())
    assert result["state"] == "complete" and result["fidelity_qualified"]
    inputs = [json.loads(x) for x in (A.parents[2] / "input-top1000.jsonl").read_text().splitlines() if x.strip()]
    header = "import Mathlib\nimport Aesop\n"
    assert all(x["code"].startswith(header) for x in inputs)
    source_to_id = {"\n\n" + x["code"][len(header):]: x["proof_id"] for x in inputs}
    assert len(inputs) == len(source_to_id) == 1000
    native = result["conditions"]["native"]["source_service_seconds"]
    power = result["conditions"]["power"]["source_service_seconds"]
    current = {x["proof_id"] for x in result["observed_candidate_regressions"]["current_slower_sources"]}
    persistent = set(result["observed_candidate_regressions"]["prior_common_still_slower_IDs"])
    assert persistent <= current and set(native) == set(power) == set(source_to_id.values())
    assert current == {x for x in native if power[x] > native[x]}
    sources = {key: {
        "proof_id": key,
        "group": "persistent_regression" if key in persistent else "other_current_regression" if key in current else "current_non_regression",
        "native_service_seconds": native[key], "power_service_seconds": power[key],
        "service_difference_seconds": power[key] - native[key],
        "numeric_races": 0, "legacy_winners": collections.Counter(),
        "race_decision_seconds_sum_NOT_CPU": 0.0,
        "race_retirement_seconds_sum_NOT_CPU": 0.0,
        "reaped_numeric_child_CPU_seconds": 0.0,
        "cancelled_numeric_child_CPU_seconds": 0.0,
        "parsed_external_models": 0, "external_solver_reported_seconds_sum_NOT_CPU": 0.0,
        "external_model_intervals": [], "matrix_rows": [], "matrix_cols": [], "matrix_nnz": [],
    } for key in native}
    cell = A / "full1000/power"
    races, bad_races = read_rows(cell / "rep1-oracle-highs/lp-races.jsonl.gz")
    models, bad_models = read_rows(cell / "rep1-oracle-highs-backend/support-calls.jsonl.gz")
    seen_children, child_errors = set(), []
    for event in races:
        row = sources[source_to_id[event["source"]]]
        row["numeric_races"] += 1
        row["legacy_winners"][event["winner"]] += 1
        row["race_decision_seconds_sum_NOT_CPU"] += event["decision_ns"] / 1e9
        row["race_retirement_seconds_sum_NOT_CPU"] += event["retirement_ns"] / 1e9
        for role in ["cpu", "gpu", "strong_cpu"]:
            child = event.get(role + "_exit")
            if not isinstance(child, dict):
                continue
            assert child["pid"] not in seen_children
            seen_children.add(child["pid"])
            if child.get("kill_error") or child.get("wait_error"):
                child_errors.append({"call_id": event["call_id"], "role": role, "receipt": child})
            cpu = (child["wait4_user_cpu_ns"] + child["wait4_system_cpu_ns"]) / 1e9
            row["reaped_numeric_child_CPU_seconds"] += cpu
            if child["signal"] is not None:
                row["cancelled_numeric_child_CPU_seconds"] += cpu
    non_models = []
    for event in models:
        if not isinstance(event.get("rows"), int):
            non_models.append(event)
            continue
        row = sources[source_to_id[event["input"]["source"]]]
        row["parsed_external_models"] += 1
        row["external_model_intervals"].append((event["start_ns"], event["end_ns"]))
        row["external_solver_reported_seconds_sum_NOT_CPU"] += event["reply"].get("solver_seconds", 0)
        for name in ["rows", "cols", "nnz"]:
            row["matrix_" + name].append(event[name])
    groups = {}
    for name in ["persistent_regression", "other_current_regression", "current_non_regression"]:
        selected = [x for x in sources.values() if x["group"] == name]
        sums = ["native_service_seconds", "power_service_seconds", "service_difference_seconds",
                "numeric_races", "race_decision_seconds_sum_NOT_CPU", "race_retirement_seconds_sum_NOT_CPU",
                "reaped_numeric_child_CPU_seconds", "cancelled_numeric_child_CPU_seconds",
                "parsed_external_models", "external_solver_reported_seconds_sum_NOT_CPU"]
        winners = collections.Counter()
        for x in selected:
            winners.update(x["legacy_winners"])
        groups[name] = {"sources": len(selected),
                       "sources_without_recorded_race": sum(x["numeric_races"] == 0 for x in selected),
                       "sources_without_parsed_external_model": sum(x["parsed_external_models"] == 0 for x in selected),
                       **{k: sum(x[k] for x in selected) for k in sums},
                       "legacy_winners": dict(winners),
                       "external_interval_union_seconds_NOT_removable_wall":
                           union_seconds([t for x in selected for t in x["external_model_intervals"]]),
                       "external_shapes": {k: quantiles([v for x in selected for v in x["matrix_" + k]])
                                           for k in ["rows", "cols", "nnz"]}}
    for row in sources.values():
        row["external_model_interval_union_seconds_NOT_removable_wall"] = union_seconds(row.pop("external_model_intervals"))
        row["external_shapes"] = {name: quantiles(row.pop("matrix_" + name)) for name in ["rows", "cols", "nnz"]}
    out = {
        "scope": "All1000 closed E1080 sources including rejected. Groups are retrospective measured outcome strata, unsuitable for answer-aware routing or held-out prediction. Prior persistence uses different affinity/instrumentation. No current Lean stage/fallback diagnostics were captured; zero external records means unobserved/inapplicable, not zero Lean LP work. Numeric race winners are not successful Lean certificate checks. Legacy gpu winner denotes CPU HiGHS. Child CPU and overlapping elapsed/solver sums are distinct; neither is a removable full-wall fraction. Root self-review only.",
        "groups": groups,
        "data_quality": {"race_rows": len(races), "reaped_distinct_children": len(seen_children),
                         "race_parse_errors": bad_races, "external_parse_errors": bad_models,
                         "non_model_external_rows": len(non_models), "child_receipt_errors": child_errors},
        "per_source": sorted(sources.values(), key=lambda x: x["service_difference_seconds"], reverse=True),
    }
    (A / "regression-cost-analysis.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"groups": groups, "data_quality": out["data_quality"]}, indent=2))


if __name__ == "__main__":
    main()
