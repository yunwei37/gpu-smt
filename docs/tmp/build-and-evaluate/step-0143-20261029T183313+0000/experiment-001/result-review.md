# Actual native semantic qualification on G10

Pinned stock SDK:Lean4.9.0-rc1,commit be6c4894e0a6,Release,x86_64.
G10 CPU6–7;no fixedAS;no Mathlib population or production caching. Latest user
permits these development tests separately from the formal resource point.

FailureReplayControl.lean exited0 with empty stdout/stderr and produced its
compiled .olean on the PVC. Its checked example proves True after asserting
that the caught ordinary failure leaves the modified empty goal list and an
advanced fresh-name counter,and then restoring the original goal.
ExceptionOnlySubstitute.lean replaces that native action with only the same
error text. It exited1 at the explicit post-failure-state assertion. Raw JSON
diagnostic and both sources are preserved. No operational failure was recast
as a logical false goal.

The two processes actually retired. Combined own-tree nominal1s sampled RSS
was453607424bytes for the baseline and25600000bytes for the fast mutation.
These are samples,not kernel high-water bounds;no budget abort occurred.
Elapsed/setup differences are not performance results and cannot enter the
lab measurement's denominators. Compiled outputs remain at the PVC path in
native-unit-results.json;rebuildable binaries are not added to Git.

This converts step0141's specific control from prepared to actually executed,
without rewriting its historical unexecuted record. It is a custom tactic
counterexample to generic exception-only substitution,not evidence that all
four selected expensive tactics make these effects,nor a complete replay
qualification or measured cache hit. Their actual input-match/cost study is
still incomplete. The useful method obligation is to preserve/validate the
failed transition and fallback,not just the exception payload.
Root self-review only;no independent audit,novelty or venue claim.
