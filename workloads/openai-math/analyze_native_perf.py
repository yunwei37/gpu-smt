#!/usr/bin/env python3
"""Analyze native-only period-weighted perf stacks, retaining unresolved callers."""
import argparse,collections,csv,gzip,json,re,statistics
from pathlib import Path
HEADER=re.compile(r"^(\S+)\s+(\d+)/(\d+)\s+([\d.]+):\s+(\d+)\s+(.+):\s*$")
FRAME=re.compile(r"^\s+[0-9a-f]+\s+(.*?)\s+\((.*)\)\s*$")
def anchor(symbol):
    if symbol.startswith(("lean::type_checker::","lean_kernel_check","lean_kernel_add_decl")):
        return "cpp_type_checker_routines"
    for namespace,kind in [("Meta","lean_meta"),("Compiler","lean_compiler"),("Elab","lean_elab")]:
        if re.match(r"^l_(?:__private_)?Lean_"+namespace+r"(?:_|$)",symbol):
            return kind
    if symbol.startswith(("lean_import_modules","lean::load_module","l_Lean_importModules","l_Lean_Environment_importModules","l___private_Lean_Environment_0__Lean_readIRPartsOfMod","l___private_Lean_Environment_0__Lean_readModuleDataPartsOfMod","l___private_Lean_Environment_0__Lean_importModulesCore")):
        return "module_import"
    if symbol.startswith(("lean_write_module","l_Lean_writeModule","lean::write_module")):
        return "module_serialization"
    return None
def runtime_leaf(symbol):
    return symbol.startswith(("lean_inc","lean_dec","lean_alloc","lean_mark","lean_name","mi_","malloc","free","memcpy","memmove"))
def stacks(path):
    current=None
    with gzip.open(path,"rt")as source:
        for line in source:
            match=HEADER.match(line)
            if match:
                if current:yield current
                current=dict(comm=match[1],pid=int(match[2]),tid=int(match[3]),period=int(match[5]),event=match[6],frames=[])
            else:
                frame=FRAME.match(line)
                if current and frame:current["frames"].append((frame[1],frame[2]))
    if current:yield current
def write(path,rows):
    if not rows:return
    with path.open("w",newline="")as f:
        w=csv.DictWriter(f,fieldnames=rows[0],lineterminator="\n");w.writeheader();w.writerows(rows)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--capture",type=Path,required=True);p.add_argument("--out",type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    plan=json.loads((a.capture/"plan.json").read_text());returns=[json.loads(x)for x in(a.capture/"results.jsonl").read_text().splitlines()]
    completed={(x["module"],x["mode"])for x in returns}
    summary=[];phases=[];leaves=[];counters=[];anchors=[];subfamilies=[]
    for i,job in enumerate(plan["jobs"]):
        if(job["module"],job["mode"])not in completed:continue
        q=a.capture/("invocation-"+str(i).zfill(2))
        if job["mode"]=="perf_stat"and(q/"counters.csv").exists():
            for raw in csv.reader((q/"counters.csv").read_text().splitlines()):
                if len(raw)>=5 and not raw[0].startswith("#")and raw[2]:
                    counters.append(dict(module=job["module"],event=raw[2],value=raw[0],runtime_ns=raw[3],running_percent=raw[4],scope="leaf launcher plus native descendants; raw tool values"))
        if job["mode"]!="perf_record"or not(q/"stacks.txt.gz").exists():continue
        native=json.loads((q/"native-rusage.json").read_text());native_pid=native["pid"];all_period=0;total=0;count=0;unknown_leaf=0;runtime=0;depths=[];categories=collections.Counter();leaf_periods=collections.Counter();anchor_periods=collections.Counter();checker_parts=collections.Counter();markers=0
        for sample in stacks(q/"stacks.txt.gz"):
            all_period+=sample["period"]
            if sample["pid"]!=native_pid:continue
            count+=1;weight=sample["period"];total+=weight;frames=sample["frames"];depths.append(len(frames))
            leaf=frames[0][0]if frames else"[missing]";leaf_periods[leaf]+=weight
            if leaf in ["[unknown]","[missing]"]:unknown_leaf+=weight
            if runtime_leaf(leaf):runtime+=weight
            if any(s in ["_start","start_thread","clone","__clone3","__libc_start_main"]for s,d in frames):markers+=1
            matched=next(((anchor(s),s)for s,d in frames if anchor(s)),None)
            kind=matched[0]if matched else None
            if matched:
                anchor_periods[matched]+=weight
                if matched[0]=="cpp_type_checker_routines":
                    symbol=matched[1]
                    if "type_checker::state::~state"in symbol:subfamily="checker_state_cleanup"
                    elif any("type_checker::"+s in symbol for s in ["whnf","reduce_","unfold_","is_delta"]):subfamily="checker_normalization_anchors"
                    elif any("type_checker::"+s in symbol for s in ["infer","check","ensure_"]):subfamily="checker_inference_or_check_anchors"
                    elif any("type_checker::"+s in symbol for s in ["is_def_eq","is_def_eq_core","quick_is_def_eq"]):subfamily="checker_equality_anchors"
                    else:subfamily="other_checker_anchors"
                    checker_parts[subfamily]+=weight
            categories[kind or("runtime_leaf_without_phase_anchor"if runtime_leaf(leaf)else"unresolved_or_other")]+=weight
        report=(q/"report-leaf.txt").read_text()if(q/"report-leaf.txt").exists()else""
        lost=re.search(r"Total Lost Samples:\s*(\d+)",report);reported=re.search(r"Event count \(approx.\):\s*(\d+)",report)
        if reported and int(reported[1])!=all_period:raise ValueError("decoded periods disagree with stock perf report")
        if not count:raise ValueError("no samples match recorded native PID")
        summary.append(dict(module=job["module"],native_samples=count,native_period=total,non_native_launcher_period=all_period-total,stock_report_total_period=int(reported[1])if reported else"",lost_samples=int(lost[1])if lost else"unknown",median_stack_depth=statistics.median(depths),max_stack_depth=max(depths),root_marker_sample_count=markers,unknown_leaf_period_share=unknown_leaf/total,runtime_primitive_leaf_period_share=runtime/total,denominator="decoded native PID user-cycle sample periods; not wall or unprofiled CPU",panel_terminal=(a.capture/"capture-terminal.json").exists()))
        for kind,weight in categories.items():phases.append(dict(module=job["module"],nearest_recognized_caller=kind,period=weight,period_share=weight/total,interpretation="symbol-family attribution; not guaranteed final proof-checking phase"))
        for symbol,weight in leaf_periods.most_common(30):leaves.append(dict(module=job["module"],symbol=symbol,period=weight,period_share=weight/total))
        for(kind,symbol),weight in anchor_periods.most_common(30):anchors.append(dict(module=job["module"],caller_family=kind,anchor_symbol=symbol,period=weight,period_share=weight/total))
        for subfamily,weight in checker_parts.items():subfamilies.append(dict(module=job["module"],nearest_checker_anchor=subfamily,period=weight,native_period_share=weight/total))
        if sum(checker_parts.values())!=categories["cpp_type_checker_routines"]:raise ValueError("checker subfamilies do not partition checker family")
        if sum(categories.values())!=total:raise ValueError("period attribution does not partition native periods")
    write(a.out/"checker-subfamilies.csv",subfamilies);write(a.out/"sampling-quality.csv",summary);write(a.out/"caller-families.csv",phases);write(a.out/"top-native-leaves.csv",leaves);write(a.out/"raw-counters.csv",counters);write(a.out/"top-caller-anchors.csv",anchors)
    state=dict(native_returned=len(returns),planned_invocations=len(plan["jobs"]),cases=len(plan["cases"]),decoded_native_recordings=len(summary),planned_recordings=sum(x["mode"]=="perf_record"for x in plan["jobs"]),panel_terminal=(a.capture/"capture-terminal.json").exists(),classification_revision=2,profile_phase_claim="tentative nearest symbol-family anchors; lost/unknown/launcher periods explicit")
    (a.out/"scope.json").write_text(json.dumps(state,indent=2)+"\n");print(json.dumps(state));print(json.dumps(summary))
if __name__=="__main__":main()
