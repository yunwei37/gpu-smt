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

## Exact source native CI completed — 2026-10-25T14:52Z

Source6e3d858919ff0309ab9306e0fbf0da26896abfe8 passes the actual
[engine/native workflow](https://github.com/yunwei37/gpu-smt/actions/runs/40203946559)
and smoke40203946557. Rust formatting/Clippy/tests/docs pass. All four actual
native tests execute:4passed,0failed,0ignored in3.36s. The expanded prepared
parent test observes old-parent retirement, unchanged raw fresh native response,
a new parent for later ordinary work and complete cleanup. The raw native job
log and terminal receipt are retained in artifacts/prepared-engine-2026-10-25/
resource-retry. The earlier pending-CI text records the state at source push.

This qualifies the declared Lean4.18 Init/Timer lifecycle context. It does not
execute Mathlib candidates,42isolated retries or a throughput matrix, and does
not prove all finite-resource populations preserve the same timeout/resource
labels. Root self-review remains self-review; CI is not an independent scientific
audit. No performance conclusion or completion of the research goal follows.
