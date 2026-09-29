# Preliminary experiments — 2026-09-29

This note records the second round of early experiments for VeriServe/gpu-smt.

These are **mechanism probes**, not end-to-end paper results. Their purpose is to test whether live solver state, copy-on-write snapshots, and incremental replay have enough headroom to justify building a serving runtime around unmodified solvers.

## Environment

- stock system libz3: 4.13.3.0
- Linux 6.18 x86-64
- CPU: Intel Xeon Platinum 8573C
- 5 visible CPU cores in the current execution environment
- all semantic checks matched between compared paths

Timing is noisy on this shared environment. The important signals are the mechanism-level differences and crossovers, not the last decimal place.

---

## 1. Reuse hierarchy: cold ASTs vs shared ASTs vs live solver state

We decomposed reuse into three paths over 32 related QF_BV queries:

1. **cold** — create a new Z3 context, term DAG, and solver for every query;
2. **AST reuse** — keep one Z3 context and shared term DAG, but create a fresh solver for each query;
3. **live state** — keep the context, terms, and solver alive, using push/pop for each delta.

The benchmark now records both **end-to-end** timing (including the one-time creation of reusable state) and **warm steady-state** timing. The table below is an end-to-end, single-CPU-pinned run using the median of 5 repetitions.

| Shared prefix constraints | Cold | AST reuse | Live solver | Cold / AST | AST / live | Cold / live |
|---:|---:|---:|---:|---:|---:|---:|
| 16 | 80.77 ms | 23.55 ms | 4.90 ms | 3.43x | 4.81x | 16.50x |
| 64 | 121.75 ms | 48.88 ms | 10.45 ms | 2.49x | 4.68x | 11.65x |
| 256 | 224.29 ms | 126.68 ms | 31.32 ms | 1.77x | 4.05x | 7.16x |
| 1024 | 704.85 ms | 422.10 ms | 118.41 ms | 1.67x | 3.56x | 5.95x |

Warm AST-to-live ratios for the same run were 8.03x, 7.33x, 4.74x, and 3.87x respectively.

Interpretation:

- Reusing only parsed/constructed terms is useful: about 1.7–3.4x end-to-end here.
- Retaining **live solver state** adds another 3.6–4.8x end-to-end beyond AST reuse in this workload.
- The additional steady-state advantage can be larger once reusable state is already resident.
- The relative benefit shrinks as the context becomes larger/more expensive to reason about, so a runtime should still measure the crossover instead of assuming every context is worth retaining.

This experiment is implemented in:

- `bench/reuse_levels_bench.py`

## 2. Fork/COW solver snapshots

The runtime may need to fan out several related requests from one hot context. Exporting Z3 internals is undesirable if the design goal is to leave Z3 unmodified, so we tested a Linux process-snapshot approach.

Both compared paths use the same parallel width:

- **fresh children:** fork workers and rebuild the entire solver context in each child;
- **snapshot children:** build the shared context once in a parent, then fork children that inherit it copy-on-write and add only their query delta.

16 queries, 2 repetitions:

| Prefix | Parallel width | Fresh total | Snapshot total | Speedup |
|---:|---:|---:|---:|---:|
| 64 | 1 | 642.2 ms | 224.4 ms | 2.86x |
| 64 | 2 | 303.6 ms | 115.0 ms | 2.64x |
| 64 | 4 | 209.2 ms | 127.3 ms | 1.64x |
| 256 | 1 | — | — | 2.19x |
| 256 | 2 | — | — | 2.67x |
| 256 | 4 | — | — | 2.09x |
| 1024 | 1 | — | — | 1.86x |
| 1024 | 2 | — | — | 3.14x |
| 1024 | 4 | — | — | 2.06x |

For parallel width 2, median child PSS also fell:

| Prefix | Fresh child PSS | Snapshot child PSS |
|---:|---:|---:|
| 64 | 47.0 MiB | 34.4 MiB |
| 256 | 47.6 MiB | 36.0 MiB |
| 1024 | 48.8 MiB | 38.7 MiB |

This is useful for two reasons.

First, snapshotting is not simply a latency optimization: it can also reduce the physical memory cost of holding many related workers.

Second, the best policy depends on concurrency. At width 4, snapshot gains can shrink because fork/IPC/scheduling overhead becomes a larger part of the request. This is exactly the kind of crossover an SLO-aware scheduler should model.

### Important safety constraint

Python warned when forking from a process that the runtime considered multithreaded. A production implementation must **not** fork arbitrary multithreaded solver processes. The intended design would use a controlled single-threaded forkserver or an equivalent snapshot primitive.

Implemented in:

- `bench/fork_snapshot_bench.py`

---

## 3. Pinned public SMT-LIB workloads

We added a manifest that pins public workloads by upstream repository and commit, plus a fetcher that downloads them without copying third-party benchmark files into this repository.

Current supported sources include Z3 bounded-model-checking loop-unrolling examples and CBMC SMT2 regression workloads.

Files:

- `bench/real_smt_manifest.json`
- `bench/fetch_real_smt.py`
- `bench/smt2_replay_bench.py`

### Fair replay methodology

The replay harness now reports two incremental measurements:

- **incremental E2E:** includes creation of one Z3 context, parsing/replaying the command stream, and solving all checks;
- **incremental warm:** starts after the reusable Z3 context already exists, matching a steady-state serving worker.

The fresh baseline creates/rebuilds a solver context independently for every active `check-sat` snapshot.

We repeated the experiment three times pinned to one CPU. Each run internally reports the median of 20 repetitions.

| Workload | Checks | E2E speedup range | Warm speedup range |
|---|---:|---:|---:|
| Z3 BMC bit-vector loop | 2 | 2.10–2.47x | 3.39–3.95x |
| Z3 BMC integer loop | 2 | 2.11–2.74x | 4.26–5.43x |
| CBMC QF_BV no-division regression | 1 | 0.91–1.42x | 1.18–1.81x |

This corrects an earlier preliminary measurement that compared fresh end-to-end timing against warm-only incremental timing and therefore overstated the speedup. Keeping both numbers is useful, but they answer different questions.

The BMC examples naturally contain two related verification branches and show consistent end-to-end reuse. The CBMC regression contains only one check and can be slightly slower end-to-end despite a faster warm path.

That negative result is important:

> **state reuse is a policy choice, not an unconditional optimization.**

A serving scheduler must account for setup/amortization, query count, context size, queueing delay, and deadline.

## 4. Real branch fan-out with fork/COW

For the two Z3 loop-unrolling BMC examples, we reconstructed the exact context at each check and factored out the longest shared command prefix.

- bit-vector example:
  - 14 shared commands
  - 1-command delta per branch
- integer example:
  - 13 shared commands
  - 1-command delta per branch

We then compared two parallel children:

- each child rebuilding common context + branch delta;
- common context built once, then forked into two branch children.

Across three runs pinned to one CPU, with each run taking the median of 30 repetitions:

| Workload | Snapshot speedup range |
|---|---:|
| Z3 BMC bit-vector loop | 2.40–2.81x |
| Z3 BMC integer loop | 2.26–2.73x |

This is a more realistic form of the snapshot mechanism than the synthetic chain because the shared context and branch deltas come from actual BMC examples.

Implemented generically in:

- `bench/related_snapshot_bench.py`

## 5. Better trace similarity metrics

The first analyzer only measured a longest exact command prefix. That is too conservative for real verification traces because equivalent or highly related contexts can reorder independent declarations/assertions.

The analyzer now reports:

- exact query duplicate fraction;
- exact ordered common-prefix fraction;
- order-insensitive normalized-command multiset overlap;
- byte-weighted context overlap;
- estimated command additions/removals needed to move from a nearby recent context.

A tiny smoke corpus of five query snapshots from the current real examples produced:

- exact duplicates: 0;
- nearest-recent exact-command context overlap:
  - mean about 0.42
  - p50 about 0.21
  - p95 about 0.93
- byte-weighted overlap:
  - mean about 0.41
  - p50 about 0.23
  - p95 about 0.93
- median estimated transition: 2 commands.

This corpus is far too small and heterogeneous for a scientific result. Its only purpose is to validate that prefix-only similarity would miss useful structure.

---

## 6. What these experiments change in the design

The current data supports a **reuse hierarchy** rather than a binary cache/no-cache design:

```text
exact result
   |
live matching solver
   |
nearby live solver context
   |
fork/COW snapshot of popular context
   |
shared AST/context + fresh solver
   |
warm empty solver
   |
cold solver
```

The scheduler should choose among these using at least:

- request deadline;
- queueing delay;
- amount of reusable context;
- expected transition cost;
- context size;
- current parallelism;
- memory pressure;
- predicted solve difficulty.

The results also make GPU less urgent. Before adding a GPU path, the project should first characterize whether real Verus/Dafny/Kani workloads contain enough small related QF_BV/SAT-like work to batch without violating latency SLOs.

---

## 7. Next real benchmark: VeruSAGE-Bench

The repository already contains `bench/run_verus_trace.py`, which uses Verus's solver-path mechanism to insert the capture shim without modifying Verus.

The next experiment is:

1. run 100 mixed VeruSAGE ground-truth tasks;
2. run project-specific slices for NRKernel, ATMO, IronKV, and Anvil;
3. capture every Z3 session;
4. report exact duplicate, prefix reuse, context overlap, query size, Z3 sessions/task, task latency, and arrival-order sensitivity;
5. compare ground-truth verification with repeated AI-generated candidates when candidate traces are available.

This experiment is still pending because the current execution environment has no usable network path to build/fetch Verus, and the repository's GitHub-hosted Actions jobs are currently failing before runner allocation. We should not claim VeruSAGE numbers until the real harness has executed.

Issue tracking this milestone:

- https://github.com/yunwei37/gpu-smt/issues/2

---

## Current conclusion

The preliminary mechanism experiments justify continuing:

- term/AST reuse is measurable;
- live solver state adds substantially more value than AST reuse alone;
- fork/COW can turn a hot context into multiple unmodified-Z3 workers while sharing memory;
- actual BMC command streams show strong reuse;
- isolated one-shot queries show much less benefit.

The remaining high-risk hypothesis is no longer “can solver state reuse ever be fast?” It is:

> **How much reusable context appears across independent jobs in large real verification workloads, and can a transparent scheduler exploit it while meeting latency and throughput SLOs?**

That is the next result needed before treating VeriServe as an OSDI-scale system rather than a promising mechanism prototype.
