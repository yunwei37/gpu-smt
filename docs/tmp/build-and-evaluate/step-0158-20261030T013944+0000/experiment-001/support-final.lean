/- Test-only whole-candidate differential support;no production interception. -/
import FailureTransition
open Lean Meta Elab Tactic
open GpuSmt.FailureTransition

namespace GpuSmt.FailureDifferential

private def emit (fields : List (String × Json)) : IO Unit :=
  IO.eprintln <| "[gpu-smt-failure-diff] " ++ (Json.mkObj fields).compress

elab "differentialMutation" : tactic => do
  discard <| Core.mkFreshUserName (Name.mkSimple "differential")
  let orphan ← mkFreshExprSyntheticOpaqueMVar (mkConst (Name.mkSimple "True"))
  modifyThe Term.State fun s => { s with pendingMVars := orphan.mvarId! :: s.pendingMVars }
  logInfo "diagnostic before ordinary failure"
  setGoals []
  throwError "ordinary differential failure after state changes"

elab "differentialHeartbeat" : tactic =>
  Core.throwMaxHeartbeat (Name.mkSimple "differential") (Name.mkSimple "maxHeartbeats") 1

elab "failure_probe " inner:tactic : tactic => do
  let mode := (← IO.getEnv "GPU_SMT_FAILURE_DIFF_MODE").getD "original"
  if mode == "original" then
    emit [("event",toJson ("original" : String))]
    evalTactic inner
  else if mode == "default_off" then
    emit [("event",toJson ("default_off" : String))]
    discard <| capture inner
  else if mode == "record" || mode == "replay" then
    let result ← capture inner true
    match result with
    | none =>
      emit [("event",toJson ("normal_return" : String))]
    | some record =>
      if mode == "record" then
        emit [("event",toJson ("recorded_failure" : String))]
        throw record.exception
      else
        -- Controlled producer in this SAME candidate;full restore keeps the
        -- original reader/syntax identities. Producer wall/HB cost is not free.
        discard <| Tactic.withRestoreOrSaveFull
          (some ((),record.input.state)) (pure ())
        let some exception ← tryReplay record inner true |
          throwError "controlled replay unexpectedly missed"
        emit [("event",toJson ("hit" : String))]
        throw exception
  else
    throwError "unsupported differential test mode"

elab "#audit_candidate" : command => do
  let env ← getEnv
  let fields := match env.find? (Name.mkSimple "candidateProof") with
    | some (.thmInfo info) =>
      [("found",toJson true),("direct_sorry",toJson info.value.hasSorry)]
    | _ => [("found",toJson false)]
  emit <| ("event",toJson ("proof_audit" : String)) :: fields

end GpuSmt.FailureDifferential
