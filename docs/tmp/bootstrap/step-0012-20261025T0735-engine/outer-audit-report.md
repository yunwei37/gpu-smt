# Step0012 outer audit — root self-review

User explicitly requires this thread alone. Scope is new Rust engine and
dynamic-resource contract; historical capture retained. No independent audit.
Architecture is a plan, not implementation or a performance result. Safe COW,
new-resource native differential parity and full throughput remain open.

## Implemented boundary and validation — 2026-10-25

Four Rust crates now implement typed contracts, joint admission/global priority
queue, measured RSS watchdog, owned PID/birth history, exclusive requeue,
exact native result/in-flight sharing, all versus first-success consumers,
fresh native process transport and local HTTP/JSONL adapters.
Idle native preparation descendants are included in RSS. Waiting forecasts
refresh from actual observations; queued jobs do not each scan/proc.
Last-subscriber cancellation waits for backend retirement before result/clock.

All18unit/integration/process/HTTP checks pass; no whole-population native
semantic or speedup conclusion follows. One native differential test remains
explicitly ignored locally to preserve the healthy existing full collection;
dedicated pinned official Lean4.18/REPL CI runs that contract separately.
Formatting, warning-free Clippy, warning-free docs and executable/help pass.
Exact receipts/logs are artifacts/rust-engine-2026-10-25/validation-20261025T082239.
Low-threshold real RSS fault injection exercises kill/reap/exclusive retry,
not just mocked counters. Backend preparation is fresh, not COW/one Mathlib
load. Detector/prepared-state traits do not implement those methods.

Self-review found/fixed malformed-response acceptance, cancellation/retirement
under-counting, idle-memory omission, stale forecasts serializing a first batch,
and per-waiter process scanning. Remaining limitations: native parity outside
the core contract, safe COW, source model calibration and multi-node work.
Source consists of~1.8K production Rust lines and~0.8Ktest lines for four
crates/protocols. Shared fixture implementations serve multiple scenarios;
no per-feature helper service/Workspace/runner or unused dependency layer.
No foreign dirty file, historical source/raw result or CPUoracle code changed.
This is a reviewed implementation boundary, not a completed research objective.

## Follow-up root self-review

Verified real native core-contract CI on f016161, without treating three proof controls as full-population parity. Found/fixed supervisor CPU-accounting escape before any new-resource full measurement: runtime is now constructed only after its thread inherits the selected mask. Added executable-thread affinity regression. Complete request latency includes ranking from batch entry. No other Agent or native AI session used.

## Hardware/telemetry self-review

Rechecked stdout/log separation, actual thread affinity inheritance, full-core exclusive semantics, attempt PID/birth/preemption provenance and admission/retirement. Latest20tests all pass; read raw nativeCI success for f016161 without pooling with new resource-point evidence. Input preparation for42reruns is not execution. Remaining safeCOW, full matched throughput/native parity and source-cost learning remain open; no independent audit or novelty claim.

## Capture/comparison self-review

Root-only self-review of the measurement addition: reject changed population/timeouts/environment/aggregate hardware; compare identities rather than counts; preserve operational outcomes and retry cost; no per-candidate parity claim for first-success consumers; no concurrency phase sum presented as end-to-end clock. A real subprocess fixture exercises capture/native retirement; fixture output is not Lean proof evidence. Official nativeCI remains separate. No independent audit claimed.

## Exact-duplicate existing-data result

Direct UTF8 comparison over all 7808 original miniF2F sources finds 7791 unique
sources; only 18 literal None failures duplicate. 17 repeated historical intervals
sum to 13.337753652s (0.03093% of cumulative native HTTP spans), not lifecycle
savings. Raw duplicate IDs/statuses, source/command and result-review are retained
under artifacts/engine-resource-profile-2026-10-25/exact-duplicates. No substantive
proof duplication or large exact-cache opportunity found; no new proof collection.
Current engine code e010988 passes its actual Rust/native CI jobs. All four
research directions remain active, no stopping criterion or independent audit.
