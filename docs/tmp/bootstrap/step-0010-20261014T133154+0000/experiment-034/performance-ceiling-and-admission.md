# E034: performance ceiling and backend admission

Observed 2026-10-16; root disposition follows the user's request to estimate
end-to-end opportunity before implementing another narrow GPU kernel.

## Question and existing evidence

What fraction of complete source verification could the proposed independent
argument-comparison batch actually remove? A successful interface build does
not answer this question. No GPU backend is implemented or admitted by this note.

E032's complete 29,750-source CPU capture reports 5,401,763 user CPU samples,
54,563,262,080,630 sampled period and no reported sample loss. The inclusive
report gives the following rows (overlapping ancestors, never added):

| Symbol or region | Inclusive share of sampled user CPU | Meaning |
|---|---:|---|
| lean_is_expr_def_eq | 35.00% | Exported native Meta definitional-equality subtree |
| Lean.Meta.isDefEqArgs | 23.16% | All observed argument-comparison work, including stateful work |
| specialized isDefEqArgsFirstPass loop | 11.58% | An overlapping part of argument comparison |
| isDefEqArgsFirstPass | 11.45% | An overlapping symbol; do not add to the loop |

[Original report receipt](../experiment-032/full-inclusive-report-receipt.json)
names the retained complete inclusive report. These are a single sampled CPU
capture's symbol costs, with callchain/DSO attribution limitations, not fractions
of elapsed request latency or system makespan. The full capture's elapsed clock,
native CPU accounting and sampled period have different boundaries.

E033's separate instrumented full capture returns all 29,750 sources.
Of 13,041.048187034 seconds of completed observed outer thread CPU:
23.6089361932% enters with neither expression nor universe metavariable flags;
17.9309687465% enters with no cached variable/level-parameter flags and
nonidentical pointers. These are overlapping entry descriptors, not time spent
doing independent argument comparisons. Instrumentation and interception bias,
three censored outer calls and nested work remain explicit.
[Group evidence](../experiment-033/full-observed-category-groups-20261016.json)
and [complete review](../experiment-033/result-review.md) retain the measurements.

## What can actually be calculated

For a CPU-bound workload with unchanged parallelism and zero extra costs,
Amdahl's expression is speedup = 1 / (1 - f + f / S), where f is the fraction
actually accelerated and S its acceleration. With infinite S, zero transfer,
packing, dispatch, fallback or synchronization cost:

| Deliberately optimistic scenario | Assumed removable CPU fraction | Ideal CPU-bound speedup |
|---|---:|---:|
| Erase the entire observed defeq subtree | 35.00% | 1.5385x |
| Erase all observed argument comparison, including stateful operations | 23.16% | 1.3014x |
| Assume E033's no-metavariable descriptor transfers exactly to E032's defeq CPU distribution | 35% x 23.608936% = 8.263128% | 1.0901x |
| Make the same cross-run assumption for no-flags/nonidentical entries | 35% x 17.930969% = 6.275839% | 1.0670x |

The last two rows are **conditional sensitivity calculations, not established
end-to-end upper bounds**. They multiply different captures and timing scopes.
Nor does E034 eligibility equal either E033 descriptor: an application containing
metavariables in some arguments can still contain closed candidate pairs in
other arguments. Conversely, a completely closed outer call may have no useful
independent batch or costly reduction. Thus 23.6% is not a measured GPU coverage
fraction, and its complement is not automatically recoverable GPU opportunity.

Let q be the genuinely removable independent fraction of the observed
argument-comparison CPU, and h the added cost expressed in the same CPU-bound
baseline units. The optimistic reduction is at most 0.2316*q - h; ideal speedup
is 1/(1 - 0.2316*q + h). At q=25%, 50%, 100% and h=0, the ideal speedups are
1.0615x, 1.1310x, 1.3014x respectively. Reaching 10% time reduction requires
q >= 43.18%, and 20% requires q >= 86.36%, before any overhead. These are
sensitivity examples, not a new quota, budget, admission threshold or promise.

Neither q, the ready batch-width distribution, reduction cost within those
pairs nor critical-path coverage is measured in the existing aggregates.
There is therefore no defensible numeric end-to-end benefit bound for this
candidate yet. Aggregate defeq prevalence cannot supply the missing joint
distribution. A profile-based CPU ceiling is not a latency/makespan guarantee.

## Root disposition

Do not proceed from the linked interface to implementing a narrow GPU backend
on the strength of these counters. Preserve the source/build/fallback smoke as
completed interface work; leave the provider unresolved and report zero actual
device engagement. No speedup or RQ is closed.

The conditional 1.067-1.090x scenarios leave little room for the already observed
packing/transfer/fallback costs. A larger claim cannot be obtained by pretending
all 23.16% stateful argument work is independent. Existing scalar routes remain
closed negative implementations, not candidates for another small tuning pass.

Proceed with the already authorized contribution/closest-work review and
complete-system experiment/ablation assessment. Prefer a system design that
covers substantial complete verification work or amortizes actual service
costs across real requests, only if it is distinguishable from existing services,
caches and snapshots. Do not label ordinary CPU compilation as that contribution.
Reopen GPU backend implementation only with evidence establishing a useful
independent work frontier and a credible complete-cost opportunity, or a
source-grounded broader mechanism. This does not narrow the original four RQs
or stop the overall research. No additional observation-only full run is
launched merely to fill this missing percentage.

## Limitations and review

This is root analysis, not an independent audit. A fresh OMP reviewer must
check the scopes, calculations, completeness and resulting research decision.
Missing measurements stay missing. Source records and original failed routes
remain preserved; no held-out source is removed to improve a ratio.
