"""Reproduce E1071 budgets, matched native-ranked tails, and checked-negative attribution.
No new experiment. CPU capacity and fixed-lane models are conditional diagnostic models.
"""
from pathlib import Path
import collections,json,importlib.util,os,resource
A=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location("numeric",A/"analyze-numeric-phases.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def dump(name,j): (A/name).write_text(json.dumps(j,indent=2)+"\n")
def negative_fallbacks():
 cell=A/"full1000-raw/direct/rep1-oracle-highs"
 negative={x["call_id"] for x in m.rows(cell/"lp-races.jsonl") if x["winner"]=="external-infeasible"}
 latest={};active={};groups=collections.defaultdict(list);query={};nqueries=0;nfallback=0
 for x in m.rows(cell/"lean-costs.jsonl.gz"):
  source=x.get("source");ty=x.get("ty")
  if not source:continue
  if ty=="cost-direct-roundtrip":
   nqueries+=1;ci=x["call_id"];latest[source]=ci;active[source]=None;query[ci]=x
  elif ty=="direct-oracle-fallback":
   ci=latest.pop(source,None);active[source]=ci
   if ci is not None:nfallback+=1
  elif ty=="direct-oracle":
   latest.pop(source,None);active[source]=None
  elif ty=="cost-stage" and active.get(source) is not None:
   groups[active[source]].append(x)
 out=[];ambiguous=0;totals=collections.Counter()
 for ci,stages in groups.items():
  if ci not in negative:continue
  valid=[x for x in stages if x["start_ns"]>=query[ci]["end_ns"]]
  ambiguous+=len(stages)-len(valid);values=collections.Counter()
  for x in valid:
   contained=[y for y in valid if y is not x and x["start_ns"]<=y["start_ns"] and y["end_ns"]<=x["end_ns"]]
   immediate=[y for y in contained if not any(z is not y and z["start_ns"]<=y["start_ns"] and y["end_ns"]<=z["end_ns"] for z in contained)]
   ns=x["cpu_ns"]-sum(y["cpu_ns"]for y in immediate)
   assert ns>=0
   values[x["stage"]]+=ns/1e9
  totals.update(values);out.append({"call_id":ci,"negative":True,"exclusive_Lean_CPU_seconds":dict(values)})
 result={"scope":"Root self-review. Captured external-infeasible labels follow exact dual-ray checking in the coordinator; not infeasibility of the Lean theorem. Raw dual witnesses have not been independently replayed. Attribution follows one consumed direct request per fallback and subtracts nested stage timers; unsupported pre-query fallback resets attribution.",
 "direct_requests":nqueries,"direct_recorded_fallbacks_with_query":nfallback,
 "checked_negative_direct_failures":sum(ci in negative and q["answer"].get("cert")is None for ci,q in query.items()),
 "checked_negative_failures_with_attributed_stages":len(out),"ambiguous_excluded_stage_intervals":ambiguous,
 "attributed_Lean_CPU_seconds":dict(totals),"fallbacks":out}
 dump("checked-negative-fallback-analysis.json",result);return result
def main():
 os.sched_setaffinity(0,{12,13,14,15});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
 numeric=json.loads((A/"full1000-numeric-analysis.json").read_text())
 phases={method:json.loads((A/("full1000-"+method+"-phase-analysis.json")).read_text()) for method in ["native","direct"]}
 neg=negative_fallbacks();result={"scope":"Same-dual-backend native-frontend vs direct-frontend diagnostic, official omega on both, four CPU/eight queues. Native reference already includes our numerical oracle: a component control, not the original stock/native whole-system criterion. No GPU measurement here.",
 "assumptions":["All remaining work, representation, proof path and effective CPU rate fixed.","Remove all collector CPU, even work that might not disappear in a faster run.","Count sampled per-process self CPU only; replace all sampled leaf CPU by exact wait4 totals.","Give GPU all completed floating/exact LP CPU, AST products, every unassigned killed-worker CPU second, and ALL HiGHS process CPU including startup/bookkeeping. Packing, IPC and exact repair otherwise remain.","Compute-only capacity models retain Lean proof-producing products. Separate favorable variant deletes all those products too, without claiming this is feasible.","Four CPU capacity is ideal, ignoring contention and queue/transfer/cancellation overhead. Instrumentation remains; no universal bound on a redesigned system."]}
 for method in ["native","direct"]:
  cell=A/"full1000-raw"/method/"rep1-oracle-highs"
  collector=json.loads((cell.parent/"launch.json").read_text())["pid"]
  ws=[x for x in numeric["workers"]if x["method"]==method];leaves={x["pid"]for x in ws};observed={}
  for row in m.rows(cell/"resources.jsonl.gz"):
   for p in row["processes"]:
    if p["pid"] in leaves or p["pid"]==collector:continue
    key=(p["pid"],p["created"]);observed[key]=max(observed.get(key,0),p["user"]+p["system"])
  total=sum(observed.values())+sum(x["total_cpu_ns"]for x in ws)/1e9
  c=numeric["numeric_CPU"][method];cpu=c["CPU_seconds_exclusive_completed_phases"]
  gpu=sum(cpu.get(k,0)for k in ["lp_float_solve","lp_exact_solve","AST_products"])+c["reaped_unassigned_CPU_seconds_upper_for_any_unmeasured_phase"]+numeric["external_service_CPU"][method]["whole_service_process_CPU_seconds"]
  products=phases[method]["Lean_exclusive_calling_thread_CPU_seconds"].get("products",0)
  reference=numeric["methods"]["native"]["whole_seconds"];whole=numeric["methods"][method]["whole_seconds"]
  def model(removable):
   floor=(total-removable)/4
   return {"GPU_removable_CPU_seconds_generous_upper":removable,"mandatory_CPU_seconds_lower":total-removable,"ideal_four_CPU_wall_seconds_lower":floor,"native_component_reference_speedup_upper":reference/floor}
  fixed=phases[method]["optimistic_fixed_path_envelope"]
  result[method]={"observed_whole_seconds":whole,"noncollector_CPU_work_seconds_lower":total,
   "compute_only_model":model(gpu),"all_Lean_product_proofs_deleted_model":model(gpu+products),
   "wide_elapsed_union_seconds":fixed["occupied_union_seconds"],"wide_elapsed_union_fraction":fixed["occupied_union_fraction"],
   "wide_fixed_lane_model_wall_seconds":fixed["fixed_lane_model_whole_seconds"],
   "wide_fixed_lane_native_component_speedup":reference/fixed["fixed_lane_model_whole_seconds"],
   "wide_window_warning":"Includes entire numerical RPC/wait and Lean product construction. Overlapping union is not additive removable critical-path time; fixed lanes/gaps/proof path are assumptions.",
   "numeric_CPU":c,"service_CPU":numeric["external_service_CPU"][method],
   "LP_and_product_shapes":phases[method]["coefficient_space_sizes"],
   "request_overlap":phases[method]["request_availability"]}
  if method=="direct":
   result[method]["additional_CPU_work_removal_needed_after_perfect_numerics_for_1_5x"]=total-gpu-4*reference/1.5
   unavoidable=neg["attributed_Lean_CPU_seconds"].get("products",0)
   result[method]["same_IR_negative_fallback_products_preserved_model"]=model(gpu+products-unavoidable)
 tails={}
 native=phases["native"]["per_candidate"];direct={x["proof_id"]:x for x in phases["direct"]["per_candidate"]}
 for n in [10,100]:
  ids=[x["proof_id"]for x in sorted(native,key=lambda x:-x["service_seconds"])[:n]]
  tail={"rank":"native service wall, fixed IDs for both methods","proof_ids":ids}
  for method in ["native","direct"]:
   index={x["proof_id"]:x for x in phases[method]["per_candidate"]};stage=collections.Counter();rpc=collections.Counter()
   for pid in ids:
    stage.update(index[pid]["Lean_exclusive_calling_thread_CPU_seconds"]);rpc.update(index[pid]["numeric_reply_elapsed_sums_seconds_NOT_CPU"])
   tail[method]={"summed_service_seconds_NOT_whole":sum(index[p]["service_seconds"]for p in ids),"Lean_exclusive_calling_thread_CPU_seconds":dict(stage),"RPC_elapsed_sums_NOT_CPU":dict(rpc)}
  tails[str(n)]=tail
 result["native_ranked_matched_tails"]=tails
 dump("full1000-complete-budget.json",result)
 print(json.dumps({k:{q:v for q,v in result[k].items()if q in ["observed_whole_seconds","noncollector_CPU_work_seconds_lower","compute_only_model","all_Lean_product_proofs_deleted_model","same_IR_negative_fallback_products_preserved_model","additional_CPU_work_removal_needed_after_perfect_numerics_for_1_5x"]} for k in ["native","direct"]},indent=2))
if __name__=="__main__":main()
