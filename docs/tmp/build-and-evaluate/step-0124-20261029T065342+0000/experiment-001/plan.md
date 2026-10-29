# Complete retry-tail decomposition within RQ3

RQ3: How does prepared-state branching change end-to-end latency, throughput
and memory at equal resources compared with established warm-session reuse?

Reuse the existing complete7808pair;no new native run. This supporting
analysis asks whether the already-fixed ordinary-frontier-first mechanism
engages,or whether ordinary admission still leaves most allocated slots idle.
The answer changes which resource implementation needs attention. It does
not establish a new contribution or isolated queue-policy speedup.

Use all frozen13d4606 native registration/release events and all7850attempts.
Exclude the persistent prepared parent from candidate concurrency;otherwise
one parent appears as a candidate for the full ordinary phase. Attribute
birth-matched processes to each original ID/attempt and sweep the complete
declared lifecycle. Retain registration envelopes as such,not CPU or lease
occupancy. Compare against archived retry-frontier source/negative control/CI;
do not rerun tests or a second Lean capture while original42runs.

Missing/duplicate identity,unattributed attempt,ordinary work after the first
exclusive attempt,or more than four candidate envelopes invalidate the
corresponding interpretation. Preserve zero-root intervals as unattributed.
All data is already terminal;no preflight or new external baseline is needed.
The strongest alternative is a new queue-policy-only full A/B;that would be
redundant for basic engagement and cannot currently share the native slot.
The independent full native42result and own whole-module method remain next.

Command:
python3 artifacts/engine-resource-profile-2026-10-25/retry-tail-full7808-20261029/analyze.py
