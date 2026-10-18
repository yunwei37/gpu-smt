# gpu-smt

A research prototype for **low-latency and high-throughput verification serving**.

The long-term goal is a transparent runtime that accelerates existing formal verification workloads without requiring changes to Z3/cvc5/Lean or to the applications that use them.

The current research hypothesis is:

> Modern verification workloads are increasingly streams of related jobs. A runtime can recover shared contexts across otherwise independent jobs and reuse solver state to improve both tail latency and aggregate throughput.

## Current status

Lean-first research prototype on main. The goal is useful end-to-end
verification acceleration, with all four RQs and the OSDI-quality systems
objective retained. **The first full GPU race is 1.7% faster than the CPU oracle with a warm
server, and 0.15% faster when its cold lifecycle is charged; this single
observation does not establish stable GPU benefit.**

The current [linarith/nlinarith experiment](artifacts/linarith-oracle-2026-10-17/plan.md)
checks the same 1,000 arithmetic-heavy released GoedelWorkbook candidates.
An untrusted external oracle proposes coefficient certificates; Lean checks
them and falls back on failure. Final continuation requires **more than 1.5×**
over the strongest matched native baseline, using the better valid CPU/GPU result.
GPU route closure requires applicable evidence that the zero-GPU-cost opportunity
cannot reach that target; a slow implementation alone is insufficient.
The hourly research task remains active.

| Complete comparison | Native / CPU oracle elapsed | Ratio | Scope |
|---|---:|---:|---|
| Current pooled daemon baseline / CPU oracle | 1,237.37 / 1,037.85 s | 1.19224× | One full pair, width8, same4CPUs,48GiB |
| Current pooled baseline / GPU race | 1,237.37 / 1,020.12 s | 1.21296× | Warm server; full GPU lifecycle1,036.25s gives1.19408× |
| Corrected serial-family baseline | 6,691.60 / 5,164.85 s | 1.29560× | Three full pairs, each with its own matched reference |
| Historical CPU stage | See retained record | 1.34668× | Earlier unbounded-address-space epoch; not pooled with current data |

Every cell in these CPU comparisons returns 992 complete / 8 rejected / zero
operational outcomes. Source verdicts and non-message native payloads agree;
88 source responses differ only in warnings.
[Current complete pair and raw/tail data](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/full1000-cpu/result-review.md),
[corrected three-pair series](artifacts/linarith-oracle-2026-10-17/gpu-stage/header-corrected-full1000/three-pair-result.json),
[historical record](artifacts/linarith-oracle-2026-10-17/decision-20261017.md).

The full GPU comparison is complete on the same sources, candidate concurrency
and CPU eligibility: 992complete/8rejected/zerooperational outcomes, matching
native source verdicts and non-message payloads. Only LPs with at least11rows
are eligible; CPU and GPU race with exact repair and native checking.
There are **384 real cross-candidate batches of2–5requests**, of which311are
cancelled after a member withdraws and73return results. All384retire.
This result remains below1.5× and is not GPU route closure.
[Complete GPU results, heavy tails and raw/lifecycle evidence](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/full1000-gpu/result-review.md).

The private CPU FP-first, exact-fallback mechanism completes hardware
qualification: CPU27.65s versus GPU28.05s, all24sources accepted with matching
native verdicts. It shows no useful GPU benefit, so no full matrix is admitted
for that variant. This is not a GPU-route impossibility result.
[Qualification and raw data](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/fp-first/GPU-result-review.md).

A complete separate width4 wall-cost diagnostic gives a **conditional1.93412×**
zero-LP-cost sensitivity, or **2.24363×** when deleting all CPU-oracle numeric
products and LP search relative to its own native reference. These are
optimistic fixed-other-work calculations, not GPU speedups or universal bounds,
and cannot be rescaled to the faster pooled-native clock. The stronger pooled
family's own cost diagnostic has passed real24-source qualification and
started after the completed GPU lifecycle retired.
[Complete profile and denominator limits](artifacts/linarith-oracle-2026-10-17/gpu-stage/corrected-wall-profile/full1000-result-review.md),
[pooled diagnostic protocol](artifacts/linarith-oracle-2026-10-17/gpu-stage/pooled-wall-profile/plan.md).

A supporting SHRED-parser experiment measures proof-prefix sharing on the
original miniF2F and ProofNet candidates against native batch execution.
Counts are not saved verification time. Completed, failed and partial work,
including rejected GPU integrations and closed CPU-runtime/constructor routes,
remain in the [evaluation record](docs/evaluation.md).
All work and review run in this thread; no OMP or subagents are used.
Reviews are **self-review**, not independent audit.

| Workload | Retained input | Scope |
|---|---|---|
| GoedelWorkbook | 29,750 released source files, Lean4.27 | Candidate files, not a generator arrival trace |
| miniF2F | 244 tasks ×32 candidates, Lean4.9.0-rc1 | Includes rejected, incomplete and operational outcomes |
| ProofNet | 186 tasks ×32 candidates, Lean4.9.0-rc1 | Includes rejected, incomplete and operational outcomes |
| AutoVerus / VeruSAGE | Original source runs and solver traces | SMT results remain separate from Lean results |

RTX5090 is shared through NVIDIA time slicing, without fixed half-card partitions.
Product expansion, exact repair and Lean checking currently run on CPU.
Preparation, packing/transfer, queueing, fallback and retirement belong in the
measured end-to-end cost; warm-server and cold-lifecycle clocks are reported
separately. Native compilation, warm REPLs, caches, snapshots, tries and external
arithmetic oracles are established techniques, not new contributions by themselves.
Tests or reviews do not establish venue acceptance.

## Repository guide

- [Evaluation and completed results](docs/evaluation.md): current evidence and limitations.
- [Experiment implementation](bench/lean-native/linarith-oracle/README.md): build/run entry points and retained dependencies.
- [Reproduction guide](docs/reproduce-checkpoint.md): historical commands, inputs and raw results.
- [Research story](docs/idea-story.md), [design](docs/design.md) and [related work](docs/background-related-work.md).
- [Paper source](docs/paper/main.tex): build with `make -C docs/paper` when `latexmk` is installed.
- `bench/` and `tools/`: experiments and adapters; `artifacts/` and `results/`: retained evidence; `docs/paper/`: manuscript.

The current Workspace also has Tectonic available; see the reproduction guide
for the retained build environment. Historical failures are preserved and
linked rather than removed during repository cleanup.

## Quick start

With Z3 installed:

```bash
python3 bench/synthetic_prefix_bench.py \
  --queries 32 \
  --prefix-constraints 512 \
  --dump-dir traces \
  --json result.json

python3 tools/analyze_smt_trace.py traces \
  --json trace-analysis.json
```

Capture a real interactive Z3 client:

```bash
GPU_SMT_REAL_Z3=/usr/bin/z3 \
GPU_SMT_TRACE_DIR=$PWD/traces \
python3 tools/z3_capture.py -in
```

The intended long-term integration is a drop-in solver shim or launcher, similar in deployment spirit to `ccache`/`sccache`, with a stateful verification-serving runtime underneath.

## Initial serving integration scope

The following constraints describe the initial serving prototype. The expanded
Lean/SMT/GPU scientific scope and native-adapter qualification rules are recorded
in [the current design frontier](docs/design.md); GPU exploration remains required
on RTX 5090, with its usefulness determined by complete measurements.

Original constraints for the first system:

1. stock solver/checker backends;
2. no application source changes for baseline integration;
3. semantic compatibility;
4. low-latency and high-throughput SLOs are both first-class;
5. GPU support is optional and must preserve correctness through validation/fallback.

See:

- [Research plan](docs/research-plan.md)
- [Prior art and differentiation](docs/prior-art.md)
- [Benchmark methodology](bench/README.md)

Lean acceleration thread:

- [Lean acceleration plan](docs/lean-acceleration-plan.md)
- [Lean kernel stage split and checker comparison (2026-10-04)](results/2026-10-04-lean-kernel-stage-split.md)
- [Persistent official Lean replay: fixed-fixture throughput and normal frontend profiles](results/2026-10-04-lean-persistent.md)
- [Retained commands, inputs and raw results](artifacts/lean-2026-10-04/README.md)
- [Real Mathlib proofs and environment reuse](results/2026-10-04-lean-mathlib-state-reuse.md)
- [Executed RTX 5090 expression-DAG primitive](results/2026-10-04-lean-gpu-dag.md)
- [Mathlib/GPU raw evidence](artifacts/lean-state-2026-10-04/README.md)

Real SMT workload continuation:

- [VeruSAGE traces, replay and scope/history regression](results/2026-10-04-verusage-real-traces.md)
- [Pinned sources, traces and per-query decisions](artifacts/verusage-2026-10-04/README.md)
