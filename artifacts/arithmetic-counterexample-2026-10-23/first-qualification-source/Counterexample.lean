import Init.System.Mutex
import Mathlib.Tactic.Linarith.Frontend

open Lean Meta Elab Tactic
namespace ArithmeticCounterexample

private def arr (tag : String) (xs : List Json := []) : Json :=
  Json.arr ((toJson tag :: xs).toArray)

private def domain (e : Expr) : MetaM String := do
  let ty ← instantiateMVars (← inferType e)
  if ty.isConstOf ``Nat then return "nat"
  if ty.isConstOf ``Int then return "int"
  if ty.isConstOf ``_root_.Rat then return "rat"
  if ty.isConstOf `Real then return "real"
  throwError "unsupported arithmetic type"

private partial def term (vars : IO.Ref (Array (Expr × String))) (e : Expr) : MetaM Json := do
  let e ← instantiateMVars e
  if e.hasExprMVar then throwError "unassigned arithmetic metavariable"
  let ty ← domain e
  if let .fvar fid := e then
    let decl ← getLocalDecl fid
    if let some value := decl.value? then return ← term vars value
    let all ← vars.get
    if let some i := all.findIdx? (fun x => x.1 == e) then return arr "v" [toJson i]
    vars.set (all.push (e,ty))
    return arr "v" [toJson all.size]
  if let some q := e.rat? then
    return arr "q" [toJson (toString q.num),toJson (toString q.den)]
  match e.getAppFnArgs with
  | (``HAdd.hAdd, #[_,_,_,inst,a,b]) =>
    if inst.hasFVar then throwError "local arithmetic instance"
    return arr "+" [← term vars a, ← term vars b]
  | (``HSub.hSub, #[_,_,_,inst,a,b]) =>
    if inst.hasFVar then throwError "local arithmetic instance"
    return arr (if ty == "nat" then "nat_sub" else "-") [← term vars a, ← term vars b]
  | (``HMul.hMul, #[_,_,_,inst,a,b]) =>
    if inst.hasFVar then throwError "local arithmetic instance"
    return arr "*" [← term vars a, ← term vars b]
  | (``Neg.neg, #[_,inst,a]) =>
    if inst.hasFVar then throwError "local arithmetic instance"
    return arr "neg" [← term vars a]
  | (``HDiv.hDiv, #[_,_,_,inst,a,b]) =>
    if inst.hasFVar || ty == "nat" || ty == "int" then throwError "unsupported division"
    if let some q := b.rat? then
      if q != 0 then
        let inverse := q⁻¹
        return arr "*" [← term vars a, arr "q" [toJson (toString inverse.num),toJson (toString inverse.den)]]
    throwError "nonconstant or zero division"
  | (``HPow.hPow, #[_,_,_,inst,a,n]) =>
    if inst.hasFVar then throwError "local arithmetic instance"
    if let some exponent := n.nat? then
      if exponent ≤ 8 then return arr "pow" [← term vars a,toJson exponent]
    throwError "unsupported exponent"
  | (name,args) =>
    if (name == ``Nat.cast || name == ``Int.cast || name == ``Int.ofNat) && !args.isEmpty then
      return ← term vars args[args.size-1]!
    throwError "unsupported arithmetic head {name}"

private partial def proposition (vars : IO.Ref (Array (Expr × String))) (e : Expr) : MetaM Json := do
  let e ← instantiateMVars e
  if e.hasExprMVar then throwError "unassigned proposition metavariable"
  if e.isConstOf ``True then return arr "true"
  if e.isConstOf ``False then return arr "false"
  match e.getAppFnArgs with
  | (``And, #[a,b]) => return arr "and" [← proposition vars a, ← proposition vars b]
  | (``Or, #[a,b]) => return arr "or" [← proposition vars a, ← proposition vars b]
  | (``Not, #[a]) => return arr "not" [← proposition vars a]
  | (``Eq, #[_,a,b]) => return arr "eq" [← term vars a, ← term vars b]
  | (``Ne, #[_,a,b]) => return arr "ne" [← term vars a, ← term vars b]
  | (``LT.lt, #[_,inst,a,b]) =>
    if inst.hasFVar then throwError "local order instance"
    return arr "lt" [← term vars a, ← term vars b]
  | (``LE.le, #[_,inst,a,b]) =>
    if inst.hasFVar then throwError "local order instance"
    return arr "le" [← term vars a, ← term vars b]
  | (name,_) => throwError "unsupported proposition {name}"

private def exportGoal : TacticM Json := withMainContext do
  let vars ← IO.mkRef #[]
  let target ← proposition vars (← getMainTarget)
  let mut hyps : Array Json := #[]
  for decl in ← getLCtx do
    if ← isProp decl.type then
      hyps := hyps.push (← proposition vars decl.type)
  let mut varDescriptions : Array Json := #[]
  for (e,ty) in ← vars.get do
    let name ← match e with
      | .fvar id => pure (← getLocalDecl id).userName.toString
      | _ => pure "unexpected"
    varDescriptions := varDescriptions.push (Json.mkObj [("name",toJson name),("domain",toJson ty)])
  return Json.mkObj [("variables",Json.arr varDescriptions),("hypotheses",Json.arr hyps),("goal",target)]

private abbrev Child := IO.Process.Child {stdin := .piped,stdout := .piped,stderr := .inherit}
initialize idle : IO.Mutex (List Child) ← IO.Mutex.new []
private def query (q : Json) : IO Json := do
  let cached ← idle.atomically do
    match ← get with
    | [] => pure none
    | x :: xs => set xs; pure (some x)
  let c ← match cached with
    | some c => pure c
    | none => do
      let some worker ← IO.getEnv "GPU_SMT_CEX_WORKER" | throw (IO.userError "missing counterexample worker")
      IO.Process.spawn {cmd := "/usr/bin/python3", args := #[worker], stdin := .piped, stdout := .piped, stderr := .inherit}
  try
    c.stdin.putStrLn q.compress
    c.stdin.flush
    let line ← c.stdout.getLine
    let .ok reply := Json.parse line | throw (IO.userError "invalid counterexample worker reply")
    idle.atomically (modify (c :: ·))
    return reply
  catch ex =>
    try c.kill catch _ => pure ()
    try discard c.wait catch _ => pure ()
    throw ex

syntax (name := guardArithmetic) "cex_guard" str tactic : tactic

elab_rules : tactic
  | `(tactic| cex_guard $source:str $original:tactic) => do
    let mode := (← IO.getEnv "GPU_SMT_CEX_MODE").getD "off"
    if mode != "off" then
      let saved ← saveState
      let started ← IO.monoNanosNow
      let payload ← try
          let ast ← exportGoal
          pure (Json.mkObj [("supported",toJson true),("ast",ast)])
        catch ex =>
          pure (Json.mkObj [("supported",toJson false),("reason",toJson (← ex.toMessageData.toString))])
      saved.restore
      let reply ← try
          query (Json.mkObj [("source_id",toJson source.getString),("mode",toJson mode),
            ("entry_ns",toJson started),("export_ns",toJson ((← IO.monoNanosNow)-started)),("payload",payload)])
        catch _ => pure Json.null
      if (reply.getObjValAs? Bool "exact_counterexample").toOption == some true then
        throwError "arithmetic goal refuted by an exact checked counterexample"
    evalTactic original

end ArithmeticCounterexample
