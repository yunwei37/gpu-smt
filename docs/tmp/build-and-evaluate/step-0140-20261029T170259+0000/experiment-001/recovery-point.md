# Durable recovery preparation — not launched

Restored original data and frozen source at:
/workspaces/.agent-state/gpu-smt-captures/state-reuse-recovery-20261029T165905Z

The57 archived files expanded byte-for-byte from existing gzip archives;
no old archived/native record was rewritten. Original8031 cells and2640 ledger
rows are retained. The existing aee0932 continuation planner reproduced5390
pending cells,5 deferred solo retries, and one derived old Nat.pow operational
failure with unknown elapsed. This dry run executed no Lean candidate.

Native modules in the evicted writable layer must be rebuilt from the retained
qualified source. No native compilation/measurement is launched on G10:
its visible CPUs are0–7 and total host RAM is29,177,340KiB, whereas the approved
point uses CPUs8–11/48GiB. This is not a new valid resource point or permission
to alter CPU IDs silently. Existing dependency paths/PVC remain preserved.

Use the current Workspace and existing PVC. Put resumed raw/source/module
outputs under this PVC-backed agent-state directory,not container/tmp.
Do not restore stale native PID identities or treat reconstructed metadata as
fresh native results. No auto queue or second collection was created.
