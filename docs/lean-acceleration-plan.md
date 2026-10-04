# Lean acceleration plan (research thread)

This document scopes the second research thread — **accelerating Lean
verification** — and its relation to the existing SMT solver-serving work. It is
companion to `docs/research-plan.md`.

Measured evidence lives in `results/`; this file is the plan and the decision
rules, not the numbers.

## Question

User ask: *can Lean verification be made dramatically faster, and can useful
parts run on a GPU?* Concretely, is there a large, real class of Lean work that
is (a) dominant in wall time, and (b) batchable enough to exploit GPU
throughput while preserving proof accept/reject semantics?

## Stage model (mandatory in every measurement)

Lean work must be reported by stage; a single "Lean is slow" number is
meaningless:

| Stage | What it is | Where measured |
|---|---|---|
| import/parse setup | deserialize + materialize the environment | `--parse-only`, RSS |
| elaboration | tactic execution + proof term construction | `set_option profiler true` |
| kernel checking | type-check the elaborated proof term | full-run − `--parse-only` |

The same split applies to external checkers: they all pay a parse/load floor
(≈ the same RSS as the official kernel) and differ only in the checking stage.

## Benchmark choice: lean-kernel-arena

[`lean-kernel-arena`](https://github.com/leanprover/lean-kernel-arena) is the
right primary benchmark:

- **real**: `init` / `std` / `cslib` / `mathlib` are complete library exports
  from the pinned upstream revisions, not synthetic formulas;
- **reproducible**: exports are content-addressed by sha256 recorded in arena
  metadata;
- **correctness-preserving**: it scores accept/reject, so acceleration cannot
  silently weaken the check;
- **directly relevant**: it is literally the community's cross-checker speed
  benchmark for Lean kernels.

Secondary probes: the arena `perf` suite (kernel stress tests) and
`set_option profiler true` runs on representative proofs, which separate
elaboration from kernel checking.

## Observations from the first measurement round

(Full tables: `results/2026-10-04-lean-kernel-stage-split.md`.)

- Kernel checking is **84–94%** of wall on real libraries and **97%** of the
  `perf` stress suite.
- The kernel is **memory-latency-bound**: 2.6× instructions and half the IPC of
  parse-only. This is the mechanism that decides whether a GPU can help.
- Best-in-class alternative checkers (nanoclo, lazylean) already reach **7.6×**
  the official kernel on kernel-bound tests by parallelizing across declarations.
  Any GPU claim must beat *those*, not single-threaded Lean.
- Elaboration can dominate individual proofs (`magma-list-deep-n36`: 17.1 s in
  `decide`, 1.65 ms in the kernel), so "Lean is kernel-bound" is a *class*
  statement, not a universal one.
- Batching independent exports scales ~**12–14×** on 24 CPU cores for small
  exports; giant exports thrash and batching degrades past width 8.
- Per-declaration check cost is **uniform** (0.7–0.9 ms/decl across `init`), so
  the batchable class needs no exotic load-balancing; resident environment size
  (linear in decls), not per-decl work, is the resource limit.
- In a *static* arena pass, checking time is concentrated in ~7 giant library
  exports (97.9% of a 3635 s pass; `mathlib` alone is 62.6%); tests ≤100 KB are
  0.14% of time. The batchable class therefore must be justified by an
  **agent/proof-search workload** of many small independent checks, not by the
  arena's own distribution. That is the key open measurement for rung 4.

## Acceleration ladder

Ordered by expected value / risk. Each rung must be entered only after the
previous one has a measured result.

1. **Measure and publish the stage split** (done this round). Deliverable:
   parse/elaboration/kernel separated, per corpus, with correctness.
2. **Cross-declaration CPU parallelism as the baseline accelerator** (done by
   third parties; we must reproduce and pin it). Deliverable: reproducible
   nanoclo/lazylean numbers on the same corpora, with semantics verified.
3. **Batched independent-check serving** (measured this round): treat each
   small export as a job and batch it. Deliverable met:
   `results/2026-10-04-lean-batch-serving.json` — 920 repeated-candidate jobs,
   35.9 → 517.8 jobs/s at width 24 with accept counts unchanged, via
   `bench/lean_export_batch.py`.
4. **GPU prototype for the batchable class**: a data-parallel kernel-checker
   that processes *many declarations at once*, validated declaration-by-declaration
   against the official kernel. Deliverable: GPU vs CPU makespan on a real
   corpus plus the correctness table. **Blocked on device passthrough.**
5. Only if 4 is favorable: integrate GPU behind the serving runtime as an
   optional accelerator for the small-independent-check class.

Explicitly **out of scope**: porting a whole kernel/proof search to CUDA;
rewriting tactic search; changing the export format.

## GPU decision rule

A GPU path is worth building only if all hold:

1. the target class is large in the real workload (fraction of total checking
   time in small independent checks);
2. CPU batching has not already saturated (we measured ~12–14× at 24 cores and
   bandwidth saturation, so the GPU must beat ~14× on the same class);
3. transfer cost is amortized: the batch must be large enough that PCIe
   transfer is small versus check time. Measured arithmetic: a whole `mathlib`
   export transfers in ~124 ms versus a 1.4–1.6 ks check = **~0.008%**, so
   per-corpus transfer is *not* the bottleneck; the win must come from GPU
   compute/latency on many concurrent declarations.

If (2) or (3) fails, the honest result is the corresponding negative — e.g. "a
GPU cannot beat the 7.6× CPU alternative checkers on this class" — and that is
a publishable outcome, not a failure to hide.

## Distinction from prior CUDA work

`argumentcomputer/ix` ("CUDA-accelerated Aiur proving") accelerates **STARK
certificate proving** for its own proof system, not ordinary Lean kernel
checking. Its CUDA path is not a Lean checker. We must not conflate the two when
claiming novelty.

## Infrastructure requirement

The measurement machine has an **NVIDIA RTX 5090** (PCI `10DE:2B85`, driver
610.57.04) on the host, but this container is not passed any device node: no
`/dev/nvidia*`, no `/dev/dri`, and `mknod` of major 195/226 opens with `EPERM`
(container device allowlist). See
`/workspaces/.agent-state/gpu-smt-research-request-20261004.md` for the concrete
passthrough request.

Until that lands, the CPU path (rungs 1–3) proceeds and is not blocked.

## Falsification criteria

The GPU thread is falsified (and should be reported as a negative result) if:

- small independent checks are a small fraction of real Lean checking time;
- CPU batching already reaches the memory-bandwidth ceiling with no GPU headroom;
- export transfer dominates check time at realistic batch sizes;
- a GPU checker cannot match the official kernel on the full accept/reject suite.
