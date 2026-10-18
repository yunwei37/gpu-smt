/- Direct certificate reconstruction experiment. Untrusted AST oracle; native Lean
ring/checker verifies one weighted contradiction. Unsupported cases fall back. -/
import Mathlib.Tactic.Linarith.Frontend
import GpuArithmetic.IntegerAstControl
open Lean Meta Elab Tactic Mathlib.Tactic.Linarith
namespace GpuArithmetic.GoalBatchOracle

private abbrev Child := IO.Process.Child {stdin := .piped, stdout := .piped, stderr := .inherit}
initialize idleDaemons : Std.Mutex (List Child) ← Std.Mutex.new []
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


private structure Prepared where
  goal : MVarId
  carrier : Expr
  raw : Array Expr
  atoms : Array Expr
  request : String
  callId : Nat

private partial def prepare (nlin : Bool) (g : MVarId) : MetaM (Array Prepared) := g.withContext do
  if (← whnfR (← instantiateMVars (← g.getType))).isEq then
    let [a,b] ← g.apply (← mkConst' ``eq_of_not_lt_of_not_gt) | failure
    return (← prepare nlin a) ++ (← prepare nlin b)
  let (goal,pref,nv) ← match ← applyContrLemma g with
    | (none,g) => pure (← g.exfalso,none,none)
    | (some (ty,h),g) => pure (g,some ty,some h)
  goal.withContext do
    let sources ← ((← getLocalHyps).toList).flatMapM collect
    let carrier ← match pref with
      | some ty => pure ty
      | none => sources.firstM fun h => do
        let (_,_,ty,_,_) ← (← inferType h).ineqOrNotIneq?
        pure ty
    unless carrier.isConstOf `Real || carrier.isConstOf ``Rat do throwError "unsupported carrier"
    let atoms ← IO.mkRef #[]
    let mut raw : Array Expr := #[]
    let mut rows : Array String := #[]
    for h in sources do
      if let some row ← item atoms carrier h then
        rows := rows.push row
        raw := raw.push h
    let id ← IO.monoNanosNow
    let request := "{\"source\":" ++ Farkas.Telemetry.jstrEsc (← getFileMap).source ++
      ",\"call_id\":" ++ toString id ++ ",\"nlin\":" ++ (if nlin then "true" else "false") ++
      ",\"hyps\":[" ++ ",".intercalate rows.toList ++ "]}"
    return #[{goal,carrier,raw,atoms := ← atoms.get,request,callId := id}]

initialize batchLogMutex : Std.Mutex Unit ← Std.Mutex.new ()
private def recordBatch (source outcome : String) (goals models checked fallback : Nat)
    (start finish : Nat) (ids : Array Nat) (workers : Nat) (error : String) : IO Unit := do
  if let some path ← IO.getEnv "GPU_SMT_GOAL_BATCH_LOG" then
    batchLogMutex.atomically do
      let f ← IO.FS.Handle.mk path IO.FS.Mode.append
      f.putStrLn <| (Json.mkObj [("source",toJson source),("outcome",toJson outcome),
        ("goals",toJson goals),("models",toJson models),("checked",toJson checked),
        ("call_ids",toJson ids),("numeric_workers",toJson workers),("error",toJson error),
        ("fallback",toJson fallback),("start_ns",toJson start),("end_ns",toJson finish)]).compress
      f.flush

private def runBatch (nlin : Bool) : TacticM Unit := do
  unless (← IO.getEnv "GPU_ARITHMETIC_GOAL_BATCH") == some "1" do throwUnsupportedSyntax
  let goals ← getGoals
  unless goals.length > 1 do throwUnsupportedSyntax
  let saved ← saveState
  let source := (← getFileMap).source
  let start ← IO.monoNanosNow
  let mut models := 0
  let mut checked := 0
  let mut fallback := 0
  let mut ids : Array Nat := #[]
  let mut workers := 0
  try
    let mut prepared : Array Prepared := #[]
    for goal in goals do
      unless ← goal.isAssigned do
        prepared := prepared ++ (← prepare nlin goal)
    models := prepared.size
    ids := prepared.map (·.callId)
    unless models > 1 do throwError "no multiple ready numerical goals"
    let request := "{\"batch\":[" ++ ",".intercalate (prepared.toList.map (·.request)) ++ "]}"
    let answer ← query request
    let .ok reply := Json.parse answer | throwError "invalid batch reply"
    let .ok replies := reply.getObjValAs? (Array Json) "batch" | throwError "missing batch replies"
    unless replies.size == prepared.size do throwError "batch response count"
    let .ok nworkers := reply.getObjValAs? Nat "workers" | throwError "missing worker count"
    workers := nworkers
    let cfg : LinarithConfig := {}
    for (p, response) in prepared.zip replies do
      setGoals [p.goal]
      let beforeCheck ← saveState
      try
        let .ok cj := response.getObjVal? "cert" | throwError "missing coefficient certificate"
        let cert ← getArray cj
        liftMetaFinishingTactic fun goal => goal.withContext <| checkCertificate cfg goal p.carrier p.raw p.atoms cert
        checked := checked + 1
      catch _ =>
        beforeCheck.restore
        -- The prepared contradiction goal stays in this sequential MetaM context.
        -- Native exact search/proof construction remains the fallback authority.
        GpuArithmetic.BatchBaseline.run nlin false [] cfg
        fallback := fallback + 1
    for g in goals do
      unless ← g.isAssigned do throwError "original goal not solved"
    setGoals []
    recordBatch source "checked" goals.length models checked fallback start (← IO.monoNanosNow) ids workers ""
  catch e =>
    saved.restore
    recordBatch source "fallback" goals.length models checked fallback start (← IO.monoNanosNow) ids workers (← e.toMessageData.toString)
    throwUnsupportedSyntax

elab_rules : tactic
  | `(tactic| all_goals linarith) => runBatch false
  | `(tactic| all_goals nlinarith) => runBatch true
end GpuArithmetic.GoalBatchOracle
