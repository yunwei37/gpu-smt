# Original LeanMLIR library prerequisites

Continue direction 3 while the sole retained candidate group runs first-original.
The native-parser graph contains 37 LeanMLIR library prerequisites, 20 SSA
prerequisites, and the actual bv_decide workload root. Build only the first 37
in the original LeanMLIR package, pinned SDK and unchanged original manifest.
Reuse already compiled external packages through temporary path links only
when their Git revisions match the original manifest. Preserve old 802-module
setup and source graph; no comparison system, CPU oracle, workload-root run,
or new candidate collection.

Use source topological order and original native Lake module facets. Before
each library leaf, Lake --no-build checks dependencies: a missing/stale facet
fails preparation rather than spawning a large unbudgeted rebuild. Compile on
CPU11, monitor combined old-owner plus new tree RSS every second, stop only
the new setup on 48GiB pressure. Preserve all commands, actual logs, partial
failures and sampled memory. Old run stays frozen at its original point.
This source compilation is prerequisite preparation, not bv_decide timing.

Success here only means these 37 prerequisite olean targets build. It does not
complete the remaining SSA prerequisites, candidate workload, COW children,
throughput pairs or paper evaluation. Self-review actual native outputs and
dependency versions; do not report dependency-only time as verification gain.
