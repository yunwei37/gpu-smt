"""Fixed49-source original/certificate pair at one finite phobos-vt point."""
from pathlib import Path
import csv,gzip,json,re,time
import run_finite
from run_candidate_recovery import rewrite,classify,HERE,PAIR
from candidate_power_auto import transform
LABEL="power-family32-pair-v1"
LIB=run_finite.BUILD_ROOT/"power-certificate-v1"
def finite(source):
    source,n=re.subn(r"(set_option\s+maxHeartbeats\s+)\d+",r"\g<1>200000",source)
    return source if n else "set_option maxHeartbeats 200000\n"+source
def main():
    out=run_finite.persistent_capture_path(run_finite.CAPTURE_ROOT.parent/LABEL)
    out.mkdir(exist_ok=False);(out/"collector.py").write_bytes(Path(__file__).read_bytes())
    inputs={x["id"]:x for x in json.load(gzip.open(PAIR/"input7808.json.gz","rt"))["candidates"]}
    historical={x["id"]:x for x in json.load(gzip.open(PAIR/"engine.stdout.gz","rt"))["results"]}
    selected=[{"id":x["id"]} for x in inputs.values() if x["task_id"]=="mathd_numbertheory_296"]
    assert len(selected)==32
    (out/"plan.json").write_text(json.dumps({"ids":[x["id"] for x in selected],"modes":["original","certificate"],
      "order":"alternate which mode goes first per source","heartbeats":200000,"self_wall_s":16,
      "native_memory_MiB":8192,"jobs":1,"cpus":"8-11","M_branch_total_budget_GiB":16,
      "whole_group_max_s":1750,"module":str(LIB),
      "scope":"paired whole-source diagnostic verification on phobos, not warmed Rust/Kimina service throughput",
      "historical_point":"original48GiB4worker outcomes/costs retained byid; not used as speedup denominator",
      "setup_cost":"proof module preparation outside candidate phase, own receipts retained separately"},indent=2)+"\n")
    started=time.monotonic();count=0;abort=False
    with (out/"results.jsonl").open("w") as ledger:
      for i,row in enumerate(selected):
        for mode in (["original","certificate"] if i%2==0 else ["certificate","original"]):
          left=1750-(time.monotonic()-started)
          if left<22 or (out/"STOP").exists():abort=True;break
          x=inputs[row["id"]];family="power"
          if mode=="certificate":source,meta=transform(x["code"]);edits=meta["edits"];source=finite(source)
          else:source,edits=finite(x["code"]),[]
          source+="\n#print axioms "+x["task_id"]+"\n"
          f=out/(x["id"]+"-"+mode+".lean");f.write_text(source)
          label=LABEL+"-"+x["id"]+"-"+mode
          code=run_finite.run(f,label,wall_seconds=min(16,int(left-5)),
                              module_path=LIB if mode=="certificate" else None)
          cap=run_finite.CAPTURE_ROOT/label;stdout=(cap/"stdout.txt").read_text();stderr=(cap/"stderr.txt").read_text()
          events=(cap/"certificate-events.txt").read_text() if (cap/"certificate-events.txt").exists() else ""
          receipt=json.loads((cap/"receipt.json").read_text());status=classify(code,stdout,stderr)
          errors=[{"line":int(a),"message":b} for a,b in re.findall(r":(\d+):\d+: error: ([^\n]+)",stdout)]
          hook=min((e["line"]+1 for e in edits),default=10**9)
          record={"id":x["id"],"task":x["task_id"],"mode":mode,"family":family,"status":status,
             "wall_s":receipt["wall_s"],"cpu_s":receipt["native_cpu_seconds"],
             "sampled_peak_owned_rss_bytes":receipt["sampled_peak_owned_rss_bytes"],
             "hits":events.count("M_CERT_HIT"),"fallbacks":events.count("M_CERT_FALLBACK"),
             "unsupported":events.count("M_CERT_UNSUPPORTED"),"errors":errors,"edits":edits,
             "prefix_error_observed":bool(edits) and any(e["line"]<hook for e in errors),
             "contains_sorry":"sorryAx" in stdout,"capture":str(cap),
             "historical_status":historical[x["id"]]["outcome"]["status"],
             "historical_attempt_wall_s":sum(a["elapsed_seconds"] for a in historical[x["id"]]["attempts"])}
          ledger.write(json.dumps(record)+"\n");ledger.flush();count+=1
          print("M_PAIR",x["id"],mode,status,record["hits"],round(record["wall_s"],4),flush=True)
          if mode=="certificate" and status=="native_process_failure":abort=True;break
        if abort:break
    (out/"terminal.json").write_text(json.dumps({"complete":count==64,"completed_units":count,"planned_units":64,"group_wall_s":time.monotonic()-started,"stopped":abort})+"\n")
if __name__=="__main__":main()
