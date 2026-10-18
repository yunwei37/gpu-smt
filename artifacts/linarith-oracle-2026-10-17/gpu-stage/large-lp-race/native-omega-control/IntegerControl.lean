import GpuArithmetic.BatchBaseline
import Lean.Elab.Tactic.Omega
open Lean Meta Elab Tactic
namespace GpuArithmetic.IntegerControl
initialize logMutex : Std.Mutex Unit ← Std.Mutex.new ()
private partial def discrete (e : Expr) : Bool :=
  match e.getAppFnArgs with
  | (name, args) =>
    if name == ``Not && args.size == 1 then discrete args[0]!
    else if name == ``LE.le || name == ``LT.lt || name == ``Eq then
      args.size > 0 && (args[0]!.isConstOf ``Nat || args[0]!.isConstOf ``Int)
    else false
private def record (source outcome : String) (start finish : Nat) : IO Unit := do
  if let some path ← IO.getEnv "GPU_SMT_OMEGA_CONTROL_LOG" then
    logMutex.atomically do
      let f ← IO.FS.Handle.mk path IO.FS.Mode.append
      f.putStrLn <| (Json.mkObj [("source",toJson source),("outcome",toJson outcome),
        ("start_ns",toJson start),("end_ns",toJson finish)]).compress
      f.flush
private def run : TacticM Unit := withMainContext do
  unless (← IO.getEnv "GPU_SMT_NATIVE_OMEGA_CONTROL") == some "1" do throwUnsupportedSyntax
  let g ← getMainGoal
  let ty ← instantiateMVars (← g.getType)
  let mut eligible := discrete ty
  if !eligible && ty.isConstOf ``False then
    for localDecl in ← getLCtx do
      unless localDecl.isImplementationDetail do
        if discrete (← instantiateMVars localDecl.type) then eligible := true
  unless eligible do throwUnsupportedSyntax
  let saved ← saveState
  let source := (← getFileMap).source
  let start ← IO.monoNanosNow
  let mut accepted := false
  try
    evalTactic (← `(tactic| omega))
    unless ← g.isAssigned do throwError "omega left the goal open"
    accepted := true
  catch _ =>
    saved.restore
  let finish ← IO.monoNanosNow
  record source (if accepted then "checked" else "fallback") start finish
  unless accepted do throwUnsupportedSyntax
elab_rules : tactic
  | `(tactic| linarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => do
    if bang.isSome || o.isSome || args.isSome || !(Lean.Parser.Tactic.getConfigItems cfg.raw).isEmpty then throwUnsupportedSyntax
    run
elab_rules : tactic
  | `(tactic| nlinarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => do
    if bang.isSome || o.isSome || args.isSome || !(Lean.Parser.Tactic.getConfigItems cfg.raw).isEmpty then throwUnsupportedSyntax
    run
end GpuArithmetic.IntegerControl
