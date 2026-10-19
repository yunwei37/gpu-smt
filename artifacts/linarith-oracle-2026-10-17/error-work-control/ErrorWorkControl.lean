import Mathlib

open Lean Elab Tactic

namespace GpuSmt.ErrorWorkControl

/-- A diagnostic continuation guard, not a proof cache or no-recovery mutation. -/
syntax (name := errorWorkControl) "error_work_control " "in " tactic : tactic

elab_rules : tactic
  | `(tactic| error_work_control in $inner:tactic) => do
    let alreadyErrors := (← getThe Core.State).messages.hasErrors
    let started ← IO.monoNanosNow
    try
      if alreadyErrors then
        throwError "candidate already has Lean errors before this tactic"
      else
        evalTactic inner
    finally
      let finished ← IO.monoNanosNow
      logInfo m!"ERROR_WORK_CONTROL prior_errors={alreadyErrors} skipped={alreadyErrors} elapsed_ns={finished - started}"

end GpuSmt.ErrorWorkControl
