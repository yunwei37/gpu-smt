# Step0015 — task-aware ordering in the reusable engine

Phase BUILD_AND_EVALUATE. Previous turn is progress: reproducible ordering defect
fixed, actual native CI passes, real retained4.9host compiles/links. None of that
is a new whole-population performance result. Root-only work/self-review.

## EXPERIMENT_GATE

Fixed four RQs/user goal unchanged. Continue workload-layer candidate scheduling.
Existing data show142solvable/102unsolved tasks;17of83timeouts are in solvable
groups. First-success can avoid redundant checked work, but cannot remove
unsolvable-group costs. Ordinary round-robin is prior technique, not novelty.

Re-analyze existing fixed HTTP-span records for task-first-success event time
and same-task simultaneous work under flat/interleaved source order. This is
retrospective optimistic modeling, not physical CPU/wall/Amdahl evidence.
Implement batch-aware priorities as a backward-compatible default trait method;
a composable TaskInterleave wrapper delegates ranking/memory forecasts and
interleaves same-task candidates only in first-success mode. No fixed per-task
concurrency cap, native rejection rule, prefix/certificate sharing or oracle.

Add internal per-task accepted-decision timestamps/unsolved tasks to measurement
reports. They are internal availability, not streamed client delivery: current
HTTP/CLI batch replies return after the batch. Name returned-row throughput so
cancelled/cache/coalesced rows cannot masquerade as native checks.

Preserve active original native group283334/birth134434505 and frozen sources.
No second native collection. Actual new-resource/full pairs stay pending after
retirement; no threshold, deadline or closure criterion.

## WRITE_GATE

Update architecture/API/benchmark/examples for real methods and explicit scopes.
No scientific-contract rewrite or whole-paper/milestone claim at this dependency
boundary. No frozen CPU oracle/old GPU counterexample experiments are expanded.

## REVIEW_GATE

Root self-review only. Check default policy behavior/API compatibility, invalid
priority vectors, ranking/memory delegation, all-mode noncancellation, exact
caller/result identity, incomplete-vs-accepted decisions and complete retirement.
Existing native differential CI must continue passing. Goal remains active.

## Actual local boundary

The composable batch policy/CLI and internal task-availability accounting are
implemented. All33ordinary tests and6validation commands pass at
artifacts/rust-engine-2026-10-25/validation-20261025T112606. The Rust public-policy
example matches every original7808ID against expected original/interleaved order
in both consumer modes, without native execution. Core documentation links pass.

The native CI control uses matching propositions within each task, distinguishes
admission from checked acceptance, preserves unresolved-task exhaustion/raw
responses and verifies retirement. It remains locally ignored during the old
group; exact-head CI is the next evidence. Retrospective timing labels have been
clarified to no observed success, never theorem unsolvability; prior raw metadata
are preserved. No new scientific/performance conclusion or independent audit.

## Actual native CI result

Implementation commit d5ed7c6f998f259ad173ec7323ad6702ce1db803 passes
engine CI40189403240 and benchmark-smoke40189403249. Rust checks pass and
both actual native tests execute (2passed,0ignored). The first native test now
runs the task-aware policy in all-mode and first-success mode: checked
same-proposition siblings, admission retained as incomplete, rejected-only task
exhaustion, raw-response equality for executed controls and final retirement.
The prepared-parent concurrent/timeout/lifecycle native test still passes.
Raw native log and terminal CI metadata are retained here.

This closes this implementation dependency only. No actual full-population
task-aware throughput or client-delivery improvement has been measured.
