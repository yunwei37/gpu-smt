# Device path bottlenecks — root self-review

The original-prefix64/capacity32 trial actually launched 10 CUDA kernel groups
containing 25 distinct-source models; it was not 10 cuOpt single-request jobs.
Nevertheless GPU45.022186258s trails the matched CPU oracle39.662807654s by
13.512% (all verdict/non-message parity retained). This analysis uses only
the already-complete source-labelled raw data, not a new benchmark.

## Measured supply and response costs

The same four CPUs/32 candidate queues yield 63 numeric connections per
oracle. Only52CPU/51GPU connections contain parsed LPs; the remaining
interrupted JSON frames are not solves. CPU HiGHS reports29optimal and
23infeasible returns, summing1.316882133s solver wall. This is concurrent
solver-call time, not the whole39.66s denominator or all exact fallback work.

GPU returns6feasible,6phase-I negative hints,5numerical declines and34client
disconnections. The actual25models include8cancelled models. Of68native
races, only6positive and2negative certificates are won by the device path;
25positive and35negative exact CPU decisions remain. Some device hints
arrive too late or fail exact reconstruction. Numerical no-hint is distinct
from a verified infeasibility certificate.

For all25models, arrival at the proxy to dispatch has median0.561439373s,
p90 3.919167370s and maximum8.913590424s. Dispatch to provider group begin
has median0.011706310s and maximum0.027392834s. Provider group begin through
observed model result has median0.067176791s and maximum8.849305373s.
It includes allocation, copying, startup and host observation, not just
device compute. Individual model construction sums1.025526680s, of which
the first allocation alone is0.909295460s. No numerical warmup was hidden.

49GPU calls match exact full numerical input and source from the CPU cell.
The machine-readable analysis retains each side's times, shapes and states.
They are observations from different elapsed captures, not simultaneous
latency races or proof of isolated causal savings.

## Concrete head-of-line dependency

The proxy's gpu_dispatch calls solve_cuda_batch synchronously and waits for
all model/kernel retirement before draining later arrivals. The provider
also has one launch owner. Although individual results/cancellation are
streamed, the next group cannot progress independently of the longest live
member. A cancelled66,393-pivot model retains its group for about4.15s
after the first sibling result. A41,616-pivot model similarly retains its
group for8.78s. Subsequent requests can wait seconds before dispatch.
Thus independent request cancellation has not eliminated group-level
head-of-line blocking. This is a concrete limitation of the implementation;
do not claim the GPU cannot slow the overall CPU path merely because its
LP search is speculative. Host service/repair competes for the same CPUs.

Removing this dependency requires independent in-flight groups and memory
operations that do not reintroduce global synchronization; adding Python
threads alone is not sufficient evidence of concurrent GPU execution.
[NVIDIA's stream-ordered allocation documentation](https://docs.nvidia.com/cuda/archive/13.1.0/cuda-programming-guide/04-special-topics/stream-ordered-memory-allocation.html)
describes the relevant allocation/stream ordering. Any new implementation
must qualify under the unchanged48GiBlimit and prove actual overlapping
groups, individual cancellation and complete retirement before a real64source
preflight; no free warmup, abandoned contexts, resource enlargement or
parameter grid is admitted by this diagnosis.

## Limits and next decision

The maximum/quantiles are cumulative host-model observations; their sums
cannot be subtracted from cell wall, combined into an Amdahl fraction or
called GPU kernel time. CUDA event timing and current Lean-certificate stage
timing are unknown. Negative cancel acknowledgement-to-result intervals
can occur because the result precedes the RPC acknowledgement; these are
signed host ordering records, not negative cancellation latency.

This evidence explains why more nominal candidate concurrency did not
establish benefit. It does not prove a below1.5x GPU opportunity bound or
justify global route closure. Preserve the CPU reversed-order replication
and the original broader systems/RQ goal. Exact numerical-query reuse remains
a strong CPU baseline question, not the proposed new systems contribution.
