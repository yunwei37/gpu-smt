# Matched Rust resource-pair preparation — root self-review

## Implemented and executed engineering boundary
A reusable public-API Rust example now owns both native/prepared conditions,
the48GiB runtime monitor and compressed capture helper in the same process
tree. Exact same Batch/Config/FIFO/native context on both sides. Existing
dynamic admission,1s watchdog,preempt/reap/exclusive retry and parent-eviction
logic are reused;no new scheduler/controller or Python runtime admission.
All candidate decisions/operational failures,attempts and native output remain
in compressed Capture records. Comparator checks source/ID/task/timeout/resource
identity. External clocks extend through input decoding,serialization,
compression and compressor wait,whose narrower inner clocks remain labelled.
CPU tick/affinity observations are birth-checked;unavailable fields stay null.
Registered leader count is not busy CPU count or proof of four active workers.

Fmt/Clippy/all-target tests/docs/CLI checks pass(artifacts/rust-engine-2026-10-25/validation-20261025T171032/validation.json):
36ordinary tests pass,4native integration tests explicitly ignored locally
during the retained capture. Two new meaningful fixtures roundtrip real gzip
output/reap its child and record actual ownedRSS. Release build completes.
An actual empty-batch native/prepared pair exercises capture/compare/ownership/
compression with positive sampledRSS and0native leaders. That fixture is
plumbing ONLY,not a proof run,Mathlib preparation,four-worker qualification,
throughput ratio or acceptance result. Raw empty ratios stay in fixture files
and are not admitted as research data.

## Prepared actual original resource point
Freeze references to the canonical7808original inputs(all-mode,reuse=false),
identical source/task/native timeout bytes,48GiBactual aggregateRSS,
CPU8–11/cores_per_worker1. This permits at most4leases,subject to memory and
cleanup. No per-process AS cap or GPU/CPU oracle path is introduced. Exact
command/native project/SDK/host/source references and declared runtime scope
are in preparation/manifest.json. Large JSON is compressed incrementally by
an owned helper to avoid filling the small project volume. Raw results and
partial/interrupted data remain;SIGINT shuts down/reaps native work before
recording interrupted output and does not start the second condition.

This is an own-engine native-fresh/prepared SUPPORT comparison. It cannot be
presented as a strongest warm-service advantage or novelty from preparation.
The current matched native/prepared small Mathlib child controls still have
only two simultaneous children;actual four-native-worker/full population
evidence is pending,not implied by API support or these tests. No original
full pair starts while the retained three-cell scheduler group runs.
Old42bad_alloc retries and the current43-resource-failure cell remain separate
from the new dynamic point. Do not mix old24GiB-AS clocks/labels into it.

## Continuing work
The original group is still nonterminal;preserve its frozen settings.
At its actual completion collect all raw/consumer/failure/memory/retirement
records and pair native/scheduling results,then start the requested original
lean-mlir bv_decide measurement. The original23phase diagnostic and48interval
semantic work remain native runtime nodes. Four directions continue;closed
CPU oracle routes stay frozen. Root self-review,not independent audit.
