# Ordinary-failure replay is a state transition

The retained Lean4.9.0-rc1 SDK files exactly match official tag bytes in the
adjacent provenance record. This is source provenance,not a runtime gate.

## Runtime catch and ordinary backtracking differ

Core.tryCatchRuntimeEx invokes its handler on the same state reference through
Reader/StateRef lifts. Our observer uses that operation and does not itself
restore pre-tactic state. Core's ordinary backtracking restore covers
environment/messages/info,while fresh-name and other state remain distinct.
[CoreM lines488–510 and249–250](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/CoreM.lean#L488).

## The dispatcher retains the failed evaluator's state

evalTactic records exceptions with their failed state while trying alternatives.
When none succeeds,it restores the chosen failed state before rethrowing.
An ordinary error cannot generally be represented as an exception Boolean
without state effects.
[Dispatcher lines169–194](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Elab/Tactic/Basic.lean#L169).

The prepared failure-post-state-control.lean changes goals and allocates a
fresh name before throwing. An outer control compares that failed execution
with an exception-only stub,then restores the original goal and finishes True.
**Not compiled or executed.** It is custom qualification input,not a selected
expensive tactic,observed cache hit or proof of their post-error behaviour.

## Upstream already provides full snapshots and heartbeat debit

Core.withRestoreOrSaveFull restores full state and adds recorded action
heartbeats. Its source scopes accounting as approximate because some snapshot/
reuse-handler overhead is excluded. Reimplementing the primitive is neither
novelty nor proof of exact timeout parity.
[CoreM lines212–246](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/CoreM.lean#L212).

Term.observing/applyResult already packages an ordinary exception with saved
state. Term state includes pending/synthetic metavariables and error details.
This is elaborator machinery,not demonstrated cross-candidate caching.
[Term state and result application](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Elab/Term.lean#L118).

## Existing incremental entry conditions are stronger than our observed key

The tactic-snapshot invariant requires unchanged state up to tactic entry.
Builtin sequence reuse additionally guards syntax/separators. Its finished
snapshot assignment follows normal evalTactic return;these lines alone do not
establish either generic throwing-failure reuse or its absence elsewhere.
[Term context](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Elab/Term.lean#L266);
[builtin sequence](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Elab/Tactic/BuiltinTactic.lean#L37).

## Consequence for our implementation

The observed key still omits Core fresh-name/resource/trace/message state,
Term context/state and complete Meta state. It already declares itself
observed-input-only. A producer's full snapshot cannot safely replace a
different candidate's state without compatible pre-state and identity mapping;
dropping post-error effects is not justified either.

Finish the real selected capture before estimating supported failure-reuse
cost. For material matches,compare native post-state,subsequent fallback,
diagnostics,acceptance and resource boundaries. Runtime/timeout/RSS/interrupt
outcomes remain excluded. The custom control alone cannot certify real tactics.
No frozen source/module or production cache changed in this audit.
