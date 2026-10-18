"""Read closed full-population cells. No final ratios or filtering from partial captures."""
from pathlib import Path
import json,gzip,collections,math
A=Path(__file__).resolve().parent
def rows(p):
 if not p.exists():return[]
 with gzip.open(p,"rt")as f:return[json.loads(l)for l in f if l.strip()]
def quantiles(xs):
 xs=sorted(xs)
 return{"n":len(xs),**{k:xs[max(0,math.ceil(q*len(xs))-1)]for k,q in[("p50",.5),("p90",.9),("p99",.99),("max",1)]}}if xs else{"n":0}
def main():
 result={"state":"partial","scope":"One fixed-order complete original formal-population observation, three modes. FourCPU12--15/native4.9/48GiB/300s/warm4batch; source-native nonmatching-header fallback. Shared host; no fastest-globalCPU, confidence, GPU or whole-upstream-service claim. Root self-review only.","datasets":{}}
 for ds,n in[("proofnet",5952),("minif2f",7808)]:
  res={"state":"partial","conditions":{}};responses={}
  for mode in["stock","native","direct"]:
   out=A/ds/mode
   if not(out/"terminal.json").exists():continue
   t=json.loads((out/"terminal.json").read_text())
   if t["state"]!="complete":res["conditions"][mode]={"terminal":t};continue
   assert t["returned"]==n and t["expected"]==n and t["memory_limit_bytes"]==51539607552
   data=rows(out/"results.jsonl.gz");assert len(data)==n
   indexed={x["index"]:x for x in data};assert len(indexed)==n and set(indexed)==set(range(n))
   assert dict(collections.Counter(x["outcome"]for x in data))==t["counts"]
   responses[mode]=indexed
   requests=rows(out/"requests-responses.jsonl.gz")
   values=[x["wall_ns"]/1e9 for x in requests if x["event"]=="response"and("cmds"in x["request"]or"cmd"in x["request"])]
   failures=[x for x in requests if x["event"]=="request_failure"]
   res["conditions"][mode]={"terminal":t,"closed_command_request_latency_seconds":quantiles(values),"request_failures":len(failures),"latency_scope":"whole header/source/command-group request spans, not individually attributable candidate latencies"}
  if len(responses)==3:
   res["state"]="complete";ref=responses["stock"];res["fidelity"]={}
   for mode,out in responses.items():
    res["fidelity"][mode]={"verdict_differences":[{"index":k,"stock":ref[k]["outcome"],"mode":out[k]["outcome"]}for k in ref if ref[k]["outcome"]!=out[k]["outcome"]],"non_message_differences":[k for k in ref if {a:b for a,b in ref[k]["response"].items()if a!="messages"}!={a:b for a,b in out[k]["response"].items()if a!="messages"}],"message_only_difference_IDs":[k for k in ref if ref[k]["response"]!=out[k]["response"]]}
   res["fidelity_qualified"]=all(not v["verdict_differences"]and not v["non_message_differences"]for v in res["fidelity"].values())
   if res["fidelity_qualified"]:
    res["whole_ratios"]={mode:res["conditions"]["stock"]["terminal"]["whole_seconds"]/res["conditions"][mode]["terminal"]["whole_seconds"]for mode in["native","direct"]}
   else:res["ratio_disposition"]="No validated transparent speed ratio: retain wall clocks and all source transitions."
  result["datasets"][ds]=res
 if all(x["state"]=="complete"for x in result["datasets"].values()):result["state"]="complete"
 p=A/("result.json"if result["state"]=="complete"else"partial-result.json")
 p.write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps({"state":result["state"],"datasets":{ds:{"state":x["state"],"closed_cells":list(x["conditions"]),"fidelity_qualified":x.get("fidelity_qualified")}for ds,x in result["datasets"].items()}},indent=2))
if __name__=="__main__":main()
