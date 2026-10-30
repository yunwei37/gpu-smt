# Generalization: checked expressions do not imply complete proof recovery

Self-review, 2026-10-30. M-lane evidence for the root paper; no production feature
enabled. Reflection, chunked arithmetic and existing Mathlib lemmas are established
techniques, not novelty by themselves.

| Observed source frame | Budget sources | Budget request-time share | Existing three-family hits | Checked new expression exposure | Recovered budget sources | New tasks |
|---|---:|---:|---:|---:|---:|---:|
| miniF2F full 7,808 |126|73.21%|57|see earlier full-source checks|32|3|
| ProofNet full 5,952, repetition 0 |70|11.57%|0|0|0|0|
| EPFL evaluation, 136 returned |12|25.60%|0|2 sources, 0.66%|0|0|
| EPFL remaining 7, smaller budget |5|90.83%|0|0|0|0|
| EPFL training sample 12 |6|55.04%|0|0|0|0|
| APRIL 39 mutations |16|50.53%|0|0|0|0|
| APRIL corresponding 39 references |4|18.94%|0|0|0|0|

Every percentage uses its own observed point's request/attempt sum, not a shared
wall denominator, kernel-only time or removable cost. Charge each request once
if it contains a budget diagnostic, including requests with earlier ordinary
errors. miniF2F uses historical worker-attempt sums52,992.1241s including retries;
its57shape hits/33.02%exposure are not57repairs. Actual32/126budget-source repairs
plus1ordinary-error repair yield33new accepted candidates and142→145/244tasks.

## ProofNet: complete source frame, no implemented-route recovery

All5,952original sources/responses in each of3retained original ZIPs checked.
Rep0total1,192.4351s;70budget-containing requests138.0112s. Diagnostics are
56recursion/14heartbeat; the separate JSON/process operational failure is not
a budget source. Reps1/2have the same70budget sources, costing135.1908/133.8571s.
All have413complete candidates and28solved32-candidate groups out of186.
The detector finds no digits/grid/power or factorial-rfl route in ALL5,952sources,
including non-budget sources. No modified ProofNet source is emitted; pass@32
stays28/186=15.0538%. Five groups without parseable theorem names remain in186.

Historical command metadata: Lean4.9Kimina, one request in flight, CPU4–7,
12GiB AS; not the new phobos diagnostic point. Source/diagnostic review finds
one bounded arithmetic opportunity under an abstract Group/Sylow proof
(exercise_4_5_23,0.81%request exposure), needing a new proved bridge. Most
budget failures concern symbolic analysis/algebra or recursive rewriting.
This review is not an exhaustive semantic classifier or a proof that no other
computation strategy exists. Closed abstract statements or symbolic(n-1)!
are not literal finite-evaluator opportunities.

Operational source5879 proposes a=2,n=5 for a Nat-subtraction equation=2001;
a short actual Lean4.9decide control proves that witness false. It is not
recovered or reclassified as ordinary/budget failure.

## EPFL/APRIL: every returned budget source, distinct native points

budget-source-audit.csv contains113budget observations: ProofNet70,
EPFL12+5+6, APRIL16+4, with original source/log references and diagnostic lines.
Full external source/log text remains on PVC, not republished with unknown license.

All six EPFL training heartbeat cases were individually reviewed: unknown Real
function equation; arbitrary continuous functions; cosine at symbolic frequency;
Real sequence at arbitrary index; symbolic square-root inequality; closed
noncomputable trigonometry at pi/9. None is in the proved numeric fragment.
Closed Real statements alone are insufficient.

The EPFL evaluation point has136returned of144selected, with a censored/live
source and later pending observations at another point. Do not splice200kHB
and10kHB timing or count missing returns as failures. APRIL uses qualified
39mutation/reference pairs, excluding earlier startup/import failures.
These unequal/stratified samples are not population timing estimates.
They have no32-candidate task frame here: pass@32isN/A. Zero recovered sources
means no new solved observed task, not a claim about all tasks in those datasets.

Unimplemented source-review opportunities, SEPARATE from checked coverage:
EPFL-evaluation7sources/10.81%request exposure (2literal arithmetic,3recurrence,
finite complex sum and rational/divisibility sum); APRIL mutations6/18.89%,
references2/8.69% (rational/floor sum and closed cube-sum helpers under other
symbolic or malformed steps). No assumed savings or recoveries from these.

## Automatic arithmetic extension: 2 checked expressions, 0 complete sources

Detected source literals select factorials942/5000/10000; powers2^5000,
15^233,5^234; odd filter/product on range10000. emit_closed_nat.py emits
untrusted values in structural chunks100. ClosedNatBase.lean proves composition
using ordinary Mathlib lemmas. Automatically regenerated proof source is
byte-identical to the actual kernel-checked5,215,539-byte module
(automatic-generation-check.json). Large generated source/oleans stay PVC.

Actual checked true goals: 942! modulo15^233=0, and the complete odd-product
factorial identity on range10000. Positive control passes with standard axioms;
false modulus control rejects. The rejected control's diagnostic sorryAx is
NOT an accepted proof. The odd-product identity passes at default recursion depth.

Whole-source differential at the same M point:
- epfl-31023/amc12_2001_p5: original budget3.4710s; final insertion budget3.4215s.
  Entry observed, no successful leaf event; target refinement/synthetic
  obligations fail before completed application.
- epfl-2994/mathd_numbertheory_43: original budget3.9769s; final insertion
  budget3.8734s. One leaf checks, but a later wrong divisor obligation
  (5^n divides15) and factorial simplification remain.

No full source or task recovered. These small timing differences are not a
speedup claim. Lean4.15original kernel,200kHB,native8GiB cooperative check,
j1/CPU8–15,finite30s self wall; originals rerun at this same M point.
Never compare new M elapsed times to old W elapsed times as speedup.

Preparation charged separately: base3.4754s + facts85.2639s + final tactic3.7721s
=92.5113s. Numeric proof compile sampled4.773GB own-tree RSS.
All failed earlier modules/insertion diagnostics remain in native-invocations.json
and immutable PVC captures. No amortized end-to-end benefit established.

closed_nat_route.py replaces rfl sites only in the detected source shape;
both final source rewrite payloads match observed captures. The tactic attempts
restore-and-original-rfl on ordinary failure, but the deep failure in the first
source does NOT qualify universal in-process fallback. The offline experiment
keeps the paired actual original native result when a full repair fails.
No engine/API enablement or identical operational timeout-diagnostic promise.

TCB: stock Lean kernel and imported proved equivalences; no native_decide,
new axiom or sorry acceptance. Successful primitive checks print only
propext/Classical.choice/Quot.sound as applicable.

## Reproduce and inspect

Run python3 analyze_generalization.py in this M directory on retained Workspace.
It reads original archives and W captures read-only. Exact denominators:
cross-dataset.csv, summary.json, proofnet-repetitions.csv. Compact full source
census: full-source-routing.csv. Detailed budget review: budget-source-audit.csv.

For numeric payloads call emit_closed_nat.emit(output_dir,factorials,powers,
odd_ranges), using automatic-payload-parameters.json. Build ClosedNatBase.lean,
generated ClosedNatFacts.lean, then ClosedNatMethods.lean in the retained4.15
Mathlib environment. The latter is the measured specialization for the observed
constants, not an arbitrary-goal extractor. Source router takes input/output
paths and refuses overwrite. Exact actual commands/receipts for all22native
invocations, including failures, are in native-invocations.json. Short own-source
controls are published; external candidates, large proof payloads and memory
traces stay at recorded persistent capture paths.

Conclusion: miniF2F recovery is real but concentrated. This held-out matrix
adds zero complete recovery. General factorial expressions can be checked, yet
that alone does not repair malformed prefixes, later false obligations or
embedding blow-ups. No broad cross-dataset recovery/speedup claim is supported.
