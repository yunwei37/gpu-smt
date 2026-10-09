# gpu-smt

A research prototype for **low-latency and high-throughput verification serving**.

The long-term goal is a transparent runtime that accelerates existing formal verification workloads without requiring changes to Z3/cvc5/Lean or to the applications that use them.

The current research hypothesis is:

> Modern verification workloads are increasingly streams of related jobs. A runtime can recover shared contexts across otherwise independent jobs and reuse solver state to improve both tail latency and aggregate throughput.

## Current status

The user expanded this project on 2026-10-07 into a complete autonomous research
and paper effort targeting OSDI-level quality. The sole current paper is
[docs/paper/main.tex](docs/paper/main.tex), built with `make -C docs/paper`.
The project is in BOOTSTRAP: its four RQs remain unanswered by final evidence
and its scientific contract is not frozen. The existing outer hourly heartbeat
resumes the same owning session; no second scheduler or Workspace is created.
See [the research frontier](docs/idea-story.md) and
[step 0003](docs/tmp/bootstrap/step-0003-20261009T132427+0000/step-report.md).
Legacy `paper/` sources and the completed initial checkpoint remain preserved.

Milestone M0 is implemented on the `research/verification-serving` branch:

- research plan and prior-art map;
- streaming Z3 trace capture shim;
- SMT-LIB trace/context analyzer;
- synthetic cold-vs-incremental Z3 benchmark;
- CI smoke tests with stock Z3.

The current branch has real VeruSAGE traces, complete Mathlib proof/state-reuse
measurements, and an executed RTX 5090 expression-DAG primitive. The VeruSAGE
prefix pool changes `unsat`/`unknown` outcomes; it is a negative fidelity result,
not a serving speedup. Mathlib replay uses the established community REPL. The
GPU result covers metadata computation, not full proof checking. The new
[complete native branching discriminator](artifacts/native-branch-2026-10-07/README.md)
rejects its library adapter against the original executable on five other
query outcomes, even though all earlier31 pooling differences recover.

The new [normal-check Mathlib profile](artifacts/lean-module-profile-2026-10-08/README.md)
completes six full source modules, paired profiled/unprofiled paths and three
repetitions. It locates costly frontend/meta work at that boundary; profiler
category shares are not CPU fractions or a GPU speedup ceiling. The approved
real generated-candidate experiment still awaits the finite RTX 5090 Job;
no generated output or runtime result is yet recorded.

The [native constructor comparison](artifacts/native-frontend-2026-10-09/README.md)
completes 156 original streams, four conditions and three repetitions. The lazy
command frontend matches the same-source stock CLI's non-statistical responses;
early manager creation changes six checks and requested responses in every pass.
Release version metadata still differs explicitly. This is local causal evidence
for interface construction, without a branching-safety or acceleration claim.
Raw native outcomes and failed model readouts remain reproducible.

The initial investigation/workspace/GPU-benchmark request is complete, including
the temporary RTX 5090 Job cleanup receipt. Full GPU Lean checking and a novel
production SMT runtime remain undemonstrated. [Reproduction after container
recovery](docs/reproduce-checkpoint.md) documents surviving inputs and rebuilding
lost temporary dependencies, with an evidence-grounded next research direction.

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
