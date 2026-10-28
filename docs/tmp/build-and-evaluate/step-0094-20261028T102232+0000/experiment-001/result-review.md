# Queue-frontier retry result — root self-review

The runtime now defers resource retries behind first-attempt tickets already
registered when the retry is queued. Each retry closes that ordinary frontier;
later batches cannot overtake it. Policy keys/order within a frontier remain
stable. All admissions, one-second watchdog, native retirement, idle-parent
reclamation, attempt timeouts, provenance and verdict semantics remain.
Initial forecast-exclusive work obeys its ordinary queue position, rather than
blocking unrelated older tickets through the former solo-waiter counter.

Two real engine regression fixtures verify normal work progresses while a
surviving peer is deliberately held; even maximum-priority-key normal work
precedes the retry. The retry begins with zero live peers; later arrivals wait
behind it. Shutdown wakes deferred work without dispatching another retry.
The old source actually fails the same free-slot progress assertion after2s;
fixed bytes are restored in finally. Raw old failure/source are retained.
These are deterministic engine fixtures, not Lean or measured throughput.

Initial supporting guard launch had a relative-cwd output-directory failure
before tests; no native request ran. One-CPU workspace tests then hit the
existing subprocess watchdog fixture's two-CPU prerequisite. The second run
usesCPU10–11 within the allocated8–11 set: all workspace targets,doctest,
format and clippy pass;five actualLean tests remain ignored locally.
Documentation generation is killed by the combined RSS guard at
51,691,917,312B sampled total,retained as exit-9. Only the new compiler group
is killed;the warm collection continues. Single-CPU documentation retry
passes (see receipt);do not call the killed command a pass or a kernel quota.
All supporting overlap is development-qualification contention,not final timing.

This does not remove the8924.78s exclusive-checking cost or establish that a
full-budget retry can share memory. Only repeated mid-batch drain/queue blocking
is addressed. Complete full-budget retries still serialize at the end.
No native speedup,matching accepted set,novelty or independent audit is claimed.
The running qualifier retains its frozen old binary. Real retry-order
measurement is deferred until the corrected warm/engine pair is reviewed.

Warm qualification has now truly completed24sources/27attempts:
14valid,7Leanerrors,1timeout,2resourcefailures;all native workers retired.
Its1429.077858s internal and1430.677580s external clocks remain separate.
The existing continuation starts its frozen engine phase at10:27:16UTC.
That is one sequential native collection,not a completed pair or final gain.

## Actual source CI and release followthrough

db8ecbf GitHub engine run40672462407 completes both Rust and native-repl-contract
jobs successfully. Actual native job122762431233 runs all5pinnedLean4.18
differential/lifecycle tests with0ignored/0failed. Rust job122762431683
includes the two new engine regression controls and actual owned-process
watchdog tests. Benchmark-smoke run40672462371 also succeeds.
Exact metadata and rawcompressedlogs/testlines are in actual-source-ci/.
This is boundednativecontract evidence,not native4.9throughput or fullMathlib
matching and not independent auditing.

A singleCPU11releasebuild completes27.034840s with48,069,668,864Bcombinedpeak,
no pressureabort/monitorerror. Copying the full bytes freezes a prospective
newretry-orderbinary and unchanged24inputs privately;pending-native-release.json
records the exact latercommand. No runner/autostart is installed and current
qualificationbinary/nativehost remain unchanged. Executeonlyafter complete
rootreview of that pair. Preparation is not a measuredperformance result.
