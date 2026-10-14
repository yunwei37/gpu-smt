# Experiment020: preparation retention across native worker lifetimes

## Research question

RQ3 exactly: **How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse?**

Specific uncertainty: does retaining native import/index preparation across configured worker replacement materially change complete formal verification cost, and does any benefit disappear when a strong warm pool uses unlimited lifetimes? This is one lifecycle relation, not separate initialization, correctness or checker experiments.

## Paper-value admission

Planned role: **decisive implementation discriminator**, additional RQ3 evidence, not sufficient RQ closure. The largest credible story is that the service can separate expensive preparation lifetime from candidate-worker lifetime while preserving basic decisions and changing the end-to-end resource frontier. Bare fork/pooling/COW/retirement is prior art, not the contribution.

The strongest rejection is that established warm full snapshots already capture the useful reuse, as E016's small/variable2.04% descriptive ProofNet difference suggests. Existing E014/E016/E017 data do not measure repeated native worker replacement, and source inspection cannot determine its latency/CPU/private-memory cost. Reanalysis cannot add a lifecycle that was never executed. Citation does not settle numerical effects on the original complete proof pools.

Positive material effects at finite lifetimes would support retaining preparation where replacement is required. A benefit only at128, absent at512/unlimited, limits that decision to frequent configured replacement; it is not a universal service speedup. Negative results would reject preparation retention as a material acceleration explanation in this setting. Mixed/noisy results retain uncertainty and resource tradeoffs; no further small frequency tuning to seek a favourable headline. The strongest alternative is the full heterogeneous checking comparison, already collecting as E019; the current experiment tests the main formal service frontier while that frozen acquisition proceeds. It does not repeat a GPU metadata primitive, export qualification or new cache0.x% mechanism.

## Expected and alternative outcomes

Expectation: finite replacement exposes some avoidable native preparation; candidate work and inherited-state mutation may nevertheless dominate or consume the sharing. Unlimited reuse is expected to be a strong competitor, based on prior complete ProofNet observations. Contradictory evidence is matching or worse whole latency/throughput/CPU at finite lifetimes, or a private-memory penalty that removes the intended resource benefit. An observed advantage is conditional evidence, not a necessary universal thesis prediction.

## Published precedent and real assets

[Pinned policy/source report](../literature-20261013T081000+0000/report.md) verifies official Kimina fb2393de: default `max_repl_uses=-1`, configurable finite uses, gc pruning and memory limits. We do **not** claim128/512 are its defaults, reproduce its RLIMIT_AS/network/manager, or reproduce official service performance. The same-toolchain full-snapshot native path is the stronger directly runnable comparator on these inputs; official Kimina supplies lifecycle competition and source precedent, not a second numerical baseline.

[SOCK ATC2018](https://www.usenix.org/conference/atc18/presentation/oakes) supplies the accepted-paper provisioning/whole-throughput/memory precedent and establishes process-tree reuse overlap. Existing E014/E016 source-native whole capture, native full frontend/kernel and official4.9 toolchain are reused; custom code only controls actual native worker lifetime and records ordinary outputs/resources.

Formal assets are all Goedel-captured miniF2F244test×32=7808 and ProofNet186test×32=5952 original complete code attempts in `artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs/`. Ports/task/model/runtime lineage remains as qualified E002. These are ordered offline pools, not measured deployment arrivals or proving accuracy. Failed, incomplete, duplicate, empty-code and operational attempts remain included. Supporting LeanPolish E018/E019 is not substituted.

## Comparison and fairness

**Proposed method:** one candidate-free prepared native parent imports/prepares only the first actually supplied public header and persists that native state. Warm worker descendants retain native full command snapshots privately between candidates and are normally reaped/recreated after the configured use count. Later different headers are handled in workers; no preloading of all future ProofNet headers or candidate code.

**One main baseline:** optimized independently prepared native full-snapshot warm pool, with the same executable, Lean objects, persistence/import-index optimization, allowed CPUs, worker width, original order, native default threads and configured use count. It is the competing answer that current warm reuse is sufficient. If it matches or wins, claimed retention benefit is absent at that tested policy.

**Lifetime controls/ablations:**128 and512 body responses per worker (4/16 original32-candidate batches), plus corpus-sized count5952/7808, which gives no elective retirement before corpus EOF. They are explicitly chosen policy configurations, not measured operator defaults. Compare both methods at each, and retain all three rather than selecting a frequency post hoc. Both count successful protocol responses, including ordinary proof rejection/incompleteness; crashed/timeout workers are replaced with no same-input retry. This is a lifetime control, not three baseline families.

All methods receive only original public input information. Parent first-header setup, command-line startup, import/index construction, all candidate processing, transport/persistence, normal EOF/wait, crash replacement, final teardown and necessary resource polling are included in the complete command interval. Native checker operation and original300s per-input timeout are unchanged; there is no new memory quota, cleanup deadline or whole-experiment cutoff. RLIMIT_CORE=0 prevents crash files; historical cores remain intact. No future-header or candidate-proof seed is supplied.

## Workloads and metrics

Both complete formal pools, original order. ProofNet width4; miniF2F width1 because actual old mini workers exceeded50GiB and simultaneous heavy replication caused global OOM on the shared128GiB host. Each method gets the identical CPU9–12 affinity, with native default threads regardless of width; affinity is not exclusive scheduling. This is a disclosed constrained configuration, not a width-scaling claim. Mini starts only after original E015 full profile reaches terminal and no original heavy mini worker remains. Other active CPU/GPU owners remain untouched.

Primary paper-facing metrics: complete corpus makespan and terminal attempts/second (all source outcomes), paired whole-run percent difference with all three paired values and mean/range; these are standard whole provisioning/throughput metrics following SOCK and existing paper RQ3. Secondary admission-to-terminal candidate median/p95/p99 is closed-loop latency, not offered-load queueing latency. `/usr/bin/time -v` records process-tree user/system CPU, faults and RSS; separate resource cells measure sampled whole-fleet PSS/private-dirty/RSS with sample completeness. Peak PSS is the maximum **sampled** aggregate, not an atomic or repeated-confidence physical peak. One profile per method/policy bounds interpretation; no stability claim from a single sample.

Basic completed/rejected/incomplete/operational decisions are compared per original source against matched comparator and retained original full outcomes. Diagnostic wording/thread cleanup is not a new hypothesis. Missing rows, transport failures, timeout and crashes remain explicit; an environment/adapter failure is not proof rejection. A result cannot support superiority if the main baseline fails to engage intended full snapshots or is avoidably broken. Replacement counts, seed roots and successful reuse are engagement evidence, not performance proxies.

## Planned complete matrix

| Dataset | Workers / allowed CPUs | Lifetime | Methods | Whole repetitions | Separate profiles |
|---|---|---|---|---:|---:|
| ProofNet5952 |4 /9–12|128,512,5952|prepared parent / native snapshot pool|3each|1each|
| miniF2F7808 |1 /9–12|128,512,7808|prepared parent / native snapshot pool|3each|1each|

Total48 whole conditions, **330240 source outcomes**. Lifetimes rotate across repetitions; paired method order alternates across repetition/policy. Profile cells run separately after primaries, in fixed reverse method order. No inspected partial cell tunes widths/lifetimes/algorithm. Prior E016 outcomes qualify mechanisms; none is inserted as a fresh E020 repetition.

## Execution and preflight

New isolated build1 `artifacts/lean-service-lifecycle-2026-10-13/build1/Lean49PreparedBranches` links the exact archived E016 Lean-native object and owned runtime libraries. Only finite warm C lifecycle glue changes; the original binary and active E015/E018/E019 versions are untouched. Both new methods use this same binary. Complete commands and hashes are ordinary build/raw evidence, not gate authority.

Single real preflight: first128 untouched ProofNet sources plus original257(accepted),2913(incomplete),5879(operational crash),5880(following rejected),132unique attempts; width1/lifetime128 on both paths, CPU9–12. This crosses one actual elective worker retirement and actual failure replacement, with necessary basic native outcomes. Original indices are mapped explicitly to dense transport indices for this preflight only; full inputs are unchanged. This is readiness, not a performance result or a small formal benchmark substitute. Max3 actual preflight attempts; current0/3. Review current0/3; one fresh reviewer and at most two follow-ups in one plan-review file.

Command: `python3 -u artifacts/lean-service-lifecycle-2026-10-13/experiment020/run.py preflight` then, on real engagement/basic completion, the same script `full`. It calls the existing official-native snapshot/seeded-stream acquisition adapters, exact4.9 runtime and default native checking. It archives ordinary complete capture directories into lossless ZIP **after** timed acquisition, verifies archive integrity/member coverage before reclaiming only those own completed expanded members. Failed/partial raw are never removed. Inputs, all source objects, binary/source copies and commands remain retained.

Full completion requires all48 terminal complete source populations plus raw metrics/engagement/basic comparisons and fresh independent result review. Driver first completes ProofNet24conditions, then waits for actual E015 terminal before mini24; waiting is a physical heavy-resource constraint, not a research deadline. It does not stop because a result is negative. Capacity/external faults preserve every partial and resume only valid terminal unaffected cells; no timing-state stitching across interruption. Whole failed cells are excluded from effect ratios with stated reasons, not dropped from coverage.

Raw root: `artifacts/lean-service-lifecycle-2026-10-13/experiment020/`; separate preflight1 and full1 output directories. Ordinary analysis recomputes terminal coverage, paired makespan/throughput/CPU, basic differences, native engagement and profile resources; analysis files do not control gates.

## Interpretation and paper output

Target figure/table: complete formal makespan/CPU/PSS versus worker lifetime for both methods, with all paired values and clearly separate resource samples. Positive effect depends on complete matched engagement, basic outcome fidelity and full costs. Lack of material improvement or reversal is retained as a tested native lifecycle boundary. Material memory reduction with flat latency is a resource tradeoff, not throughput speedup. Missing/biased/concurrently disrupted conditions are incomplete or inconclusive. No invented numerical threshold, significance from three small ratios, universal service isolation, whole-RQ closure or GPU extrapolation.

The full paper remains ambitious Lean/SMT service and heterogeneous verification. This comparison cannot alone establish per-candidate native-history isolation, bounded placement, cancellation, online load scaling, full GPU checking, modern snapshot superiority or OSDI novelty. Those obligations stay open.

## Actual execution record

Fresh independent round1 admits execution; root accepts it after reading actual report. Initial model-capacity failure returned no review. Ordinary session-count display and heavy-owner terminal observation corrected without changing scientific matrix/source/native version. Actual preflight1/3 starts PID22277; review1/3 retained. No empirical result yet. Numerical resource estimate from prior complete ProofNet ordinary captures:8.5–16.6MB ZIP/cell, roughly0.30GB for24ProofNet rows plus summaries; mini storage/runtime remains uncertain because slow original whole profile is still running. Previous unlimited4workerProofNet whole~436–445s; finite replacement can add import cost, so these are logistics observations rather than predictions/quotas or budget limits. All full48conditions remain required.

Actual integrated preflight1/3 returns both132ordinary outcomes with zero basic native differences and normal acquisition EOF:129rejected/1complete/1incomplete/1operational source5879. One normal elective retirement at128responses, three worker lifetimes including failure replacement, parent1seedroot. Root independently reads raw events/outputs. Frozen complete full1 now launched; ordinary full1-launch.json/command files hold actual handle/source identity. No lifetime/source/oracle/width/matrix change. Complete planned48conditions remains pending.
