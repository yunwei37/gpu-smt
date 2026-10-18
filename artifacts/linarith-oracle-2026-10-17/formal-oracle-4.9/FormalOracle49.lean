import Init.System.Mutex
/- Direct certificate reconstruction experiment. Untrusted AST oracle; native Lean
ring/checker verifies one weighted contradiction. Unsupported cases fall back. -/
import Mathlib.Tactic.Linarith.Frontend

open Lean Meta Elab Tactic Linarith
namespace GpuArithmetic.FormalOracle49

private abbrev Child := IO.Process.Child {stdin := .piped, stdout := .piped, stderr := .inherit}


initialize idleDaemons : IO.Mutex (List Child) ← IO.Mutex.new []
private def borrowDaemon : IO Child := do
  let cached ← idleDaemons.atomically do
    match ← get with
    | [] => pure none
    | c :: cs => set cs; pure (some c)
  if let some c := cached then return c

  let some bin ← IO.getEnv "GPU_ARITHMETIC_ORACLE" | throw (IO.userError "missing oracle")
  IO.Process.spawn {cmd := bin, stdin := .piped, stdout := .piped, stderr := .inherit}

private def query (request : String) : IO String := do
  let child ← borrowDaemon
  try
    child.stdin.putStr (request ++ "\n")
    child.stdin.flush
    let answer ← child.stdout.getLine
    if answer.isEmpty then throw (IO.userError "oracle EOF")
    idleDaemons.atomically (modify (child :: ·))
    return answer
  catch e =>
    try child.kill catch _ => pure ()
    try discard child.wait catch _ => pure ()
    throw e


initialize traceMutex : IO.Mutex Unit ← IO.Mutex.new ()
private def emit (fields : List (String × Json)) : IO Unit := do
  if let some path ← IO.getEnv "GPU_SMT_FORMAL_ORACLE_LOG" then
    traceMutex.atomically do
      let h ← IO.FS.Handle.mk path .append
      h.putStrLn (Json.mkObj fields).compress
      h.flush

initialize idleNative : IO.Mutex (List Child) ← IO.Mutex.new []
private def nativeQuery (request : String) : IO String := do
  let cached ← idleNative.atomically do
    match ← get with
    | [] => pure none
    | c :: cs => set cs; pure (some c)
  let child ← match cached with
    | some c => pure c
    | none => do
      let some bin ← IO.getEnv "FARKAS_NATIVE_BIN" | throw (IO.userError "missing native oracle")
      let c ← IO.Process.spawn {cmd := bin, stdin := .piped, stdout := .piped, stderr := .inherit}
      c.stdin.putStr "{\"hello\":true}\n"
      c.stdin.flush
      let hello ← c.stdout.getLine
      unless ((Json.parse hello >>= (·.getObjValAs? Nat "farkas_protocol")).toOption == some 1) do
        try c.kill catch _ => pure ()
        try discard c.wait catch _ => pure ()
        throw (IO.userError "native oracle protocol")
      pure c
  try
    child.stdin.putStr (request ++ "\n")
    child.stdin.flush
    let answer ← child.stdout.getLine
    if answer.isEmpty then throw (IO.userError "native oracle EOF")
    idleNative.atomically (modify (child :: ·))
    return answer
  catch e =>
    try child.kill catch _ => pure ()
    try discard child.wait catch _ => pure ()
    throw e

def native : CertificateOracle where
  produceCertificate hyps maxVar := do
    let start ← IO.monoNanosNow
    let rows := hyps.map fun h => Json.arr #[toJson (match h.str with | .eq => "eq" | .le => "le" | .lt => "lt"),
      toJson (h.coeffs.map fun (i,c) => Json.arr #[toJson i,toJson c])]
    let request := (Json.mkObj [("source",toJson (← getFileMap).source),
      ("call_id",toJson start),("maxVar",toJson maxVar),("hyps",toJson rows)]).compress
    let answer ← nativeQuery request
    emit [("type",toJson "native-search"),("source",toJson (← getFileMap).source),
      ("request",toJson request),("answer",toJson answer),
      ("search_ns",toJson ((← IO.monoNanosNow)-start))]
    let .ok j := Json.parse answer | throwError "native response"
    let .ok (.arr entries) := j.getObjVal? "cert" | throwError "no native certificate"
    let mut cert : Batteries.HashMap Nat Nat := {}
    for entry in entries do
      let .arr #[index, .str coeff] := entry | throwError "native certificate entry"
      let .ok index := index.getNat? | throwError "native hypothesis index"
      let some coeff := coeff.toNat? | throwError "native coefficient"
      cert := cert.insert index coeff
    return cert

private def nativeRun (nlin onlyOn : Bool) (args : List Expr) (cfg : LinarithConfig) : TacticM Unit := do
  let cfg := {cfg with oracle := some native}
  let cfg := if nlin then { cfg with preprocessors := some (cfg.preprocessors.getD defaultPreprocessors ++ [(nlinarithExtras : GlobalBranchingPreprocessor)]) } else cfg
  commitIfNoEx do liftMetaFinishingTactic <| Linarith.linarith onlyOn args cfg
  emit [("type",toJson "native-tactic-checked"),("source",toJson (← getFileMap).source)]

private def comparison (e : Expr) : MetaM (Bool × Ineq × Expr × Expr × Expr) := do
  let (pos,e) := if e.isAppOfArity ``Not 1 then (false,e.getArg! 0) else (true,e)
  match e.getAppFnArgs with
  | (``LT.lt, #[ty, _, a, b]) => return (pos,.lt,ty,a,b)
  | (``LE.le, #[ty, _, a, b]) => return (pos,.le,ty,a,b)
  | (``Eq, #[ty, a, b]) => return (pos,.eq,ty,a,b)
  | (``GE.ge, #[ty, _, a, b]) => return (pos,.le,ty,b,a)
  | (``GT.gt, #[ty, _, a, b]) => return (pos,.lt,ty,b,a)
  | _ => throwError "unsupported comparison"

private def atom (ref : IO.Ref (Array Expr)) (e : Expr) : MetaM String := do
  let all ← ref.get
  if let some i := all.findIdx? (· == e) then return s!"[\"a\",{i}]"
  ref.set (all.push e)
  return s!"[\"a\",{all.size}]"

private def rational (q : _root_.Rat) : String :=
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
    if let some exponent := n.nat? then
      return s!"[\"pow\",{← exportExpr ref a},\"{exponent}\"]"
    atom ref e
  | _ => atom ref e

private partial def collect (h : Expr) : MetaM (List Expr) := do
  let ty ← instantiateMVars (← inferType h)
  if ty.and?.isSome then
    return (← collect (← mkAppM ``And.left #[h])) ++ (← collect (← mkAppM ``And.right #[h]))
  return [h]

private def item (ref : IO.Ref (Array Expr)) (carrier h : Expr) : MetaM (Option String) := do
  try
    let (pos, rel, ty, lhs, rhs) ← comparison (← instantiateMVars (← inferType h))
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
  let pf ← mkAppM ``Linarith.lt_irrefl #[pf]
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
    let sources ← (List.join <$> sources.mapM collect)
    let carrier ← match pref with
      | some ty => pure ty
      | none => sources.firstM fun h => do
        let (_,_,ty,_,_) ← comparison (← inferType h)
        pure ty
    unless carrier.isConstOf `Real || carrier.isConstOf ``_root_.Rat do throwError "unsupported carrier"
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
    let request := "{\"source\":" ++ (toJson (← getFileMap).source).compress ++ ",\"call_id\":" ++ toString exported ++ "," ++ (request.drop 1)
    let answer ← query request
    let answered ← IO.monoNanosNow
    let .ok j := Json.parse answer | throwError "invalid oracle response"
    let .ok cj := j.getObjVal? "cert" | throwError "oracle failure"
    let cert ← getArray cj
    checkCertificate cfg goal carrier raw (← atoms.get) cert
    emit [("type",toJson "checked"),("source",toJson (← getFileMap).source),
      ("request",toJson request),("answer",toJson answer),
      ("export_ns",toJson (exported-start)),("search_ns",toJson (answered-exported)),
      ("check_ns",toJson ((← IO.monoNanosNow)-answered))]

def run (nlin onlyOn : Bool) (args : List Expr) (cfg : LinarithConfig) : TacticM Unit := do
  let some mode ← IO.getEnv "GPU_SMT_FORMAL_MODE" | throwUnsupportedSyntax
  if mode != "native" && mode != "direct" then throwUnsupportedSyntax
  let saved ← saveState
  if mode == "direct" then
    try
      commitIfNoEx do liftMetaFinishingTactic <| solve nlin onlyOn args cfg
      return
    catch e =>
      emit [("type",toJson "fallback"),("source",toJson (← getFileMap).source),
        ("error",toJson (← e.toMessageData.toString))]
      saved.restore
  try
    nativeRun nlin onlyOn args cfg
  catch _ =>
    saved.restore
    throwUnsupportedSyntax

elab_rules : tactic
  | `(tactic| linarith $[!%$bang]? $[$cfg]? $[only%$o]? $[[$args,*]]?) => withMainContext do
    if cfg.isSome then throwUnsupportedSyntax
    let args ← ((args.map (Syntax.TSepArray.getElems)).getD {}).mapM (elabLinarithArg `linarith)
    let cfg := (← elabLinarithConfig (mkOptionalNode cfg)).updateReducibility bang.isSome
    run false o.isSome args.toList cfg
elab_rules : tactic
  | `(tactic| nlinarith $[!%$bang]? $[$cfg]? $[only%$o]? $[[$args,*]]?) => withMainContext do
    if cfg.isSome then throwUnsupportedSyntax
    let args ← ((args.map (Syntax.TSepArray.getElems)).getD {}).mapM (elabLinarithArg `nlinarith)
    let cfg := (← elabLinarithConfig (mkOptionalNode cfg)).updateReducibility bang.isSome
    run true o.isSome args.toList cfg
end GpuArithmetic.FormalOracle49
