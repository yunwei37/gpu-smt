# Prepared graph retention: novelty and baseline handoff

## Objective, parent and coverage boundary

Parent: step0007 E62 / experiment014, BOOTSTRAP EXPERIMENT_GATE. The question is whether avoiding reference-count writes to prepared state is a new contribution, and whether the same optimization must be granted to the warm native baseline. This supporting mechanism audit does not change the four RQs or the Lean/SMT/RTX5090 objective. User instructions and the complete Initial Narrative were reread; the current paper remains a hypothesis draft with result placeholders. The latest human direction prioritizes complete performance over more diagnostic/thread-lifetime work.

Three name-free claim questions cover the declared finite search: (1) retained read-mostly object graphs avoid copy-on-write through reference-count suppression; (2) Lean already shares imported checked objects this way; (3) a prepared parent spawning independent requests is itself novel. Search branches are runtime mechanism, native Lean implementation, and accepted systems-service precedent. No broad new baseline campaign is admitted by this literature node.

## Searches and primary verification

External search began 2026-10-12 around20:58UTC. Exact strings: `fork copy on write reference counting freeze Python gc.freeze systems memory`; `SOCK serverless fork reference counting copy on write memory Oakes paper`; `Lean verification server process fork copy on write memory reference counting`. Direct primary-source verification continued around21:03UTC. Secondary posts were leads only.

- [PEP683](https://peps.python.org/pep-0683/), accepted Python3.12: fixed reference counts suppress runtime writes; pre-fork/COW savings and earlier enterprise/Pyston practice are explicit. This is mechanism precedent, not numerical verification evidence.
- [CPython gc.freeze documentation](https://docs.python.org/3.11/library/gc.html#gc.freeze): permanent-generation tracking avoids later cyclic-GC writes before fork and discusses freed holes. It does not establish suppression of ordinary reference counting; do not equate gc.freeze with immortality.
- [Ullrich thesis](https://lean-lang.org/papers/thesis-sebastian.pdf), printed pp155-156 / PDF pp166-167: Lean supports single-threaded, multi-threaded and persistent values. Persistent values have no reference-count updates, are not freed or reused, and may reference only persistent values. Compiler constants and serialized checked-module objects already use this state and imported payload can be mapped read-only. Ordinary import replication is therefore not entirely private duplicated memory.
- [SOCK, ATC2018](https://www.usenix.org/system/files/conference/atc18/atc18-oakes.pdf), pp63-64 / PDF pp7-8: pre-imported zygote trees preserve COW without exec, with cache selection and shared-memory-aware eviction. Its mechanism is direct prior art; its serverless workloads are not numerical Lean baselines.

## Coverage, contradictions and disposition

All three threat categories have verified primary evidence. Same-mechanism risk is high: graph persistence and prepared process branches are established mechanisms. Claiming either alone as the contribution is rejected. Generic gc.freeze is an incorrect substitute for the current Lean operation. Minor page faults include allocation and runtime startup, so the older 75.7million-fault branch cell does not uniquely identify reference counts as its cause. Existing read-only imported module payload also weakens any claim that each baseline copies all of Mathlib.

The scientific objective stays unchanged: consequential complete verification performance and resource/history/lifetime behavior beyond competent warm and native reuse, with Lean prioritized. These sources do not establish that larger contribution or a positive device result. No new terminology, scientific-contract narrowing or hypothesis replacement is adopted.

## Markdown handoff to experiment design

The competing position is that a competent warm native snapshot worker can obtain the same metadata and reference-count optimization without per-candidate process cloning. Both E014 final methods already use the same build5 binary and persistent prepared metadata. This is the mandatory numerical comparison for this implementation question; PEP683, gc.freeze and SOCK remain citation-only mechanism precedents. The implementation is pinned to the original Lean4.9rc1 formal candidate toolchain; no workload migration occurs.

Proceed with the already admitted fresh32condition matrix: complete original ProofNet5952 and miniF2F7808 attempts; both methods at widths2/4; three rotated whole repetitions and separate full resource profiles. Charge preparation, retention, fork/runtime, transport, checking and teardown. Report whole CPU/system time, memory and page-fault changes as measured associations unless the causal ablation supports more. If the matched warm pool wins, do not replace it with a cold process comparator. No additional standalone lifecycle/diagnostic tests are requested.

Canonical related work receives this known-mechanism qualification. Remaining uncertainty: actual final whole performance, retention/memory cost, broader service placement and SMT/device scope. Next node is the current experiment's full run and result review, not another search loop or new probe.
