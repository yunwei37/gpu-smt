# Research plan: verification serving runtime

## Thesis

Modern verification workloads are increasingly **streams of related verification jobs**, not isolated hard formulas. CI, interactive verification, and AI-generated proof/program candidates repeatedly solve queries that share declarations, axioms, program semantics, and path conditions.

This project asks:

> Can a transparent systems runtime recover and reuse verification state across otherwise independent jobs, while jointly optimizing low latency and high throughput?

The intended system is not a new SMT solver. It sits around existing solvers/checkers and treats verification state as a reusable systems resource.

## Hard design constraints

1. **Unmodified backends first.** Stock Z3/cvc5/Bitwuzla/Lean should remain usable without maintaining a fork.
2. **Application-transparent baseline.** Existing applications should work by changing a solver path, PATH entry, or launcher; source changes are optional.
3. **Semantic fidelity.** For the supported interface, the runtime must preserve SAT/UNSAT/UNKNOWN and requested artifacts such as models, proofs, and unsat cores. Unsafe accelerators may only provide hints or validated certificates.
4. **Both latency and throughput are first-class.** Interactive verification and request-path policy checks care about p95/p99 latency; CI and agent workloads care about makespan, queries/s, and cost.
5. **GPU is optional.** The CPU-only runtime must be useful. GPU support should improve part of the latency-throughput Pareto frontier rather than define correctness.
6. **No benchmark-only APIs.** The same compatibility path used in experiments should be usable by real Verus/Dafny/Viper/Kani/etc. workflows.

## Research questions

### RQ1: Do real workloads contain exploitable cross-job structure?

Measure:

- exact query duplicates;
- shared declaration/axiom prefixes;
- nearest-recent-context similarity;
- query-size distribution;
- inter-arrival time;
- solver runtime and tail behavior;
- fraction of work spent in parsing, preprocessing, solving, and process startup where measurable.

The project should be abandoned or reframed if large real workloads show little reusable structure.

### RQ2: How much can an external runtime reuse without modifying the solver?

Candidate hierarchy:

- L0: exact result cache;
- L1: hot solver session already at the desired context;
- L2: nearest prefix context plus a small delta;
- L3: warm solver process;
- L4: cold solver process.

Possible mechanisms:

- canonicalized content-addressed contexts;
- incremental SMT push/pop;
- worker affinity;
- process snapshots/fork with copy-on-write;
- persistent caches across CI runs;
- backend portfolio routing.

A key comparison is **reuse vs fresh solving**: incremental state is not always faster because it can inhibit global preprocessing.

### RQ3: How should the runtime jointly optimize latency and throughput?

Model a request with at least:

- deadline/SLO class;
- priority;
- requested result artifact;
- backend compatibility requirements.

A scheduler should estimate:

[
T(w,q) = Q_w + T_{transition}(w,q) + T_{solve}(w,q)
]

and choose between a state-affine worker, a fresh worker, a hedge/portfolio execution, or a batch.

### RQ4: When is GPU execution useful?

Do not start by porting Z3 to CUDA.

Initial GPU candidates:

- many independent small QF_BV/SAT-like queries;
- batched bit-blasting;
- batched simplification/preprocessing;
- hashing/deduplication;
- model validation;
- proof/certificate checking.

The main GPU hypothesis is **inter-query parallelism over many related small jobs**, which differs from prior work that accelerates phases within one SAT instance.

### RQ5: Can the runtime remain a drop-in open-source tool?

Target UX:

```bash
veriserve run -- verus ...
veriserve run -- dafny verify ...
veriserve run -- kani ...
```

or a solver shim:

```bash
REAL_Z3=/usr/bin/z3 GPU_SMT_TRACE_DIR=traces ./tools/z3_capture.py -in
```

Longer term, a user should be able to install one daemon/shim and get useful metrics and acceleration without understanding SMT internals.

## Proposed architecture

```text
Existing applications
Verus / Dafny / Viper / Kani / custom SMT clients
                    |
             compatibility shim
                    |
                    v
          content-addressed context DAG
          /          |             \
 exact results   hot contexts    trace/profile DB
          \          |             /
                    v
              SLO-aware scheduler
             /        |          \
       warm CPU   batched/GPU   hedge/portfolio
       workers      workers       workers
             \        |          /
                    v
          stock Z3 / cvc5 / Bitwuzla
```

## SLO classes

### Interactive

Examples: IDE verification, compiler feedback, policy checks, eBPF load/admission checks.

Primary metrics:

- p50/p95/p99 latency;
- deadline miss rate;
- cold vs warm latency.

Policy:

- no intentional batching delay for tight deadlines;
- prefer exact cache and state-affine warm workers;
- optionally hedge tail queries.

### Batch / CI

Primary metrics:

- total makespan;
- queries/s;
- CPU-hours and GPU-hours;
- energy/cost where available.

Policy:

- allow queueing and micro-batching;
- maximize reuse across jobs/commits;
- prefer throughput-efficient routing.

### Agent / proof search

An agent may generate many candidates but only need one valid result.

Primary metrics:

- time-to-first-valid;
- candidates verified/s;
- wasted work after a valid candidate exists;
- cancellation latency.

Policy:

- speculative parallel verification;
- early cancellation;
- optional priority from model confidence or predicted verification cost.

## Benchmark plan

### 0. Synthetic prefix workload

Purpose: validate instrumentation and quantify the upper bound of state reuse.

Run the same QF_BV queries as:

1. a fresh Z3 process per query;
2. one incremental Z3 process with a common prefix and per-query deltas.

This is a smoke test, not paper evidence.

### 1. Verus / VeruSAGE-Bench

Primary candidate for the first real workload study.

VeruSAGE-Bench contains 849 repository-level Verus tasks from real systems projects: Anvil, IronKV, a memory allocator, Node Replication, NRKernel, ATMO, storage, and Vest.

Why it matters:

- real systems verification;
- a natural AI-agent workload;
- many proof candidates can share nearly identical program/specification context.

Collect the SMT traces emitted by Verus and measure cross-task/cross-candidate reuse.

### 2. Dafny / Boogie

Needed both as a workload and as a comparison against prior fine-grained caching. Measure whether an external solver-state runtime adds value beyond program-level invalidation/caching.

### 3. Viper ecosystem

ViperServer is an important baseline because it already keeps verifier infrastructure warm and exposes a server interface. Workloads may include Viper, Gobra, and Prusti.

### 4. Kani / CBMC

Covers bounded model checking and SAT/SMT workloads from Rust systems software.

### 5. Lean / Mathlib

Later-stage backend to test whether the runtime abstraction generalizes beyond SMT. Lean-specific internal optimizations are explicitly out of scope for the first system.

### 6. SMT-COMP as a control

Random/unrelated SMT-COMP instances are expected to have little cross-job reuse. This is a useful negative control rather than the primary workload.

## Metrics

Always report both latency and throughput:

- p50, p95, p99 latency;
- deadline miss rate;
- queries/s;
- total wall time;
- CPU-seconds/query;
- GPU-seconds/query;
- memory footprint;
- exact-cache hit rate;
- nearest-prefix reuse fraction;
- context transition cost;
- percentage of requests routed to each execution path.

For agent workloads additionally report time-to-first-valid.

## First implementation milestones

### M0: instrumentation and workload characterization

- transparent Z3 capture shim;
- SMT trace parser;
- exact-duplicate and nearest-prefix analysis;
- synthetic cold-vs-incremental benchmark;
- CI smoke tests.

Success criterion: reproduce traces reliably and establish whether real workloads have substantial reusable structure.

### M1: CPU-only runtime

- persistent worker pool;
- exact result cache;
- context DAG;
- state-affinity scheduling;
- incremental push/pop reuse;
- reuse-vs-fresh cost model.

### M2: process snapshotting and tail control

- fork/COW snapshots for popular contexts;
- deadline-aware scheduling;
- hedged/portfolio requests;
- cross-run persistent state metadata.

### M3: heterogeneous execution

Only after traces identify a sufficiently large GPU-friendly query class:

- batch classifier;
- GPU prototype for that class;
- CPU validation/fallback;
- adaptive batching under deadlines.

## Falsification criteria

The project should not claim a general serving advantage unless real traces show it.

Potential negative results:

- low cross-job context similarity;
- incremental reuse slower than fresh solving for important workloads;
- scheduling overhead dominates sub-millisecond queries;
- GPU crossover requires unrealistically large batches;
- solver shims break required interactive/proof/model interfaces.

Any of these should narrow or change the project before a large implementation effort.

## Paper shape

A strong systems paper would need four contributions:

1. **Workload characterization:** modern verification traffic is dominated by repeated/related jobs and has distinct interactive, CI, and agent SLOs.
2. **Verification context as a systems abstraction:** a content-addressed DAG of reusable solver state across process/job boundaries.
3. **State-aware SLO scheduling:** jointly reason about queueing delay, context-transition cost, solver runtime, and optional hedging/batching.
4. **Transparent deployment:** meaningful gains on unmodified solvers and real applications.

The target is not “GPU makes SMT faster.” The target is a better latency-throughput frontier for real verification workloads.

## Prior art to compare directly

See `docs/prior-art.md`.

Key systems include Mallob, Boogie fine-grained verification caching, ViperServer, KLEE/Green-style query caching, ParaFROST, and production portfolio solving such as AWS Zelkova.
