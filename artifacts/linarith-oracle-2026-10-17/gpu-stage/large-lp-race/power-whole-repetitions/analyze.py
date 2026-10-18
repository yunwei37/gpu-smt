"""Three whole-cohort observations, same fixed first-reference tails; no partial ratios."""
from pathlib import Path
import json,gzip,math,collections,shutil,importlib.util
A=Path(__file__).resolve().parent
U=Path("/tmp/gpu-smt-linarith-oracle-20261017/power-whole-repetitions")
Q=A.parent/"power-export"
def rows(p):
 if not p.exists()and p.with_name(p.name+".gz").exists():p=p.with_name(p.name+".gz")
 opener=gzip.open if p.name.endswith(".gz")else open
 with opener(p,"rt")as f:return[json.loads(l)for l in f if l.strip()]
def archive(src,dst):
 dst.mkdir(exist_ok=False)
 for p in src.rglob("*"):
  if not p.is_file():continue
  rel=p.relative_to(src);target=dst/rel;target.parent.mkdir(parents=True,exist_ok=True)
  if p.suffix==".jsonl"or p.suffix==".log":
   target=target.with_name(target.name+".gz")
   with p.open("rb")as fin,gzip.open(target,"wb",compresslevel=6)as fout:shutil.copyfileobj(fin,fout,1024*1024)
  else:shutil.copy2(p,target)
def main():
 if not(A/"terminal.json").exists():
  print("Capture driver has not closed all four cells; no partial result promoted.");return
 if not(A/"raw").exists():archive(U,A/"raw")
 inputs=rows(A.parents[2]/"input-top1000.jsonl")
 h="import Mathlib\nimport Aesop\n"
 ids={"\n\n"+x["code"][len(h):]:x["proof_id"]for x in inputs};assert len(ids)==1000
 first=json.loads((Q/"full1000-result.json").read_text());assert first["state"]=="complete"
 result={"state":"complete","scope":"Three composition-matched original1000 whole observations,8queues/4CPU4--7/48GiB/officialomega; first four-condition block contains intervening ablations, next two pairs alternate. Offline builds outside all clocks; normal-output retains common compiled Cost hooks. Shared host; no confidence/globalCPU/OSDIclaim. No GPU measured. Root self-review only.","blocks":[]}
 firstnative=first["methods"]["stock-native"]
 firstpower=first["methods"]["power"]
 tails={n:first["native_ranked_matched_tails"][n]["proof_ids"]for n in["10","100"]}
 firstblock={"block":1,"order":["power","direct-ablation","native-dual-ablation","native-control"],"native-control_seconds":firstnative["whole_seconds"],"power_seconds":firstpower["whole_seconds"],"native-control_over_power":firstnative["whole_seconds"]/firstpower["whole_seconds"],"fidelity":first["fidelity"]["power"],"counts":{"native-control":firstnative["counts"],"power":firstpower["counts"]},"observer_read_errors":{"native-control":firstnative["observer_read_errors"],"power":firstpower["observer_read_errors"]},"fixed_first_native_tail_service_sums":{n:{"native-control":first["native_ranked_matched_tails"][n]["summed_service_seconds"]["stock-native"],"power":first["native_ranked_matched_tails"][n]["summed_service_seconds"]["power"]}for n in tails}}
 result["blocks"].append(firstblock)
 for rep,order in[(2,["native-control","power"]),(3,["power","native-control"])]:
  block={"block":rep,"order":order,"counts":{},"observer_read_errors":{}}
  responses={};times={}
  for label,method in[("native-control","fast-hybrid"),("power","oracle-highs")]:
   root=A/"raw"/("rep"+str(rep)+"-"+label)
   assert json.loads((root/"terminal.json").read_text())["state"]=="complete"
   cell=root/("rep1-"+method);term=json.loads((cell/"terminal.json").read_text())
   assert term["state"]=="complete"and term["attempts"]==1000 and term["effective_RLIMIT_AS"]==51539607552
   block[label+"_seconds"]=term["whole_ns"]/1e9;block["counts"][label]=term["counts"]
   block["observer_read_errors"][label]=term["sampling_read_errors"]
   responses[label]={x["proof_id"]:x for x in rows(cell/"responses.jsonl.gz")}
   tm=collections.defaultdict(list)
   for x in rows(cell/"candidate-times.jsonl"):
    assert x["source"]in ids
    tm[ids[x["source"]]].append((x["end_ns"]-x["start_ns"])/1e9)
   assert len(tm)==1000 and all(len(v)==1 for v in tm.values())
   times[label]={k:v[0]for k,v in tm.items()}
  ref=responses["native-control"];out=responses["power"];assert len(ref)==len(out)==1000 and ref.keys()==out.keys()
  block["fidelity"]={"verdict_differences":[k for k in ref if ref[k]["outcome"]!=out[k]["outcome"]],"non_message_differences":[k for k in ref if {a:b for a,b in ref[k]["response"].items()if a!="messages"}!={a:b for a,b in out[k]["response"].items()if a!="messages"}],"message_only_difference_IDs":[k for k in ref if ref[k]["response"]!=out[k]["response"]]}
  block["native-control_over_power"]=block["native-control_seconds"]/block["power_seconds"]
  block["fixed_first_native_tail_service_sums"]={n:{label:sum(tm[k]for k in keys)for label,tm in times.items()}for n,keys in tails.items()}
  result["blocks"].append(block)
 nt=sum(x["native-control_seconds"]for x in result["blocks"]);pt=sum(x["power_seconds"]for x in result["blocks"])
 result["aggregate"]={"native-control_sum_seconds":nt,"power_sum_seconds":pt,"ratio_of_whole_sums":nt/pt,"individual_ratio_range":[min(x["native-control_over_power"]for x in result["blocks"]),max(x["native-control_over_power"]for x in result["blocks"])],"meaning":"Three complete cells each, not 3000 independent whole repetitions. Descriptive range only; no confidence interval."}
 result["fidelity_qualified"]=all(not x["fidelity"]["verdict_differences"]and not x["fidelity"]["non_message_differences"]for x in result["blocks"])
 result["fixed_tail_IDs"]=tails
 (A/"result.json").write_text(json.dumps(result,indent=2)+"\n")
 summary={**result,"blocks":[{k:v for k,v in x.items()if k!="fidelity"}|{"fidelity_counts":{k:len(v)for k,v in x["fidelity"].items()}}for x in result["blocks"]],"fixed_tail_IDs":"retained in result.json"}
 print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
