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
def cpu_ledger(records):
    requests=collections.defaultdict(list);ends={};exits={}
    for x in records:
        pid=x.get("pid")
        if x.get("kind") in ["direct","fallback"]:requests[pid].append(x)
        elif x.get("kind")=="worker-eof":ends[pid]=x
        elif x.get("kind")=="process-exit":exits[pid]=x
    workers=[]
    for pid,rs in requests.items():
        end=ends.get(pid);exit=exits.get(pid);phases=collections.Counter()
        for rec in rs:
            for e in rec.get("events",[]):
                if "cpu_ns" in e:phases[e["stage"]]+=e["cpu_ns"]
        session=sum(x["cpu_ns"] for x in rs)
        row={"pid":pid,"service_kind":rs[0]["kind"],"records_including_handshake":len(rs),
             "complete_worker_cpu_receipt":exit is not None,
             "phase_cpu_seconds":{k:v/1e9 for k,v in phases.items()},
             "session_other_cpu_seconds":(session-sum(phases.values()))/1e9,
             "session_cpu_seconds":session/1e9}
        if end:
            row.update({"eof_counter_agrees":end["sessions"]==len(rs) and end["session_cpu_ns"]==session,
                        "stdin_read_cpu_seconds":end["stdin_read_cpu_ns"]/1e9,
                        "diagnostic_write_cpu_seconds":end["diagnostic_write_cpu_ns"]/1e9})
        if exit:
            total=(exit["user_us"]+exit["system_us"])*1000
            row.update({"worker_total_cpu_seconds":total/1e9,"wait_status":exit["wait_status"],
                        "supervisor_cpu_seconds_before_exit_receipt":exit["supervisor_cpu_ns"]/1e9 if "supervisor_cpu_ns" in exit else None})
            if end:
                row["startup_exit_and_other_cpu_seconds"]=(total-session-end["stdin_read_cpu_ns"]-end["diagnostic_write_cpu_ns"])/1e9
        workers.append(row)
    return {"workers":workers,"all_worker_receipts_complete":bool(workers) and all(x["complete_worker_cpu_receipt"] and x.get("eof_counter_agrees") for x in workers),
            "scope":"wait4 measures complete worker user+system CPU through actual exit, including diagnostics; no sampling denominator. Request timers are disjoint calling-thread CPU. Remaining CPU includes startup/EOF/exit, instrumentation and any other worker threads. Supervisor CPU before receipt is separate. Missing receipts remain censored. This is numeric-service CPU accounting, not a whole-verification wall fraction."}

def analyze(cell,inputs,lean_log=None):
    terminal=json.loads((cell/"terminal.json").read_text())
    if terminal["state"]!="complete":raise ValueError("closed complete capture required")
    xs=list(stream(inputs));body=collections.defaultdict(list)
    for i,x in enumerate(xs):
        assert x["code"].startswith(HEADER)
        body["\n\n"+x["code"][len(HEADER):]].append((i,x["proof_id"]))
    defects=collections.Counter();ambiguity=sum(len(v)>1 for v in body.values())
    numeric_records=list(stream(existing(cell,"solver-costs.jsonl")))
    solver=[x for x in numeric_records if x.get("kind") in ["direct","fallback"]]
    lean=list(stream(lean_log or existing(cell,"oracle.jsonl")))
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
    responses=list(stream(cell/"responses.jsonl.gz"));wave_rows=collections.defaultdict(list)
    for response in responses:wave_rows[response["batch_offset"]].append(response)
    wave_cpu=collections.defaultdict(collections.Counter);unlabelled=[];rust_eligible=[]
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
        flags=req.get("product_columns")
        if kind=="direct":flags=next((e["columns"] for e in rec["events"] if e.get("stage")=="product_columns"),None)
        if isinstance(flags,list) and all(type(x) is bool for x in flags):
            sizes[kind+"_product_columns"].append(sum(flags))
            expected=next((e["cols"] for e in rec["events"] if e.get("stage")=="shape" and e.get("kind")=="certificate-unscaled"),None)
            if expected is not None and len(flags)!=expected:defects["product_column_length_mismatch"]+=1
        phases=rec["events"];cpu=collections.Counter();wall=collections.Counter()
        for ev in phases:
            st=ev["stage"]
            if "end_ns" in ev:
                cpu[st]+=ev["cpu_ns"];wall[st]+=ev["end_ns"]-ev["start_ns"]
                allphases[st].append((ev["start_ns"],ev["end_ns"]))
                if st in ["products","fp_solve","exact_lp"]:
                    eligible.append((ev["start_ns"],ev["end_ns"]));rust_eligible.append((ev["start_ns"],ev["end_ns"]));generous.append((ev["start_ns"],ev["end_ns"]))
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
        wave=None
        if index is not None:
            wave=next((x["batch_offset"] for x in responses if x["index"]==index),None)
        else:
            matches=[offset for offset,rs in wave_rows.items()
                if rs[0]["admitted_ns"]<=rec["start_ns"] and rec["end_ns"]<=rs[0]["observed_ns"]]
            wave=matches[0] if len(matches)==1 else None
            unlabelled.append({"pid":rec["pid"],"kind":kind,"wave":wave,"cpu_seconds":rec["cpu_ns"]/1e9,
                "candidate_indices":sorted(x["index"] for x in wave_rows.get(wave,[])),
                "scope":"source and client ID absent; unique enclosing native wave only, no candidate identity invented"})
        if wave is not None:wave_cpu[wave].update(cpu)
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
            wave=next((x["batch_offset"] for x in responses if x["index"]==i),None)
            if wave is not None:wave_cpu[wave]["lean_"+st]+=e["cpu_ns"]
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
            wave=next((x["batch_offset"] for x in responses if x["index"]==i),None)
            if wave is not None:wave_cpu[wave]["lean_direct_check"]+=e["cpu_ns"]
        allphases["lean_direct_check"].append((e["start_ns"],e["end_ns"]))
    responses=list(stream(cell/"responses.jsonl.gz"));waves=collections.defaultdict(list)
    for x in responses:waves[x["batch_offset"]].append(x)
    ordered=sorted(waves.values(),key=lambda w:w[0]["batch_latency_ns"],reverse=True)
    tails={}
    for fraction in [.01,.1]:
        n=math.ceil(len(ordered)*fraction);selected=ordered[:n];inds={x["index"] for w in selected for x in w}
        cpu=collections.Counter()
        for w in selected:cpu.update(wave_cpu[w[0]["batch_offset"]])
        tails[str(fraction)]={"waves":n,"candidates":len(inds),"indices":sorted(inds),
             "summed_wave_wall_seconds":sum(w[0]["batch_latency_ns"] for w in selected)/1e9,
             "component_cpu_seconds_not_additive_across_Lean_LP_and_service":{k:v/1e9 for k,v in cpu.items()},
             "scope":"Ranked complete four-source wave wall; individual-candidate wall is unavailable. Whole tied waves retained."}
    whole=terminal["whole_ns"];sum_eligible=sum(b-a for a,b in eligible);sum_generous=sum(b-a for a,b in generous)
    complete=not any(defects.values()) and not ambiguity
    return {"terminal":terminal,"numeric_worker_CPU_ledger":cpu_ledger(numeric_records),"telemetry_defects":dict(defects),"ambiguous_source_groups":ambiguity,
        "all_call_schema_complete":complete,"unlabelled_requests_wave_binding":unlabelled,"call_outcomes":dict(classifications),"internal_Lean_LP_invocations":internal,
        "fallback_Lean_calling_thread_CPU_seconds":{k:v/1e9 for k,v in lean_aggregate.items()},
        "numeric_cpu_seconds_by_daemon":{k:{n.removesuffix("_ns"):v/1e9 for n,v in c.items() if n not in ["client_minus_service_wall_ns","total_service_wall_ns"]} for k,c in totals.items()},
        "numeric_wall_seconds_by_daemon":{k:{n.removesuffix("_ns"):c[n]/1e9 for n in ["client_minus_service_wall_ns","total_service_wall_ns"]} for k,c in totals.items()},
        "metadata_coverage":{"numeric_requests":len(calls),"direct_generated_product_count_records":len(sizes["direct_products"]),
            "fallback_product_column_records":len(sizes["fallback_product_columns"]),
            "fallback_missing_product_column_records":sum(x["kind"]=="fallback" for x in calls)-len(sizes["fallback_product_columns"]),
            "product_scope":"Generated polynomial products for direct; mirrored probe products or generated-proof ancestry for native fallback. Unknown metadata is not zero.",
            "direct_FP_shape_records":len(sizes["direct_fp-scaled_rows"]),
            "fallback_FP_shape_records":len(sizes["fallback_fp-scaled_rows"])},
        "distributions":{k:spread(v) for k,v in sorted(sizes.items())},
        "observed_interval_union_seconds_by_phase":{k:union(v)/1e9 for k,v in allphases.items()},
        "accelerable_cost":{"whole_seconds":whole/1e9,"sum_interval_seconds":sum_eligible/1e9,
          "numeric_only_sum_interval_seconds":sum(b-a for a,b in rust_eligible)/1e9,
          "numeric_only_union_seconds":union(rust_eligible)/1e9,
          "numeric_only_occupancy_fraction":union(rust_eligible)/whole,
          "numeric_zero_cost_fixed_work_sensitivity_seconds":max(0,whole-sum(b-a for a,b in rust_eligible))/1e9,
          "observed_union_seconds":union(eligible)/1e9,"observed_union_fraction":union(eligible)/whole,
          "generous_sum_seconds_including_all_Lean_product_construction":sum_generous/1e9,
          "optimistic_zero_cost_elapsed_lower_bound_seconds":max(0,whole-sum_generous)/1e9 if complete else None,
          "scope":"Summed eligible interval wall deliberately overcounts overlap. Conditional on fixed certificates, fallback decisions and noneligible work. Only a fixed-work scheduling upper bound; union is observed occupancy, not critical-path saving. Generous bound additionally eliminates Lean product proof construction and internal exact LP, beyond a floating GPU's guarantee. No bound certified with missing attribution."},
        "batching":outstanding(clientseq),"tails":tails,"calls":calls,
        "per_source":[{"index":i,"proof_id":xs[i]["proof_id"],"calls":v["calls"],
          "component_cpu_seconds":{k:n/1e9 for k,n in v["phase_cpu"].items()},
          "component_summed_wall_seconds":{k:n/1e9 for k,n in v["phase_wall"].items()}} for i,v in sorted(per.items())],
        "scope":"Diagnostic capture, all success/fallback calls. Timers and JSON logging overhead are charged, not corrected away. Overlapping parent Lean LP CPU/service CPU are reported separately. Same-method native JSON agreement required separately. Root self-review."}
def call_outcome_costs(analysis):
    groups={}
    for call in analysis["calls"]:
        key=call["kind"]+"_"+call["state"]
        g=groups.setdefault(key,{"calls":0,"cpu":collections.Counter(),"wall":collections.Counter(),"service_intervals":[]})
        g["calls"]+=1
        g["cpu"].update(call["phase_cpu_seconds"])
        g["wall"].update(call["phase_wall_seconds"])
        g["service_intervals"].append((call["start_ns"],call["end_ns"]))
    return {key:{"calls":g["calls"],"component_cpu_seconds":dict(g["cpu"]),
        "component_summed_wall_seconds":dict(g["wall"]),
        "service_observed_union_seconds":union(g["service_intervals"])/1e9,
        "scope":"Includes failed/no-certificate calls. Exact search is separated from FP, repair and protocol; child CPU/parent Lean intervals must not be added as disjoint wall."}
        for key,g in groups.items()}

def zero_cost_summary(analysis, native_seconds=None):
    """Algebra on this closed capture's own clocks; never relabel historical data."""
    a=analysis["accelerable_cost"];t=a["whole_seconds"]
    valid=analysis["all_call_schema_complete"]
    def row(cost):
        remaining=max(0,t-cost)
        return {"removed_summed_wall_seconds":cost,"removed_sum_over_whole":cost/t,
                "remaining_fixed_work_seconds":remaining,
                "same_method_optimistic_multiple":t/remaining if valid and remaining else None,
                "matched_native_over_remaining":native_seconds/remaining if valid and remaining and native_seconds is not None else None,
                "unbounded_when_zero_remaining":bool(valid and not remaining)}
    return {"capture_whole_seconds":t,"matched_native_profile_seconds":native_seconds,
        "full_source_attribution_complete":valid,
        "LP_and_numeric_product_zero":row(a["sum_interval_seconds"]),
        "generous_all_product_construction_zero":row(a["generous_sum_seconds_including_all_Lean_product_construction"]),
        "numeric_LP_product_observed_union_fraction":a["numeric_only_occupancy_fraction"],
        "threshold_rule":"A multiple at or above1.5, unbounded deletion, or incomplete/inapplicable attribution cannot close the GPU route.",
        "scope":"Conditional fixed-work zero-cost sensitivity, not a measured GPU speedup or universal scheduler theorem. Summed wall intervals overcount overlap. Generous deletion also removes Lean product-proof construction. Fixed certificates/fallback/noneligible work are assumed. Observed union is occupancy, not removable critical-path wall. Profile and reference must share this corrected family/configuration; historical2234.69 is never substituted."}

def source_tails(analysis,cell,inputs):
    """Use actual individual candidate intervals, not the older wave proxy."""
    p=existing(cell,"candidate-times.jsonl")
    if p is None:return {"available":False,"reason":"capture predates native candidate intervals"}
    rows=list(stream(inputs));by_source={}
    for i,x in enumerate(rows):
        body="\n\n"+x["code"][len(HEADER):]
        by_source.setdefault(body,[]).append(i)
    spans={}
    for span in stream(p):
        ids=by_source.get(span["source"],[])
        if len(ids)==1:
            if ids[0] in spans:raise ValueError("duplicate individual candidate span")
            spans[ids[0]]=span
    response_indices={x["index"]for x in stream(cell/"responses.jsonl.gz")}
    rank=sorted(spans,key=lambda i:spans[i]["end_ns"]-spans[i]["start_ns"],reverse=True)
    costs={x["index"]:x for x in analysis["per_source"]}
    tails={}
    for fraction in [.01,.1]:
        ids=rank[:math.ceil(len(response_indices)*fraction)];cpu=collections.Counter();wall=collections.Counter()
        for i in ids:
            cpu.update(costs.get(i,{}).get("component_cpu_seconds",{}))
            wall.update(costs.get(i,{}).get("component_summed_wall_seconds",{}))
        tails[str(fraction)]={"indices":ids,"proof_ids":[rows[i]["proof_id"]for i in ids],
            "summed_candidate_wall_seconds":sum((spans[i]["end_ns"]-spans[i]["start_ns"])/1e9 for i in ids),
            "component_cpu_seconds":dict(cpu),"component_summed_wall_seconds":dict(wall)}
    return {"available":True,"missing_candidate_indices":sorted(response_indices-set(spans)),"tails":tails,
        "scope":"Ranked actual candidate service intervals, original population including failures. CPU and wall components include overlapping parent Lean LP and numeric child LP; they must not be summed as disjoint whole-wall fractions."}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("cell",type=Path,nargs="?");p.add_argument("--numeric-log",type=Path);p.add_argument("--lean-log",type=Path,help="Explicit derived telemetry log; retain raw and recovery provenance");p.add_argument("--input",type=Path,default=INPUT);a=p.parse_args()
    if a.numeric_log:
        result=cpu_ledger(list(stream(a.numeric_log)))
        print(json.dumps(result,indent=2));return
    if a.cell is None:p.error("cell or --numeric-log is required")
    result=analyze(a.cell,a.input,a.lean_log)
    result["lean_log_used"]=str(a.lean_log or existing(a.cell,"oracle.jsonl"))
    native=a.cell.parent/"rep1-fast-hybrid"/"terminal.json"
    nt=json.loads(native.read_text())["whole_ns"]/1e9 if native.exists() else None
    result["call_outcome_costs"]=call_outcome_costs(result)
    result["own_clock_zero_cost_summary"]=zero_cost_summary(result,nt)
    result["individual_candidate_tails"]=source_tails(result,a.cell,a.input)
    (a.cell/"cost-analysis.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ["calls","per_source","distributions","tails"]},indent=2))
if __name__=="__main__":main()
