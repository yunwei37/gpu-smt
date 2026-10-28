# Exclusive retry headroom — completed historical resource traces

All42exclusive attempts are matched by exactPID/birth to retained RSS/CPU
samples;none lacks a sampledleader.41finish resource-exhausted,one timesout.
This asks whether the86%singleton-exclusive attribution proves safe backfill;
it does not. [Exact per-source analysis](analysis.json),[executed source](analysis-source.py).

| Observed quantity | Result |
|---|---:|
| Exclusive resource failures |41|
| Resource-failure native peak lower bound |47.749–47.967GiB|
| Median exclusive attempt duration |213.015s|
| All exclusive attempt envelope sum |8927.470s|
| Samples with an exclusive leader alone |7389|
| Samples with at least4GiB aggregate headroom |6598|
| Samples with at least8GiB aggregate headroom |5962|
| Samples with at least16GiB aggregate headroom |4658|

The first four observations explain why a retry cannot be declared a small
fixed-memory job. But late growth is real:many earlier samples leave substantial
headroom. Neither fact licenses assuming constant memory or discarding the
opportunity. Samplecounts are not uniform elapsed-time shares or a speedup.
These sampled peaks are lowerbounds,not safe reservations for futureattempts.

Accepted/rejected ordinary attempt peaks have median487,299,072B and maximum
5,684,461,568B. They omit unsampled spikes and may coexist with backend-owned
importstate. Counting just the medianchild as the full incremental Mathlib
working set would underreserve memory. Adding it to an exclusive retry
invalidates the existing guarantee that finalresource failure was observed
with all peers retired.

The committed retry-frontier change is the first pending native test. It
avoids intermediate queue drains;it does not remove the8927s envelope sum.
A later backfill design would need explicit preemption/requeue semantics
so that a failure under sharedmemory is never reported as final solo failure,
and must include lost work,extra attempts,parent preparation and cleanup.
Do not implement anotherpolicy before reviewing the currentmatchedqualification
and testing the alreadycompletedchange.

All data here precede the compiledMathlib loader repair,so neither native
costs nor observedgrowth ratios transfer automatically to the newpoint.
No newcandidate/collection/observer is run. Rootself-review,no novelmethod
or strongest-warm throughputclaim.
