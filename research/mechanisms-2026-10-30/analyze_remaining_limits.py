"""Summarize genuine4-source C timing separately from changed-source ablations."""
from pathlib import Path
import json,csv,tarfile,shutil
HERE=Path(__file__).resolve().parent
ROOT=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30")
def main():
    g=ROOT/"remaining-four-c-diagnostic-v1"
    assert json.loads((g/"terminal.json").read_text())["complete"]
    rows=json.loads((g/"results.json").read_text())
    a=ROOT/"remaining-four-ablation-v1";b=ROOT/"remaining3683-composition-v1"
    assert json.loads((a/"terminal.json").read_text())["complete"]
    assert json.loads((b/"terminal.json").read_text())["complete"]
    ablations=json.loads((a/"results.json").read_text())+json.loads((b/"results.json").read_text())
    diagnoses={
      "minif2f-3683":"timeout inside original kernel declaration check after all tactic calls returned; source card_filter expansion triggers expensive proof composition/conversion",
      "minif2f-3698":"prefix simp heartbeat exhaustion, certificate later constructed after error recovery but full source rejected",
      "minif2f-3703":"generic bridge attempt fails, then original rfl/eqRefl fallback still running at wall timer",
      "minif2f-3710":"maximum recursion in bridge matching after source card_filter expansion; prefix omega also fails"}
    out=HERE/"remaining-four-result";out.mkdir(exist_ok=False)
    table=[]
    for row in rows:
        assert row["status"]==row["prior_status"] and row["diagnostic_text_equal"] and row["receipt"]["retired"]
        table.append({"id":row["id"],"unchanged_native_status":row["status"],
          "observed_wall_s":row["receipt"]["wall_s"],"C_events":row["trace_records"],
          "diagnostics_equal":row["diagnostic_text_equal"],
          "last_open_C_stack":">".join(f["category"]+":"+f["kind"] for f in row["open_frames"]),
          "diagnosis":diagnoses[row["id"]]})
    with (out/"four.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(table[0]));w.writeheader();w.writerows(table)
    (out/"native-C-summary.json").write_text(json.dumps(rows,indent=2)+"\n")
    (out/"ablation-summary.json").write_text(json.dumps(ablations,indent=2)+"\n")
    direct=next(x for x in ablations if x.get("variant")=="direct-core")
    raw=list(map(json.loads,(Path(direct["capture"])/"tactics.jsonl").read_text().splitlines()))
    entries={x["id"]:x for x in raw if x["event"]=="enter"}
    exits={x["id"]:x for x in raw if x["event"]=="exit"}
    kernel=[(exits[i]["cpu_ns"]-x["cpu_ns"])/1e9 for i,x in entries.items()
            if x["category"]=="type checking" and i in exits]
    (out/"direct-core-check.json").write_text(json.dumps({"whole_wall_s":direct["receipt"]["wall_s"],
       "completed_kernel_check_CPU_s":kernel,
       "limits":"whole-source direct application imports differ; no whole-source speedup comparison; direct control replaces entire source body and is not counted as a recovered candidate"},indent=2)+"\n")
    caps=[Path(x["capture"]) for x in rows+ablations]+[ROOT/"captures/remaining-c-positive-v1"]
    with tarfile.open(out/"raw-native.tgz","w:gz") as t:
      for cap in caps:
        for f in cap.iterdir():
          if f.is_file():t.add(f,arcname=cap.name+"/"+f.name)
      for base in [g,a,b]:
        for f in base.iterdir():
          if f.is_file():t.add(f,arcname=base.name+"/"+f.name)
      build=ROOT/"generated/remaining-wrapped-cli-v1"
      for f in build.iterdir():
        if f.suffix in {".json",".jsonl",".log"}:t.add(f,arcname="link-build/"+f.name)
    print("direct kernel seconds",kernel)
    print(json.dumps(table,indent=2))
if __name__=="__main__":main()
