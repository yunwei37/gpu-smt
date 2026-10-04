# Lean verification acceleration

The user asks how to accelerate Lean verification, including useful GPU work.
This continues the solver-serving research in `docs/research-plan.md`; Lean is
in scope now. Evidence and its limits take priority over a prescribed CPU/GPU
sequence. Measurements live in `results/` and raw data in `artifacts/`.

## Separate the stages

| stage | experiment | interpretation |
|---|---|---|
| theorem search/tactics | frontend profiles or collected candidate streams | proof construction; not measured by arena exports |
| frontend elaboration/checking | normal-check runs with complete profiler logs | disable-check profiles cannot identify the normal split; nested categories overlap |
| export parsing/setup | official `--parse-only`, implementation-specific RSS | cost of this parser/representation, not a shared irreducible floor |
| post-export replay | official full and separate parse-only runs | difference estimates added replay cost; run variability remains |
| repeated serving | fixed fixture throughput, dispatch-to-response times | amortized throughput differs from request latency; fixtures are a proxy |

## Current evidence

[Corrected first-round report](../results/2026-10-04-lean-kernel-stage-split.md)
uses pinned real init/std/cslib/mathlib exports and arena stress/correctness
fixtures. It preserves the prior observations while correcting their scope.

- Official full-minus-parse differences are about 84–94% of full wall for these
  library runs; the exported perf suite is also replay dominated. This is not
  a conclusion about all normal frontend or theorem-search workloads.
- The 398.337/105.408 G instruction ratio is 3.779. IPC differs, but no memory
  traffic or memory-latency bottleneck has been established.
- Nanoclo reaches 69.97 seconds on Mathlib versus official 1565.93 seconds in
  the completed rerun (22.4×); perf-suite speedup is separately 7.6×. Different
  algorithms, representations, parsing and parallelism all contribute.
- Tiny fixed-fixture process pools scale; large perf batches show weak scaling.
  Neither observation proves bandwidth saturation. Affinity masks and unequal
  CPU core groups must be retained; `taskset` does not establish isolation.
- Prefix block means include parsing and thousands of declarations. Individual
  check-cost distribution and optimal declaration scheduling remain unmeasured.
- Alternatives pass their tested definitive subsets, but some `either` inputs
  differ from official. Finite fixture agreement does not prove equivalence.
- Public arena static time is concentrated in large exports. Repeated small
  fixtures are not a real agent candidate stream and cannot establish its share.

## Next implementation and experiments

1. **Persistent official replay**, using the same parser and official kernel,
   but removing repeated executable startup. Every request builds a fresh
   environment and parses its input; no result memoization. Compare cold versus
   persistent at identical masks/widths, alternating order with repeats. Retain
   input SHA256, each decision, errors and response times. Validate both rejected
   and accepted fixtures after preceding requests, and the heavier perf suite.
   Completed: three repeated small-fixture trials per mode/width showed 9.5×
   lower median makespan at width 16; 215-fixture validation matched every official
   decision and all 197 definitive expectations. See the continuation report.
   Code: `bench/lean-persistent` and `bench/lean_persistent_bench.py`.
2. **Normal frontend profile corrections**: run representative stress proofs
   with checking enabled and disabled, after valid module headers, with complete
   outputs and exit status. Completed for deep-n36 and grind-ring-5: normal deep-n36 reported 61.8 s
   in type checking, versus 0.499 ms with checks disabled. Use normal-check
   observations in conclusions; categories may overlap.
3. **Stronger CPU baseline**: matched repeated alternative-checker scaling on
   pinned identical core groups, with frontend/post-export boundaries explicit.
   Do not subtract official parse time from other implementations.
4. **Candidate workload characterization**: collect complete generated proofs
   with imports/context and official accept/reject results; statements alone
   cannot measure verification throughput. Then evaluate shared-environment reuse
   with prefix/dependency validation and fresh-state fallback.
5. **GPU experiment when justified**: select a measured hot operation or a
   clearly delimited checker subset, implement CPU reference and GPU variant,
   quantify coverage and compare to the best CPU backend on the same inputs.
   Full accept/reject fidelity or official fallback is mandatory for a serving
   claim. A preparatory primitive is not a validated whole Lean checker.

No GPU code has yet been validated. Persistent CPU replay is the selected next
experiment because the small-fixture baseline pays a separate process per check.
This directly connects to the existing serving work and needs no infrastructure
change. If it removes most overhead, a GPU tiny-export checker becomes a weaker
near-term target; large-library checking remains a separate opportunity.

## GPU decision and resource coordination

Export bytes per input record are 5.97/5.89/6.31/8.81 decimal KB. Assuming
50 GB/s effective PCIe throughput gives 123.69 ms to copy Mathlib's raw NDJSON;
that is 0.177% of nanoclo's measured full run and 0.0079% of official full wall.
These are conditional estimates, excluding parsing, GPU representation building,
allocation, launch/sync, return transfer and runtime startup. Measure those costs
before drawing an end-to-end conclusion. Neither these estimates nor weak CPU
scaling establishes a GPU win or a GPU impossibility result.

The `standard-dev` workspace has not been assigned a GPU. Host sysfs/proc/dmem
visibility does not demonstrate container allocation. Use the existing Kubernetes
NVIDIA device-plugin/runtime path for a bounded experiment with matching driver
libraries, preserving this project's Workspace/PVC and other projects' processes.
No manual device allowlist changes or host-device probing is needed.

A GPU resource request should name the ready executable, input hashes, CPU
reference, measured operation/coverage and device memory requirement. The old
whole-checker sketch is not a ready executable and is not an execution request.
Current delivery/resource state is in `docs/lean-resource-status.md` and the
owning agent-state request file.

`argumentcomputer/ix`'s GPU certificate proving must remain distinct from ordinary
Lean type checking. A certificate proving speedup does not establish a kernel
checking speedup.
