"""Sensitivity check of retained memory attribution using full capture windows.

The primary477-source observation remains in source-memory-attribution-2026-10-25.
This one-off control uses active body ownership and the entire sampling window.
It runs no verifier or model; observations remain history/resource-dependent.
"""
import argparse
import bisect
import collections
import gzip
import importlib.util
import json
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / "bench/lean-failure-profile/analyze.py").is_file())
_SPEC = importlib.util.spec_from_file_location(
    "gpu_smt_failure_profile", ROOT / "bench/lean-failure-profile/analyze.py")
_PROFILE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_PROFILE)


def owner(event, wanted):
    """Require one observed active source/body owner, never an idle tag."""
    if event.get("event") == "source_boundary" or event.get("sampler_error"):
        return None
    active = {(t.get("source_id"), t.get("phase"))
              for t in event.get("threads", []) if t.get("active")}
    if len(active) != 1:
        return None
    source, phase = next(iter(active))
    return source if source in wanted and phase == "body" else None


def body_runs(events, wanted):
    """Coalesce equal observations; do not extrapolate past their endpoints."""
    runs, current, previous = [], None, None
    for event in events:
        if "_stream_closed" in event:
            continue
        now = event["time_ns"]
        if previous is not None and now < previous:
            raise ValueError("nonmonotonic native profile")
        gap = now - previous if previous is not None else 0
        previous = now
        source = owner(event, wanted)
        if source is None:
            if current is not None:
                runs.append(current)
            current = None
        elif current is not None and current[2] == source and gap <= 2_500_000_000:
            current = (current[0], now, source)
        else:
            if current is not None:
                runs.append(current)
            current = (now, now, source)
    if current is not None:
        runs.append(current)
    return runs


def native_processes(row):
    return {(p["pid"], p["birth"]): p
            for p in row["processes"] if p.get("native_repl")}


def associate(previous, current, runs, births, envelopes):
    """Return source/identity/RSS only when the whole capture window fits."""
    matches, excluded = [], collections.Counter()
    before = native_processes(previous)
    lo, hi = previous["time_ns"], current["time_ns"]
    if hi < lo:
        raise ValueError("nonmonotonic RSS stream")
    for identity, process in native_processes(current).items():
        pid, birth = identity
        if births.get(pid) != {birth}:
            excluded["ambiguous_or_missing_birth"] += 1
            continue
        if identity not in before:
            excluded["first_or_changed_process_sample"] += 1
            continue
        candidates = runs.get(pid, [])
        starts = [r[0] for r in candidates]
        index = bisect.bisect_right(starts, lo) - 1
        if index < 0 or candidates[index][1] < hi:
            excluded["window_not_inside_body_owner_run"] += 1
            continue
        source = candidates[index][2]
        if not any(begin <= lo <= hi <= end
                   for begin, end in envelopes.get(source, [])):
            excluded["window_outside_matching_HTTP_envelope"] += 1
            continue
        matches.append(dict(source_id=source, pid=pid, birth=birth,
                            capture_lower_ns=lo, capture_upper_ns=hi,
                            sampled_rss_bytes=process["rss"]))
    return matches, excluded


def analyze(run, inputs, out):
    selected = json.loads((run / "selected.json").read_text())
    wanted = set(selected["ids"])
    terminal = json.loads((run / "profile/terminal.json").read_text())
    if terminal["state"] != "complete" or terminal["returned"] != len(wanted):
        raise ValueError("retain incomplete capture; do not call it the full cohort")
    batch = json.loads(gzip.decompress(inputs.read_bytes()))
    canonical = {c["id"]: c for c in batch["candidates"]}
    envelopes, source_mismatches = collections.defaultdict(list), []
    for event in _PROFILE.rawrows(run / "profile/http.jsonl"):
        if event.get("event") != "response":
            continue
        snippets = json.loads(event["request"]).get("snippets", [])
        if len(snippets) != 1 or snippets[0]["id"] not in wanted:
            continue
        snippet = snippets[0]
        source = snippet["id"]
        if snippet["code"] != canonical[source]["code"]:
            source_mismatches.append(source)
            continue
        envelopes[source].append((event["start_ns"], event["end_ns"]))

    births = collections.defaultdict(set)
    for row in _PROFILE.rawrows(run / "profile/memory-rss.jsonl"):
        for pid, birth in native_processes(row):
            births[pid].add(birth)
    runs, stream_metadata = {}, []
    for path in sorted((run / "profiles").glob("*.jsonl.gz")):
        pid = int(path.name.split(".")[0])
        metadata = {}
        def events():
            for event in _PROFILE.snapshots(path):
                if "_stream_closed" in event:
                    metadata.update(event)
                else:
                    if event["pid"] != pid:
                        raise ValueError("profile filename/native PID mismatch")
                    yield event
        runs[pid] = body_runs(events(), wanted)
        stream_metadata.append(dict(path=str(path), pid=pid,
                                    body_runs=len(runs[pid]), **metadata))

    statuses = {row["proof_id"]: row["status"]
                for row in _PROFILE.rawrows(run / "profile/results.jsonl")}
    output = out.open("w")
    samples, exclusions = collections.defaultdict(list), collections.Counter()
    previous, memory_rows = None, 0
    for row in _PROFILE.rawrows(run / "profile/memory-rss.jsonl"):
        memory_rows += 1
        if previous is not None:
            matches, dropped = associate(previous, row, runs, births, envelopes)
            exclusions.update(dropped)
            for match in matches:
                samples[match["source_id"]].append(match)
        previous = row
    histories = collections.defaultdict(dict)
    for pid, intervals in runs.items():
        for begin, _, source in intervals:
            histories[pid].setdefault(source, begin)
    per_source = []
    for source in selected["ids"]:
        observed = samples[source]
        peak = max(observed, key=lambda r: r["sampled_rss_bytes"]) if observed else None
        first = min(observed, key=lambda r: r["capture_upper_ns"]) if observed else None
        contexts = []
        for pid, birth in sorted({(r["pid"], r["birth"]) for r in observed}):
            first_run = histories[pid][source]
            contexts.append(dict(pid=pid, birth=birth,
                prior_observed_selected_sources=sum(t < first_run for t in histories[pid].values())))
        per_source.append(dict(source_id=source, task_id=canonical[source]["task_id"],
            baseline_status=selected["baseline_statuses"][source],
            profile_status=statuses[source], code_bytes=len(canonical[source]["code"].encode()),
            associated_samples=len(observed),
            sampled_body_leader_peak_rss_bytes=peak["sampled_rss_bytes"] if peak else None,
            first_associated_rss_bytes=first["sampled_rss_bytes"] if first else None,
            observed_growth_from_first_bytes=peak["sampled_rss_bytes"]-first["sampled_rss_bytes"] if peak else None,
            peak_sample=peak, contexts=contexts,
            resource_or_timeout_censored=statuses[source] in ["resource_failure", "timeout_error"]))
    with gzip.open(out.with_suffix(".samples.jsonl.gz"), "wt") as stream:
        for source in selected["ids"]:
            for sample in samples[source]:
                stream.write(json.dumps(sample) + chr(10))
    summary = dict(planned_sources=len(wanted),
        sources_with_associated_samples=sum(bool(samples[s]) for s in wanted),
        associated_samples=sum(len(v) for v in samples.values()),
        RSS_records=memory_rows, exclusions=dict(exclusions),
        source_code_mismatches=source_mismatches,
        profile_streams=stream_metadata,
        resource_point=dict(concurrency=terminal["source_concurrency"],
            per_repl_AS_bytes=terminal["per_native_repl_address_limit_bytes"],
            aggregate_budget_bytes=terminal["aggregate_memory_budget_bytes"],
            native_version=terminal["lean_version"]),
        scope="Body-active sampled native leader RSS with HTTP/time/birth checks; includes warm history, not isolated demand, true peak, causal tactic memory, training success or uncapped counterfactual.",
        sources=per_source)
    json.dump(summary, output, ensure_ascii=False, indent=2)
    output.write("\n")
    output.close()
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.run, args.inputs, args.out)
    print(json.dumps({k:v for k,v in result.items() if k not in ["sources", "profile_streams"]}))


if __name__ == "__main__":
    main()
