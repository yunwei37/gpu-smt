"""Review full32 power family and update full-corpus acceptance/coverage counts."""
from pathlib import Path
import json,gzip,csv,tarfile,collections,re,shutil
from run_candidate_recovery import HERE,PAIR
from candidate_power_auto import transform
ROOT=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30")
def write(path,rows):
    with path.open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    g=ROOT/"power-family32-pair-v1";terminal=json.loads((g/"terminal.json").read_text())
    assert terminal["complete"] and terminal["completed_units"]==64
    rows=list(map(json.loads,(g/"results.jsonl").read_text().splitlines()))
    assert len(rows)==64 and len({(x["id"],x["mode"]) for x in rows})==64
    inputs={x["id"]:x for x in json.load(gzip.open(PAIR/"input7808.json.gz","rt"))["candidates"]}
    original={x["id"]:x for x in json.load(gzip.open(PAIR/"engine.stdout.gz","rt"))["results"]}
    selected={x["id"] for x in csv.DictReader((HERE/"coverage/minif2f126.csv").open()) if x["task"]=="mathd_numbertheory_296"}
    checked=[]
    for x in rows:
        c=Path(x["capture"]);receipt=json.loads((c/"receipt.json").read_text());assert receipt["retired"]
        if x["mode"]=="certificate":
            code,meta=transform(inputs[x["id"]]["code"])
            code=re.sub(r"(set_option\s+maxHeartbeats\s+)\d+",r"\g<1>200000",code)
            if not re.search(r"set_option\s+maxHeartbeats",code):code="set_option maxHeartbeats 200000\n"+code
            assert code+"\n#print axioms "+x["task"]+"\n"==(c/"source.lean").read_text()
        if x["status"]=="accepted":
            text=(c/"stdout.txt").read_text();m=re.search("'"+x["task"]+r"' depends on axioms: \[([^\]]*)\]",text)
            assert receipt["exit"]==0 and "sorryAx" not in text and m
            ax=[v.strip() for v in m[1].split(",") if v.strip()]
            assert set(ax)<={"propext","Quot.sound","Classical.choice"}
            checked.append({"id":x["id"],"mode":x["mode"],"axioms":",".join(ax),"capture":str(c)})
    pairs=[]
    for id in sorted({x["id"] for x in rows}):
        d={x["mode"]:x for x in rows if x["id"]==id}
        pairs.append({"id":id,"in_fixed8":id in selected,"historical":d["certificate"]["historical_status"],
          "original":d["original"]["status"],"certificate":d["certificate"]["status"],
          "original_wall_s":d["original"]["wall_s"],"certificate_wall_s":d["certificate"]["wall_s"],
          "hits":d["certificate"]["hits"],"errors":json.dumps(d["certificate"]["errors"])})
    oldpassed={i for i,x in original.items() if x["outcome"]["status"]=="accepted"}
    prev={x["id"] for x in csv.DictReader((HERE/"pass32-recomputed/full7808.csv").open()) if x["combined_accepted"]=="True"}
    after=set(prev)
    for x in rows:
        if x["mode"]!="certificate":continue
        if x["status"]=="accepted":after.add(x["id"])
        else:after.discard(x["id"])
    beforetasks={inputs[i]["task_id"] for i in oldpassed};tasks={inputs[i]["task_id"] for i in after}
    fixedpassed=[x["id"] for x in rows if x["mode"]=="certificate" and x["status"]=="accepted" and x["id"] in selected]
    familynew=[x["id"] for x in rows if x["mode"]=="certificate" and x["status"]=="accepted"]
    coverage=list(csv.DictReader((HERE/"coverage/minif2f126.csv").open()))
    opportunity={x["id"] for x in coverage if x["category"]=="checked_family"} | selected
    recovered=sum(x["id"] in after and x["id"] not in oldpassed for x in coverage)
    out=HERE/"power-family-result";out.mkdir(exist_ok=False)
    write(out/"paired32.csv",pairs);write(out/"checked-proofs.csv",checked)
    write(out/"full7808-after-power.csv",[{"id":i,"task":x["task_id"],"baseline_accepted":i in oldpassed,"after_power_accepted":i in after}
         for i,x in inputs.items()])
    with tarfile.open(out/"raw-native.tgz","w:gz") as t:
      caps=[Path(x["capture"]) for x in rows]
      caps += [ROOT/"captures"/name for name in ["power-certificate-build-v1","power-method-build-v1","power-control-v1-positive","power-control-v1-negative"]]
      for cap in caps:
        for n in ["source.lean","stdout.txt","stderr.txt","launch.json","receipt.json","memory.jsonl","certificate-events.txt"]:
          if (cap/n).exists():t.add(cap/n,arcname=cap.name+"/"+n)
    for name in ["terminal.json","plan.json"]:shutil.copyfile(g/name,out/name)
    with gzip.open(out/"results64.jsonl.gz","wb") as z:z.write((g/"results.jsonl").read_bytes())
    summary={"terminal":terminal,"flow":dict(collections.Counter(x["original"]+" -> "+x["certificate"] for x in pairs)),
      "family_complete_accepted":familynew,"fixed8_complete_accepted":fixedpassed,
      "native_wall_sum_s":{m:sum(x["wall_s"] for x in rows if x["mode"]==m) for m in ["original","certificate"]},
      "all7808_accepted_after_power":len(after),"solved_tasks_after_power":len(tasks),"pass32_after_power":len(tasks)/244,
      "new_tasks_vs_original":sorted(tasks-beforetasks),"total_new_accepted_vs_original":len(after-oldpassed),
      "opportunity_shapes_covered_of126":len(opportunity),
      "opportunity_shape_attempt_work_s":sum(float(x["physical_attempt_wall_s"]) for x in coverage if x["id"] in opportunity),
      "actually_recovered_of126":recovered,
      "limit":"shape/type coverage differs from recovered valid source; broad/full native point300s not rerun"}
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
