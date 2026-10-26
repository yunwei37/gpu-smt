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
The implementation has nine small native paired controls, detailed below;
original-cohort behavior and performance remain unmeasured.

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
proof terms on any original candidate. The initial small qualification now executes below. Original-cohort execution
still uses the sole collection slot, with original diagnostics,
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

## Before-expansion domain diagnostics

IntervalProfile.lean is a separate opt-in observer. It inspects numeric native
bounds in saved/restored state,constructs no leaves,then delegates the original
interval_cases. Actual control qualification and exact48-source/116-call
preparation are retained under artifacts/hotspot-mechanisms-2026-10-25/
interval-bound-profile/. The observer is not the on-demand traversal and does
not classify failure/timeout. Original48runtime fractions remain unmeasured.


## Original-cohort preparation and association limits

`prepare-cohort.py` reads retained native Syntax and complete source, not a
regex reconstruction of proof grammar. The [prepared original48 experiment](../../../artifacts/hotspot-mechanisms-2026-10-25/interval-continuation/original48-preparation/README.md)
contains original/import-control/lazy batches and exact inverse edit maps.
Actual native parsing confirms48 sources/116 prototype sites with correct
variables/spans, while executing zero candidate proofs.

Native `<;>` is left-associative; its `all_goals` accumulator completes each
stage before the next. Reassociation into nested closing continuations changes
that interleaving and may change fresh metavariable names, shared state and
resource-limited outcomes. This is an explicit experimental variant, not a
transparent automatic rewrite or a sufficient failure certificate. It is
disabled in the engine. Keep unknown fallback; do not infer guaranteed timeout
from syntactic range count or failed speculative leaves.

## First-stage map (runtime qualification pending)

[IntervalMap.lean](IntervalMap.lean) adds a separate opt-in form which allows
surviving goals. It interleaves one pruning stage with interval construction,
collects survivors in leaf order, and leaves later stages outside:

```lean
(interval_cases_map m => (interval_cases_map n => norm_num at h)) <;> omega
```

Unlike interval_cases_then, the callback need not close each goal. Native
all_goals handles callback errors/recovery; propagated construction errors
restore tactic entry state. Errors are never interpreted as a mathematical
counterexample or a guaranteed native failure. Surviving goals and completed
proof terms can still consume large memory; bounded live memory is not proved.

Prepare the retained original48 source variants with:

```sh
python3 bench/lean-failure-profile/interval-continuation/prepare-cohort.py \
  --mode map --inputs ORIGINAL48.json.gz --sites NATIVE_SITES.json --out OUTPUT
```

Default mode remains the previous closing-continuation preparation, with all
four retained source artifacts byte-identical. The new mode changes only the
native interval chain and its first subsequent tactic; exact suffix bytes,
comments, variable order and inverse edits are checked. All48sources/116sites
pass native parsing. First stages:19norm_num,17omega,12simp_all. Only the19
norm_num sources have a later stage suffix. [Evidence and pending controls](../../../artifacts/hotspot-mechanisms-2026-10-25/interval-continuation/first-stage-map/README.md).

Definition compilation and parsing do not execute proofs. The22prepared
native/map controls (11pairs) and original48runtime comparison remain pending
the sole acquisition slot. No reliable-failure or speedup result follows.
Native left-associated eager staging and this construction/first-stage
interleaving still differ in metavariable history, recovery, tags and resources;
this is not an automatic service rewrite or transparent rejection path.
