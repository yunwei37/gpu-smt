# Point provider / Lean worker interface — CPU protocol qualification

## Implemented path

The finite point provider accepts typed goal queries, batches requests already
available without waiting for a minimum batch, packs the fixed CUDA program
format and returns a candidate rational point. Its host CPU first filters
numeric hints with the exact checker; the Lean-side Python worker independently
rechecks the returned point against its own full typed context. A remote
Boolean alone cannot authorize failure. Source ID and actual-entry identity
must agree. No point, unsupported input, malformed response or endpoint error
returns ordinary native fallback through the existing tactic wrapper.

Registration locking covers only enqueue/shutdown bookkeeping, never point
evaluation or exact checking. The provider has one main execution loop and
non-daemon request handlers. Shutdown stops acceptance, resolves queued
requests, joins transport threads, and exits its CUDA context manager before
emitting provider_retired. Actual GPU cleanup is still unverified.

Queue, batch preparation, synchronized device/transfer/free, exact checking,
worker RPC/recheck, provider setup and retirement have separate telemetry.
Only complete candidate/process/Job clocks can establish end-to-end benefit;
these phase numbers are not additive Amdahl fractions.

## Real protocol execution

The CPU-reference provider and actual standard-library worker execute two
retained false-goal entries plus one real correct-goal control. All three
return; the two exact witnesses are confirmed again on the worker, and the
control is not refuted. A real closed local endpoint produces a fallback
response rather than a counterexample. Provider and worker exit0 and are
reaped. Final qualification takes0.671982seconds; provider RSS is38,961,152
bytes and CPU eligibility is8–11. This is CPU-reference RPC qualification,
**not GPU execution, a Lean source replay or acceptance-set equivalence**.

All three development qualifications remain in separate directories. The
first proves transport/point checking, the second adds owned-provider sampling,
and the third validates final telemetry/retirement ordering. No failed
response or earlier source is overwritten. Source and entry logs, returned
points, closed-endpoint response and PID/start evidence are retained.

## Aggregate memory connection

The provider exposes only its own process-tree RSS, PID/start identity,
backend and affinity. The client sampler checks these on every call. A
seven-line optional callback connects this sampler to the existing capture
watchdog without selecting its legacy LP GPU algorithm. Future own captures
still call stock transport with the same48GiBtotal/2×24GiBcontract, and the
provider's host RSS is added before the first REPL starts and every sample.
No quota, Workspace permission or other process is changed. The API sampler
is exercised against the real CPU-reference process. A full Lean+device
capture has not exercised the new callback yet.

The active full observation loaded the previous capture function before
this source edit and uses its frozen original worker. It is not restarted,
retargeted or rebuilt by this node.

## Next actual qualification

qualify-screening.py prepares one own off/on replay of24original sources,
including source379/source802 plus22controls, at the existing native request
boundary. It refuses to launch while the full observation lacks a complete
terminal record. Preparation and verification both include provider memory.
The actual built source is recorded so the pending comparison-alias repair
cannot silently be called qualified. The script is syntax-checked only,
**not executed**. Device launch, native backtracking/outcomes, full coverage
and same-candidate performance all remain pending.

This is root self-review. No subagent, external-system reproduction,
persistent provider, Kubernetes Service, second full group or GPU Job is added.
