# Recorded numerical cost and ready-work boundary — root self-review

Observed2026-10-22UTC. This is reanalysis of the already complete protected
whole-population matrix, answering the existing GPU-cost/ready-work question;
it is not another experiment, new solver variant or full GPU evaluation.
The source/native/full results in a4c4b67 and the updated paper in cf9b4c5
remain unchanged. No capture, device, Agent or resource setting is started.

## Existing records actually consumed

[Reader](analyze-recorded-numerical-costs.py),
[all counts, phase totals, unknown request IDs, LP shapes and source-owned
overlap pairs](full-recorded-numerical-costs.json).
All three full Power cells' closed support-calls and phases are consumed,
not a favorable prefix. Decoded input source bodies join uniquely to original
released sources after removing only leading import/blank lines.

|Pair|Connection records|Decoded inputs|Input unavailable|Known HiGHS solver seconds|Different-source overlap pairs|
|---|---:|---:|---:|---:|---:|
|1|5618|3041|2577|15.662468|3|
|2|5641|3026|2615|16.096152|2|
|3|5654|3175|2479|16.154946|2|

The HiGHS timer is the solver's reply field for the decoded requests only.
The matching highs_solve phase wrappers sum16.711/16.779/17.226seconds;
difference from the reply timer is wrapper overhead, not a separate LP gain.
Build phases sum1.742/1.765/1.809seconds and extraction3.340/3.412/3.524.
All decoded phase begin/end records pair; no decoded source attribution is
unknown. Whole Power clocks are16,661.346/16,912.114/16,750.330seconds.
These component observations are not exhaustive removable wall fractions.

Decoded LP rows have median82–85,p99400.5–410.26,
maximum1,511. Columns median189,p99658.3–665,maximum1,596. Nonzeros
median1,309–1,341,p995,657–5,660,maximum11,950. Exact per-repetition quantiles
and observed denominators are in the linked output, not all exported LPs.

## Missing-input records are not LP solves or zero work

There are2,577/2,615/2,479JSONDecodeError records with input/shape/call ownership
unavailable. They are connection-handler failures, not2,500additional solved
LPs or final Lean candidate failures. No source ID or matrix is invented.
The actual frozen service adapter uses StreamRequestHandler.rfile.readline(),
then json.loads(), records exceptions and keeps input None when decoding fails
(bench/lean-native/linarith-oracle/reproduction/support-proxy.py:247–263).
An owner winning/cancelling while its numerical child is still writing can
cause EOF with partial JSON; this is a possible cause, **not classified as
proven for every record**, because the failed raw request bytes/peer ownership
are not retained. A single-read fragmentation bug is not established by these
logs, and no speculative protocol change or blind new whole matrix is made.
Numerical source/repair/fallback remains checked by the final native verifier.

All connection-handler envelopes, including these failures, sum
37.431/37.979/38.496seconds, caller-thread CPU21.952/22.108/22.373seconds.
Retired service whole-process CPU is separately112.698/113.641/116.290seconds.
It includes other threads, startup and bookkeeping; assigning its difference
to LP or communication is unjustified. No overlapping per-request process
timers are subtracted.

## Actual concurrency and interpretation

The decoded service intervals have maximum overlap two. Exact overlap pairs
are source-owned and all3/2/2pairs are between different original candidates.
This is observable cross-candidate CPU numerical overlap, **not actual GPU
batches, GPU eligibility, or a guarantee that all phase work is simultaneously
ready**. The full raw records' active_at_arrival counts2for7/3/5connections
also include undecoded requests, so they are not substituted for decoded pairs.
No large ready backlog has been demonstrated in this protected-source2path.

The recorded completed numerical path is small. This makes another GPU
replacement of only these decoded completed HiGHS calls a weak next target.
However, it does not cover all native/early/cancelled/small-LP paths, product
construction, exact reconstruction or their own-clock critical path, and the
native reference has no complete matching phase partition in this capture.
Do not rescale historical2234.69or divide this solver timer by a different
run to manufacture the required below1.5×bound. Original better-valid-CPU/GPU
criterion and prohibition on premature GPU closure remain unchanged.

Run status: closed raw reanalysis completed, with explicit missing input.
Hypothesis: large already-ready cross-candidate numerical batches are not
supported by the observed protected CPU service path.
Research value: supporting cost/coverage boundary for the existing RQ4
experiment, not a second headline result or independent audit.
Next decision: retain unknowns and obtain missing same-strong-reference native/
product attribution before admitting a new accelerator mechanism; do not
restart a whole solver/grid or claim GPU failure from this component timer.
