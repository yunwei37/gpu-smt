# Global fallback repair — root self-review

Only explicit policy forecasts stay attached to queued requests. The existing
global median is selected/refreshed at queue-head admission instead of becoming
a cached request-specific value. FIFO ranking,actual48GiB accounting,watchdog,
exclusive retries,deadlines,cache/source/verdict and public APIs are unchanged.
No new predictor or scheduling/failure mechanism is added.

A deterministic engine fixture first queues five unknown jobs under median60,
then lowers the observed median with two completed peak1jobs. The last three
must become concurrent within the same100budget/three virtualslots. This tests
actual engine admissions/completions rather than asserting a helper's own output.
It has cleanup even if the old serializing behavior regresses. It is not Lean
or measured native throughput. An old-behavior negative control is retained
separately;its observed result is appended after actual completion.

The fixed source passes56workspace tests/doctest,clippy with warnings denied,
andfmt. Four actualLean tests remain locallyignored while preserving the sole
native collection;native CI is separate. Combined existinggroup/helper sampled
peak6,386,573,312B,no helper pressure abort/monitor error. Supporting CPU10–11
tests/builds are disclosed contention on the old nonfinal FIFOpoint.

The retrospective singleton partition does not show a thousands-of-seconds
conservative-forecast effect. This warm queued-batch bug is a separate real
resource defect,not asserted as the explanation for the historical45%.
Representative full4warm parity and allsource outcomes still need actual matched
measurement. Do not delete mandatory exclusive retries to improve utilization.
Root-only self-review,not independent audit or a performance acceptance verdict.

The same regression is also run with only the original stale-fallback block
restored temporarily in the owned uncommitted source. It fails the intended
concurrency assertion after2s;its rawsource/command/output remain. The fixed
source is byte-restored in finally without any Git history change,then the
exact targeted test passes again. This is an observed old-behavior negative
control,not an assertion that it would fail. The existing native executable
is never changed by this control. A fresh release build succeeds afterward.
