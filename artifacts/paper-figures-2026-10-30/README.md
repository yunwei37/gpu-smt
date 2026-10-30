# Retained resource comparison figure

Inputs are existing retained data: the completed warm/engine result review
and M commit e259a49's observed-memory-thresholds.json. No native workload is
run by this script. Run `python3 artifacts/paper-figures-2026-10-30/plot.py`
with Matplotlib 3.11.2; the noninteractive Agg backend writes PDF/SVG/PNG here.

The first panel uses the original complete batch clock; the second uses each
trace's own covered span. Lower RSS thresholds are offline fixed-trace queries,
not new-budget executions or outcomes. Retry/affinity differences and shared-host
ordered-pair limitations remain in the manuscript. Resource-layer engineering is
not the paper's novelty. The PDF was prepared offline from byte/JSON-equal inputs
and is installed here for the actual Workspace manuscript build.

# Retained resource comparison — offline figure draft

## Proposed caption

**Complete batch time and sampled RSS envelopes at one historical resource
point.** (a) External launch-to-exit time for all 7,808 original miniF2F
candidates in the retained warm-first comparison. Both paths return the same
final status aliases and 3,014 accepted IDs. Raw reply payloads and operational
error strings differ, so this figure does not establish full artifact
transparency. The 1.23882× ratio describes the complete batch at this point;
it is not an isolated copy-on-write effect or a steady-state service frontier.

(b) Fractions of each original RSS trace above four thresholds under left-hold
sampling. Both captures used a configured 48 GiB aggregate RSS threshold;
8, 16 and 32 GiB are thresholds evaluated offline against the unchanged traces,
not runs with those resource budgets. The vertical axis is logarithmic.
Markers are evaluated points; no interpolation or counterfactual throughput
curve is drawn. Each fraction uses that trace's first-to-last sample span.

The historical comparison uses four eligible CPUs 8–11, Lean 4.9 with the same
ordinary compiled Mathlib, no fixed per-process address-space cap, and a
300-second admitted-attempt allowance. Warm group affinity/immediate resource
retries and engine per-worker leases/frontier-delayed retries differ. It is one
ordered shared-host comparison, with the documented support work retained.
Error bars are absent because there is no independent replication at this
point. No COW, workload-policy or GPU benefit is isolated.

## Denominator and boundary checks

| Quantity | Warm trace | Engine trace |
|---|---:|---:|
| Observations | 25,167 | 20,323 |
| First-to-last sample span (s) | 25,174.736735515 | 20,321.999419928 |
| Held-sample time above 48 GiB (s) | 92.937076032 | 83.008803368 |
| Own trace fraction above 48 GiB | 0.369168% | 0.408468% |

The shorter absolute above-threshold duration and the slightly larger fraction
for the engine are both retained. They have different denominators and do not
prove better memory control. Sampled RSS includes observed overshoot and does
not enforce a hard quota or establish physical-memory/PSS savings. These trace
spans differ from the external batch clocks in panel (a); they are not silently
substituted for them. The files reflect the historical capture, not a new run
on phobos-vt or the maintenance-time 40 GiB allocation.

## Sources and reproduction

- Batch times and outcomes: fixed commit 5916957023ff07b07e1437248a3ef232095fc5b7,
  [complete result review](https://github.com/yunwei37/proofserve/blob/5916957023ff07b07e1437248a3ef232095fc5b7/artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z/result-review.md).
- RSS summaries: fixed commit e259a49,
  [observed-memory-thresholds.json](https://github.com/yunwei37/proofserve/blob/e259a49/research/mechanisms-2026-10-30/retained-analysis/observed-memory-thresholds.json).
- Local render script: plot-retained-resource-point.py; Matplotlib 3.11.2,
  noninteractive Agg backend; no verifier, browser or GUI is launched.
- Outputs: retained-resource-point-draft.pdf, .svg and .png. PDF and SVG are
  standalone vector artifacts. The PNG was visually inspected: labels,
  annotations, axis units, logarithmic scale and footer are legible and
  unclipped. No visual or statistical acceptance beyond this draft is claimed.

## Integration status

This is an offline paper artifact produced during the explicit Workspace
maintenance window. No Workspace connection, source-tree edit, product test,
benchmark, resource/lifecycle mutation, new agent, commit or push occurred.
It does not replace the current paper or choose a new scientific mainline.
After the explicit restoration notice, reconcile it with step0178 and intervening
root work in the original checkout. Compile and validate there before considering
paper integration. Keep all existing raw results and actor-owned files intact.