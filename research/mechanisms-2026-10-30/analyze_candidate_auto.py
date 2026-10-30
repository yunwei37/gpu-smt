"""Full released-source routing and two-family native extension audit."""
from pathlib import Path
import json,gzip,csv,collections,tarfile,re,shutil
from run_candidate_recovery import HERE,PAIR
from candidate_certificate_auto import transform
ROOT=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30")
def main():
    inputs={x["id"]:x for x in json.load(gzip.open(PAIR/"input7808.json.gz","rt"))["candidates"]}
    first=ROOT/"candidate-recovery49-pair-v3";extra=ROOT/"candidate-auto-extra15-pair-v1"
    assert json.loads((first/"terminal.json").read_text())["complete"]
    assert json.loads((extra/"terminal.json").read_text())["complete"]
    rows=[]
    for g in [first,extra]:
        rows.extend(map(json.loads,(g/"results.jsonl").read_text().splitlines()))
    assert len(rows)==128 and len({(x["id"],x["mode"]) for x in rows})==128
    for row in rows:
        if row["mode"]!="certificate":continue
        s,meta=transform(inputs[row["id"]]["code"])
        s=re.sub(r"(set_option\s+maxHeartbeats\s+)\d+",r"\g<1>200000",s)
        if not re.search(r"set_option\s+maxHeartbeats",s):s="set_option maxHeartbeats 200000\n"+s
        expected=s+"\n#print axioms "+row["task"]+"\n"
        assert expected==(Path(row["capture"])/"source.lean").read_text(),row["id"]
        assert json.loads((Path(row["capture"])/"receipt.json").read_text())["retired"]
    controls=json.loads((ROOT/"candidate-auto-controls-v2/results.json").read_text())
    assert controls["source_mapped_diagnostics_equal"]
    out=HERE/"automation/native64";out.mkdir(exist_ok=False)
    with gzip.open(out/"results128.jsonl.gz","wt") as z:
        for x in rows:z.write(json.dumps(x)+"\n")
    extra_rows=list(map(json.loads,(extra/"results.jsonl").read_text().splitlines()))
    with tarfile.open(out/"extra-controls-raw.tgz","w:gz") as t:
        for row in extra_rows+controls["records"]:
            cap=Path(row["capture"])
            for n in ["source.lean","stdout.txt","stderr.txt","launch.json","receipt.json","memory.jsonl","certificate-events.txt"]:
                if (cap/n).exists():t.add(cap/n,arcname=cap.name+"/"+n)
    for name in ["terminal.json","plan.json"]:shutil.copyfile(extra/name,out/("extra-"+name))
    (out/"controls.json").write_text(json.dumps(controls,indent=2)+"\n")
    pairs=[]
    for id in sorted({x["id"] for x in rows},key=lambda s:int(s.split("-")[-1])):
        d={x["mode"]:x for x in rows if x["id"]==id};a,b=d["original"],d["certificate"]
        pairs.append({"id":id,"task":b["task"],"original":a["status"],"certificate":b["status"],
          "original_wall_s":a["wall_s"],"certificate_wall_s":b["wall_s"],"hits":b["hits"],"fallbacks":b["fallbacks"],
          "source_supported":transform(inputs[id]["code"])[1]["route"] is not None})
    with (out/"paired64.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
    summary={"candidate_sources":64,"native_invocations":128,"source_identity_after_auto_routing":"all64 byte-identical to native-tested certificate source",
      "flow":dict(collections.Counter(x["original"]+" -> "+x["certificate"] for x in pairs)),
      "mode_wall_sum_s":{m:sum(x["wall_s"] for x in rows if x["mode"]==m) for m in ["original","certificate"]},
      "typed_runtime_guard_controls":"2 adversarial sources each original/certificate;0 accepted; source-mapped diagnostics equal",
      "malformed_source_id":"minif2f-7206 literal None, unsupported, native rejected",
      "scope":"two hand-proved parameter families, automatic source routing/tactic replacement, native type guard; not arbitrary computation extraction or production acceptance parity"}
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
