/- Direct certificate reconstruction experiment. Untrusted AST oracle; native Lean
ring/checker verifies one weighted contradiction. Unsupported cases fall back. -/
import Mathlib.Tactic.Linarith.Frontend
import GpuArithmetic.CostBaseline
open Lean Meta Elab Tactic Mathlib.Tactic.Linarith
namespace GpuArithmetic.CostOracle

private abbrev Child := IO.Process.Child {stdin := .piped, stdout := .piped, stderr := .inherit}
initialize daemon : Std.Mutex (Option Child) ← Std.Mutex.new none

private def query (request : String) : IO String :=
  daemon.atomically do
    let child ← match ← get with
      | some c => pure c
      | none => do
        let some bin ← IO.getEnv "GPU_ARITHMETIC_ORACLE" | throw (IO.userError "missing oracle")
        let c ← IO.Process.spawn {cmd := bin, stdin := .piped, stdout := .piped, stderr := .inherit}
        set (some c)
        pure c
    child.stdin.putStr (request ++ "\n")
    child.stdin.flush
    let answer ← child.stdout.getLine
    if answer.isEmpty then
      set (none : Option Child)
      throw (IO.userError "oracle EOF")
    return answer

private def atom (ref : IO.Ref (Array Expr)) (e : Expr) : MetaM String := do
  let all ← ref.get
  if let some i := all.findIdx? (· == e) then return s!"[\"a\",{i}]"
  ref.set (all.push e)
  return s!"[\"a\",{all.size}]"

private def rational (q : Rat) : String :=
  s!"[\"q\",\"{q.num}\",\"{q.den}\"]"

private partial def exportExpr (ref : IO.Ref (Array Expr)) (e : Expr) : MetaM String := do
  if let some q := e.rat? then return rational q
  match e.getAppFnArgs with
  | (``HAdd.hAdd, #[_,_,_,_,a,b]) =>
    return s!"[\"+\",{← exportExpr ref a},{← exportExpr ref b}]"
  | (``HSub.hSub, #[_,_,_,_,a,b]) =>
    return s!"[\"-\",{← exportExpr ref a},{← exportExpr ref b}]"
  | (``HMul.hMul, #[_,_,_,_,a,b]) =>
    return s!"[\"*\",{← exportExpr ref a},{← exportExpr ref b}]"
  | (``Neg.neg, #[_,_,a]) => return s!"[\"neg\",{← exportExpr ref a}]"
  | (``HDiv.hDiv, #[_,_,_,_,a,b]) =>
    if let some q := b.rat? then
      if q != 0 then return s!"[\"*\",{← exportExpr ref a},{rational q⁻¹}]"
    atom ref e
  | (``HPow.hPow, #[_,_,_,_,a,n]) =>
    if n.nat? == some 2 then
      let a ← exportExpr ref a
      return s!"[\"*\",{a},{a}]"
    atom ref e
  | _ => atom ref e

private partial def collect (h : Expr) : MetaM (List Expr) := do
  let ty ← instantiateMVars (← inferType h)
  if ty.and?.isSome then
    return (← collect (← mkAppM ``And.left #[h])) ++ (← collect (← mkAppM ``And.right #[h]))
  return [h]

private def item (ref : IO.Ref (Array Expr)) (carrier h : Expr) : MetaM (Option String) := do
  try
    let (pos, rel, ty, lhs, rhs) ← (← instantiateMVars (← inferType h)).ineqOrNotIneq?
    unless ty == carrier do return none
    let rel := if pos then rel else match rel with | .lt => .le | .le => .lt | .eq => .eq
    if !pos && rel == .eq then return none
    let (lhs,rhs) := if pos then (lhs,rhs) else (rhs,lhs)
    let tag := match rel with | .eq => "eq" | .lt => "lt" | .le => "le"
    return some s!"[\"{tag}\",{← exportExpr ref lhs},{← exportExpr ref rhs}]"
  catch _ => return none

private def getArray (j : Json) : MetaM (Array Json) :=
  match j with | .arr a => pure a | _ => throwError "expected array"

private def getNat (j : Json) : MetaM Nat :=
  match j.getNat? with | .ok n => pure n | .error e => throwError "{e}"

private def getString (j : Json) : MetaM String :=
  match j.getStr? with | .ok s => pure s | .error e => throwError "{e}"

private partial def realize (raw atoms : Array Expr) (carrier : Expr) (origin : Json) : MetaM Expr := do
  let a ← getArray origin
  let tag ← getString a[0]!
  if tag == "seed" then return ← mkNegOneLtZeroProof carrier
  let pf ← if tag == "h" then do
      let i ← getNat a[1]!
      let some h := raw[i]? | throwError "bad hypothesis index"
      let hs ← removeNegations.transform h
      let [pf] ← compWithZero.globalize.transform hs | throwError "unsupported normalized hypothesis"
      pure pf
    else if tag == "sq" then do
      let i ← getNat a[1]!
      let some e := atoms[i]? | throwError "bad square atom"
      let pf ← mkAppM ``sq_nonneg #[e]
      let [pf] ← compWithZero.globalize.transform [pf] | throwError "unsupported square"
      pure pf
    else if tag == "mul" then do
      let x ← realize raw atoms carrier a[1]!
      let y ← realize raw atoms carrier a[2]!
      let (rx,_) ← parseCompAndExpr (← inferType x)
      let (ry,_) ← parseCompAndExpr (← inferType y)
      let pf ← match rx,ry with
        | .eq,_ => mkAppM ``zero_mul_eq #[x,y]
        | _,.eq => mkAppM ``mul_zero_eq #[x,y]
        | .lt,.lt => mkAppM ``mul_pos_of_neg_of_neg #[x,y]
        | .lt,.le => do
          let x ← mkAppM ``le_of_lt #[x]
          mkAppM ``mul_nonneg_of_nonpos_of_nonpos #[x,y]
        | .le,.lt => do
          let y ← mkAppM ``le_of_lt #[y]
          mkAppM ``mul_nonneg_of_nonpos_of_nonpos #[x,y]
        | .le,.le => mkAppM ``mul_nonneg_of_nonpos_of_nonpos #[x,y]
      let [pf] ← compWithZero.globalize.transform [pf] | throwError "unsupported product"
      pure pf
    else throwError "unknown origin"
  return pf

private def checkCertificate (cfg : LinarithConfig) (g : MVarId) (carrier : Expr)
    (raw atoms : Array Expr) (cert : Array Json) : MetaM Unit := do
  let mut zip : List (Expr × Nat) := []
  for entry in cert do
    let .ok origin := entry.getObjVal? "origin" | throwError "missing origin"
    let mut pf ← realize raw atoms carrier origin
    if (entry.getObjValAs? Bool "flip").toOption.getD false then
      let (rel,t) ← parseCompAndExpr (← inferType pf)
      unless rel == .eq do throwError "negative inequality coefficient"
      pf := mkAppN (← mkAppM ``Iff.mpr #[← mkAppOptM ``neg_eq_zero #[none,none,t]]) #[pf]
    let .ok digits := entry.getObjValAs? String "coeff" | throwError "coefficient"
    let some c := digits.toNat? | throwError "invalid coefficient"
    if c > 0 then zip := (pf,c) :: zip
  let terms ← zip.mapM fun (pf,c) => do mulExpr c (← leftOfIneqProof pf)
  let sm ← addExprs terms
  let zero ← proveEqZeroUsing cfg.discharger sm
  let neg ← mkLTZeroProof zip
  let ⟨_, nep, _⟩ ← g.rewrite (← inferType neg) zero
  let pf ← mkAppM ``Eq.mp #[nep,neg]
  let pf ← mkAppM ``Mathlib.Tactic.Linarith.lt_irrefl #[pf]
  g.assign pf
  (Expr.mvar g).ensureHasNoMVars

private partial def solve (nlin onlyOn : Bool) (args : List Expr)
    (cfg : LinarithConfig) (g : MVarId) : MetaM Unit := g.withContext do
  if (← whnfR (← instantiateMVars (← g.getType))).isEq then
    let [a,b] ← g.apply (← mkConst' ``eq_of_not_lt_of_not_gt) | failure
    solve nlin onlyOn args cfg a
    solve nlin onlyOn args cfg b
    return
  let (goal,pref,nv) ← match ← applyContrLemma g with
    | (none,g) => pure (← g.exfalso,none,none)
    | (some (ty,h),g) => pure (g,some ty,some h)
  goal.withContext do
    let sources ← if onlyOn then pure (nv.toList ++ args) else do pure ((← getLocalHyps).toList ++ args)
    let sources ← sources.flatMapM collect
    let carrier ← match pref with
      | some ty => pure ty
      | none => sources.firstM fun h => do
        let (_,_,ty,_,_) ← (← inferType h).ineqOrNotIneq?
        pure ty
    unless carrier.isConstOf `Real || carrier.isConstOf ``Rat do throwError "unsupported carrier"
    let atoms ← IO.mkRef #[]
    let mut raw : Array Expr := #[]
    let mut rows : Array String := #[]
    let start ← IO.monoNanosNow
    for h in sources do
      if let some row ← item atoms carrier h then
        rows := rows.push row
        raw := raw.push h
    let exported ← IO.monoNanosNow
    let request := s!"\{\"nlin\":{if nlin then "true" else "false"},\"hyps\":[{",".intercalate rows.toList}]}"
    let request := "{\"source\":" ++ Farkas.Telemetry.jstrEsc (← getFileMap).source ++ "," ++ (request.drop 1).toString
    let answer ← query request
    let answered ← IO.monoNanosNow
    Farkas.Telemetry.emit <| Farkas.Telemetry.row [("ty","\"cost-direct-roundtrip\""),("source",Farkas.Telemetry.jstrEsc (← getFileMap).source),("start_ns",toString exported),("end_ns",toString answered),("answer",answer.trimAscii.toString)]
    let searched ← IO.monoNanosNow
    let .ok j := Json.parse answer | throwError "invalid oracle response"
    let .ok cj := j.getObjVal? "cert" | throwError "oracle failure"
    let cert ← getArray cj
    checkCertificate cfg goal carrier raw (← atoms.get) cert
    let checked ← IO.monoNanosNow
    if (← IO.getEnv "FARKAS_CORPUS_FILE").isSome then
      Farkas.Telemetry.emit <| Farkas.Telemetry.row
        [("ty","\"direct-oracle\""),("source",Farkas.Telemetry.jstrEsc (← getFileMap).source),
         ("export_ns",toString (exported-start)),("search_roundtrip_ns",toString (searched-exported)),
         ("check_ns",toString (checked-searched)),("oracle",answer.trimAscii.toString)]

def run (nlin onlyOn : Bool) (args : List Expr) (cfg : LinarithConfig) : TacticM Unit := do
  if (← IO.getEnv "GPU_ARITHMETIC_ORACLE").isNone then throwUnsupportedSyntax
  let saved ← saveState
  try
    commitIfNoEx do liftMetaFinishingTactic <| solve nlin onlyOn args cfg
  catch e =>
    if (← IO.getEnv "FARKAS_CORPUS_FILE").isSome then
      Farkas.Telemetry.emit <| Farkas.Telemetry.row [("ty","\"direct-oracle-fallback\""),("source",Farkas.Telemetry.jstrEsc (← getFileMap).source),("error",Farkas.Telemetry.jstrEsc (← e.toMessageData.toString))]
    saved.restore
    throwUnsupportedSyntax

elab_rules : tactic
  | `(tactic| linarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => withMainContext do
    if !(Lean.Parser.Tactic.getConfigItems cfg.raw).isEmpty then throwUnsupportedSyntax
    let args ← ((args.map (Syntax.TSepArray.getElems)).getD {}).mapM (elabTermWithoutNewMVars `linarith)
    let cfg := (← Mathlib.Tactic.elabLinarithConfig cfg).updateReducibility bang.isSome
    run false o.isSome args.toList cfg
elab_rules : tactic
  | `(tactic| nlinarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => withMainContext do
    if !(Lean.Parser.Tactic.getConfigItems cfg.raw).isEmpty then throwUnsupportedSyntax
    let args ← ((args.map (Syntax.TSepArray.getElems)).getD {}).mapM (elabTermWithoutNewMVars `nlinarith)
    let cfg := (← Mathlib.Tactic.elabLinarithConfig cfg).updateReducibility bang.isSome
    run true o.isSome args.toList cfg
end GpuArithmetic.CostOracle
