#!/usr/bin/env python3
"""Analyze complete retained four-warm/engine pairs, without running them."""
import argparse
import collections
import datetime
import gzip
import json
import math
from pathlib import Path

WARM_STATUS = {
    "valid": "accepted", "lean_error": "rejected", "sorry": "incomplete",
    "timeout_error": "timeout", "resource_failure": "resource_exhausted",
    "repl_error": "backend_error", "server_error": "backend_error",
}
ENGINE_STATUS = set(WARM_STATUS.values()) | {"cancelled", "preempted"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def duration(value):
    require(isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value >= 0, "invalid elapsed clock")
    return value


def index(rows, expected, label):
    require(len(rows) == len(expected), label + " row count differs")
    result = {row["id"]: row for row in rows}
    require(len(result) == len(rows) and set(result) == set(expected),
            label + " IDs are missing, duplicated or foreign")
    return result


def incidental(payload):
    """Keep diagnostics intact; label these two explicit wire differences only."""
    if not isinstance(payload, dict):
        return payload
    result = dict(payload)
    result.pop("env", None)
    if result.get("ast") == []:
        result.pop("ast")
    return result


def executable_resolution(requested):
    """Observe an existing alias after a run; never rewrite its frozen manifest."""
    path = Path(requested)
    resolved = path.resolve(strict=True)
    a, b = path.stat(), resolved.stat()
    require(path.is_file() and resolved.is_file()
            and (a.st_dev, a.st_ino) == (b.st_dev, b.st_ino),
            "executable alias does not identify the same existing file")
    return {"requested": requested, "resolved": str(resolved),
            "device": a.st_dev, "inode": a.st_ino, "bytes": a.st_size,
            "same_file": True, "observed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "scope": "post-run filesystem alias observation; not a frozen launch-time attestation"}


def read_engine_memory(root, budget):
    path = root / "engine.stderr"
    if path.exists():
        stream = path.open("rt")
    elif path.with_name(path.name + ".gz").exists():
        path = path.with_name(path.name + ".gz")
        stream = gzip.open(path, "rt")
    else:
        return None
    samples, above, actions, malformed, invalid = 0, 0, 0, 0, 0
    peak, logged_budgets = None, set()
    with stream:
        for line in stream:
            try:
                fields = json.loads(line)["fields"]
                if not isinstance(fields, dict):
                    raise ValueError("non-object fields")
            except (ValueError, KeyError, TypeError):
                malformed += 1
                continue
            if fields.get("message") == "preempt owned attempt and requeue exclusively":
                actions += 1
            if fields.get("message") != "owned RSS sample":
                continue
            rss = fields.get("rss_bytes")
            if not isinstance(rss, int) or isinstance(rss, bool) or rss < 0:
                invalid += 1
                continue
            samples += 1
            peak = rss if peak is None else max(peak, rss)
            above += rss > budget
            logged = fields.get("budget_bytes")
            if isinstance(logged, int) and not isinstance(logged, bool):
                logged_budgets.add(logged)
    return {
        "source": path.name, "rss_samples": samples,
        "peak_sampled_owned_RSS_bytes": peak,
        "samples_above_declared_budget": above, "declared_budget_bytes": budget,
        "logged_budget_values": sorted(logged_budgets), "watchdog_events": actions,
        "malformed_log_lines": malformed, "invalid_rss_sample_lines": invalid,
        "scope": "Existing aggregate owned-RSS log samples,not per-leader maxima or a kernel hard quota. Missing/malformed observations are not zero.",
    }


def compare(point):
    m, batch = point["manifest"], point["input"]
    warm, wt, engine = point["warm"], point["warm_terminal"], point["engine"]
    phase = m.get("phase", "qualification")
    require(phase in {"qualification", "full"}, "unknown resource comparison phase")
    terminal_state = "full-pair-complete" if phase == "full" else "qualification-pair-complete"
    require(point["terminal"]["state"] == terminal_state,
            "pair has no successful terminal receipt for its phase")
    require(wt["state"] == "complete" and not wt["native_survivors"]
            and wt["memory"]["error"] is None, "warm collection is incomplete or unhealthy")
    require(batch["mode"] == "all" and engine["batch"] == batch
            and warm["original_candidates"] == batch["candidates"],
            "mode or exact source/timeout/task/reuse population differs")
    ids = [c["id"] for c in batch["candidates"]]
    require(ids and len(set(ids)) == len(ids), "input IDs are empty or duplicated")
    if phase == "full":
        require(m.get("candidate_count") == len(ids), "full input count differs from declared population")
    require(wt["returned"] == len(ids), "warm returned count differs")
    w, e = index(warm["results"], ids, "warm"), index(engine["results"], ids, "engine")
    require(set(warm["attempts"]) == set(ids), "warm physical histories differ")
    require(wt["physical_attempts"] == sum(len(v) for v in warm["attempts"].values()),
            "warm physical-attempt total differs")
    resource, wr = engine["resources"], wt["resources"]
    require(sorted(resource["cpus"]) == sorted(wr["cpus"]) == sorted(m["cpus"])
            and resource["memory_bytes"] == wr["memory_bytes"] == m["memory_bytes"],
            "aggregate CPU/RSS resource points differ")
    require(wr["per_process_AS"] is None and m["fixed_process_AS_cap"] is False,
            "fixed per-process AS differs")
    require(resource["cores_per_worker"] > 0
            and wr["maximum_native_workers"] == len(resource["cpus"]) // resource["cores_per_worker"]
            and wt["memory"]["peak_sampled_native_repl_count"] == wr["maximum_native_workers"],
            "four-warm engagement or worker resource point differs")
    library = m["native_library"]
    require(wt["native_library"] == library and wt["source_repl"] == m["warm_repl"],
            "warm native library or executable differs")
    resolution = point.get("executable_resolution")
    native_repl = m["warm_repl"]
    if resolution is not None:
        require(resolution["requested"] == native_repl and resolution["same_file"] is True,
                "executable alias receipt differs from the original requested path")
        native_repl = resolution["resolved"]
    # Match complete quoted path fields, not prefixes such as repl-backup.
    require(("lean-repl|" + json.dumps(native_repl, ensure_ascii=False) + "|") in engine["backend"]
            and ("|" + json.dumps(wt["source_context"]["project"], ensure_ascii=False) + "|")
            in engine["backend"], "engine native fallback executable/project differs")
    mapped = point["warm_libraries"]
    identities = {(p["pid"], p["birth"]) for p in mapped}
    require(len(identities) == len(mapped) == wr["maximum_native_workers"]
            and all(p["mapped"] is True and p["native_library"] == library for p in mapped),
            "warm native-library engagement is missing")
    attempts = [a for row in e.values() for a in row["attempts"]]
    contexts = [json.loads(v["detail"])["prepared_context"]
                for a in attempts for v in a.get("backend_events", [])
                if v["stage"] == "prepared_ready"]
    require(contexts and all(c.get("native_library") == library for c in contexts),
            "prepared native-library engagement is missing")
    require(not any(v["cached"] or v["coalesced"] for v in e.values()),
            "completed-result reuse is outside this resource comparison")
    raw_warm = {i: w[i]["status"] for i in ids}
    require(all(v in WARM_STATUS for v in raw_warm.values()), "unknown warm status")
    ws = {i: WARM_STATUS[raw_warm[i]] for i in ids}
    es = {i: e[i]["outcome"]["status"] for i in ids}
    require(all(v in ENGINE_STATUS for v in es.values()), "unknown engine status")
    accepted_w = {i for i in ids if ws[i] == "accepted"}
    accepted_e = {i for i in ids if es[i] == "accepted"}
    changed = [{"id": i, "warm_raw": raw_warm[i], "warm": ws[i], "engine": es[i]}
               for i in ids if ws[i] != es[i]]
    wp = {i: w[i]["result"].get("response") for i in ids}
    ep = {i: e[i]["outcome"].get("response") for i in ids}
    clocks = {}
    for name, internal in [("warm", wt["whole_seconds"]), ("engine", engine["lifecycle_seconds"])]:
        exit_record = point[name + "_exit"]
        require(exit_record["exit"] == 0, name + " executable exit is not successful")
        external = duration(exit_record["external_seconds"])
        require(external > 0 and external + 1e-6 >= duration(internal),
                name + " internal/external clocks are inconsistent")
        clocks[name] = {"launch_to_exit_seconds": external, "internal_seconds": internal,
                        "external_minus_internal_seconds": external - internal}
    warm_attempt_seconds = {i: math.fsum(duration(a["wall_seconds"])
                            for a in warm["attempts"][i]) for i in ids}
    engine_attempt_seconds = {i: math.fsum(duration(a["elapsed_seconds"])
                              for a in e[i]["attempts"]) for i in ids}
    ranked = sorted(ids, key=lambda i: (-warm_attempt_seconds[i], i))
    tails = []
    for percent in [1, 10]:
        selected = ranked[:math.ceil(len(ids) * percent / 100)]
        tails.append({"warm_slowest_percent": percent, "ids": selected,
                      "warm_admitted_envelope_seconds_sum": math.fsum(warm_attempt_seconds[i] for i in selected),
                      "engine_native_attempt_seconds_sum": math.fsum(engine_attempt_seconds[i] for i in selected),
                      "statuses": [dict(id=i, warm=ws[i], engine=es[i]) for i in selected]})
    fallbacks = collections.Counter(v["detail"] for a in attempts
                                   for v in a.get("backend_events", [])
                                   if v["stage"] == "fresh_fallback")
    result = {
        "scope": ("complete full-phase resource pair; root result review required"
                  if phase == "full" else
                  "development-selected resource qualification; root result review required"),
        "candidate_count": len(ids), "external_clocks": clocks,
        "executable_resolution": resolution,
        "descriptive_external_elapsed_ratio": clocks["warm"]["launch_to_exit_seconds"] / clocks["engine"]["launch_to_exit_seconds"],
        "ratio_is_not_a_gain_claim": True, "resource_layer_gain_established": False,
        "accepted_set_only_warm": sorted(accepted_w - accepted_e),
        "accepted_set_only_engine": sorted(accepted_e - accepted_w),
        "changed_statuses": changed,
        "raw_warm_status_counts": dict(collections.Counter(raw_warm.values())),
        "warm_status_counts": dict(collections.Counter(ws.values())),
        "engine_status_counts": dict(collections.Counter(es.values())),
        "status_aliases": WARM_STATUS,
        "raw_native_payload_changed_ids": [i for i in ids if wp[i] != ep[i]],
        "top_level_env_and_empty_ast_normalized_payload_changed_ids":
            [i for i in ids if incidental(wp[i]) != incidental(ep[i])],
        "both_native_payloads_available_ids": [i for i in ids if wp[i] is not None and ep[i] is not None],
        "missing_warm_native_payload_ids": [i for i in ids if wp[i] is None],
        "missing_engine_native_payload_ids": [i for i in ids if ep[i] is None],
        "diagnostic_normalization": "Only top-level env handles and empty ast are removed in the labelled secondary view; raw payload differences remain. No metavariable/message/position normalization.",
        "warm_preparation_seconds": duration(wt["preparation_seconds"]),
        "engine_prepared_ready_event_rows": len(contexts),
        "engine_preparation_seconds": None,
        "engine_preparation_scope": "duration is not recoverable from ready event counts alone",
        "fresh_fallback_event_reasons": dict(fallbacks),
        "warm_physical_attempts": wt["physical_attempts"], "engine_attempts": len(attempts),
        "warm_admitted_envelope_seconds_sum": math.fsum(warm_attempt_seconds.values()),
        "engine_native_attempt_seconds_sum": math.fsum(engine_attempt_seconds.values()),
        "tails": tails,
        "clock_limits": "External clocks include program loading, setup, queueing, native work, retries, serialization and retirement. Warm admitted-envelope clocks can end before asynchronous teardown; engine attempt clocks include retirement. Neither overlapping sum is whole-run time or comparable isolated native CPU. Logging/observation CPU is not independently identified.",
        "resource_limits": "Same aggregate CPU/RSS point; warm pool and engine per-worker affinity differ. Configuration/terminal receipts are recorded evidence, not independent authentication or proof of arbitrary FFI/fork safety.",
    }
    if phase == "full":
        result.update(
            whole_batch_candidates_per_second={
                name: len(ids) / clocks[name]["launch_to_exit_seconds"]
                for name in ["warm", "engine"]
            },
            operational_error_differences=[
                {"id": i, "warm": w[i]["result"].get("error"), "engine": e[i]["outcome"].get("error")}
                for i in ids if w[i]["result"].get("error") != e[i]["outcome"].get("error")
            ],
            warm_memory_summary=wt["memory"],
            engine_memory_summary=point.get("engine_memory"),
        )
    return result


def read_point(root):
    def read_json(path):
        path = root / path
        if path.exists():
            return json.loads(path.read_text())
        return json.loads(gzip.decompress(path.with_name(path.name + ".gz").read_bytes()))

    manifest = read_json("manifest.json")
    phase = manifest.get("phase", "qualification")
    require(phase in {"qualification", "full"}, "unknown resource comparison phase")
    paths = {
        "input": "input7808.json" if phase == "full" else "input24.json",
        "warm": "warm/results.json", "warm_terminal": "warm/terminal.json",
        "engine": "engine.stdout", "warm_exit": "warm-exit.json",
        "engine_exit": "engine-exit.json", "terminal": "terminal.json",
        "warm_libraries": "warm/native-library-readiness.json",
    }
    point = {"manifest": manifest, **{name: read_json(path) for name, path in paths.items()}}
    if phase == "full":
        point["engine_memory"] = read_engine_memory(root, manifest["memory_bytes"])
    receipt = root / "native-executable-resolution.json"
    if receipt.exists():
        point["executable_resolution"] = json.loads(receipt.read_text())
    elif ("lean-repl|" + json.dumps(point["manifest"]["warm_repl"], ensure_ascii=False) + "|") not in point["engine"]["backend"]:
        point["executable_resolution"] = executable_resolution(point["manifest"]["warm_repl"])
    return point


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    print(json.dumps(compare(read_point(args.root)), indent=2))
