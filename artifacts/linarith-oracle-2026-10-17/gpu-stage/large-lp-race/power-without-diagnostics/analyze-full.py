"""Read the actual completed reduced-diagnostic native/direct pair, including failures."""
from pathlib import Path
import collections,gzip,json,math
A=Path(__file__).resolve().parent
def rows(p,strict=True):
 if not p.exists()and p.with_name(p.name+".gz").exists():p=p.with_name(p.name+".gz")
 if not p.exists():return[],[]
 good=[];bad=[]
 with(gzip.open(p,"rt")if p.suffix==".gz"else p.open())as f:
  for i,line in enumerate(f,1):
   if not line.strip():continue
   try:good.append(json.loads(line))
   except json.JSONDecodeError as e:
    if strict:raise
    bad.append({"line":i,"error":str(e)})
 return good,bad
def dist(xs):
 xs=sorted(xs)
 return{"n":len(xs),**{k:xs[max(0,math.ceil(q*len(xs))-1)]for k,q in[("p50",.5),("p90",.9),("p99",.99),("max",1)]}}if xs else{"n":0}
def main():
 inputs,_=rows(A.parents[2]/"input-top1000.jsonl")
 header="import Mathlib\nimport Aesop\n"
 mapping={"\n\n"+x["code"][len(header):]:x["proof_id"]for x in inputs};assert len(mapping)==1000
 result={"state":"partial","scope":"Original1000 arithmetic-heavy cohort, native Fast/hybrid versus direct natural powers; reduced Lean diagnostic operations, fixed numerical binaries, native omega,8queues/fourCPU8--11/48GiB. Optional process-tree observer off in both; remaining RPC/candidate/omega/backend recording charged. One shared-host fixed-order pair, not wholly uninstrumented/globalCPU/GPU/OSDI evidence. Root self-review only.","conditions":{}}
 responses={};times={}
 for label,method in[("native","fast-hybrid"),("power","oracle-highs")]:
  root=A/"full1000"/label;cell=root/("rep1-"+method)
  if not(cell/"terminal.json").exists():continue
  term=json.loads((cell/"terminal.json").read_text())
  if term["state"]!="complete":result["conditions"][label]={"terminal":term};continue
  assert term["attempts"]==1000 and term["effective_RLIMIT_AS"]==51539607552 and term["resource_observer_enabled"]is False
  data,_=rows(cell/"responses.jsonl.gz");rs={x["proof_id"]:x for x in data};assert len(data)==len(rs)==1000
  assert dict(collections.Counter(x["outcome"]for x in data))==term["counts"]
  responses[label]=rs
  spans,_=rows(cell/"candidate-times.jsonl");tm=collections.defaultdict(list)
  for x in spans:
   assert x["source"]in mapping
   tm[mapping[x["source"]]].append((x["end_ns"]-x["start_ns"])/1e9)
  assert len(tm)==1000 and all(len(x)==1 for x in tm.values())
  times[label]={k:v[0]for k,v in tm.items()}
  race,bad=rows(cell/"lp-races.jsonl",False);children=[];seen=set()
  for x in race:
   for role in["cpu","gpu","strong_cpu"]:
    e=x.get(role+"_exit")
    if not isinstance(e,dict):continue
    assert e["pid"]not in seen;seen.add(e["pid"])
    assert not e.get("wait_error")and not e.get("kill_error")
    children.append({"role":role,"cancelled":e["signal"]is not None,"CPU_seconds":(e["wait4_user_cpu_ns"]+e["wait4_system_cpu_ns"])/1e9})
  external,bad_external=rows(root/(cell.name+"-backend")/"support-calls.jsonl.gz",False)
  models=[x for x in external if isinstance(x.get("rows"),int)]
  phases,bad_phases=rows(root/(cell.name+"-backend")/"support-calls.jsonl.gz.phases",False)
  ended=[x for x in phases if x.get("event")=="process_retired"]
  result["conditions"][label]={"terminal":term,"source_service_seconds":times[label],"service_span_quantiles_seconds":dist(list(times[label].values())),"numeric_races":len(race),"race_parse_errors":bad,"race_winners_legacy":dict(collections.Counter(x["winner"]for x in race)),"numeric_reaped_children":len(children),"numeric_reaped_CPU_seconds":sum(x["CPU_seconds"]for x in children),"cancelled_numeric_children":sum(x["cancelled"]for x in children),"cancelled_numeric_CPU_seconds":sum(x["CPU_seconds"]for x in children if x["cancelled"]),"parsed_external_models":len(models),"external_shapes":{k:dist([x[k]for x in models])for k in["rows","cols","nnz"]},"external_parse_errors":bad_external,"phase_parse_errors":bad_phases,"external_service_CPU_seconds":sum(x["process_user_seconds"]+x["process_system_seconds"]for x in ended)if ended else None,"accounting_limit":"No external records for native is unprofiled, not zero LP work. Legacy gpu race label means CPU HiGHS in these cells. Reaped child CPU includes cancelled work and overlaps numerical phases; summed candidate spans overlap. No pure-LP wall fraction or universal GPU bound is derived."}
 if set(responses)=={"native","power"}:
  result["state"]="complete";ref=responses["native"];out=responses["power"];assert ref.keys()==out.keys()
  result["fidelity"]={"verdict_differences":[k for k in ref if ref[k]["outcome"]!=out[k]["outcome"]],"non_message_differences":[k for k in ref if {a:b for a,b in ref[k]["response"].items()if a!="messages"}!={a:b for a,b in out[k]["response"].items()if a!="messages"}],"message_only_difference_IDs":[k for k in ref if ref[k]["response"]!=out[k]["response"]]}
  result["fidelity_qualified"]=not result["fidelity"]["verdict_differences"]and not result["fidelity"]["non_message_differences"]
  if result["fidelity_qualified"]:
   result["native_over_power"]=result["conditions"]["native"]["terminal"]["whole_ns"]/result["conditions"]["power"]["terminal"]["whole_ns"]
  first=json.loads((A.parent/"power-export/full1000-result.json").read_text())
  ranked=sorted(times["native"],key=lambda k:-times["native"][k])
  result["matched_tails"]={}
  for n in[10,100]:
   for name,ids in[("current-native-ranked",ranked[:n]),("fixed-E1074-native-ranked",first["native_ranked_matched_tails"][str(n)]["proof_ids"])]:
    result["matched_tails"][name+"-"+str(n)]={"proof_ids":ids,"summed_service_seconds":{label:sum(tm[k]for k in ids)for label,tm in times.items()},"meaning":"same IDs in both modes; overlapping service spans, not whole wall or CPU"}
 if set(times)=={"native","power"}:
  previous=json.loads((A.parent/"power-whole-repetitions/service-span-analysis.json").read_text())
  prior_common=[x["proof_id"]for x in previous["same_source_slower_in_all_three_observations"]]
  assert len(prior_common)==len(set(prior_common))and set(prior_common)<=set(times["native"])
  slower=sorted((k for k in times["native"]if times["power"][k]>times["native"][k]),key=lambda k:-(times["power"][k]-times["native"][k]))
  result["observed_candidate_regressions"]={
    "current_slower_sources":[{"proof_id":k,"native_seconds":times["native"][k],"power_seconds":times["power"][k]}for k in slower],
    "current_slower_count":len(slower),
    "prior_common_count":len(prior_common),
    "prior_common_still_slower_IDs":[k for k in prior_common if k in slower],
    "scope":"All original1000 including rejected candidates. Source service spans include scheduling/waiting. Prior three observations use another affinity and diagnostic build; direction consistency by source ID is descriptive, not a causal diagnostic-overhead ablation, isolated CPU cost, new independent repetition or per-candidate guarantee."}
 p=A/("full1000-result.json"if result["state"]=="complete"else"full1000-partial-result.json")
 p.write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps({"state":result["state"],"conditions":{k:{"whole_seconds":v["terminal"]["whole_ns"]/1e9,"counts":v["terminal"]["counts"]}for k,v in result["conditions"].items()},"native_over_power":result.get("native_over_power"),"fidelity":{k:len(v)for k,v in result.get("fidelity",{}).items()},"matched_tails":result.get("matched_tails")},indent=2))
if __name__=="__main__":main()
