"""Prepare untrusted Int/list row payloads from the locked openai/math definitions.
No native Lean process starts here. Run paired checks only after recovery/automation.
"""
from pathlib import Path
from functools import lru_cache
from math import comb,factorial
import ast,csv,json,re,time
HERE=Path(__file__).resolve().parent
DATA=Path("/workspaces/.agent-state/gpu-smt-workloads/openai-math-4eaee875/lean")
RAW=Path("/workspaces/.agent-state/gpu-smt-captures/workloads")
OUT=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/openai-row-preparation-v3")
def choose(n,k):return comb(n,k) if 0<=k<=n else 0
@lru_cache(None)
def u(c,z,T,p):
    if z>T or p>T:return 0
    return sum((-1)**(z-h)*choose(z,h)*choose(T-z,p-h)*c**(p-h)
               for h in range(min(p,z)+1) if p+z<=T+h)
@lru_cache(None)
def v(r,D,T,p,j,k):
    return u(1,r,j+k,j)*u(1,max(D-r,0),max(T-r,0),p) if r<=j+k else 0
def entry(D,r,s,t,e,f):
    p,j,a=e;q,l,b=f;i=max(p+j-t,0);k=max(q+l-t,0);T=p+j+k
    if D>T:return 0
    exponent=max(65-2*T+p+q-t+(r+s)//2,0)
    length=max(24-max(T-D,0),0)
    desc=__import__("math").prod(24-z for z in range(length))
    return a*b*v(r,D,T,p,j,k)*v(s,D,T,q,l,i)*2**exponent*factorial(i)*factorial(k)*factorial(t)*desc
def nat_cases(count,depth=0):
    indent="  "*(depth+2)
    if depth==count:return indent+"omega\n"
    return (indent+"cases n with\n"+indent+f"| zero => exact inner_{depth}\n"+
            indent+"| succ n =>\n"+nat_cases(count,depth+1))
RECHECK = """
open Lean Elab Command in
elab "#recheck_fresh_kernel" : command => do
  let env ← getEnv
  let mut count : Nat := 0
  let mut total : Nat := 0
  for (name, ci) in env.constants.toList do
    if (env.getModuleIdxFor? name).isSome then continue
    let .thmInfo value := ci | continue
    let renamed := Name.str `MKernelRecheck name.toString
    let began ← IO.monoNanosNow
    match env.addDeclCore (Core.getMaxHeartbeats (← getOptions)).toUSize (maxRecDepth.get (← getOptions)).toUSize
        (.thmDecl {value with name := renamed, all := [renamed]}) none with
    | .error e => throwError m!"kernel recheck {name}: {e.toMessageData (← getOptions)}"
    | .ok _ => pure ()
    let ended ← IO.monoNanosNow
    total := total + (ended - began)
    count := count + 1
    logInfo m!"M_OPENAI_KERNEL {name} {ended - began}"
  logInfo m!"M_OPENAI_KERNEL_TOTAL {count} {total}"
#recheck_fresh_kernel
"""
def main():
    from run_finite import persistent_capture_path
    out=persistent_capture_path(OUT);out.mkdir(exist_ok=False)
    text=(DATA/"OAI/Analysis/Laughlin/FourBody/RowCompute.lean").read_text()
    literal=text.split("def rows :",1)[1].split(":=",1)[1].split("def UFast",1)[0].strip()
    rows=ast.literal_eval(literal)
    public=(DATA/"OAI/Analysis/Laughlin/FiniteFlux/ComputeRow1115Batch17.lean").read_text()
    goals={int(i):int(value) for i,value in re.findall(
        r"theorem computeRow_17_11_15_(\d+).*?=\s*\(\s*(-?\d+)\s*:\s*ℤ\s*\)",public,re.S)}
    assert len(goals)==7
    typed=[json.loads(line[6:]) for line in
      (RAW/"openai4341-olean-types-v3/native.log").read_text().splitlines()
      if line.startswith("AUDIT ")]
    groups=[x for x in typed if x["decide_shaped_auxiliary"]]
    assert len({x["expr_group"] for x in groups})==45
    started=time.monotonic();payloads=[];manifest=[]
    for i,row in enumerate(rows):
        values=[sum(entry(17,11,15,row[0],e,f) for f in row[2]) for e in row[2]]
        numeric=sum(values)
        payloads.append({"row":i,"outer_terms":len(values),"scalar_cells":len(values)**2,
           "values":values,"total":numeric,"published":goals[i],"matches":numeric==goals[i]})
        stem=f"row{i}"
        preamble=("import OAI.Analysis.Laughlin.FourBody.RowCompute\nimport Lean\n"
          "set_option maxHeartbeats 200000\nset_option maxRecDepth 10000\n"
          "open OAI.Laughlin.Certificate.RowCompute\nnamespace MOpenAISample\n")
        goal=f"yRowIntegralFast 17 11 15 (rows[{i}]!) = ({numeric} : Int)"
        (out/(stem+"-original.lean")).write_text(preamble+
          "theorem result : "+goal+" := by decide +kernel\n#print axioms result\nend MOpenAISample\n")
        parts=[preamble, f"abbrev currentRow := rows[{i}]!\n",
          "abbrev inner (e : Nat × Nat × Int) : Int :=\n"+
          "  (currentRow.2.2.map (fun f => yEntryIntegralFast 17 11 15 currentRow.1 e f)).sum\n"]
        for j,value in enumerate(values):
            parts.append(f"theorem inner_{j} : inner (currentRow.2.2[{j}]!) = ({value} : Int) := by decide +kernel\n")
        literal="["+", ".join(f"({n} : Int)" for n in values)+"]"
        parts.append("theorem list_certificate : currentRow.2.2.map inner = "+literal+" := by\n"+
          "  apply List.ext_getElem\n  · rfl\n  · intro n hn hm\n    simp only [List.length_cons, List.length_nil] at hm\n"+nat_cases(len(values)))
        parts.append("theorem result : "+goal+" := by\n"+
          "  change (currentRow.2.2.map inner).sum = _\n"+
          "  rw [list_certificate]\n  decide +kernel\n"+
          "#print axioms result\nend MOpenAISample\n")
        (out/(stem+"-certificate.lean")).write_text("".join(parts))
        # Separate observer copies do not masquerade as plain one-check latency.
        for mode in ["original","certificate"]:
            f=out/(stem+"-"+mode+".lean")
            (out/(stem+"-"+mode+"-recheck.lean")).write_text(f.read_text()+RECHECK)
        record=next(x for x in groups if x["name"]==f"OAI.Laughlin.Certificate.computeRow_17_11_15_{i}._proof_1_1")
        manifest.append({"row":i,"typed_group":record["expr_group"],"type_source":record["module"],
          "proof_name":record["name"],"original_source":str(out/(stem+"-original.lean")),
          "certificate_source":str(out/(stem+"-certificate.lean"))})
    (out/"payload.json").write_text(json.dumps({"numeric_wall_s":time.monotonic()-started,
      "untrusted":True,"payloads":payloads,"all_match":all(x["matches"] for x in payloads)},indent=2)+"\n")
    (out/"selected.json").write_text(json.dumps({"typed_subset":45,"selected_typed_distinct":7,
      "population_source_annotations":1354379,
      "scope":"seven distinct compiled goal types in one integer-row stratum; not a global1.35m typed census or representative sample",
      "status":"prepared, not Lean checked","targets":manifest},indent=2)+"\n")
    print(json.dumps({"rows":len(payloads),"matched":sum(x["matches"] for x in payloads),
      "scalar_cells":sum(x["scalar_cells"] for x in payloads),"generation_wall_s":time.monotonic()-started}))
if __name__=="__main__":main()
