# Default build is not all released source

Pinned openai/math4eaee875. Static import reachability is computed from
module OAI with the publisher's srcDir overrides, then joined to original
per-file token metrics. **No additional native invocation.**

| Scope | Modules | Source bytes | decide+kernel lexical occurrences |
|---|---:|---:|---:|
| All released .lean source |163,097|1,785,499,363|1,354,379|
| Default OAI-root import closure |130,834|1,397,800,941|903,371|
| Outside default root |32,263|387,698,422|451,008|

The omitted domain contains33.30%of lexical decide+kernel occurrences.
All562PlanarPacking modules (255,199occurrences) and all466Transonic
modules (193,076occurrences) lie outside this default root at the pin.
Their explicit sample builds are valid workload extensions; their costs
must not be silently attributed to plain default-root compilation.
Source tokens are not runtime calls, cache misses or CPU fractions.

scope-comparison.csv records exact joined counts. outside-projects.csv
ranks omitted directory groups by kernel-token count; these groups are not
independent Lake projects. probability-target-domain.csv annotates the
fixed42random draws without changing their selection or weights.

## CPU inference scope

The primary SRS frame samples all163,097modules.
For a default-root domain total under that frame, use response
z_i = y_i * I(module in default-root) with the **original all-source
inclusion probabilities**, rather than substituting130,834for N in each
old stratum. A known out-of-domain target contributes exact domain zero;
that does **not** mean a native zero-cost measurement or accepted proof.

At standard-artifact sampleA,26native costs are complete. Two additional
pending draws are known outside the root, so28domain responses are known,
not28native returns. Remaining14domain responses are unknown; full default
and all-source CPU totals/CI remain unavailable. Native run budgets,
cache/setup, memory and artifact assumptions remain those of each point.
No new global CI, walltime, parallelism or memory forecast is inferred here.
