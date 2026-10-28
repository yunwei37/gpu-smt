# Exact resource median maintenance — root source review

The previous goal turn is concrete progress: completed24 results, raw artifacts
and actual full7808 start, not an empty wait. The sole full pair remains source
13d4606; this source edit never replaces its frozen binary or warm program.

Finding: acquire's FIFO fallback cloned and sorted all completed positive RSS
observations while holding the admission-state lock, on every eligible query.
This work grows with request history and repeats on watchdog/admission wakes.
Its isolated runtime cost is unknown; no measured speedup is claimed.

Use two binary heaps to maintain exactly the same upper median: upper has
ceil(n/2) elements,lower floor(n/2),and every lower value is no greater than
every upper value. Reading upper.min equals sorted[n/2]. Insert is O(log n),
read O(1),storage O(n). No changed percentile,window,forecast,cap,policy,
watchdog cadence,timeout or resource point. Other prediction fallbacks and
resource retry logic remain byte-unchanged.

Tests compare every prefix against the previous sorted-history definition:
ascending,descending,repeated,zero/u64 extremes,mixed deterministic streams,
and the existing falling-fallback concurrency regression. These validate
semantic equivalence, not Lean correctness or end-to-end performance.
Do not spend the live paired benchmark's CPU budget compiling/running helpers:
existing CI performs source checks. Local native/runtime requalification is
deferred until this sole group retires if another measured version is needed.
This is maintenance of an existing resource layer, not scientific novelty.
