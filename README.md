# gpu-smt

A research prototype for accelerating native Lean and SMT verification.
The current implementation moves arithmetic search outside Lean and returns
certificates for native checking, with fallback for unsupported cases.
Lean has priority; RTX 5090 is the only GPU target.

The broader research hypothesis is that related verification jobs can share
expensive prepared state while preserving native behavior and independent
candidate execution. [The initial narrative and four research questions](docs/idea-story.md)
remain intact. The OSDI-quality systems contribution and all four final RQ
answers are still open.

## Current result

The corrected native-array comparison uses the original **1,000 arithmetic-heavy
Goedel candidates**, selected before the implementation's measurements:

| Composition | Complete whole time |
|---|---:|
| Adapted compiled Fast/hybrid + official omega | 810.71 s |
| Direct natural-power oracle + official omega | 476.73 s |

This is **1.70059×**, or 41.20% lower elapsed time. Both conditions return
992 complete and eight rejected sources, with matching per-source verdicts
and non-message fields. All 108 message differences are retained.
Direct source service spans are longer for169candidates, including63of the
70IDs that regress in all three earlier instrumented observations. All
remain in the result. Whole-corpus improvement coexists with these regressions;
source spans include waiting and do not establish per-candidate guarantees.

Both use eight queues, four CPUs (8–11), a 48 GiB address-space limit and the
same original input order. Preparation, parsing, numerical search, native
checking, fallback, queueing and retirement are charged. Eager Lean diagnostic
rows, stage clocks and product tagging are removed; the optional process-tree
observer is off in both. Candidate, RPC, omega and backend records remain,
so this is not entirely instrumentation-free.

The control includes common product-application reuse and is an adapted
frontend, not pristine stock Mathlib. The proposed composition includes the
numerical portfolio and direct proof path; the result is not attributable to
power coverage or ordinary compilation alone. This is one fixed-order,
shared-host observation, not a global CPU optimum or a GPU gain.
[Complete source, protocol, raw data and limitations](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-without-diagnostics/full1000-result-review.md).

Three earlier observations of the instrumented build aggregate **1.78205×**.
They use a different affinity and retain diagnostic computation, so their
absolute clocks are not pooled with the comparison above.
[All three observations](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-whole-repetitions/result-review.md).
Their complete candidate distributions improve, but 70 source IDs have longer
service spans in all three observations. Those regressions remain in the data.
Service spans include waiting and cannot be relabeled CPU work.
[Distributions, figure and retained regressions](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-whole-repetitions/service-span-result-review.md).

A complete three-pair check of **438 official DeepSeek-Prover-V2 proof
outputs** through the unchanged Kimina HTTP app/SDK gives **1.05863×**
aggregate whole-lifecycle speedup (5.54% less elapsed). Each of six cells
returns 263 valid and 175 Lean-error results, with matching verdicts and
non-message fields and one warning-only source difference between methods.
This modest transfer uses overlapping miniF2F tasks and an adapted Lean 4.27
default-exact reference; it is neither a new theorem domain nor a GPU gain.
[All three pairs, returned records and latency distributions](artifacts/linarith-oracle-2026-10-17/kimina-dsv2/result-review.md).

The original Goedel cohort's separate official HTTP comparison has closed
its first stock/native/Power block: 2888.76/857.11/534.48 seconds, respectively.
Power is 1.60363× faster than the strong native reference in that block.
The original three-block matrix continues; this is not its final aggregate.
[Scoped checkpoint and raw data](artifacts/linarith-oracle-2026-10-17/kimina-http/first-block-result-review.md).

A separate complete default-tiered/Power control on the same 1,000 inputs
takes **1018.23/492.98 s**. Its 2.06546× ratio is against a slower measured
reference and does not replace the faster hybrid comparison above.
[Complete default-engine control](artifacts/linarith-oracle-2026-10-17/kimina-http/reference-engine/full1000-result-review.md).

The existing SHRED closing-certificate executor now has real native and
HTTP qualifications. Its complete formal-population service comparison is
running; early cache hits are not a new system contribution or a full speed
result. [Baseline source, failures and scope](artifacts/linarith-oracle-2026-10-17/shred-closing/README.md).

## Complete workloads and scope

| Workload | Retained input | Native environment |
|---|---|---|
| GoedelWorkbook | 29,750 released original source files | Lean 4.27 |
| miniF2F | 244 tasks × 32 candidates = 7,808 | Lean 4.9.0-rc1 |
| ProofNet | 186 tasks × 32 candidates = 5,952 | Lean 4.9.0-rc1 |
| AutoVerus / VeruSAGE | Original source runs and solver traces | Version-aligned native SMT execution |

All populations retain accepted, rejected, incomplete and resource-failure
outcomes. Released candidate files are not a generator arrival trace.
The selected 1,000-source result does not establish whole-population speed.

The oracle now runs in the formal datasets' unchanged Lean 4.9 environment.
An actual 64-source integration check produces identical complete responses
in stock, native-preprocessing and direct modes, with 88 direct native
certificate checks including six nonlinear requests. The complete ProofNet comparison returns matching outcomes on all5,952
originals: stock1151.88s, native1160.92s and direct1178.93s. Direct is2.35%
slower in this component experiment; its module-loaded stock condition is
not pristine Mathlib. miniF2F continues acquiring.
[Closed ProofNet evidence and baseline limitations](artifacts/linarith-oracle-2026-10-17/formal-oracle-4.9/full-populations/proofnet-result-review.md).
[Adapter, qualification and full-population protocol](artifacts/linarith-oracle-2026-10-17/formal-oracle-4.9/README.md).
The native-only mode is a component control, not the fully ported 4.27 Fast
frontend or an entire upstream Kimina service.

An earlier full 29,750-source acquisition uses a frozen older oracle build;
it cannot generalize the current natural-power implementation.
[Earlier implementation and capture scope](artifacts/linarith-oracle-2026-10-17/gpu-stage/full29750-generalization/).
The [current whole-Goedel protocol](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-full29750/plan.md)
extends the corrected comparison to all originals, without another solver grid.

The official Kimina HTTP comparison now closes all **nine planned
1,000-source cells**. The first two intact strong-native/Power pairs are
857.11/534.48 and 812.07/456.82 seconds, a ratio of summed whole times
**1.68383×**. Every cell returns 992 complete/eight rejected/zero operational;
all per-source verdicts and non-message fields agree, with 108 message
differences per pair. The third pair spans a container restart and is
reported separately. Power has 152–245 longer individual body spans per pair.
[Complete matrix, raw records, tails and restart limits](artifacts/linarith-oracle-2026-10-17/kimina-http/full-matrix-result-review.md).

## What the GPU measurements show

**No useful extra end-to-end GPU acceleration over the strongest measured CPU
composition has been demonstrated.**

RTX 5090 executes independently cancellable LP groups using request-sized CUDA
VMM. A valid additive portfolio retains native hybrid and CPU HiGHS while
adding GPU support: 38.02 s CPU versus 39.33 s CPU+GPU on the same 64 originals,
about 3.43% more elapsed time.
[Actual device composition and lifecycle](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-cpu-gpu-portfolio/result-review.md).

A ready-goal trial gives 79.93 s CPU and 79.59 s CPU+GPU on 15 originals, but
no GPU answer wins. Two actual groups contain three device models, including
a cross-candidate group; that small elapsed difference does not demonstrate
device benefit.
[Ready-goal device evidence](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/ready-goal-batch/additive-device/result-review.md).

An earlier representation has detailed own-clock numerical/CPU accounting.
Its conditional bounds do not prove all GPU designs impossible and are not
transferred to the current implementation.
[Accounting, assumptions and retained raw data](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-omega-cost/full1000-result-review.md).
The GPU route remains open. An LP count, a narrow kernel speedup, a live server
or overlapping candidate spans alone does not establish whole-verifier benefit.

The 5090 is shared through NVIDIA time slicing, without fixed half-card
partitions. Current product expansion, exact repair and Lean checking run on
CPU. Device preparation, transfer, batching, fallback and retirement belong
in the end-to-end comparison.

## Preparation and prefix reuse

Complete original miniF2F/ProofNet prefix experiments are retained. Parsed
unit-prefix potential is 13.44%/18.38% of tactic edges, not time saved.
The current prefix executor has no validated whole-verification speedup;
native outcomes and resource failures differ.
[Sharing and actual request costs](artifacts/linarith-oracle-2026-10-17/formal-default/sharing-result-review.md),
[miniF2F results](artifacts/linarith-oracle-2026-10-17/formal-default/minif2f/unit-result-review.md),
[ProofNet results](artifacts/linarith-oracle-2026-10-17/formal-default/proofnet/result-review.md).
This is a source-native executor using SHRED's parser, not a complete upstream
SHRED/Kimina service comparison.

The complete as-integrated SHRED/Kimina HTTP ProofNet comparison now covers
all **5,952 originals**. Native takes **356.37 s**, SHRED **373.22 s** including
preparation, **4.73% more elapsed time** in one shared-host fixed-order pair.
Both have 413 genuine completions, but twenty native rejections become
sorry-bearing incomplete responses with cache-hit messages. SDK valid counts
417/437 therefore are not verified-proof counts. This is no matched transparent
speedup and no whole-family impossibility result.
[Full raw comparison, costs and self-review](artifacts/linarith-oracle-2026-10-17/shred-closing/proofnet-full-result-review.md).
The miniF2F eight-source capture exhausts host memory despite each process
staying below 48 GiB. Recovery compares both methods at two outstanding
sources, the same four CPUs and 48 GiB per process; original partial data
remain, and these new clocks stay separate from the eight-source point.
[Failure evidence and recovery plan](artifacts/linarith-oracle-2026-10-17/shred-closing/memory-recovery-20261019/plan.md).
Completed ProofNet is not rerun.

Warm REPLs, caches, snapshots, native compilation, batched LPs and external
certificate oracles are established techniques. They are not individual
novelty claims here. Known failures, earlier clocks and closed constructors
remain in [the evaluation ledger](docs/evaluation.md).

## Repository guide

- [Current evaluation and original evidence](docs/evaluation.md).
- [Arithmetic implementation and experiment commands](bench/lean-native/linarith-oracle/README.md).
- [Current measured Lean source and build](artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-without-diagnostics/README.md).
- [Portable arithmetic source build and64-source functional qualification](bench/lean-native/linarith-oracle/reproduction/README.md).
- [Retained-environment reproduction guide](docs/reproduce-checkpoint.md).
- [Research story](docs/idea-story.md), [design](docs/design.md) and [related work](docs/background-related-work.md).
- [Paper source](docs/paper/main.tex) and [current PDF](docs/paper/main.pdf).
- `bench/` and `tools/`: experiments and adapters; `artifacts/` and `results/`:
  source snapshots, raw data and reviews; `docs/paper/`: manuscript.

Current run records identify the exact retained SDK, native libraries and
numeric binaries. The separate arithmetic source build passes64real-source functional checks;
the historical Workspace-specific capture paths are not a universal installation recipe.

All implementation, experiments and review run in this thread. Reviews are
**self-review**, not independent audit. Tests and measurements do not establish
venue acceptance or submission readiness.

## Initial SMT tools

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

[Initial research plan](docs/research-plan.md),
[benchmark methodology](bench/README.md) and
[real SMT replay](results/2026-10-04-verusage-real-traces.md)
retain the earlier serving prototype and its limitations.
