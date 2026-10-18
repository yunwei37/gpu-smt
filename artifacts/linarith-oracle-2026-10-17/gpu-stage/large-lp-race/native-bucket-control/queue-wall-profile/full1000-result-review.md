# Complete strongest-queue all-call profile

This report is root self-review of the original1,000-source cohort under the
stronger upstream eight-queue interface.

## Matched clocks and engagement

The diagnostic's own native clock is691.204649455seconds; its CPU oracle
clock is545.050104294seconds. Both return992complete/eightrejected/no
operational outcomes. Every native responseJSON exactly matches the
corresponding uninstrumented primary,including the oracle's existing warnings.
These clocks remain separate from primary685.730742286/537.312851014seconds
and the earlier eight-item-wave1245.96/1072.37profile.

There are13,230native and10,251oracle numerical calls. All source IDs,
FP matrix shapes and product metadata are complete; no ambiguous/unmatched
calls or numerical errors remain. Every numerical worker has an EOF-count
agreement,complete waited CPU receipt and exit status0. Stderr is empty.
The initial qualifier with the missing row parameter remains explicitly
invalid; this full capture passes the repaired existing row11.

## Four observed native regions

| Region | Calling/numerical CPU seconds | Occupied wall union seconds | Fraction of691.20s |
| --- | ---: | ---: | ---: |
| Hypothesis preprocessing and linearization | 250.701699413 | 362.219912604 | 52.4041% |
| Nonlinear product proof construction | 211.555251509 | 335.243647575 | 48.5014% |
| Numeric floating/exact LP search | 859.531730268 | 544.439052770 | 78.7667% |
| Lean certificate construction/checking | 208.565876734 | 325.794004146 | 47.1342% |

These wall occupancies overlap across concurrent candidates. They are not a
disjoint four-way partition. Numeric generation is distinct from building
Lean product proofs. Other frontend,export,kernel and full retirement work
remains charged to the native clock.

## All-branch numerical costs

CPU-oracle numerical services consume554.829665890CPU seconds:
546.831982314LP search,3.132194694numeric products,0.261489586exact repair,
0.040906871exact coefficient verification,and the remaining parsing,
packing,linearization,response and dispatch work. Failed direct searches
alone use76.601090922LP CPU seconds; failed fallback searches44.279118153.
The complete outcome split is3,597checked direct certificates,605direct
no-certificate results,5,440fallback certificates and609fallback misses.
The raw error fields contain no internal service error.

The exact-search fallback dominates:1,888oracle calls use518.393022903CPU
seconds after cheap floating search fails. All have at least15rows; median
82rows/230columns/1,514nonzeros. There are221.403723389seconds with exact
searches from at least two different source candidates active together.
This is potential availability at the CPU exact-search stage,not achieved
GPU batching or device-ready transfer time. Any implementation still owes
packing,communication,queueing,repair,fallback and cancellation costs.

## Applicable zero-cost conclusion

GPU-replaceable numeric products plus all FP/exact LP search sum to
833.985378914interval seconds on the545.050104294second oracle clock.
Concurrency makes that sum exceed the whole clock; subtracting it doesnot
produce a useful finite upper bound.

Their observed interval union is411.683389511seconds,75.5313%of that same
oracle clock. A deliberately optimistic fixed-timeline compression deleting
every occupied instant leaves133.366714783seconds and yields
691.204649455/133.366714783=5.182737316xagainst this diagnostic's own native
reference. It also deletes concurrent non-GPU work. This is not a
scheduler-invariant upper bound or a measured/achievable GPU speedup.
Neither the overlap sum nor union establishes a below1.5xopportunity ceiling;
the user's negative-GPU-closure condition is not met. No old2234.69or
eight-item-wave clock is substituted into the new denominator.

## Derived CPU accounting correction

The raw Rust timers include exact verification nested inside response
packing. Naively summing parent and child CPU double-counts it and produces
two negative residual records. The analyzer now subtracts direct child CPU
from its containing phase while preserving every raw interval. All request
CPU residuals reconcile; raw clocks,LP/product wall,call outcomes and worker
receipts are unchanged. The initial derivation and two examples remain
retained. This is an accounting correction,not smoothing or omitted work.

The [machine summary](full1000-own-clock-summary.json),[native raw](full1000-native/),
[oracle raw](full1000-oracle/),[region unions](native-four-observed-regions.json),
[exact-LP availability](large-exact-LP-availability.json) and
[nesting diagnosis](numeric-timer-nesting-review.json) provide reproduction
inputs. Use the canonical checked-in analyze-cost.py with exclusive CPU
accounting; the launch-time source snapshot predates this derived correction.
All fourRQs and systems novelty remain unresolved; no independent audit or
OSDI acceptance is claimed.
