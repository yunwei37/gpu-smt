# Two-sided numerical oracle: discharge negative searches exactly

Root sole executor/self-review. Preserve original Lean/GPU/SMT fourRQs and
OSDI systems goal. Current complete native/HiGHS result1.49425x is one pair,
not stability or closure. HiGHS LP wall sums7.295s,but1,214negative exact race
decisions sum177.756s. These overlapping decisions include process/repair
costs;the opportunity is failed searches,not simply faster positive LPs.

Return both positive coefficient supports and dual rays certifying primal LP
infeasibility. For A*mu=b,mu>=0,a rational y with A^T*y>=0 and b^T*y<0
rules out a feasible coefficient vector. The existing certificate-space LP
includes the constant atom and the strict-normalization row. Its per-column
positive integer scaling is undone exactly during validation:for columnj,
sum(c_jr*y_r)+strict_j*scale_j*y_norm>=0,and y_norm<0.
This matches the pinned verifier's identicallyzero sum plus a positive strict
weight;the native injected -1<0 handles constant slack. No floating
infeasibility verdict is trusted.

HiGHS getDualRay may solve again without presolve;charge all its time.
First reconstruct rationals using the existing num-rational approximation
routine,then verify every original exact coefficient. If reconstruction or any
inequality fails,retain the exact CPU shadow and native fallback. The numerical
worker returns the rational certificate,which the parent verifies again before
accepting a negative result and cancelling/reaping the shadow. Failed or missing
rays never change native search outcomes. Native Lean remains proof authority.

The existing GPU phase-I tableau can return a dual candidate at positive
optimal artificial cost;apply the original row/column transformation before
exact CPU validation. Each model remains independently cancellable in real
cross-source batches. CPU-only dual capability is a baseline/control,not GPU
speedup or novelty. A surviving systems contribution must be evaluated beyond
using HiGHS/Farkas certificates,which are established prior work.

Freeze ten candidates by greatest measured negative exact-decision cost in the
complete HiGHS run,retaining original input order. They are inspected diagnostic
sources,not a fresh headline subset. Compare native,success-only HiGHS and
two-sided HiGHS at max8tasks/eight nativequeues,CPU8-11,48GiB,same imports/
heartbeats/full cleanup. Qualified complete-cost improvement admits the same
original1000source cohort. GPU implementation uses the same selected10 and
strong CPUtwo-sided control before any fullGPU run. Retain every failed ray,
source response,warning,LP outcome,winner and CPU/kernel retirement.
No new deadline,iteration grid,resource quota or competing schedule.

Source grounding:
https://ergo-code.github.io/HiGHS/dev/interfaces/c_api/#Highs_getDualRay
The pinned verify.rs explicitly requires exact zero across all atoms and at
least one strict hypothesis. This is a prototype within the existing RQ,not
a new theorem,independent audit or claimed accepted paper contribution.

## First real preflight and numerical reconstruction repair
Native28.576s,success-onlyHiGHS40.845s,two-sided41.428s,all10complete.
128actualdualraysreturn,butnonefinishasvalidatednegativecertificates.
The library approximation defaults target1e-19relativeaccuracy;noisy near-unit
ray entries become large-denominator fractions rather than the intended simple
rational. Replace this with continued-fraction reconstruction to1e-9relative
nearness,thenretainexactBigIntverificationofeverycolumn. The approximation
tolerance isnot an acceptance tolerance;all failed rays stillfall back.
Preservefirstsource/raw. Rerunthissamesubsetafterthe actual engagement repair,
not a fullmatrix or parameter sweep. No scientific hypothesis/scope change.
