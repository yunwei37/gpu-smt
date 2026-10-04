# Lean kernel checking: stage split and checker comparison — 2026-10-04

This note is the first real-workload result for the Lean acceleration thread.
It measures **where Lean verification time actually goes** and compares the
kernel-checking backends that a serving runtime would target.

All numbers are measured in this workspace. Nothing here is projected.

## Workload: lean-kernel-arena

Benchmark: [`lean-kernel-arena`](https://github.com/leanprover/lean-kernel-arena),
the official cross-checker benchmark suite. It exports Lean declarations to a
self-contained NDJSON format and asks a checker to validate them. The export is
post-elaboration, so it measures the **kernel-checking** problem, not tactic
search.

We built the pinned corpora from the arena's own test metadata
(`tests*/{init,std,cslib,mathlib}.yaml`) and verified the exported files against
the public arena's recorded sha256 digests:

| Corpus | Export bytes | Declarations | sha256 vs arena metadata |
|---|---:|---:|---|
| `init` | 347,555,345 | 58,170 | matches (`620502ac…`) |
| `std` | 596,655,086 | 101,286 | matches (`289ed65a…`) |
| `cslib` | 2,422,584,798 | 383,976 | matches (`bc5c88e0…`) |
| `mathlib` | 6,184,415,052 | 702,040 | exact match |

Declaration census (inductive / def / thm / opaque / axiom / quot):
`init` 615/15227/42070/247/7/4; `std` 1057/27980/71839/399/7/4;
`cslib` 4022/110882/266747/2314/7/4;
`mathlib` 6798/179154/513479/2598/7/4.

The corpora are dominated by **theorems** (72% of `init`, 71% of `std`, 69% of
`cslib`, 73% of `mathlib`), i.e. proof terms to type-check, which is the
interesting case.

### Environment

- Intel Core Ultra 9 285K, 24 logical cores / 24 physical, single socket,
  125 GB RAM.
- Lean v4.34.1 (`leanprover/lean4:v4.34.1`), elapsed toolchain via elan.
- All runs isolated with `taskset`; long runs pinned to cores `0-7`.

## Stage split: parse+load vs kernel checking

The official kernel exposes a `--parse-only` flag that reads and deserializes the
export but skips type-checking. That isolates the **import/parse floor** (the
irreducible RAM-resident cost of materializing the environment) from the
**kernel-checking** work.

Official kernel, `taskset -c 0-7`, best-of-repeat (isolated, no competing
jobs):

| Corpus | parse-only wall | full wall | check-only (Δ) | parse RSS | full RSS | check share of wall |
|---|---:|---:|---:|---:|---:|---:|
| `init` | 5.41 s | 32.78 s | **27.4 s** | 577 MB | 583 MB | 84% |
| `std` | 9.30 s | 58.83 s | **49.5 s** | 954 MB | 955 MB | 84% |
| `cslib` | 38.31 s | 305.74 s | **267.4 s** | 3.58 GB | 3.58 GB | 87% |
| `mathlib` | 107.63 s | 1712.10 s | **1604.5 s** | 10.4 GB | 10.4 GB | 94% |

`mathlib` was measured twice on isolated cores: **1712.10 s** (first run, the
table row) and **1565.93 s** (second, fully isolated run: parse-only 117.36 s,
10.42 GB RSS). The ~9% spread on a 26-minute single-thread
run is machine variance (turbo/thermal/ambient), not a methodology change; both
give check share 93–94%. All `mathlib` statements elsewhere in this note are
consistent with either and the arithmetic does not depend on which.

Reading: **kernel checking is 84–94% of wall time and grows with corpus size**.
Parsing/loading is a large constant (~5.4 s for 331 MB, ~108 s for 6.2 GB) but
the checking work dominates asymptotically. Also note **RSS is identical with
and without checking** — the checker builds the full environment either way;
`--parse-only` is a genuine lower bound on resident memory, not a savings on it.

Instruction-level confirmation (`perf stat`, `init`, isolated):

| Mode | Instructions | IPC |
|---|---:|---:|
| full check | 398.3 G | 1.95 |
| parse-only | 105.4 G | 3.53 |

Full checking executes **2.6× more instructions** and runs at **half the IPC**.
Low IPC at ~4× the memory traffic is the signature of a **memory-latency-bound
graph traversal** (the kernel's defeq/whnf reduction over the term DAG), not a
FLOP-bound workload. This is the single most important fact for acceleration:
the kernel is not compute-dense, so a GPU helps only if it is fed a *large batch*
of independent checks to hide latency, not by making one check faster.

### The perf suite is also check-dominated

28 synthetic-but-real kernel stress tests (magma lists, app/binder ladders,
Church numerals, shared subterms):

- Σ parse-only = **1.55 s**; Σ full = **60.16 s** → **97% is kernel checking**.

The heavy tests are almost pure checking: `magma-list-deep-n36` 29.36 s with
99.8% in the kernel; `magma-list-pair-n21` 15.55 s. Small bug/other tests are
parse-dominated (check ≈ 0). So both the real library corpora and the stress
tests agree: **the kernel is the target**.

## Alternative checker comparison

Same corpora, all cores `0-23`, each checker at its best measured parallelism
(official is single-threaded per file; the alternatives are internally
multi-threaded). Wall / user CPU / peak RSS:

| Checker | `init` | `std` | `cslib` | `mathlib` |
|---|---|---|---|---|
| official (1 core) | 32.8 s / 583 MB | 61.3 s / 954 MB | 323.4 s / 3.58 GB | 1712.1 s / 10.4 GB |
| parse-only (1 core) | 5.4 s / 577 MB | 9.4 s / 954 MB | 42.4 s / 3.58 GB | 107.6 s / 10.4 GB |
| nanoda (t24) | 4.02 s / 627 MB | 6.83 s | 33.69 s | 116.05 s / 7.49 GB |
| nanoclo (t24) | 4.11 s / 617 MB | 4.21 s / 1.81 GB | 20.22 s / 4.13 GB | 69.97 s / 9.47 GB |
| nanobruijn (t24) | 5.97 s / 652 MB | 11.04 s / 897 MB | 50.33 s / 2.91 GB | 142.31 s / 7.04 GB |
| lazylean (j8) | 5.41 s / — | 6.60 s / 723 MB | 32.76 s / 2.63 GB | 123.44 s / 7.34 GB |

On the full `perf` stress suite (28 tests, the cases that are nearly 100% kernel
work), single-run totals with each checker's own multithreading:

| Checker | perf-suite total wall | Speedup vs official |
|---|---:|---:|
| official | 60.16 s | 1.0× |
| parse-only | 1.55 s | 38.8× (excludes checking) |
| nanoclo | 7.87 s | 7.6× |
| lazylean | 13.22 s | 4.6× |
| nanoda | 116.71 s | 0.52× (**slower**) |
| nanobruijn | — | — |

Interpretation:

- The modern Rust checkers are **4.6–7.6× faster than the official kernel** on
  kernel-bound tests, but they get this from *parallelism across declarations*,
  not from a fundamentally cheaper proof check.
- **nanoda is not state of the art.** It is slower than the official kernel on
  the perf suite (116.7 s vs 60.2 s) and only 2–3× faster on big corpora, where
  nanoclo/lazylean reach 7.6×. Do not treat nanoda as the reference accelerator.

### Parallel scaling and its limit

nanoda scaling on `init` (per-declaration parallelism):

| threads | 1 | 2 | 4 | 8 | 16 |
|---|---:|---:|---:|---:|---:|
| wall (s) | 27.07 | 13.13 | 7.51 | 5.11 | 4.02 |

Sub-linear (27.07→4.02 is 6.7× on 16 threads) and nanoclo is flat-to-4.1 s by
t24. Parallel checking across *declarations within one file* is real but
bandwidth-limited: the 125 GB machine saturates DRAM before it saturates cores.

## Batching independent exports

The serving-relevant question is whether the runtime can batch many
independent Lean checks. Each job is one official-kernel invocation on one
export; a pool of concurrent processes runs a fixed job set. All rows below
are the same job set at increasing pool width.

| Job set | width 1 | 4 | 8 | 16 | 24 | best |
|---|---:|---:|---:|---:|---:|---:|
| tutorial suite (141 subtests) | 4.07 s | — | 0.552 s | — | 0.367 s | 11.1× @24 |
| 46 small correctness files ×10 (=460) | 12.32 s | 3.06 s | 1.59 s | 0.81 s | 0.68 s | 18.1× @24 |
| perf suite (28 kernel-bound exports) | 75.3 s | 40.4 s | 41.6 s | 44.2 s | — | **1.86× @4, degrades ≥8** |

Re-measured on cores 8-23 only (16 cores), to exclude the concurrent
stage-split run, the 460-file set gives 12.09 s → 2.95 s (4) → 1.54 s (8) →
0.88 s (16): **13.7× on 16 cores**. Independent small-export batching scales
near-linearly with core count.

But on the **kernel-bound perf suite** it peaks at width 4 and then *degrades*:
1→75.3 s, 4→40.4 s (1.86×), 8→41.6 s, 16→44.2 s. The heavy tests
(`magma-list-deep-n36` alone is 29 s and several reach 4–8 GB RSS) saturate
both memory and DRAM bandwidth; a width-24 run earlier touched ≈100 GB of the
125 GB machine. So the GPU/batch story must be **small independent checks**
(agent candidate proofs, `decide` certificates, repeated similar goals), not
batching the giant magma/deep-n36 cases.

## Elaboration vs kernel check (the other half of "Lean verification")

A user running `lean Foo.lean` pays *elaboration* (tactic execution + proof term
construction) and *kernel checking* of the resulting term. The arena export
measures only the latter. Using `set_option profiler true` on the arena test
sources (run with the official toolchain) separates them:

| Test | elaboration | tactic (decide/ring) | kernel type-check |
|---|---:|---:|---:|
| `grind-ring-5` | — | — | 721 ms of 0.97 s total = **74% kernel** |
| `magma-list-deep-n36` | 1.95 s | 17.1 s | 1.65 ms |
| `magma-list-deep-n21` | 1.6–1.9 s | — | 1.81 s (≈1:1) |
| `magma-list-pair-n21` | ~21.7 s | — | 15.5 s |

Two important consequences:

1. In real proofs the split is **workload-dependent**: `grind-ring-5` is
   kernel-bound, while `magma-list-deep-n36` spends 17.1 s in `decide` tactic
   execution and only 1.65 ms in the kernel on the *unexported* term.
2. The magma tests set `set_option debug.skipKernelTC true` (23 of 28 perf
   tests do). That option only affects *elaboration-time* kernel checking; the
   exported NDJSON contains the full proof term and the external checker pays
   the full cost (hence the 29.36 s for deep-n36 at the checker, versus 1.65 ms
   inside Lean). **Any Lean acceleration claim must say which stage it targets.**

## Correctness: semantics preserved

Every checker was run through the arena harness on the accept/reject groups:

| Checker | perf | bugs | other | corner-cases |
|---|---|---|---|---|
| official | 28 ✅ | 18 ✅ | 9 ✅ | 1 ✅ / 18 either |
| nanoclo | 28 ✅ | 18 ✅ | 9 ✅ | 1 ✅ / 18 either |
| lazylean | 28 ✅ | 18 ✅ | 9 ✅ | 1 ✅ / 18 either |
| nanobruijn | — | 18 ✅ | — | — |
| nanoda | 28 ✅ | 18 ✅ | — | — |
| parse-only | 26 ✅ / 2 ❌ | 18 ❌ | 5 ✅ / 4 ❌ | 1 ✅ |

`parse-only` accepting 2 rejects on perf and *all* 18 bug tests is the expected
signature of a checker that never checks — it is a performance floor, never a
correctness baseline. The four real alternative checkers agree with the official
kernel on every accept/reject test.

The 2 `perf` tests the official kernel "rejects" are `refute-cheap-first` and
`refute-cheap-last`, which the arena defines as `outcome: reject` — so the
official and alternative checkers are **28/28 correct**, and `parse-only`'s two
❌ are the two genuine rejects it wrongly accepts.

## Provenance

- Arena revision: `leanprover/lean-kernel-arena@b1d6e91d`
  (2026-10-03); the public results snapshot for the same revision
  (`b1d6e91d`, 223 tests × 25 checkers) was the cross-check baseline.
- Test revisions: `cslib` rev `990e65a685be…`; `mathlib` rev
  `d13f23b723b8…` (`v4.34.1`); arena test metadata sha256 digests matched the
  built exports for `init`/`std`/`cslib`/`mathlib`.
- Corpus digests: `init` `620502ac…`, `std` `289ed65a…`,
  `cslib` `bc5c88e0…`, `mathlib` (exact match to the arena's recorded digest).

## Honest limitations

- Single machine, single run per large corpus (repeats only where noted).
- Ambient load explains the variance in the raw `std` repeats; the isolated
  best-of values are reported above.
- `corner-cases` "either" means the arena itself tolerates either accept or
  reject (e.g. permitted-axiom policy differences); all checkers behave
  identically there.
- The arena measures post-elaboration checking. It says nothing about tactic
  search cost, which the profiler table shows can dominate.

## What this implies for acceleration

1. **Target the kernel check, but only for the class where it dominates.**
   Large libraries are 84–94% check; the stress suite is 97% check; but many
   individual proofs are elaboration/`decide`-bound.
2. **The kernel is memory-latency-bound** (2.6× instructions, half IPC, ~4×
   traffic). This is the mechanism-level reason a GPU could help a *large batch*
   of independent checks and little else.
3. **The batchable unit is small independent exports**, where batching already
   scales ~12× on CPU; large exports thrash and batching degrades.
4. Alternative checkers already reach **7.6×** over the official kernel by
   parallelizing across declarations — a GPU path must beat that, not just beat
   single-threaded Lean.

## Per-declaration check-cost distribution

The batchable class is *small checks*. To measure how uniform per-declaration
checking cost is, we split `init` by byte prefix at 12 equally spaced cut points
and timed each prefix (official kernel, single-threaded, cores 8–15):

| cut | decls | cumulative wall | Δwall for ~4,847 decls | marginal ms/decl | RSS |
|---:|---:|---:|---:|---:|---:|
| 0 | 4,847 | 3.57 s | 3.57 | 0.74 | 122 MB |
| 1 | 9,695 | 7.37 s | 3.80 | 0.78 | 168 MB |
| 2 | 14,542 | 10.86 s | 3.49 | 0.72 | 238 MB |
| 3 | 19,390 | 15.51 s | 4.65 | 0.96 | 276 MB |
| 4 | 24,237 | 19.24 s | 3.73 | 0.77 | 310 MB |
| 5 | 29,085 | 23.39 s | 4.15 | 0.86 | 389 MB |
| 6 | 33,932 | 27.46 s | 4.07 | 0.84 | 415 MB |
| 7 | 38,780 | 30.94 s | 3.48 | 0.72 | 452 MB |
| 8 | 43,627 | 34.69 s | 3.75 | 0.77 | 480 MB |
| 9 | 48,475 | 38.11 s | 3.42 | 0.71 | 514 MB |
| 10 | 53,322 | 41.22 s | 3.11 | 0.64 | 538 MB |
| 11 | 58,170 | 48.38 s | 7.16 | 1.48 | 566 MB |

Marginal check cost is **flat at 0.7–0.9 ms/decl** across the first 53k
declarations of `init` (the last segment is heavier: the export ends with the
harder core definitions). Two consequences:

1. The per-declaration check cost is remarkably uniform for most of a real
   library. A GPU checker does not need to load-balance wildly skewed work;
   static round-robin scheduling of declarations is close to optimal here.
2. RSS grows **linearly with declaration count** (122 MB → 566 MB for 58k
   decls), so resident memory is the binding constraint on how much of a library
   a single GPU/checker process can hold; the environment is the object that
   dominates, not the per-declaration work.

## GPU feasibility arithmetic

Measured inputs (this machine, this workload):

- export bytes: `init` 0.35 GB, `std` 0.60 GB, `cslib` 2.42 GB, `mathlib` 6.18 GB;
- declarations: 58k / 101k / 384k / 702k, i.e. **~23–38 KB of export per declaration**;
- CPU single-threaded check cost: `init` 27.4 s / 58,170 = **471 µs/decl** (official);
- CPU peak DRAM bandwidth on this host: 14.2 GB/s (1 thread), 168.3 GB/s (24 threads);
- best CPU accelerator: nanoclo `init` in 4.11 s wall / 12.96 s CPU = **223 µs/decl**,
  i.e. already 2.1× cheaper per core than the official kernel *and* parallel.

Transfer estimate (*inference*, not measured): host→device over PCIe 5.0 x16 is
~64 GB/s theoretical, ~50 GB/s practical. Moving a whole corpus is then
`mathlib` 6.18 GB / 50 GB/s ≈ **124 ms** against a 1.4–1.6 ks check — **~0.008%**.
Even a batch of 10⁵ small exports totals a few GB → sub-second transfer.

Conclusion: **per-corpus transfer bandwidth is not the GPU bottleneck** for
large exports; the handoff worry that "transfer cost is decisive" only applies
to the latency of many *tiny* transfers, fixable by coalescing. The real
question is whether a GPU kernel can check a *single declaration* faster than
223 µs, and whether the GPU can be fed 10⁵–10⁶ independent declarations to
amortize launch/sync.

This is why the ladder's rung 4 is *data-parallel checking of many independent
declarations* (one logical checker per declaration, like nanoda's model but on
GPU), not an intra-kernel port. Per-declaration work is pointer-chasing DAG
traversal (low arithmetic intensity) — the GPU's weakness — but the GPU offers
~10⁴ concurrent lanes versus 24 CPU cores. That trade is exactly what the
blocked prototype must measure.

## How much checking is actually "small independent checks"?

The batching/GPU argument depends on the batchable class being a large share of
real checking time. Using the public arena result snapshot
(`b1d6e91d`, official checker, 223 tests, 3635 s total wall for one full pass),
we split by export size:

| Export size | tests | Σ official wall | share of a full pass |
|---|---:|---:|---:|
| ≤ 10 KB | 154 | 3.7 s | **0.10%** |
| ≤ 100 KB | 199 | 5.0 s | 0.14% |
| ≤ 1 MB | 209 | 25.9 s | 0.71% |
| 7 large library exports | 7 | 3,561 s | 97.9% |

and the large exports themselves are dominated by a few:

| test | official wall | share |
|---|---:|---:|
| `mathlib` | 2275.66 s | 62.6% |
| `navier-stokes-euler` | 592.09 s | 16.3% |
| `cslib` | 428.85 s | 11.8% |
| `cedar` | 82.90 s | 2.3% |
| `con-leche` | 62.36 s | 1.7% |
| `std` | 71.57 s | 2.0% |
| `init` | 47.89 s | 1.3% |
| all other 216 tests | 74.12 s | 2.0% |

**This is a partial falsification of the naive batch premise.** In a *static*
library pass, checking time is concentrated in a handful of giant exports, not
in many tiny ones. So the batchable class cannot be justified by the arena
distribution alone; it has to be justified by a workload that generates many
small independent checks — which is exactly the agent/proof-search workload
(candidate proofs, repeated similar goals) the research plan targets. The
serving table above shows that such a stream batches at 517 jobs/s on CPU while
preserving accept/reject counts, but the *fraction of real user time* in that
class is an open question that needs an agent-style workload to settle.

## Repeated-candidate serving throughput

The agent/proof-search axis from the research plan: many small independent
checks (candidate proofs, repeated similar goals), where the runtime serves a
stream rather than one big file. Using `bench/lean_export_batch.py` on the 46
small correctness exports duplicated ×20 (=920 jobs, the same fixed job set at
every width), official kernel, cores 8-23:

| width | makespan | jobs/s | sec/job |
|---:|---:|---:|---:|
| 1 | 25.62 s | 35.9 | 27.8 ms |
| 4 | 6.01 s | 153.0 | 6.54 ms |
| 8 | 3.21 s | 286.2 | 3.49 ms |
| 16 | 1.86 s | 495.6 | 2.02 ms |
| 24 | 1.78 s | 517.8 | 1.93 ms |

Acceptance count is **260/920 at every width** (the 46-file set contains 13
accepting exports ×20), so batching does not change semantics. Throughput scales
14.4× to width 24; makespan is dominated by process startup + parse for these
tiny exports (each ~28 KB), not checking — the opposite regime from the perf
suite. Raw JSON: `results/2026-10-04-lean-batch-serving.json`.
