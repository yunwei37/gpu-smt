# Additional closest-work verification — same-thread self-review

2026-10-30UTC. Follow-up queries:"theorem proving cache failed tactics timeouts
resource limits memoization Lean";"constraint solver caching timeout results
monotonic resource budget". No competitor is built or run.

LeanGraphSearch,arXiv2610.22339v1,submitted2026-10-15:
https://arxiv.org/html/2610.22339v1#A2.SS4 .
Primary appendixB.4 says an unchanged candidate with a cached deterministic
failure avoids another compilation,and infrastructure failures are excluded.
Its failure memory is problem-scoped and guides a generation/refinement loop.
This is direct overlap for generic deterministic-failure caching. It is not
evidence of our complete failed-state/diagnostic/heartbeat transition replay,
nor a proof that aggregate-RSS preemption can be cached as monotone rejection.
No claim of first failure caching is supportable.

Rognvaldsson,Sun,Dekoninck,Vechev,arXiv2606.04883v3:
https://arxiv.org/abs/2606.04883 .
The primary abstract describes observing failed Lean attempts and predicting
success/cost to choose between continuing a target and a new decomposition.
History-based cost-aware theorem-proving control is therefore prior work.
It changes generation/search;our exact finite candidate consumer cannot skip
every remaining candidate on an observed-unsolved task based on predicted reward.

SAW's official manual was also checked:
https://galoisinc.github.io/saw-script/master/saw-user-manual/interactive-proofs.html .
It documents solver-result caching and backend-version distinctions. This was
not treated as evidence of cross-budget timeout or RSS-failure monotonicity.
No unrelated code or competitor experiments were added.

Disposition:no existing-data result here establishes novel end-to-end benefit
for the proposed resource cache or new ordering/restart heuristic. The original
four RQs/directions stay active;this scopes claims rather than closing research.
