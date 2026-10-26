# Root result self-review — idle forecast admission liveness

Self-review only;independent review forbidden by user. Source/caller/tests/docs
reviewed as one change. No novel resource primitive or native speed claim.

## Reproduction and repair

Original production code484fd57plus the new test fails on actualRSS20/budget100/
forecast90after the fitting control succeeds:there is no active attempt to
release headroom. Cargo101is an expected reproduced defect,not a native
collector fault. An earlier wrapper SyntaxError did not launch testing;its raw
source/note remain and the repaired wrapper propagates the actual child exit.

Lease admission now recognizes a forecast that cannot fit idle resident memory.
It gets exclusive execution with unconsumed growth reservation removed,while
actual measuredRSS still passes the same AdmissionPolicy. A lease records
whether the existing resource-reclaim hook is needed. No new scheduler,limit,
flag,monitor or CPU allocation is added. Parent teardown and fresh fallback
remain under the original deadline and in attempt cost/provenance.
Fitting forecasts keep the old normal path. Over-budget actualRSS cannot launch
a backend. Predictions never become rejection and no failed attempt is invented.

The same existing0.1backend method may now be called on a first exclusive
headroom request;API docs tell implementers not to require prior attempt history.
Attempt.exclusive is documented accurately and initial exclusive_headroom events
identify forecast/actualRSS/budget. Prepared backend code changes only its comment;
real reclamation behavior is reused.

## Executed validation and limits

[All raw/index](../../../../../artifacts/rust-engine-2026-10-25/idle-headroom-20261026/README.md).
Initial failure and both success validations are retained. Final fmt,Clippy,
49ordinary tests,warning-free docs and CLIhelp pass. The five-case fixture matrix
covers ordinary/idle-headroom/at-total/oversized/actual-over-budget behavior.
Final combined own/full sampled peak50,051,530,752Bunder48GiB,0pressure/errors;
the first patched run had a different active-capture memory state and its own
15,698,292,736Bpeak. Do not compare these as implementation memory effects.

Native4tests compile/skip locally. Strengthen the existing native prepared-parent
CI case by replacing direct resource-hook invocation with actual Engine routing.
Its below-total-budget synthetic prediction forces exclusive first admission
without actual allocation. Assert unchanged raw response,one actual fresh
attempt,no invented failure,old parent exit,child retirement and later new-parent
preparation. Only publication-time CI executes this real native case.
No additional local acquisition or new workflow.

Run status:reproduced fixture defect/ordinary repair valid,native CI pending.
Research value:resource-layer dependency-only.
Paper impact:none;original fullpopulation parity/throughput/novelty unanswered.
Next decision:verify exact-pushed native CI and retain executed evidence,then
continue original fullpair/nightly/hotspot work,not more admission tuning.

## Live original capture

Original408739/start_ticks140695363still runs its unchanged release42659a8.
At04:24:09UTC3719physical attempts,no terminal or prepared cell. Later trace
seconds13107–13110and a separate1s owned-process check show nativeREPL429819/
start_ticks142003975actually running at~oneCPU with growing9.6–10.4GBtreeRSS.
The prior journal entries are native cancellations followed by exclusive retry;
engine-final preemption/resource classification belongs to finalCapture.
This is heavy resource-constrained work,not evidence it hit the repaired
empty-active-set path. No restart,signal,source/config/binary replacement.

## Post-publication executed native evidence

Sourcea3052a0has both existing workflows successful. The actual native job
executes4tests,4passed/0failed/0ignored,including the strengthened engine-driven
exclusive-headroom parent eviction/reference-response/re-preparation contract.
[Executed receipt/log/self-review](../../../../../artifacts/rust-engine-2026-10-25/idle-headroom-20261026/native-ci-a3052a0/result-review.md)
resolves the earlier publication-time pending status only. No new runtime/source
change is made. Scope remains pinned4.18lifecycle,not complete4.9Mathlib
population parity,throughput,high-memory benchmark or independent audit.
Historical42isolated inputs were already prepared;no redundant generator/run
was added. Preserve the sole fullpair and the pending original workload order.
