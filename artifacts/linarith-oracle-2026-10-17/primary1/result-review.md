# First complete heavy-cohort pair — root self-review

Reference2282.741330131s; corrected direct oracle1694.374646240s.
Observed speedup1.347247100986x and whole-time reduction25.77%.
This first observation misses the predeclared1.5xthreshold. The remaining
paired observations and diagnostics still run. No final gate decision,
stable speedup, global strongest-baseline result or venue readiness follows.

Both methods execute all1000original sources in the frozen original order.
Native outcomes match per source:992complete/8rejected, zero operational.
Normal native EOF/exit0 is recorded in both.88complete-source responses have
different unused-variable warnings, including changed warning positions/counts.
After classifying just those warnings, allother native response fields match.
Original responses remain unnormalized and unchanged; do not claim bytewise
or complete-diagnostic transparency. Different checked proof construction can
use a different hypothesis subset, which is consistent with these linter changes.

Both whole clocks include native setup, full source verification, collector
capture/resource observation and retirement. Separate diagnostic logs are off.
Observed collectorCPU is312.537590sreference and224.174179sprototype.
The common one-second process-memory observer is part of these measurements,
so ratios do not isolate performance without that observer or an observer-free
causal verifier effect. Captured waited-child CPU is2075.141985sreference and
1717.720833sprototype, without exhaustive external-grandchild accounting.

Prototype peak sampled PSS4,344,808,448bytes vsreference8,724,948,992bytes,
with3incomplete reads vs0. Single non-atomic profiles do not establish exact,
replicated memory savings. Offline batch P95=18.5066s vs25.8451s; shared
batch waits are not individual proof times or online SLOs.

Reference uses the same executed Fast/hybrid/product code, but the common
library was built before the unused oracle fallback branch was corrected.
That complete reference is reused rather than rerun. Later pairs load the
same corrected common library in both methods. Different capture epochs and
shared background remain important limitations; final analysis reports allpairs.

This is native CPU polynomial/product/LP/certificate work with strongfallback.
No GPU work or GPU acceleration is asserted. Root both authored and reviewed.


The manuscript includes this first observation with its pending repetitions,
warning differences and observer scope. Tectonic0.17.0 exits0 and produces
18pages. Updated page12is rendered with Poppler and visually checked without
clipping or overlapping text. This is a finite source/result writeup and root
self-review, not full WRITE/REVIEW completion or independent auditing.
