# Ordered admission result — root self-review

The original controlled regression fails on the pre-repair engine: actual
execution is late/early. The source is unchanged and the repaired result is
early/late. Full workspace validation passes29ordinary tests;2real-native tests
remain locally ignored to preserve the sole active native collection.

The second regression couples two physical starts around unused cache/coalesced
queue tickets and completes successfully, so unused subscriber slots do not
silently serialize available CPU capacity. Existing resource preemption/requeue,
exclusive exhaustion, RL sharing and full-retirement tests also pass.

Raw before/after receipts and source snapshots are in
artifacts/engine-queue-order-2026-10-25. Validation logs are in
artifacts/rust-engine-2026-10-25/validation-20261025T104731.
These are dependency semantics, not a native performance or full RQ result.
Actual exact-head CI must still run after the forward push.
