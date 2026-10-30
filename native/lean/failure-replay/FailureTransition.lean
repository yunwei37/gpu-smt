/- Experimental native transition primitive. Imported alone, it runs no tactics,
registers no hook and enables no cache. Pinned development target: Lean4.9.0-rc1. -/
import Lean

open Lean Meta Elab Tactic

namespace GpuSmt.FailureTransition

private unsafe def sameObjectImpl {α : Type} (a b : α) : Bool := ptrEq a b

@[implemented_by sameObjectImpl]
private opaque sameObject {α : Type} (a b : α) : Bool := false

/-- Strong references to one process's exact retained entry.
Pointer identity is intentionally stricter than observed goal/context equality.
It does not prove absence of effects through mutable references or IO. -/
structure Input where
  coreContext : Core.Context
  metaContext : Meta.Context
  termContext : Term.Context
  tacticContext : Tactic.Context
  state : Tactic.SavedState
  stx : Syntax

/-- Backend-owned ordinary failure with full post-state and recorded action
heartbeats. Native references must not be serialized or moved across processes. -/
structure Record where
  input : Input
  exception : Exception
  post : Tactic.SavedState

private def input (stx : Syntax) : TacticM Input := do
  return {
    coreContext := ← readThe Core.Context
    metaContext := ← readThe Meta.Context
    termContext := ← readThe Term.Context
    tacticContext := ← readThe Tactic.Context
    state := ← Tactic.saveState
    stx
  }

/-- Exact retained object identity for all reader/state layers and stx.
Freshly reconstructed equivalent inputs can miss. Shared mutable referents and
ambient effects remain the qualifying backend's responsibility. -/
def sameRetainedInput (a b : Input) : Bool :=
  sameObject a.coreContext b.coreContext &&
  sameObject a.metaContext b.metaContext &&
  sameObject a.termContext b.termContext &&
  sameObject a.tacticContext b.tacticContext &&
  sameObject a.state.term.meta.core.toState b.state.term.meta.core.toState &&
  sameObject a.state.term.meta.meta b.state.term.meta.meta &&
  sameObject a.state.term.elab b.state.term.elab &&
  sameObject a.state.tactic b.state.tactic &&
  sameObject a.stx b.stx

/-- Capture only a caller-qualified action's ordinary failed transition.
Default-off directly executes the original tactic and propagates any exception.
When enabled, Some returns with the original failed state still installed; its
caller MUST propagate record.exception through the original failure handler.
Known heartbeat/recursion/interrupt/runtime/internal exceptions are rethrown.
Qualification is NOT inferred from tactic text, an observed key or pointer match:
the backend must establish compatible state, effect and diagnostic obligations. -/
def capture (stx : Syntax) (qualifiedByCaller := false) : TacticM (Option Record) := do
  unless qualifiedByCaller do
    evalTactic stx
    return none
  let before ← input stx
  let (exception, post) ← Tactic.withRestoreOrSaveFull none <|
    tryCatchRuntimeEx
      (do evalTactic stx; pure (none : Option Exception))
      (fun ex => pure (some ex))
  match exception with
  | none => return none
  | some ex =>
    if ex.isInterrupt || ex.isRuntime || ex.isMaxHeartbeat || ex.isMaxRecDepth then
      throw ex
    match ex with
    | .error .. => return some { input := before, exception := ex, post }
    | _ => throw ex

/-- Try applying a qualified record in the same retained input. None requests
original execution without installing the recorded state or action debit.
Some(exception) has applied full post-state and original action heartbeats:
rethrow it through the native failure/backtracking path, NEVER return tactic
success or a whole-source verdict. Upstream snapshot/reuse overhead accounting
is approximate; this primitive does not promise exact timeout or wall parity.
Caller qualification defaults off and must also exclude external/mutable effects
and operational diagnostics not identified by the native exception predicates. -/
def tryReplay (record : Record) (stx : Syntax)
    (qualifiedByCaller := false) : TacticM (Option Exception) := do
  unless qualifiedByCaller do return none
  unless sameRetainedInput record.input (← input stx) do return none
  Core.checkInterrupted
  let ctx ← readThe Core.Context
  let used := (← IO.getNumHeartbeats) - ctx.initHeartbeats
  let charge := record.post.term.meta.core.passedHearbeats
  if ctx.maxHeartbeats != 0 && used + charge > ctx.maxHeartbeats then
    return none
  let (exception, _) ← Tactic.withRestoreOrSaveFull
    (some (record.exception, record.post)) (pure record.exception)
  return some exception

end GpuSmt.FailureTransition
