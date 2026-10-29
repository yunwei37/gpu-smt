"""Analyze exact-input observations;never promote them to certified replay."""
import argparse
import collections
import gzip
import json
from pathlib import Path


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument("--raw", type=Path, required=True)
    a.add_argument("--out", type=Path, required=True)
    args = a.parse_args()
    data = (gzip.decompress(args.raw.read_bytes()) if args.raw.suffix == ".gz"
            else args.raw.read_bytes()).decode()
    begins = {}
    ends = {}
    sources = []
    current = None
    call_sources = {}
    errors = []
    for line in data.splitlines():
        if line.startswith("[gpu-smt-state-reuse] "):
            x = json.loads(line.split("] ", 1)[1])
            if x["event"] == "begin":
                begins[x["call"]] = x
                call_sources[x["call"]] = current
            elif x["event"] == "end":
                ends[x["call"]] = x
        elif line.startswith("{"):
            x = json.loads(line)
            if x.get("event") == "candidate_begin":
                current = (x["id"], x["mode"])
            elif x.get("event") == "candidate_end":
                assert current == (x["id"], x["mode"])
                sources.append(x)
                current = None
    prior = {}
    repeats = []
    failures = []
    changes = []
    outcomes = collections.Counter()
    for call, start in sorted(begins.items()):
        end = ends.get(call)
        if end is None:
            continue
        outcomes[end["outcome"]] += 1
        key = start["key"]
        if key is None:
            continue
        if key in prior:
            pcall, pend = prior[key]
            item = dict(call=call, prior_call=pcall, key=key,
                        source=call_sources[call], prior_source=call_sources[pcall],
                        outcome=end["outcome"], prior_outcome=pend["outcome"],
                        observed_action_ns=end["elapsed_ns"])
            repeats.append(item)
            if end["outcome"] != pend["outcome"]:
                changes.append(item)
            if end["outcome"] == pend["outcome"] == "native_error":
                failures.append(item)
        else:
            prior[key] = (call, end)
    result = dict(native_sources=len(sources),
        native_error_sources=sum(x["native_error"] for x in sources),
        observed_begins=len(begins), completed_observations=len(ends),
        open_observations=sorted(set(begins)-set(ends)),
        unsupported_inputs=sum(x["key"] is None for x in begins.values()),
        outcomes=dict(outcomes), completed_input_match_occurrences=len(repeats),
        repeated_ordinary_error_occurrences=len(failures),
        observed_repeated_error_wall_seconds=sum(
            x["observed_action_ns"] for x in failures)/1e9,
        repeated_outcome_changes=changes,
        capture_seconds=sum(x["capture_ns"] for x in begins.values())/1e9,
        observed_action_seconds=sum(x["elapsed_ns"] for x in ends.values())/1e9,
        repeats=repeats, complete_replay_certification=False,
        complete_state_hit_count=None, end_to_end_speedup=None,
        errors=errors, scope="One process segment;input-key equality with conservative opaque identity. "
        "Ordinary errors only;not cached failure,proof accepted or population benefit.")
    args.out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ["repeats"]}))


if __name__ == "__main__":
    main()
