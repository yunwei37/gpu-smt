# Plan review — self-review

The user directly requests the output check. Existing /workspaces is the
declared Coder PVC mount;confirm mount/path/device rather than string prefixes.
Canonicalize --out so an alias is not later used as a misleading destination.
Do this before optional psutil import,affinity,directory creation or subprocess.
No bypass flag,new storage backend or production-engine location policy.

7 regressions cover real main-entry ordering plus filesystem boundaries.
Mocked mount/device tests are distinguished from actual filesystem checks.
The helper does not certify a Kubernetes PVC identity in arbitrary containers,
crash consistency,backups or adversarial mount changes. The owning Workspace's
actual PVC mount remains the externally verified context. No formal Lean run.
