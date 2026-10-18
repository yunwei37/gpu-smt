from pathlib import Path
import json,gzip,collections
A=Path(__file__).resolve().parent
def rows(p):
 if not p.exists()and p.with_name(p.name+".gz").exists():p=p.with_name(p.name+".gz")
 if not p.exists():return[]
 with(gzip.open(p,"rt")if p.suffix==".gz"else p.open())as f:return[json.loads(l)for l in f if l.strip()]
def main():
 result={"state":"complete","scope":"selected real64 engagement; not population speed, transparent substitution, GPU evaluation or independent audit","conditions":{}}
 responses={}
 for mode in["stock","native","direct"]:
  p=A/("qualify-"+mode)
  t=json.loads((p/"terminal.json").read_text());assert t["state"]=="complete"and t["normal_native_exit"]and t["returned"]==64 and t["memory_limit_bytes"]==51539607552
  rs=rows(p/"results.jsonl.gz");responses[mode]={(x["dataset"],x["index"]):x for x in rs};assert len(responses[mode])==64
  trace=rows(p/"oracle-trace.jsonl");counts=dict(collections.Counter(x["type"]for x in trace))
  numerical=[json.loads(x["request"])for x in trace if x["type"]in["checked","native-search"]]
  result["conditions"][mode]={"terminal":t,"events":counts,"numerical_requests":len(numerical),"nonlinear_request_count":sum(x.get("nlin")is True for x in numerical)if mode=="direct"else None,"direct_export_sum_seconds":sum(x.get("export_ns",0)for x in trace)/1e9,"search_sum_seconds":sum(x.get("search_ns",0)for x in trace)/1e9,"native_check_sum_seconds":sum(x.get("check_ns",0)for x in trace)/1e9}
 ref=responses["stock"];result["fidelity"]={}
 for mode,out in responses.items():
  assert ref.keys()==out.keys()
  result["fidelity"][mode]={"verdict_differences":[list(k)for k in ref if ref[k]["outcome"]!=out[k]["outcome"]],"non_message_differences":[list(k)for k in ref if {a:b for a,b in ref[k]["response"].items()if a!="messages"}!={a:b for a,b in out[k]["response"].items()if a!="messages"}],"message_only_difference_IDs":[list(k)for k in ref if ref[k]["response"]!=out[k]["response"]]}
 result["engaged"]=result["conditions"]["direct"]["events"].get("checked",0)>0 and result["conditions"]["native"]["events"].get("native-tactic-checked",0)>0
 result["qualified"]=result["engaged"]and all(not x["verdict_differences"]and not x["non_message_differences"]for x in result["fidelity"].values())
 (A/"qualification-result.json").write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
if __name__=="__main__":main()
