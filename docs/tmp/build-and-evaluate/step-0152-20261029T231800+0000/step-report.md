# Step0152 — read-only own-child signal diagnosis

BUILD_AND_EVALUATE; root only; operational dependency, not research evidence.

## EXPERIMENT_GATE
Two finite Python children only read process metadata, print JSON and exit0.
No kill/killpg, security mutation or Lean launch occurred. Parent and children
have UID/GID0, CAP_KILL, Seccomp0, NoNewPrivs0, the same user/PID/mount/cgroup
namespaces and cgroup0::/. A new session changes PGID/SID only.
All effective labels are cri-containerd.apparmor.d//&unconfined (enforce).
Raw snapshots and filtered runtime/Pod fields are in experiment-001/.

Owning Pod UID50c30780-d682-44ec-8471-1107dd8d2e70 is on g10; hostPID unset,
empty podSecurityContext. Dev is not privileged, permits privilege escalation
and has no explicit AppArmor/seccomp override or relevant annotation.
CRI of the SAME dev container records base cri-containerd.apparmor.d, no OCI
seccomp filter, UID/GID0 and CAP_KILL, in the owning Pod's besteffort slice.
Observed containerd version: v2.3.2-k3s2.

Earlier kernel audit retained in step0149 explicitly denied signal send from the
base AppArmor profile to the stacked peer. That historical host audit PID was
not independently mapped to the exact earlier namespace caller. The actual
earlier guarded exception was errno13/EACCES, not errno1/EPERM.

## Disposition
Evidence points to AppArmor stacked-peer mediation, rather than UID/capability,
seccomp, PID namespace or cgroup separation of our children.
Official [issue12886](https://github.com/containerd/containerd/issues/12886)
describes the precise base/stacked peer mismatch; the upstream
[fix commit](https://github.com/containerd/containerd/commit/2e3ace04afcd313db009b4028a067521cc06882c)
also documents root failing to signal its own child in an exec session.
This is a mechanism inference grounded in audit/runtime and primary sources.
Complete active compiled rules were not dumped; exact earlier-call attribution
and whether this K3s build includes the fix remain unverified.
No patch or security change was attempted.

The cluster helper intermittently failed readiness before exec. Existing G10 SSH
returned /readyz=ok; runtime reads used that existing path. Process reads used
CRI exec in the SAME owning dev container, with no replacement environment.

## WRITE_GATE
Keep native collection off until signalling is qualified. Record errno and
attribution limits, without paper performance/cache coverage changes. Continue
explicitly authorized default-off engine cache integration and pure Rust tests.

## REVIEW_GATE — same-thread self-review
Compared effective process fields with actual runtime/Pod fields. No AppArmor,
seccomp, permission, schedule, quota, Workspace or other security change.
All cluster CronJobs untouched, including no manual trigger. No signal or Lean
collection. Both finite children retired. No native replay or throughput claim.
