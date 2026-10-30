"""Retained leader/parent RSS scope audit, not a new native throughput result."""
from pathlib import Path
import gzip,json,collections,statistics
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
POINT=ROOT/"artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z"
def read(p):
    with gzip.open(p,"rt") as f:return json.load(f)
def quant(xs):
    xs=sorted(xs)
    return {"count":len(xs),"minimum":xs[0],"median":statistics.median(xs),
        "p90":xs[int((len(xs)-1)*.9)],"p99":xs[int((len(xs)-1)*.99)],"maximum":xs[-1]} if xs else {"count":0}
def main():
    data=read(POINT/"engine.stdout.gz")
    parents=set();leader=[];ordinary=[];rows=[];missing=collections.Counter()
    for result in data["results"]:
        for i,a in enumerate(result["attempts"]):
            ready=[];rss=[]
            for e in a["backend_events"]:
                try:d=json.loads(e["detail"])
                except (ValueError,TypeError):continue
                if e["stage"]=="prepared_ready":ready.append(d);parents.add(d["parent_pid"])
                if e["stage"]=="rss_observation":rss.append(d)
            valid=[x for x in rss if x.get("kind")=="leader_kernel_high_water_rss" and "native parent wait4" in x.get("scope","")]
            if not ready:missing["no_per_attempt_prepared_ready_event"]+=1
            if not valid:missing["no_leader_high_water"]+=1
            if valid:
                v=max(x["bytes"] for x in valid)
                leader.append(v)
                if a["status"] in ["accepted","rejected"]:ordinary.append(v)
                rows.append({"id":result["id"],"attempt":i,"status":a["status"],"exclusive":a["exclusive"],
                    "leader_peak_bytes":v,"reported_attempt_peak_bytes":a["peak_rss_bytes"],
                    "parent_from_same_attempt_ready_event":ready[-1]["parent_pid"] if ready else None,"process_count":len(a["processes"]),
                    "physical_attempt_seconds":a["elapsed_seconds"]})
    observed={pid:[] for pid in parents};solo=[];unattributed=[];samples=0
    with gzip.open(POINT/"engine.stderr.gz","rt") as f:
        for line in f:
            try:d=json.loads(line)["fields"]
            except (ValueError,KeyError):continue
            if d.get("message")!="owned RSS sample":continue
            samples+=1;ps=json.loads(d["processes"])
            total=0
            for x in ps:
                total+=x["rss_bytes"];pid=x["identity"]["pid"]
                if pid in parents:observed[pid].append(x["rss_bytes"])
            if len(ps)==1 and ps[0]["identity"]["pid"] in parents:solo.append(ps[0]["rss_bytes"])
            unattributed.append(max(0,d["rss_bytes"]-total))
    parent_max=[max(v) for v in observed.values() if v]
    result={"source":str(POINT.relative_to(ROOT)),"native_executions":0,"prepared_parent_count":len(parents),
      "prepared_attempt_count":len(rows),"missing_attempt_metrics":dict(missing),
      "all_prepared_leader_peak_bytes":quant(leader),"accepted_or_rejected_prepared_leader_peak_bytes":quant(ordinary),
      "registered_parent_observed_peak_bytes":quant(parent_max),"solo_registered_parent_bytes":quant(solo),
      "rss_samples":samples,"total_minus_registered_process_RSS_bytes":quant(unattributed),
      "prepared_attempts_with_more_than_parent_plus_one_process":sum(x["process_count"]>2 for x in rows),
      "conclusions":[
       "Per-attempt aggregate peak is not the sum of marginal job footprints; a retained parent can be charged repeatedly by an independent-job reservation model.",
       "Leader wait4 high water excludes descendants and the shared parent. It is not an aggregate RSS upper bound.",
       "The residual is not attributed solely to a shared parent: it can include engine and retained/inactive owned processes.",
       "No parent discount or native-outcome parity is inferred by subtracting independently observed maxima.",
       "A corrected physical-memory/COW gain requires synchronized process ownership, active/idle state and RSS trajectories, not a per-source peak scalar."] }
    out=HERE/"retained-analysis"
    (out/"parent-rss-scope.json").write_text(json.dumps(result,indent=2)+"\n")
    with gzip.open(out/"prepared-leader-observations.jsonl.gz","wt") as f:
        for x in rows:f.write(json.dumps(x)+"\n")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
