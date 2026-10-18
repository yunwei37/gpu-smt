"""Measure exact numerical request reuse; this does not estimate cache speedup."""
import argparse,collections,gzip,json
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument("cell",type=Path);a=p.parse_args()
q=a.cell/"solver-costs.jsonl.gz";groups=collections.defaultdict(list);terminal=0;handshakes=0
with gzip.open(q,"rt")as f:
 for line in f:
  x=json.loads(line);r=x.get("request")
  if not isinstance(r,dict):terminal+=1;continue
  if"hello"in r:handshakes+=1;continue
  body={k:v for k,v in r.items()if k not in["source","call_id"]}
  key=json.dumps({"kind":x.get("kind"),"request":body},sort_keys=True,separators=(",",":"))
  cost=sum(e.get("cpu_ns",0)for e in x.get("events",[])if e.get("stage")in["fp_solve","exact_lp"])/1e9
  answer=x.get("answer")
  semantic={k:v for k,v in answer.items()if k not in["linear_ns","products_ns","lp_ns"]}if isinstance(answer,dict)else answer
  groups[key].append({"source":r.get("source"),"start_ns":x["start_ns"],"end_ns":x["end_ns"],"LP_CPU_seconds":cost,"answer":answer,"semantic":semantic})
dupes=[xs for xs in groups.values()if len(xs)>1]
cross=[xs for xs in dupes if len(set(x["source"]for x in xs))>1]
hits=[];allcost=0.;cachedcost=0.;raw_conflicts=0;semantic_conflicts=0
for xs in groups.values():
 finished=min(x["end_ns"]for x in xs);allcost+=sum(x["LP_CPU_seconds"]for x in xs)
 for x in xs:
  if x["start_ns"]>=finished:hits.append(x);cachedcost+=x["LP_CPU_seconds"]
 raw_conflicts+=len({json.dumps(x["answer"],sort_keys=True,separators=(",",":"))for x in xs})>1
 semantic_conflicts+=len({json.dumps(x["semantic"],sort_keys=True,separators=(",",":"))for x in xs})>1
out={"cell":str(a.cell),"requests":sum(map(len,groups.values())),"terminal_worker_records":terminal,"handshakes":handshakes,
 "unique_exact_ordered_payloads":len(groups),"repeated_payload_groups":len(dupes),"cross_source_repeated_payload_groups":len(cross),
 "cross_source_requests_in_those_groups":sum(map(len,cross)),"requests_without_source":sum(x["source"]is None for xs in groups.values()for x in xs),
 "already_completed_exact_payload_hits":len(hits),"all_LP_CPU_seconds":allcost,"LP_CPU_on_historical_hits_seconds":cachedcost,
 "groups_with_raw_answer_differences":raw_conflicts,"groups_with_non_timing_answer_differences":semantic_conflicts,
 "scope":"Exact numerical kind/input JSON excluding source/call_id metadata only. Answers exclude only the three observed timing counters when testing semantic equality. No permutation/subsumption/proof-state canonicalization or cache performance claim. Historical hits require earlier identical-request completion;validation/key/queue/cleanup/resource costs are unmeasured."}
print(json.dumps(out,indent=2))
