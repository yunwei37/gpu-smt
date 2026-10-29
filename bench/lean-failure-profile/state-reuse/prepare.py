"""Select the complete expensive repeated-text opportunity; never reuse old parser offsets.

Retained native units were parsed in a different input coordinate system.
Only IDs/kinds/text serve selection. Original source is unchanged. A native
original-source parse must supply positions before observer insertion.
"""
import argparse
import collections
import gzip
import json
import re
from pathlib import Path

def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument("--input", type=Path, required=True)
    a.add_argument("--units", type=Path, required=True)
    a.add_argument("--corpus", choices=["minif2f", "proofnet"], required=True)
    a.add_argument("--out", type=Path, required=True)
    args = a.parse_args()
    args.out.mkdir(exist_ok=False)
    with gzip.open(args.input, "rt") as f:
        inputs = {f"{args.corpus}-{x['index']}": x for x in map(json.loads, f)}
    with gzip.open(args.units, "rt") as f:
        units = {x["proposalId"]: x for x in map(json.loads, f)
                 if x["proposalId"] in inputs}
    # Use the literal known Lean tactic kinds, not a substring cost classifier.
    wanted = {"nlinarith",
              "Mathlib.Tactic.intervalCases", "Lean.Parser.Tactic.simpAll",
              "Mathlib.Tactic.normNum"}
    actual = collections.Counter(u["syntaxKind"] for row in units.values()
                                 for u in row["units"])
    # The 4.9 parser may namespace arithmetic declarations differently; record
    # the exact retained kinds rather than guessing equivalent syntax.
    observed = {k for k in actual if any(
        k.rsplit(".", 1)[-1] == n for n in
        ["nlinarith", "intervalCases", "simpAll", "normNum"])}
    assert observed <= wanted, (wanted, observed)
    groups = collections.defaultdict(list)
    missing = []
    for source_id, row in units.items():
        if not row["eligible"]:
            continue
        source = inputs[source_id]
        match = re.search(r":=\s*by\b", source["code"])
        if not match:
            missing.append(source_id)
            continue
        task = source["index"] // 32
        statement = source["code"][:match.end()]
        for rank, unit in enumerate(row["units"]):
            if unit["syntaxKind"] in wanted:
                groups[(task, source["header"], statement,
                        unit["syntaxKind"], unit["text"])].append(
                    dict(id=source_id, rank=rank, kind=unit["syntaxKind"],
                         text=unit["text"]))
    repeated = [rows for rows in groups.values() if len(rows) > 1]
    selected = {x["id"] for group in repeated for x in group}
    candidates = [dict(id=k, task_id=f"{args.corpus}-{inputs[k]['index']//32}",
                       code=inputs[k]["code"], reuse=False)
                  for k in sorted(selected, key=lambda s: inputs[s]["index"])]
    for name, value in [
        ("original.json.gz", dict(mode="all", candidates=candidates)),
        ("repeated-text-groups.json.gz", repeated),
    ]:
        (args.out/name).write_bytes(gzip.compress(
            (json.dumps(value, ensure_ascii=False)+"\n").encode(), mtime=0))
    result = dict(corpus=args.corpus, original_population=len(inputs),
        repeated_text_groups=len(repeated), selected_sources=len(candidates),
        repeated_text_occurrences=sum(map(len, repeated)),
        maximum_text_reuse_occurrences=sum(len(g)-1 for g in repeated),
        exact_native_kinds=sorted(wanted),
        native_kind_counts={k: actual[k] for k in sorted(observed)},
        unsupported_missing_delimiter=missing, original_source_bytes_unchanged=True,
        parser_coordinate_scope="Old spans must not index original source.",
        actual_native_candidate_executions=0, complete_state_hits=None,
        native_failure_reuse_seconds=None, replay_qualified=False)
    (args.out/"preparation.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k != "unsupported_missing_delimiter"}))

if __name__ == "__main__":
    main()
