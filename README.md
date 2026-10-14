# gpu-smt

A research prototype for **low-latency and high-throughput verification serving**.

The long-term goal is a transparent runtime that accelerates existing formal verification workloads without requiring changes to Z3/cvc5/Lean or to the applications that use them.

The current research hypothesis is:

> Modern verification workloads are increasingly streams of related jobs. A runtime can recover shared contexts across otherwise independent jobs and reuse solver state to improve both tail latency and aggregate throughput.

## Current status

This is an active Lean-first research prototype targeting OSDI-level quality.
The project remains in BOOTSTRAP with four open RQs and an unfrozen scientific
contract. The current paper is [docs/paper/main.tex](docs/paper/main.tex), built
with `make -C docs/paper`. Research iterates directly on `main`; publication
occurs at complete research-step boundaries. See the [evaluation authority](docs/evaluation.md) for the current step,
[research narrative](docs/idea-story.md) and [evaluation frontier](docs/evaluation.md).

The main formal workloads contain all captured ProofNet test candidates
(186 tasks × 32 = 5952 attempts) and miniF2F test candidates
(244 tasks × 32 = 7808 attempts), including rejected, incomplete and operational
outcomes. Statement-only tasks and supporting Mathlib subsets do not replace
complete candidate verification. Lean4.9 and Lean4.21 evidence remain separate.

The latest completed source-native GPU comparison is **native6 on ProofNet**:
all sixteen planned conditions completed, including three primary rotations
against competent warm/snapshot CPU paths and separate resource profiles.
The GPU method is slower than the fastest native CPU path in all three primary
blocks. See [complete clocks, resource observations and scope](docs/evaluation.md#rq4-complete-native6-proofnet-comparison).
Actual device work includes readback and enclosing native verification; this is
not full GPU Lean kernel checking.

The miniF2F acquisition failed in a host OOM before its GPU conditions ran.
The failed/partial inputs, outputs and runtime evidence are preserved.
[MiniF2F status and remaining coverage](docs/evaluation.md#rq4-complete-minif2f-continuation)
distinguish this failure from a performance result. No blind rerun or omitted
candidate turns it into a completed benchmark.

[Complete E030 acquisition](artifacts/lean-parallel-verification-2026-10-12/experiment030/plan.md)
is implemented and run directly by the desktop root. It measures complete native
response extraction after warm preparation; it is a CPU comparison. All8conditions/47616outcomes now finish; the three complete primary pairs
show a descriptive mean1.63percent wall reduction. The [complete review](artifacts/lean-parallel-verification-2026-10-12/experiment030/result-review.md)
retains uncertainty, native response differences and censored profile records.
This supporting CPU optimization does not establish the larger systems claim.

Earlier implementation versions remain historical evidence:
[preparation-retention figures](artifacts/lean-gpu-checking-2026-10-13/experiment021/performance-figures-20261013T1555/README.md),
[native4 GPU figures](artifacts/lean-gpu-checking-2026-10-13/experiment022/figures-proofnet-complete-20261013T2245/README.md),
and [offered-load primary figures](artifacts/lean-service-lifecycle-2026-10-13/experiment023/figures-three-primary-20261013T2359/README.md).
Their complete cells do not imply all promised matrices finished. Native4,
native6 and component-only closure/metadata timings must not be combined into
a hardware-only speedup claim. All original failures and partials remain.

The project uses shared RTX5090 resources, which provide neither a fixed
half-card nor performance isolation. No complete GPU Lean kernel or
end-to-end GPU benefit is established.

The full goal includes strong warm/cache/snapshot CPU competitors, equal-resource
end-to-end latency, throughput and memory, necessary basic correctness and
isolation, useful heterogeneous verification, realistic service traffic, SMT,
source-grounded novelty and a complete paper. Fork/COW, worker pools, caches,
flat arrays and metadata primitives are existing mechanisms rather than novelty
claims. Passing tests or review does not establish OSDI acceptance.

The initial SMT prototype remains available below: streaming Z3 trace capture,
SMT-LIB context analysis and a synthetic cold/incremental benchmark. Retained
real VeruSAGE/AutoVerus traces, native constructor qualification, prior GPU
metadata experiments and recovery records remain linked from the research
frontier and [reproduction guide](docs/reproduce-checkpoint.md).

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
