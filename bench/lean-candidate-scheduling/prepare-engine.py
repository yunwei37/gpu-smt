"""Preserve the original miniF2F population in the Rust engine's Batch API."""
from pathlib import Path
import argparse,gzip,json,re
from analyze import strip_comments

def rows(path):
    with gzip.open(path,"rt",encoding="utf8") as stream:
        return [json.loads(line) for line in stream]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,required=True)
    parser.add_argument("--task-metadata",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    sources=rows(args.input);metadata=rows(args.task_metadata)
    names={}
    for task in metadata:
        if task["dataset"]=="minif2f":
            name=re.findall(r"^\s*theorem\s+([^\s(:]+)",strip_comments(task["statement"]),re.M)
            assert len(name)==1
            names[task["task"]]=name[0]
    assert len(sources)==7808 and len(names)==244
    candidates=[]
    for index,item in enumerate(sources):
        assert item["index"]==index
        name=names[index//32];code=item["code"]
        declarations=re.findall(r"^\s*theorem\s+([^\s(:]+)",strip_comments(code),re.M)
        assert declarations==[name] or (not declarations and code.strip()=="None")
        candidates.append(dict(id=f"minif2f-{index}",task_id=name,code=code,
            timeout_ms=300000,reuse=False))
    args.out.mkdir(exist_ok=False)
    for mode in ["all","first_success"]:
        with gzip.open(args.out/(mode+".json.gz"),"xt",encoding="utf8") as stream:
            json.dump(dict(mode=mode,candidates=candidates),stream,ensure_ascii=False)
            stream.write("\n")
    (args.out/"README.md").write_text("""# Prepared engine population inputs

Original7,808sources and244task identities, validated against native theorem
declarations and existing producer metadata. All18literalNone errors remain.
Every original UTF8source is retained without header rewriting or normalization.
300s timeout, reuse=false, same candidate IDs/order. all and first_success
differ only in consumer mode. Full gzip objects feed gpu-smt measure through
stdin; they are not JSONL. This preparation executes no Lean, model or solver.

These are prepared inputs, not an executed new-resource or COW result.
Do not start another native collection while the retained original group is live.
Record exact binary/project pin and controller/JSONL/resource logs when running.
""")
    print(json.dumps(dict(candidates=len(candidates),tasks=len(names),
        modes=["all","first_success"],source_changed=False,new_native_run=False)))
if __name__=="__main__":
    main()
