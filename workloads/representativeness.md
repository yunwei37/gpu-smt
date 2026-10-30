# Cost concentration versus failure frequency

AutoVerus direct native records contain3,566 candidates per repetition.
Top58 candidates (ceil1.6%) use3.399%,3.338%,3.315% of each repetition's
summed process elapsed. The tiny candidate tail consuming73% of Lean time
does not reproduce at this program-verification point.

This does not mean failed work is cheap in aggregate. Nonzero process exits
use94.99–95.02% of process elapsed:3,376/3,566 candidates exit nonzero.
JSON success=false alone uses91.92–91.97%. High failure frequency can
dominate cost without a concentrated slow-failure tail. None proves a
candidate was doomed before verification.

419 rows per repetition have JSON success=true but process exit1;17 exit101
rows have no native JSON verdict. Keep both axes in
[cross-tabulated cost](candidates/autoverus-outcome-time.csv) and original
receipts. Do not treat the JSON flag as whole-process acceptance or relabel
operational failures as tactic errors.

The denominator sums direct process elapsed per repetition, excluding capture
conditions and model generation; it is not batch wall or a hardware speedup.
No Verus rerun or verdict-changing intervention was performed.

[The earlier scenario gap audit](../docs/workloads-audit.md) remains linked.
This update stays under workloads/ per the latest W ownership restriction.
EPFL excludes timeout/operational failures, APRIL is a mutation distribution,
and successful-proof releases omit failed arrivals. None supplies uncensored
causal costs from labels or tactic tokens alone.
