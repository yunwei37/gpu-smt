"""Matched default/hybrid native-tail pairs; no full-engine admission from incomplete data."""
from pathlib import Path
import gzip,json
A=Path(__file__).resolve().parent
def response(p):
 with gzip.open(p,"rt")as f:return {x["proof_id"]:x for x in map(json.loads,f)}
def main():
 baseline=response(A.parent/"power-export/full1000-raw/stock-native/rep1-fast-hybrid/responses.jsonl.gz")
 out={"state":"partial","scope":"Native-reference slowest1%,10originals in original order,2opposingorders,8queues/fourCPU4--7/48GiB/officialomega/frozenCostfrontend. Upstreamdefaulttiered vs explicit hybrid only. Tailqualification, not whole1000baseline winner/confidence/novelty.","cells":{}}
 for pair in [1,2]:
  for route in ["default-tiered","hybrid"]:
   label="pair"+str(pair)+"-"+route;cell=A/(label+"-raw")/"rep1-fast-hybrid"
   if not(cell/"terminal.json").exists():continue
   t=json.loads((cell/"terminal.json").read_text());assert t["state"]=="complete"and t["attempts"]==10 and t["effective_RLIMIT_AS"]==51539607552
   receipt=json.loads((A/(label+"-engine-route.json")).read_text());assert receipt["hybrid_override"]==("1"if route=="hybrid"else None)
   rs=response(cell/"responses.jsonl.gz");assert len(rs)==10
   out["cells"][label]={"whole_seconds":t["whole_ns"]/1e9,"counts":t["counts"],"observer_errors":t["sampling_read_errors"],
    "verdict_differences_from_full_reference":[k for k in rs if rs[k]["outcome"]!=baseline[k]["outcome"]],
    "non_message_differences_from_full_reference":[k for k in rs if {a:b for a,b in rs[k]["response"].items()if a!="messages"}!={a:b for a,b in baseline[k]["response"].items()if a!="messages"}],
    "message_only_difference_IDs_from_full_reference":[k for k in rs if rs[k]["response"]!=baseline[k]["response"]],"engine_parent_receipt":receipt}
 if len(out["cells"])==4:
  out["state"]="complete";out["pairs"]=[]
  for pair in [1,2]:
   d=out["cells"]["pair"+str(pair)+"-default-tiered"];h=out["cells"]["pair"+str(pair)+"-hybrid"]
   out["pairs"].append({"pair":pair,"default_seconds":d["whole_seconds"],"hybrid_seconds":h["whole_seconds"],"hybrid_over_default_ratio":h["whole_seconds"]/d["whole_seconds"]})
  out["consistent_default_improvement"]=all(x["hybrid_over_default_ratio"]>1 for x in out["pairs"])
  out["fidelity_qualified"]=all(not x["verdict_differences_from_full_reference"]and not x["non_message_differences_from_full_reference"]for x in out["cells"].values())
 out["qualification_note"]="Actual child environment receipts, where sampled, strengthen the parent route receipt. Missing child snapshots are not invented. This reader does not establish complete upstream byteidentity or a stable engine winner."
 (A/("result.json"if out["state"]=="complete"else"partial-result.json")).write_text(json.dumps(out,indent=2)+"\n")
 print(json.dumps({k:v for k,v in out.items()if k!="cells"}|{"times":{k:(v["whole_seconds"],v["counts"])for k,v in out["cells"].items()}},indent=2))
if __name__=="__main__":main()
