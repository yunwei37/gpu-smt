"""Recompute closed arithmetic preflight; preserve actual native outcomes."""
from pathlib import Path
import collections,gzip,json,runpy
O=Path(__file__).resolve().parent
H=runpy.run_path(str(O.parent/"shred-closing/analyze-http.py"))
Q=O/"preflight"
expected=json.loads((Q/"source-ids.json").read_text())
data={m:H["rows"](Q/("rep1-"+m)/"results.jsonl")for m in["native","power"]}
terms={m:json.loads((Q/("rep1-"+m)/"terminal.json").read_text())for m in data}
result=dict(scope="Real24fixed-original-selection engagement, not whole-population evidence. Root self-review.",source_IDs=expected,conditions={},native_outcome_differences=[],status_differences=[],non_message_differences=[],raw_response_difference_IDs=[])
for m,t in terms.items():
 assert t["state"]=="complete"and t["returned"]==len(expected)==24
 assert [x["proof_id"]for x in data[m]]==expected
 assert not t["owned_live_descendants_after_shutdown"]
 assert t["source_concurrency"]==t["maximum_live_native_repls"]==2
 assert t["affinity"]==[8,9,10,11]and t["per_native_repl_address_limit_bytes"]==24*1024**3
 assert t["aggregate_memory_budget_bytes"]==48*1024**3
 samples=H["rows"](Q/("rep1-"+m)/"memory-rss.jsonl")
 assert len(samples)==t["memory_watchdog"]["samples"]
 assert max(x["total_rss_bytes"]for x in samples)==t["memory_watchdog"]["peak_sampled_owned_rss_bytes"]<48*1024**3
 assert max(x["native_repl_count"]for x in samples)==2 and not any("kill"in x for x in samples)
 native_limits={line for x in samples for p in x["processes"]if p["native_repl"]for line in p.get("address_limit",[])}
 assert native_limits and all(str(24*1024**3)in line for line in native_limits)
 gaps=[(y["time_ns"]-x["time_ns"])/1e9 for x,y in zip(samples,samples[1:])]
 pending={};attempts=collections.Counter()
 for event in H["rows"](Q/("rep1-"+m)/"http.jsonl"):
  if event["event"]=="request":pending[event["start_ns"]]=event
  else:
   pending.pop(event["start_ns"])
   ident=json.loads(event["request"])["snippets"][0]["id"]
   assert event["status"]==200
   attempts[ident]+=1
 assert not pending and all(attempts[x]==1 for x in expected)
 result["conditions"][m]=dict(whole_lifecycle_seconds=t["whole_lifecycle_seconds"],preparation_seconds=t["preparation_seconds"],warm_verify_seconds=t["warm_verify_seconds"],
  genuine_outcomes=dict(collections.Counter(H["verification_outcome"](x)for x in data[m])),
  counts=t["counts"],HTTP_attempts=dict(attempts),memory_watchdog=t["memory_watchdog"],
  actual_native_address_limit_lines=sorted(native_limits),maximum_sample_gap_seconds=max(gaps))
for x,y in zip(data["native"],data["power"]):
 ident=x["proof_id"]
 if H["verification_outcome"](x)!=H["verification_outcome"](y):result["native_outcome_differences"].append(ident)
 if x["status"]!=y["status"]:result["status_differences"].append(ident)
 b=x["result"].get("response",{});p=y["result"].get("response",{})
 fields={k:[b.get(k),p.get(k)]for k in set(b)|set(p)if k!="messages"and b.get(k)!=p.get(k)}
 if fields:result["non_message_differences"].append(dict(proof_id=ident,fields=fields))
 if b!=p:result["raw_response_difference_IDs"].append(ident)
result["whole_native_over_power"]=terms["native"]["whole_lifecycle_seconds"]/terms["power"]["whole_lifecycle_seconds"]
result["warm_native_over_power"]=terms["native"]["warm_verify_seconds"]/terms["power"]["warm_verify_seconds"]
(O/"preflight-analysis.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
