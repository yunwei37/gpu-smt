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


## Versioned native samples and constructed training releases

[EPFL136 native returns](candidates/native-versioned/epfl-completed136/)
have12explicit budget returns,159.68/623.80s (25.60%). This is a completed
prefix, not the full144-source plan; the unresolved exact?-search candidate
is separately censored and excluded from that denominator.
[APRIL39pairs](candidates/native-versioned/april39/) supply78actual returns:
16mutation budget errors consume50.53% of unweighted selected-mutation time.
Budget-text oversampling changes the released-test inverse-inclusion weighted
ratio to11.05%, without a confidence interval. It is not a natural arrival log.

EPFL's4.84million-row training release contains250,000publisher synthetic
pairs, fallback-recovered inputs and explicit exclusions of infrastructure,
missing-declaration and invalid-without-error records.
[Construction audit](candidates/epfl-training-provenance/) attributes those
counters to the publisher. [First-group](candidates/epfl-training-rowgroup0/)
and [three-group](candidates/epfl-training-random3/) static scans have no
per-row native cost. Label/annotation agreement partly follows enforced
filtering, not independent semantic validation.

Native tail ratios cannot be transferred directly between these samples,
Verus and the older Lean1.6%/73% point. Each needs its own runtime denominator,
budget provenance, arrival distribution and censoring analysis.
