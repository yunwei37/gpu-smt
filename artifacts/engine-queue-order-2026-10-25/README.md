# Ordered-admission regression and repair

This is engine correctness/measurement-contract evidence, not a Lean speed result.

On implementation head ea2ea299f32d9dcefd1eb50e4f6f823c6a8f34d7 plus the new
regression fixture, a delayed first forecast allows actual execution order
late/early despite early/late submission. before-test.json and its raw compressed
log retain the real failure (exit101). engine-before.rs.gz and
regression-before.rs.gz preserve the exact pre-repair source/test.

The repair reserves ranked queue tickets before task execution and establishes
cache/in-flight sharing in that same order. Unused cache/coalesced tickets drop
immediately, and physical jobs retain ticket ownership through queueing.
No public trait signature or native acceptance rule changes. A separate coupled
start fixture checks that cache hits/shared subscribers cannot block the other
CPU slot. Existing preemption, cancellation/RL sharing and retirement tests run
as part of the workspace validation.

after-test.json/log retains the passing original regression. Full validation:
../rust-engine-2026-10-25/validation-20261025T104731/validation.json.
All29ordinary tests pass; the2real-native tests are explicitly skipped locally
while the original native group is active. Exact-head native CI remains the
next dependency check. No new native collection is started here.
