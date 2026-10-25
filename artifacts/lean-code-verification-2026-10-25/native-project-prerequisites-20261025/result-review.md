# Root-context attempt — root self-review

All original root Git packages are now present at their recorded revisions.
The root context reveals another actual mismatch: its Cli55c3729 dependency is
different from Mathlib/subproject Cli d9fc8ae used by the earlier source resolver.
The explicit no-build check stops at LeanMLIR.Util before silently rebuilding
or mixing the wrong Cli. 15 project targets returned successfully; raw partial
results remain. This is a preparation/context failure, not a rejected proof.

Correct the source resolver to follow original root manifest locations/pins.
Actual native reparse still finds 860 modules with zero unresolved/collisions/
header errors, but assigns three Cli sources to the original root revision.
Build those three external-in-root prerequisites and 57 project prerequisites
in mixed native order, still excluding the candidate workload itself. Keep all
earlier graphs and 802-subproject setup as scope-limited evidence.
