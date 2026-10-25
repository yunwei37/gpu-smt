# Complete 480-source failure profile — root self-review

Observed 2026-10-25 07:08:54 UTC terminal; all 480 selected original slow failures
returned, all have actual body-boundary observations, and every original status
is unchanged: 355 lean_error, 83 timeout_error, 42 resource_failure. This run contains
no accepted candidates, so it does not validate whole-population acceptance preservation.

The 83 original timeouts spend an estimated 24810.117616 sampled endpoint-weighted
thread CPU seconds in observed intervals. interval_cases accounts for 13692.704229 s
(55.19%), simp_all for 6998.012502 s (28.21%). These percentages use observed
timeout thread CPU, not total miniF2F wall time. Combined they dominate the sampled
timeout work; nlinarith accounts for only 6.001381 s in this timeout cohort.
Across the 355 ordinary errors, simp_all accounts for 2466.245399 s
(48.65% of their 5069.301003 sampled seconds), followed by nlinarith 1064.083660 s.
For the 42 resource failures, eqRefl accounts for 2769.189048 s of 3791.242442
sampled seconds. This narrows the first direction to actual finite case construction,
simplifier repetition, and definitional reduction rather than numerical LP.

The stock boundary counters independently place intervalCases exclusive CPU at
10657.589777 s and simp at 9235.109871 s over all selected failures. They are a
different decomposition: typeclass work nested under intervalCases is separated
by child subtraction. Do not add inclusive tactic and child spans.
Per-source.csv/JSON retain all 480 source IDs, baseline/profile statuses, missing
body clocks, top boundaries and named component observations.

Whole owned lifecycle = 17333.487669261 s, includes warmup,
startup and retirement. Cumulative per-request HTTP: baseline 34602.439199711 s,
profile 34643.101644578 s (+0.117513%). These are overlapping envelopes under two
workers, and the baseline came from the earlier full cohort, not a newly matched
480-source control. Available returned body clocks sum 30298.268678/30298.694177 s;
the 42 resource body clocks are absent. No zero-overhead or Amdahl inference is made.
Preparation of independent code-verification dependencies and offline analysis
overlapped portions of the run; their timing/aggregate-memory receipts are retained
in the corresponding artifacts. Shared-node contention was not measured away.

Memory: peak sampled owned tree 47774306304 bytes
(44.493 GiB), max 2 REPLs, each 24 GiB address-space limit, 17331 one-second
samples, zero watchdog kills/errors, all descendants retired. The watchdog is
sampled response, not a kernel hard RSS quota. Existing address-space failures
remain failures, not missing or zero-time work.

Raw snapshot streams retain termination without gzip trailer after process
retirement. The reader salvages complete JSON records and reports stream closure,
partial bytes, final open frames and 457 source transition intervals. Sampler,
table truncation, dropped-key, frame overflow and clock-error maxima are all zero.
126 snapshots have unknown source ownership; warmup is separately named and not
silently assigned to a candidate. Thread CPU in final open frames ends at the
last observation, so it is censored.

Next implementation: inspect the actual interval_cases and simp_all hotspots for
a sufficient failure witness. A branch-count heuristic, an expensive prefix, a
source-token pattern or a shorter timeout does not prove failure. Keep native
fallback when a sufficient witness cannot be established; test full accepted-ID
parity once a mechanism exists. This is continuing work, with no improvement
gate, deadline or closure. CPU oracle remains frozen and is not revived.

Review method: this thread reran the analyzer, checked all IDs/statuses against
the fixed selection and terminal, compared named versus sampled decompositions,
and inspected memory/stream diagnostics. This is self-review, not independent audit.
