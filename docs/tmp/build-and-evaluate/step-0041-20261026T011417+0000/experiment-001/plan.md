# Preserve upstream source-compiler context for the next workload

The original lean-mlir root uses --tstack=400000. The current NativeLean
always invokes --json --stdin and has no way to preserve upstream argv.
Implement an optional with_args builder without adding fields to the existing
public struct,keep default behavior/identity,partition nonempty argv in backend
identity,forward exact tokens,and expose repeated --lean-arg in the CLI.
Do not add flags by default or change active fullrun/binary/upstream source.

Meaningful process fixture captures exact argv and UTF8/CRLF stdin,including
an argument with spaces. Exercise public backend and executable Capture,
identity separation,default compatibility and full child retirement.
These are transporttests,not real Lean differential evidence. No new native
workload may overlap the active full7808pair. Build/tests in the owning
Workspace use only CPUs10–11 and retain combined owned RSS observations.
Actual lean-mlir raw/native differential remains after fullpair as userorders.

The existing ignored native-source differential now also compares raw native
--tstack=400000 --json --stdin with the configured backend for an accepted and
a rejected Init proof, and verifies retirement. Compile locally; execute only
in existing pinned-native CI, without another Workspace native acquisition.
