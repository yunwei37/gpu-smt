# gpu-smt

A research prototype for **low-latency and high-throughput verification serving**.

The long-term goal is a transparent runtime that accelerates existing formal verification workloads without requiring changes to Z3/cvc5/Lean or to the applications that use them.

The current research hypothesis is:

> Modern verification workloads are increasingly streams of related jobs. A runtime can recover shared contexts across otherwise independent jobs and reuse solver state to improve both tail latency and aggregate throughput.

## Current status

Lean-first research prototype; all four RQs and the OSDI-quality systems goal
remain open. There is **no demonstrated end-to-end GPU verification speedup**.
The native CPU branch-runtime and scalar GPU constructor routes are closed;
their complete, failed and partial results remain in the
[evaluation record](docs/evaluation.md). Research runs directly on `main`.

The completed primary arithmetic comparison follows the [bounded linarith/nlinarith oracle protocol](artifacts/linarith-oracle-2026-10-17/plan.md):
1,000 arithmetic-heavy original GoedelWorkbook candidates, native stage-cost
measurement, external untrusted polynomial/product/LP search, and one native
coefficient-certificate check with fallback. Success requires **more than 1.5×
end-to-end improvement over the fastest valid native baseline**, with matching
verification outcomes. The final decision uses the better of CPU and GPU oracle; GPU evaluation must
finish before negative closure or stopping the hourly task. Preflight values are not full results.

Three complete matched observations on the frozen1,000 sources give
**1.34668×** in aggregate (**25.74%** less elapsed time), below the predeclared
**more-than1.5×** continuation rule. Every cell returns992complete/8rejected,
zerooperational, with matching source verdicts and the same88unused-variable
warning differences. **CPU stage: 1.34668×; GPU stage: in progress.**
These historical CPU pairs inherited unbounded address space. Current captures
use 48 GiB and keep their clocks separate. Header inspection also found stacked
old/new arithmetic elaborators in the GPU integration; a correction passes real
24-source CPU qualification. Three alternating full CPU pairs now measure the
corrected headers under 48 GiB; the corrected GPU preflight runs separately.
The hourly research automation is active; this CPU result is not project closure.
[Decision, raw data and limits](artifacts/linarith-oracle-2026-10-17/decision-20261017.md)
retain every pair and the post-fault rebuild lineage. Both full1,000-source
[phase diagnostics](artifacts/linarith-oracle-2026-10-17/native-stages/oracle-result-review.md)
are complete, with native responses matching their primary captures.
The first full GPU variant attempts all1,000sources in3,374.15seconds, with984complete/8rejected/8operational; it has no successful parity or acceleration result. [Complete raw GPU record](artifacts/linarith-oracle-2026-10-17/gpu-stage/full1000-phase1/result-review.md). The same-plan native control completes in 2,331.39 seconds and the robust CPU support control in 2,363.00 seconds. These observations retain the old stacked headers. A direct-feasibility GPU repair failed real numeric qualification and remains closed. The corrected-family GPU preflight and original-population prefix timing are in progress.

A supporting experiment measures shared proof prefixes on all 7,808 miniF2F
and 5,952 ProofNet candidates using SHRED's official Lean parser, followed by
actual native execution comparisons. Prefix counts alone are not time savings.
All implementation, execution, analysis, writing and self-review are performed
in the owning thread; no OMP or subagents are used. Self-review is not an
independent audit.

| Workload | Retained input | Scope |
|---|---|---|
| GoedelWorkbook | 29,750 released source files, Lean 4.27 | Released candidate files, not a generator arrival trace |
| miniF2F | 244 tasks × 32 candidates, Lean 4.9.0-rc1 | Includes rejected, incomplete and operational outcomes |
| ProofNet | 186 tasks × 32 candidates, Lean 4.9.0-rc1 | Includes rejected, incomplete and operational outcomes |
| AutoVerus / VeruSAGE | Original source runs and solver traces | SMT results remain separate from Lean results |

RTX 5090 is shared through NVIDIA time slicing; it is not partitioned into
fixed half-cards. The arithmetic prototype has CPU and experimental GPU LP-support paths.
Product expansion, exact repair and Lean checking currently run on CPU.
Measured whole costs include preparation, pack/transfer/queueing, fallback
and retirement; a warm upstream GPU server has separately reported cold costs. Native compilation, warm REPLs, caches, snapshots, tries and external
arithmetic oracles are established techniques, not new contributions by
themselves. Tests or reviews do not establish venue acceptance.

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
