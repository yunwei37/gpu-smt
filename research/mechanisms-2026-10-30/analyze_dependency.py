"""Analyze actual retained InfoTree/trace observations without inventing full DAG joins."""
from pathlib import Path
import argparse,collections,json,statistics
def walk(nodes):
    for n in nodes:
        yield n
        yield from walk(n.get("children",[]))
def components(goals):
    parent=list(range(len(goals)))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    owners={}
    for i,(_,refs) in enumerate(goals):
        for ref in set(refs):
            if ref in owners:parent[find(i)]=find(owners[ref])
            else:owners[ref]=i
    groups=collections.defaultdict(list)
    for i in range(len(goals)):groups[find(i)].append(i)
    return list(groups.values())
def timed(n):
    return max(0.,float(n["stopSeconds"])-float(n["startSeconds"]))
def model(row):
    infos=[x for x in walk(row["infos"]) if "before" in x]
    traces=list(walk(row["traces"]))
    events=[x for x in infos if x["kind"]=="Lean.Parser.Tactic.allGoals"]
    times=[x for x in traces if x.get("kind")=="Lean.Parser.Tactic.allGoals"]
    wall=row["wallNanoseconds"]/1e9
    result={"id":row["id"],"mode":row.get("mode","observe"),"hasErrors":row["hasErrors"],
      "wall_seconds":wall,"thread_CPU_seconds":row.get("cpuNanoseconds",0)/1e9,
      "ordinary_error_messages":row.get("errors",[]),"tactic_info_nodes":len(infos),
      "profiler_step_nodes":len(traces),"all_goals_info_nodes":len(events),
      "all_goals_trace_nodes":len(times),"full_DAG_span_seconds":None,
      "full_DAG_available_parallelism":None,"model_saved_seconds":0.,
      "optimistic_allGoals_span_seconds":wall,"model_eligible":False}
    multi=[x["after"] for x in infos if len(x["after"])>1]
    result["multi_goal_snapshots"]=len(multi)
    result["multi_goal_dependency_snapshots"]=[{
      "goals":len(gs),"components":len(components(gs)),
      "contains_universe_refs":any(ref.startswith("u:") for _,rs in gs for ref in rs)}
      for gs in multi]
    if len(events)!=1 or len(times)!=1:
        result["model_reason"]="Requires a unique allGoals node in each representation; no naive global kind/order join."
        return result
    info,trace=events[0],times[0];goals=info["before"]
    children=[x for x in trace.get("children",[]) if x.get("kind")=="Lean.Parser.Tactic.tacticSeq"]
    branches=[x for x in info.get("children",[]) if x.get("kind")=="Lean.Parser.Tactic.tacticSeq"]
    if len(goals)<2 or len(children)!=len(goals) or len(branches)!=len(goals):
        result["model_reason"]="Branch counts do not align exactly with the observed before-goal list."
        return result
    if any(len(b["before"])!=1 or b["before"][0][0]!=g[0] for b,g in zip(branches,goals)):
        result["model_reason"]="Info child goal identity/order mismatch."
        return result
    if any(ref.startswith("u:") for _,rs in goals for ref in rs):
        result["model_reason"]="Universe-assignment transitive closure is unqualified."
        return result
    costs=[timed(n) for n in children];groups=components(goals)
    serial=sum(costs);parallel=max(sum(costs[i] for i in group) for group in groups)
    saving=serial-parallel
    if saving>wall+1e-5 or serial>timed(trace)+1e-5:
        result["model_reason"]="Timing/overlap inconsistency; no saving assigned."
        return result
    result.update(model_eligible=True,model_reason="Local allGoals-only opportunity model; merge semantics/overhead unproved.",
      branch_wall_seconds=costs,conservative_dependency_components=groups,
      model_saved_seconds=saving,optimistic_allGoals_span_seconds=wall-saving,
      allGoals_model_wall_ratio=wall/(wall-saving) if wall>saving else None)
    return result
def classify(row):
    text="\n".join(row.get("errors",[])).lower()
    if any(s in text for s in ["heartbeats","maximum recursion","maximum number of memory allocations","(kernel) deterministic timeout","(deterministic) timeout"]):return "diagnostic_budget_interruption"
    if any(s in text for s in ["bad_alloc","out of memory","memory limit"]):return "memory_diagnostic"
    return "ordinary_lean_error" if row["hasErrors"] else "no_lean_errors"
def analyze(paths,out,expected):
    rows=[]
    for p in paths:
        for line in p.read_text().splitlines():
            if line.startswith("M_DAG "):rows.append(json.loads(line[6:]))
    keys=[(r["id"],r.get("mode","observe")) for r in rows]
    assert len(keys)==len(set(keys)), "Do not merge duplicate candidate/mode units or restarted IDs"
    obs=[model(r) for r in rows if r.get("mode","observe")=="observe"]
    controls={r["id"]:r for r in rows if r.get("mode")=="control"}
    paired=[r for r in rows if r.get("mode")=="observe" and r["id"] in controls]
    same=sum(r["hasErrors"]==controls[r["id"]]["hasErrors"] for r in paired)
    wall=sum(r["wall_seconds"] for r in obs);saved=sum(r["model_saved_seconds"] for r in obs)
    report={"observed_units":len(rows),"expected_units":expected,"complete_units":len(rows)==expected,
      "observed_sources":len({r["id"] for r in rows}),"classification":dict(collections.Counter(classify(r) for r in rows)),
      "control_observe_pairs":len(paired),"same_error_flag_pairs":same,
      "profiler_control_wall_ratio":sum(r["wallNanoseconds"] for r in paired)/sum(controls[r["id"]]["wallNanoseconds"] for r in paired) if paired else None,
      "observed_instrumented_body_wall_seconds":wall,"observed_thread_CPU_seconds":sum(r["thread_CPU_seconds"] for r in obs),
      "qualified_local_model_candidates":sum(r["model_eligible"] for r in obs),
      "modeled_local_branch_saved_seconds":saved,
      "allGoals_only_model_ratio":wall/(wall-saved) if wall>saved else None,
      "full_200_DAG_average_parallelism":None,"rows":obs,
      "limits":[
       "This is an allGoals-only model, not a complete critical-path measurement or global upper bound.",
       "Per-goal closure overapproximates reads and includes assigned metavariables; shared refs do not prove mutable conflicts.",
       "Hidden state, namespace generation, message order, caches, heartbeat accounting and merge costs remain unproved.",
       "Have/case/first and unmatched/nested allGoals opportunities are unknown.",
       "Trace times are wall-clock floats, not per-branch CPU cycles; all unsupported work is serial in this narrow model.",
       "Both modes use a new heartbeat3000 diagnostic point, not original 300-second outcomes or production service throughput.",
       "hasErrors is a diagnostic error flag, not the production acceptance/sorry policy or proof-set parity."]}
    out.mkdir(parents=True,exist_ok=True)
    (out/"summary.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ["rows"]},indent=2))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("inputs",nargs="+",type=Path);p.add_argument("--out",required=True,type=Path);p.add_argument("--expected",type=int,default=400)
    args=p.parse_args();analyze(args.inputs,args.out,args.expected)
