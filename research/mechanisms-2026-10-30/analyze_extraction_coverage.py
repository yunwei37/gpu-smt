"""Reproduce the per-candidate, source-reviewed computational-extraction audit.
Categories are explicit reviewed assignments, not a token-based eligibility detector.
Worker-attempt wall sums include retries; they are not batch critical-path time.
"""
from pathlib import Path
import collections, csv, gzip, json, re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PAIR=ROOT/"artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z"
W=Path("/workspaces/.agent-state/gpu-smt-captures/workloads")
def stripped(source):
    # Evidence display only: classification comes from reviewed task/id assignments below.
    source=re.sub(r"/-.*?-/", "", source, flags=re.S)
    source=re.sub(r"--[^\n]*","",source)
    return "\n".join(line for line in source.splitlines() if line.strip())
def write_csv(path, rows):
    with path.open("w",newline="") as f:
        out=csv.DictWriter(f,fieldnames=list(rows[0]));out.writeheader();out.writerows(rows)
# task -> category, closed computational opportunity, exact missing obligation.
REVIEW={
"amc12a_2020_p4":("checked_family","digits/filter/card after set equality","DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified"),
"mathd_numbertheory_541":("checked_family","bounded Nat product grid after proved bounds","ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement"),
"mathd_numbertheory_3":("closed_potential","closed sum of ten squares modulo10","structural finite sum equivalence/certificate not implemented"),
"mathd_numbertheory_427":("closed_potential","sum divisors500 then prime-divisor sum after a substitution","closed but requires divisor/primality certificate and proof bridge"),
"mathd_numbertheory_430":("bounded_potential","3-dimensional1..9 Nat grid of closed polynomial predicates","all inputs bounded in original assumptions; closed checker soundness not implemented"),
"mathd_numbertheory_277":("bounded_potential","bounded product756/gcd/lcm grid","must retain gcd/lcm hypotheses and prove bounds/bridge"),
"mathd_numbertheory_711":("bounded_potential","bounded product896/gcd/lcm grid","product alone insufficient:28,32 sum60<72; retain gcd8/lcm112"),
"mathd_numbertheory_296":("bounded_potential","bounded cube/fourth-power grid under n<4096","must eliminate or quantify n and prove witness bounds; no compiled certificate yet"),
"amc12_2000_p12":("bounded_potential","finite Nat triple from sum12","rcases leaves unbounded tail constructors; use proved a,m,c<=12 and checked finite bridge"),
"amc12_2001_p21":("bounded_potential","bounded4-variable Nat polynomial grid","candidate bounds differ; no certified source bridge or actual cheap grid established"),
"mathd_algebra_289":("bounded_potential","bounded prime/polynomial grid","m,n grid alone leaves k,t symbolic in some candidates; full elimination/bridge required"),
"amc12_2000_p1":("bounded_potential","finite distinct factor triples of2001","bounds and source errors require checking; no end-to-end source integration"),
"amc12a_2003_p23":("proof_repair","closed divisor/card expression appears after incorrect set equality","false auxiliary set equality; cannot accept original source by computing a different final theorem"),
"mathd_numbertheory_483":("bridge_required","recurrence determines positive Fibonacci values","current expensive simp works over symbolic function/quantified recurrence; first prove equivalence to structural evaluator; not closed input now"),
"imo_1992_p1":("bounded_potential","bounded integer triple divisibility grid","must prove exhaustive bounds; Int signed evaluation/sound bridge not implemented"),
"mathd_numbertheory_451":("not_closed","finite outer n range contains unbounded existential m","bounded outer syntax does not close existential search; divisors symbolic"),
"amc12a_2020_p10":("not_closed","logarithmic hypotheses on symbolic n before interval_cases","Real.logb noncomputable and disputed n bounds; numeric digits suffix does not establish hot-path coverage"),
"imo_1997_p5":("not_closed","exponential equation with unbounded match tails","finite syntax of match does not bound x,y; symbolic simp/nlinarith"),
"imo_1982_p1":("not_closed","symbolic function with disjunctive recurrence constraints","hypotheses do not uniquely define closed function values; omega over symbolic applications"),
"numbertheory_fxeq4powxp6powxp9powx_f2powmdvdf2pown":("not_closed","symbolic exponent divisibility","unbounded m,n; repeated simp is not closed finite evaluation"),
"mathd_numbertheory_495":("not_closed","symbolic gcd/lcm and congruences","unbounded variables; no certified finite reduction"),
"amc12a_2021_p14":("not_computable","closed Real.logb sums","closed does not imply executable: requires analytic logarithm lemmas before reflection"),
"aime_1984_p1":("not_closed","symbolic rational sequence sums","u0 remains free; algebraic cancellation/proof needed, not closed evaluation"),
"amc12a_2020_p15":("not_computable","complex roots/absolute value/square root","symbolic complex and Real.sqrt proof search"),
"numbertheory_3pow2pownm1mod2pownp3eq2pown2":("not_closed","symbolic power modular identity","unbounded induction parameter"),
"numbertheory_3pow2pownm1mod2pownp3eq2pownp2":("not_closed","symbolic power modular identity","unbounded induction parameter"),
"amc12a_2021_p12":("not_computable","symbolic complex polynomial/real coefficients","root and positivity assumptions require symbolic proof"),
"numbertheory_aoddbdiv4asqpbsqmod8eq1":("not_closed","symbolic integer modular polynomial","could design residue-class theorem but current calls not closed; not counted"),
"mathd_algebra_158":("not_closed","finite sums with symbolic a and commutative rewriting","small closed sub-sum is not evidence that dominant rewrite work can be extracted"),
"mathd_numbertheory_582":("not_closed","symbolic Nat modular sum","unbounded n; residue reduction needs new symbolic bridge"),
}
OVERRIDE={
"minif2f-3689":("proof_repair","filter omits5-divisibility","even-digit4-digit set has500 members, not100; false intermediate equality"),
"minif2f-4997":("proof_repair","asserts each factor<=40","(667,3,1) satisfies original assumptions and violates asserted bound; Lean witness already retained"),
"minif2f-5006":("proof_repair","asserts each factor<=31","(667,3,1) refutes auxiliary bound; original final goal remains true"),
"minif2f-5016":("proof_repair","asserts each factor<=44","(667,3,1) refutes auxiliary bound; original final goal remains true"),
"minif2f-1846":("not_closed","rcases over integers retains symbolic tails","cannot equate nested rcases to finite exhaustive grid"),
}
EPFL_REVIEW={
"epfl-34888":("bridge_required","Nat recurrence with fixed initial values","timeout at symbolic induction/omega, not a closed evaluator; derive structural recursion first"),
"epfl-43586":("not_computable","Real.logb/log equations","symbolic nlinarith/definitional equality; no closed computable hot region"),
"epfl-53843":("not_computable","symbolic Real.sqrt inequalities","nlinarith Simplex timeout; closed extraction inapplicable"),
"epfl-58867":("not_closed","arbitrary-dimensional Euclidean vector construction","aesop/type/elaboration failures; finite dimension is symbolic"),
"epfl-31023":("closed_potential","odd product below10000 vs factorial quotient","rfl reaches recursion depth; structural product/factorial and proved equivalence could apply, no prototype for huge integer kernel cost"),
"epfl-27729":("bridge_required","Int recurrence determines positive indices","attempted periodicity proof has prior error on free x0; extraction requires a new proved recurrence bridge and may repair the proof"),
"epfl-2994":("closed_potential","942! modulo15^233 and5^234","rfl reaches recursion depth; big-integer modular evaluator certificate not implemented"),
"epfl-1576":("not_computable","bounded sums of floor(Real.logb2 k)","Real.logb has no executable instance; a proved integer log equivalence would be a new bridge, not current closed code"),
"epfl-6919":("closed_potential","finite rational harmonic sum embedded in Real","recursion-depth at norm_num sum expansion; rational embedding equivalence required, unsupported by current Nat-only prototypes"),
"epfl-47766":("bridge_required","Complex.I finite sum after an unproved n bound","can in principle reduce to integer pairs but actual timeout precedes finite enumeration in symbolic proof"),
"epfl-47248":("bridge_required","Int recurrence with fixed positive initial values","prior linarith error plus symbolic periodicity timeout; target extraction needs new bridge, no source-preserving claim"),
"epfl-45746":("not_closed","bounded sums but u2/u3 unconstrained","recurrence only constrains u(n+2) for n>=2; missing initial values prevent closed extraction"),
"epfl-62942":("not_closed","symbolic polynomial root sets","dependent elaboration/aesop; no numeric finite closed computation"),
"epfl-61171":("not_closed","infinitely many irreducible rational polynomials","unbounded construction/search; try decide is not finite computable coverage"),
"epfl-63380":("not_closed","arbitrary finite-dimensional endomorphism space","symbolic submodule/adjoint proof, not concrete finite matrix data"),
"epfl-61885":("not_closed","arbitrary group conjugacy","symbolic group/simp, no closed computation"),
"epfl-60781":("not_closed","abstract finite p-group normality","symbolic group/order and exact? search, not concrete closed finite group"),
}
def main():
    results=json.load(gzip.open(PAIR/"engine.stdout.gz","rt"))["results"]
    inputs={str(x["id"]):x for x in json.load(gzip.open(PAIR/"input7808.json.gz","rt"))["candidates"]}
    bad=[x for x in results if x["outcome"]["status"] in {"timeout","resource_exhausted"}]
    assert len(bad)==126
    rows=[]
    reviewed=[]
    for x in bad:
        c=inputs[str(x["id"])];kind,comp,note=OVERRIDE.get(str(x["id"]),REVIEW[c["task_id"]])
        src=stripped(c["code"]);src=src[src.find("theorem"):]
        attempts=x["attempts"]
        rows.append({"id":x["id"],"task":c["task_id"],"status":x["outcome"]["status"],"category":kind,
            "computation":comp,"obligation":note,"attempts":len(attempts),
            "physical_attempt_wall_s":sum(a["elapsed_seconds"] for a in attempts),
            "exclusive_attempt_wall_s":sum(a["elapsed_seconds"] for a in attempts if a["exclusive"]),
            "budget_scope":"shared48GiB,no-AS,4workers,CPU8-11; resource labels operational not logical",
            "source_replacement_qualified":False,"actual_saved_s":"unknown"})
        reviewed.append(f"### {x['id']} — {c['task_id']}\n\n{kind}: {comp}. {note}.\n\n```lean\n{src}\n```\n")
    out=HERE/"coverage";out.mkdir(exist_ok=True)
    write_csv(out/"minif2f126.csv",rows)
    (out/"minif2f126-source-review.md").write_text("# Individual computational extraction review — 自审\n\nEach selected original source reviewed; categories are opportunities, not accepted transformed candidates. Comments stripped for display only.\n\n"+"\n".join(reviewed))
    total=sum(sum(a["elapsed_seconds"] for a in x["attempts"]) for x in results)
    bad_total=sum(x["physical_attempt_wall_s"] for x in rows)
    groups=[]
    for key,items in __import__("itertools").groupby(sorted(rows,key=lambda x:x["category"]),lambda x:x["category"]):
        items=list(items);cost=sum(x["physical_attempt_wall_s"] for x in items)
        groups.append({"category":key,"candidates":len(items),"attempt_wall_s":cost,
          "share_of126_attempt_work":cost/bad_total,"share_of7808_attempt_work":cost/total})
    write_csv(out/"minif2f-category-cost.csv",groups)
    wr=[json.loads(l) for l in (W/"candidate-native-v1/results.jsonl").read_text().splitlines()]
    wi={x["case_id"]:x for x in map(json.loads,(W/"candidate-native-inputs/epfl.jsonl").read_text().splitlines())}
    selected=[x for x in wr if x.get("status")=="budget_exceeded"]
    small=[json.loads(l) for l in (W/"candidate-epfl-pending-v3/results.jsonl").read_text().splitlines()]
    extra=[x for x in small if x["status"] not in {"compile_ok","lean_error"}]
    wrows=[];wtexts=[]
    for point,data in [("EPFL136-HB200k",selected),("EPFLpending7-HB10k",extra)]:
        for x in data:
            kind,comp,note=EPFL_REVIEW[x["case_id"]]
            log=Path(x["log"]) if "log" in x else None
            txt=log.read_text() if log and log.exists() else ""
            wrows.append({"id":x["case_id"],"point":point,"status":x["status"],"category":kind,
              "computation":comp,"obligation":note,"wall_s":x["wall_s"],"source_replacement_qualified":False,
              "first_native_error":next((l.split("error:",1)[1].strip() for l in txt.splitlines() if "error:" in l),"unknown")})
            wtexts.append(f"### {x['case_id']} — {point}\n\n{kind}: {comp}. {note}.\n\n```lean\n{stripped(wi[x['case_id']]['source'])}\n```\n")
    assert len(selected)==12 and len(extra)==5
    write_csv(out/"epfl17.csv",wrows)
    (out/"epfl17-source-review.md").write_text("# EPFL individual review — 自审\n\nSeparate resource points; 12 budget-exceeded returns atHB200k, and3HB/2self-wall returns atHB10k. Stuck214 is censored and not counted.\n\n"+"\n".join(wtexts))
    summary={"minif2f126_statuses":dict(collections.Counter(x["status"] for x in rows)),
      "all7808_physical_attempt_wall_s":total,"bad126_physical_attempt_wall_s":bad_total,
      "category_cost":groups,"accepted_source_replacements":0,
      "EPFL136_total_wall_s":sum(x["wall_s"] for x in wr if x.get("dataset")=="EPFL-evaluation"),
      "EPFL136_budget_wall_s":sum(x["wall_s"] for x in selected),
      "EPFL136_closed_potential_wall_s":sum(x["wall_s"] for x in selected if EPFL_REVIEW[x["case_id"]][0]=="closed_potential"),
      "EPFLpending7_total_wall_s":sum(x["wall_s"] for x in small),
      "EPFLpending7_budget_wall_s":sum(x["wall_s"] for x in extra)}
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
