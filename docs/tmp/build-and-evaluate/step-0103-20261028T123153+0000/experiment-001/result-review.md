# Exact median maintenance result — root self-review

Sourcebf4eb8c replaces history clone/sort at each admission query with two
incremental heaps. All values and the exact sorted index n/2 are preserved.
The old sorted definition is the every-prefix test oracle.66 workspace tests
pass,including new equivalence and old falling-forecast/concurrency controls.
Five actual pinned native differential/lifecycle tests pass separately.
CI40688762011 and smoke40688762081 finish successfully; full raw logs are kept.

This verifies an engineering boundary. Runtime savings,48GiB safety beyond
the declared sampling contract,full Mathlib equality and scientific novelty
are not established by these tests. Heap storage is still O(n). No percentile,
policy,resource setting or workload method changed. Full7808 remains the
already-frozen13d4606 one-group measurement,not an A/B for this later change.

Daily cleanup also updates public completed/running status,the actual36-page
draft label,and the obsolete continuation's scope.74 relative entry-document
targets exist; external URL availability and anchor coverage were not audited.
No author/failed data or frozen arithmetic-oracle code was changed.
