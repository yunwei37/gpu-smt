# Lean kernel checking: measured stages and checker comparison — 2026-10-04

This report corrects the first-round draft at commit `00400a8`; that commit and
all prior data remain preserved. Local measurements and the downloaded public
arena snapshot are identified separately. GPU transfer estimates are conditional
arithmetic, not measurements. New persistent-process results are in
[the continuation report](2026-10-04-lean-persistent.md).

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

### Environment and affinity

Intel Core Ultra 9 285K, 24 distinct logical/physical cores, one socket and
approximately 125 GB RAM. Checker toolchain `leanprover/lean4:v4.34.1`; CSLib export is from Lean
4.34.0 and the other three library exports from 4.34.1, per retained headers.
[Topology](../artifacts/lean-2026-10-04/cpu-topology.txt) reports CPUs 0–7 at
5.5–5.7 GHz maximum, and 8–23 at 4.7 GHz maximum. The hybrid perf counters also
identify core/atom classes. These groups cannot be treated as equal-speed cores.

`taskset` restricts affinity; it does not reserve cores or isolate memory,
frequency, thermals or background work. Earlier runs overlapped on this machine,
including the Mathlib stage-split and small-export measurements. Masks varied:
0–7 for later official library runs, 0–15 for nanoda t1–t16, 0–23 for several
alternatives/batches, and 8–23 or 8–15 for later batching/prefixes. Consult the
[original commands](../artifacts/lean-2026-10-04/prior-commands.json) for each run.
There is no evidence supporting a global “no competing jobs” assertion.

## Official parse/load versus replay

`--parse-only` reads/materializes the export but omits replay. Full minus
parse-only is a difference between separate runs, estimating additional replay
cost in this implementation. It is not direct instrumentation of every kernel
operation and includes variability between runs.

| Corpus | parse wall | full wall | difference | parse peak RSS (KiB) | full peak RSS (KiB) | difference/full |
|---|---:|---:|---:|---:|---:|---:|
| init | 5.47 s | 33.67 s | 28.20 s | 576960 | 582968 | 83.8% |
| std | 9.30 s | 58.83 s | 49.53 s | 954416 | 954812 | 84.2% |
| cslib | 38.31 s | 305.74 s | 267.43 s | 3581564 | 3581732 | 87.5% |
| mathlib | 117.36 s | 1565.93 s | 1448.57 s | 10424436 | 10417484 | 92.5% |

The init row uses retained GNU-time records (`tv-init.log`, `tvpo-init.log`);
the draft's 32.78/5.41 seconds could not be located in a raw timing record and
is superseded here. Other rows come from the completed `clean_timings.log`.
That script ended with `CLEAN_DONE` before takeover; no duplicate was launched.
Std's second pair was 59.00/9.33 seconds. Cslib and Mathlib each have one pair
in that script. The earlier Mathlib pair was 1712.10/107.63 seconds, with
1604.47 seconds difference (93.7%). Full-wall spread is 8.5% relative to the
first run; its cause was not measured. These are descriptive single-run or
limited-repeat estimates, not confidence intervals or asymptotic scaling laws.

Parse/full RSS is similar within the official implementation, approximately
9.94 GiB for Mathlib. This is not a universal resident-memory floor. Alternative
parsers, term representations, reduction algorithms and memory reclamation can
change both time and memory. Nanoclo's full Mathlib run (69.97 seconds) is already
below either official parse-only wall time.

### Instruction counters

Retained `ps-full.csv` and `ps-po.csv`, init, affinity 0–7:

| mode | instructions | IPC | task clock |
|---|---:|---:|---:|
| full | 398.337 G | 1.95 | 44.157 s |
| parse-only | 105.408 G | 3.53 | 6.124 s |

The instruction ratio is **3.779×**; full IPC is **0.552×** parse IPC.
These counters establish more instructions and fewer instructions per cycle.
They do not measure memory traffic, cache misses, DRAM stalls or bandwidth.
Pointer-heavy reduction may be sensitive to memory latency, but that remains a
hypothesis. No GPU benefit follows from IPC alone.

The prior `bw.c` experiment reported 14.2/55.2/168.3 GB/s. Its OpenMP loop
parallelizes repetitions writing the same destination array concurrently,
without independent thread partitions or a validated checksum. It is not a
sound bandwidth calibration and is excluded from mechanism conclusions.

## Alternative checker measurements

Wall times combine parsing and checking. They are individual observations with
varying settings, not a matched, repeated best-backend study. Peak RSS is GNU
`time`'s KiB value; for lazylean's forked workers it is not aggregate pool RSS.

| checker | init wall / threads | std wall / threads | cslib wall / threads | mathlib wall / threads |
|---|---|---|---|---|
| nanoda (Rust) | 4.02 s / t16 | 6.83 s / t16 | 33.69 s / t16 | 116.05 s / t24 |
| nanoclo (Rust) | 4.11 s / t4; 3.74 s / t8 | 4.21 s / t24 | 20.22 s / t24 | 69.97 s / t24 |
| nanobruijn (Rust) | 5.97 s / t24 | 11.04 s / t24 | 50.33 s / t24 | 142.31 s / t24 |
| lazylean (C++) | 5.41 s / j8; 4.00 s / j24 | 6.60 s / j8 | 32.76 s / j8 | 123.44 s / j8 |

Nanoclo init's 4.11-second command changed `num_threads` from 4 to 24 **after**
running; its original t24 label was incorrect. The later explicitly configured
scaling series gives t1/t4/t8 = 11.86/4.57/3.74 seconds. Nanoda init t1/t2/t4/t8/t16
was 27.07/13.13/7.51/5.11/4.02 seconds, affinity 0–15.

Using the official table above, nanoda library speedups are 8.4×/8.6×/9.1×/13.5×,
and nanoclo's displayed fastest library observations are 9.0×/14.0×/15.1×/22.4×.
These ratios should not be confused with perf-suite totals below. Nanoclo at
t1 was already faster than official init; parallelism is one contributor,
alongside parser, representation and algorithm differences. This data does not
attribute the speedup among those contributors.

Retained peak RSS examples: nanoda Mathlib 7490252 KiB; nanoclo Mathlib
9473224 KiB; nanobruijn Mathlib 7036272 KiB; lazylean Mathlib 7338096 KiB. Raw logs take precedence
over rounded prose, and worker-process RSS does not establish total pool memory.

### Perf stress suite

28 exported kernel stress fixtures. Official sum is 60.155 seconds; parse-only
sum 1.549 seconds; their difference is 97.4% of full wall. These are summed
separate invocations, not normal frontend stage timings.

| Checker | perf-suite total wall | Speedup vs official |
|---|---:|---:|
| official | 60.16 s | 1.0× |
| parse-only | 1.55 s | 38.8× (excludes checking) |
| nanoclo | 7.87 s | 7.6× |
| lazylean | 13.22 s | 4.6× |
| nanoda | 116.71 s | 0.52× (**slower**) |
| nanobruijn | — | — |

The arena integration defaults to four internal threads/workers, with some
manual configurations changed during measurement. Nanoclo's suite command
explicitly set t16; nanoda/lazylean use their arena configuration. Retained YAML,
commands and per-test JSON document what is available; configs copied at takeover
are final state and do not retroactively prove historical thread settings.
These totals establish workload-specific performance, not a parallelism-only
explanation or bandwidth saturation.

## Independent export batching

The original fixed-corpus process-pool observations are retained:

| Job set | width 1 | 4 | 8 | 16 | 24 | best |
|---|---:|---:|---:|---:|---:|---:|
| tutorial suite (141 subtests) | 4.07 s | — | 0.552 s | — | 0.367 s | 11.1× @24 |
| 46 small correctness files ×10 (=460) | 12.32 s | 3.06 s | 1.59 s | 0.81 s | 0.68 s | 18.1× @24 |
| perf suite (28 kernel-bound exports) | 75.3 s | 40.4 s | 41.6 s | 44.2 s | — | **1.86× @4, degrades ≥8** |

A later affinity-8–23 run (16 lower-clock CPUs) of 460 small fixtures yielded
12.09/2.95/1.54/0.88 seconds at widths 1/4/8/16 (13.7×). Perf28 at that mask
was 75.3/40.4/41.6/44.2 seconds. Stragglers, aggregate memory demand, shared
resources and oversubscription may contribute to weak scaling; no memory-stall
or bandwidth measurement diagnoses which. Process peak RSS is not aggregate
pool RSS. Width 24 under an 8–23 mask oversubscribes 16 CPUs.

## Frontend profiles: disabled checks are not a normal stage split

The original magma profiles used `debug.skipKernelTC=true`. For deep-n36,
17.1 seconds in `decide` and 1.65 ms in the profiler's type-check category
therefore **do not** establish that normal kernel checking is negligible.
Elaboration and tactic categories can overlap/nest and should not be added as
independent stages. Exported replay checks the complete term regardless of
this frontend option.

The old grind-ring 721 ms sample also contained a syntax error from inserting
`profiler` before its `module` header. It is not a validated normal frontend
measurement. The original profile claims/table are withdrawn. Corrected normal
and disabled-check runs are reported separately in the continuation report,
including commands, exit codes and complete profiler output.

## Correctness coverage and differences

The retained local harness records establish the following tested subsets:

| Checker | perf | bugs | other | corner-cases |
|---|---|---|---|---|
| official | 28 ✅ | 18 ✅ | 9 ✅ | 1 ✅ / 18 either |
| nanoclo | 28 ✅ | 18 ✅ | 9 ✅ | 1 ✅ / 18 either |
| lazylean | 28 ✅ | 18 ✅ | 9 ✅ | 1 ✅ / 18 either |
| nanobruijn | — | 18 ✅ | — | — |
| nanoda | 28 ✅ | 18 ✅ | — | — |
| parse-only | 26 ✅ / 2 ❌ | 18 ❌ | 5 ✅ / 4 ❌ | 1 ✅ |

A dash means untested, not agreement. All tested definitive accept/reject
fixtures scored correct for the alternative checkers in these records. That
is finite test coverage, not proof of semantic equivalence. Some arena wrappers
map all nonzero failures to rejection, so a “correct reject” score alone may
not distinguish a deliberate rejection from a backend exception.

The `either` cases are explicitly outside a single expected decision.
Nanoclo differs from official on five such inputs: `proj-maybe-prop`,
`proj-maybe-prop-past`, `nested-nonuniform-param`, `alg-conv-trans-quot-left`,
and `imax-right-successor`. Lazylean differs on `nested-nonuniform-param`.
Thus the claim that all checkers behaved identically was false. Parse-only
fails all 18 bugs, two perf rejects and four other rejects; it is not a
correctness baseline. Repeated acceptance counts alone cannot establish identity.

## Prefix experiment: block averages including parsing

`prefix_split.py` scans declaration record byte offsets, then selects endpoints
at approximately equal **declaration counts**, not equally spaced bytes. Counts
in the table are observed from the record scan, including inductive groups as
one export record each. Every prefix reparses and replays its whole prefix.
Affinity was 8–15 and the long Mathlib run overlapped on other CPUs.

| cut | decls | cumulative wall | Δwall for ~4,847 decls | Δ full-wall ms/record | RSS (MiB) |
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

The last column is actually MiB (`rss_kb / 1024` in the script), despite the
original MB label. “Δ full-wall ms/record” divides differences of independent prefix
**full-wall** measurements by blocks of roughly 4,847 export records. It includes
parse/setup differences, not just checking. The block means range from 0.64 to
1.48 ms; neither their narrow middle range nor rising RSS establishes individual
cost uniformity, optimal round-robin scheduling, linear memory scaling or a
binding device-capacity constraint. Per-declaration measurements are still needed.

## Conditional GPU transfer arithmetic

Using decimal KB (1000 bytes), the measured export bytes divided by export
record counts are **5.9748 / 5.8908 / 6.3092 / 8.8092 KB per record** for
init/std/cslib/mathlib. The earlier 23–38 KB statement was arithmetic error.
These denominators count input records, not necessarily all generated kernel
constants or independent scheduling tasks.

Assuming, without measurement, effective host-to-device throughput of 50 GB/s,
a one-way copy of raw Mathlib NDJSON is 123.69 ms. That is 0.0085% of the
completed official full-minus-parse estimate (1448.57 s), **0.0079% of official
full wall (1565.93 s)**, and **0.177% of the fastest measured complete CPU run
(nanoclo, 69.97 s)**. This calculation includes no JSON parsing, GPU term layout
construction, allocation, launch, synchronization, driver startup, return path
or checking, and it assumes a transfer bandwidth that was not measured.
It only bounds a hypothetical raw byte-copy component under that assumption;
it does not establish that GPU transfer/setup is negligible or that a GPU
checker can beat the CPU. CPU time/declaration quotients are amortized corpus
costs, not per-declaration latency or a target for an individual GPU lane.

## Public snapshot workload distribution

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

The size buckets are cumulative. These are public snapshot observations,
from another runner, not timings collected on this workspace. The static pass
is dominated by large libraries, which can still expose parallel declarations
inside an export. It does not establish a real agent candidate distribution.

## Repeated fixed-fixture throughput proxy

46 other/bugs/corner-case exports repeated 20 times, 920 jobs, affinity 8–23:

| width | makespan | jobs/s | amortized ms/job |
|---:|---:|---:|---:|
| 1 | 25.62 s | 35.9 | 27.8 ms |
| 4 | 6.01 s | 153.0 | 6.54 ms |
| 8 | 3.21 s | 286.2 | 3.49 ms |
| 16 | 1.86 s | 495.6 | 2.02 ms |
| 24 | 1.78 s | 517.8 | 1.93 ms |

The last column is milliseconds of **amortized throughput cost**, makespan/jobs,
not seconds and not per-request latency. Width 24 still has only 16 allowed CPUs.
The old JSON retains aggregate acceptance 260/920 at every width but no individual
decisions; it cannot establish semantic fidelity. These are repeated correctness
fixtures, not a collected agent/proof-search candidate stream. The new experiment
records each input and compares its actual decision with official replay.

## Provenance and limitations

Retained data: [artifact directory](../artifacts/lean-2026-10-04/), including
manual GNU-time/perf logs, scripts, local per-test arena records, the public
snapshot, selected original command journal, topology and checker metadata.
Arena revision: `b1d6e91d6de351f9bcf21e6b039f4d51d6b9bb42`.
Exporter revision: `f297dfe2a8557e8674fe892bb49dffe4bfadc0e9`.
CSLib and Mathlib revisions and full input hashes are in the artifact manifest.
The checked-out code/builds/large exports remain in `/tmp/lean-kernel-arena` in
this owning workspace. Large input bytes are retained there, with reproducible
build metadata and hashes in the repository.

One machine, limited repeats, mixed affinity and historical overlap limit causal
and cross-machine claims. The strongest established conclusions are that official
post-export replay is costly on these libraries, alternatives can be much faster
on exactly those exports, and tiny fixture process pools scale. The next useful
experiment is persistent official replay with fresh state, per-input parity and
service-time measurements. No GPU checker or GPU acceleration result has been
validated. Mechanism profiling and a real candidate stream remain open.
