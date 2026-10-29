# PVC output regression

The user explicitly requires capture outputs on the existing PVC and a script
check after ephemeral-storage eviction. Scope:the active state-reuse collector's
output validation,nearby Python tests and durability documentation. No native
logic/resource-point change,hardware mutation,second collector or new service.

Resolve the output path before creating files,importing optional process
support,binding CPUs or launching Lean. Require containment in the existing
/workspaces mount and the same filesystem device;reject symlink escapes and
nested different filesystems. This checks declared Workspace-volume placement,
not persistence guarantees/backups against all storage failures.

A main-entry regression must show rejection before affinity/subprocess work;
retain its failing result before implementation. Boundary tests exercise valid
nonexistent descendants,unmounted root,outside/symlink/prefix escapes and
another device. Tests use simulated mount boundaries,clearly separated from
actual G10 path/CLI checks. Run the existing Python suite on G10;no formal Lean
capture. The earlier resource/hardware approval remains pending.
