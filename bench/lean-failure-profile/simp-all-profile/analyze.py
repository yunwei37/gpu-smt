"""Attribute retained native simp diagnostics without inferring rejection.

Source positions join the exact preparation mapping. Missing/unterminated
phases and unavailable original runtime records remain explicit. Used origins
are cumulative observations, not a causal blame list or loop certificate.
"""
import argparse
import collections
import gzip
import json
from pathlib import Path

PREFIX = "[gpu-smt-simp-stage] "

def analyze_source(source_id, path, mapping):
    if path is None:
        return dict(id=source_id, runtime_record_available=False,
                    observed_phases=[], open_phases=[], last_progress=None,
                    certified_impossible=False, reason="runtime record unavailable")
    opener = gzip.open if path.suffix == ".gz" else open
    events, malformed = [], []
    with opener(path, "rt") as stream:
        for number, line in enumerate(stream, 1):
            if line.startswith(PREFIX):
                try:
                    events.append(json.loads(line[len(PREFIX):]))
                except json.JSONDecodeError:
                    malformed.append(number)
    original = {x["instrumented_keyword_byte"]: x["original_byte"]
                for x in mapping.get("sites", [])}
    active = {}
    phases = collections.defaultdict(lambda: dict(
        began=0, ended=0, elapsed_ns=0, progress_snapshots=0, used_origins=set()))
    last_progress = None
    mismatched = []
    for event in events:
        key = (event.get("invocation_byte"), event.get("phase"),
               event.get("round"), event.get("slot"))
        phase = phases[key]
        kind = event.get("event")
        if kind == "begin":
            phase["began"] += 1
            if key in active:
                mismatched.append(dict(reason="repeated begin", key=key))
            active[key] = event
        elif kind == "end":
            phase["ended"] += 1
            phase["elapsed_ns"] += event.get("elapsed_ns", 0)
            if active.pop(key, None) is None:
                mismatched.append(dict(reason="end without begin", key=key))
        elif kind == "progress":
            phase["progress_snapshots"] += 1
            phase["used_origins"].update(
                x["origin"] for x in event.get("used_origins", []))
            last_progress = dict(event,
                original_invocation_byte=original.get(key[0]))
    def describe(key, value):
        return dict(invocation_byte=key[0],
                    original_invocation_byte=original.get(key[0]),
                    phase=key[1], round=key[2], slot=key[3],
                    **{k:sorted(v) if isinstance(v,set) else v
                       for k,v in value.items()})
    return dict(id=source_id, runtime_record_available=True,
        diagnostic_file=str(path), parsed_events=len(events),
        observed_phases=[describe(k,v) for k,v in phases.items()],
        open_phases=[describe(k,phases[k]) for k in active],
        last_progress=last_progress, malformed_event_lines=malformed,
        unmatched_events=mismatched, certified_impossible=False,
        scope="Phase end may unwind an error; cumulative used origins and hash hints are not a causal or cycle certificate.")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diagnostics", type=Path, required=True)
    parser.add_argument("--preparation", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    mapping = {}
    if args.preparation:
        mapping = {x["id"]:x for x in
                   json.loads(args.preparation.read_text())["manifest"]}
    files = {}
    for path in args.diagnostics.iterdir():
        if path.is_file() and (path.name.endswith(".jsonl") or
                               path.name.endswith(".jsonl.gz")):
            source_id = path.name.removesuffix(".gz").removesuffix(".jsonl")
            if source_id in files:
                raise ValueError("ambiguous diagnostic files for "+source_id)
            files[source_id] = path
    if mapping:
        ids = list(mapping)
    elif (args.diagnostics / "terminal.json").exists():
        terminal = json.loads((args.diagnostics / "terminal.json").read_text())
        ids = [row["id"] for row in terminal["results"]]
    else:
        raise ValueError("exact preparation or terminal candidate inventory required")
    sources = [analyze_source(i, files.get(i), mapping.get(i,{})) for i in ids]
    output = dict(planned_sources=len(ids),
        sources_with_runtime_records=sum(x["runtime_record_available"] for x in sources),
        certified_impossible_sources=0,
        original_cohort=bool(mapping), sources=sources,
        scope="Diagnostic attribution only; no automatic early rejection, timeout proof or end-to-end speed claim. Missing input remains unavailable.")
    args.out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in output.items()if k!="sources"}))
if __name__ == "__main__":
    main()
