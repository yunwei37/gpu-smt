"""Recompute actual real-source budget qualification and safe fault injection."""
from pathlib import Path
import json,gzip,collections,runpy
O=Path(__file__).resolve().parent
native_outcome=runpy.run_path(str(O.parent/"analyze-http.py"))["verification_outcome"]
def rows(path):
 if not path.exists():path=path.with_name(path.name+".gz")
 with(gzip.open(path,"rt")if path.suffix==".gz"else path.open())as stream:
  return[json.loads(x)for x in stream]
expected=json.loads((O/"qualification24/source-ids.json").read_text())
result=dict(scope="User-requested memory qualification only; normal24vs24 and separate real2 low-threshold fault injection. Not a performance or full-corpus result.",conditions={})
for name in["fault-injection-real2","rep1-native","rep1-shred"]:
 p=O/"qualification24"/name
 terminal=json.loads((p/"terminal.json").read_text())
 data=rows(p/"results.jsonl");samples=rows(p/"memory-rss.jsonl");http=rows(p/"http.jsonl")
 assert terminal["state"]=="complete"and not terminal["owned_live_descendants_after_shutdown"]
 assert terminal["aggregate_memory_budget_bytes"]==48*1024**3
 assert terminal["per_native_repl_address_limit_bytes"]==24*1024**3
 assert terminal["maximum_live_native_repls"]==terminal["source_concurrency"]==2
 counts=dict(collections.Counter(x["status"]for x in data));assert counts==terminal["counts"]
 assert[x["proof_id"]for x in data]==(expected[:2]if terminal["fault_injection"]else expected)
 assert max(x["native_repl_count"]for x in samples)<=2
 assert max(x["total_rss_bytes"]for x in samples)==terminal["memory_watchdog"]["peak_sampled_owned_rss_bytes"]<48*1024**3
 actual_limits=[line for sample in samples for x in sample["processes"]if x["native_repl"]for line in x.get("address_limit",[])]
 assert actual_limits and all(str(24*1024**3)in line for line in actual_limits)
 kills=[sample["kill"]for sample in samples if "kill"in sample]
 for sample in samples:
  if "kill"in sample:
   assert sample["total_rss_bytes"]>sample["effective_threshold_bytes"]
   assert sample["kill"]["victim_rss_bytes"]==max(x["rss"]for x in sample["processes"]if x["native_repl"])
   assert sample["kill"]["source_id"]in[x["proof_id"]for x in data]
 if terminal["fault_injection"]:
  assert counts=={"resource_failure":2}and len(kills)==2
  assert all(x["status"]==200 for x in http if x["event"]=="response")
 else:assert terminal["memory_watchdog"]["effective_threshold_bytes"]==48*1024**3
 resource=[dict(proof_id=x["proof_id"],sdk_status=x["sdk_status"],original_error=x["result"].get("error"))for x in data if x["status"]=="resource_failure"]
 times=[x["time_ns"]for x in samples]
 result["conditions"][name]=dict(returned=len(data),counts=counts,watchdog=terminal["memory_watchdog"],
  whole_with_input_preparation_seconds=terminal["whole_with_input_preparation_seconds"],
  actual_native_limit_lines=sorted(set(actual_limits)),kills=kills,resource_failures=resource,
  maximum_sample_gap_seconds=max((b-a)/1e9 for a,b in zip(times,times[1:]))if len(times)>1 else None)
left={x["proof_id"]:x for x in rows(O/"qualification24/rep1-native/results.jsonl")}
right={x["proof_id"]:x for x in rows(O/"qualification24/rep1-shred/results.jsonl")}
result["status_difference_IDs"]=[k for k in left if left[k]["status"]!=right[k]["status"]]
result["native_outcome_counts"]={method:dict(collections.Counter("resource_failure"if x["status"]=="resource_failure"else native_outcome(x)for x in values.values()))for method,values in[("native",left),("shred",right)]}
result["native_outcome_difference_IDs"]=[key for key in left if native_outcome(left[key])!=native_outcome(right[key])]
result["native_response_difference_IDs"]=[k for k in left if left[k]["result"].get("response")!=right[k]["result"].get("response")]
result["top_level_error_difference_IDs"]=[k for k in left if left[k]["result"].get("error")!=right[k]["result"].get("error")]
(O/"qualification-analysis.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({key:dict(counts=value["counts"],peak_owned_rss_GiB=value["watchdog"]["peak_sampled_owned_rss_bytes"]/1024**3,largest_repl_kills=len(value["kills"]),max_gap=value["maximum_sample_gap_seconds"])for key,value in result["conditions"].items()}))
