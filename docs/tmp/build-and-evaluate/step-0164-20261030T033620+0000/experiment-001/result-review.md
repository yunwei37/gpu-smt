# Exact finite pass@k cost selection — root self-review

All7,808sources/244tasks are used at each point.142tasks have an observed native
acceptance and102do not. Every policy must complete all32candidates of every
observed-unsolved task. Predictions hold out whole tasks in five folds;all
fits converge. Cheap lexical lengths,numerals and tactic-family/count features
feed logistic acceptance and a log-link quasi-Poisson arithmetic-mean observed
cost predictor. The old geometric/log-cost score is not substituted for E[c].
The history extension sees only completed same-task/family failures and costs.

## Primary result: complete frozen work,not measured service wall time

| Policy | Current four-worker attempt-cost seconds | Historical two-worker HTTP-span seconds |
|---|---:|---:|
| All7,808 |52992.124106|43209.621347|
| FIFO first-success |37164.887410|29613.524167|
| Short-source first-success |36498.245764|29363.916962|
| Learned probability/expected cost |36356.850563|29541.465173|
| Plus observed sibling history |36902.147937|29986.700131|
| Training-index one-prefix probe/restart |37451.494218|30433.426036|
| Hindsight minimum work,unsolved exhaustive |35838.016728|28923.681945|

The exact-first-success hindsight row is a minimum of these frozen serial costs,
not the best parallel makespan or a global acceleration bound. Original source
outcomes are operating-point observations,not uncensored runtimes or theorem truth.
The known measured1.439031x is21746.811714/15112.118703at the older2worker/24GiB-AS
point. It is not calculated from this table or used as a four-worker denominator.

Unsolved mandatory work is35686.071288s(67.3422%)at the current point and
28784.510314s(66.6160%)at the old point. Short-code work is only1.018423x/
1.015221x the corresponding hindsight minimum. Those are residual frozen-work
ratios;they cannot be multiplied/divided into the measured1.439wall ratio.

At the current point,p/c saves141.395201work seconds(0.3874%)versus short-code,
improving51tasks,regressing79,and leaving114unchanged. A task-paired exploratory
bootstrap interval for the inspected delta is[-638.44,1025.35]seconds;not a fresh
benchmark or runtime CI. On the older point,p/c adds177.548211work seconds.
The bare CPU-slot proxy also disagrees:current p/c is328.18s slower than short-code,
while the old point is123.37s faster. That proxy ignores RSS admission and
exclusive retry serialization,so it is not a physical four-worker service model
and is not eligible for end-to-end acceleration claims.

Current first-success p/c selects30resource-failed sources on observed-unsolved
tasks,versus31for short-code;all11failures on the two observed-solved tasks can
be avoided by a hindsight successful choice. Remaining exclusive frozen attempt
work is6930.255991s. The conditional minimum ordinary work/4 plus this serial
debt is14157.196176s under the frozen frontier/exclusive protocol. It explains
why a CPU-only proxy below that duration is not a feasible RSS-aware prediction;
it is not an applicable cross-scheduling Amdahl proof.

## Restart accounting and the Gittins distinction

The probe row chooses a training-distribution age-zero completion-reward/cost
threshold,tries one prefix,and charges the discarded prefix before a full
restart if still needed. It is a Gittins-inspired one-probe heuristic,not full
age-updated Gittins or a lossless native resume implementation. Actual prefix
history is observable;future heldout outcomes affect only simulated completion.

The row discards1087.369912s/886.683530s across the current/old points and
needs2645/2644restarts. It is worse even when optimistically retaining each
original terminal label. Original cumulative native budget eligibility for those
restarts is unknown:elapsed attempt/HTTP spans are not native heartbeats.
No renewed300s allowance,free restart,free snapshot,checkpoint or exact parity
is assumed as an implemented facility. These optimistic labels cannot qualify
the restart row for production exact-pass@k. SOAP's lossless M/G/1 theorem and
Luby's independent randomized restart theorem do not establish such eligibility.

## Implementation disposition

There is no currently supported safe resource-failure rejection cache,or useful
end-to-end learned/restart accelerator to enable. Do not ship a new runtime
policy simply because one inspected work sum is0.39%lower. Existing Rust default-
off replay extension and prior ordinary schedulers remain available;no runtime,
RL every-candidate contract or accepted-set rule is changed. These are measured
opportunity limits for the specified models,not a closure of the four directions.
Next substantive failure-reuse evidence requires actual complete input/effect
qualification;data here leave it unknown rather than turning RSS kills into proof.
