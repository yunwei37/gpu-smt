# Native error propagation prototype and reviewed23sources

No new logging/diagnostic engine. NativeFailFast.lean is an opt-in proof wrapper
using existing Lean4.9 Term.withoutErrToSorry and Tactic.withoutRecover.
No heuristic,timeout change,global elaborator replacement or engine integration.
Pinned evalAllGoals logs a branch exception and continues when recover=true.
Native tryCatch restores state including messages;an arbitrary observed error
cannot certify request failure. withoutRecover already underlies alternatives.
These primitives are existing functionality,not a scientific novelty.

The hypothesis is that batch verification can avoid further work after errors
ordinary recovery would retain. Accepted-set equivalence/saved-work coverage
are unknown. Recovery-dependent custom tactics,nested postponed terms and
explicit message manipulation may differ. Do not deploy or advertise universal
Lean equivalence. This is not a proof of a false theorem/infinite rewrite/
inevitable timeout or expansion of the frozen closed-goal-tail predicate.

## Source-specific facts

source-review23.json retains exact lemma groups,site counts,existing native
cumulative counters and uncertainty for every source.9have long final inner
calls,including finite sum/distributive expansion,recurrence,gcd unfolding and
Complex normalization hypotheses.14have short final calls:8show thousands of
completed outer simpAll calls plus interval_cases/rcases fanout;5have0returned
outer calls and1has1in induction. Do not call the latter6outer loops.
1816/5006have7static sites;3610has2. Native frames alone do not assign active
source bytes or prove phase/lemma causality. Finite fanout,large counts and
commutativity do not prove divergence. Native simp already orders permutations,
checks unchanged expressions and enforces native step/recursion checks.

## Prepared inputs and actual validation

original23/import-control23/wrapped23.json.gz retain IDs/tasks/full source,
all-mode/no-reuse and the inherited300s default made explicit. Import-only
separates module import from wrapper effects. Add import and indent/wrap root
proof;inverse edits restore original bytes on all23. These are unexecuted.
Initial absent timeout-key failure occurred before batches were written;
repair and preparation script remain. No changed original file.

compile-001 compiles definitions successfully to a separate temporary4.9olean;
zero candidate proofs executed. Combined1s peak41,197,547,520B,zero pressure/
monitor errors under48GiB,CPU11. This is not native differential qualification
or a performance result. Existing release/host and old qualoleans untouched.

After the solepair and42exclusive retries,qualify accepted/rejected/first/try/
cases controls before interpreting original23proof measurements. Keep exact
accepted IDs,native diagnostics,resource outcomes,import/queue/cleanup costs.
Diagnostic stderr is not native acceptance. Existing simp observer remains
responsible for phase/origin timing. No new diagnostics are added here.
Same-thread self-review,not independent audit.71timeout/lean-mlir work remains.
