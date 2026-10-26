# Step0048 — idle prepared memory cannot strand a large forecast

BUILD_AND_EVALUATE,root-only implementation/self-review.
Observed2026-10-26T04:24UTC;goal stays active.
Previous turn progressed source/validation/push484fd57;CI40266991487now succeeds.

## EXPERIMENT_GATE

Entry follows unchanged user-instruction/questions-for-author,CONTRIBUTING,
core/engine/native contracts,nearby tests and the existing validation workflow.
Apply auto-research-orchestrator and oss-change-workflow. This project usesmain;
no PR/release or other agent is created. User prohibition overrides delegated
review requirements. FixedRQ2and narrow scope are in the [plan](experiment-001/plan.md).

### Admission/source mechanism node
Source inspection finds an actual liveness defect:with idleRSS20andforecast90
below budget100,the ordinary queue cannot admit110and has no active peer to
retire. Forecasts>=budgetget exclusive admission but the initial run did not
invoke the existing idle-reclaim hook. These are concrete resource-layer defects,
not a reason to tune concurrency or resume frozen CPU/GPU branches.
[Plan self-review](experiment-001/plan-review.md).

### Reproduction node
New fixture matrix first passes its ordinary case,then reproduces the idle
headroom wait on unchanged production484fd57,Cargo101after5s test timeout.
The first monitor wrapper had a syntax error and launched no workload;its source
and note remain. Repair actual newline/exit propagation,then retain real failure
and combined27,437,404,160BsampledRSS/0pressure. No native candidate body runs.

### Implementation node
Promote a forecast that cannot fit idle headroom to an exclusive lease. Lease
records idle-reclaim dispatch;actualRSS policy,CPU,watchdog,request timeouts,
cache/subscribers/ordering and logical outcomes remain unchanged.
Initial resource dispatch uses the existing backend hook after all peers retire,
not a new fallback/helper. NativePreparedcode only updates its comment.
API0.1hook docs now permit initial calls and Attempt.exclusive does not imply
past failure. Initial exclusive_headroom event records actual reason/values.

### Validation/real-native path node
The fixture handles fitting/below-total shortage/at-total/oversized/actual-over
budget,with no backend call when actualRSSviolates budget. First repaired
ordinary validation passes. Strengthen the existing pinned-native CI lifecycle
case to go through Engine instead of directly calling the resource hook:
force a forecast of budget-minus1byte (no actual allocation),then check one
exclusive attempt,real parent/fresh-child retirement,unchanged raw response,
and later re-preparation. Local compilation succeeds;all49ordinary tests,
fmt,Clippy,docs and CLIhelp pass on final source. Four actual native tests are
explicitly skipped locally,not passed by inference.

Both successful validations remain because native CI fixture changed between
them. Final combined sampledRSS50,051,530,752Bwith0pressure/errors under48GiB,
CPU10–11. Only extra development validation would be withdrawn on pressure;
original fullpair never signalled. [Result self-review](experiment-001/result-review.md)
and [raw/index](../../../../artifacts/rust-engine-2026-10-25/idle-headroom-20261026/README.md).

### Actual collection state node
OriginalPID408739/birth140695363still runs the old release(mtime00:43:14UTC),
source42659a8,unchanged7808input/resources.04:24:09snapshot has3719physical
attempts,no terminal/prepared cell. A targeted read of slow-tail progress shows
a live single-coreREPL growing memory,not an empty active set or observation
failure. Raw backend cancellation does not define final engine resource status.
Preserve it;no ratio or counterfactual new-code speedup. No minute waiting loop.
Previous-stepCI484fd57success is retained separately from this pending nativeCI.

## WRITE_GATE

Only necessary API/architecture/implementation/evaluation paragraphs change:
exclusive headroom can be initial,overrides must not require prior history,
same actualRSS/watchdog/deadline,ordinary fitting path unchanged. No QuickStart,
dependencies,configuration,workflow,resource budget or frozen paper prose/RQs/
Initial Narrative change. No paper compilation needed for unchanged source;
full refinement/milestone review entry unmet.

## REVIEW_GATE

[Outer root self-audit](outer-audit-20261026T041112+0000.md) checks exact defect,repro,
dispatch/actual-budget boundaries,source-growth and native CI scope.
Independent review is not claimed. Status includes a reproduced fixture defect/
repaired ordinary liveness boundary,native CI pending,dependency-only value.
No RQ/native population speed/parity/novelty conclusion.

Outstanding:fullpair final strong matched frontier;actual nightlySAT/LRAT and
original23/48measurements;sufficient validated failure mechanisms;attributable
prediction data;42exclusive reruns/multi-node service;paper/novelty/independent
scientific audit. User four directions remain,no threshold/deadline/closure.

## Meta-review and routing

Direction stays on the user-approved dynamic resource layer. Fixing this
observable starvation is preferable to adding speculative detectors/knobs.
No source cost model is retrained from partial data. Source/native tests retain
real scope;native CI fixture replaces rather than duplicates the direct control.
Production diff is narrow;fixture105linescovers five cases and reuses one fake
backend/monitor,not a new test framework. No mature-project PR or delegated
review applies;user main/self-review constraints take precedence.

Daily maintenance already exists forOct26. Preserve original/failed/partial
records,unrelated dirty files,current native release/host. Publish coherent
boundary onmain and push. Verify existing exact-headCI;native contract execution
is required before claiming that changed route qualified. Continue fullpair to
actual terminal,then original nightly and prepared hotspot cohorts under one
native group/48GiB. No waiting-only goal loop or new admission tuning.
