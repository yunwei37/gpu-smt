"""Static parsed prefix sharing and nonoverlapping client-clock costs.
Uses all retained original32-candidate blocks and exact captured native-parser units.
Static sharing is potential work-unit reuse, never a measured CPU/time saving.
"""
from pathlib import Path
import collections,gzip,json,re,math,os,resource
R=Path(__file__).resolve().parents[3];A=R/"artifacts/linarith-oracle-2026-10-17"
def rows(p):
 with gzip.open(p,"rt")as f:
  for line in f:
   if line.strip():yield json.loads(line)
def distribution(xs):
 xs=sorted(xs)
 return {"count":len(xs),"min":xs[0],"p50":xs[math.ceil(len(xs)*.5)-1],"p90":xs[math.ceil(len(xs)*.9)-1],"max":xs[-1]}if xs else {"count":0}
def analyze(ds):
 items=list(rows(A/"prefix-opportunity"/(ds+"-input.jsonl.gz")));root=A/"formal-default"/ds
 parser={int(x["proposalId"]):x for x in rows(root/"unit/native-parser.jsonl.gz")}
 assert len({x["index"]for x in items})==len(items)
 groups=collections.defaultdict(list)
 for x in items:groups[x["index"]//32].append(x)
 assert all(len(xs)==32 for xs in groups.values())
 result={"sources":len(items),"original32candidateblocks":len(groups),
 "group_scope":"Retained original contiguous32candidate blocks. Input adapter retains index/header/code, not explicit task IDs; root keys use exact header and statement, without assuming every block is one semantically identical task.",
 "static_scope":"Parsed edge occurrences minus unique prefixes under exact header/statement roots. Ignores native preparation failure, early rejection, RPC/retirement costs and state liveness. Not CPU or end-to-end time saved.","methods":{}}
 headers={x["header"]for x in items}
 for method in ["exact","unit"]:
  total=unique=candidates=shared_candidates=eligible=0;depths=[];root_counts=[]
  for xs in groups.values():
   prefixes=collections.Counter();plans=[];roots=set()
   for x in xs:
    match=re.search(r":=\s*by\b",x["code"]);info=parser.get(x["index"])
    if not match or not info or not info.get("eligible"):continue
    statement=x["code"][:match.end()];proof=x["code"][match.end():]
    if chr(96)*3 in proof or not statement.startswith(x["header"]):continue
    rootkey=(x["header"],statement);roots.add(rootkey);source=proof.encode();previous=0;edges=[]
    for unit in info["units"]:
     stop=unit["stopByte"];edge=source[previous:stop].decode()if method=="exact"else unit["text"]
     edges.append(edge);previous=stop;prefixes[(rootkey,tuple(edges))]+=1
    plans.append((rootkey,edges));eligible+=1
   total+=sum(prefixes.values());unique+=len(prefixes);root_counts.append(len(roots))
   for rootkey,edges in plans:
    if not edges:continue
    depth=max([i for i in range(1,len(edges)+1)if prefixes[(rootkey,tuple(edges[:i]))]>1],default=0)
    candidates+=1;shared_candidates+=depth>0;depths.append(depth/len(edges))
  total_reuse=total-unique;terminal=json.loads((root/method/"terminal.json").read_text())
  costs=collections.defaultdict(lambda:{"requests":0,"completed_response_wall_seconds":0.0,"failed_request_wall_seconds":0.0})
  for x in rows(root/method/"requests-responses.jsonl.gz"):
   if x["event"]not in ["response","request_failure"]:continue
   q=x["request"]
   category=("prefix_step"if "proofSteps"in q else"source_fallback_batch"if "cmds"in q else"snapshot_clear"if "clearProofSnapshots"in q else"quit"if "quit"in q else"header_prepare"if q.get("cmd")in headers else"root_prepare"if q.get("cmd","").endswith("\n  sorry")else"source_or_other_command")
   costs[category]["requests"]+=1
   key="completed_response_wall_seconds"if x["event"]=="response"else"failed_request_wall_seconds"
   costs[category][key]+=x["wall_ns"]/1e9
  result["methods"][method]={"statically_eligible_sources":eligible,"sources_with_nonempty_parsed_units":candidates,
   "sources_with_any_shared_prefix":shared_candidates,"parsed_edge_occurrences":total,"distinct_prefix_nodes":unique,
   "potential_reused_edge_occurrences":total_reuse,"potential_edge_reuse_fraction":total_reuse/total if total else None,
   "candidate_shared_prefix_depth_fraction_distribution":distribution(depths),
   "distinct_exact_roots_per32block":distribution(root_counts),
   "measured_cached_lookups":terminal["cached_lookups"],"measured_executed_nodes":terminal["executed_prefix_nodes"],
   "measured_fallbacks":terminal["fallbacks"],"whole_seconds":terminal["whole_seconds"],
   "serialized_client_clock_costs":dict(costs),
   "cost_scope":"Nonoverlapping sequential client intervals, per analyze-prefix-runs.py validation. Includes waiting, not internal/native CPU; unrecorded parser/setup/cleanup remains in whole clock. Grouping is request shape, not inferred solver work."}
 batch=json.loads((root/"batch/terminal.json").read_text())
 for x in result["methods"].values():
  phase=x["serialized_client_clock_costs"]["prefix_step"];deleted=phase["completed_response_wall_seconds"]+phase["failed_request_wall_seconds"];remaining=x["whole_seconds"]-deleted
  x["all_prefix_step_intervals_zero_fixed_path_model"]={"deleted_seconds":deleted,"remaining_whole_seconds":remaining,"batch_over_remaining_ratio":batch["whole_seconds"]/remaining,"scope":"Delete ALL prefix-step request intervals including waiting/failure, keep other costs and fallback path fixed. Conditional sensitivity, not valid measured speedup or universal upper bound."}
 (root/"sharing-and-request-costs.json").write_text(json.dumps(result,indent=2)+"\n");return result
def main():
 os.sched_setaffinity(0,{12,13,14,15});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
 for ds in ["minif2f","proofnet"]:
  j=analyze(ds);print(json.dumps({"dataset":ds,"sources":j["sources"],"methods":{k:{q:v for q,v in x.items()if q in ["sources_with_any_shared_prefix","potential_edge_reuse_fraction","measured_fallbacks","serialized_client_clock_costs"]}for k,x in j["methods"].items()}},indent=2))
if __name__=="__main__":main()
