"""Analyze closed official-service cells without replacing incomplete populations."""
import argparse
import collections
import csv
import gzip
import json
import math
from pathlib import Path
import runpy

O = Path(__file__).resolve().parent
R = O.parents[2]
H = runpy.run_path(str(O.parent / "shred-closing/analyze-http.py"))
GIB = 1024 ** 3

def rows(path):
    """Prefer closed plain data; tolerate its simultaneous lossless archival."""
    try:
        stream = path.open("rt")
    except FileNotFoundError:
        try:
            stream = gzip.open(path.with_name(path.name + ".gz"), "rt")
        except FileNotFoundError:
            return
    with stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)

def native_outcome(row):
    if row["status"] == "resource_failure":
        return "resource_failure"
    if row["status"] == "timeout_error":
        return "timeout"
    return H["verification_outcome"](row)

def distribution(values):
    values = sorted(values)
    out = {"observed": len(values)}
    for name, q in [("p50", .5), ("p90", .9), ("p99", .99), ("max", 1)]:
        if not values:
            out[name] = None
            continue
        position = (len(values) - 1) * q
        lo, hi = math.floor(position), math.ceil(position)
        out[name] = values[lo] * (hi - position) + values[hi] * (position - lo) if hi != lo else values[lo]
    return out

def without_none(value):
    if isinstance(value, dict):
        return {k: without_none(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [without_none(v) for v in value]
    return value

def resource_accounting(directory, terminal, ids):
    summary = terminal.get("memory_watchdog", {})
    expected_threshold = summary.get("effective_threshold_bytes", 48 * GIB)
    count = peak = max_native = excess = 0
    previous = None
    gap = 0
    limits = set()
    kills = []
    for row in rows(directory / "memory-rss.jsonl"):
        count += 1
        peak = max(peak, row["total_rss_bytes"])
        max_native = max(max_native, row["native_repl_count"])
        excess += int(row["total_rss_bytes"] > row["effective_threshold_bytes"])
        assert row["budget_bytes"] == 48 * GIB and row["effective_threshold_bytes"] == expected_threshold
        if previous is not None:
            assert row["time_ns"] >= previous
            gap = max(gap, (row["time_ns"] - previous) / 1e9)
        previous = row["time_ns"]
        natives = [p for p in row["processes"] if p["native_repl"]]
        for proc in natives:
            limits.update(proc.get("address_limit", []))
        if "kill" in row:
            notice = row["kill"]
            kills.append(dict(notice, observed_largest_native=bool(natives) and
                notice["victim_rss_bytes"] == max(p["rss"] for p in natives),
                attributed_to_original_source=notice.get("source_id") in ids))
    summary = terminal.get("memory_watchdog", {})
    if summary:
        assert count == summary["samples"] and peak == summary["peak_sampled_owned_rss_bytes"]
        assert max_native == summary["peak_sampled_native_repl_count"] and len(kills) == summary["kills"]
    return dict(samples=count, peak_sampled_owned_RSS_bytes=peak if count else None,
        maximum_live_native_REPLs=max_native if count else None,
        effective_threshold_bytes=expected_threshold,
        fault_injection=terminal.get("fault_injection", False),
        maximum_sample_gap_seconds=gap if count > 1 else None,
        actual_native_address_limit_lines=sorted(limits), over_threshold_samples=excess,
        watchdog_kills=kills, monitor_error=summary.get("error"),
        source_attribution_issues=[k for k in kills if not k["attributed_to_original_source"]],
        scope="Conservative sum of owned process RSS, sampled non-atomically. Not kernel-hard RSS enforcement or PSS; overshoot remains visible.")

def http_accounting(directory, ids, data):
    pending = {}
    requests = collections.Counter()
    statuses = collections.Counter()
    starts = {}
    ends = {}
    attempt_sums = collections.Counter()
    returned = {}
    maximum = 0
    for event in rows(directory / "http.jsonl"):
        if event["event"] == "request":
            ident = json.loads(event["body"])["snippets"][0]["id"]
            assert event["start_ns"] not in pending
            pending[event["start_ns"]] = ident
            requests[ident] += 1
            starts[ident] = min(starts.get(ident, event["start_ns"]), event["start_ns"])
            maximum = max(maximum, len(pending))
            continue
        assert event["event"] == "response"
        ident = pending.pop(event["start_ns"])
        assert ident == json.loads(event["request"])["snippets"][0]["id"]
        statuses[str(event["status"])] += 1
        ends[ident] = max(ends.get(ident, event["end_ns"]), event["end_ns"])
        attempt_sums[ident] += (event["end_ns"] - event["start_ns"]) / 1e9
        if event["status"] == 200:
            body = json.loads(event["body"])
            if isinstance(body.get("results"), list):
                returned[ident] = body["results"]
    unanswered = set(pending.values())
    spans = {i: (ends[i] - starts[i]) / 1e9 for i in ids
             if i in starts and i in ends and i not in unanswered}
    wire_differences = []
    for ident, row in data.items():
        if ident in returned:
            replies = returned[ident]
            if len(replies) != 1 or without_none(replies[0]) != without_none(row["result"]):
                wire_differences.append(ident)
    summary = dict(recorded_HTTP_statuses=dict(statuses), maximum_open_trace_requests=maximum,
        maximum_inflight_HTTP_requests=maximum if not pending else None,
        real_source_attempts=sum(requests[i] for i in ids),
        warm_attempts=sum(v for i, v in requests.items() if i.startswith("warm-")),
        missing_request_IDs=[i for i in ids if not requests[i]],
        unanswered_request_IDs=sorted(unanswered),
        retry_IDs={i: requests[i] for i in ids if requests[i] > 1},
        HTTP_envelope_censored_IDs=[i for i in ids if i not in spans],
        final_HTTP200_payload_mismatch_IDs=wire_differences,
        SDK_results_without_recorded_HTTP200_payload_IDs=[i for i in ids if i not in returned],
        HTTP_source_envelope_seconds=distribution(spans.values()),
        scope="First recorded HTTP request to final recorded response for each source, including inter-attempt retry gaps. Excludes SDK waiting before the first request and final process retirement; whole clocks include them. Missing network response ends stay censored. Concurrent source spans overlap, not CPU/removable wall or Amdahl.")
    return summary, spans, requests, attempt_sums

def closed_cell(directory, expected):
    path = directory / "terminal.json"
    if not path.exists():
        return dict(observation="not_terminal"), None, None
    terminal = json.loads(path.read_text())
    out = dict(observation=terminal["state"], terminal=terminal)
    if terminal["state"] != "complete":
        return out, None, None
    assert terminal["affinity"] == [8, 9, 10, 11] and terminal["lean_version"] == "v4.27.0"
    assert terminal["source_concurrency"] == terminal["maximum_live_native_repls"] == 2
    assert terminal["per_native_repl_address_limit_bytes"] == 24 * GIB
    assert terminal["aggregate_memory_budget_bytes"] == 48 * GIB
    assert terminal["memory_watchdog"]["effective_threshold_bytes"] == 48 * GIB
    assert not terminal["owned_live_descendants_after_shutdown"]
    data_rows = list(rows(directory / "results.jsonl"))
    assert [x["proof_id"] for x in data_rows] == expected
    assert len(data_rows) == terminal["expected"] == terminal["returned"]
    assert dict(collections.Counter(x["status"] for x in data_rows)) == terminal["counts"]
    data = {x["proof_id"]: x for x in data_rows}
    assert len(data) == len(expected)
    out["native_outcomes"] = dict(collections.Counter(native_outcome(x) for x in data_rows))
    out["missing_native_response_IDs"] = [i for i, x in data.items()
        if not isinstance(x["result"].get("response"), dict) and
        x["status"] in ("valid", "lean_error", "sorry")]
    out["resource_accounting"] = resource_accounting(directory, terminal, set(expected))
    http, spans, attempts, sums = http_accounting(directory, expected, data)
    exits = list(rows(directory / "process-exits.jsonl"))
    out["observed_native_EOF_exits"] = dict(records=len(exits),
        returncodes=dict(collections.Counter(str(x["returncode"]) for x in exits)),
        bad_alloc_stderr_records=sum("std::bad_alloc" in x.get("stderr", "") for x in exits),
        scope="Observed no-response EOF diagnostics only, not exhaustive normal/cancelled descendant exit accounting.")
    out["HTTP"] = http
    out["HTTP_attempts"] = dict(attempts)
    out["HTTP_attempt_sums_seconds"] = dict(sums)
    return out, data, spans

def analyze(stage):
    directory = O / stage
    full = list(rows(R / "artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl"))
    assert len(full) == len({x["proof_id"] for x in full}) == 29750
    expected_rows = list(rows(O.parent / "input-top1000.jsonl"))[:24] if stage == "preflight" else full
    expected = [x["proof_id"] for x in expected_rows]
    by_id = {x["proof_id"]: x for x in full}
    assert all(x["code"] == by_id[x["proof_id"]]["code"] for x in expected_rows)
    assert json.loads((directory / "source-ids.json").read_text()) == expected
    repetitions = 1 if stage == "preflight" else 3
    tall_fields = ["cell", "proof_id", "native_outcome", "recorded_status", "SDK_status",
                   "HTTP_source_envelope_seconds", "HTTP_attempts"]
    tall_stream = (O / (stage + "-closed-source-latencies.csv")).open("w", newline="")
    tall_writer = csv.DictWriter(tall_stream, fieldnames=tall_fields, lineterminator="\n")
    tall_writer.writeheader()
    output = dict(scope="Closed original-source arithmetic HTTP comparison at source2/live2/native24GiB/aggregate48GiB/fourCPU8-11. Root self-review; no GPU, independent audit or OSDI acceptance.", stage=stage,
        expected_sources_per_cell=len(expected), expected_cells=2 * repetitions,
        conditions={}, pairs={}, all_planned_cells_terminal_complete=False)
    csv_path = O / (stage + "-paired-sources.csv")
    fields = ["pair", "proof_id", "native_outcome", "power_outcome", "native_status", "power_status",
              "native_HTTP_envelope_seconds", "power_HTTP_envelope_seconds",
              "native_HTTP_attempts", "power_HTTP_attempts"]
    with csv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for rep in range(1, repetitions + 1):
            cells = {}
            data = {}
            spans = {}
            for method in ("native", "power"):
                label = "rep" + str(rep) + "-" + method
                cell, values, observed = closed_cell(directory / label, expected)
                output["conditions"][label] = cell
                cells[method], data[method], spans[method] = cell, values, observed
                if values is not None:
                    for ident in expected:
                        row = values[ident]
                        tall_writer.writerow(dict(cell=label, proof_id=ident,
                            native_outcome=native_outcome(row), recorded_status=row["status"],
                            SDK_status=row.get("sdk_status", row["status"]),
                            HTTP_source_envelope_seconds=observed.get(ident),
                            HTTP_attempts=cell["HTTP_attempts"].get(ident, 0)))
            if any(data[m] is None for m in data):
                continue
            t = {m: cells[m]["terminal"] for m in cells}
            comparison = dict(order=["native", "power"] if rep % 2 else ["power", "native"],
                whole_native_over_power_observed=t["native"]["whole_lifecycle_seconds"] / t["power"]["whole_lifecycle_seconds"],
                warm_native_over_power_observed=t["native"]["warm_verify_seconds"] / t["power"]["warm_verify_seconds"],
                native_outcome_differences=[], recorded_status_differences=[], SDK_status_differences=[],
                SDK_error_text_difference_IDs=[], non_timing_result_difference_IDs=[],
                non_message_differences=[],
                raw_response_difference_IDs=[], matched_native_ranked_HTTP_tails={},
                scope="Observed complete-pair clocks; changed outcomes or resources are reported, never silently certified as a transparent speedup.")
            for ident in expected:
                native, power = data["native"][ident], data["power"][ident]
                if native_outcome(native) != native_outcome(power):
                    comparison["native_outcome_differences"].append(dict(proof_id=ident,
                        native=native_outcome(native), power=native_outcome(power)))
                if native["status"] != power["status"]:
                    comparison["recorded_status_differences"].append(dict(proof_id=ident, native=native["status"], power=power["status"]))
                if native.get("sdk_status", native["status"]) != power.get("sdk_status", power["status"]):
                    comparison["SDK_status_differences"].append(dict(proof_id=ident,
                        native=native.get("sdk_status", native["status"]), power=power.get("sdk_status", power["status"])))
                if native["result"].get("error") != power["result"].get("error"):
                    comparison["SDK_error_text_difference_IDs"].append(ident)
                if {k:v for k,v in native["result"].items() if k != "time"} != {k:v for k,v in power["result"].items() if k != "time"}:
                    comparison["non_timing_result_difference_IDs"].append(ident)
                before, after = native["result"].get("response", {}), power["result"].get("response", {})
                fields_changed = [k for k in set(before) | set(after) if k != "messages" and before.get(k) != after.get(k)]
                if fields_changed:
                    comparison["non_message_differences"].append(dict(proof_id=ident, fields=sorted(fields_changed)))
                if before != after:
                    comparison["raw_response_difference_IDs"].append(ident)
                writer.writerow(dict(pair=rep, proof_id=ident, native_outcome=native_outcome(native),
                    power_outcome=native_outcome(power), native_status=native["status"], power_status=power["status"],
                    native_HTTP_envelope_seconds=spans["native"].get(ident),
                    power_HTTP_envelope_seconds=spans["power"].get(ident),
                    native_HTTP_attempts=cells["native"]["HTTP_attempts"].get(ident, 0),
                    power_HTTP_attempts=cells["power"]["HTTP_attempts"].get(ident, 0)))
            comparison["longer_Power_HTTP_source_envelope_IDs"] = [i for i in expected
                if i in spans["native"] and i in spans["power"] and spans["power"][i] > spans["native"][i]]
            if len(spans["native"]) == len(expected):
                ranked = sorted(expected, key=lambda i: (-spans["native"][i], i))
                for fraction in (.01, .1):
                    ids = ranked[:math.ceil(fraction * len(expected))]
                    comparison["matched_native_ranked_HTTP_tails"][str(fraction)] = dict(source_IDs=ids,
                        overlapping_envelope_sums_seconds={m: sum(spans[m][i] for i in ids)
                            if all(i in spans[m] for i in ids) else None for m in spans},
                        outcomes={m: dict(collections.Counter(native_outcome(data[m][i]) for i in ids)) for m in data},
                        scope="Same native-ranked IDs; overlapping wall envelopes, not CPU, isolated-subset performance or removable critical path.")
            else:
                comparison["HTTP_tail_coverage_note"] = "Native HTTP ends are censored; full-population native-ranked tails are unavailable."
            output["pairs"][str(rep)] = comparison
    tall_stream.close()
    output["population_scope"] = "Real24preflight engagement only, not full-population performance." if stage == "preflight" else "All29750original sources, three predeclared paired observations."
    output["all_planned_cells_terminal_complete"] = all(x["observation"] == "complete" for x in output["conditions"].values())
    if output["all_planned_cells_terminal_complete"]:
        output["whole_ratio_of_complete_sums_observed"] = sum(
            output["conditions"]["rep" + str(i) + "-native"]["terminal"]["whole_lifecycle_seconds"]
            for i in range(1, repetitions + 1)) / sum(
            output["conditions"]["rep" + str(i) + "-power"]["terminal"]["whole_lifecycle_seconds"]
            for i in range(1, repetitions + 1))
        output["aggregate_scope"] = "All declared cells only; no confidence interval from three shared-host runs. Raw native outcome/field differences still determine interpretation."
        if stage == "full":
            pairs = output["pairs"].values()
            regressions = [set(x["longer_Power_HTTP_source_envelope_IDs"]) for x in pairs]
            output["Power_HTTP_regression_IDs_in_all_three_pairs"] = sorted(set.intersection(*regressions))
            output["persistent_regression_scope"] = "HTTP-envelope directions in every observed pair; censored ends and shared-host/queue effects remain explicit, not isolated CPU causes."
    staging = directory / "input-materialization.json"
    output["shared_input_materialization"] = json.loads(staging.read_text()) if staging.exists() else None
    (O / (stage + "-closed-analysis.json")).write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(dict(stage=stage, complete_cells=sum(x["observation"] == "complete" for x in output["conditions"].values()),
        expected_cells=output["expected_cells"], whole_ratio_of_complete_sums_observed=output.get("whole_ratio_of_complete_sums_observed"),
        native_outcome_changes={k: len(v["native_outcome_differences"]) for k, v in output["pairs"].items()})))
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["preflight", "full"], default="full")
    analyze(parser.parse_args().stage)
