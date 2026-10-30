# M step021 — batch numeric proposal, complete grid certificate, original-kernel checks

自审,2026-10-30. This completes the requested second minimal prototype and pairs it with the individual opportunity audit in step020. It changes a computational representation and proves the original mathematical goal; it is **not** a transparent same-budget replacement inside the production engine.

## Question, result and role

Supporting experiment: can a bounded numeric computation be extracted into a small certificate whose completeness/soundness the original kernel actually checks, and can independent check chunks overlap? A positive result supports integrating a narrowly defined certificate method; a negative result would reject extrapolation from the digits example. A whole7808speedup, automatic extraction and unchanged source outcomes remain separate uncertainties.

Actual result:
- Full4,016,016-cell C scan proposes exactly(5,401),(401,5).
- A proved row-division checker covers the **whole** m,n=2..2005 square, rather than checking only the proposed solutions or sampled blocks.
- Stock Lean4.9.0-rc1 accepts all16block proofs, the coverage assembly, and the original mathd_numbertheory_541 theorem.
- Independent original-kernel rechecks achieve1.78/3.10/5.00× at2/4/8tasks, with actual overlapping intervals for every group.
- A complete generation+Lean check pipeline takes2.290783s in a separate, bounded run. This is not a ratio against the historical300s run on another node.

## Algorithm and trust boundary

1. `compute_reference.c` performs an ordinary unsigned64-bit batch scan over the4,016,016grid points. All arithmetic here fits, but **correctness of the generator is not trusted**. The generated solution list is inserted into a source copy on the existing PVC by `generate_grid_certificate.py`.
2. For a row m>0, a proved lemma uses mn=2005 to derive2005%m=0 and2005/m=n. If the quotient lies in2..2005, the checker requires both that the pair occurs in the payload **and** that its sum equals406. Omitting a real solution cannot produce a successful check. Out-of-range n=1 at m=2005 is handled by the bound conditions, not silently discarded.
3. `block_sound` proves every row in a successful structural block is checked. `block_append`/`block_join` compose sixteen disjoint128-row blocks (last84rows), covering all2004rows.
4. The final theorem derives m,n<=2005 from the original hypotheses and applies the checked row result. Original kernel rechecking verifies the declaration and all its mathematical dependencies.

TCB: original Lean kernel and its standard logical foundations; evaluator/completeness/equivalence lemmas are proved **in Lean**, not new axioms. The axiom reports contain only propext/Quot.sound; no sorryAx, native_decide, trusted C answer, GPU predicate or assumed certificate soundness. The prototype is specialized to this Nat product grid, not a general verified IR for Nat/Int/Bool/List/Finset/arbitrary recursion.

The key improvement is algorithmic **row compression using division**, not a faster implementation of4million Boolean kernel reductions. The old dense-check projections remain projections. No exact speedup is computed between them and this different algorithm. CPU numeric generation already costs only milliseconds here; these measurements do not motivate a GPU generator for this instance.

## Native execution and own denominator

All outputs/modules/source snapshots are on existing PVC, no container/tmp outputs. One M native process at a time; source maxHeartbeats200000; every explicit kernel recheck has finite1000000heartbeat argument; -M8192cooperative process-RSS guard; internal wall120s; CPU8–15/eight jobs within M16GiB/eight-core allocation. No external kill, host security/configuration or other branch mutation.

The v5 group is finite and terminal: three complete source checks followed by one chunk-measurement process. All four return0 and retire:
- Full Lean source runs2.171878,2.172063,2.171900s, each including imports, declaration construction/initial checking, axiom printing and one **additional** final-theorem recheck.
- Extra final theorem kernel rechecks39.630,40.147,39.625ms.
- Maximum sampled own-tree RSS across these runs631,984,128B, not a claim of total four-branch/node memory.
- v5 generation: C compile74.267ms, numeric process3.241ms; scan's own lattice CPU2.384ms. Source-emission IO was not separately isolated in v5.

The v6 single pipeline closes that cost boundary. **2.290783s** includes compiler invocation, numeric scan, payload emission, full native Lean invocation, collection IO and one additional final recheck. Generator/source-emission subtotal75.206ms (compile71.211ms, scan process3.335ms); native invocation2.171983s. Difference includes Python/import/capture overhead, so do not force rounded subtotals to add or subtract the extra recheck to claim an unmeasured optimized latency.

v6 measured source phases:
- sixteen initial chunk declarations:790.054ms, includes elaboration/proof construction plus checking;
- block coverage assembly:29.227ms;
- final theorem construction/check:137.320ms;
- extra isolated final theorem kernel recheck:39.546ms.
The phase markers omit preceding imports and generic soundness proofs; **2.290783s is the whole pipeline denominator**. The final kernel recheck and initial final-theorem construction are separate, overlapping-content work and not added as new saved time.

v6 sampled own-tree peak566,886,400B (~.528GiB); native process CPU2.145372s; sampled node MemAvailable remained above allocated branch budgets. Every receipt contains actual boot/PID/birth and retirement checks.

## Chunk parallelism: actual measurements

Within one Lean process, each task receives the same immutable already-checked environment, rechecks independent closed chunk proof values with `Environment.addDeclCore`, and returns success only after the kernel accepts them. No shared goal/metavariable merge occurs. Results are collected in input order; per-chunk log arrival can differ.

The returned environments are discarded. The original chunk declarations have **already been initially checked sequentially**; the final theorem uses those original declarations. This measures parallel **recheck** capacity, not a completed parallel first-check/merge pipeline or service-throughput gain. Per-task finite budgets are not a globally merged native heartbeat policy; operational parity has not been demonstrated.

v5 runs both8→4→2→1and1→2→4→8orders, three repetitions each. Absolute monotonic chunk start/end intervals confirm maximum concurrency1/2/4/8in **every** respective group. No repetitions were removed.

| tasks | groups | minimum s | median s | maximum s | serial/median |
|---|---:|---:|---:|---:|---:|
|1|6|.273800|.276177|.278787|1.000|
|2|6|.154461|.155573|.156680|1.775|
|4|6|.087807|.089030|.089737|3.102|
|8|6|.054438|.055213|.058854|5.002|

The earlier v4 point showed near-serial first groups. Its raw data remain, cause unknown; no assertion that it was a kernel global lock or a particular thread-pool bug. The counterbalanced v5 result supplies actual concurrency evidence but does not retroactively rewrite v4.

For this already compressed checker,8tasks save about.221s in the recheck phase. Total2.291s pipeline throughput improvement is **not measured**. Cold imports, proof generation, coverage assembly, final checking, memory, and future environment merge cannot be assumed free.

## Outcome modes and integration obligations

- If the original proof has valid preceding steps and the expensive closed computation is true, a proved equivalent evaluator/certificate can make a native timeout or memory-budget failure complete. Mathematical truth is preserved; **the fixed-budget operational verdict changes**. Such recoveries belong to an explicit acceleration/new operational mode, with accepted-set differences reported.
- If an intermediate assertion is false (nine explicitly identified cases in the126audit), proving the final problem by a different certificate does not validate the original proof. Keep rejection in a source-verification mode; a new proof must be reported as proof repair separately.
- If exact native budget labels and diagnostics are required, the current prototypes provide **zero qualified original-source replacements**. We have two checked goal-family theorems, not49demonstrated timeout recoveries. No production adapter/cache/CLI behavior changed.
- False computational propositions cannot be accepted by a sound original-kernel certificate path. Timeout/resource labels themselves are not a proof of falsity.

Prior art: verified reflection, specialized evaluation, and asynchronous independent proofs are established; see prior-work.md. The new evidence is workload-specific coverage and actual construction/checking costs, not novelty from reusing those techniques.

## Receipt correction and preservation

v5 run_finite used cumulative RUSAGE_CHILDREN CPU and highwater fields across serial runs. Those original receipts are preserved, **not** used as per-run CPU/residence evidence. Future receipts use a CPU delta and explicitly label highwater cumulative scope; v6 uses the corrected snapshot. The v5 old human hardware label still saysCPU8–11/serial, while its authoritative argv/jobs/affinity fields sayCPU8–15/-j8; original metadata remain and this erratum resolves scope. No v5 timing was rerun just to relabel receipts.

The witness-v2 controller was launched immediately before that source-scope correction; its captured runner.py actually contains the corrected version. Interpret that run by its frozen snapshot, not an assumption about launch timing. New captures start from complete frozen source in future groups.

All v1–v3prototype failures, v4startup behavior, v5repetitions and v6pipeline remain on PVC; small source/stdout/stderr/receipts are archived under this M directory. No generated binary or large capture was added to Git.

## Daily substantive reflection and next evidence

The useful split is **algorithmic normalization first, parallel certificate checking second**. The grid's original4millionbranch formulation becomes2004row checks after a short proved theorem; a GPU or generic branch scheduler would attack a poorer representation. The digits example similarly avoids expensive proof-bearing recursion by a proved structural evaluator. However, nine explicitly identified incorrect prefixes and EPFL's mainly symbolic budget failures prevent treating a true final theorem as an original proof verifier.

Next supported work is a narrow original-goal adapter that identifies a closed subgoal and applies an already-proved equivalence without dropping prior errors, then a matched new-resource-point measurement that separates changed budget outcomes from source-verdict preservation. A general computable-fragment compiler, parallel environment merger and49source recoveries remain unimplemented; no hidden task is declared complete by these microbenchmarks.

## Reproduction and final self-review correction

From the retained Workspace, choose a fresh PVC capture label:

```sh
python3 research/mechanisms-2026-10-30/run_grid_certificate.py FRESH_LABEL
# Optional distinct fresh label, includes all24counterbalanced chunk groups:
python3 research/mechanisms-2026-10-30/run_grid_certificate.py FRESH_CHUNK_LABEL --measure-chunks
```

The checked-in runner uses this declared M hardware point and finite budgets; it is not a production engine default. Its public one-command path was actually executed once with a fresh label; receipt/source and pipeline terminal are retained under reflected-grid-public-repro. Python syntax compilation and --help also pass. It is a reproducibility check, not another throughput experiment.

Final prefix review found two more definite incorrect restrictions: minif2f970excludes the valid(16,2) power solution, and minif2f2401asserts period2for Fibonacci residues despite a1=a2=1 forcing a3=2. Original-kernel witness-v3 accepts the counterarguments, no sorryAx. Derived coverage tables now have9known proof-repair cases rather than7; the49checked-family/37other opportunity totals do not change. Step020's original count is preserved with a forward erratum. This is not an exhaustive proof-correctness audit of every other prefix.
