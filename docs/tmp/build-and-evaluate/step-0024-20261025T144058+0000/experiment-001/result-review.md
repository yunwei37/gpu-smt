# Prepared-parent resource retry — root self-review

The actual source fix adds a defaulted VerificationBackend resource-retry method.
Engine routes a previously interrupted candidate to it only after the earlier
attempt retired and its retry acquired exclusive admission. PreparedRepl holds
its state lock while gracefully retiring the idle parent, records PID/birth in
prepared_evicted, and uses unchanged fresh verification for that attempt within
the remaining request deadline. It does not recreate the parent immediately.
Later ordinary requests can prepare again. Ordinary timeout/cancellation still
preserves prepared state. No Candidate/Execution shape, proof/source semantics,
AS cap, watchdog cadence, total budget or existing native collection changes.

Local actual Rust validation-20261025T144242 passes formatting,Clippy/all-target
compilation,34 ordinary unit/integration/process tests,docs andCLI help.
The existing preemption control now confirms resource-retry routing/history;
the default hook remains exercised by existing unchanged backends.
Four actual Lean tests remain intentionally ignored locally while the original
candidate group owns the collection slot. The existing pinned-native CI will
execute the expanded parent control after this source is pushed: old-parent
retirement,raw-response fresh retry,later re-preparation and final cleanup.
Do not claim these native assertions passed before that exact-head CI finishes.

The targeted paper implementation paragraph renders to PDF with actual compiler
exit0; layout warnings remain, no visual or submission readiness is claimed.
Architecture/API/native/resource documentation agree with the code. No title,
abstract,contribution,RQ or evaluation meaning is changed. This is ordinary
resource recovery, not a novel failure detector or demonstrated throughput gain.

Limits remain: fullMathlib COW-child/whole-population parity and new-resource
throughput are not measured by these tests. The repair applies to the exclusive
resource retry after a concurrent interruption, not a guarantee that every
prepared/fresh resource point accepts the same finite-resource population.
Sampling remains1s and is not a kernel quota. Goal still reports blocked despite
the user's resume message and available API lacks an active transition; actual
root work continues without requesting another resume command. Self-review
was performed by the implementing root, not an independent reviewer.
