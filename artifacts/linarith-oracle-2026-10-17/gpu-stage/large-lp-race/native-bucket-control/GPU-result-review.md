# Native eight-queue GPU qualification: root self-review

## Question and native protocol
Does the upstream eight sequential queues, instead of the collector's eight-item
wave barriers, supply a useful GPU oracle path under the same maximum eight
candidate tasks, four allowed CPUs (8–11), 48 GiB address-space limit, and same
24 original-order sources? The upstream mode is spelled "parrallel"; it is an
existing API, not a new scheduling contribution. The only private Lean change
adds existing candidate timing to that queue implementation. Whole-array
observation has no artificial 300-second client deadline; native command
behavior and heartbeat settings are retained. This does not prove timeout
equivalence for sources that would exceed an old array deadline.

## Completed real observations
| Condition | Whole cell seconds | Native/condition |
| --- | ---: | ---: |
| Native compiled | 29.551738559 | 1.000000 |
| CPU AST oracle | 23.475818756 | 1.258816 |
| CPU/GPU same-LP race, warm cuOpt | 23.857266664 | 1.238689 |

All 24 sources complete in each cell, in original order. Native verdict and
all non-message native response fields agree. The CPU oracle has two and GPU
three accepted-source warning-only response changes. All 24 task spans are
present in each condition and actual simultaneous candidate peak is eight.
The GPU is 1.6249% slower than CPU oracle in this single qualification.
Seven transient process-read errors in the GPU sampler prevent a complete
peak-resource assertion; the CPU native cell has six. Do not compare incomplete
sampled peaks as a resource benefit.

125 labelled races select 112 CPU certificates, ten CPU no-certificate answers
and three exactly repaired GPU certificates. Nine actual two-source batches
are submitted: two return results, seven are cancelled, all nine have client
retirement receipts and the dispatcher reports zero pending jobs. Returned
jobs report 0.362 seconds of solve time; cancelled device compute is unknown.
Summed overlapping race decision/retirement spans are 12.352334634/0.102193656
seconds, not disjoint portions of the 23.857-second cell.
There are 56 accepted proxy connections, only 15 fully parsed requests:
41 JSONDecodeError records, 11 client-disconnected requests and four
PDLP_OPTIMAL replies. An accepted/aborted connection is not an LP solve.
The exact failed-frame byte sequence was not retained; CPU-winner termination
during request writing is an explanation, not a source-by-source fact.

The pinned upstream cuOpt Job is retired and deleted after qualification.
Its complete start-to-restoration lifecycle is 40.0839035 seconds:
5.7427047 to PodReady, 26.0502647 client wrapper, 8.2889444 retirement/restoration.
This is a cold lifecycle clock, not a solver-only time. Lab remains Ready and
the other Workspace remains Running. Server and clients share CPUs8–11; the
GPU server is not included in the client's sampled PSS.

## Decision and limitations
The queue protocol helps CPU qualification, but the matched GPU condition does
not improve CPU time. No full1000 GPU matrix is admitted for this unchanged
backend. This qualification does not establish full-cohort queue performance,
stable GPU benefit, an impossibility bound, or new systems novelty. The current
own-clock Amdahl sensitivity remains above1.5x and the GPU route stays open.
The next causal question is whether the joint LP solve and any-member
cancellation destroy independent useful GPU work. Check the actual pinned
upstream API before implementation; do not open a parameter grid.

Raw cells, native responses, real task spans, resources, all proxy records and
job events are retained in [the qualification directory](bucket8-qualification24-gpu/).
The [machine summary](GPU-qualification-summary.json) is regenerated from these
closed cells. This review is performed by the same root thread. It is not an
independent audit or a whole-paper milestone review.
