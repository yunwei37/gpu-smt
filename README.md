# gpu-smt

A research prototype for **low-latency and high-throughput verification serving**.

The long-term goal is a transparent runtime that accelerates existing formal verification workloads without requiring changes to Z3/cvc5/Lean or to the applications that use them.

The current research hypothesis is:

> Modern verification workloads are increasingly streams of related jobs. A runtime can recover shared contexts across otherwise independent jobs and reuse solver state to improve both tail latency and aggregate throughput.

## Current status

Lean-first research prototype on main. All four research questions and the
OSDI-quality systems objective remain open. **Useful GPU acceleration beyond
the strongest measured CPU composition has not been demonstrated.**

The strongest completed native-arithmetic control uses stock Lean omega in
both frontends, with the same two-sided numerical backend, eight candidate
queues, four CPUs and48GiB:

| Complete original1,000-source control | Whole time |
|---|---:|
| Native frontend + omega |454.82s|
| Direct frontend + omega |388.17s|
| Direct frontend without omega |450.99s|

Direct export gives **1.17172×** over this common-omega native path. Each returns
992complete/8reject/0operational with matching verdicts and non-message fields;
warning differences and observer failures are retained. This is one fixed-order
block, not confidence, a globally optimal CPU frontier or a novel solver.
[Source, complete data and limitations](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/native-omega-control/full1000-result-review.md).

The earlier three predeclared native/oracle pairs aggregate **1.50862×** against
their original reference; one pair is below1.5×. That result remains valid at
its declared scope, but must not be called an advantage over the stronger
composition above or an OSDI-level systems contribution.
[All original pairs](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/two-sided-oracle/three-pair-result.json).

An untrusted external arithmetic oracle exports assumptions once, constructs
products and searches for coefficients outside Lean, then returns a certificate
for native checking. Failed hints retain native fallback. The original complete
29,750-source generalization acquisition is running on its frozen earlier build;
it is not a completed comparison against every newer CPU composition.

Current work exposes already-ready proof goals to the numerical batch interface.
Original argument-bearing nonlinear goals now form real groups, with1050problems,
1040native certificate checks and10fallbacks in a15-source qualification.
Whole84.06s sequential/79.77s batch is selected CPU evidence, not a GPU result.
Full immutable requests/replies and actual LP shapes distinguish exported problems
from floating-service work.
[Implementation and real qualification](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/ready-goal-batch/argument-goals/README.md).

RTX5090 executes independently cancellable LP groups using request-sized CUDA
VMM. The last valid additive portfolio retains native hybrid and CPU HiGHS:
38.02s CPU versus39.33s CPU+GPU on64 originals, **3.43%more elapsed**.
[Valid device composition and lifecycle](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-cpu-gpu-portfolio/result-review.md).
The ready-goal additive trial on15 originals gives116.99s native/79.93s CPU/
79.59s CPU+GPU. All56races retainHiGHS; noGPUanswerwins. Actualtwo groups/
three device models retire, including one cross-candidate group, but the0.42%
elapsed difference doesnot establish device benefit or admit a fullmatrix.
The first stale-library attempt is retained separately; the valid trial uses
the default private Cargo build and fresh CPU/reference capture.
[Ready-goal device evidence](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/ready-goal-batch/additive-device/result-review.md).

Current complete phase accounting includes successful and failed oracle calls,
products, proof checks, model shapes and matched source tails. Its fixed-path
zero-cost envelopes do **not** establish a scheduler-independent Amdahl bound.
A losing backend is not proof that all GPU approaches are impossible.
Final continuation uses the better valid CPU/GPU result against its own strong
reference; broad GPU closure requires applicable exclusion evidence.
[Own-clock accounting and gaps](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/current-dual-phase-profile/full1000-result-review.md).

The original7,808-source miniF2F prefix captures are complete:
batch28,673.00s, exact-text41,738.63s and unit-text40,943.77s.
Unit reuse has3711cache lookups, but operational outcomes differ from batch
and complete CPU accounting is censored. These are descriptive elapsed
observations, **not validated speedups**. ProofNet continues in the original
driver. This is the project's SHRED-parser-based native executor, not a full
upstream SHRED/Kimina service comparison.
[Complete prefix outcomes and raw data](artifacts/linarith-oracle-2026-10-17/formal-default/minif2f/unit-result-review.md).

All work and review run in this thread, with no OMP or subagents. Reviews are
**self-review**, not independent audit. Original, failed and partial results,
closed routes, exact protocols and historical clocks remain in
[the evaluation ledger](docs/evaluation.md); the current paper is in
[docs/paper](docs/paper/). No paper acceptance or submission readiness is claimed.

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

A complete known-answer numerical omission control returns actual recorded
coefficients while Lean still checks every proof: fresh native1,228.00s,
native omission866.84s,AST omission767.62s(1.600×),all1,000source verdicts
preserved with zero lookup misses. **This is a diagnostic,not a valid CPU/GPU
speedup.** It does not establish a below1.5× bound for that wave protocol and cannot be transferred to the stronger native-queue reference.
[Raw control and limits](artifacts/linarith-oracle-2026-10-17/gpu-stage/pooled-wall-profile/fixed-certificate-control/full1000-result-review.md).

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
