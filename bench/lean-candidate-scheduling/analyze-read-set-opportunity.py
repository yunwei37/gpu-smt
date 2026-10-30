"""Offline read-set opportunity audit; source projections are not actual read traces."""
import argparse
import collections
import gzip
import json
from pathlib import Path
import re
import runpy

ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT / "artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z"

def read(path):
    with gzip.open(path, "rt") as f:
        return json.load(f)

def analyze(out):
    candidates = {x["id"]: x for x in read(PAIR / "input7808.json.gz")["candidates"]}
    results = read(PAIR / "engine.stdout.gz")["results"]
    by_result = {x["id"]: x for x in results}
    assert len(candidates) == len(by_result) == 7808
    groups = collections.defaultdict(list)
    for sid, c in candidates.items():
        groups[c["task_id"]].append(sid)
    costs = {sid: sum(a["elapsed_seconds"] for a in x["attempts"]) for sid, x in by_result.items()}
    unsolved = [task for task, ids in groups.items()
                if not any(by_result[s]["outcome"]["status"] == "accepted" for s in ids)]
    top = sorted(unsolved, key=lambda task: -sum(costs[s] for s in groups[task]))[:3]
    selected = {sid for task in top for sid in groups[task]}
    assert len(selected) == 96
    syntax = {}
    with gzip.open(ROOT / "artifacts/linarith-oracle-2026-10-17/prefix-opportunity/native-units.jsonl.gz", "rt") as f:
        for line in f:
            x = json.loads(line)
            if x["proposalId"] in selected:
                syntax[x["proposalId"]] = x
    profile = {x["source_id"]: x for x in json.loads(
        (ROOT / "artifacts/lean-failure-profile-2026-10-25/full480-analysis/per-source.json").read_text())}
    strip = runpy.run_path(str(ROOT / "bench/lean-candidate-scheduling/analyze.py"))["strip_comments"]
    # Narrow unchanged source projection from the native parser. This is deliberately
    # not a Lean Expr encoder, dynamic read-set recorder or production cache key.
    templates = collections.defaultdict(list)
    rows = []
    for task in top:
        for sid in groups[task]:
            x = by_result[sid]
            units = syntax.get(sid, {}).get("units", [])
            projection = None
            if task == "amc12a_2020_p4" and len(units) == 3:
                h, rw, close = units
                m = re.fullmatch(r"\s*have(?:\s+([^\s:]+))?\s*:\s*S\s*=\s*(.*?)\s*:=\s*by\b.*",
                                 strip(h["text"]), re.S)
                if (m and h["syntaxKind"].endswith(".tacticHave_")
                        and rw["syntaxKind"].endswith(".rwSeq")
                        and strip(rw["text"]).strip() == "rw [" + (m.group(1) or "this") + "]"
                        and close["syntaxKind"].endswith(".tacticRfl")
                        and strip(close["text"]).strip() == "rfl"):
                    expression = " ".join(m.group(2).split())
                    projection = "(" + expression + ").card = 100"
                    templates[(task, projection, "rfl")].append(sid)
            old = profile.get(sid, {})
            components = old.get("components", {})
            family_seconds = collections.Counter()
            for name, entry in components.items():
                low = name.lower()
                family = ("rfl_eqrefl" if name.startswith("tactic execution|") and
                          ("rfl" in low or "eqrefl" in low) else
                          "interval_cases" if name.startswith("tactic execution|") and "intervalcases" in low else
                          "simp_all" if name.startswith("tactic execution|") and "simpall" in low else
                          "other")
                family_seconds[family] += entry["exclusive_cpu_ns"] / 1e9
            rows.append({
                "id": sid, "task": task, "final_status": x["outcome"]["status"],
                "current_composed_attempt_seconds": costs[sid],
                "native_syntax_present": sid in syntax,
                "native_syntax_eligible": syntax.get(sid, {}).get("eligible"),
                "outer_units": units, "source_target_projection": projection,
                "historical_profile_present": sid in profile,
                "historical_profile_exclusive_cpu_seconds": old.get("measured_exclusive_cpu_seconds"),
                "historical_profile_family_exclusive_cpu_seconds": dict(family_seconds),
                "actual_dynamic_read_set": None, "negative_lookups_recorded": False,
                "elaborated_closed_target": None,
                "remaining_native_heartbeat_budget": None,
                "completed_ordinary_failure_producer": None,
            })
    rows_by = {x["id"]: x for x in rows}
    opportunities = []
    for key, ids in templates.items():
        if len(ids) < 2:
            continue
        # No native call-completion order is available in this source census.
        # Show every possible choice of first producer, rather than invent one.
        budgets = []
        for first in ids:
            later = [s for s in ids if s != first]
            budgets.append({
                "assumed_first_producer": first, "later_source_ids": later,
                "later_whole_candidate_attempt_envelope_seconds": sum(costs[s] for s in later),
                "later_historical_rfl_family_cpu_envelope_seconds": sum(
                    rows_by[s]["historical_profile_family_exclusive_cpu_seconds"].get("rfl_eqrefl", 0) for s in later),
                "later_current_final_statuses": dict(collections.Counter(
                    by_result[s]["outcome"]["status"] for s in later)),
            })
        opportunities.append({
            "source_projection": key, "sources": ids,
            "conditional_collapsible_calls": len(ids) - 1,
            "first_producer_scenarios": budgets,
            "qualified_replay_hits": None, "qualified_saved_seconds": None,
        })
    total = sum(costs.values())
    task_rows = []
    for task in top:
        ids = groups[task]
        task_rows.append({
            "task": task, "candidates": len(ids),
            "composed_attempt_seconds": sum(costs[s] for s in ids),
            "fraction_all_composed_attempt_work": sum(costs[s] for s in ids) / total,
            "final_statuses": dict(collections.Counter(by_result[s]["outcome"]["status"] for s in ids)),
            "native_syntax_sources": sum(s in syntax for s in ids),
            "historical_profile_sources": sum(s in profile for s in ids),
            "source_projection_sources": sum(rows_by[s]["source_target_projection"] is not None for s in ids),
        })
    result = {
        "point": "retained four-worker engine; same input7808, composed physical-attempt seconds",
        "total_composed_attempt_seconds": total, "top_unsolved_tasks": task_rows,
        "top_three_composed_attempt_fraction": sum(x["composed_attempt_seconds"] for x in task_rows) / total,
        "sources": rows, "source_projection_groups": opportunities,
        "actual_read_set_coverage": 0, "qualified_ordinary_failure_replay_hits": None,
        "qualified_saved_seconds": None, "native_invocations": 0,
        "interpretation": [
            "No actual read sets were retained for these calls; zero trace coverage is not zero opportunity.",
            "Native Syntax identifies source calls, not reached calls, post-rewrite Lean Expr targets or reads.",
            "Closed targets do not establish absence of local-instance, metavariable, environment-extension or negative-lookup dependencies.",
            "Whole candidate attempts include all their work and resource retries, not just the projected call.",
            "Historical profiler CPU is a separate run; rfl family totals may include earlier/internal calls.",
            "Resource-exhausted/timeout attempts are not completed ordinary-failure cache producers.",
            "No guaranteed RSS-failure monotonicity follows from a semantic read-set key.",
            "No source-feature prediction, new native collection or production cache is enabled.",
        ],
    }
    out.mkdir(parents=True, exist_ok=False)
    (out / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    result = analyze(args.out)
    print(json.dumps({k: v for k, v in result.items() if k not in ("sources",)}, ensure_ascii=False, indent=2))
