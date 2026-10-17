"""All-call Lean/Rust attribution. Wall overlaps and missing records stay explicit."""
from pathlib import Path
import argparse,collections,gzip,json,math
HEADER="import Mathlib\nimport Aesop\n"
INPUT=Path("/workspaces/repository/artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl")
def stream(p):
    with (gzip.open(p,"rt") if p.suffix==".gz" else p.open()) as f:
        for line in f:yield json.loads(line)
def existing(cell,name):
    return next((p for p in [cell/name,cell/(name+".gz")] if p.exists()),None)
def spread(xs):
    if not xs:return None
    ys=sorted(xs);n=len(ys)
    return {"count":n,"min":ys[0],"median":ys[n//2],"p90":ys[int(.9*(n-1))],"p95":ys[int(.95*(n-1))],"p99":ys[int(.99*(n-1))],"max":ys[-1]}
def union(intervals):
    end=None;total=0
    for a,b in sorted(intervals):
        if b<a:raise ValueError("reversed interval")
        if end is None or a>end:total+=b-a;end=b
        elif b>end:total+=b-end;end=b
    return total
def outstanding(calls):
    ev=[]
    for i,x in enumerate(calls):
        ev.extend([(x["start_ns"],1,i),(x["end_ns"],-1,i)])
    active={};hist=collections.Counter();points=[];last=None
    for at,sign,i in sorted(ev): # completion before arrival at equal time
        if last is not None:hist[len(active)]+=at-last
        if sign<0:active.pop(i,None)
        else:
            active[i]=calls[i].get("source")
            points.append({"calls":len(active),"distinct_sources":len(set(active.values()))})
        last=at
    return {"arrival_outstanding_calls":spread([p["calls"] for p in points]),
            "arrival_distinct_candidates":spread([p["distinct_sources"] for p in points]),
            "time_seconds_by_outstanding_calls":{str(k):v/1e9 for k,v in sorted(hist.items())},
            "scope":"Client exported-AST or LP request intervals, including mutex wait; direct AST requests need product/LP construction before actual device-ready LP. Sequential future branches are excluded."}
def analyze(cell,inputs):
    terminal=json.loads((cell/"terminal.json").read_text())
    if terminal["state"]!="complete":raise ValueError("closed complete capture required")
    xs=list(stream(inputs));body=collections.defaultdict(list)
    for i,x in enumerate(xs):
        assert x["code"].startswith(HEADER)
        body["\n\n"+x["code"][len(HEADER):]].append((i,x["proof_id"]))
    defects=collections.Counter();ambiguity=sum(len(v)>1 for v in body.values())
    solver=list(stream(existing(cell,"solver-costs.jsonl")))
    lean=list(stream(existing(cell,"oracle.jsonl")))
    clients={};checks={};stages=[];native_lp=[];lean_aggregate=collections.Counter()
    for e in lean:
        kind=e.get("ty")
        if kind in ["cost-direct-roundtrip","cost-native-roundtrip"]:
            k=("direct" if kind=="cost-direct-roundtrip" else "fallback",e.get("call_id"))
            if k in clients:defects["duplicate_client_id"]+=1
            clients[k]=e
        elif kind=="cost-direct-check":
            if e.get("call_id") in checks:defects["duplicate_check_id"]+=1
            checks[e.get("call_id")]=e
        elif kind=="strong-arithmetic-stages":
            for name,cost in e.get("stages",{}).items():lean_aggregate[name]+=cost[0]
        elif kind=="cost-stage":stages.append(e)
        elif kind=="cost-lp-input":native_lp.append(e)
    if sum(bool(e.get("accepted")) for e in checks.values()) != sum(e.get("ty")=="direct-oracle" for e in lean):
        defects["check_accept_count_inconsistent"]+=1
    calls=[];per=collections.defaultdict(lambda:{"phase_cpu":collections.Counter(),"phase_wall":collections.Counter(),"calls":0})
    totals=collections.defaultdict(collections.Counter);sizes=collections.defaultdict(list)
    eligible=[];generous=[];allphases=collections.defaultdict(list);clientseq=[];classifications=collections.Counter()
    def assign(source):
        v=body.get(source,[])
        if len(v)!=1:defects["unmatched_or_ambiguous_source"]+=1;return None
        return v[0][0]
    used=set()
    for rec in solver:
        req=rec.get("request") or {}
        if req.get("hello") is True:continue
        kind=rec["kind"];cid=req.get("call_id");key=(kind,cid);src=req.get("source")
        index=assign(src);parent=clients.get(key)
        if cid is None:defects["missing_call_id"]+=1
        if parent is None:defects["missing_client"]+=1
        elif parent.get("source")!=src:defects["client_source_mismatch"]+=1
        else:
            used.add(key);clientseq.append(parent)
            # Native line is flushed before final daemon bookkeeping.
            delta=parent["end_ns"]-parent["start_ns"]-(rec["end_ns"]-rec["start_ns"])
            totals[kind]["client_minus_service_wall_ns"]+=delta
            sizes[kind+"_client_residual_ns"].append(delta)
        phases=rec["events"];cpu=collections.Counter();wall=collections.Counter()
        for ev in phases:
            st=ev["stage"]
            if "end_ns" in ev:
                cpu[st]+=ev["cpu_ns"];wall[st]+=ev["end_ns"]-ev["start_ns"]
                allphases[st].append((ev["start_ns"],ev["end_ns"]))
                if st in ["products","fp_solve","exact_lp"]:
                    eligible.append((ev["start_ns"],ev["end_ns"]));generous.append((ev["start_ns"],ev["end_ns"]))
            elif st=="shape":
                for k in ["rows","cols","nnz"]:sizes[kind+"_"+ev["kind"]+"_"+k].append(ev[k])
            elif st=="products_count":
                for k in ["products","pool_facts"]:sizes[kind+"_"+k].append(ev[k])
        residual=rec["cpu_ns"]-sum(cpu.values())
        if residual<0:defects["nested_or_bad_cpu_interval"]+=1
        cpu["protocol_dispatch_unattributed"]+=residual
        totals[kind].update(cpu);totals[kind]["total_service_cpu_ns"]+=rec["cpu_ns"]
        totals[kind]["total_service_wall_ns"]+=rec["end_ns"]-rec["start_ns"]
        answer=rec.get("answer") or {}
        if answer.get("cert") is None:state="no_certificate_or_error"
        elif kind=="direct":
            check=checks.get(cid)
            if check is None:defects["missing_direct_check"]+=1;state="unknown_check"
            elif check.get("accepted"):state="checked"
            else:state="check_failed"
        else:state="certificate"
        classifications[kind+"_"+state]+=1
        if index is not None:
            per[index]["calls"]+=1;per[index]["phase_cpu"].update(cpu);per[index]["phase_wall"].update(wall)
        calls.append({"index":index,"kind":kind,"call_id":cid,"state":state,"start_ns":rec["start_ns"],"end_ns":rec["end_ns"],
                      "phase_cpu_seconds":{k:v/1e9 for k,v in cpu.items()},"phase_wall_seconds":{k:v/1e9 for k,v in wall.items()}})
    defects["unmatched_client_calls"]=len(set(clients)-used)
    # All Lean timed stages include failed branches. Internal-stock LP has no
    # corresponding native-client roundtrip inside it; count it optimistically.
    internal=0
    for e in stages:
        st=e["stage"];i=assign(e["source"]);a,b=e["start_ns"],e["end_ns"]
        if i is not None:
            per[i]["phase_cpu"]["lean_"+st]+=e["cpu_ns"]
            per[i]["phase_wall"]["lean_"+st]+=b-a
        allphases["lean_"+st].append((a,b))
        if st=="lp":
            external=any(x.get("source")==e["source"] and a<=x["start_ns"]<=b for x in clients.values())
            if not external:internal+=1;generous.append((a,b));eligible.append((a,b))
        if st=="products":generous.append((a,b))
    for e in checks.values():
        i=assign(e["source"])
        if i is not None:
            per[i]["phase_cpu"]["lean_direct_check"]+=e["cpu_ns"]
            per[i]["phase_wall"]["lean_direct_check"]+=e["end_ns"]-e["start_ns"]
        allphases["lean_direct_check"].append((e["start_ns"],e["end_ns"]))
    responses=list(stream(cell/"responses.jsonl.gz"));waves=collections.defaultdict(list)
    for x in responses:waves[x["batch_offset"]].append(x)
    ordered=sorted(waves.values(),key=lambda w:w[0]["batch_latency_ns"],reverse=True)
    tails={}
    for fraction in [.01,.1]:
        n=math.ceil(len(ordered)*fraction);selected=ordered[:n];inds={x["index"] for w in selected for x in w}
        cpu=collections.Counter()
        for i in inds:cpu.update(per[i]["phase_cpu"])
        tails[str(fraction)]={"waves":n,"candidates":len(inds),"indices":sorted(inds),
             "summed_wave_wall_seconds":sum(w[0]["batch_latency_ns"] for w in selected)/1e9,
             "component_cpu_seconds_not_additive_across_Lean_LP_and_service":{k:v/1e9 for k,v in cpu.items()},
             "scope":"Ranked complete four-source wave wall; individual-candidate wall is unavailable. Whole tied waves retained."}
    whole=terminal["whole_ns"];sum_eligible=sum(b-a for a,b in eligible);sum_generous=sum(b-a for a,b in generous)
    complete=not any(defects.values()) and not ambiguity
    return {"terminal":terminal,"telemetry_defects":dict(defects),"ambiguous_source_groups":ambiguity,
        "all_call_schema_complete":complete,"call_outcomes":dict(classifications),"internal_Lean_LP_invocations":internal,
        "fallback_Lean_calling_thread_CPU_seconds":{k:v/1e9 for k,v in lean_aggregate.items()},
        "numeric_cpu_seconds_by_daemon":{k:{n:v/1e9 for n,v in c.items()} for k,c in totals.items()},
        "distributions":{k:spread(v) for k,v in sorted(sizes.items())},
        "observed_interval_union_seconds_by_phase":{k:union(v)/1e9 for k,v in allphases.items()},
        "accelerable_cost":{"whole_seconds":whole/1e9,"sum_interval_seconds":sum_eligible/1e9,
          "observed_union_seconds":union(eligible)/1e9,"observed_union_fraction":union(eligible)/whole,
          "generous_sum_seconds_including_all_Lean_product_construction":sum_generous/1e9,
          "optimistic_zero_cost_elapsed_lower_bound_seconds":max(0,whole-sum_generous)/1e9 if complete else None,
          "scope":"Summed eligible interval wall deliberately overcounts overlap. Only a fixed-work scheduling upper bound; union is observed occupancy, not critical-path saving. Generous bound additionally eliminates Lean product proof construction and internal exact LP, beyond a floating GPU's guarantee. No bound certified with missing attribution."},
        "batching":outstanding(clientseq),"tails":tails,"calls":calls,
        "per_source":[{"index":i,"proof_id":xs[i]["proof_id"],"calls":v["calls"],
          "component_cpu_seconds":{k:n/1e9 for k,n in v["phase_cpu"].items()}} for i,v in sorted(per.items())],
        "scope":"Diagnostic capture, all success/fallback calls. Timers and JSON logging overhead are charged, not corrected away. Overlapping parent Lean LP CPU/service CPU are reported separately. Same-method native JSON agreement required separately. Root self-review."}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("cell",type=Path);p.add_argument("--input",type=Path,default=INPUT);a=p.parse_args()
    result=analyze(a.cell,a.input)
    (a.cell/"cost-analysis.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ["calls","per_source","distributions","tails"]},indent=2))
if __name__=="__main__":main()
