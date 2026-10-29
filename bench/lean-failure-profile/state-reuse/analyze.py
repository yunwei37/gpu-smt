"""Analyze observed inputs and ordinary errors; never certify failure replay."""
import argparse
import collections
import gzip
import json
from pathlib import Path

PREFIX = "[gpu-smt-state-reuse] "


def lines(path):
    """Read a retained plain or losslessly compressed stream."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        yield from stream


def retained(directory, name):
    choices = [p for p in [directory/name, directory/(name+".gz")] if p.exists()]
    if len(choices) > 1:
        raise ValueError(f"Ambiguous retained copies: {directory/name}")
    return choices[0] if choices else None


def diagnostic_limits(row):
    # Conservative exclusion, not a semantic classifier or early rejection.
    text = "\n".join(x.get("text", "") for x in row.get("diagnostics", [])).lower()
    needles = {
        "memory_diagnostic": ["bad_alloc", "out of memory", "allocation failed"],
        "heartbeat_diagnostic": ["maximum number of heartbeats", "maxheartbeats",
                                 "maximum heartbeat"],
        "recursion_diagnostic": ["maximum recursion depth", "maxrecdepth"],
        "interrupt_diagnostic": ["interrupted", "interrupt exception"],
    }
    return [kind for kind, words in needles.items() if any(w in text for w in words)]


def source_status(row):
    if row["event"] == "operational_end":
        return row["status"]
    limits = diagnostic_limits(row)
    if limits:
        return "+".join(limits)
    if row.get("native_error"):
        return "native_error"
    if any("sorry" in x.get("text", "").lower()
           for x in row.get("diagnostics", [])):
        return "admission_diagnostic"
    return "completed_no_native_error"


def analyze_raw(path, eligible_sources=None):
    """One native process only. IDs from different segments are never joined."""
    begins, ends, call_sources, positions = {}, {}, {}, {}
    sources, anomalies = [], []
    current = None
    for line_number, line in enumerate(lines(path), 1):
        observed = line.startswith(PREFIX)
        if not observed and not line.startswith("{"):
            continue
        try:
            row = json.loads(line[len(PREFIX):] if observed else line)
        except ValueError:
            if observed:
                anomalies.append(dict(line=line_number, reason="malformed_observer_record"))
            continue
        if not isinstance(row, dict):
            continue
        event = row.get("event")
        if observed and event in ("begin", "end"):
            call = row["call"]
            table = begins if event == "begin" else ends
            if call in table:
                anomalies.append(dict(line=line_number, reason="duplicate_"+event, call=call))
            table[call] = row
            positions[(call, event)] = line_number
            if event == "begin":
                call_sources[call] = current
        elif event == "candidate_begin":
            current = (row["id"], row["mode"])
        elif event == "candidate_end":
            identity = (row["id"], row["mode"])
            if current != identity:
                anomalies.append(dict(line=line_number, reason="candidate_identity_mismatch"))
            sources.append(row)
            current = None
    completed_sources = {(r["id"], r["mode"]) for r in sources
                         if not diagnostic_limits(r)}
    if eligible_sources is not None:
        completed_sources &= eligible_sources
    prior, repeats, outcomes, changes = {}, [], collections.Counter(), []
    for call, start in sorted(begins.items(), key=lambda item: positions[(item[0], "begin")]):
        end = ends.get(call)
        if end is None:
            continue
        outcomes[end["outcome"]] += 1
        key = start["key"]
        source = call_sources[call]
        if key is None or source not in completed_sources:
            continue
        # A producer must have finished before this call starts. Open/overlapping
        # invocations cannot become a cached answer, even if they finish later.
        candidates = [c for c in prior.get(key, [])
                      if positions[(c, "end")] < positions[(call, "begin")]]
        if candidates:
            pcall = candidates[0]
            pend = ends[pcall]
            item = dict(call=call, prior_call=pcall, key=key, source=source,
                        prior_source=call_sources[pcall], kind=start["kind"],
                        outcome=end["outcome"], prior_outcome=pend["outcome"],
                        observed_action_ns=end["elapsed_ns"],
                        same_goal_generation_indexes=(
                            start["goal_generation_indexes"] == begins[pcall]["goal_generation_indexes"]
                            if "goal_generation_indexes" in start and
                            "goal_generation_indexes" in begins[pcall] else None))
            repeats.append(item)
            if end["outcome"] != pend["outcome"]:
                changes.append(item)
        prior.setdefault(key, []).append(call)
    unstable = {r["key"] for r in changes}
    failures = [r for r in repeats if r["outcome"] == r["prior_outcome"] == "native_error"
                and r["key"] not in unstable]
    by_kind = {}
    for row in failures:
        bucket = by_kind.setdefault(row["kind"], dict(occurrences=0, action_ns=0))
        bucket["occurrences"] += 1
        bucket["action_ns"] += row["observed_action_ns"]
    return dict(native_sources=len(sources),
        native_error_sources=sum(r["native_error"] for r in sources),
        observed_begins=len(begins), completed_observations=len(ends),
        open_observations=sorted(set(begins)-set(ends)),
        unsupported_inputs=sum(r["key"] is None for r in begins.values()),
        excluded_operational_or_limit_calls=sum(
            call_sources[c] not in completed_sources for c in begins),
        outcomes=dict(outcomes), completed_input_match_occurrences=len(repeats),
        repeated_ordinary_error_occurrences=len(failures),
        same_generation_input_matches=sum(r["same_goal_generation_indexes"] is True for r in repeats),
        different_generation_input_matches=sum(r["same_goal_generation_indexes"] is False for r in repeats),
        unobserved_generation_input_matches=sum(r["same_goal_generation_indexes"] is None for r in repeats),
        observed_repeated_error_wall_seconds=sum(r["observed_action_ns"] for r in failures)/1e9,
        repeated_ordinary_errors_by_kind=by_kind,
        cross_source_repeated_ordinary_errors=sum(r["source"] != r["prior_source"] for r in failures),
        cross_source_repeated_error_seconds=sum(r["observed_action_ns"] for r in failures
                                                if r["source"] != r["prior_source"])/1e9,
        within_source_repeated_ordinary_errors=sum(r["source"] == r["prior_source"] for r in failures),
        repeated_outcome_changes=changes,
        unstable_input_keys=sorted(unstable),
        capture_seconds=sum(r["capture_ns"] for r in begins.values())/1e9,
        observed_action_seconds=sum(r["elapsed_ns"] for r in ends.values())/1e9,
        repeats=repeats, errors=anomalies,
        unmatched_end_calls=sorted(set(ends)-set(begins)),
        complete_replay_certification=False, complete_state_hit_count=None,
        end_to_end_speedup=None,
        scope="One process segment; observed input matches only. Operational/limit sources "
              "and outcome-unstable keys receive no ordinary-failure cost credit. "
              "Generation/hidden/post-error/heartbeat/diagnostic replay remains unqualified.")


def analyze_collection(directory):
    """Recompute a finite collection, preserving attempts, retries and unknowns."""
    result_path = retained(directory, "results.jsonl")
    lifecycle_path = retained(directory, "lifecycle.jsonl")
    rows = [json.loads(s) for s in lines(result_path)] if result_path else []
    lifecycle = [json.loads(s) for s in lines(lifecycle_path)] if lifecycle_path else []
    terminal_path, exit_path = retained(directory, "terminal.json"), retained(directory, "client-exit.json")
    terminal = json.loads("".join(lines(terminal_path))) if terminal_path else None
    client_exit = json.loads("".join(lines(exit_path))) if exit_path else None
    segments, eligible, final, attempt_counts = [], {}, {}, collections.Counter()
    late = 0
    for row in rows:
        if row["event"] == "late_candidate_end":
            late += 1
            continue  # Raw native completion is not completion within caller budget.
        if row["event"] not in ("candidate_end", "operational_end"):
            continue
        identity = (row["id"], row["mode"])
        final[identity] = row
        attempt_counts[(row["mode"], source_status(row))] += 1
        if row["event"] == "candidate_end" and not diagnostic_limits(row):
            eligible.setdefault(row["segment"], set()).add(identity)
    for segment in sorted(directory.glob("segment-*")):
        path = retained(segment, "raw.log")
        if path is None:
            continue
        number = int(segment.name.split("-")[1])
        analysis = analyze_raw(path, eligible.get(number, set()))
        analysis["segment"] = number
        segments.append(analysis)
    final_counts, datasets = collections.Counter(), {}
    for (identity, mode), row in final.items():
        status = source_status(row)
        final_counts[(mode, status)] += 1
        dataset = identity.split("-", 1)[0]
        datasets.setdefault(dataset, collections.Counter())[(mode, status)] += 1
    differences, diagnostic_differences = [], []
    ids = sorted({i for i, _ in final})
    for identity in ids:
        reference = final.get((identity, "original"))
        if reference is None:
            continue
        for mode in ("import-control", "observe"):
            other = final.get((identity, mode))
            if other is None:
                continue
            if source_status(reference) != source_status(other):
                differences.append(dict(id=identity, mode=mode,
                                        original=source_status(reference), other=source_status(other)))
            if reference["event"] == other["event"] == "candidate_end":
                if reference["diagnostics"] != other["diagnostics"]:
                    diagnostic_differences.append(dict(id=identity, mode=mode))
    def counted(counter):
        return [dict(mode=mode, status=status, count=count)
                for (mode, status), count in sorted(counter.items())]
    return dict(terminal=terminal, client_exit=client_exit,
        collection_complete=bool(terminal and terminal.get("state") == "complete"
                                 and client_exit and client_exit.get("state", "returned") == "returned"
                                 and "error" in client_exit
                                 and client_exit.get("error") is None
                                 and terminal.get("planned") == len(final)),
        final_cells_returned=len(final), attempt_outcomes=counted(attempt_counts),
        final_outcomes=counted(final_counts),
        datasets={name: counted(counts) for name, counts in datasets.items()},
        watchdog_events=sum(r["event"] == "watchdog_kill" for r in lifecycle),
        unresolved_native_exits=[r for r in lifecycle if r["event"] == "retired"
                                 and r.get("exit") and not r.get("operational")],
        exclusive_retry_attempts=sum(r.get("exclusive_retry", False) for r in rows
                                     if r["event"] in ("candidate_end", "operational_end")),
        late_native_completions=late, paired_status_differences=differences,
        paired_raw_diagnostic_differences=diagnostic_differences,
        segments=segments,
        observed_repeated_error_wall_seconds=sum(
            r["observed_repeated_error_wall_seconds"] for r in segments),
        repeated_ordinary_error_occurrences=sum(
            r["repeated_ordinary_error_occurrences"] for r in segments),
        complete_state_hit_count=None, complete_replay_certification=False,
        end_to_end_speedup=None,
        scope="Selected outer-unit population. No joins across native process segments. "
              "Final outcomes never discard prior operational attempts. Raw clock sums "
              "are not warm-service speedup or a global Amdahl bound. An incomplete "
              "collection is not a population result; process retirement is checked separately.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--raw", type=Path)
    choice.add_argument("--collection", type=Path,
                        help="Completed run directory with retained segments/results/lifecycle")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = analyze_raw(args.raw) if args.raw else analyze_collection(args.collection)
    args.out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("repeats", "segments")}))


if __name__ == "__main__":
    main()
