# Native-stage diagnostic qualification — root self-review

2026-10-22UTC. This supplies missing own-comparator phase evidence for RQ4;
preflight is engineering engagement, not a population result or GPU bound.

## Source and actual build
The published reduced-diagnostic CostStages.timed is literally a no-op and
CostBaseline emits no final cost record. Old full traces cannot recover those
erased timings. Added opt-in per-call timed wrappers with finally, retained
intervals, aggregate CPU/wall values and source-owned final records. Native
Fast probe, restricted reconstruction, full-native and stock fallback share
the same invocation-local IO.Ref. No product tags, representation, solver,
certificate selection or fallback order is changed.
The external LP interval is a complete oracle invocation envelope, including
packing/IPC/repair, not pure solver time. Product intervals include native
proof construction, not just GPU-ready numeric expansion.

Built all15custom Lean modules sequentially against the frozen dependencies.
Original binaries remain untouched. Incremental build uses24GiB address
limit and existing48GiBowned-tree watchdog; first/v2peakRSS1.78GiB-range,
no monitor failure/kill. Actual commands, output and build metadata remain.
An initial output-directory-order setup failure occurs before any compiler/
REPL and is preserved, then repaired. No new dependency grid or container.

## Actual original-source comparisons
All conditions use source2/live2/native24GiB/total48GiBsampledRSS/fourCPU8–11.

|Condition|Whole seconds|Warm verification seconds|Native outcomes|
|---|---:|---:|---|
|Frozen published build|39.369182|32.811940|24complete|
|Diagnostic build, flag off|39.757321|33.591338|24complete|
|Initial timing on, incorrect return tag|39.089490|32.711362|24complete|
|Repaired timing on(v2)|38.660213|32.409110|24complete|
|All8original rejected sources, v2|19.946063|13.690385|8rejected|

Every positive per-source native outcome and raw response matches the frozen
24reference. Rejected8match their actual original IDs/outcomes in the complete
same-resource native population; no historical elapsed clock is pooled.
No process remains after each cell. Every capture has at most2liveREPLs,
sampled aggregate RSSabout13.5GiB, zero monitor errors/kills.
One fixed sequence/shared-host observation cannot establish zero profiling
overhead, nor is the lower v2clock a claimed performance improvement.

## Failure retained and bounded repair
The first profile has115events falsely tagged failed, despite24genuine
completions. Lean's finally runs with transactional state semantics that
discarded the local mutable return tag. This tag is invalid for outcome
statistics; the entire raw capture and actual source diff remain.
Move only that diagnostic tag to an invocation-local IO.Ref, like the cost
object. Build into a fresh v2output; do not overwrite the frozen/v1binaries.
The repaired24capture has115returned events. The actual8rejected-source
capture has49returned and2failed pipeline events. Candidate rejection and
a pipeline returning are different layers: no49proof successes are claimed.
Both successful and throwing wrappers now retain their stages.

## Costs and coverage actually observed
Repaired24stage wall sums: preprocess1.640936s, linearization1.927528s,
native products6.829245s, LP invocation envelopes19.316296s,
certificate construction6.052781s. The wrapper LP caller-thread CPU is
only0.196282s; helper/process/scheduling work is not counted as that thread's
CPU. The8rejected stage wall sums include6.495722sLP,4.342071sproducts
and2.109534scertificate work. No failure branch is dropped.

Every profile event joins uniquely to an original source, and all timed
intervals lie inside its own invocation. Product+LPglobal time unions are
21.737641s for the24profile and8.716764s for rejected8; these are occupied
observed intervals, **not removable critical path**. Per-source sums overlap.
Do not subtract these concurrent quantities to report a strictGPUceiling.

The profile covers the wrapped native route, not all possible Lean code:
term elaboration before CostBaseline.run, omega, explicit configured tactics,
indirect stock-core calls and finally records lost to hard process death
remain outside this hook. Legacy manual parse timing enters preprocess
totals but does not have an interval; that discrepancy is explicit.
No literal configured linarith/nlinarith line occurs in selected1,000sources,
but this lexical check does not prove absence of indirect uncovered work.
All coverage limitations remain in the full diagnostic.

## Decision
The real path qualifies the predeclared own-denominator diagnostic on the
original1,000, with unchanged native algorithm and all outcomes retained.
Run only a frozen-native/diagnostic-on pair at these same safe resources;
this is missing phase attribution, not a new performance solver matrix.
Its own clock and instrumentation difference stay separate from all older
810.71/2234.69/full29750clocks. No resource/worker/grid enlargement.
Analyze same-native-ranked1%/10% and every failure; include unknowns.
It does not authorize GPU/project closure, a new kernel, another Agent or
an independent-audit claim. Recompute with analyze-preflight.py.
