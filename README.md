# gpu-smt

A Rust verification-engine prototype with a native Lean REPL backend and
verifier-neutral extension traits. Lean and SMT remain the research scope.
Lean has priority; RTX 5090 is the only GPU target.

The broader hypothesis is that related verification jobs can share expensive
prepared state while preserving native behavior and independent candidate
execution. [The initial narrative and four research questions](docs/idea-story.md)
remain intact. The OSDI-quality systems contribution and all four final RQ
answers are still open.

## Engine quick start

The Rust workspace separates public contracts, resource/workload scheduling,
native backends and HTTP adapters. Existing raw research data stays outside
the core. This is an experimental 0.1 engine, not a production-ready service
or a demonstrated speedup.

    cargo build -p gpu-smt-server
    cargo run -p gpu-smt-server --bin gpu-smt -- --help
    cargo test --workspace --all-targets

Supply an existing pinned Lean REPL and its project environment. From that
Lean project, use Lake's discovered import paths:

    lake env /absolute/path/to/gpu-smt/target/debug/gpu-smt check \
      --repl /absolute/path/to/repl --project /absolute/path/to/lean-project \
      --environment your-immutable-toolchain-project-pin \
      --cpus 8,9,10,11 --worker-cores 1 --memory-gib 48 \
      < /absolute/path/to/gpu-smt/examples/check.jsonl

Use serve for local Kimina core/check, legacy/verify and typed/v1/verify.
The optional typed/v1/verify/stream route sends NDJSON results as they complete,
with a final count marker; existing collected routes retain their order/schema.
[Streaming and disconnect semantics](docs/api.md#http) distinguish checked
first-success cancellation from every-candidate RL delivery.
Unsupported debug/infotree extensions return explicit errors. Native env
fields are output provenance, not persistent remote session handles.

For original code-verification source, --lean /absolute/pinned-sdk/bin/lean
selects the stock JSON stdin frontend through the same resource engine. Its
[output and source-path scope](docs/api.md#stock-source-frontend) are distinct
from REPL JSON; no whole-workload speedup follows from backend availability.

| Crate | Responsibility |
|---|---|
|gpu-smt-core|Requests, verdicts, attempt provenance and extension traits|
|gpu-smt-engine|Joint admission, global queue, watchdog, exclusive retries, exact deduplication, consumer modes|
|gpu-smt-lean|Original native REPL JSON transport and process retirement|
|gpu-smt-server|Embeddable HTTP adapter and JSONL/HTTP executable|

The composable task-interleave policy orders first-success work across task
groups while retaining wrapped source ranking and memory forecasts. It is an
ordinary scheduling component; workload-layer novelty and whole-flow benefit
remain research questions.
The optional --policy task-memory keeps FIFO order while learning RSS
reservations from completed same-task attempts. It shares no proof outcome;
[matched measurement and limits](docs/benchmarking.md#measured-same-task-memory-policy)
separate native control qualification from still-pending throughput evidence.

RL mode returns every candidate outcome. First-success mode cancels siblings
only after checked same-task acceptance. Exact completed/in-flight reuse
retains each caller's identity; cancellation and resource failures are not
native rejections or cacheable proof results.

The [standalone tactic-failure cache skeleton](docs/api.md#standalone-tactic-failure-replay-skeleton)
is an optional library development component. A backend owns replay-qualified
inputs and complete ordinary-failure transitions; fixtures and a simulated
example exercise its contract. It is not enabled in engine verification and
has no stock Lean replay adapter or measured workload benefit.

[Architecture](docs/architecture.md) · [API and compatibility scope](docs/api.md) ·
[Examples](examples/README.md) · [Paired measurement](docs/benchmarking.md) · [Contributing and checks](CONTRIBUTING.md) ·
[CI](.github/workflows/engine.yml) · [Apache-2.0 engine license](LICENSE).

An [optional native import parent](native/lean/README.md) passes the pinned Lean4.18
native differential/lifecycle CI; the default backend remains fresh-process.
[Actual Mathlib import-only preparation](artifacts/mathlib-import-preparation-2026-10-25/README.md)
loads5,545modules and retires normally; no candidate child executes in that setup.
A complete matched four-warm comparison is retained below. Native failure
detectors, source-aware cost models and multi-node execution remain
implementation/research work.
Resource mechanisms are prior techniques; novelty must come from workload
methods and actual end-to-end results.

## Resource and verification contracts

The current research resource point uses **48 GiB total sampled owned RSS** on
CPUs 8–11, up to four one-core workers, and no fixed per-process address-space
cap. Admission uses actual memory plus measured forecasts. The one-second
watchdog interrupts owned native groups independently of request execution;
retirement remains awaited and charged. Sampling can overshoot: this is **not
a kernel hard memory quota**.

Preempted work follows the already queued ordinary frontier, then retries alone
after peers retire. Later arrivals cannot starve that retry. Observed peaks are
forecasts, not safe memory caps; moving retries to the tail does not parallelize
the tail itself. [Resource implementation](docs/implementation.md#resource-contract)
and [measurement protocol](docs/benchmarking.md) document the boundaries.

## Research status and retained results

**No useful extra end-to-end GPU acceleration over the strongest measured CPU
composition has been demonstrated.** One complete resource-path comparison takes19.28%less elapsed time than the
matched four-worker warm service;different retry ordering and CPUeligibility
remain,so this is not an isolated COWor general service-superiority result. Source tests
and selected-cohort results do not establish whole-population speedup, novelty,
or unchanged accepted sets.

| Evidence | Result and scope |
|---|---|
| [Matched warm-resource comparison](bench/lean-warm-resource/README.md) | The complete7,808-source pair returns identical final statuses and3,014accepted IDs;engine20,323.01s versus four-warm25,176.49s. Retry-order/CPUeligibility differences,23secondary-view diagnostic differences and sampled RSSovershoot remain. [Complete result](artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z/result-review.md). |
| [Own-engine fresh/prepared pair](artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z/README.md) | 1.24028× compares two own-engine components. It does **not** establish a gain over the strongest warm baseline; baseline compilation, resource-point and status differences remain. |
| [Full GPU counterexample pair](artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md) | At the historical two-worker/24GiB-AS point, all 7,808 statuses agree; GPU takes 8.86% longer before 23.99s input preparation. Screening does not reduce timeouts. |
| [Failure hotspot profile and prototypes](docs/evaluation.md#failure-and-scheduling) | interval_cases and simp_all dominate observed timeout thread CPU. These are not total wall fractions or proven early-failure certificates; the 48-source interval prototype has 0/48 reliable early-failure coverage. |
| [First-success scheduling matrix](artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/full-result-review.md) | All three 7,808-source conditions complete and preserve 142 solved tasks. First-success cancellation serves pass@k/best-of-n, not every-candidate RL rewards or a novelty claim. |
| [Measured sibling-memory development pair](artifacts/engine-resource-profile-2026-10-25/task-memory32-20261027T193536Z/result-review.md) | A selected 32-source pair reduces elapsed time 23.40% with equal outcomes. It is not a full-population result. Further policy measurement is deferred behind resource parity. |
| [Lean code-verification workload](bench/lean-code-verification/README.md) | Original Verina and lean-mlir characterization is retained. The own closed-CNF whole-module prototype is slower than native; it is not enabled by default. |

The external CPU oracle remains **frozen as a baseline**: no optimization,
extension, new oracle experiments or contribution claim. All original, failed
and partial results remain in [the evaluation index](docs/evaluation.md),
including Goedel, ProofNet, earlier GPU/CPU compositions, prefix integrations,
resource failures and baseline limitations. Earlier resource captures retain a
historically accepted candidate becoming a timeout; accepted-set equivalence is
not established by their component ratio. Historical resource points are not
pooled with the current point. A corrected fixed 42-source solo replay remains separate
from its earlier 41-budget-failure/1-timeout result, which did not explicitly
select the now-matched native Mathlib library.

Four directions continue: the layered engine, reliable failure/timeout
determination, same-task scheduling, and public Lean code-verification workloads.
The priority is resource-layer parity with the installed warm baseline before
enabling additional workload methods. Warmup, snapshots, caches, native
compilation and external certificate oracles are prior techniques; workload-layer
novelty remains an open research requirement.

[Exact-duplicate analysis](artifacts/engine-resource-profile-2026-10-25/exact-duplicates/result-review.md)
found no duplicate substantive miniF2F proofs. The
[heldout source-cost analysis](artifacts/candidate-scheduling-2026-10-25/source-cost-crossfit-20261026/README.md)
did not improve frozen first-success work over FIFO. These limitations remain
part of the evidence, rather than reasons to assume a scheduling gain.

## Workloads and reproduction

| Workload | Retained input | Native environment |
|---|---|---|
| GoedelWorkbook |29,750 released original source files|Lean 4.27|
| miniF2F |244 tasks × 32 candidates =7,808|Lean 4.9.0-rc1|
| ProofNet |186 tasks × 32 candidates =5,952|Lean 4.9.0-rc1|
| AutoVerus / VeruSAGE |Original source runs and solver traces|Version-aligned native SMT execution|

Released candidates are replay workloads, not generator arrival traces.
[Benchmark methodology](bench/README.md), the
[retained-environment reproduction guide](docs/reproduce-checkpoint.md), and
each result's manifest identify actual SDKs, native libraries, clocks and
resource points. Historical Workspace paths are not a universal installer.

- [Matched native/warm resource comparison](bench/lean-warm-resource/README.md).
- [First-success candidate scheduling](bench/lean-candidate-scheduling/README.md).
- [Public Lean code-verification profiling](bench/lean-code-verification/README.md).
- [Counterexample component](bench/lean-counterexample/README.md).
- [Frozen arithmetic baseline and historical commands](bench/lean-native/linarith-oracle/README.md).
- [Real SMT replay and limitations](results/2026-10-04-verusage-real-traces.md).

## Repository and paper

- crates/: reusable Rust engine; [architecture and extension points](docs/architecture.md).
- native/: optional pinned Lean+C import-parent adapter.
- bench/, tools/: experiments and retained adapters.
- artifacts/, results/: source snapshots, raw data, failures and self-reviews.
- [Implementation status](docs/implementation.md), [evaluation](docs/evaluation.md),
  [research narrative and four RQs](docs/idea-story.md), [related work](docs/background-related-work.md).
- [Paper source](docs/paper/main.tex) and [compiled draft](docs/paper/main.pdf).

The paper is a research draft, not submission-ready or accepted. All current
implementation, experiments and reviews run in this thread. Reviews are
**self-review**, not independent audit; tests and a compiled paper do not
establish venue acceptance.

The detailed previous README is preserved [byte-for-byte](docs/tmp/build-and-evaluate/step-0114-20261028T181730+0000/readme-before.md.gz).
Its relative links use the original repository-root context; the
[original rendered revision](https://github.com/yunwei37/gpu-smt/blob/5e5e3e50ad4b2390e591ad2a7d88f851c53f4847/README.md)
retains that link context. No result or source data was deleted.
