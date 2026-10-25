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

RL mode returns every candidate outcome. First-success mode cancels siblings
only after checked same-task acceptance. Exact completed/in-flight reuse
retains each caller's identity; cancellation and resource failures are not
native rejections or cacheable proof results.

[Architecture](docs/architecture.md) · [API and compatibility scope](docs/api.md) ·
[Examples](examples/README.md) · [Paired measurement](docs/benchmarking.md) · [Contributing and checks](CONTRIBUTING.md) ·
[CI](.github/workflows/engine.yml) · [Apache-2.0 engine license](LICENSE).

An [optional native import parent](native/lean/README.md) passes the pinned Lean4.18
native differential/lifecycle CI; the default backend remains fresh-process. Full Mathlib COW
qualification, native failure detectors, source-aware
cost models and multi-node execution remain implementation/research work.
Resource mechanisms are prior techniques; novelty must come from workload
methods and actual end-to-end results.

An [exact-source audit](artifacts/engine-resource-profile-2026-10-25/exact-duplicates/result-review.md)
finds no duplicate substantive proofs among the 7,808 miniF2F candidates:
only 18 repeated literal None failures. Exact caching is supported, but is
not the expected source of meaningful acceleration on this population.

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

The completed 480-source failure profile attributes 55.19% of observed
timeout thread CPU to interval_cases and 28.21% to simp_all. All selected
statuses are unchanged. These diagnostic fractions are not total elapsed-time
fractions or a proven early-rejection mechanism.

Four directions continue: the layered Rust engine, reliable early failure/timeout determination,
same-task ranking/cancellation for pass@k or best-of-n, and public Lean
code-verification workloads. The sole active full collection now compares
native all-candidate execution against two first-success scheduling policies
on all 7,808 original candidates. Its real eight-candidate qualification
checked winners before cancelling siblings. The original Verina 189-file
native/profile characterization is complete; admitted stubs and source-version
errors are reported separately from completed reference files.
There is no performance admission threshold, deadline or closure decision.
The external CPU oracle stays **frozen as a baseline**: no optimization,
extension or new oracle experiments, and no contribution claim.
Candidate cancellation serves first-success inference, not per-candidate RL
reward collection. Existing comparisons and all raw data remain.
[Current scope and evidence boundaries](docs/evaluation.md#current-decision-frozen-oracle-and-three-continuing-directions).

## Collection resources

The **next resource point** keeps **48 GiB total actual RSS**, removes fixed
per-process address-space caps, and jointly admits candidates by measured
memory and CPU demand on CPUs8–11. A15-second observation of existing REPLs
finds one active thread/~one core per worker, motivating up to four workers
at this point, subject to actual memory admission. The Rust watchdog samples
owned trees each second; concurrent preemptions are requeued for an exclusive
retry, whose resource failures remain separately reported. This is sampled
response, not a kernel hard RSS quota.

The healthy original7808capture retains its frozen two-worker/24GiB-AS
settings and remains the sole full group. Its results are not mixed with the
new resource point. The historical42bad_alloc candidates await separate
larger isolated reruns after that group retires.
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

- [First-success candidate scheduling](bench/lean-candidate-scheduling/README.md).
- [Public Lean code-verification profiling](bench/lean-code-verification/README.md).
- [Current counterexample source and execution instructions](bench/lean-counterexample/README.md).
- [Frozen arithmetic baseline and historical commands](bench/lean-native/linarith-oracle/README.md).
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

- `crates/`: reusable Rust engine; [layered design](docs/architecture.md).
- `bench/` and `tools/`: experiments and historical adapters.
- `artifacts/` and `results/`: source snapshots, raw data and self-reviews.
- [Research narrative and fixed RQs](docs/idea-story.md),
  [design](docs/design.md), [related work](docs/background-related-work.md).
- [Paper source](docs/paper/main.tex) and [current PDF](docs/paper/main.pdf).

The manuscript has completed a
[12-round serial writing self-review](docs/tmp/bootstrap/step-0011-20261023T195335-0700/iter-refine-writing-20261024T0615/round-11-meaning-preservation.md).
Its current citation update retains all numerical results, four RQs and
14 missing result slots. The compiled draft is 34 pages including appendices;
it is not submission-ready.

All implementation, experiments and review run in this thread. Reviews are
**self-review**, not independent audit. Tests, measurements and a compiled
paper do not establish venue acceptance.
