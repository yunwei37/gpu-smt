"""Compare unchanged native stock default/hybrid on the retained15 originals."""
from pathlib import Path
import json,gzip
A=Path(__file__).resolve().parent
def rows(p):
 with gzip.open(p,"rt")as f:
  return [json.loads(s)for s in f if s.strip()]
def main():
 out={}
 for route in ["default-tiered","hybrid"]:
  cell=A/("qualification15-"+route+"-raw")/"rep1-fast-hybrid"
  t=json.loads((cell/"terminal.json").read_text());assert t["state"]=="complete"and t["attempts"]==15 and t["effective_RLIMIT_AS"]==51539607552
  route_receipt=json.loads((A/(route+"-engine-route.json")).read_text())
  assert route_receipt["hybrid_override"]==("1"if route=="hybrid"else None)
  out[route]={"whole_seconds":t["whole_ns"]/1e9,"counts":t["counts"],"observer_read_errors":t["sampling_read_errors"],"route":route_receipt}
  current={x["proof_id"]:x for x in rows(cell/"responses.jsonl.gz")}
  if route=="default-tiered":base=current
  else:
   assert current.keys()==base.keys()
   out["fidelity"]={"verdict_differences":[k for k in base if base[k]["outcome"]!=current[k]["outcome"]],
   "non_message_differences":[k for k in base if {a:b for a,b in base[k]["response"].items()if a!="messages"}!={a:b for a,b in current[k]["response"].items()if a!="messages"}],
   "message_only_difference_IDs":[k for k in base if base[k]["response"]!=current[k]["response"]]}
 out["default_elapsed_increase_fraction"]=out["default-tiered"]["whole_seconds"]/out["hybrid"]["whole_seconds"]-1
 out["scope"]="One selected15-original native control, officialomega,eightqueues,fourCPU4--7,48GiB. Historical raw collector method name fast-hybrid does not identify actual engine; inspect actual late route receipt/source. Parent environment at worker creation captured; not an independent child-environment audit. No new solver or parameter sweep; no global-optimality/inconclusive-margin claim."
 (A/"qualification-result.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
if __name__=="__main__":main()
