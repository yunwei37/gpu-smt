# Experimental interval closing continuation

This prototype explores the measured interval_cases hotspot. It is not enabled
by the Rust service, does not override Mathlib tactics, and does not change any
retained original candidate. It is not a reliable request-rejection detector or
a demonstrated performance result.

Mathlib4.9 constructs every case metavariable and its bisection tree before
later tactics run. IntervalContinuation.lean uses the same native Methods and
proof constructors while visiting leaves depth-first. The caller supplies a
continuation that must close the current leaf. A failure stops traversal; the
frontend restores saved tactic state before propagating the failure.
Successful calls leave a native proof for the normal Lean checker.
The implementation has only been compiled, not behavior-qualified.

The opt-in syntax is interval_cases_then n => omega (for example). It supports
inferred Nat/Int bounds and closing single-leaf continuations, not arbitrary
native all_goals/first/try/goal-order-dependent programs or an automatic
transformation of interval_cases chains. Tactic failure is not proof that the
mathematical target is false. Numeric range size is never used as rejection.
All-positive traversal still constructs a growing proof; no logarithmic total
memory or unchanged resource-limited outcome is asserted. Native case tags are
carried from the root through leaf construction.

[Actual compile attempts and limits](../../../artifacts/hotspot-mechanisms-2026-10-25/interval-continuation/result-review.md)
retain both the initial reserved-name parser failure and the successful pinned
4.9 build. Compiling metaprogram definitions does not validate the generated
proof terms on any original candidate. The prepared qualification input is
unexecuted. Run it only in the sole collection slot, with original diagnostics,
acceptance/incomplete/failure sets,cleanup and resource/clock evidence.
Kernel-checked success/failure/rollback, nested scopes and native accepted-set
comparison must precede any original-population integration.

Lazy traversal is a standard technique, not itself a novelty claim. The open
question is whether this particular expensive native work can be avoided in
actual failed candidates, and whether any benefit survives full-flow costs.
No CPU oracle/GPU narrow-kernel route or another verifier system is reopened.

## Executed development qualification

The first runtime qualification now executes18native frontend controls
(9native/prototype pairs), including kernel-checked successful examples,
rejected/unsolved leaves, rollback and admitted proofs. All9status pairs match;
the sorry pair remains incomplete. See
[retained result](../../../artifacts/hotspot-mechanisms-2026-10-25/interval-continuation/qualification-001/result-review.md).
This is not original-population parity, a reliable timeout detector or a
performance result. Diagnostic multiplicity differs on the failed-leaf pair.
