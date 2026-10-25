# Runtime-guarded closed-tail prototype

The opt-in early_fail_tail script uses the native separator evaluator. It
inspects only its last adjacent pair. A supported closer is default omega or
a pure interval_cases(identifier) tree with a final default omega. The tail
must be exact(identifier). The runtime must have exactly one unassigned goal.
Every relevant omega/exact/interval/<;>/focus/all_goals handler and macro must
match the pinned4.9 identities; any changed dispatch,unsupported syntax or
multiple goals runs the original remaining script.

Under those native contracts,the closer either raises/logs a native error,
or closes every goal generated from the sole incoming goal. In the second
case exact has no main goal and fails;in the first case the native script
already failed. This is a local unaccepting suffix,not mathematical falsity,
a wall-time lower bound or a completed formal verification of native Lean.
The guarded code propagates an ordinary tactic exception. Enclosing first/try
still runs and may accept the request. A stderr witness is NEVER a global
failure label. The native final status stays authoritative.

The braces are a syntax carrier:the implementation evaluates the original raw
separator list,without bracket close/admit semantics. Prefixes run natively
before actual goal-count and handler checks. This avoids falsely rejecting
constructor-created sibling goals. No source keyword/hash/range cutoff,
shortened timeout,CPU oracle or global builtin replacement is used.

[Actual native controls](../../../artifacts/hotspot-mechanisms-2026-10-25/closed-tail/result-review.md)
include failure,acceptance,siblings,fallback and a runtime omega override.
Scope is the deterministic pinned native tactic context and complete tail
script. Arbitrary metaprograms that erase diagnostics/change semantics outside
that context are not qualified. No default engine rejection plugin is installed.

## Measured original-source scope

[The exact native71-source audit](../../../artifacts/hotspot-mechanisms-2026-10-25/goal-effects/cohort-result-review.md)
finds0supported pairs in48interval and23simp_all timeout sources. In particular,
an outer exact following an inner have proof is not a doomed local suffix.
This prototype has no demonstrated original-timeout coverage or speed benefit.
Keep the local control result separate from original-candidate performance.
