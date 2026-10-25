# Step0012 — extensible Rust engine

## Entry and scope
Latest verbatim human request appended to docs/user-instruction.md.
Scope: engine crates/APIs/tests/CI/examples/architecture/contribution/license;
preserve foreign dirty paths, all research data, CPUoracle freeze and healthy
old-resource full7808capture. Rust resources/service; Lean+C internal hooks.
No delegation or independent-audit claim.

## EXPERIMENT / implementation
Full480 retired. Full7808 original scheduling remains live unchanged.
A15second observation measures existing native CPU/RSS without a second proof
workload. Next group uses aggregate48GiB/no fixed per-process cap. Historical
42resourcefailures require separately reported isolated reruns after the live
group. docs/architecture.md defines extension contracts and evidence limits.

## WRITE
Keep initial narrative/fourRQs, document actual implementation and unknowns.

## REVIEW and next
Root self-review only. Architecture establishes no safe COW, acceleration,
native parity or novelty. Continue implementation/tests and publish each
coherent verified boundary. Goal remains active.

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

## Native CI and hardware accounting follow-up

Exact implementation head f016161 passes both engine jobs, including pinned official Lean4.18/REPL raw JSON differential for accepted/rejected/sorry examples, plus retained Z3smoke CI. Full native population parity remains open. Self-review then found the CLI created its Tokio runtime before applying CPU eligibility; the forward fix binds the calling thread before runtime creation so every runtime/native thread stays within the declared CPU budget. A real executable/proc-thread-affinity regression is added. Per-candidate complete latency now begins at batch entry, including policy ranking. Historical capture remains untouched. Subsequent exact-head CI is tracked separately.

## Hardware/telemetry boundary validated

Latest local validation is artifacts/rust-engine-2026-10-25/validation-20261025T084048: all six build/format/Clippy/test/doc/help commands pass,20checks pass and the local raw-native test remains explicitly skipped in favor of the pinned official nativeCI. Runtime/native threads share the chosen mask; resources emit complete1sJSON events to stderr without corrupting stdoutJSONL. Attempt history retains process birth and preemption RSS. Source sorting/queueing/retries/retirement enter per-candidate batch-entry latency. Prepared42unchanged sources are one-candidate-per-line/uncached for the isolated48GiB/all4eligibleCPUs point; no actual rerun has started. Existing full7808group/source/settings remain preserved. New exact-head CI must be checked after this forward commit.
