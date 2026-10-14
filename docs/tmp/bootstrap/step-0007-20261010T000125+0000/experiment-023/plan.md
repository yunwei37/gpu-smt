# Experiment023: complete native verification under scheduled arrivals

## Research question and admission

RQ3 exactly: **How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse?**

Test whether separating an immutable prepared parent from independently executed candidate branches changes the latency/memory tradeoff under offered load relative to competent warm native reuse. Offline closed-loop E020 measurements cannot answer this: the unlimited warm policy has only1.7861% mean improvement with one slower pair, and instrumented median latency is worse despite lower sampled PSS. Finite retirement128 gains are configuration effects, not universal reuse benefits. New external arrivals expose queue buildup and resource costs hidden by closed-loop dispatch.

This is a decisive main-formal service comparison, not a benchmark of fork or worker retirement. It uses every original candidate and all native outcomes. A useful positive result must survive both strong reuse paths at the same offered rate/resources; a negative result bounds the proposed service mechanism. Neither outcome establishes novelty by itself. Fork/COW, snapshots, REPL backtracking, pooling and success caches are existing mechanisms. All other RQs, concurrency/placement/history/cancellation/SMT and actual heterogeneous service remain open.

The best alternative is the actual heterogeneous full verification matrix E022. It is already admitted and has a ready repaired finite GPU request. Duplicating it or its negative373-graph component comparison adds no evidence. This service experiment addresses an independent load-bearing promise while preserving all effective E008/E018/E015 and the original finite queue.

The current expectation is that disposable branches pay more per-candidate startup cost and can lose latency/throughput to long warm workers. Shared preparation may reduce sampled memory, but a tail-latency loss can offset that saving. A reproducible advantage against both competent methods over the complete load sweep would contradict this narrow overhead prediction. Cache timing, finite arrival duration, CPU competition and first-header preparation are competing explanations that must remain visible.

## Real assets and published protocol

Use all5952 ProofNet186test×32 and7808 miniF2F244test×32 original captured Lean4-port candidates, including failures, incomplete proofs, duplicates and original operational sources. Exact official problem lineage, port/toolchain adaptation, generation restart segments and fixed Lean4.9.0-rc1/Mathlib versions remain those of E014/E020/E021; no resampling or success selection. Original ProofNet is Lean3, so the port is explicitly disclosed. Inputs remain `experiment014/inputs/{proofnet,minif2f}/input.jsonl`.

The measurement follows the author's [wrk2 scheduled-arrival latency protocol](https://github.com/giltene/wrk2): latency begins when a request was scheduled, so delayed release and queueing cannot disappear. [DeathStarBench](https://github.com/delimitrou/DeathStarBench) supplies a systems benchmark precedent for externally offered load and latency/resource interpretation. This implementation uses actual native NDJSON stdin, with synthetic evenly spaced arrival times over real candidate bodies. It is neither production traffic nor an HTTP/wrk2/DeathStarBench performance reproduction. The first header is prepared only after it actually arrives; the verifier cannot inspect future candidates for free.

Necessary adapter: the existing native seeded stream, guarded quiescent fork and normal checking from E020, plus nonblocking stdin, finite load generation and ordinary raw analysis. No persistent service, scheduler, research-control schema or toy checker is installed.

## Methods and fairness

1. **branch:** runtime2 stream with retirement1. Each executed candidate receives a separate COW child from the quiescent first-header parent; later different headers use original private native preparation/fallback. Completed exact duplicates may use the common success-only cache. This is the proposed isolated lifetime method, not an algorithm/checker change.
2. **prepared:** the same runtime2 with unlimited shared warm children. This is a direct component replacement that tests whether lifetime separation costs outweigh sharing; it is not another novelty claim.
3. **snapshot:** unchanged E020 native `full` stream per worker, with original native full command snapshots and the same caller success-only cache. This is the strong independent warm/logical-snapshot competitor. It is not cold compilation or repeated fresh imports. The implementation retains candidate-prefix snapshots and performs ordinary native checks.

Both comparison paths matter: beating a weak snapshot implementation while losing to long-lived warm children cannot support superiority. Every method uses the same real source bodies/order, finite pending FIFO, worker opportunities, completed-success-only exact(header,code) cache and no in-flight duplicate coalescing. No failed/incomplete response is cached. Native threads/options and original300s dispatch allowance are unchanged. Queue waiting does not consume that allowance. All initialization/root preparation, dispatch, verification, cache, failure/replacement, output and EOF costs are measured.

All methods inherit CPUs0–3 in this owning Workspace, whose actual allowed mask is0–23. ProofNet has4 native frontend workers; mini has1 because the demonstrated heavy-native footprint cannot support duplicate concurrent mini workers alongside the existing shared host. Affinity is permission, not CPU isolation. The same mask/width applies to every matched condition. There is no memory quota or exclusive-host claim. This fixed-resource load sweep supplies evidence toward RQ3; it does not complete promised concurrency/placement/cancellation evaluation. Mini starts only after the original heavy queue actually finishes, never by stopping another owner.

## Rates and metrics

Rate selection is fixed from the independent strong snapshot path in the already admitted E020, not from a favourable new service result. For each dataset, define mu=N divided by the mean whole time of its three valid primary snapshot cells with no elective retirement. Use rates0.5mu,mu,1.5mu unchanged across methods and repetitions. Existing complete ProofNet snapshot times461.812460563/451.787762609/455.610208771s give mu13.041092576735014/s and rates6.520546288367507/13.041092576735014/19.561638865102523/s. The mini rate follows the same declared formula once all three original mini snapshot cells are actually valid; no new calibration corpus or tuning search is added.

Primary: scheduled-arrival-to-terminal p50/p95/p99/max, complete throughput/makespan and queue growth at each offered rate. Actual release, generator lag, dispatch and queue delay remain separate. Low-load terminal throughput following the offered rate is not evidence of capacity. Full drain includes every source; overload does not drop pending candidates or invent an arrival deadline. Report all outcomes, not only accepted proofs. Secondary: success-cache engagement, actual child starts/exits/retirement, sampled process-tree CPU/PSS/private memory and native EOF. One-second non-atomic sampling/observer cost/incomplete samples and unsampled peaks remain explicit.

Three whole primary repetitions use rotated method order: branch/prepared/snapshot, prepared/snapshot/branch, snapshot/branch/prepared. Load factors are0.5,1,1.5 in rep0,1,1.5,0.5 in rep1,1.5,0.5,1 in rep2. One separate resource profile per method/dataset at mu uses snapshot/prepared/branch. Report paired effects and observed ranges; no fabricated confidence interval or profile clocks substituted for primary means. Equal-source basic outcomes use retained stock references plus direct paired comparisons. Original operational source5879 is kept separately; any new avoidable failure invalidates the affected performance comparison.

## Complete matrix and execution

| Group | Methods | Loads | Repetitions | Cells per dataset |
|---|---:|---:|---:|---:|
| primary |3|3|3|27|
| resource profile |3|mu|1|3|
| total | | | |30|

Both complete datasets therefore require60 cells/412800 original source outcomes:30ProofNet cells178560 plus30mini cells234240. This is one integrated service experiment, not one contribution per rate, worker or dataset.

Authoritative finite command is `python3 artifacts/lean-service-lifecycle-2026-10-13/experiment023/run.py preflight` after one fresh independent plan review. The smallest actual end-to-end case uses unchanged E021 ProofNet8/mini3 originals, all three methods, with scheduled arrivals, all native outcomes and actual responses before input EOF. No generated fixture or diagnostic-string campaign. Root verifies branch worker replacement, warm snapshot engagement, source identity/basic outcomes and final EOF using existing raw events. Genuine systematic runner faults are repaired without changing the approved hypothesis.

Full commands are `run.py full-proofnet` and later `run.py full-minif2f --calibration E020_COMPLETE_ANALYSIS.json`. They select the complete30-cell dataset block and exclusive raw output. The E020 analysis is ordinary raw evidence for the numeric load parameter, not an executable gate or authority artifact. The root's Markdown disposition remains authority. No preflight automatically launches full work. Exact runtime2 source/build/commands/input identities are retained per cell. Complete measured cells are losslessly archived only after whole EOF clocks, with CRC/exact-member verification before expanded duplicate reclamation. Failed/partial/unique raw/core/other owner data are preserved. No clock stitching or unchanged invalid retry.

## Interpretation and result review

A benefit requires valid complete basic pairs and lower arrival latency or a reproducible memory/throughput frontier advantage against both competent methods at the same rate/resources. A resource saving with slower tails is a tradeoff, not an unconditional acceleration. If warm/snapshot match or win, report that result and reject this tested branch policy as the claimed performance contribution. A shared warm replacement gain is a CPU reuse result, not GPU acceleration. Avoidable failures, mismatched information/resources or incomplete cells make a comparison invalid/inconclusive.

Target figures show latency and queue buildup versus offered rate, separate three-run whole observations, and the single profile memory/CPU tradeoff. A fresh independent complete-run result review recomputes every original source, metric, native mechanism and resource boundary before paper numbers. All60 cells, complete paired populations and source-native cost engagement are required; compilation, initial response or a partial prefix is not completion. All four RQs, complete service/SMT/GPU scope, full writing and independent outer audit remain open until their own evidence is delivered.
