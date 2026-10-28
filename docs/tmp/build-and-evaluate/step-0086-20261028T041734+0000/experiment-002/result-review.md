# Monitor repair self-review

The implementation now strictly revalidates known owned descendants and prunes
confirmed retired/reused identities before following new child links. Live
identities are kept without requiring the old parent link;sampling errors
propagate. This removes historical stale entries while retaining accounting
across reparenting. No new cap,reservation,scheduler,daemon or worker limit.

Two actual helper-process tests cover retirement pruning and live/wrong-birth
retention. The first workspace run passes these but an existing watchdog fixture
requires two eligible CPUs and fails under the single-CPU supporting build mask.
The next run supplies CPUs10–11,but catches a new test race:successful exec can
precede the first resident-page fault. Synchronize the owned helper's readiness
instead of assuming initial RSS>0. Both failed outputs are preserved. Neither is
hidden as a pass nor repaired by changing the existing resource contract.

Final qualified run:55tests including one doctest pass;four pinned-native Lean
tests explicitly remain ignored locally. Real process watchdog preemption/reap/
exclusive retry test passes. Workspace clippy with warnings denied and format
check pass. Maximum combined oldgroup/helper sampled RSS49,852,178,432B,
no pressure abort/monitor error. Supporting tests use CPUs10–11 inside the same
four-core allowance and therefore add disclosed contention to the running cell.
All fixture processes/commands are waited/reaped.

The source fix is validated as an accounting regression repair,not as a measured
whole-verification speedup. No native population/4warm comparison is complete for
this revision;the active cell uses its original8045cca executable unchanged.
Self-review only,not independent auditing.
