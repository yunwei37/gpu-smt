# Official native WHNF cache comparison

Question: is E028's additional native-mode cache already implemented in official current source? Read entire source at immutable commit 153e01180e59305df575e24b803cf7416a251bcf; source date 2026-10-07T11:06:51Z. Source version is not automatically a release or an executed baseline.

https://raw.githubusercontent.com/leanprover/lean4/153e01180e59305df575e24b803cf7416a251bcf/src/Lean/Meta/WHNF.lean

Answer: official current WHNF.lean no longer restricts caching to default/all transparency; it uses mkExprConfigCacheKey and a unified cache.whnf map. E028 is therefore an older pinned-backend comparison candidate, not a new general caching mechanism. Any published claim of current-Lean acceleration requires a version-compatible current native baseline; this source inspection does not establish its speed or release membership. Keep measured4.9 workload findings scoped and preserve the broader system/GPU goal.
