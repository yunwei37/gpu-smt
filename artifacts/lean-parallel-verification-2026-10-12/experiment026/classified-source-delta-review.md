# Native miss-context cost reanalysis

Reused the completed original E015 classified archive; no new timing run.
Paired native frontend-begin/complete counter snapshots for5951sources;
one original operational source has no complete snapshot and remains censored.
All paired counters are monotone. These are native expensive-WHNF-miss scopes
after easy traversal/cache lookup, measured by exclusive calling-thread CPU
with nested child scopes subtracted.

Observed complete-pair exclusive CPU:369.605477s.
No expression-metavariable/free-variable/custom-unfold/level-metavariable flags:
97.576700s. The complementary flagged union is272.028777s
(73.600% of this observed miss-scope CPU only).
Expression metavariable, free-variable and level-metavariable marginals overlap;
joint masks are retained. A zero flag set is not a GPU-eligibility or cache-safety
certificate. These figures are not whole-verification CPU/wall fractions, a GPU
ceiling or an uninstrumented performance comparison.

Decision: a context-blind closed-fragment reducer omits much of the observed
miss computation. Broader offload needs genuine native context/continuation
handling and a strong CPU implementation comparison; repeated tiny beta
optimization cannot be promoted to full Lean acceleration. The new official
diagnostic source-coverage results identify common projection families, while
these prior counters identify their missing contextual boundary. Neither alone
attributes CPU cost to a particular displayed declaration.

Next decisive implementation discriminator remains actual cost/context for
common projection/instance paths, with current official dependency-aware
native caches as competing mechanisms. All RQs and complete source-native/GPU
scope remain open. Direct root reanalysis; no independent reviewer is claimed.
