# M systime001 — usable PMU and bounded native setup

EXPERIMENT: perf hardware user/kernel events and trace summary actual controls
pass; owned-child TERM works. perf package/binary provenance retained on PVC.
Temporary15GiB same-Workspace-Pod cgroup control passes under P0–7 flock and is
removed; no host sysctl, module, other Pod or parent cgroup limit changed.
The affinity helper error and three failed imports under AS15GiB are preserved
and excluded. Corrected native setup has no AS cap and asserts P affinity.

WRITE: plan, preflight metadata, thin native/perf runner and result-analysis paths.
Source evidence identifies mimalloc and a getrusage-based native memory check;
cycle fractions/root cause still unknown. This is dependency completion,
not a scientific measurement result or a claim of3completed repeats.

REVIEW — 自审: UMoments9 plain triplet has a real queued controller7507
behind the W lock owner7216. No duplicate/native overlap started; no result
inferred from a state file. Full attribution and requested matrix remain open.
Only M systime paths changed. Overall goal active.
