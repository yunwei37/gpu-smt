# Prior art and differentiation

This file tracks the closest systems and solver work. The goal is to avoid claiming novelty for ideas that already exist and to sharpen the system boundary.

## 1. Mallob

- Project: https://github.com/domschrei/mallob
- Scope: scalable automated reasoning on demand, multi-user job scheduling, distributed SAT, incremental SAT, and recent SMT extensions.

Why it is close:

- treats automated reasoning as a service/runtime problem;
- dynamically allocates compute to reasoning jobs;
- supports priorities and incremental solving.

Difference we want to test:

- Mallob primarily scales reasoning jobs across CPU/HPC resources.
- Our target is **cross-job incrementalization**: automatically discover related contexts across otherwise independent application jobs and reuse live solver state.
- We explicitly target both low-latency and high-throughput SLOs for many small/medium related verification requests.

Any paper must compare against Mallob conceptually and, where practical, experimentally.

## 2. Fine-grained caching in Boogie/Dafny

- Rustan Leino and Valentin Wüstholz, “Fine-grained Caching of Verification Results,” CAV 2015.
- https://www.microsoft.com/en-us/research/publication/fine-grained-caching-verification-results/

What it does:

- uses program call/control-flow structure to avoid reverifying unaffected parts after edits;
- implemented in Boogie and used by Dafny.

Difference:

- program-level invalidation and cached verification results are not new;
- our proposed runtime operates below the frontend, across applications/processes, and reuses **solver contexts/state**, not only completed verification results.

## 3. ViperServer

- https://github.com/viperproject/viperserver

What it does:

- server for Viper verification requests;
- avoids JVM startup overhead;
- exposes HTTP APIs;
- supports caching/development workflows.

Difference:

- Viper-specific server infrastructure;
- not a general solver-state serving layer across unmodified verifier frontends/backends.

It is an important baseline for “warm process/server” effects.

## 4. KLEE solver chain and Green-style constraint reuse

KLEE already uses:

- query cache;
- counterexample cache;
- expression hashing;
- independence decomposition.

Green and related work explored persistent reuse/canonicalization of constraints across symbolic execution.

Implication:

> exact query caching, canonicalization, and result reuse are infrastructure, not the main novelty.

Our stronger target is a hierarchy of reusable state:

```text
exact result
  -> exact hot context
  -> nearest prefix context
  -> warm solver
  -> cold solver
```

plus state-aware scheduling.

## 5. ParaFROST

- https://github.com/muhos/ParaFROST

What it does:

- parallel SAT solver;
- GPU-accelerated inprocessing;
- variable elimination, simplification, garbage collection, and related operations on GPU;
- incremental SAT support and CBMC integration.

Difference:

- ParaFROST accelerates phases **inside one SAT solving engine/instance**.
- Our GPU hypothesis is primarily **inter-query parallelism across many related verification jobs**.

Therefore “GPU SAT” is not a novelty claim.

## 6. AWS Zelkova

- https://www.amazon.science/blog/a-billion-smt-queries-a-day

What it shows:

- production verification can reach roughly billion-query/day scale;
- synchronous solver latency matters in request paths;
- solver runtime is highly variable;
- portfolio solving with Z3/CVC4/cvc5/custom engines is useful.

Implication:

- low tail latency and high aggregate throughput are both real industrial requirements;
- hedging/portfolio routing is already used in production and should not be claimed as new by itself.

Potential difference:

- a general open runtime that automatically reuses state across related jobs and applications.

## 7. Incremental SMT itself

SMT-LIB and major solvers already provide push/pop and check-sat-assuming.

Therefore:

> “reuse a prefix with push/pop” is not novel.

The research question is whether a transparent runtime can **recover incremental structure across independent clients/jobs**, decide when reuse beats a fresh solve, and schedule requests around the physical location of reusable state.

## 8. Lean/checker optimization

Lean kernel/checker performance work — Lean Kernel Arena, LazyLean, Nanobruijn,
Nanoda, Nanoclo, and concurrent convertibility checking — already shows
substantial headroom. Our 2026-10-04 measurements on the arena confirm this:
the best current alternative checkers (nanoclo, lazylean) reach **7.6×** the
official kernel on kernel-bound tests by parallelizing across declarations, and
kernel checking is 84–94% of real library check time
(`results/2026-10-04-lean-kernel-stage-split.md`).

This shapes differentiation rather than eliminating it:

- we do **not** claim novelty for a faster kernel algorithm or a faster
  standalone checker;
- the Lean thread here contributes (a) the stage-separated characterization
  (parse/setup vs elaboration vs kernel checking) that most checker papers
  collapse, and (b) the *serving* question: batch many independent checks
  (agent candidate proofs, `decide` certificates) under latency/throughput SLOs.
- GPU differentiation is specifically **data-parallel checking of many
  independent declarations**, not an intra-kernel CUDA port and not the
  STARK-certificate proving of `argumentcomputer/ix`, which is a different
  proof system.

Lean is therefore no longer only a later generalization test; it is an active
second workload for the same reuse/serving abstraction.

## Proposed differentiation

The strongest current formulation is the combination of:

1. **backend-unmodified compatibility**;
2. **application-transparent integration**;
3. **cross-job context recovery**;
4. **live solver-state reuse, not just result caching**;
5. **state-affine SLO-aware scheduling**;
6. **joint latency/throughput optimization**;
7. **optional heterogeneous CPU/GPU paths**;
8. **real CI, interactive, and agent-generated verification workloads**.

No single bullet should be presented as sufficient novelty. The contribution is the systems abstraction and end-to-end design.

## Primary novelty risk

The biggest risk is that a close system already performs automatic cross-client context recovery and live state reuse at the same abstraction boundary.

Before paper writing, continue searching in:

- SAT/SMT serving and cloud solver systems;
- symbolic execution cache systems;
- theorem prover servers;
- incremental compilation/verification;
- process checkpointing of solver state;
- multi-query optimization in databases and model checking.

If close prior art appears, update this document and narrow the claim.
