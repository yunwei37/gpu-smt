/- Native semantic qualification input based on the prepared step0141 control.
   Custom tactic,not an expensive-workload measurement or production cache. -/
import Lean

open Lean Meta Elab Tactic

namespace GpuSmt.FailureReplayBoundary

elab "mutatingOrdinaryFailure" : tactic => do
  discard <| Core.mkFreshUserName `failureProbe
  setGoals []
  throwError "ordinary failure after changing goals"

private def catchOrdinary (action : TacticM Unit) : TacticM Bool :=
  tryCatchRuntimeEx
    (do action; pure false)
    (fun ex => do
      if ex.isRuntime || ex.isInterrupt then throw ex
      match ex with
      | .error .. => pure true
      | _ => throw ex)

elab "checkFailureReplayBoundary" : tactic => do
  let initial ← Tactic.saveState
  let initialGoals ← getGoals
  if initialGoals.isEmpty then throwError "control requires a goal"
  let beforeScope := (← getThe Core.State).nextMacroScope
  let failed ← catchOrdinary (evalTactic (← `(tactic| mutatingOrdinaryFailure)))
  let nativeGoals ← getGoals
  let nativeScope := (← getThe Core.State).nextMacroScope
  unless failed && nativeGoals.isEmpty && nativeScope > beforeScope do
    throwError "native post-failure-state control did not engage"

  -- Ordinary backtracking restoration,not full snapshot replay.
  -- Restore goals without rewinding non-backtracked fresh-name state.
  initial.restore (restoreInfo := true)
  let replayFailed ← catchOrdinary
    (throwError "ordinary failure after changing goals")
  let replayGoals ← getGoals
  unless replayFailed && replayGoals == initialGoals && replayGoals != nativeGoals do
    throwError "exception-only replay counterexample did not engage"

-- Expected after native qualification: checked acceptance,without sorry.
-- The custom failure is caught solely to compare post-state with a stub.
-- Neither failure proves the target false.
example : True := by
  checkFailureReplayBoundary
  trivial

end GpuSmt.FailureReplayBoundary
