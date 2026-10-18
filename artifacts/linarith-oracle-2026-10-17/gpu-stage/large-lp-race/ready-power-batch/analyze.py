"""Actual CPU ready-power qualification and batch/model accounting."""
from pathlib import Path
import json,gzip,collections
A=Path(__file__).resolve().parent
def rows(p):
 if not p.exists():return []
 opener=gzip.open if p.name.endswith(".gz")else open
 with opener(p,"rt")as f:return [json.loads(l)for l in f if l.strip()]
def main():
 out={"scope":"One original15source CPUqualification,8queues/fourCPU8--11/48GiB/officialomega. Powersequential/ready; no physicalGPU. Hostshared with E1074nativecontrol during acquisition. Root self-review."}
 for label in ["sequential","ready"]:
  root=A/("preflight15-"+label+"-raw");cell=root/"rep1-oracle-highs";t=json.loads((cell/"terminal.json").read_text())
  assert t["state"]=="complete"and t["attempts"]==15 and t["effective_RLIMIT_AS"]==51539607552
  resp={x["proof_id"]:x for x in rows(cell/"responses.jsonl.gz")}
  if label=="sequential":reference=resp
  out[label]={"whole_seconds":t["whole_ns"]/1e9,"counts":t["counts"],"observer_errors":t["sampling_read_errors"],
   "verdict_differences":[k for k in reference if reference[k]["outcome"]!=resp[k]["outcome"]],
   "non_message_differences":[k for k in reference if {a:b for a,b in reference[k]["response"].items()if a!="messages"}!={a:b for a,b in resp[k]["response"].items()if a!="messages"}],
   "message_only_difference_IDs":[k for k in reference if reference[k]["response"]!=resp[k]["response"]]}
  if label!="ready":continue
  groups=rows(root/"goal-batches.jsonl.gz");exchanges=rows(root/"batch-exchanges.jsonl.gz");model={};intervals=[];answers=[]
  for e in exchanges:
   request=json.loads(e["request_json"]);reply=json.loads(e["reply_json"]);assert len(request["batch"])==len(reply["batch"])
   for q,v in zip(request["batch"],reply["batch"]):
    assert q["call_id"]not in model;model[q["call_id"]]=v["exact_certificate_shape"];answers.append(v);intervals.append([v["worker_start_ns"],v["worker_end_ns"]])
  merged=[]
  for s,e in sorted(intervals):
   if merged and s<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],e)
   else:merged.append([s,e])
  union=sum(e-s for s,e in merged)/1e9
  svc=rows(root/"rep1-oracle-highs-backend/support-calls.jsonl.gz")
  joins=[x for x in svc if x.get("input",{}).get("call_id")in model and isinstance(x.get("rows"),int)]
  committed=[x for x in groups if x["outcome"]=="checked"];rolled=[x for x in groups if x["outcome"]!="checked"]
  out["batches"]={"groups":[{k:x[k]for k in ["outcome","goals","models","checked","fallback","call_ids"]}for x in groups],
   "exported_models":len(model),"committed_native_certificate_checks":sum(x["checked"]for x in committed),"committed_model_fallbacks":sum(x["fallback"]for x in committed),
   "outer_fallback_goals_NOT_source_failures":sum(x["goals"]for x in rolled),"exported_models_below_existing_row11_gate":sum(x["rows"]<11 for x in model.values()),
   "parsed_external_models_joined_to_ready_groups":len(joins),"parsed_external_shapes":[{k:x[k]for k in ["rows","cols","nnz"]}for x in joins],
   "product_elapsed_sum_seconds_NOT_CPU":sum(x["products_ns"]for x in answers)/1e9,"LP_elapsed_sum_seconds_NOT_CPU":sum(x["lp_ns"]for x in answers)/1e9,
   "ready_numeric_worker_lifetime_union_seconds":union,
   "fixed_path_all_ready_worker_intervals_zero_ratio":out["ready"]["whole_seconds"]/(out["ready"]["whole_seconds"]-union),
   "model_scope":"Delete whole1050ready-worker lifetime intervals (a superset of their numericproducts/LP), hold other observed costs/paths fixed. Does not cover scalar calls outside these groups, parser/transport/Lean checks, or alternative scheduling/representation. NOT a universal whole-GPU Amdahl bound."}
 out["sequential_over_ready_ratio"]=out["sequential"]["whole_seconds"]/out["ready"]["whole_seconds"]
 out["fidelity_qualified"]=not out["ready"]["verdict_differences"]and not out["ready"]["non_message_differences"]
 (A/"preflight-analysis.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
if __name__=="__main__":main()
