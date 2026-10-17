# GPU-stage acquisition in progress

Restoration/correction published as fdea219. CPU primary 1.34668x remains a
stage result, not final project closure. The hourly gpu-smt-osdi is ACTIVE.

New namespaced diagnostic .so and separate Rust binaries preserve existing
primary files and active prefix captures. All new captures use 48 GiB; bad_alloc
remains an explicit resource/operational failure. Completed 24-source native
checks agree exactly with same-method primary JSON.

The current full capture is full1000-launch.json: original 1,000 sources,
oracle then strong Fast/hybrid, four-wide, CPUs12–15. It is running, not completed;
do not compute a final GPU bound from partial rows. Prefix continues on its
existing driver, and its observation-only minute waiter has been terminated.

Numeric timers now include successful and no-cert/failed paths: parsing,
polynomial/LP construction, floating LP, exact LP fallback, support repair,
exact verification and response packing/write. Client call IDs join to source
bodies; all direct check attempts have timing and acceptance, corrected after
self-review found an earlier false local-mutable flag in finally. Raw development
captures and generated sources remain in preflight-v1..v4; no rows are spliced.

Current attribution limits:
- Numeric per-request CPU excludes startup, stdin line collection and diagnostic
  log-write outside the measured session. Whole capture and sampled per-process
  CPU retain these costs; residuals and lower-bound process observations must
  not be labelled a partition of the old sampled 976.25 seconds.
- Direct generated product counts are explicit; fallback native matrix shapes
  are exact observed FP shapes, but product-origin counts are not yet attached
  to each fallback request. Keep unknown provenance explicit.
- Per-source end-to-end latency is not available from this four-source collector.
  Report whole tied-wave tails; do not invent candidate times from wave durations.
- An observed interval union is occupancy, not a critical-path saving. Only a
  generous removal bound with all missing-work conditions explicit may rule out
  the threshold. Otherwise the GPU prototype remains admitted for real testing.

No OSDI acceptance, independent audit, final GPU gain or impossibility is claimed.
