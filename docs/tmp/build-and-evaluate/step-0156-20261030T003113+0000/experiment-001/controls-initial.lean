/- Finite native semantics controls,not workload opportunity or performance. -/
import FailureTransition

open Lean Meta Elab Tactic
open GpuSmt.FailureTransition

set_option maxHeartbeats 100000
set_option maxRecDepth 256

namespace GpuSmt.FailureTransition.Test

elab "transitionMutation" : tactic => do
  discard <| Core.mkFreshUserName (Name.mkSimple "transition")
  let orphan ← mkFreshExprSyntheticOpaqueMVar (mkConst (Name.mkSimple "True"))
  modifyThe Term.State fun s => { s with pendingMVars := orphan.mvarId! :: s.pendingMVars }
  setGoals []
  logInfo "native failed transition diagnostic"
  -- Artificial debit makes loss of recorded action charges observable without
  -- running a slow action. This is not an execution-time measurement.
  IO.addHeartbeats 50000
  throwError "ordinary failure with state effects"

elab "transitionHeartbeat" : tactic =>
  Core.throwMaxHeartbeat (Name.mkSimple "transition-control") (Name.mkSimple "maxHeartbeats") 1

elab "transitionInterrupt" : tactic =>
  throw <| Exception.internal Core.interruptExceptionId

elab "transitionInternal" : tactic => throwUnsupportedSyntax

private def restore (s : Tactic.SavedState) : TacticM Unit := do
  discard <| Tactic.withRestoreOrSaveFull (some ((), s)) (pure ())

private def caught (action : TacticM Unit) : TacticM Exception :=
  tryCatchRuntimeEx
    (do action; throwError "control unexpectedly returned")
    pure

private def ordinaryMessage (ex : Exception) : TacticM String := do
  match ex with
  | .error _ data => data.toString
  | _ => throwError "expected ordinary native exception"

private def requireMiss (record : Record) (stx : Syntax) : TacticM Unit := do
  if (← tryReplay record stx true).isSome then
    throwError "changed or unqualified input was replayed"

elab "checkNativeTransition" : tactic => do
  let entry ← Tactic.saveState
  let stx ← `(tactic| transitionMutation)
  -- Default-off preserves the original failed action and exception path.
  let disabled ← caught (do discard <| capture stx)
  unless (← ordinaryMessage disabled) == "ordinary failure with state effects" do
    throwError "default-off changed the native exception"
  unless (← getGoals).isEmpty do throwError "default-off did not execute original action"
  restore entry

  let some record ← capture stx true | throwError "qualified ordinary failure not captured"
  let message ← ordinaryMessage record.exception
  let failedScope := (← getThe Core.State).nextMacroScope
  let failedPending := (← getThe Term.State).pendingMVars
  unless (← getGoals).isEmpty && !failedPending.isEmpty do
    throwError "native failed post-state did not engage"
  -- The original exception is still propagated through an outer native handler.
  let original ← caught (throw record.exception)
  unless (← ordinaryMessage original) == message do throwError "original handler changed exception"
  restore record.input.state

  unless (← tryReplay record stx).isNone do throwError "replay defaults on"
  discard <| Core.mkFreshUserName (Name.mkSimple "changed-hidden-state")
  requireMiss record stx
  restore record.input.state
  setGoals []
  requireMiss record stx
  restore record.input.state
  withOptions (fun opts => opts.setBool (Name.mkSimple "pp.universes") true) do
    requireMiss record stx
  requireMiss record (← `(tactic| assumption))
  restore record.input.state

  -- A recorded charge larger than the remaining original budget must miss,
  -- without installing the recorded goal/term/core post-state.
  let hugeCore := { record.post.term.meta.core with
    passedHearbeats := (← readThe Core.Context).maxHeartbeats + 1 }
  let huge := { record with post := { record.post with term := { record.post.term with
    meta := { record.post.term.meta with core := hugeCore } } } }
  requireMiss huge stx
  unless (← getGoals) == entry.tactic.goals do throwError "budget miss installed failed state"

  let before ← IO.getNumHeartbeats
  let replayed ← caught do
    let some ex ← tryReplay record stx true | throwError "same retained native input missed"
    throw ex
  let debit := (← IO.getNumHeartbeats) - before
  unless (← ordinaryMessage replayed) == message do throwError "replay changed native exception"
  unless (← getGoals).isEmpty &&
      (← getThe Core.State).nextMacroScope == failedScope &&
      (← getThe Term.State).pendingMVars == failedPending do
    throwError "replay lost failed post-state"
  unless debit >= record.post.term.meta.core.passedHearbeats do
    throwError "replay lost recorded action heartbeat debit"
  restore entry

  -- Real builtin ordinary failure: assumption cannot close True without a hypothesis.
  let assumption ← `(tactic| assumption)
  let some ordinary ← capture assumption true | throwError "builtin ordinary failure not captured"
  let expected ← ordinaryMessage ordinary.exception
  restore ordinary.input.state
  let actual ← caught do
    let some ex ← tryReplay ordinary assumption true | throwError "builtin failure replay missed"
    throw ex
  unless (← ordinaryMessage actual) == expected do throwError "builtin failure diagnostics changed"
  restore entry

  -- Real simp_all unresolved-lemma error is an ordinary failure,not a false goal.
  let simpError ← `(tactic| simp_all only [transitionUnknownLemma])
  let some ordinary ← capture simpError true | throwError "simp_all ordinary error not captured"
  let expected ← ordinaryMessage ordinary.exception
  restore ordinary.input.state
  let actual ← caught do
    let some ex ← tryReplay ordinary simpError true | throwError "simp_all failure replay missed"
    throw ex
  unless (← ordinaryMessage actual) == expected do throwError "simp_all error changed"
  restore entry

  -- A normal builtin return with an OPEN goal is never an ordinary failure.
  let falseGoal ← mkFreshExprSyntheticOpaqueMVar (mkConst (Name.mkSimple "False"))
  setGoals [falseGoal.mvarId!]
  unless (← capture (← `(tactic| simp_all only)) true).isNone do
    throwError "normal open-goal return became a failure record"
  unless !(← getGoals).isEmpty do throwError "open-goal control did not engage"
  restore entry

  let hb ← caught (do discard <| capture (← `(tactic| transitionHeartbeat)) true)
  unless hb.isMaxHeartbeat do throwError "heartbeat exception was recorded or changed"
  restore entry
  let interrupt ← caught (do discard <| capture (← `(tactic| transitionInterrupt)) true)
  unless interrupt.isInterrupt do throwError "interrupt was recorded or changed"
  restore entry
  let internal ← caught (do discard <| capture (← `(tactic| transitionInternal)) true)
  match internal with
  | .internal .. => pure ()
  | _ => throwError "internal exception was recorded or changed"
  restore entry

example : True := by
  checkNativeTransition
  exact True.intro

end GpuSmt.FailureTransition.Test
