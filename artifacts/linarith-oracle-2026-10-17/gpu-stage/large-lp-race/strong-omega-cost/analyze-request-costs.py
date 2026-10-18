"""Full E1071 success/fallback and native-ranked numeric tails; no rerun."""
from pathlib import Path
import json,collections,importlib.util,os,resource,math
A=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location("numeric",A/"analyze-numeric-phases.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def dist(xs):
 xs=sorted(xs)
 return {"n":len(xs),"min":min(xs),"p50":xs[math.ceil(len(xs)*.5)-1],"p90":xs[math.ceil(len(xs)*.9)-1],"p99":xs[math.ceil(len(xs)*.99)-1],"max":max(xs)}if xs else {"n":0}
def main():
 os.sched_setaffinity(0,{12,13,14,15});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
 numeric=json.loads((A/"full1000-numeric-analysis.json").read_text());calls=numeric["per_call_completed_exclusive_CPU_ns"]
 native=json.loads((A/"full1000-native-phase-analysis.json").read_text())["per_candidate"]
 inputpath=A.parents[2]/"input-top1000.jsonl"
 # Strong-omega-cost is under gpu-stage/large-lp-race; parent[2] is experiment root.
 inputs=[json.loads(line)for line in inputpath.read_text().splitlines()]
 header="import Mathlib\nimport Aesop\n";source_id={"\n\n"+x["code"][len(header):]:x["proof_id"]for x in inputs}
 result={"scope":"Completed exclusive CPU and completed solver wall only; unknown killed work stays separately bounded in complete-budget. Summed solver wall is not whole verification wall. Tail IDs fixed by native service rank; no causal wall-fraction claim.","methods":{}}
 for method in ["native","direct"]:
  cell=A/"full1000-raw"/method/"rep1-oracle-highs";metadata={};group=collections.defaultdict(collections.Counter);counts=collections.Counter()
  for x in m.rows(cell/"lean-costs.jsonl.gz"):
   if x.get("ty")not in ["cost-native-roundtrip","cost-direct-roundtrip"]:continue
   ci=x["call_id"];pid=source_id.get(x["source"]);assert pid is not None
   outcome=("direct"if x["ty"]=="cost-direct-roundtrip"else"native")+("_certificate"if x["answer"].get("cert")is not None else"_no_certificate_or_error")
   metadata[ci]=(pid,outcome);counts[outcome]+=1
   group[outcome].update({k:v/1e9 for k,v in calls.get(str(ci),{}).items()})
  events=list(m.rows(cell.parent/"numeric-phases.jsonl"));completed,opened,errors=m.exclusive(events);assert not errors
  walls=collections.defaultdict(collections.Counter)
  for x in completed:
   if x["call_id"]in metadata:
    walls[metadata[x["call_id"]][1]][x["stage"]]+=(x["end_ns"]-x["start_ns"])/1e9
  service=list(m.rows(cell.parent/(cell.name+"-backend")/"support-calls.jsonl.gz"))
  shape={k:dist([x[k]for x in service if isinstance(x.get(k),(int,float))])for k in ["rows","cols","nnz"]}
  known=[x for x in service if isinstance(x.get("rows"),int)];edges=[]
  for x in known:
   ci=x.get("input",{}).get("call_id")
   if ci not in metadata:continue
   pid=metadata[ci][0];edges.extend([(x["start_ns"],1,pid),(x["end_ns"],-1,pid)])
  active=collections.Counter();last=None;overlap=0;peak=0
  for t,d,pid in sorted(edges):
   if last is not None and len(active)>1:overlap+=t-last
   active[pid]+=d
   if active[pid]==0:del active[pid]
   peak=max(peak,len(active));last=t
  tails={}
  for n in [10,100]:
   ids={x["proof_id"]for x in sorted(native,key=lambda x:-x["service_seconds"])[:n]};cpu=collections.Counter()
   for ci,(pid,outcome) in metadata.items():
    if pid in ids:cpu.update({k:v/1e9 for k,v in calls.get(str(ci),{}).items()})
   tails[str(n)]={"completed_numeric_exclusive_CPU_seconds":dict(cpu)}
  result["methods"][method]={"request_counts":dict(counts),"completed_exclusive_CPU_seconds_by_request_result":{k:dict(v)for k,v in group.items()},
   "completed_scope_wall_seconds_NONADDITIVE_by_request_result":{k:dict(v)for k,v in walls.items()},
   "actual_external_parsed_model_shapes":shape,"external_records":len(service),"parsed_model_records":len(known),
   "cross_candidate_parsed_service_overlap_seconds":overlap/1e9,"peak_distinct_candidates_with_parsed_service_requests":peak,
   "overlap_warning":"Lifetime includes build/queue/solve/extract; does not establish simultaneously GPU-ready LPs.",
   "native_ranked_matched_tails":tails}
 (A/"full1000-request-costs.json").write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps({k:{"requests":v["request_counts"],"shapes":v["actual_external_parsed_model_shapes"],"overlap_s":v["cross_candidate_parsed_service_overlap_seconds"]}for k,v in result["methods"].items()},indent=2))
if __name__=="__main__":main()
