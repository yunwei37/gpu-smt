"""Analyze original/certificate openai sample; failures and unknowns remain literal."""
from pathlib import Path
import json,csv,re,tarfile,shutil,collections,statistics
from run_openai_native import ROOT,HERE
def csvwrite(p,rows):
    if not rows:return
    with p.open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    group=ROOT/"openai-kernel-seven-v1"
    terminal=json.loads((group/"terminal.json").read_text())
    assert terminal["complete"] and terminal["units"]==30
    rows=list(map(json.loads,(group/"results.jsonl").read_text().splitlines()))
    second=ROOT/"openai-recheck-v2"
    assert json.loads((second/"terminal.json").read_text())["complete"]
    later=list(map(json.loads,(second/"results.jsonl").read_text().splitlines()))
    allrows=rows+later
    rows=[x for x in rows if not x.get("observer") and x.get("kind")!="typed45"]+later
    mainrows=[x for x in rows if "row" in x]
    assert len(mainrows)==28 and len({(x["row"],x["mode"],x["observer"]) for x in mainrows})==28
    for x in allrows:
        assert x["retired"] and not x["sampled_budget_violation"]
        if x.get("accepted"):
            stdout=(Path(x["capture"])/"stdout.txt").read_text()
            match=re.search(r"'MOpenAISample.result' depends on axioms: \[([^\]]*)\]",stdout)
            assert match and set(map(str.strip,match[1].split(",")))<={"propext","Quot.sound","Classical.choice"}
    out=HERE/"openai-kernel-sample";out.mkdir(exist_ok=False)
    paired=[]
    for row in range(7):
        d={(x["mode"],x["observer"]):x for x in mainrows if x["row"]==row}
        a,b=d["original",False],d["certificate",False]
        c,e=d["original",True],d["certificate",True]
        paired.append({"row":row,"original_pass":a["accepted"],"certificate_pass":b["accepted"],
          "original_whole_wall_s":a["wall_s"],"certificate_whole_wall_s":b["wall_s"],
          "original_whole_cpu_s":a["cpu_s"],"certificate_whole_cpu_s":b["cpu_s"],
          "whole_wall_ratio_original_over_certificate":a["wall_s"]/b["wall_s"],
          "original_extra_kernel_s":c["extra_kernel_ns"]/1e9 if c["extra_kernel_ns"] is not None else None,
          "certificate_extra_kernel_s":e["extra_kernel_ns"]/1e9 if e["extra_kernel_ns"] is not None else None,
          "original_extra_kernel_declarations":c["extra_kernel_declarations"],
          "certificate_extra_kernel_declarations":e["extra_kernel_declarations"],
          "max_sampled_owned_RSS_bytes":max(x["sampled_peak_owned_tree_RSS_bytes"] for x in d.values())})
    csvwrite(out/"paired7.csv",paired)
    kerneldecl=[{"row":x["row"],"mode":x["mode"],**d} for x in mainrows if x["observer"] for d in x["kernel_declarations"]]
    csvwrite(out/"kernel-declarations.csv",kerneldecl)
    typedfile=second/"typed-baseline.jsonl"
    typed=list(map(json.loads,typedfile.read_text().splitlines())) if typedfile.exists() else []
    completed=[x for x in typed if x["status"]=="checked"]
    starts=[x for x in typed if x["status"]=="started"]
    timings=[]
    for x in starts:
        times=[r["kernel_ns"] for r in completed if r["name"]==x["name"]]
        timings.append({"name":x["name"],"module":x["module"],"repetitions":len(times),
          "median_kernel_ns":statistics.median(times) if times else None,
          "axioms":json.dumps(x["axioms"]),"type_repr":x["type_repr"]})
    csvwrite(out/"typed-baseline.csv",timings)
    negatives=[x for x in rows if x.get("kind")=="mutated-payload"]
    summary={"terminal":terminal,"paired_goal_types":7,
      "all_plain_accepted":all(x["accepted"] for x in mainrows if not x["observer"]),
      "all_observer_accepted":all(x["accepted"] for x in mainrows if x["observer"]),
      "plain_sums":{m:{"wall_s":sum(x["wall_s"] for x in mainrows if not x["observer"] and x["mode"]==m),
                         "cpu_s":sum(x["cpu_s"] for x in mainrows if not x["observer"] and x["mode"]==m)} for m in ["original","certificate"]},
      "kernel_recheck_sums":{m:sum(x["extra_kernel_ns"] or 0 for x in mainrows if x["observer"] and x["mode"]==m)/1e9 for m in ["original","certificate"]},
      "mutated_payload_rejected":len(negatives)==1 and negatives[0]["rejected"],
      "typed_probe":next(x for x in rows if x.get("kind")=="typed45"),
      "typed_started":len(starts),"typed_checks":len(completed),"typed_status_counts":dict(collections.Counter(x["status"] for x in typed)),"typed_terminal":[x for x in typed if x["status"]=="complete"],
      "max_sampled_owned_RSS_bytes":max(x["sampled_peak_owned_tree_RSS_bytes"] for x in rows),
      "scope":"availability-biased typed45 subset of135compiled modules;7 integer row types selected, not a full1.35m typed census or representative performance estimate"}
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    shutil.copyfile(group/"plan.json",out/"plan.json")
    shutil.copyfile(group/"terminal.json",out/"terminal-v1.json")
    shutil.copyfile(second/"terminal.json",out/"terminal-v2.json")
    shutil.copyfile(second/"plan.json",out/"plan-v2.json")
    shutil.copyfile(ROOT/"openai-row-preparation-v3/payload.json",out/"payload.json")
    with tarfile.open(out/"raw-native.tgz","w:gz") as t:
        for x in allrows:
            cap=Path(x["capture"])
            for f in cap.iterdir():
                if f.is_file():t.add(f,arcname=cap.name+"/"+f.name)
        for cap in sorted((ROOT/"openai-native").glob("*preflight*")):
            for f in cap.iterdir():
                if f.is_file():t.add(f,arcname=cap.name+"/"+f.name)
        if typedfile.exists():t.add(typedfile,arcname="typed-baseline-v2.jsonl")
        if (group/"typed-baseline.jsonl").exists():t.add(group/"typed-baseline.jsonl",arcname="typed-baseline-v1.jsonl")
        cap=ROOT/"openai-native/row3-recheck-diagnose-v1"
        for f in cap.iterdir():
            if f.is_file():t.add(f,arcname=cap.name+"/"+f.name)
    (out/"results.jsonl").write_text("".join(json.dumps(x)+"\n" for x in allrows))
    print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
