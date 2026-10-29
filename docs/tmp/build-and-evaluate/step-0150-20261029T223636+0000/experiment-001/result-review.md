# Shared-node guard result — root self-review

Source adds startup PID/group interruption controls,6GiB host-availability floor
and existing-account /readyz probing. Current default/maximum sampledRSS is12GiB;
there is no per-processAS or raised retry threshold. No permission/scheduling,
Workspace or CronJob action. This is finite capture supervision,not a new
production-engine mechanism or scientific result.

API I/O runs on one owned background worker;parent sampling does not synchronously
wait on HTTP. Non-200/unreachable/missing credentials or a probe unresolved2s
stop the whole group. Request timeout1s and nominal1s sampling are response
limits,not an instantaneous hard quota. Final pending API failure is drained
before a complete terminal. The interrupted source stays pending and receives
neither rejection nor automatic resource retry;retirement evidence is retained.

Nine new regressions (eight safety cases plus12GiB cap) bring the Python suite
to81passes. Initial80-test run had two errors from escaped fake readiness bytes;
the fixture now supplies a real newline and unexpected readiness failure is
recorded as HostSafetyStop. Failed/intermediate logs are retained. Final suite
usesCPU6–7,about80MB own sampledRSS and hostMemAvailable~21.7GBminimum.

Actual guarded entry uses retained inputs/context but cannot execute a candidate:
the new owned control PID12829/birth1793313800.28 is deniedSIGKILL(errno13),
naturally exits0,and is confirmed retired. Entry exits1 with explicit operational
stop. No segment/Lean launch,zero candidate rows and no complete terminal.
Own sampled development tree max81,956,864B;all output onPVC. This proves current
startup refusal,not live low-memory/API abort under native load,full kernel
enforcement,Lean semantic replay or workload opportunity.

Readiness credentials remain absent in the Pod;none are added. Native captures
remain off and other permitted low-load engineering can continue. Existing
cluster CronJobs,duties/backups/dumps/archives are not queried for mutation,
paused,deleted,triggered or rescheduled. Existing Github CI on push is separate.

Self-review moved readiness drain/worker shutdown ahead of computing terminal
seconds and writing complete. Thus final API work cannot disappear from the
controller phase clock or remain active after a successful terminal. Early
CLI/import and final metadata writes are still not a full service wall clock;
no phase number is promoted to end-to-end throughput.

entry-source-reconstructed.py is transparently reconstructed from the two
subsequent local help/cleanup-clock edits,not a file copied at execution time.
Startup-control branches were unchanged. It must not be mistaken for a fresh
run or a newly frozen native-workload source.
