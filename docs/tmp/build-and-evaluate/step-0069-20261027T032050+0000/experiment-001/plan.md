# Plan — complete the native/Mathlib-derived engine resource pair

RQ2 native behavior and RQ3 equal-resource service benefit remain open. The
previous complete native cell cannot pair with its ENOSPC-truncated prepared
cell. Since then a real shutdown/admission race was repaired. Run both
conditions with one frozen current binary/source, preserving the old data as
partial and using existing/tmp for all large raw output.

Reuse the existing resource_pair Rust example, canonical7808 original Batch,
original Lean4.9rc1 REPL/Mathlib/prepared host, original order native then
prepared, all-mode,no source normalization,no reuse and original300s deadline.
Both conditions use actual48GiB aggregate RSS,CPU8–11,one core per worker,
dynamic admission,max4leases,noAScap and the existing1s watchdog/exclusive
retry/parent-eviction path. Do not count a cancelled or resource-failed request
as native rejection, or sampled watchdog response as a hard memory quota.

Build the current release example once, then copy its executable into the
existing run output as a frozen binary artifact. This avoids accidental
replacement if later source work builds a different target. Use the existing
24 original candidate qualification before the new full pair because this
binary includes the actual lifecycle repair. Require actual source/response
and process-retirement checks, not an efficacy threshold or research gate.
Reuse the prior24 reference labels; no generated proof/empty fixture substitutes
for real Mathlib engagement. Capture21accepted/3rejected if the native path
still matches; record any difference rather than inventing equivalence.

The full comparison preserves every source ID,status,accepted set,attempt/
fallback/preemption,parent preparation,consumer latency,CPU/RSS observation,
whole lifecycle,serialization/compression/cleanup. Matched cardinality or
controls alone do not establish full transparency. Report accepted-set
differences and reason tails separately, including expected difficult memory/
timeout cases. A result can be positive,negative,mixed or censored; no minimum
speedup or deadline is imposed. Preparation/snapshots/resource primitives are
prior work and this own-engine support pair is not a strongest warm-service
advantage or a novelty claim. No competitor reproduction or CPU oracle work.

The preceding original compiler group has completed/been ingested; no other
native capture runs. Root thread only. While full data accumulate, advance
failure/certificate/source implementation rather than wait or poll each minute.
Publish verified setup/qualification/launch, then preserve the healthy frozen
group and collect actual terminal data once. Root self-review, not independent audit.
