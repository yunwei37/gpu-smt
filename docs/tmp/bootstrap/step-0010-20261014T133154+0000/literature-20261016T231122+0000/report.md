# Deeper Lean state reuse: source and workload admission

Observed 2026-10-16T23:11–23:20Z, root direct work under step0010. Parent: the complete E040negative constructor and current E038native comparison. User instruction, complete Initial Narrative, current paper/RQs, evaluation and prior closest-work map were read. This is research-literature-novelty with primary verification and experiment handoff, not a performance experiment or independent review. No agent/model/native session or replacement Workspace was started.

## Questions and finite coverage

C1/RQ1: does a released deeper proof/search context provide real paid reusable work beyond already-warm imports? C2/RQ2–3: which current tools already supply intermediate-state reuse, independent goals and native lifetime management? C3/RQ3: would switching the workload or adding a benchmark actually discriminate the proposed runtime mechanism from competent reuse? Claims are stated without system names: native state sharing must improve the complete behavior/resource frontier, beyond existing snapshots and logical branching.

Coverage branches: official benchmark/tracing assets; released search trajectories versus extracted successful proofs; actual state-reuse/parallelism source; version compatibility and complete-cost measurement. The related systems/venue precedents already verified in the current closest-work map are reused, rather than repeating their search. Completion here means a source-supported include/defer/reject decision for these declared branches, not exhaustive literature or final novelty certification.

Exact initial web queries:
- Lean theorem proving proof search released search trees traces LeanDojo ReProver dataset
- Lean proof search traces benchmark released failed tactics DeepSeek Prover search trees
- Lean proof verification server snapshot batching benchmark Pantograph LeanDojo native state reuse

Revised queries:
- "LeanProgress" "github" "dataset"
- "LeanTree" "Factorized States" github
- "ReProver" "search_traces"

Primary pages opened: LeanDojo official project/docs and NeurIPS2023paper; LeanTree author GitHub/README, arXiv2507.14722v1 full text/PDF and official dataset card; ReProver and DeepSeek-Prover-V1.5 official repositories; Pantograph official mirror/README; official LeanDojo-v2 issue5. Secondary Reddit, ecosystem directories, ResearchGate and blog summaries were leads only and do not support the judgments. OpenReview PDF returned a browser challenge; the author-identified arXiv version supplies the independently accessible primary paper, without bypassing the challenge or inventing access.

## Verified source and version findings

**LeanTree paper.** [Primary paper](https://arxiv.org/html/2507.14722v1), Kripner/Šustr/Straka,19July2025; [author citation](https://github.com/Kripner/leantree/blob/53493b9fb48a10a21d01cc6ff77f824e26b6217f/README.md) identifies the ICML2025AIforMath workshop, not the main conference. Goal factoring and verification of only newly introduced assignments (AppendixB) already reduce repeated work. They cannot be claimed as our new device algorithm. No published speedup is transferred. Primary PDF: docs/reference/leantree-2507.14722v1.pdf.

**Current LeanTree source.** GitHub HEAD was pinned to53493b9fb48a10a21d01cc6ff77f824e26b6217f, with lean-repl submodule620bc68ed74bdffc35fe17116e68e0cc977f23cc. [README](https://github.com/Kripner/leantree/blob/53493b9fb48a10a21d01cc6ff77f824e26b6217f/README.md) declares Lean4.27.0. This removes a superficial version-based reason to omit it from source comparison, but does not establish Mathlib/REPL protocol identity or a runnable numerical baseline. Its current warm server and historical workshop experiment are different versions.

[process_pool.py](https://github.com/Kripner/leantree/blob/53493b9fb48a10a21d01cc6ff77f824e26b6217f/leantree/repl_adapter/process_pool.py#L514) drains output and rolls back the environment checkpoint before returning a worker. [interaction.py](https://github.com/Kripner/leantree/blob/53493b9fb48a10a21d01cc6ff77f824e26b6217f/leantree/repl_adapter/interaction.py#L528) implements that checkpoint as the environment ID. This is not evidence of complete native mutable-cell privatization or of a fully finished arbitrary background task graph. Do not mislabel environment-ID reset as either full runtime isolation or no reuse.

[metavar_graph.py](https://github.com/Kripner/leantree/blob/53493b9fb48a10a21d01cc6ff77f824e26b6217f/leantree/metavar_graph.py#L47) groups goals using shared metavariable dependencies. These logical independence checks are prior art. They do not identify costly independent dynamic defeq work, GPU batching readiness or a wall-time fraction. Distinguish goal-state parallelism, native mutable runtime cells and task lifetime.

**Official LeanTree dataset.** [Card](https://huggingface.co/datasets/ufal/leantree) describes extracted Mathlib4.19and DeepSeek-Prover-V1proof trees, source spans/imports/contexts and extraction errors. The inspected file-tree API lists250,180,579-byte Mathlib and51,595,228-byte DeepSeek JSONL artifacts. It is not a measured request-arrival trace or complete failed model-search stream. The current code's4.27pin does not retroactively version-migrate the4.19data. The dataset viewer reports a schema-casting failure, not missing raw files. No whole-data download, migration, artificial verifier arrivals or new performance census was performed. Source graph shape alone cannot establish paid preparation.

**ReProver.** Official HEADfd6d99c01e8bd8fd8f3fd1de4cd0bc4a7f158eaa. [proof_search.py](https://github.com/lean-dojo/ReProver/blob/fd6d99c01e8bd8fd8f3fd1de4cd0bc4a7f158eaa/prover/proof_search.py#L96) retains one Dojo environment while expanding states and returns proof/status/actor/environment timing and node aggregates. These aggregates alone are not timestamped failure-inclusive verifier requests. Source inspection does not prove that no external release exists; a faithful live/released trace still needs exact per-request native state associations.

**DeepSeek-Prover-V1.5.** Official HEAD2c4ba9119eef74d0d611f494261b2c5bae98c69a. [RMaxTS implementation](https://github.com/deepseek-ai/DeepSeek-Prover-V1.5/blob/2c4ba9119eef74d0d611f494261b2c5bae98c69a/prover/algorithms/rmax_tree_search.py) writes search checkpoints and final trees. Executable logging code is not a discovered published complete trace. No untrusted pickle is loaded and no new model inference run is launched.

**LeanProgress and retained LeanPolish.** Official [LeanDojo-v2 issue5](https://github.com/lean-dojo/LeanDojo-v2/issues/5) requests artifact publication; its current status is not proof of a runnable complete release. A source synthetic-sample helper is not a real workload. Existing LeanPolish pinned complete-menu/native saved-state source,4.21assets and failed alternatives were already verified in step0005/0006. That prior handoff is reused. Repeating their counts or silently replacing native menus by later successful rewritten tactics would add no new evidence.

## Novelty judgment and experiment handoff

Same-mechanism risk remains high for saved states, independent goal factoring, warm workers, ordinary native tasks, pools and rollback. No newly discovered differentiated system contribution follows. The current runtime-cell/task-lifetime constructor must earn a useful complete frontier against its actual same-toolchain native batch competitor; a new name or deeper-state dataset cannot make ordinary snapshots novel.

Use LeanTree as citation/source-level prior art now. A numerical comparison becomes necessary only if the proposed complete interface/workload actually matches its factorized proof-state contract; then use its official version and published protocol rather than a newly written toy search engine. Its current server defaults/policies are not silently applied to the owning Workspace or existing captures. Do not add it as another redundant main baseline to the ongoing stock/private/off matrix.

Reject a standalone new tree/context census or full Mathlib re-extraction: neither success nor failure would show saved expensive work, runtime-branch isolation or complete source speed. Defer new live search/model generation until a concrete mechanism and matched complete-cost question require it; existing source-based traces are not genuine request arrivals. This is an admission decision, not a negative measurement of unavailable work.

Preserve the current E038full acquisition and collect its whole terminal once, distinguishing eager-v1capture from the first-write implementation. Full RQ3performance, supported artifacts/lifetime behavior, broader real contexts, useful GPUwork and differentiated contribution remain open. E040stays closed. The original Lean/SMT/service/RTX5090/OSDI-quality goal is retained; it is not reduced to a source survey.

Canonical background-related-work.md contains another retained author's dirty work and is not overwritten/staged here. Root adds the verified prior-art distinction/citation to the current manuscript and links this handoff from evaluation. Scope of review is root self-check only; independent audit remains missing. Exact source retrievals were small public GitHub commit/tree/raw and HF file-tree/card requests from the owning Workspace; inspected sources remain in /tmp/gpu-smt-proof-search-assets-20261016T2311, reproducible from pinned URLs above, no alternate checkout/build tree or project model deployment.
