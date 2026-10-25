# gpu-smt

A research prototype for accelerating native Lean and SMT verification.
Lean has priority; RTX 5090 is the only GPU target.

The broader hypothesis is that related verification jobs can share expensive
prepared state while preserving native behavior and independent candidate
execution. [The initial narrative and four research questions](docs/idea-story.md)
remain intact. The OSDI-quality systems contribution and all four final RQ
answers are still open.

## Current work: failure hotspots in Lean

The complete native/GPU counterexample-screening pair returns all **7,808**
miniF2F candidates with identical statuses and accepted sets: **3,014 valid,
4,669 Lean errors, 83 timeouts and 42 resource failures**. Native takes
21,693.76s; GPU takes23,615.03s (**8.86% slower**) before its additional
23.99s input preparation. The full cold-controller clock is unavailable
after an observation outage; actual completion and cleanup are recorded.

Exact screening refutes34 intermediate goals in29candidates, all ordinary
Lean errors, with no timeout reduction. It remains a small component; no
further GPU-pair expansion is planned. All42resource failures report native
allocation failure under the24GiB-per-process limit on both sides. The48GiB
aggregate watchdog records no kills or errors.
[Complete pair, accepted sets, failure causes and limitations](artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md).

Next, profile the baseline's83timeouts and slowest10%of failed requests
(480sources) using actual Lean tactic/phase measurements, then choose our
method from the dominant measured cost. All4RQs and the systems goal remain
open. Existing external-system comparisons are retained without expansion.

## Collection resources

New runs use the user-requested **48 GiB total owned-process RSS budget**,
at most **two live REPLs**, each with a **24 GiB address-space limit**, and
CPU eligibility on CPUs 8–11. A parent watchdog samples the owned tree every second,
kills the largest owned REPL on excess and records its candidate as a resource
failure. This is a sampled response, not a kernel hard RSS quota.
RTX 5090 is shared through NVIDIA time slicing, without fixed half-card
partitions. Only one full acquisition group runs at a time.

[Implementation, real qualification and limits](artifacts/linarith-oracle-2026-10-17/shred-closing/aggregate-budget-20261019/README.md).
Older unbudgeted captures and captures with 48 GiB per worker are stopped partial records;
their results are not pooled with this resource point.

## Completed measurements

**No useful extra end-to-end GPU acceleration over the strongest measured CPU
composition has been demonstrated.** Selected-cohort improvements do not
establish whole-population performance or a new systems contribution.

| Completed comparison | Whole elapsed | Scope and result |
|---|---|---|
| 29,750 Goedel originals, three native/CPU pairs|18,584.96/16,661.35;18,478.26/16,912.11;18,608.55/16,750.33s|CPU-only aggregate 1.10627×, 9.61% less elapsed; two additional checked completions and the same 40 timeouts|
| 1,000 selected heavy originals: native / CPU / CPU+GPU|1,376.24 /769.12 /762.44s|1.789× CPU and 1.805× CPU+GPU versus native; 992 complete and eight rejected throughout|
| Same GPU condition including cold provider lifecycle|797.61s|3.70% more elapsed than CPU; no established useful extra GPU gain|
| 7,808 miniF2F originals: native / retained SHRED integration|18,987.74 /19,235.45s|3,015 versus 3,010 genuine completions; five regressions and 11 sorry-bearing incomplete results retained|
| 5,952 ProofNet originals: native / retained SHRED integration|356.37 /373.22s|413 genuine completions each; 20 native rejections become sorry-bearing incomplete responses|

All outcomes, resource failures, latency tails and baseline limitations remain:

- [Complete Goedel population](artifacts/linarith-oracle-2026-10-17/kimina-full29750-budgeted-20261019/full-result-review.md), [cohort cost figure](docs/paper/figures/full-goedel-cohort-costs.pdf).
- [Matched heavy-cohort CPU/GPU results](artifacts/linarith-oracle-2026-10-17/current-budget-gpu-20261023/full-result-review.md).
- [Complete miniF2F comparison](artifacts/linarith-oracle-2026-10-17/shred-closing/aggregate-budget-20261019/full-pair-result-review.md).
- [Complete ProofNet comparison](artifacts/linarith-oracle-2026-10-17/shred-closing/proofnet-full-result-review.md).
- [Current evaluation, earlier experiments and open requirements](docs/evaluation.md).

The same-clock native profile on the 1,000 heavy inputs finds 39.94 s in floating
LP solves and 951.85 s in 1,636 exact fallbacks within its own 1,380.32 s lifecycle.
Concurrent phase sums are not an Amdahl ceiling. A faster narrow LP kernel
alone therefore does not establish whole-verifier benefit.
[Attribution, shapes and tails](artifacts/linarith-oracle-2026-10-17/native-stage-profile-20261022/reference-full-result-review.md).

Warm REPLs, caches, snapshots, native compilation, batched LPs, external
certificate oracles and counterexample testing are prior techniques, not
individual novelty claims. The remaining scientific question concerns useful
whole-flow savings beyond competent native execution.

## Workloads and reproduction

| Workload | Retained input | Native environment |
|---|---|---|
|GoedelWorkbook| 29,750 released original source files|Lean 4.27|
|miniF2F|244 tasks × 32 candidates = 7,808|Lean 4.9.0-rc1|
|ProofNet|186 tasks × 32 candidates = 5,952|Lean 4.9.0-rc1|
|AutoVerus / VeruSAGE|Original source runs and solver traces|Version-aligned native SMT execution|

Released candidate files are replay workloads, not generator arrival traces.
All populations retain accepted, rejected, incomplete and resource-failure
outcomes. Current run records identify actual SDKs, native libraries and
numerical binaries; historical Workspace paths are not a universal installer.

- [Current counterexample source and execution instructions](bench/lean-counterexample/README.md).
- [Arithmetic implementation and experiment commands](bench/lean-native/linarith-oracle/README.md).
- [Portable arithmetic source build and 64-source functional qualification](bench/lean-native/linarith-oracle/reproduction/README.md).
- [Retained-environment reproduction guide](docs/reproduce-checkpoint.md).
- [Benchmark methodology](bench/README.md).
- [Real SMT replay and limitations](results/2026-10-04-verusage-real-traces.md).

For an existing captured SMT trace directory:

    python3 tools/analyze_smt_trace.py traces --json trace-analysis.json

Initial synthetic-prefix commands and the complete previous README remain in
the [dated historical archive](docs/tmp/bootstrap/step-0011-20261023T195335-0700/readme-history-through-20261024T0707.md.gz).
Synthetic controls are not the real-workload evidence.

## Repository and paper

- `bench/` and `tools/`: experiments and adapters.
- `artifacts/` and `results/`: source snapshots, raw data and self-reviews.
- [Research narrative and fixed RQs](docs/idea-story.md),
  [design](docs/design.md), [related work](docs/background-related-work.md).
- [Paper source](docs/paper/main.tex) and [current PDF](docs/paper/main.pdf).

The manuscript has completed a
[12-round serial writing self-review](docs/tmp/bootstrap/step-0011-20261023T195335-0700/iter-refine-writing-20261024T0615/round-11-meaning-preservation.md).
Its current citation update retains all numerical results, four RQs and
15 missing result slots. The compiled draft is 32 pages including appendices;
it is not submission-ready.

All implementation, experiments and review run in this thread. Reviews are
**self-review**, not independent audit. Tests, measurements and a compiled
paper do not establish venue acceptance.
