"""Compare the complete six-cell cohort before interpreting timing."""
from pathlib import Path
import collections, csv, json, sys
from analyze_c_timing import read_rows, read_events, cost, normalized, analyze
from analyze_dependency import walk, components
sys.setrecursionlimit(20000)
ROOT=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30")
HERE=Path(__file__).resolve().parent

def dependency_census(captures):
    counts=collections.Counter();exclusive=collections.Counter();sources=collections.Counter()
    multi_sources=shared_sources=multi=shared=0
    for capture in captures:
        events=read_events(capture/"tactics.jsonl")
        for row in read_rows(capture/"stdout.txt"):
            present=set()
            for n in walk(events[row["id"]]["nodes"]):
                k=normalized(n["kind"])
                group=("have" if k.endswith(".tacticHave_") else
                       "case" if k.endswith((".case",".caseTag")) else
                       "allGoals" if k.endswith(".allGoals") else
                       "and_then" if k.endswith(".tactic_<;>_") else
                       "first" if k.endswith(".first") else None)
                if group:
                    counts[group]+=1;present.add(group)
                    exclusive[group]+=max(0,cost(n)-sum(cost(c) for c in n["children"]))
            for group in present:sources[group]+=1
            snapshots=set()
            for n in walk(row["infos"]):
                for field in ["liveBefore","liveAfter"]:
                    gs=n.get(field,[])
                    if len(gs)>1:
                        snapshots.add(tuple((g,tuple(sorted(set(refs))))for g,refs in gs))
            if snapshots:multi_sources+=1
            had_shared=False
            for gs in snapshots:
                multi+=1
                if len(components(gs))<len(gs):shared+=1;had_shared=True
            shared_sources+=int(had_shared)
    return {"sources":200,"C_calls_by_construct":dict(counts),
            "sources_by_construct":dict(sources),"exclusive_C_cpu_s_by_construct":dict(exclusive),
            "sources_with_multiple_live_goals":multi_sources,
            "sources_with_at_least_one_shared_live_meta_snapshot":shared_sources,
            "observable_multi_goal_live_dependency_snapshots":multi,
            "snapshots_with_shared_live_meta":shared,
            "limits":["Exclusive construct CPU is wrapper work,not inclusive parallelizable proof work.",
                      "Snapshots deduplicate goal IDs+live dependency sets per source,not full semantic contexts.",
                      "Shared live variables are conservative conflicts; independent sets are not effect safety.",
                      "Have/case/first counts are not runnable jobs or an effect-qualified full DAG."]}

def main():
    matrix=ROOT/"native-cohort-matrix"
    terminal=matrix/"terminal.json"
    if not terminal.exists():
        raise SystemExit("Matrix has no terminal receipt; preserve healthy running collection.")
    t=json.loads(terminal.read_text())
    if len(t["cells"])!=6:raise ValueError("Incomplete cell receipts")
    byid=collections.defaultdict(dict);native_models=[];receipts=[]
    for cell in t["cells"]:
        capture=Path(cell["raw_capture"])
        receipt=json.loads((capture/"receipt.json").read_text());receipts.append(receipt)
        if receipt["exit"]!=0 or not cell["native_retired"] or cell["rows"]!=100:
            raise ValueError("Incomplete/failed native cell: preserve separately, not full parity")
        rows=read_rows(capture/"stdout.txt")
        if len(rows)!=100:raise ValueError("Wrong row count")
        for row in rows:
            if cell["cell"] in byid[row["id"]]:raise ValueError("Duplicate source/cell")
            byid[row["id"]][cell["cell"]]=row
        if cell["cell"]=="linked-on":
            native_models.append(analyze(capture))
    if len(byid)!=200:raise ValueError("Wrong source population")
    captures=[Path(c["raw_capture"]) for c in t["cells"] if c["cell"]=="linked-on"]
    census=dependency_census(captures)
    comparisons=[];counts=collections.Counter();significant=[]
    for id,cells in byid.items():
        if set(cells)!={"stock","linked-off","linked-on"}:raise ValueError("Missing source comparison")
        for comparator in ["linked-off","linked-on"]:
            a,b=cells["stock"],cells[comparator]
            differences=[f for f in ["hasErrors","errors","infos","allocatedHeartbeatDelta"] if a[f]!=b[f]]
            for f in differences:counts[comparator+"/"+f]+=1
            result={"id":id,"comparator":comparator,
                    "same_error_flag":a["hasErrors"]==b["hasErrors"],
                    "same_diagnostics":a["errors"]==b["errors"],
                    "same_InfoTrees":a["infos"]==b["infos"],
                    "same_raw_HB":a["allocatedHeartbeatDelta"]==b["allocatedHeartbeatDelta"],
                    "stock_raw_HB":a["allocatedHeartbeatDelta"],"comparator_raw_HB":b["allocatedHeartbeatDelta"],
                    "stock_body_cpu_s":a["cpuNanoseconds"]/1e9,"comparator_body_cpu_s":b["cpuNanoseconds"]/1e9,
                    "stock_body_wall_s":a["wallNanoseconds"]/1e9,"comparator_body_wall_s":b["wallNanoseconds"]/1e9}
            comparisons.append(result)
            if any(f!="allocatedHeartbeatDelta" for f in differences):
                significant.append({"id":id,"comparator":comparator,"differences":differences,
                                    "stock_errors":a["errors"],"comparator_errors":b["errors"]})
    out=HERE/"native-cohort-analysis";out.mkdir(exist_ok=True)
    with (out/"differential.csv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(comparisons[0]));w.writeheader();w.writerows(comparisons)
    rows=[r for model in native_models for r in model["rows"]]
    kinds=collections.Counter()
    for m in native_models:kinds.update(m["exclusive_cpu_by_kind_s"])
    cpu=sum(r["body_cpu_s"] for r in rows)
    saved=sum(r["local_allGoals_saved_cpu_s"] for r in rows)
    leaf_lower=sum(r.get("largest_opaque_leaf_cpu_s",0) for r in rows)
    summary={"sources":200,"native_returns":600,"completed_cells":6,
             "difference_counts":dict(counts),"diagnostic_differences":significant,
             "same_observed_flags_diagnostics_InfoTrees":not significant,
             "strict_raw_heartbeat_equality":not any(k.endswith("/allocatedHeartbeatDelta") for k in counts),
             "instrumented_body_cpu_s":cpu,
             "instrumented_body_wall_s":sum(r["body_wall_s"] for r in rows),
             "complete_C_sources":sum(r["complete_C_tree"] for r in rows),
             "eligible_local_allGoals_sources":sum(r["local_allGoals_eligible"] for r in rows),
             "local_allGoals_model_saved_cpu_s":saved,
             "local_allGoals_model_ratio":cpu/(cpu-saved) if cpu>saved else None,
             "full_DAG_parallelism":None,
             "sum_per_source_largest_atomic_leaf_cpu_s":leaf_lower,
             "fixed_atomic_leaf_granularity_aggregate_parallelism_ceiling":cpu/leaf_lower if leaf_lower else None,
             "untraced_body_cpu_s":sum(r.get("untraced_body_cpu_s",0) for r in rows),
             "largest_atomic_leaf_cpu_s":max((r.get("largest_opaque_leaf_cpu_s",0) for r in rows),default=0),
             "classification":dict(collections.Counter(r["classification"] for r in rows)),
             "exclusive_cpu_by_kind_s":dict(kinds.most_common()),
             "body_totals_by_cell":{cell:{k:sum(c[cell][k]/1e9 for c in byid.values())
                                         for k in ["wallNanoseconds","cpuNanoseconds"]}
                                   for cell in ["stock","linked-off","linked-on"]},
             "whole_process_receipts":receipts,
             "limits":native_models[0]["limits"]+[
               "Raw heartbeat differences are reported even if flags/diagnostics match.",
               "Strict unchanged budget semantics is not implied by observed flag parity.",
               "Fixed200 selected sources,not full7808 acceptance/sorry policy.",
               "Untraced body time is not automatically kernel time; software PC samples required.",
               "Cell order reversed across disjoint shards; no repeated variance estimate.",
               "No complete merge-safe critical path or actual parallel runtime implemented.",
               "Leaf-only bound assumes fixed work and unchanged atomic C leaf calls, not a general kernel-parallelism bound.",
               "minif2f-4544 exceeds historical300s cutoff here; this budget3000 diagnostic population cannot establish production parallelism."]}
    (out/"dependency-census.json").write_text(json.dumps(census,indent=2)+chr(10))
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+chr(10))
    (out/"local-model-per-source.json").write_text(json.dumps(rows,indent=2)+chr(10))
    print(json.dumps({k:v for k,v in summary.items() if k not in ["whole_process_receipts","exclusive_cpu_by_kind_s","diagnostic_differences"]},indent=2))
if __name__=="__main__":main()
