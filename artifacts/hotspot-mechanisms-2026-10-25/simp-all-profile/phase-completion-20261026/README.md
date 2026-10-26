# Native simp_all attribution: initialization and finalization

Root-only source work/self-review,2026-10-26. No new candidate capture.

The retained native4.9source creates/changes local simp theorem origins and
goal metavariables between rounds. Existing hash hints omit theorem caches,
proofs,metacontext,simprocs and options. Repetition of a hint does not prove
repetition of a complete deterministic transition; no cycle/failure detector
is enabled and original23cycle prevalence remains unknown.

Source inspection finds two unlabelled potentially expensive native calls:
assertHypotheses and tryClearMany. Initialization formerly had only one total.
The current source now exposes disjoint collect-hypotheses and ordered
initialize-hypothesis phases,as well as assert-hypotheses/clear-hypotheses.
Hypothesis subjects and action return-vs-unwind fields are diagnostic only.
Native call order,results,simproc methods and progress decisions remain the
same by source inspection. This is not an executed native parity result.

## Actual validation

[Compile receipt](compile-001/receipt.json):actual retained4.9definition
compiles exit0,combined own-controller+activefull peak37,198,471,168B,
0pressure/monitor errors under51,539,607,552B,CPU11. No candidate body runs.
New olean is separate;the previously qualified old one remains untouched.
[Provenance](source-provenance.json) confirms prior source exactly matches the
retained qualification source. Its seven native/profile pairs do NOT qualify
the changed source. Native source is preserved as native-SimpAll.lean.gz.

[Four analyzer tests](analyzer-validation-001/command-0.log) pass,including
actual legacy007JSON records and explicit synthetic return/unwind/open/missing
records. Existing native source counts,old phase times,origins and malformed/
unmatched fields remain identical. Added fields mark old ends unknown,never
successful. The [reanalysis](legacy007-reanalysis.json) does not rerun Lean or
create native observations. Synthetic repeated hashes never become rejection.

[Previous-step CI](previous-step-ci.json) confirms benchmark-smoke success for
939ac01. It did not execute IntervalMap proofs. No engine changes require
the engine path-filter workflow here.

## Remaining native work

The original23prepared inputs/call-position mapping stay exact. After the sole
fullpair and already-prioritized nightly workload,qualify this new observer
against native and measure those sources with full stderr. Charge observer
overhead,original timeouts/resource failures and open phases. Some outer loop/
JSON overhead is outside timed spans;periodic inner progress logging remains
inside its action span. Their sum is not whole wall.
A finally/end can mean unwinding;action_completed false records that distinction,
and missing legacy fields remain completion_unknown. Killed open phases do not
acquire fabricated elapsed time. Native parity,per-lemma causal blame and
reliable early failure remain unproven. No RQ is closed.
