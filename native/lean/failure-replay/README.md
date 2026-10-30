# Experimental native ordinary-failure transitions

This opt-in Lean4.9.0-rc1 component is a dependency for backend replay hooks,
not a production failure cache or a new snapshot algorithm. Importing
FailureTransition registers no tactic interceptor and creates no store.
Both capture and tryReplay default off. Stock Rust/CLI/HTTP backends remain off
and do not call this component.

A qualified caller captures a tactic's full native failed state and exception.
Known heartbeat/recursion/interrupt/runtime/internal exceptions are rethrown;
normal returns, including open goals and logged errors, yield no failure record.
After a captured ordinary failure the caller must propagate its exception through
the original failure/backtracking handler. A match never implies a false target.

Replay requires explicit caller qualification and identical retained Core/Meta/
Term/Tactic reader and state objects plus the exact Syntax object. References
are kept alive in the record; IDs/addresses cannot be recycled beneath it.
This is intentionally conservative and can miss reconstructed equal inputs.
In particular, independently created request contexts do not qualify merely
because goals and tactics match. Different complete source FileMaps imply
different Core contexts, so this guard cannot provide cross-source reuse for
those requests. It is a transition primitive, not the proposed semantic
goal-state cache. Cross-candidate identity/diagnostic rebasing and effect
qualification are still required; do not claim a population zero-hit result
or an impossibility bound for broader designs from this guard.
It is **not complete replay qualification**: identical objects may contain mutable
references, and ambient IO, opaque extensions, cancellation/resource observations
and diagnostic effects still require backend-specific analysis. Do not enable
arbitrary tactics based on these pointer tests or the older observed input keys.
Records cannot be serialized or transferred across native processes.

The implementation uses upstream Tactic.withRestoreOrSaveFull for complete state
installation and action-heartbeat debit. It checks current cancellation and
remaining request heartbeats before applying a record. Upstream explicitly calls
snapshot/reuse overhead accounting approximate:
[CoreM.lean](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/CoreM.lean#L212).
There is no exact wall-time or timeout-parity guarantee, no free lookup claim,
and no argument that this existing primitive is novel.

## Finite native controls

Use an existing matching SDK and a PVC output directory; do not compile outputs
into the checkout. For example, set LEAN to that SDK's bin/lean and OUT to the
owned persistent output directory, then:

    mkdir -p "$OUT"
    export LEAN_PATH="$OUT"
    "$LEAN" --root native/lean/failure-replay -T 100000 -o "$OUT/FailureTransition.olean" native/lean/failure-replay/FailureTransition.lean
    "$LEAN" --root native/lean/failure-replay/tests -T 100000 -o "$OUT/Transition.olean" native/lean/failure-replay/tests/Transition.lean

The existing native CI job runs these controls with the pinned4.9SDK, separately
from its4.18stock-REPL tests. No Mathlib population is involved. Controls check
default-off original execution; full failed post-state, exception and diagnostic
restoration; recorded action charge; fresh-name/options/goals/syntax/budget
mismatches; real assumption and simp_all no-progress exceptions; simp_all logged
error and explicit normal-open return; native heartbeat/interrupt/internal
exclusions; and final checked acceptance of True without sorry.

The custom mutating failure injects50000heartbeats to make debit loss observable
without a slow search. It is not a timing result. On G10, deleting post-state
installation or action debit separately caused the intended assertions to fail;
sources/logs are retained in step0156. These controls neither execute the selected
2677sources nor establish their full-state match frequency, cross-candidate reuse,
safe native production integration, accepted-set equality or speedup.
