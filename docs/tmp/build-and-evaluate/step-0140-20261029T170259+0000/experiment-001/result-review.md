# Result review — external eviction and recovery

The actual Kubernetes event at16:05:43UTC is Evicted for ephemeral-storage.
The dev container exited0 at16:05:44UTC; this is not a successful experiment
terminal. The same Workspace ReplicaSet recreated its Pod onG10 with the same
PVC claims. /workspaces/repository remains main/ed01cca and foreign dirty paths
remain untouched. Current native process inventory is empty.

At14:24:40UTC the former run had3914 ledger rows and no client-exit/terminal.
Only2640 rows are durably archived. One later derived old panic row remains
reconstructable;at least1273 newly recorded ledger entries are currently
unavailable,plus any not observed between14:24 and eviction. The exact final
count,outcomes,observer reachability and memory trace for the lost phase are
unknown. No zero-match result or candidate semantic failure follows.

The old container ID is absent from containerd. A read-only probe of visible
overlay snapshots found no old active-pointer file;no deleted-byte forensic
recovery,permanent-loss proof or other Workspace modification is claimed.
The prior/tmp choice failed to preserve incremental data across replacement;
the root acknowledges that storage choice and restores only proven archives.

Existing continuation planner dry-run:8031 inputs/2640 retained rows,5390
pending cells,5 deferred resource retries,1 explicit derived old operational
failure. A new durable preparation uses the existing Workspace PVC. No Lean
native launch,compile or actual system performance test occurs onG10.

The current node cannot satisfy CPUs8–11 and has less than48GiB totalRAM.
Returning the existing Workspace tolab changes its current scheduler selector;
no such change was made. A concrete temporary-placement proposal is recorded
for operator approval under spark-manage AGENTS.md§2.3. All recovery work that
does not require that mutation is completed. Real source/modules must be
qualified/rebuilt and native collection resumed only at the approved point.

The prior ed01cca CI actually completed successfully:engine40891000453
(rust and native-repl-contract) and benchmark-smoke40891000393.
Those correctness checks do not restore missing research data or prove gain.
