# Complete current-resource original1000 matrix — root self-review

**Run status: valid, complete. Tested hypothesis: additional useful GPU gain
over the retained CPU portfolio is inconclusive. Research value: supporting.
Paper impact: additional RQ4 evidence and a resource/workload boundary.**

The predeclared original1,000 heavy Goedel candidates complete on all three
conditions at the corrected shared resource point. Native outcomes/non-message
fields match for every candidate:992 complete,8 rejected, no operational
failure. CPU and GPU full native responses are identical. Relative to native,
108 sources have message-only differences, retained rather than called full
raw-response equivalence.

| Condition | Whole cell (s) | Warm verify (s) | Preparation (s) | Native / whole | Peak own RSS (GiB) |
|---|---:|---:|---:|---:|---:|
| Native compiled hybrid | 1376.236473072 | 1369.948781923 | 5.750965960 | 1.000000× | 15.259586 |
| CPU oracle (native + HiGHS) | 769.116831166 | 762.531126831 | 6.085669180 | 1.789372× | 14.731617 |
| CPU oracle + GPU | 762.439982722 | 756.120294023 | 5.793457326 | 1.805042× | 14.968769 |

The GPU cell is0.868119% less elapsed than CPU, a ratio of1.008757× CPU/GPU.
One fixed-order shared-host observation has no whole-run confidence estimate;
the small difference is not established useful device acceleration. Including
provider startup, client wrapper and provider retirement gives797.608028s,
1.725455× versus native and3.704404% more elapsed than CPU. No cold overhead
is silently dropped from the headline interpretation.

The original better-valid-CPU/GPU >1.5× selected-cohort criterion is met by
CPU1.789372×, as well as the GPU cell1.805042× (cold1.725455×).
This does not generalize to whole Goedel: the completed29,750-candidate CPU
matrix is separately1.106271× and includes two outcome changes. This new
comparison neither pools the historical8-worker clocks nor redefines the
1.5× criterion as extra GPU-over-CPU gain. It does not establish novelty or
OSDI-level system contribution.

## Protocol, complete scope and source

Frozen source695c2b485b2f7ab32579b0f93e5058195e5a84fb. Order is GPU,
actual provider retirement/UID deletion, CPU Power, native. Official Kimina
HTTP/SDK uses the unchanged original1000/order, Lean4.27.0, two source
workers/two actual live REPLs,24GiB AS per REPL,48GiB aggregate sampled
own-process RSS and CPU affinity8–11. Both CPU and GPU use the same new
private arithmetic binaries. GPU retains native and HiGHS competitors and
adds device eligibility at38 LP rows; it does not remove the small-LP CPU
competitor. Parsing, preparation, queueing, packaging, transport, fallback,
exact checks, local cancellation and retirement are in whole cell clocks.
The separate provider cold lifecycle is reported above.

Reproduction: run the recorded lifecycle.ps1 -Full through its existing
benchmark lifecycle only after preserving existing output directories; never
overwrite an existing capture. Read-only reconstruction:

    python3 artifacts/linarith-oracle-2026-10-17/current-budget-gpu-20261023/analyze.py full

The reader validates all three closed terminals, original IDs, actual HTTP
responses, resources, native outcomes and CPU/GPU fields. Closed source logs,
failure records and memory bytes are losslessly gzipped; raw-archive.json
retains original/compressed sizes and roundtrip checks. Capture startup and
prior failed/minimum2 qualifications remain separate, with no discarded rows.

## Same-native-ranked heavy tails

Selection uses native HTTP durations from this same matched cell. These are
overlapping per-source HTTP envelope sums, not isolated tail lifecycles,
removable wall fractions or pure solver time.

| Native-ranked cohort | Sources | Native HTTP sum (s) | CPU HTTP sum (s) | GPU HTTP sum (s) |
|---|---:|---:|---:|---:|
| Slowest 1% | 10 | 449.120364972 | 255.927555301 | 254.354804545 |
| Slowest 10% | 100 | 1266.105499475 | 639.657564711 | 634.291370188 |

All selected IDs remain in full-analysis.json. paired-source-latencies.csv
retains every per-source envelope: GPU is shorter on555 and longer on445;
this is not555 causal device wins. The three largest GPU regressions are
Proof_16178 (+1.048919s), Proof_23622 (+0.507380s) and Proof_16213
(+0.420904s). Small differences can include host drift and CPU contention.
Do not aggregate overlapping HTTP durations as whole experiment elapsed.

## Actual device work and limits

906 races across379 source IDs retain CPU contenders. Actual GPU results win
6 positive-certificate races and4 exactly checked negative-certificate races.
488 actual CUDA models are singleton launches, not true cross-candidate
multi-model batches. All groups retire; final provider probe has0 live device
bytes/allocations and16MiB peak device bytes. The provider's exact UID is
deleted before CPU controls, and its host RSS is included in the GPU aggregate.
[gpu-phase-result-review.md](gpu-phase-result-review.md) and full-analysis.json
retain all source joins, win IDs, cancellation states and ownership.

The existing proxy serializes new submission until prior kernel retirement.
505 inputs decode;5 source-owned arrivals occur during a prior group's
retirement,4 already CPU-finished before that retirement.192 incomplete JSON
connections remain unassigned, not solved LPs or proof that no batch supply
exists. The observed absence of batches is not a GPU impossibility proof.

All three cells have no resource failure, watchdog error/kill or live owned
descendant after shutdown. Maximum live REPL count is2.763/769/1376 samples
cover GPU/CPU/native; largest sample gaps1.018203/1.003418/1.024087s.
The48GiB protection is a sampled response, not a hard kernel RSS quota.
Original parent PIDs224887/236466 no longer exist at result collection.

## Decision and next action

Close this complete matrix, retain valid negative/mixed GPU evidence and the
selected-cohort CPU gain, and update only implementation/result/limitation
slots. All4 RQs, Lean+SMT workload promise and original system contribution
remain open. No full-paper acceptance or independent audit is claimed.

Do not repeat this same full matrix or tune a narrow solver. The concrete
admission serialization is a runtime mechanism defect, not evidence that
the device or cross-candidate batching is useless. Next inspect/remove that
single-flight admission dependency while retaining complete retirement,
CPU contenders and the same aggregate budget; qualify on the original real
prefix before admitting any further complete measurement. If qualification
does not create real concurrent device work or a defensible discriminator,
do not promote another full variant. The broad GPU route remains open because
the own-clock diagnostics do not provide a strict exclusion of1.5×.
