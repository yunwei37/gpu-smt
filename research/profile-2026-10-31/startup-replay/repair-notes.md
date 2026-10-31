# Repairing failed kernel replay measurements
## Cause (self-review)
All 28 target and 13 zero-declaration controls failed before kernel replay:
their stderr says "Could not find any oleans for: MODULE". The bundled checker
is exactly the tool in Lean 4.34.1. In that release LeanChecker.lean enumerates
olean files, then searchModuleNameOfFileName calls moduleNameOfFileName.
Lean/Util/Path.lean first calls IO.FS.realPath on the candidate file and rejects
it unless it is contained in a search-root realpath.
Our former symlink union pointed outside every listed search root, so the
enumerator silently discarded those entries. Ordinary Lean import lookup did
not make that reverse filename-to-module check, explaining why compilation
succeeded with the same dependency view. --fresh changes replay scope; it
does not repair this path-enumeration failure. Unknown -j8 was not needed
and is removed; runtime threading is recorded via LEAN_NUM_THREADS=8.

## Correction and retained evidence
The v2 raw directory and all failed CSVs/reports remain unchanged. No failed
run duration is a replay-cost denominator. A new repair-v3 directory on PVC
contains 1,079 ordinary hardlinks (about 1,591 MiB logical artifact bytes, no
extra data-copy allocation), at the same correctly named paths under a real
search root. Dependencies remain unchanged. Each of the 15 requested target
names matches exactly one path in this artifact view. LEAN_SYSROOT and PATH
both explicitly point to the matching 4.34.1 distribution.

## Locked execution
Before submission /proc/locks showed holder37246 and existing waiter11027
(the M matrix). The correction joined with one blocking flock acquisition
after that waiter; it never attempts nonblocking acquisition or repeated
reacquisition. Actual acquisition identity/order is captured in launch.json.
The first actual run is NearPinDeletion import-relative replay. Only an exit0
with the exact "replaying MODULE" output enables the target matrix.
The matrix contains the 13 previously paired short modules plus Grid and
Amplitudes. Scope controls compare import-relative and --fresh for
Init.Data.Nat.Basic and Mathlib.Data.Nat.Basic, plus --fresh NearPinDeletion.
Each process has a time bound, the whole locked block has a 1,700-second
internal deadline, and external timeout1750 is retained. Actual tree RSS is
sampled every100ms with 128MiB reserved for the small parent inside the
12GiB O allocation. The standard checker has no Lean -M memory option;
no ignored memory flag is presented as enforcement.
Timeout or memory-censored cells are reported explicitly, never given a
success ratio. Historical Grid/Amplitudes build ratios remain separately
labelled from the thirteen matched-current build denominators.
Raw root: /workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3 .

## Functional control actually completed
On E cores16-19, without recording elapsed time or a performance profile,
stock leanchecker announced NearPinDeletion and exited0 with empty stderr.
The bounded child naturally exited; no memory interruption occurred.
functional-preflight.json/stdout/stderr on PVC preserve the exact invocation.
This qualifies path repair only, not any timing result. The formal P-core
matrix remains queued and begins with its own timed preflight.
