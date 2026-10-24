# Real-goal RPC batching and device lifecycle preparation

## Completed CPU-reference batch qualification

The endpoint now preserves a supplied group as one queue item. It also merges
other already-ready groups without imposing a batching delay. The remote
qualifier sends the retained474actual entries from169source IDs. The observed
CPU-reference event is one474-entry batch, with7917numeric proposal points,
5770exact candidate checks and the same two exact witnesses. All474responses
have matching source/entry ownership; no reference witness is missing, no
returned point fails the independent worker-context check, and no provider
error occurs. Final RPC elapsed is0.517840seconds. This is **CPU-reference
functional qualification**, not GPU execution or proof speed.

The final qualification requests graceful stop through the real socket
endpoint. The provider exits0 and emits provider_retired after transport
joining/context-manager exit; the process is reaped. CPU null-context
retirement does not qualify CUDA teardown. Both initial and final records
remain in separate remote-batch-cpu-qualification directories.

## Same-clock location of the first two known witnesses

Existing own observation HTTP records can be joined to Lean entry_ns because
both use the same host monotonic clock. Canonical SDK classification returns
lean_error for both completed HTTP responses.

| Source | Current observed HTTP span | Before first exact-witness entry | Entry-to-response tail |
|---|---:|---:|---:|
| minif2f-379 |0.719964s|0.171804s|0.548160s|
| minif2f-802 |3.651470s|1.054240s|2.597230s|

These are this instrumented observation's clocks; the earlier3.052911s
historical request sum is not substituted into them. The tail includes native
search, subsequent commands, waiting and transport. It excludes unobserved
post-response cleanup and is not proven avoidable work, whole elapsed savings
or an Amdahl ceiling. A false intermediate goal still cannot justify killing
the entire candidate. Full false-goal/time/timeout coverage remains pending.
Raw identities and canonical outcomes are in current-witness-response-tails.json.

## Prepared actual device path — not executed

The package reuses the previous finite benchmark Job name, pinned image,
NVIDIA runtime class, RTX5090 hardware selector and one shared GPU allocation.
It embeds only our four Python modules and compiled PTX. There is no PVC,
Secret, Kubernetes Service, new Workspace or schedule. The base Git commit
and working-source status are explicit; full source copies are embedded,
rather than claiming the uncommitted bytes belong to that base commit.
point-job.json is **not applied**.

The lifecycle reads the original observation terminal before any mutation,
preserves existing outputs/owned Jobs, binds the Pod to its actual Job UID,
requires the real device-ready marker, executes either offline points or
the own24-source Lean qualification, then requests graceful provider stop,
waits for actual process exit, collects logs, and deletes only the same
UID-owned Job. Startup/client/retirement/complete cold clocks remain separate.
Cleanup failures or inaccessible evidence remain errors/unknowns.
Controller PowerShell7.6.5 parsing has zero syntax errors. No GPU execution,
NumPy availability in that pinned image, device retirement or real Lean
off/on consistency has yet been verified. Source preparation is not delivery.

The current sole full observation remains untouched, with its frozen worker.
The transient management-call failure and restored real Workspace access are
recorded in the owning infrastructure repository at
incident-logs/2026-10-24-gpu-smt-management-transient.md (dcac67a4).
No node or Workspace restart, permission/resource change or GPU Job occurred.

## Root disposition

This is self-review, not independent audit. Software/CPU protocol work is
ready for the next actual qualification boundary; wait for the existing full
observation's real completion, then collect its coverage/cost results and
execute the own finite GPU path. Do not turn an offline474-goal batch into
a claim of online cross-candidate batching or end-to-end benefit. Original
fourRQ and OSDI-level research requirements remain open.
