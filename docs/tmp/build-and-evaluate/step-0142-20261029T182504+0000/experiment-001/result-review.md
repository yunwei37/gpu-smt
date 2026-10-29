# Result review — requested PVC capture-output check

Before-fix main-entry regression failed because CPU binding was reached before
invalid temporary output was rejected. The raw failure is retained.
The corrected collector resolves --out,requires containment within the existing
/workspaces mount and checks its nearest existing ancestor's device against
that mount. Invalid output raises argparse exit2 before optional process support,
affinity,directory creation or native execution.

7 storage regressions pass;the complete existing Python suite now68/68 passes
on G10 CPUs6–7. This is development testing authorized by the latest user request,
not a change to the CPU8–11/48GiB native measurement point. Child ru_maxrss was
116796KiB for this test session;it is not an aggregate process-tree high-water.

Actual G10 positive check created/read a marker on the PVC with matching device.
A real CLI call through a symlink escaping to/tmp exited2 without creating output.
Temporary probe directories were cleaned. No Lean subprocess,formal collection,
Workspace placement,quota,permission or other project was changed.

The active code adds one14-line helper and its early call;7 tests use the
existing Python test module and existing CI discovery. The matching Lean/C
modules,continuation planner and input/context/results are unchanged. No bypass
or new service. The prepared next collector snapshot must include this check;
historical frozen sources and failed archives remain untouched.

The lesson records measured container total vs user-reported/tmp attribution
without inventing a per-directory du breakdown. PVC placement is not a backup
or a hard crash-persistence guarantee. No scientific hit/cost/novelty claim.
Root self-review,not independent audit.
