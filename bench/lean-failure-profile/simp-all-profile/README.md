# Pinned native simp_all phase instrumentation

This opt-in observer is disabled in the engine. It does not replace native
tactics or reject requests. Type hashes,used theorem origins and large round
counts cannot prove an infinite loop or inevitable failure.

## Current executed status

The [original23-source run and per-source attribution](../../../artifacts/hotspot-mechanisms-2026-10-25/original71-native-20261026T125951Z/simp23-analysis/README.md)
are complete. Native and import-only controls all time out. Instrumentation
returns20timeouts and3runtime deep-recursion faults,so it is not qualified as
transparent on the cohort. The historical frontend called these three faults
service rejections;[the classification repair](../../../artifacts/engine-lifecycle-2026-10-26/native-runtime-classification/README.md)
requires a recognized native JSON error before rejection. Original raw
responses/classifications remain retained;these faults are not failure witnesses.

The prior14short-call sources split into8outer-invocation fanout cases and
6inner-round repetition cases. The previous9long-call sources end in
4target and5hypothesis simplifications. Exact call sites,used-origin groups
and censored spans are in the linked result,which owns the per-source facts.
No source has a certified repeating complete native state;reliable-failure
coverage remains0. Do not rerun the cohort merely to repair these guide labels.

## Observer and analysis contract

The opt-in profile_simp_all wrapper delegates the native algorithm and records
monotonic initialization,hypothesis,target,reassertion and clearing phases on
stderr. invocation_byte maps native source positions. Binding power2 keeps
trailing tactic combinators outside the wrapper. Diagnostic timing includes
observer cost and has its own denominator.

Progress snapshots use one process-wide cadence,at most once per second.
The cadence mutex is released before simplification,hashing and output.
Native step counts and serialized Origin.key/tagged Origin values are
investigation hints. Used origins are cumulative within a call;the last seen
origin is not necessarily the cause of a stall. Entry hashes omit complete
proof/cache/metavariable/context/config state and cannot be cycle certificates.
The native simplifier already notices an unchanged post-rewrite expression;
that existing behavior is not a new method.

Successful controls emitted false action_completed fields. These flags remain
unqualified raw diagnostics:do not interpret unwound_actions as real exception
unwinding. Missing/unfinished phases remain censored;legacy records without the
field remain completion_unknown. Phase sums omit untimed loop/logging/service
work and are not an end-to-end time partition.

Reuse analyze.py with --diagnostics DIR and optional --preparation pointing to
the exact preparation.json. The analyzer requires the actual source/terminal
inventory and excludes memory sidecars. It never rejects a candidate. Existing
diagnostics are sufficient;no additional observer/parser is needed for this
completed result.

## Development provenance and limits

[Initial native controls](../../../artifacts/hotspot-mechanisms-2026-10-25/simp-all-profile/result-review.md)
and the retained seven-pair qualification007 apply to their historical observer
sources. A too-restrictive parser precedence and lazy MessageData origin output
were repaired with their failed records retained.
[Native sites and prepared source positions](../../../artifacts/hotspot-mechanisms-2026-10-25/native-sites/result-review.md)
record48simp_all sites across23sources.
[Phase-source dependency validation](../../../artifacts/hotspot-mechanisms-2026-10-25/simp-all-profile/phase-completion-20261026/README.md)
and [prior process-cadence analysis](../../../artifacts/hotspot-mechanisms-2026-10-25/simp-all-profile/process-cadence-20261026/README.md)
are historical preparation,not substitutes for the completed original run.

A future early-failure mechanism still needs a sufficient native-state witness
and preserved enclosing backtracking/fallback. Neither these diagnostics nor
small successful controls establish that witness,cohort equivalence or speedup.


[Continuing-round mechanism evidence](../../../artifacts/hotspot-mechanisms-2026-10-25/original71-native-20261026T125951Z/simp23-analysis/target-progress-20261028.md)
now narrows the six inner-round cases using existing cumulative update fields
and pinned native control flow. It remains distinct from exact target equality,
full-state recurrence and a sufficient candidate-level failure witness.
No new runtime observer/parser or engine rule is added.
