"""Recompute the full244-task pass@32 acceptance overlay, not a new full native run."""
from pathlib import Path
import json,gzip,csv,re,collections
from run_candidate_recovery import HERE,PAIR,mask_comments
from candidate_certificate_auto import transform
def main():
    source={x["id"]:x for x in json.load(gzip.open(PAIR/"input7808.json.gz","rt"))["candidates"]}
    old={x["id"]:x for x in json.load(gzip.open(PAIR/"engine.stdout.gz","rt"))["results"]}
    assert len(source)==len(old)==7808 and source.keys()==old.keys()
    groups=collections.Counter(x["task_id"] for x in source.values())
    assert len(groups)==244 and set(groups.values())=={32}
    tested=list(map(json.loads,gzip.open(HERE/"automation/native64/results128.jsonl.gz","rt").read().splitlines()))
    new={x["id"]:x for x in tested if x["mode"]=="certificate"}
    assert len(new)==64
    old_pass={i for i,x in old.items() if x["outcome"]["status"]=="accepted"}
    merged=set(old_pass);proofs=[];ledger=[]
    baseline_suspect=[];baseline_sorry_diagnostic=[]
    for i in old_pass:
        code=mask_comments(source[i]["code"])
        suspicious=re.findall(r"\b(?:sorry|admit|axiom|native_decide|run_tac|unsafe|skipKernelTC|ofReduceBool|ofReduceNat)\b",code)
        if suspicious:baseline_suspect.append({"id":i,"tokens":suspicious})
        msgs=old[i]["outcome"]["response"].get("messages",[])
        if any(re.search("sorry|axiom",m.get("data",""),re.I) for m in msgs):baseline_sorry_diagnostic.append(i)
    for i,x in source.items():
        changed,meta=transform(x["code"])
        if changed!=x["code"]:
            assert i in new,("changed but untested",i)
        if i in new and meta["route"] is not None:
            if new[i]["status"]=="accepted":
                cap=Path(new[i]["capture"]);text=(cap/"stdout.txt").read_text()
                receipt=json.loads((cap/"receipt.json").read_text())
                task=x["task_id"]
                match=re.search("'"+re.escape(task)+r"' depends on axioms: \[([^\]]*)\]",text)
                assert receipt["exit"]==0 and receipt["retired"] and "sorryAx" not in text and match
                axioms=[a.strip() for a in match[1].split(",") if a.strip()]
                assert set(axioms)<={"propext","Quot.sound","Classical.choice"}
                merged.add(i)
                proofs.append({"id":i,"task":task,"new":i not in old_pass,"axioms":",".join(axioms),
                   "native_exit":0,"capture":str(cap),"wall_s":new[i]["wall_s"]})
            else:merged.discard(i)
        ledger.append({"id":i,"task":x["task_id"],"baseline_accepted":i in old_pass,
          "rewritten":changed!=x["code"],"observed_new_native_status":new[i]["status"] if i in new else "",
          "combined_accepted":i in merged,"evidence":"new native" if meta["route"] is not None else "unchanged source historical native"})
    before={source[i]["task_id"] for i in old_pass};after={source[i]["task_id"] for i in merged}
    out=HERE/"pass32-recomputed";out.mkdir(exist_ok=False)
    def write(name,rows):
        with (out/name).open("w") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write("full7808.csv",ledger);write("checked-certificate-proofs.csv",proofs)
    tasks=[{"task":t,"new_accepted_candidates":" ".join(sorted(i for i in merged-old_pass if source[i]["task_id"]==t))} for t in sorted(after-before)]
    write("new-tasks.csv",tasks)
    summary={"total_candidates":7808,"tasks":244,"per_task":32,"baseline_accepted_candidates":len(old_pass),
      "combined_accepted_candidates":len(merged),"baseline_solved":len(before),"combined_solved":len(after),
      "baseline_pass32":len(before)/244,"combined_pass32":len(after)/244,
      "new_tasks":tasks,"lost_tasks":sorted(before-after),"lost_accepted_candidates":sorted(old_pass-merged),
      "new_complete_native_proofs":len(merged-old_pass),"new_axiom_closures":"all31 checked, allowed standard3 only, no sorry",
      "baseline_source_token_findings":baseline_suspect,"baseline_sorry_axiom_diagnostics":baseline_sorry_diagnostic,
      "baseline_axiom_scope":"retained native acceptance plus source/diagnostic audit; not a fresh transitive-axiom recheck of all3014",
      "experiment_scope":"full-corpus acceptance recomputation using unchanged historical sources and64native-tested repairs; not7808new native invocations or matched-hardware E2E throughput"}
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
