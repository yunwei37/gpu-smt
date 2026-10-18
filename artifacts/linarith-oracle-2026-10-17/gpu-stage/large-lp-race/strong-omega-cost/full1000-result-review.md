# E1071 — complete current common-omega cost accounting

This is a **diagnostic component comparison**, not another primary speed trial.
The native frontend already uses this project's two-sided numerical oracle.
It is not the original stock/native whole-system denominator, and its clocks
must not be rescaled from the historical 2,234.69-second acquisition.

## Complete observation

Both original-order cells process all 1,000 original sources, eight candidate
queues on four CPUs (4–7), official omega, 48 GiB RLIMIT_AS, no device work:

| Frontend, same numerical backend | Whole seconds | Complete / reject / operational | Observer read errors |
|---|---:|---:|---:|
| Native |475.968475283|992 / 8 / 0|94|
| Direct external AST |406.461143583|992 / 8 / 0|92|

Verdicts and every non-message response field match. There are65 message-only
differences between these cells. The native cell differs from the preceding
normal common-omega native control on10 message-only responses; IDs are retained
in full1000-native-fidelity.json. Diagnostic clocks do not replace the normal
454.82/388.17-second component experiment or the original three CPU pairs.

Full raw bytes: [native](full1000-raw/native/), [direct](full1000-raw/direct/).
For a split .gz stream concatenate its .part00000, .part00001, ... files in
numeric order, then gzip-decompress once; each archive-manifest.json records
the stream. Lossless compression preserves warnings, partial events and failures.

## CPU work, including cancelled work

There are14,307 joined numerical requests,249,532 phase events,121,039 completed
scopes and7,454 unfinished scopes. All unfinished process IDs are accounted for
by retained child wait4 receipts. Cancellation is never assigned zero CPU.

| Completed exclusive CPU seconds | Native frontend | Direct frontend |
|---|---:|---:|
| Floating LP |40.086926019|33.686155174|
| Exact LP |14.430819747|36.136897044|
| Floating input packing |1.649097528|1.414168355|
| Exact positive repair |1.183619441|0.782418417|
| Exact positive certificate verification |0.483843899|0.274126691|
| External transport |5.321208239|4.208204784|
| AST products outside Lean |not used|3.223565449|
| All reaped child CPU, **overlapping rows above** |54.073063|72.883462|
| Cancelled child CPU, **subset of previous row** |40.959283|59.687778|
| Unassigned child CPU upper residual |24.694021991|23.358800045|
| HiGHS whole-process CPU, including pool/startup |43.326535|39.025184|

HiGHS caller-thread solve CPU is2.467345045/1.985980955seconds. Its all-process
unassigned CPU is39.815768380/35.803806416seconds. This contains internal solver
threads plus startup/bookkeeping; it cannot honestly be reported as pure LP.
The generous GPU model below credits **all** of it to removable work.

Direct Lean calling-thread CPU includes183.166803832seconds of certificate
checking,66.812167007seconds of fallback product construction,
13.066571774seconds of preprocessing,39.785951057seconds of linearization and
42.680681162seconds of fallback certificate work. CPU sums are not disjoint
end-to-end wall fractions. Successful and failed request breakdowns, actual LP
shapes and native-ranked1%/10% tails are separately reproducible below.

## Request outcomes, actual models and matched tails

Completed LP CPU remains material on failed branches. For direct requests with
certificates, floating/exact solve CPU is9.999834/0.083101seconds; failed direct
requests use5.423302/21.794074seconds. Subsequent failed native fallback uses
3.746298/12.179828seconds and successful fallback14.516721/2.079895seconds.
These completed-scope sums exclude unfinished CPU, which remains bounded above.
Exact positive repair by these four groups is0.416039/0.005292/0/0.361088seconds;
do not attribute all external CPU to solver kernels.

Actual parsed external models number1175native/1085direct. Direct median/p99
shapes are82/310rows,230/861columns,1705/7477nonzeros. Complete exported-direct
problem shapes, including models never reaching HiGHS, have median43rows,
167columns,892nonzeros and120generated products; p99 is255/465/3471/406.
The direct parsed service sees at most3distinct candidates with only
1.141409928seconds of cross-candidate lifetime overlap (native1.821347382).
Service lifetime still includes building, queueing and extracting; these are
not instantaneous GPU-ready batches.

Using the same sources ranked as the native slowest1%, summed candidate-service
spans are660.702966670native/509.931125639directseconds, not whole elapsed time.
On these ten, direct certificate check CPU is16.483954485seconds, fallback
linearization15.889169385 and products6.986672008. Native slowest10% spans
sum1491.219806652/1278.955655818seconds. On that matched100-source set, direct
certificate checks use63.310012611CPU seconds, fallback products31.161836998,
linearization25.895170140 and certificate construction16.609169811.
Full IDs, stage sums and numerical per-tail CPU are in
[complete-budget](full1000-complete-budget.json) and
[request-costs](full1000-request-costs.json); they are not a critical-path
decomposition or a new primary performance score.

## Explicit conditional Amdahl/capacity models

A simple serial Amdahl expression1/(1-f) is invalid when f is a sum of
overlapping four-CPU work or request lifetimes. We therefore publish both
observable elapsed-window unions and an explicitly conditional resource bound.

* Native wide products/LP/RPC window union:327.625615356seconds,68.8335% of
 475.968475283seconds. Direct union:232.574452004seconds,57.2194% of
 406.461143583seconds. These windows generously include waiting, packing,
 non-device work and proof construction.
* Deleting those windows on the observed fixed lanes, retaining other durations,
 gaps and proof paths, models411.977130808/358.929864593seconds. The latter is
 only1.32609x relative to the native component control. A changed scheduler
 or representation need not follow these lanes.
* Excluding the collector and replacing sampled leaf CPU by exact wait4 totals
 yields at least1,438.843462 CPU seconds in the direct cell. Give GPU all
 completed floating/exact solving and external products, **all** unknown
 killed-worker CPU and **all** HiGHS process CPU: at most135.430601712 CPU
 seconds are credited removable. Remaining work needs at least
 1,303.412860288/4 =325.853215072seconds at ideal four-CPU capacity.
 The resulting native-component-reference upper ratio is **1.46068x**.
* If even all Lean fallback product proof construction were free, the favorable
 ratio becomes **1.53960x**. Perfect numerical solving alone still leaves
34.163592867 CPU seconds that must additionally disappear to reach1.5x
 against this component reference.
*199 direct failures have recorded exact-checked negative LP answers;
196 have unambiguous subsequent fallback stages containing22.721225666
 product CPU seconds. Retaining those products under the **same IR and
 fallback protocol** tightens the favorable model to **1.51182x**.
 A negative LP answer is about the exported coefficient problem, not
 mathematical falsity of the Lean theorem.

These models hold remaining work, proof path, representation and effective CPU
rate fixed, and retain diagnostic overhead. They are not scheduler-independent
or representation-independent impossibility proofs. Raw negative witnesses
have not been independently replayed; the captured coordinator's exact check
and emitted event are the evidence. This is root self-review.

**Decision:** more LP kernel/solver tuning is not admitted by these results.
Representation/fallback and proof-producing frontend work are consequential
remaining mechanisms. Broader GPU closure is **not** justified: even the
favorable current-protocol model remains above1.5, and this denominator already
contains our numerical oracle. The original whole-system criterion is unchanged;
the hourly research task stays active. No new full GPU matrix is launched.

## Reproduction and observer limitations

Run in the owning Workspace:

```sh
python3 analyze-complete-budget.py
python3 analyze-request-costs.py
```

The first script produces full1000-complete-budget.json and
checked-negative-fallback-analysis.json from retained raw data and the complete
numeric/Lean phase analyses. The second produces full1000-request-costs.json,
including request success/failure and fixed native-ranked tails. It does not
rerun Lean or a solver. Numeric phase reconstruction is documented in
[numeric-fragment-recovery-method.md](numeric-fragment-recovery-method.md).

SIGKILL interrupted16 flat numeric log fragments across17 malformed lines.
All raw bytes and recovered fragments remain; intact following records are
recovered only under the captured flat schema. Unknown phase CPU remains
bounded by wait4 residuals. The [forward logger repair](observer-forward-fix.md)
preformats records before writing, but **was not built or measured in this pair**.
Executed source is phase-executed-streamed-write.rs. Observer errors and source-
less auxiliary timers remain visible rather than being normalized away.

Root self-review accepts complete source coverage and scoped accounting,
rejects new primary GPU performance, universal upper bounds, independent audit,
global baseline optimality, systems novelty and paper-readiness claims.
