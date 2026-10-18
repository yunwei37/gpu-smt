# Reversed-order replication of the two-sided result

Admission: complete fresh 1,000-source ratio 1.502158368x, only 0.652560606s
candidate margin above the 1.5x boundary, is insufficiently stable.
Question: does the same complete pipeline remain above 1.5x when acquired
before the native reference? Freeze implementation, original source order,
width8 native contiguous queues, CPU0–3, 48GiB, imports/heartbeats and all
preparation/repair/fallback/retirement. Run two-sided CPU HiGHS first and
native second. No parameter change, no GPU warmup, no resource enlargement.
Retain every native response and raw failure; compare exact IDs, verdict,
non-message JSON, timing scope and 1%/10% native-selected tails. Message changes
remain disclosed. Publish this pair regardless of result, with its own
reference; never select a denominator from another run or average ratios into
a confidence interval. No agent delegation or full GPU admission.
