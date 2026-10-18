"""Read closed Kimina HTTP cells; distinguish body-wall and outer-attempt spans.
The server body timer runs from REPL stdin write/drain through stdout reply.
It includes native GC/IPC and is not tactic CPU or full candidate retirement.
"""
import argparse
import collections
import gzip
import json
import math
from pathlib import Path


def rows(path):
    if not path.exists() and path.with_name(path.name + ".gz").exists():
        path = path.with_name(path.name + ".gz")
    with (gzip.open(path, "rt") if path.suffix == ".gz" else path.open()) as stream:
        return [json.loads(line) for line in stream if line.strip()]


def quantiles(values):
    ordered = sorted(values)
    return {"n": len(ordered), **{
        name: ordered[max(0, math.ceil(q * len(ordered)) - 1)]
        for name, q in [("p50", .5), ("p90", .9), ("p99", .99), ("max", 1)]
    }} if ordered else {"n": 0}


def intervals_summary(intervals):
    events = []
    for begin, end in intervals:
        assert end >= begin
        events.extend([(begin, 1), (end, -1)])
    active = peak = occupied = weighted = 0
    previous = None
    # At a shared timestamp, departures precede arrivals.
    for stamp, delta in sorted(events):
        if previous is not None:
            weighted += (stamp - previous) * active
            if active:
                occupied += stamp - previous
        active += delta
        peak = max(peak, active)
        previous = stamp
    assert active == 0
    return {
        "occupied_seconds": occupied / 1e9,
        "integrated_attempt_seconds": weighted / 1e9,
        "max_completed_attempt_overlap": peak,
    }


def numeric_engagement(directory):
    race_path = directory / "lp-races.jsonl"
    if not race_path.exists():
        return {"scope": "No numerical race file; unobserved native/small LP work is not zero."}
    race_rows = rows(race_path)
    model_rows = rows(directory / "support-calls.jsonl.gz")
    parsed = [x for x in model_rows if isinstance(x.get("rows"), int)]
    children, seen, errors = [], set(), []
    for event in race_rows:
        for role in ["cpu", "gpu", "strong_cpu"]:
            receipt = event.get(role + "_exit")
            if not isinstance(receipt, dict):
                continue
            assert receipt["pid"] not in seen
            seen.add(receipt["pid"])
            children.append(receipt)
            if receipt.get("wait_error") or receipt.get("kill_error"):
                errors.append({"role": role, "receipt": receipt})
    return {
        "numeric_races": len(race_rows),
        "legacy_winners": dict(collections.Counter(x["winner"] for x in race_rows)),
        "parsed_external_models": len(parsed),
        "non_model_external_rows": len(model_rows) - len(parsed),
        "distinct_reaped_numeric_children": len(children),
        "wait_or_kill_errors": errors,
        "external_matrix_shapes": {key: quantiles([x[key] for x in parsed]) for key in ["rows", "cols", "nnz"]},
        "completed_external_solver_reported_seconds_NOT_CPU":
            sum(x.get("reply", {}).get("solver_seconds", 0) for x in parsed),
        "scope": "Legacy gpu means CPU HiGHS. Numeric winners are not confirmed Lean reconstruction hits. Completed models exclude cancelled/native/small paths; no pure all-LP fraction or GPU/Amdahl bound.",
    }


def analyze_cell(directory, expected_ids):
    terminal = json.loads((directory / "terminal.json").read_text())
    if terminal["state"] != "complete":
        return {"terminal": terminal, "scope": "No completed-cell latency attribution."}
    outcomes = rows(directory / "results.jsonl")
    assert [x["proof_id"] for x in outcomes] == expected_ids
    by_id = {x["proof_id"]: x for x in outcomes}
    events = rows(directory / "http.jsonl")
    requested = collections.Counter()
    attempts = []
    final_matches = collections.Counter()
    for event in events:
        request = json.loads(event["body"] if event["event"] == "request" else event["request"])
        assert len(request["snippets"]) == 1
        ident = request["snippets"][0]["id"]
        if ident.startswith("warm-"):
            continue
        assert ident in by_id
        if event["event"] == "request":
            requested[ident] += 1
            continue
        assert event["event"] == "response"
        body_seconds = None
        returned = json.loads(event["body"]) if event["status"] == 200 else {}
        result = next((x for x in returned.get("results", []) if x.get("id") == ident), None)
        is_final = False
        if result is not None:
            body_seconds = result.get("time")
            final = by_id[ident]["result"]
            is_final = all(result.get(k) == final.get(k) for k in ["id", "time", "response"])
            if is_final:
                final_matches[ident] += 1
        elapsed = (event["end_ns"] - event["start_ns"]) / 1e9
        attempts.append({
            "proof_id": ident, "HTTP_status": event["status"],
            "start_ns": event["start_ns"], "end_ns": event["end_ns"],
            "HTTP_attempt_seconds": elapsed, "reported_body_seconds": body_seconds,
            "outside_body_seconds": elapsed - body_seconds if body_seconds is not None else None,
            "matches_final_SDK_result": is_final,
        })
    matched = [x for x in attempts if x["matches_final_SDK_result"]]
    # More than one equal reply could be a real retry; retain it rather than
    # interpreting duplicate matching records as extra candidates.
    one_final_per_id = all(final_matches[key] == 1 for key in expected_ids)
    returned_counts = collections.Counter(x["proof_id"] for x in attempts)
    unanswered = dict(requested - returned_counts)
    intervals = [(x["start_ns"], x["end_ns"]) for x in attempts]
    summary = intervals_summary(intervals)
    envelope = (max(x[1] for x in intervals) - min(x[0] for x in intervals)) / 1e9
    per_source = sorted([{
        "proof_id": row["proof_id"], "status": row["status"],
        "reported_body_seconds": row["result"]["time"],
    } for row in outcomes], key=lambda x: x["reported_body_seconds"], reverse=True)
    tails = {}
    for label, fraction in [("slowest_1_percent", .01), ("slowest_10_percent", .1)]:
        subset = per_source[:math.ceil(len(per_source) * fraction)]
        tails[label] = {
            "sources": subset,
            "body_seconds_sum_NOT_whole_wall": sum(x["reported_body_seconds"] for x in subset),
        }
    extras = [x["outside_body_seconds"] for x in matched if x["outside_body_seconds"] is not None]
    return {
        "terminal": terminal,
        "numeric_engagement": numeric_engagement(directory),
        "source_count": len(outcomes),
        "recorded_requests": sum(requested.values()), "completed_HTTP_attempts": len(attempts),
        "exactly_one_recorded_request_per_source": all(requested[key] == 1 for key in expected_ids),
        "unanswered_recorded_requests": unanswered,
        "non_200_attempts": [x for x in attempts if x["HTTP_status"] != 200],
        "exactly_one_matching_final_attempt_per_source": one_final_per_id,
        "HTTP_interval_accounting": summary,
        "HTTP_envelope_seconds": envelope,
        "warm_clock_minus_HTTP_envelope_seconds": terminal["warm_verify_seconds"] - envelope,
        "SDK_body_seconds_sum_NOT_CPU_or_whole_wall": sum(x["reported_body_seconds"] for x in per_source),
        "SDK_body_seconds": quantiles([x["reported_body_seconds"] for x in per_source]),
        "HTTP_attempt_seconds": quantiles([x["HTTP_attempt_seconds"] for x in attempts]),
        "matched_attempt_outside_body_seconds": quantiles(extras),
        "matched_attempt_outside_body_seconds_sum_NOT_removable_wall": sum(extras),
        "own_body_ranked_tails": tails,
        "per_source": per_source, "completed_attempts": attempts,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    ids = json.loads((args.root / "source-ids.json").read_text())
    assert len(ids) == len(set(ids))
    out = {
        "scope": "Closed-cell HTTP attempts versus reported native body wall. No tactic CPU, pure LP fraction, zero-cost Amdahl ceiling, exact body positioning, full-matrix completion or independent audit is inferred. Retry/failed network attempts can be censored. Body timers include requested native GC and IPC; complete lifecycle additionally joins retirement.",
        "source": "Kimina fb2393de server/repl.py send and server/routers/check.py run_checks",
        "conditions": {}, "unfinished_cells": [],
    }
    for directory in sorted(args.root.glob("rep*-*")):
        if not directory.is_dir():
            continue
        if not (directory / "terminal.json").exists():
            out["unfinished_cells"].append(directory.name)
            continue
        out["conditions"][directory.name] = analyze_cell(directory, ids)
    out["matched_native_ranked_tails"] = {}
    for name, native in out["conditions"].items():
        if not name.endswith("-native") or "per_source" not in native:
            continue
        power_name = name[:-len("native")] + "power"
        power = out["conditions"].get(power_name)
        if not power or "per_source" not in power:
            continue
        power_rows = {x["proof_id"]: x for x in power["per_source"]}
        assert set(power_rows) == {x["proof_id"] for x in native["per_source"]}
        tails = {}
        for label, fraction in [("slowest_1_percent", .01), ("slowest_10_percent", .1)]:
            subset = native["per_source"][:math.ceil(len(native["per_source"]) * fraction)]
            tails[label] = {
                "sources": [{
                    "proof_id": x["proof_id"], "native_body_seconds": x["reported_body_seconds"],
                    "power_body_seconds": power_rows[x["proof_id"]]["reported_body_seconds"],
                } for x in subset],
                "native_body_seconds_sum_NOT_whole_wall": sum(x["reported_body_seconds"] for x in subset),
                "power_body_seconds_sum_NOT_whole_wall": sum(power_rows[x["proof_id"]]["reported_body_seconds"] for x in subset),
            }
        out["matched_native_ranked_tails"][name] = {
            "power_cell": power_name, "tails": tails,
            "sources_with_longer_power_body": sum(power_rows[x["proof_id"]]["reported_body_seconds"] > x["reported_body_seconds"] for x in native["per_source"]),
            "scope": "Retrospective diagnostic strata on all sources; no source exclusion, future routing or removable whole-wall fraction.",
        }
    (args.root / "http-boundary-analysis.json").write_text(json.dumps(out, indent=2) + "\n")
    for name, cell in out["conditions"].items():
        print(json.dumps({
            "cell": name, "sources": cell.get("source_count"),
            "warm": cell["terminal"].get("warm_verify_seconds"),
            "body_sum": cell.get("SDK_body_seconds_sum_NOT_CPU_or_whole_wall"),
            "outer_attempt_sum": cell.get("matched_attempt_outside_body_seconds_sum_NOT_removable_wall"),
            "unanswered": cell.get("unanswered_recorded_requests"),
        }))


if __name__ == "__main__":
    main()
