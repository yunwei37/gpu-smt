# Completed retry-frontier24 measurement — root self-review

| Condition | External seconds | Accepted / rejected / timeout / resource |
|---|---:|---|
| Retained four-warm baseline | 1430.677580 | 14 / 7 / 1 / 2 |
| Previous engine | 1540.705220 | 14 / 5 / 3 / 2 |
| Retry-frontier engine | 1347.584488 | 14 / 5 / 3 / 2 |

The new run uses 12.534567% less elapsed time than the old engine and
5.807954% less than the retained warm reference. This is a selected 24-source
development comparison, with order, shared-host and earlier support-CPU
differences; it is not a representative or newly interleaved full benchmark.

All 24 raw outcomes equal the old engine's outcomes. The 14 accepted IDs also
equal warm's set. Sources 2507 and 7230 still time out where warm returns Lean
errors. This is not complete observable-behavior parity.

All 27 attempts and five watchdog actions count. All 28 registered native
births are gone and reaped. Peak sampled RSS is 51,876,397,056 bytes: the
one-second watchdog can overshoot, and is not a kernel quota. One prepared
parent replaces the old two. Candidate 7230 starts at 11:07:37, before the first
exclusive retry at 11:12:38. This establishes actual queue-frontier engagement;
it does not imply that the full exclusive-checking cost disappears.

The retained Frontend and ordinary runCommand sources are equal between the
stock and prefix trees; dormant proof-step/batch extensions are not called.
This limited audit neither proves runtime equivalence nor explains the two
timeouts. A separate source inconsistency is testable: PreparedRepl includes
retirement waiting in its response deadline, whereas NativeRepl retains a
completed reply and then charges retirement. A delayed-retirement control is
the next narrow correctness experiment. Do not claim that it caused 2507/7230.

All raw inputs, responses, failed attempts, clocks, contexts and resource logs
are retained. Archive replay executes zero native candidates. Full7808 and the
corrected fixed42 rerun remain open. Review is root self-review, not independent
auditing; the four RQs and original research objective remain unchanged.

See comparison.json and ingestion.json. Run python3 analyze.py to replay against the adjacent retained reference artifact.
