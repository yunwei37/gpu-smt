# Complete native / GPU screening miniF2F pair — root self-review

## EXPERIMENT: completion and decision
Run status: valid completed native-cell pair, with missing complete cold-controller clock.
Tested hypothesis: contradicted for this screening implementation on these7,808sources.
Research value: supporting mechanism/workload boundary, not globalGPU impossibility.
Paper impact: retain counterexample screening as a small component; stop extending this GPU pair.
Next paper decision: profile the formal baseline's83timeouts and slowest10%failed requests.

Untouched original native:21693.761299439s; complete corrected-layout GPU cell:23615.030439515s.
GPU requires8.856321%more elapsed (native/GPU0.918642106).
Its23.989769s preparation/native reparse is additional, not hidden.
Fixed off-first order and shared host do not estimate variance or isolate device causation.
No partial earlier GPU data is spliced. The old109parser regressions are absent:
all7,808source IDs and statuses agree; accepted sets exactly3,014each, differences empty.
Raw native replies have no valid-with-sorry or valid-with-error cases.
Both return4,669Leanerrors/83timeouts/42resourcefailures. See analysis/accepted-sets.json,
paired-sources.csv, native-response-inspection.json and final-evidence.json.

## Failure and timeout accounting
All4,794native failures remain. Cumulative HTTP envelopes native/GPU36981.890285/
39748.728829s; cumulative reported body32327.877325/32322.929813s.
These overlap across concurrent requests: neither is an isolated elapsed clock or removableCPU.
All83same timeout sources persist; HTTP24966.405942/24998.866243s,
reported bodies24900s each. No timeout reduction is observed.
Native-ranked slowest1%all79sources: HTTP23766.365766/23798.662004s.
Native-ranked slowest10%all781sources: HTTP39833.113955/40022.919648s.
The next requested failed-only10%is480of4,794:83timeouts/355Leanerrors/42resourcefailures.
Its fixed source list is in final-evidence.json; it is not the all-source781tail.

##42resource failures, separately attributable causes
analysis/resource-failures.csv preserves each source's native/GPU error and actualHTTP time.
The identical42IDs report native allocation failure under configured24GiB address-space
limit, with std::bad_alloc, on both sides. Each side's process-exits raw contains42
returncode134/exact bad_alloc records. Aggregate watchdog kills0/errors0.
This is per-process allocation failure evidence, not evidence of a new global/cgroupOOM.
The API's failed body time0 means unavailable phase timing, not free work.
ExitPID-to-source mapping is explicitly unknown where final activity state was overwritten;
we do not fabricate ownership by ordering simultaneous failures. Per-source API errors suffice
for the stated cause, and complete exit/RSS/activity logs are retained.

## Actual component coverage
15,396hook entries;8,541supported;2,354CPU-closed;6,187actualdevice requests.
34exact refutations in29sources; every source remains a Leanerror, none a timeout.
Their native HTTP/body sums34.070886/28.410035s; GPUHTTP39.699538s.
These are outcome-conditioned accumulated costs, not savedwall or strictAmdahl upper bounds.
Old25-source/78-timeout counts refer to a source-wrapper version with109parser regressions;
do not transplant that coverage or a0.2%strict ceiling into this valid pair.
Actual5090provider:6,186batches (6,185singletons/one double),1cross-source batch,
1,528source IDs,0batcherrors/0returned-point exact recheck failures.
Batch whole9.465876s, pack3.601571s, exactcheck0.377426s are overlapping sums,
not full verification clocks. No more GPU pair expansion is admitted by latestuserdirection.

## Resource and lifecycle limits
Both source2/live2,24GiBAS each,48GiB aggregate owned RSS including provider, CPUs8–11.
Peak RSS native50,326,097,920bytes/GPU50,872,713,216bytes, max2REPLs,
zero watchdog kills/errors, all native descendants retired. Watchdog samples every1s;
it is not a hard kernel RSS quota.
Durable native client exits0, provider gracefulexit0; exact ownedJob/Pod deleted, no matchesremain.
The local observation channel failed after launch; detached native client completed independently.
Original local cold stopwatch is unavailable, represented null, never replaced with another run.
Jobcreation→providerexit32001s includes8345.949707s after durableclientexit while controller
observation was unavailable. That delay is not computation/cleanup kernel cost.
Provider's actual retirement duration0.662626s is separate. recovered-job-pod.json,
lifecycle.json, provider.log.gz and observer-failure-excerpt.txt preserve this limitation.
The observer now retries thrown read-only transport failures, preserving its finite client's identity.

## WRITE and REVIEW
The result enters the paper locally, without changing its fourRQs, central position or
claiming OSDI novelty/readiness. This component's absent complete cold clock is explicit.
Self-review recomputes complete ID/status sets, exact refutation joins, all42causes and own
clocks from raw; checks units/overlap, resource controls and cleanup. No independent audit
was performed because the user prohibits other executors. All original failed attempts remain.
Next: measured tactic/phase attribution on baseline-selected failures, no external reproduction.

## Recompute
    python3 bench/lean-counterexample/analyze-final-pair.py --off artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-20261024T0913/off --on artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/gpu --analysis artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/analysis

analyze-screening.py's original command is preserved in analysis-command.json.
All source versions, preparation, raw failures, watchdog samples and native results are linked
from this directory. Self-review, one fixed-order observation; no significance claim.
