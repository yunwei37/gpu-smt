"""Reproduce original111-source power representation preflight; not full-cohort score."""
from pathlib import Path
import gzip,json,collections
A=Path(__file__).resolve().parent
def rows(p):
 with gzip.open(p,"rt")as f:return [json.loads(l)for l in f if l.strip()]
def main():
 result={"scope":"All111 E1071 checked-negative/fallback affected originals in original order. Normal observation,8queues/fourCPU4--7/48GiB,officialomega,same dual numerical backend; native is already-oracle-containing component control. Not full1000 continuation score or GPU result.","methods":{}}
 for method in ["native","direct","power"]:
  cell=A/("affected111-"+method+"-raw")/"rep1-oracle-highs"
  t=json.loads((cell/"terminal.json").read_text());assert t["state"]=="complete"and t["attempts"]==111 and t["effective_RLIMIT_AS"]==51539607552
  rs={x["proof_id"]:x for x in rows(cell/"responses.jsonl.gz")}
  assert len(rs)==111
  if method=="native":baseline=rs
  races=[json.loads(l)for l in(cell/"lp-races.jsonl").read_text().splitlines()if l.strip()]
  result["methods"][method]={"whole_seconds":t["whole_ns"]/1e9,"counts":t["counts"],"observer_read_errors":t["sampling_read_errors"],
    "verdict_differences":[k for k in baseline if baseline[k]["outcome"]!=rs[k]["outcome"]],
    "non_message_differences":[k for k in baseline if {a:b for a,b in baseline[k]["response"].items()if a!="messages"}!={a:b for a,b in rs[k]["response"].items()if a!="messages"}],
    "message_only_difference_IDs":[k for k in baseline if baseline[k]["response"]!=rs[k]["response"]],
    "numerical_races":len(races),"race_winners":dict(collections.Counter(x["winner"]for x in races))}
 result["direct_over_power_ratio"]=result["methods"]["direct"]["whole_seconds"]/result["methods"]["power"]["whole_seconds"]
 result["native_component_over_power_ratio"]=result["methods"]["native"]["whole_seconds"]/result["methods"]["power"]["whole_seconds"]
 result["preflight_fidelity_qualified"]=all(not x["verdict_differences"]and not x["non_message_differences"]and x["counts"]=={"complete":109,"rejected":2}for x in result["methods"].values())
 result["complete1000_admission"]=result["preflight_fidelity_qualified"]and result["direct_over_power_ratio"]>1
 (A/"qualification-result.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
if __name__=="__main__":main()
