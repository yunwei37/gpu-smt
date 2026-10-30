# Native candidate scheduling

Original miniF2F32candidate/task scheduling for first checked success.
No prefix/certificate reuse or arithmetic oracle changes. This consumer
does not produce all RL candidate rewards.

[Existing-data opportunity and limitations](../../artifacts/candidate-scheduling-2026-10-25/result-review.md).
[Actual measurement plan](../../artifacts/candidate-scheduling-2026-10-25/plan.md).

Existing-data analysis uses the retained Python environment; it executes no Lean:
    python bench/lean-candidate-scheduling/analyze.py --out /tmp/a-fresh-analysis --workers 2

[Real native qualification](../../artifacts/candidate-scheduling-2026-10-25/native-qualification-20261025T0715/result-review.md)
and the [complete original7808 three-cell matrix](../../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/full-result-review.md)
are retained. Analyze closed groups with analyze-native.py --run <completed-group>.
AST parsing and offline simulation are not performance results. The legacy
run.py/source snapshot reproduces its historical48GiB/max2/24GiBeach point;
it is not the current dynamic resource runner and must not restart a competing
capture. New resource measurements use the Rust engine/current resource contract.
Reviews are root self-review.

The [existing task-held-out lexical model](../../artifacts/candidate-scheduling-2026-10-25/crossfit/result-review.md)
did not improve its own offline short-code comparison. Preserve it instead of
retraining the same inspected data or adding a redundant full cell. This is not
a route closure. New source memory/time policies still need identifiable labels
at their declared resource/backend point; final overwritten activity snapshots
alone are not a per-candidate memory trace.

The optional engine HTTP stream delivers completion-order results with a final
count marker. It shares first-success/RL semantics and does not make source
predictions into failure verdicts. See [API delivery scope](../../docs/api.md#http).

Resource-tail source/state opportunity can be recomputed without Lean:

    python3 bench/lean-candidate-scheduling/resource-failure-opportunity.py --out /workspaces/.agent-state/gpu-smt-captures/new-resource-audit

Task/last-line/whitespace keys are opportunity proxies only;RSS-watchdog
outcomes do not authorize deterministic resource-failure rejection reuse.

The complete two-resource-point cost-selection/restart analysis uses all7808
retained sources,whole-task heldout models and exhaustive observed-unsolved tasks:

    python3 bench/lean-candidate-scheduling/analyze-cost-selection.py --out /workspaces/.agent-state/gpu-smt-captures/new-cost-selection

It needs the existing numpy environment. Frozen-work/CPU-slot proxies are not
service throughput;the probe/restart row has unknown native-budget eligibility.

## Latest user correction:runtime-only continuation

Source-feature success/cost training and comparison are frozen;do not rerun
train-order.py or analyze-cost-selection.py as new research. Existing raw models
remain historical. Continue only the exact finite pass@k ideal bound and
elapsed-service-only preemption/restart. Cross-proof resource reuse is about
matching expensive calls/entry states,not identical complete proof text.

    python3 bench/lean-candidate-scheduling/analyze-resource-calls.py --out /workspaces/.agent-state/gpu-smt-captures/new-cross-proof-call-audit

This reuses original native Syntax and checks proof-relative spans. Recovered
source target templates are not complete native goal/context/budget records.
