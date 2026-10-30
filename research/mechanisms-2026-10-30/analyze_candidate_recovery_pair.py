"""Analyze only a complete fixed49 paired run; do not convert partial rows into failures."""
from pathlib import Path
import argparse,collections,csv,gzip,json,re
from run_candidate_recovery import PAIR,HERE
def write(path,rows):
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def analyze(group,output):
    terminal=json.loads((group/"terminal.json").read_text())
    assert terminal["complete"] and terminal["completed_units"]==98,terminal
    rows=list(map(json.loads,(group/"results.jsonl").read_text().splitlines()))
    assert len(rows)==98 and len({(x["id"],x["mode"]) for x in rows})==98
    data={(x["id"],x["mode"]):x for x in rows};ids=json.loads((group/"plan.json").read_text())["ids"]
    for row in rows:
        cap=Path(row["capture"]);receipt=json.loads((cap/"receipt.json").read_text())
        assert receipt["retired"],row["id"]
        if row["status"]=="accepted":
            text=(cap/"stdout.txt").read_text()
            name=re.escape(row["task"])
            match=re.search("'"+name+r"' depends on axioms: \[([^\]]*)\]",text)
            ax=[] if "'"+row["task"]+"' does not depend on any axioms" in text else (
                 [x.strip() for x in match.group(1).split(",") if x.strip()] if match else ["unknown"])
            assert set(ax)<={"propext","Quot.sound","Classical.choice"},(row["id"],ax)
    paired=[]
    for id in ids:
        old,new=data[id,"original"],data[id,"certificate"]
        paired.append({"id":id,"task":new["task"],"family":new["family"],
          "historical_status":new["historical_status"],"historical_attempt_wall_s":new["historical_attempt_wall_s"],
          "original_status":old["status"],"certificate_status":new["status"],
          "original_wall_s":old["wall_s"],"certificate_wall_s":new["wall_s"],
          "original_cpu_s":old["cpu_s"],"certificate_cpu_s":new["cpu_s"],
          "observed_wall_difference_s":old["wall_s"]-new["wall_s"],
          "certificate_hits":new["hits"],"fallbacks":new["fallbacks"],"unsupported":new["unsupported"],
          "prefix_error_observed":new["prefix_error_observed"],"error_count":len(new["errors"]),
          "contains_sorry":new["contains_sorry"],
          "budget_to_accept":old["status"] in {"budget_exceeded","resource_exhausted"} and new["status"]=="accepted",
          "error_to_accept":old["status"]=="lean_error" and new["status"]=="accepted",
          "accepted_regression":old["status"]=="accepted" and new["status"]!="accepted",
          "transformed_sampled_peak_RSS_bytes":new["sampled_peak_owned_rss_bytes"]})
    output.mkdir(parents=True,exist_ok=False)
    write(output/"paired49.csv",paired)
    costs=[]
    for mode in ["original","certificate"]:
      for status in sorted({x["status"] for x in rows if x["mode"]==mode}):
        a=[x for x in rows if x["mode"]==mode and x["status"]==status]
        costs.append({"mode":mode,"status":status,"candidates":len(a),"wall_sum_s":sum(x["wall_s"] for x in a),
          "cpu_sum_s":sum(x["cpu_s"] for x in a),"max_sampled_tree_RSS_bytes":max(x["sampled_peak_owned_rss_bytes"] for x in a)})
    write(output/"costs.csv",costs)
    before={x["task"] for x in rows if x["mode"]=="original" and x["status"]=="accepted"}
    after={x["task"] for x in rows if x["mode"]=="certificate" and x["status"]=="accepted"}
    inputs={x["id"]:x for x in json.load(gzip.open(PAIR/"input7808.json.gz","rt"))["candidates"]}
    historical=json.load(gzip.open(PAIR/"engine.stdout.gz","rt"))["results"]
    historic_tasks={inputs[x["id"]]["task_id"] for x in historical if x["outcome"]["status"]=="accepted"}
    summary={"planned_sources":49,"complete_units":98,"terminal":terminal,
      "flow_counts":dict(collections.Counter(x["original_status"]+" -> "+x["certificate_status"] for x in paired)),
      "costs":costs,"new_verified_tasks_vs_selected_native":sorted(after-before),
      "new_verified_tasks_vs_historical_full":sorted(after-historic_tasks),
      "historical_full_solved_tasks":len(historic_tasks),
      "original_accepted_ids":[x["id"] for x in rows if x["mode"]=="original" and x["status"]=="accepted"],
      "certificate_accepted_ids":[x["id"] for x in rows if x["mode"]=="certificate" and x["status"]=="accepted"],
      "budget_to_accept":sum(x["budget_to_accept"] for x in paired),"error_to_accept":sum(x["error_to_accept"] for x in paired),
      "accepted_regressions":sum(x["accepted_regression"] for x in paired),
      "prefix_errors_observed":sum(x["prefix_error_observed"] for x in paired),
      "limits":"only49selected sources at finite16s/200kHB/8GiB/native1; censored outcomes not false proofs; task-family full32candidate point pending extra15"}
    (output/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    return summary
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("group",type=Path);p.add_argument("output",type=Path);a=p.parse_args()
    print(json.dumps(analyze(a.group,a.output),indent=2))
