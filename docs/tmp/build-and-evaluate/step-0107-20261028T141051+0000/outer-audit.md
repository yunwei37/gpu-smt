# Step0107 root self-audit — queue wake coverage

Self-review by the executing root,not independent audit. No delegated Agent.
Existing Notify broadcast behavior is checked from actual source,not a claim
about measured whole-run cost. One private Notify per existing ticket changes
wake routing only;ordered keys,retry epochs,CPU/RSS checks/native execution
and result delivery keep their definitions.

Healthy resource changes wake the eligible head;removing/cancelling it wakes
the successor. Shutdown,monitor error and engine-RSS fatal release all pending
requests. Active cancellation and lease-retirement completion still use their
original paths. Stored permits prevent a pre-poll notification disappearing.

The actual private acquire-future controls cover7808waiters,lease handoff,
head cancellation and monitor-fault/shutdown termination. Their source is new
and CI is pending:neither successful compilation nor a passing test is yet
claimed. Fixtures do not prove end-to-end Lean speedup. The frozen full13d4606
native run is unchanged and will not measure this edit. No paper-level result
or independent audit is asserted;all four RQs remain open.
