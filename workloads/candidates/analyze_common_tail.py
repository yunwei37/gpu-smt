#!/usr/bin/env python3
"""Same slow-tail definition from retained native records; no rerun or generation."""
import argparse,csv,json,math,zipfile
from pathlib import Path
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--repo",type=Path,required=True);p.add_argument("--raw",type=Path,required=True);p.add_argument("--out",type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 rows=[]
 def emit(point,values,source,scope):
  n=len(values);k=math.ceil(.016*n);values=sorted(values,reverse=True);den=sum(values);tail=sum(values[:k])
  rows.append(dict(point=point,candidates=n,requested_tail_fraction=.016,tail_candidates=k,actual_tail_fraction=k/n,tail_cost_s=tail,total_cost_s=den,tail_share=tail/den,result_kind="exact_descriptive_from_retained_returns",cost_scope=scope,source=source))
 for rep in range(3):
  source=a.repo/("artifacts/lean-native-compilation-2026-10-14/full1/proofnet-rep"+str(rep)+"-original.zip")
  with zipfile.ZipFile(source)as z:raw=[json.loads(x)for x in z.read("proofnet-rep"+str(rep)+"-original/results.jsonl").splitlines()]
  assert len(raw)==5952
  emit("ProofNet5952-rep"+str(rep),[x["elapsed_seconds"]for x in raw],str(source),"sum of request wall; includes one operational source; not concurrent batch wall")
 auto=list(csv.DictReader((a.repo/"workloads/candidates/autoverus-tail-direct.csv").open()))
 for x in auto:
  assert float(x["tail_fraction_requested"])==.016 and int(x["tail_candidates"])==math.ceil(.016*int(x["candidates"]))
  rows.append(dict(point="AutoVerus3566-rep"+x["repeat"],candidates=int(x["candidates"]),requested_tail_fraction=.016,tail_candidates=int(x["tail_candidates"]),actual_tail_fraction=int(x["tail_candidates"])/int(x["candidates"]),tail_cost_s=float(x["tail_process_wall_s"]),total_cost_s=float(x["sum_candidate_process_wall_s"]),tail_share=float(x["tail_share"]),result_kind="exact_descriptive_from_retained_returns",cost_scope="sum native process wall; generation/capture excluded",source="workloads/candidates/autoverus-tail-direct.csv"))
 coverage=list(csv.DictReader((a.repo/"research/mechanisms-2026-10-30/coverage/minif2f126.csv").open()))
 assert len(coverage)==126 and len({x["id"]for x in coverage})==126
 known=sorted([float(x["physical_attempt_wall_s"])for x in coverage],reverse=True);k=math.ceil(.016*7808);assert k==125
 lower=sum(known[:k]);den=52992.124105687
 rows.append(dict(point="miniF2F7808-retained-worker-attempts",candidates=7808,requested_tail_fraction=.016,tail_candidates=k,actual_tail_fraction=k/7808,tail_cost_s=lower,total_cost_s=den,tail_share=lower/den,result_kind="lower_bound_from_125_distinct_source_witnesses",cost_scope="candidate-aggregated physical attempt wall; retries included; not concurrent batch wall",source="research/mechanisms-2026-10-30/coverage/minif2f126.csv; whole denominator from generalization/cross-dataset.csv"))
 ep=[json.loads(x)for x in(a.raw/"candidate-native-v1/results.jsonl").read_text().splitlines()];ep=[x for x in ep if x["dataset"]=="EPFL-evaluation"];assert len(ep)==136
 emit("EPFL-evaluation136-200k",[x["wall_s"]for x in ep],"candidate-native-v1/results.jsonl","sum returned native process wall; incomplete selected prefix; stuck214 excluded")
 apr=list(csv.DictReader((a.repo/"workloads/candidates/native-versioned/april39/invocations.csv").open()))
 for mode in ["candidate","reference"]:
  selected=[x for x in apr if x["mode"]==mode];assert len(selected)==39
  emit("APRIL39-"+mode,[float(x["wall_s"])for x in selected],"workloads/candidates/native-versioned/april39/invocations.csv","unweighted selected mutation/reference process wall; not natural arrivals")
 with(a.out/"tail-comparison.csv").open("w",newline="")as f:
  w=csv.DictWriter(f,fieldnames=rows[0],lineterminator="\n");w.writeheader();w.writerows(rows)
 print(json.dumps(rows,indent=2))
if __name__=="__main__":main()
