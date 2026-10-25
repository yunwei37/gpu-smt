"""Analyze byte-exact duplicate opportunity from closed native records, without running Lean."""
from pathlib import Path
import argparse, collections, csv, gzip, json

def read_jsonl(path):
    with gzip.open(path, "rt", encoding="utf8") as stream:
        return [json.loads(line) for line in stream]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--native", type=Path, required=True)
    parser.add_argument("--pairs", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args=parser.parse_args()
    source=read_jsonl(args.input)
    native={row["proof_id"]:row for row in read_jsonl(args.native)}
    with args.pairs.open() as stream:
        paired={row["source_id"]:row for row in csv.DictReader(stream)}
    assert len(source)==len(native)==len(paired)==7808
    groups=collections.defaultdict(list)
    for i,row in enumerate(source):
        assert row["index"]==i
        sid=f"minif2f-{i}"
        assert sid in native and sid in paired
        assert native[sid]["status"]==paired[sid]["off_status"]
        groups[row["code"].encode("utf8")].append(i)
    duplicates=[]
    stable={"valid","lean_error","incomplete"}
    for code,indices in groups.items():
        if len(indices)<2:
            continue
        ids=[f"minif2f-{i}" for i in indices]
        statuses=[native[sid]["status"] for sid in ids]
        spans=[float(paired[sid]["off_HTTP_seconds"]) for sid in ids]
        eligible=len(set(statuses))==1 and statuses[0] in stable
        duplicates.append(dict(ids=ids,utf8_bytes=len(code),
            status_counts=dict(collections.Counter(statuses)),
            all_observed_stable_statuses_agree=eligible,
            repeated_observed_HTTP_seconds=sum(spans[1:]),
            eligible_repeated_HTTP_seconds=sum(spans[1:]) if eligible else 0,
            first_HTTP_seconds=spans[0],
            literal_None=code==b"None"))
    total=sum(float(row["off_HTTP_seconds"]) for row in paired.values())
    eligible=sum(row["eligible_repeated_HTTP_seconds"] for row in duplicates)
    result=dict(population=len(source),distinct_exact_sources=len(groups),
        repeated_sources=len(source)-len(groups),duplicate_groups=duplicates,
        cumulative_native_HTTP_seconds=total,
        eligible_repeated_HTTP_seconds=eligible,
        eligible_repeated_HTTP_fraction=eligible/total,
        input=str(args.input),native=str(args.native),pairs=str(args.pairs),
        scope="Existing-data diagnostic only. Exact UTF8 bytes; no prefix/whitespace normalization. Repeated observed HTTP spans overlap and are not whole lifecycle savings. Frozen environment and timeout are assumed. No Lean or solver process started.",
        review="Root self-review, not independent audit.")
    args.out.mkdir(exist_ok=False)
    (args.out/"result.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="duplicate_groups"}))
if __name__=="__main__":
    main()
