# Residual import preparation versus native candidate work

Observed 2026-10-16. This node reuses the original complete E033 capture and
the source-tagged native lifecycle partition. It runs no Lean/GPU workload,
does not add another tuning condition, and does not infer preparation savings
from cache-hit counts.

## Selected uncertainty and scope

Within RQ1, how much import-header preparation remains exposed after the
actual warm service is already engaged? The decision is whether an
import-only sharing/placement mechanism has meaningful remaining opportunity
on this cohort. This does not measure deeper theorem-body preparation or
answer RQ1 for every project/context.

The source is the complete29,750-source instrumented Goedel4.27 capture at
artifacts/lean-modern-native-compilation-2026-10-14/meta-inventory/full1/.
Its whole clock is22,762.528813585seconds, including the capture's declared
startup/verification/HTTP/logging/retirement/EOF work. Original request rows,
responses, stdout and terminal remain unchanged.

The prior source/event analysis identifies60unique requests running a header
and29,690reusing an already-started worker. That disjoint partition covers all
source IDs. All sources have the same actual service import header.
The new analysis joins those exact requests to their captured HTTP and native
body timer fields; no accepted-only performance subset replaces the cohort.

## Timer semantics verified in the actual source

The recorded command resolves the existing Python service root at
/tmp/gpu-smt-kimina-header-repair-20261014. Source inspection uses:
- server/routers/check.py: run_one prepares the worker/header before sending
  the candidate body and returns the body's ReplResponse.
- server/repl.py: send starts its monotonic timer after snippet logging and
  before writing the body; the timer ends after reading the native response.
- server/routers/backward.py: the legacy /verify response exposes that
  ReplResponse.time in the response.time field.

Consequently, body time is an IO-response wall interval, not exclusive CPU,
kernel time or complete declaration lifetime. HTTP time also contains
acquisition/launch/import, logging, serialization and transport. Current-source
inspection and the recorded command do not constitute an independent proof
of immutable source at capture time; the private copied tree's revision
qualification remains as previously recorded. This is not a new source gate.

All60header requests have matching source IDs, ordinary complete/rejected
responses, positive usable body timers and no negative HTTP-minus-body residual.
They comprise55complete and5rejected outcomes under the existing capture
classifier; no operational request is silently treated as zero preparation.

## Actual results

| Quantity | Same-capture result |
|---|---:|
| All original source attempts | 29,750 |
| Normal-return requests with usable body timers | 29,694 |
| Operational requests retained without body partition | 56 |
| HTTP wall summed across all requests | 90,931.659651s |
| HTTP wall summed across normal-return requests | 77,517.488691s |
| Reported body IO wall summed across those requests | 76,700.697044s |
| Outside-body residual for those requests | 816.791647s |
| HTTP wall for56unpartitioned operational requests | 13,414.170960s |
| Header-event requests | 60 |
| HTTP wall summed across header-event requests | 463.832362s |
| Body IO wall summed across header-event requests | 176.932948s |
| Their outside-body residual envelope | 286.899414s |
| Before first HTTP admission / after last response | 1.325502s /0.160972s |

The body's share of the normal-return request-wall sum is98.946313%.
It is not a whole-capture CPU fraction or critical-path fraction. Four requests
are in flight, so per-request sums overlap and cannot be added to or substituted
for the22,762.528814s whole makespan. The56operational requests remain in the
full result and whole clock; their13,414.170960s request sum is not discarded
or assigned a fabricated body timer.

For a header-event request, preparation occurs before body execution within
that request. Its observed preparation wall is therefore no larger than the
HTTP-minus-body residual, which also includes other outside-body costs.
Summing the60residuals gives286.899414s as an observed cumulative envelope for
that preparation stage. It is not a direct measurement of header CPU.

Normalizing that cumulative envelope by the whole clock gives1.260402%.
If all of it were removable with every other cost and scheduling effect held
fixed, the arithmetic1/(1-0.01260402) gives1.012765x. This is a deliberately
optimistic fixed-other-work sensitivity calculation, NOT a measured speedup
or rigorous counterfactual system guarantee. Changes to scheduling, memory,
mutation, cache effects and replacement can violate that assumption.

## Research decision

Do not implement or retune an import-only prepared-context cache/placement
mechanism on this cohort as a new headline. The actual warm service already
engages on29,690requests, and the remaining measured envelope is small even
before removing unrelated overhead from it. Existing Kimina-style header reuse
is an engaged strong competitor, not a cold-start strawman.

Larger opportunity must be sought in real candidate elaboration/construction/
checking or demonstrably expensive deeper preparation, with a genuinely
different mechanism and an equal-resource complete comparison. The existing
CPU profile identifies Meta/argument comparison and runtime allocation as
candidate regions, but its sampledCPU percentages must not be multiplied by
this request-wall decomposition. No higher-coverage GPU method is inferred,
and the deferred narrow E034 backend remains deferred.

This decision bounds the tested import-only constructor. It does not replace
the original fourRQs, reject all snapshots, claim that deeper preparation is
free, remove SMT scope, or prove that a GPU cannot help. Ordinary native
compilation remains a mandatory baseline/control rather than our novelty.

## Reproduction, review and limitations

[Executable offline analysis](analyze-preparation-envelope.py),
[recorded command](request-body-cost-command.json), [output log](request-body-cost-analysis.log)
and [complete result](goedel-request-body-costs.json) retain all source
association, counts, normal/error partition and60header rows. The initial
header-only calculation is retained in goedel-header-request-envelope.json.

Analysis returns0. All29,750rows and the60header events associate with no extra
event IDs or negative residuals. No input or native source is changed; only offline analysis/records are added and no background acquisition row count is polled.

The capture is instrumented and shares host resources; it is not the final
uninstrumented baseline evaluation. Timer and source-provenance qualifications,
unpartitioned operational work and overlapping request wall remain explicit.
The result is supporting admission evidence, not a standalone new benchmark,
final RQ answer, a whole-service ablation or an independently reviewed result.
The existing OMP experiment/paper owners receive this node for integration;
fresh opportunity and complete-paper independent audits remain outstanding.


## Distinct larger-cost question from the existing Meta observation

The published E033 counters also permit a same-denominator mean without another
native run. [Recomputed group means](observed-meta-group-means.json) divide each
group's completed outer observed threadCPU by its completed outer call count:

| Entry descriptor | Completed outer calls | Observed mean outer threadCPU |
|---|---:|---:|
| Expression or universe metavariable present | 84,960,591 | 117.257us |
| Neither metavariable flag present | 208,151,679 | 14.791us |
| All observed completed outer calls | 293,112,270 | 44.492us |

Only the first two rows form a partition. These are instrumented outer-call
means, not uninstrumented latency or the cost of mutating a metavariable.
Expression size, nested normalization, caches, typeclass work and observer
cost can explain the association; none is causally separated by the flags.
They also do not measure E034's candidate pairs inside those outer calls.

The larger question is native candidate-body Meta reduction/comparison with
its real context and dependencies, rather than another closed-term metadata
or import-only operation. This is an opportunity question for source/algorithm
review, not an admitted GPU backend: a useful independent fraction, algorithm,
batch readiness and complete-cost advantage must still be established. The
35% sampledCPU subtree and this observer's means remain different measurements
and are not multiplied. No new claimed contribution or RQ answer follows.
