# E1080 regression cost attribution — root self-review

## Question and admission
This is a secondary analysis of the already closed original1000 comparison,
within unchanged RQ4. It tests the proposed explanation that the persistent
source regressions are simply pathological external LP solves, and whether
they justify another LP-only GPU variant. It adds source-level engagement
evidence to the previous distribution result, without another acquisition.
It cannot identify every Lean fallback or establish a causal GPU ceiling.

Reproduce: `python3 artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-without-diagnostics/analyze-regression-costs.py`.
Input is the complete original source mapping, both closed source-span arrays,
all current Power numeric-race receipts and CPU HiGHS request/reply records.
All1000sources, including eight rejected sources, enter the analysis.
Prior persistent IDs come from the already declared three earlier observations.

## Actual grouped observations

| Retrospective group | Sources | No recorded numeric race | Recorded races | Parsed HiGHS models | Reported completed HiGHS solver seconds |
|---|---:|---:|---:|---:|---:|
| Current regressions also slower in all prior observations |63|20|223|94|0.839444|
| Other current regressions |106|62|69|66|0.782553|
| Current non-regressions |831|539|614|400|4.766174|

Together,82of169current regressions have no recorded external numeric race.
The63persistent sources contain223races:168native numeric CPU winners,
47CPU HiGHS winners, three exact-negative external answers and five native
no-certificate answers. The legacy `gpu` winner here is **CPU HiGHS**.
A numeric certificate winner does not prove Lean accepted its reconstructed
certificate; the reduced-diagnostic capture did not record that boundary.

Across all169regressions, the observed positive service-span differences sum
to148.343122seconds; numeric-race decision spans sum to10.296392seconds and
retirement spans to0.659802seconds. These overlap and measure different
boundaries; subtracting them from whole elapsed, dividing them to derive
Amdahl shares, or calling the remainder Lean reconstruction CPU would be wrong.
Recorded completed HiGHS solver time is only1.621997seconds in this group,
but excludes cancelled solves, native numeric solvers, small direct paths
and all uncaptured Lean work. It is not an all-LP upper bound.

The persistent group has3.306687reaped numerical-child CPU seconds, including
2.314165cancelled-child CPU seconds. All906races across all1000sources account
for1812distinct reaped children, with no recorded wait/kill errors.
All560parsed external models are joined to original source IDs.
No race or external-row JSON parsing error occurs;227non-model external rows
remain in the original raw input and are not counted as completed models.

## Interpretation and next paper decision
The measured evidence does not support attributing all persistent regressions
to a few slow completed HiGHS solves. In particular,20persistent sources do
not enter the recorded large numeric races at all. That is absence of these
records, not proof that they perform no LP work. Another narrowly tuned
HiGHS/GPU search variant is therefore not justified by these regressions.

The original cause remains unresolved: current Lean-stage/fallback work was
deliberately not captured; cross-epoch IDs and shared-host source spans are
not causal isolation. In the earlier, different strong-omega-cost profile,
the corresponding proof IDs have distinct arithmetic/checking patterns;
those timings cannot fill the missing current fields or be divided by the
current476.725600second denominator. No answer-aware routing or source
exclusion follows from retrospective groups.

The complete service/population comparisons already running remain the
decisive next evidence. A new implementation intervention needs an actual
cost explanation and a matched beneficial preflight, rather than a new
LP/kernel/allocator grid. The1.700586x current CPU result, all four RQs,
original Lean/SMT scope and unclosed broad GPU question remain unchanged.

## Checks and review scope
A separate root recomputation reconciles all1000IDs,906races,560models,
total reaped-child CPU and cancelled-child CPU against the prior complete
analysis. The source-level output preserves every row and both source spans.
The first analyzer invocation had a literal-newline source-mapping assertion;
the string-escaping error was corrected before any result output.
No capture, source, executable, finalization rule or live worker was changed.

Run status: valid secondary analysis of closed evidence.
Tested explanation: not established; causal attribution remains inconclusive.
Research value: supporting scope/engagement evidence, not a new acquisition.
Paper impact: excludes a blanket explanation, not the GPU route or RQ4.
Review is root self-review; no independent auditor or other Agent was used.

The targeted factual insertion compiles with Tectonic0.17.0 (exit0).
Root renders and visually checks actual pages14--15; the paragraph, CDF,
captions and two columns show no overlap/clipping. Existing TeX underfull-box
warnings remain in the retained build log. This does not claim completion
of a new twelve-round writing refinement or full independent paper review.
