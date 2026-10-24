# Actual RTX5090 point qualification — functional result

## What ran and returned

The own fixed CUDA interpreter executes on **NVIDIA GeForce RTX5090** through
the existing finite Job/device-plugin route. One offline batch contains
474captured arithmetic entries from169source IDs, with4096points per entry
(1,941,504point evaluations). All474source/entry-matched replies return.
CPU exact rechecking confirms the same two known counterexamples, with
0missing reference witnesses,0additional witnesses,0invalid returned points
and0provider errors. GPU proposal-mask bitwise equality was not exported;
the established property is exact witness/result agreement on these entries.

This proves actual device engagement and functional point-proposal behavior.
It does **not** prove native proof acceptance-set equivalence, online
cross-candidate overlap, full false-goal coverage or end-to-end proof speed.

## Complete observed cost boundaries

| Observed phase | Time |
|---|---:|
| First CUDA context/module initialization |441.207ms|
| Host program/grid packing |186.075ms|
| Device allocation/upload/launch+sync/download/free together |9.342ms|
| Within that: synchronized launch/sync wall |0.649ms|
| Host exact support-point checking |227.307ms|
| Provider complete batch |864.007ms|
| Client complete batch RPC |887.299ms|
| Controller startup to API readiness |10.256s|
| Controller client wrapper |3.472s|
| Provider stop/process exit/log/Job retirement |17.016s|
| Complete finite cold Job lifecycle |30.746s|

Rows are nested/shared boundaries, **not additive stage weights**. The GPU
launch/sync phase alone cannot be called a proof speedup. The provider event
is authoritative for shared batch timings; duplicated per-entry timing
fields must not be summed474times. Cold initialization is charged, not
subtracted to invent a warm result. No matched native proof pair ran here.

API readiness reports CUDA uninitialized. The joint client monitor starts
before the first batch triggers actual context creation. Device identity
is checked after real execution, not inferred from an API-ready flag.

## Resources, coexecution and actual retirement

The monitor includes the existing observation's exact PID/start identity,
the qualifier tree and owned provider RSS. It sees max2actualREPLs, each
with24GiBaddress-space limits,0kills and0monitor errors. Its single sample
records11,894,378,496bytes (about11.08GiB) combinedRSS and40,546,304bytes
providerRSS. The device transaction is shorter than the1s sampling period:
this is a **sampled value, not a complete startup/retirement RSS peak** or
hard quota proof. Cold lifecycle resource coverage remains limited outside
that client sampling window. No RSS value is fabricated for unobserved times.

The ongoing full observation remains a diagnostic with this recorded short
coexecution window; its clocks are not an isolated final performance baseline.
The original PID255332/start124305929 is still live afterward, without a
restart or another REPL/full group.

The stop endpoint responds, transport threads retire, the CUDA context is
closed, and the provider process exits0. The controller observes actual
container termination before collecting logs and UID-owned Job deletion.
The Job is absent, cleanupErrors is empty, and clientExit/providerExit are0.
The source and provider are both on lab; fourCPUeligibility8–11 is retained.
No unrelated Workspace, permission, quota, host driver or schedule changes.

## Disposition and raw evidence

Functional hardware qualification passes for the retained supported contexts.
No new performance or OSDI contribution is admitted. Next: finish the real
full observation/coverage-cost analysis, qualify the own native tactic path
and run same-candidate end-to-end comparisons at the same resource point.
The pending GT/GE extractor repair is still separate from the frozen capture.

summary.json, checked.jsonl and response.json retain all returns;
provider.log.gz retains actual initialization/kernel/retirement events;
memory-rss.jsonl retains the sample and original process identities;
job.json/lifecycle.json retain the exact embedded source, Job/PodUIDs,
actual exit and complete cold clock. Root self-review, not independent audit.
