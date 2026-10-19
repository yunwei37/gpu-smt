"""Cost-weight recorded SHRED events; hashes/timer sums are not reuse proofs or Amdahl bounds."""
import argparse
import collections
import gzip
import json
from pathlib import Path
import re
import runpy

outcome = runpy.run_path(str(Path(__file__).with_name("analyze-http.py")))["verification_outcome"]
def rows(path):
    if not path.exists():
        path = path.with_name(path.name + ".gz")
    with (gzip.open(path, "rt") if path.suffix == ".gz" else path.open()) as stream:
        return [json.loads(line) for line in stream]

def events(row):
    result = []
    for message in row["result"].get("response", {}).get("messages", []):
        for line in message.get("data", "").splitlines():
            match = re.match(r"LEAN_PREFIX_CERT event=([a-z_]+)(.*)", line)
            if not match:
                continue
            item = dict(event=match.group(1))
            for key, value in re.findall(r"([a-z_]+)=([^\s]+)", match.group(2)):
                item[key] = int(value) if value.isdigit() else value
            result.append(item)
    return result

def grouped(captures):
    groups = collections.defaultdict(list)
    for item in captures:
        groups[str(item["key"])].append(item)
    repeated = {key:items for key,items in groups.items() if len(items)>1}
    return dict(capture_occurrences=len(captures), distinct_hash_buckets=len(groups),
        repeated_capture_hash_buckets=len(repeated),
        repeated_capture_occurrences=sum(map(len,repeated.values())),
        hash_relaxed_redundant_generator_wall_seconds=sum(
            sum(item["generator_seconds"] for item in items)
            - min(item["generator_seconds"] for item in items)
            for items in repeated.values()),
        largest_repeated_buckets=sorted(
            [dict(key=key, captured_generator_wall_seconds_sum=sum(item["generator_seconds"] for item in items),
                captures=items) for key,items in repeated.items()],
            key=lambda item:item["captured_generator_wall_seconds_sum"],reverse=True)[:10])

def analyze(root):
    native = {item["proof_id"]:item for item in rows(root/"rep1-native/results.jsonl")}
    cached = rows(root/"rep1-shred/results.jsonl")
    assert set(native) == {item["proof_id"] for item in cached}
    counts = collections.Counter()
    sums = collections.Counter()
    hits = collections.Counter()
    captures = []
    per_source = []
    for item in cached:
        ident = item["proof_id"]
        observed = events(item)
        counts.update(event["event"] for event in observed)
        for event in observed:
            for key,value in event.items():
                if key.endswith("_ns") and isinstance(value,int):
                    sums[key] += value
            if event["event"] == "hit":
                hits[outcome(item)] += 1
            if event["event"] == "capture":
                captures.append(dict(proof_id=ident,key=event["key"],
                    generator_seconds=event.get("generator_ns",0)/1e9,
                    native_outcome=outcome(native[ident]),cached_outcome=outcome(item)))
        per_source.append(dict(proof_id=ident,native_outcome=outcome(native[ident]),
            cached_outcome=outcome(item),events=observed))
    complete = [item for item in captures if item["native_outcome"]==item["cached_outcome"]=="complete"]
    return dict(scope="All observed event wall timers, not CPU. Failed/thrown generators without terminal events are unmeasured. Hash grouping is a hypothetical bucket relaxation, not structural-key/proof compatibility, scheduling gain or a whole-wall/GPU Amdahl bound. Rejected/incomplete captures remain exposed. Root self-review.",
        sources=len(cached),event_counts=dict(counts),hit_outcomes=dict(hits),
        observed_wall_timer_sums_seconds={key:value/1e9 for key,value in sums.items()},
        captures_from_noncomplete_sources=len(captures)-len(complete),
        all_captures=grouped(captures),both_sources_complete_captures=grouped(complete),
        all_source_events=per_source)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root",type=Path)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    result=analyze(args.root)
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(dict(sources=result["sources"],events=result["event_counts"],
        all_hash_relaxed_wall=result["all_captures"]["hash_relaxed_redundant_generator_wall_seconds"],
        complete_hash_relaxed_wall=result["both_sources_complete_captures"]["hash_relaxed_redundant_generator_wall_seconds"])))
