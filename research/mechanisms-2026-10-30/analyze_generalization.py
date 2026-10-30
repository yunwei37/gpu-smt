"""Cross-dataset source/diagnostic exposure, never a phase-time estimate.
Run in retained Workspace; all underlying captures are read-only."""
from pathlib import Path
import re,json,csv,zipfile,collections,sys
from run_candidate_recovery import HERE,mask_comments
from candidate_certificate_auto import route as legacy_route
from candidate_power_auto import transform as power_route
REPO=HERE.parents[1]
RAW=Path("/workspaces/.agent-state/gpu-smt-captures/workloads")
OUT=HERE/"generalization"
PAT={"heartbeats":r"maximum(?: number of)? heartbeats|deterministic.? timeout|heartbeats has been exceeded",
     "recursion":r"maximum recursion|deep recursion","memory":r"out of memory|bad_alloc|memory limit"}
def family(s):
    a=legacy_route(s)
    return a or power_route(s)[1]["route"]
def literal_params(s):
    s=mask_comments(s)
    fac=list(dict.fromkeys(map(int,re.findall(r"(?<![\w])(\d+)\s*!",s))))
    powers=list(dict.fromkeys((int(a),int(b)) for a,b in re.findall(r"(?<![\w])(\d+)\s*\^\s*(\d+)\b",s)))
    odds=list(dict.fromkeys(map(int,re.findall(r"Finset\.filter.{0,120}¬\s*Even.{0,100}Finset\.range\s+(\d+)",s,re.S))))
    return {"factorials":fac,"powers":powers,"odd_ranges":odds}
def theorem(s):
    m=re.search(r"\btheorem\s+([^\s(:]+)",mask_comments(s))
    return m[1] if m else "unparsed"
def detect(s):
    p=literal_params(s)
    return bool(p["factorials"] and re.search(r"\brfl\b",mask_comments(s)))
def broad(task,s):
    # Explicit source/diagnostic review annotations, not a trained classifier.
    if detect(s):return "closed_Nat_factorial_product","checked expression primitive; source insertion/full recovery separate"
    training_notes={
      "OMR_problem_259974":"unknown Real function equation; no closed finite evaluator",
      "lean_workbook_48322":"arbitrary Real functions f/g/h and continuity",
      "lean_workbook_40589":"cos(omega*x) with symbolic omega and x",
      "lean_workbook_plus_15663":"Real sequence with arbitrary index k; induction bridge required",
      "inequality_false":"symbolic Real square-root inequality",
      "OMR_problem_118008_0_gp7":"closed trigonometric expression at pi/9 is noncomputable Real, outside proved fragment"}
    if task in training_notes:return "symbolic_or_noncomputable",training_notes[task]
    if task=="exercise_4_5_23":return "bounded_abstract_group_arithmetic","finite arithmetic branches but abstract Group/Sylow goal needs a new proved bridge"
    if task in {"aimeII_2001_p3","amc12a_2021_p8"}:return "finite_recurrence_bridge","fixed-index recurrence evaluation possible only after a proved sequence/evaluator bridge"
    if task=="amc12a_2009_p15":return "finite_complex_sum_bridge","closed integer-valued complex sum needs casts, bounds and completeness proof"
    if task=="imo_1979_p1":return "finite_rational_sum_bridge","finite rational sum into Real plus divisibility; no current bridge"
    if task=="number_theory_319156":return "finite_rational_sum_bridge","closed rational sum into Real/floor; no current checked cast/bound bridge"
    if task=="number_theory_8962_1":return "finite_Nat_sum_sublemma","closed cube-sum helper, but native failure also includes symbolic exponent/totient and mutated syntax"
    if task=="amc12a_2002_p21":return "underspecified_sequence","u2/u3 remain free; supplied initial values do not give a closed numeric evaluator"
    if "Real.logb" in mask_comments(s):return "noncomputable_log","log/floor sum is not the supported computable fragment; source assertions not certified"
    if task in {"exercise_13_4a2","exercise_4_5b","exercise_9_4_9"}:
        return "closed_but_not_supported_decidable","a closed statement is not a closed finite Nat/Int computation"
    return "symbolic_or_noncomputable","source and native diagnostics show symbolic functions/types/algebra/analysis; no confirmed closed-heavy computation"
def proofnet():
    byrep=[];cases=[];allsource=[]
    for rep in [0,1,2]:
      zpath=REPO/f"artifacts/lean-native-compilation-2026-10-14/full1/proofnet-rep{rep}-original.zip"
      with zipfile.ZipFile(zpath) as z:
        prefix=f"proofnet-rep{rep}-original/"
        inputs={x["index"]:x for x in map(json.loads,z.read(prefix+"input.jsonl").splitlines())}
        rows=list(map(json.loads,z.read(prefix+"results.jsonl").splitlines()))
        assert len(rows)==len(inputs)==5952 and set(inputs)==set(range(5952))
        alltime=sum(x["elapsed_seconds"] for x in rows);passed={x["source_index"] for x in rows if x["basic"]=="complete"}
        budgets=[]
        for x in rows:
          response=json.loads(z.read(prefix+x["raw_response"]))
          msgs=response.get("results",[{}])[0].get("response",{}).get("messages",[])
          errs=[m for m in msgs if m.get("severity")=="error"]
          text="\n".join(m.get("data","") for m in errs)
          kinds=[k for k,pattern in PAT.items() if re.search(pattern,text,re.I)]
          if kinds:budgets.append(x)
          if rep==0:
            source=inputs[x["source_index"]]["code"];t=theorem(source)
            record={"dataset":"ProofNet","point":"ProofNet5952-original-rep0","id":"proofnet-"+str(x["source_index"]),
              "task":t,"mode":"candidate","source_index":x["source_index"],"status":x["basic"],
              "wall_s":x["elapsed_seconds"],"budget":bool(kinds),"budget_kinds":";".join(kinds),
              "source_ref":str(zpath)+"!"+prefix+"input.jsonl#"+str(x["source_index"]),
              "raw_result_ref":str(zpath)+"!"+prefix+x["raw_response"],"family":family(source) or "",
              "closed_numeric_source_hit":detect(source)}
            allsource.append({**record,"source":source})
            if kinds:
              reason,note=broad(t,source)
              sites=[str(m.get("pos",{}).get("line","")) for m in errs if any(re.search(p,m.get("data",""),re.I) for p in PAT.values())]
              cases.append({**record,"review_class":reason,"review_note":note,"error_source_lines":";".join(sites)})
        byrep.append({"rep":rep,"sources":5952,"request_wall_sum_s":alltime,
          "budget_sources":len(budgets),"budget_request_wall_s":sum(x["elapsed_seconds"] for x in budgets),
          "budget_time_share":sum(x["elapsed_seconds"] for x in budgets)/alltime,
          "complete_candidates":len(passed),"solved_groups32":len({i//32 for i in passed}),
          "tasks":186,"pass32":len({i//32 for i in passed})/186,
          "operational_sources":sum(x["basic"]=="operational" for x in rows)})
        if rep==0:
            groups=collections.defaultdict(set)
            for i,entry in inputs.items():
                if theorem(entry["code"])!="unparsed":groups[i//32].add(theorem(entry["code"]))
            assert all(len(g)==1 for g in groups.values())
    return allsource,cases,byrep
def Wpoints():
    einputs={x["case_id"]:x for x in map(json.loads,(RAW/"candidate-native-inputs/epfl.jsonl").read_text().splitlines())}
    ainputs={x["case_id"]:x for x in map(json.loads,(RAW/"candidate-native-inputs/april.jsonl").read_text().splitlines())}
    ep_raw=list(map(json.loads,(RAW/"candidate-native-v1/results.jsonl").read_text().splitlines()))
    ep_raw=[x for x in ep_raw if x["dataset"]=="EPFL-evaluation"]
    assert len(ep_raw)==136
    pend=list(map(json.loads,(RAW/"candidate-epfl-pending-v3/results.jsonl").read_text().splitlines()))
    assert len(pend)==7
    tr=list(csv.DictReader((REPO/"workloads/candidates/epfl-training12-native/candidates.csv").open()))
    for x in tr:x["log"]=str(RAW/"epfl-training12-native"/(x["index"]+".log"))
    assert len(tr)==12
    apr=[]
    for d in ["candidate-april-small-v3","candidate-april-remaining-v3"]:
        apr.extend(map(json.loads,(RAW/d/"results.jsonl").read_text().splitlines()))
    assert len(apr)==78 and len({(x["case_id"],x["mode"]) for x in apr})==78
    allsrc=[];cases=[];points=[]
    for point,arr in [("EPFL-evaluation136-200k",ep_raw),("EPFL-pending7-10k",pend),
                      ("EPFL-training12-10k",tr),("APRIL-mutations39-50k",[x for x in apr if x["mode"]=="candidate"]),
                      ("APRIL-references39-50k",[x for x in apr if x["mode"]=="reference"])]:
      tt=sum(float(x["wall_s"]) for x in arr);btime=0;bc=0
      for x in arr:
        log=Path(x["log"]);native=log.with_suffix(".lean")
        source=native.read_text()
        origin=einputs.get(x["case_id"]) or ainputs.get(x["case_id"])
        # Use native saved source for line offsets, valid reference for task identity in mutated APRIL syntax.
        task=theorem(origin["reference_source"]) if point.startswith("APRIL") else theorem(source)
        if task=="unparsed" and origin:task=theorem(origin["source"])
        budget="budget" in x["status"]
        if budget:bc+=1;btime+=float(x["wall_s"])
        rec={"dataset":"APRIL" if point.startswith("APRIL") else "EPFL","point":point,
          "id":x["case_id"],"task":task,"mode":x.get("mode","candidate"),"source_index":str(x.get("index","")),
          "status":x["status"],"wall_s":float(x["wall_s"]),"budget":budget,
          "budget_kinds":"self_wall" if x["status"].startswith("wall_") else ("native_diagnostic" if budget else ""),
          "source_ref":str(native),"raw_result_ref":str(log),"family":family(source) or "",
          "closed_numeric_source_hit":detect(source)}
        allsrc.append({**rec,"source":source})
        if budget:
          reason,note=broad(task,source)
          text=log.read_text();sites=[]
          for m in re.finditer(r"\.lean:(\d+):\d+: error:",text):
            segment=text[m.start():]
            if any(re.search(v,segment[:450],re.I) for v in PAT.values()):sites.append(m[1])
          cases.append({**rec,"review_class":reason,"review_note":note,"error_source_lines":";".join(dict.fromkeys(sites))})
      points.append({"point":point,"sources":len(arr),"request_wall_sum_s":tt,"budget_sources":bc,
          "budget_request_wall_s":btime,"budget_time_share":btime/tt})
    assert sum(x["point"]=="EPFL-training12-10k" for x in cases)==6
    return allsrc,cases,points
def write(p,rows):
    with p.open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    OUT.mkdir(exist_ok=True)
    ps,pc,pr=proofnet();ws,wc,wr=Wpoints();cases=pc+wc
    write(OUT/"budget-source-audit.csv",cases);write(OUT/"proofnet-repetitions.csv",pr)
    allsrc=ps+ws
    routing_fields=["dataset","point","id","task","mode","source_index","status","wall_s","budget","budget_kinds","family","closed_numeric_source_hit"]
    write(OUT/"full-source-routing.csv",[{k:x[k] for k in routing_fields} for x in allsrc])
    write(OUT/"W-observed-points.csv",wr)
    rawout=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/generalization-input-review")
    (rawout/"all-reviewed-budget-sources.json").write_text(json.dumps([x for x in allsrc if x["budget"]],indent=2))
    native=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/generalization-epfl-final-v4")
    assert json.loads((native/"terminal.json").read_text())["complete"]
    repaired=[]
    for attempt in json.loads((native/"results.json").read_text()):
        assert attempt["retired"]
        text=(Path(attempt["capture"])/"stdout.txt").read_text()
        if attempt["exit"]==0 and "sorryAx" not in text and "error:" not in text:
            m=re.search(r"depends on axioms: \[([^\]]*)\]",text)
            assert m and set(v.strip() for v in m[1].split(","))<={"propext","Quot.sound","Classical.choice"}
            repaired.append(attempt["id"])
    assert not repaired, "Review changed acceptance against publisher declaration policy before claiming solved tasks"
    (OUT/"native-recovery-check.json").write_text(json.dumps({"fully_recovered_ids":repaired,
       "whole_candidates":2,"final_module":"closed-nat415-v4","fallback":"paired original native observations retained on failed repair",
       "production_enablement":False},indent=2)+"\n")
    tables=[]
    for point in ["ProofNet5952-original-rep0"]+[x["point"] for x in wr]:
      rr=next(x for x in pr if x["rep"]==0) if point.startswith("ProofNet") else next(x for x in wr if x["point"]==point)
      c=[x for x in cases if x["point"]==point]
      existing=[x for x in c if x["family"]]
      literal=[x for x in c if x["closed_numeric_source_hit"]]
      potential=[x for x in c if x["review_class"] not in ["symbolic_or_noncomputable","noncomputable_log","closed_but_not_supported_decidable","underspecified_sequence"]]
      tables.append({"dataset_point":point,"sources":rr["sources"],"native_budget_sources":rr["budget_sources"],
        "native_budget_request_wall_s":rr["budget_request_wall_s"],"observed_request_wall_sum_s":rr["request_wall_sum_s"],
        "native_budget_time_share":rr["budget_time_share"],"existing_family_hits":len(existing),
        "verified_numeric_expression_candidates":len([x for x in literal if x["id"] in {"epfl-31023","epfl-2994"}]),
        "numeric_expression_request_exposure_share":sum(x["wall_s"] for x in literal)/rr["request_wall_sum_s"],
        "broader_source_review_candidates":len(potential),
        "broader_request_exposure_share":sum(x["wall_s"] for x in potential)/rr["request_wall_sum_s"],
        "complete_candidate_recoveries":sum(x["id"] in repaired for x in c),"new_solved_tasks":0,
        "interpretation":"observed point only; request exposure!=phase/removable cost; broader candidates require unimplemented bridges"})
    mini=json.loads((HERE/"power-family-result/summary.json").read_text())
    coverage=list(csv.DictReader((HERE/"coverage/minif2f126.csv").open()))
    mini_total=52992.124105687
    mini_budget=sum(float(x["physical_attempt_wall_s"]) for x in coverage)
    tables.insert(0,{"dataset_point":"miniF2F7808-retained-native-attempts","sources":7808,"native_budget_sources":126,
      "native_budget_request_wall_s":mini_budget,"observed_request_wall_sum_s":mini_total,
      "native_budget_time_share":mini_budget/mini_total,"existing_family_hits":57,
      "verified_numeric_expression_candidates":"not equated with57shape hits","numeric_expression_request_exposure_share":mini["opportunity_shape_attempt_work_s"]/mini_total,
      "broader_source_review_candidates":"not combined with37unimplemented bridges","broader_request_exposure_share":"unknown",
      "complete_candidate_recoveries":mini["actually_recovered_of126"],"new_solved_tasks":3,
      "interpretation":"32budget-source repairs plus1ordinary-error repair=33new accepted; worker-attempt sums, not concurrent wall"})
    write(OUT/"cross-dataset.csv",tables)
    (OUT/"summary.json").write_text(json.dumps({"proofnet":pr,"cross_dataset":tables,
      "proofnet_pass32_before":pr[0]["pass32"],"proofnet_pass32_after":pr[0]["pass32"],
      "proofnet_solved_before_after":[pr[0]["solved_groups32"],pr[0]["solved_groups32"]],
      "scope":"current routed method + explicitly separated broader source review; no population timing inference for sampled/censored Wframes"},indent=2)+"\n")
    # Validate that arithmetic inputs are automatically derivable, not task-ID constants.
    hit_sources=[x["source"] for x in allsrc if x["budget"] and x["closed_numeric_source_hit"]]
    fac=sorted({n for s in hit_sources for n in literal_params(s)["factorials"]})
    powers=list(dict.fromkeys(p for s in hit_sources for p in literal_params(s)["powers"] if p[1]>=128))
    odd=list(dict.fromkeys(n for s in hit_sources for n in literal_params(s)["odd_ranges"]))
    (OUT/"automatic-payload-parameters.json").write_text(json.dumps({"factorials":fac,"powers":powers,"odd_ranges":odd},indent=2)+"\n")
    print(json.dumps({"budget_sources":len(cases),"proofnet_pass32":pr[0]["pass32"],
      "points":tables,"payload_parameters":{"factorials":fac,"powers":powers,"odd_ranges":odd}},indent=2))
if __name__=="__main__":main()
