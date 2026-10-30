# Computational extraction coverage — individual source review

自审, 2026-10-30. Reproduce with `python3 research/mechanisms-2026-10-30/analyze_extraction_coverage.py` in the retained Workspace. Original inputs/results remain in their owning directories; this directory contains only derived small tables and review text.

## What is actually covered

All126 original miniF2F source texts selected by the complete warm/engine7808 resource pair were reviewed, with one row per id in [minif2f126.csv](minif2f126.csv) and comment-stripped proof text plus reasons in [minif2f126-source-review.md](minif2f126-source-review.md). Selection is **85timeout+41resource_exhausted**, not the earlier83timeout/42resource-failure point. Resource failures are operational/censored observations, never false propositions.

| source-reviewed category | candidates | physical attempt seconds | share of126 worker-attempt work | share of all7808 worker-attempt work |
|---|---:|---:|---:|---:|
| two goal families with checked certificate prototypes |49|15091.110|38.90%|28.48%|
| other bounded arithmetic opportunities, no checker bridge yet |34|10225.125|26.36%|19.30%|
| other directly closed computational opportunities |3|1072.154|2.76%|2.02%|
| recurrence could close only after a new proved bridge |11|3377.150|8.71%|6.37%|
| not closed at the expensive symbolic operation |17|5420.364|13.97%|10.23%|
| outside current executable fragment, e.g. Real.log/sqrt |5|1500.168|3.87%|2.83%|
| known incorrect intermediate assertions: proof repair |7|2109.063|5.44%|3.98%|

The49 are **28digits-goal sources +21product-grid sources**, classified by mathematical target family. Only **two family theorems** have actually been implemented and kernel checked. They are not49 transformed original candidates with proven identical behavior. One of the29digits sources is excluded because its filter drops5-divisibility. The extra37 closed/bounded candidates give **86/126 static opportunities including the49**; no automatic extractor, sound general IR, source adapter or elapsed-time recovery has been demonstrated for these37. The eleven recurrence sources operate on a symbolic function/quantified hypotheses now; do not count them as closed hits.

**Qualified unchanged-source replacements:0; measured saved seconds:unknown.** A target-family certificate may replace a valid expensive closed subproof; each candidate still needs a verified bridge and checks of the original preceding/following proof commands and diagnostics. A completely new proof of its true final theorem is a separate proof-repair/new-proof mode. We do not silently remove false intermediate assertions or earlier errors.

## Time denominator and limits

The sum over all physical attempt durations (including preempted attempts and exclusive retries) is52992.124106s; the126selected candidates account for38795.133452s. These are worker-attempt sums in **this same pair only**, not the20323s concurrent batch wall clock. Candidate attempts overlap. The category table exposes candidate work that a future method could target; it does **not** locate every second inside closed evaluation, establish a global Amdahl bound, or promise all those seconds are removable. No historical profiler-stage fraction has been rescaled into this denominator. Delays, diagnostics and exact original call positions remain implementation obligations.

Examples rejecting a lexical census:
- minif2f3689's even-digit set also contains2002, which is not divisible by5.
- minif2f4544/4552/4570 assert incorrect divisor-set equivalences/ranges. Checked witnesses:65536 divides the product1!..9!, its square does not;4180377600 squared divides that product and exceeds both9! and99999999.
- minif2f4997/5006/5016 assert factor bounds40/31/44 contradicted by(667,3,1); prior Lean witness retained.
- Finite-looking rcases can retain unbounded tail constructors. A Finset of n=2010..2019 containing an unbounded existential m is not a closed finite search.
- Real.logb at concrete numerals is closed syntax but has no executable reduction in the current fragment. An analytic equivalence theorem would be additional work.

[ExtractionAuditWitnesses.lean](../ExtractionAuditWitnesses.lean) checks the new numeric witnesses in original Lean; the old false-bound witness is not rerun. The first witness attempt could not reduce Nat.digits directly; v2 reuses the **proved** structural digits equivalence and succeeds, with no sorryAx. Both failed and successful raw records are retained.

## W EPFL sample: separate points

[epfl17.csv](epfl17.csv) and [epfl17-source-review.md](epfl17-source-review.md) cover every returned budget-exceeded EPFL source currently in W's two retained captures:
- Original136returns atHB200000:12budget-exceeded returns cost159.678453s of623.799202s native-invocation wall sum. Only3direct closed opportunities (odd product10000/factorials,942! modular divisibility, and a rational harmonic sum requiring a Real embedding bridge) total9.282563s: **5.81% of budget-return cost,1.49% of all136returned cost**. No EPFL certificate implementation is validated. Four recurrence/complex-sum candidates require new symbolic bridges;3analytic and2abstract proof candidates are not directly extractable.
- Later7returns atHB10000/M6144:3HB and2self-wall results, all5symbolic/not directly closed. Their37.234358s of40.994593s per-invocation wall sum belongs to this separate point. The owning41.069s whole-capture number includes collection overhead and is not substituted as a native-invocation denominator.
- Still-unreturned214/epfl58969 remains right-censored; no inferred timeout verdict, cost attribution or invented closedness verdict. It is not one of the17returned budget observations.

Sample/version/resource bounds and publisher filtering prevent extrapolation to the whole EPFL corpus. No W files, processes, capture settings or classifications were modified.

## Decision supported

The data support continuing a **small, explicit Nat finite-computation certificate path for the two demonstrated families** and testing original-source integration separately. They do not support a claim that all failures, arbitrary bounded syntax, EPFL symbolic timeouts, or all86opportunities are accelerated. Verified reflection and independent proof checking are prior art; see [prior-work.md](../prior-work.md). A systems contribution still needs automatic extraction coverage, total construction/checking cost, and honest changed-verdict versus preserved-verdict measurements.
