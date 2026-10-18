"""Normal original1000 paired result reader. Partial cells never become final ratios."""
from pathlib import Path
import json,gzip,collections,math
A=Path(__file__).resolve().parent
CONDITIONS={"power":"oracle-highs","direct":"oracle-highs","native-dual":"oracle-highs","stock-native":"fast-hybrid"}
def rows(p):
 if not p.exists():return []
 opener=gzip.open if p.name.endswith(".gz")else open
 with opener(p,"rt")as f:return [json.loads(l)for l in f if l.strip()]
def dist(xs):
 xs=sorted(xs)
 return {"n":len(xs),"min":xs[0],"p50":xs[math.ceil(.5*len(xs))-1],"p90":xs[math.ceil(.9*len(xs))-1],"p99":xs[math.ceil(.99*len(xs))-1],"max":xs[-1]}if xs else {"n":0}
def main():
 inputs=rows(A.parents[2]/"input-top1000.jsonl")
 header="import Mathlib\nimport Aesop\n";source_id={"\n\n"+x["code"][len(header):]:x["proof_id"]for x in inputs};assert len(source_id)==1000
 result={"state":"partial","scope":"Original1000 same8queues/fourCPU4--7/48GiB/officialomega normal fixed-order block. Stock-native is upstream Fast/hybrid; native-dual already contains our numerical oracle and is a component control. Legacy race gpu winner is CPU HiGHS, not device work. One block, not confidence/globalCPUoptimality/OSDIreadiness. Root self-review only.","methods":{}}
 responses={};timings={}
 for name,method in CONDITIONS.items():
  root=A/"full1000-raw"/name;cell=root/("rep1-"+method)
  if not(cell/"terminal.json").exists():continue
  t=json.loads((cell/"terminal.json").read_text());assert t["state"]=="complete"and t["attempts"]==1000 and t["effective_RLIMIT_AS"]==51539607552
  rs={x["proof_id"]:x for x in rows(cell/"responses.jsonl.gz")};assert len(rs)==1000;responses[name]=rs
  times={}
  for x in rows(cell/"candidate-times.jsonl"):
   pid=source_id.get(x["source"]);assert pid is not None
   times.setdefault(pid,[]).append((x["end_ns"]-x["start_ns"])/1e9)
  assert len(times)==1000 and all(len(v)==1 for v in times.values())
  timings[name]={k:v[0]for k,v in times.items()}
  races=rows(cell/"lp-races.jsonl")
  worker=[];seen=set()
  for race in races:
   for role in ["cpu","gpu","strong_cpu"]:
    q=race.get(role+"_exit")
    if not isinstance(q,dict):continue
    assert q["pid"]not in seen;seen.add(q["pid"])
    assert not q.get("wait_error")and not q.get("kill_error")
    worker.append({"role":role,"cancelled":q["signal"]is not None,"CPU_seconds":(q["wait4_user_cpu_ns"]+q["wait4_system_cpu_ns"])/1e9})
  models=rows(root/(cell.name+"-backend")/"support-calls.jsonl.gz")
  parsed=[x for x in models if isinstance(x.get("rows"),int)]
  phase_records=rows(root/(cell.name+"-backend")/"support-calls.jsonl.gz.phases.gz")
  retirements=[x for x in phase_records if x.get("event")=="process_retired"]
  serviceCPU=sum(x["process_user_seconds"]+x["process_system_seconds"]for x in retirements)if retirements else None
  request_source={x["call_id"]:x["source"]for x in races}
  edges=[];missing=0
  for x in parsed:
   ci=x.get("input",{}).get("call_id")
   if ci not in request_source:missing+=1;continue
   source=request_source[ci];edges.extend([(x["start_ns"],1,source),(x["end_ns"],-1,source)])
  active=collections.Counter();previous=None;overlap=0;peak=0
  for stamp,delta,source in sorted(edges):
   if previous is not None and len(active)>1:overlap+=stamp-previous
   active[source]+=delta
   if active[source]==0:del active[source]
   peak=max(peak,len(active));previous=stamp
  result["methods"][name]={"whole_seconds":t["whole_ns"]/1e9,"counts":t["counts"],"observer_read_errors":t["sampling_read_errors"],"cpu":t["cpu"],"numeric_races_observed":len(races),"race_winners_legacy":dict(collections.Counter(x["winner"]for x in races)),
   "reaped_numeric_children":len(worker),"cancelled_numeric_children":sum(x["cancelled"]for x in worker),
   "numeric_child_total_CPU_seconds":sum(x["CPU_seconds"]for x in worker),"cancelled_numeric_child_CPU_seconds":sum(x["CPU_seconds"]for x in worker if x["cancelled"]),
   "external_records":len(models),"actual_parsed_external_models":len(parsed),"actual_external_shapes":{k:dist([x[k]for x in parsed])for k in ["rows","cols","nnz"]},
   "external_service_process_CPU_seconds":serviceCPU,
   "parsed_models_missing_source_join":missing,"cross_candidate_parsed_service_overlap_seconds":overlap/1e9,
   "peak_distinct_candidates_with_parsed_service":peak,
   "GPU_supply_scope":"Actual parsed service lifetimes include building/queueing/solving/extracting, not simultaneouslyGPU-ready work. AST products/Lean proof work are not separated by this normal capture; do not claim a complete pure-LP Amdahl bound.",
   "source_service_seconds":timings[name],
   "numeric_scope":"No numeric records in stock-native is unprofiled upstream path, not zero CPU. Child totals overlap solver/repair and include killed work; serviceCPU is separate. Candidate-service spans overlap and do not sum to whole elapsed."}
 if set(result["methods"])==set(CONDITIONS):
  result["state"]="complete";base=responses["stock-native"];result["fidelity"]={}
  for name,rs in responses.items():
   assert rs.keys()==base.keys()
   result["fidelity"][name]={"verdict_differences":[k for k in base if base[k]["outcome"]!=rs[k]["outcome"]],
    "non_message_differences":[k for k in base if {a:b for a,b in base[k]["response"].items()if a!="messages"}!={a:b for a,b in rs[k]["response"].items()if a!="messages"}],
    "message_only_difference_IDs":[k for k in base if base[k]["response"]!=rs[k]["response"]]}
  result["reference_ratios"]={name:result["methods"][name]["whole_seconds"]/result["methods"]["power"]["whole_seconds"]for name in ["stock-native","native-dual","direct"]}
  tails={}
  ranked=sorted(timings["stock-native"],key=lambda k:-timings["stock-native"][k])
  for n in [10,100]:
   ids=ranked[:n];tails[str(n)]={"rank":"same stock-native source IDs, service spans NOT whole clock","proof_ids":ids,"summed_service_seconds":{name:sum(timings[name][k]for k in ids)for name in CONDITIONS}}
  result["native_ranked_matched_tails"]=tails
 out=A/("full1000-result.json"if result["state"]=="complete"else"full1000-partial-result.json")
 out.write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps({"state":result["state"],"methods":{k:{q:v for q,v in x.items()if q!="source_service_seconds"}for k,x in result["methods"].items()},"reference_ratios":result.get("reference_ratios"),"fidelity":{k:{q:(len(v)if isinstance(v,list)else v)for q,v in x.items()}for k,x in result.get("fidelity",{}).items()}},indent=2))
if __name__=="__main__":main()
