# Bounded linarith/nlinarith oracle experiment

User decision, 2026-10-16 local / 2026-10-17 UTC. RQ4 remains unchanged. This is the decisive last admitted arithmetic mechanism test before the user-requested negative-result wrap-up, not a reopening of E038 or defeq/constructor GPU routes.

Hypothesis: exporting arithmetic assumptions once, doing untrusted polynomial/product/LP search outside Lean, then constructing only the selected certificate and checking it once, can remove enough native proof-producing preprocessing to exceed the strongest measured native CPU path by more than 1.5x end to end. Plain LP offload is insufficient and is not the proposed mechanism. Existing Farkas Fast probes and then re-runs stock preprocessing/LP; the new path must reuse the returned coefficient certificate without that second search.

Workload: 1,000 original GoedelWorkbook sources selected by highest recorded linarith leaf wall in the closed 29,750-source capture; selection.json preserves source association and rank. This deliberately enriched opportunity cohort is not a representative all-population speedup. Execute in original source order; include failed/rejected candidates.

First measure four nonoverlapping stages on the native baseline: preprocessing/linearization, nlinarith product generation, LP, certificate reconstruction/check. Distinguish on-thread CPU, invocation wall, sum of concurrent intervals and whole-run wall. Defeq/typeclass/ring are attribution inside those stages, not additional summable stages. Final kernel and service overhead remain in whole-run measurement. Profiling is separate from performance trials. Observer overhead is measured against uninstrumented native code.

Comparator: native-compiled warm Kimina in-process batch using existing official native protocol and compiled mathlib, plus the strongest applicable existing Fast/product-reuse hybrid or HiGHS composition as the alternative native competitor. No bytecode/cold baseline may determine success. Same sources, affinity, worker configuration and original verifier limits; publish exact commands/configs. No new full old CPU matrix. First use actual selected cases to qualify engagement/outcome agreement.

Prototype: export parsed assumption expressions/atoms once; external untrusted native process performs polynomial linearization, products and LP search, returning coefficients plus product provenance. Materialize only cited facts and check a single weighted contradiction via native ring/proof reconstruction (linear_combination equivalent). Unsupported cases, failed certificate reconstruction and oracle errors restore saved state and run the original path. Keep all fallback costs. Do not label the existing probe/restrict path as this prototype. GPU products are conditional on measured eligible work; RTX5090 is not a contribution by its presence.

Three balanced matched performance repetitions on the selected cohort, after a real matched preflight. Include startup/import preparation, export/packing, IPC, GPU transfers if any, queueing, native check, fallback, and normal cleanup/process exit in whole time; builds excluded/versioned. Primary ratio is fastest valid native baseline whole time / prototype whole time, with all native proof outcomes matching per source. Preserve warnings, errors and operational rows. Differences must be explained and repaired; fewer verified sources cannot count as speedup. Report all repetitions rather than best-case selection.

Predeclared user rule: continue this route as mainline only if the completed matched end-to-end comparison exceeds 1.5x with native outcome agreement, and state exactly what GPU did. Otherwise publish a negative-result conclusion and stop/delete gpu-smt-osdi hourly automation. A build/preflight failure is not a measured 1.5x result; preserve and repair the executable path.

Supporting RQ1/RQ3 measurement: on original miniF2F (7,808 candidates, 244 tasks) and ProofNet (5,952,186 tasks), quantify exact shared tactic prefixes among each task's 32 candidates, then run actual prefix-sharing validation versus native Kimina in-process batch. Include state preparation, parsing, queueing, suffix checking, native final check and cleanup. Compare SHRED's official prefix executor, pinned source/toolchain; byte/token prefix fractions alone are opportunity statistics, not end-to-end savings. Preserve unsupported syntax and failures.

Plan review: root self-review only, per user prohibition of agents/OMP. Main risks: overlapping old wall traces, preprocessing duplicated by the prototype, numeric selection differing from proof semantics, changing source/timeouts, CPU-only gains mislabeled GPU gains, and biased top-1000 cohort. These are addressed by same-scope stage instrumentation, direct certificate reuse, native checking/fallback, paired boundaries and explicit scope. No independent audit is claimed.

Daily requirement: review README/structure/dead links and preserve historical failure artifacts; write a dated substantive-progress reflection, then perform its proposed decisive action. This daily maintenance does not replace the experiment.


## Preflight-driven plan consolidation, before any top1000 pair completed

The main comparator is the already-qualified strongest Fast/hybrid plus product
reuse CPU composition. Preserve the currently running first Fast/oracle pair
without restarting it. Complete three reversed-order pairs and one separate
native stock four-stage diagnostic. Extra stock/HiGHS timing cells are
conditional on exceeding1.5x against Fast/hybrid: if the direct path already
misses that comparison, an even faster baseline cannot make it pass, so
repeating a Full/Fast×solver grid is unnecessary. Retain any unused partial
controls from the earlier queued driver, explicitly excluded.

Report every paired ratio plus the ratio of aggregate complete whole times;
the aggregate ratio implements the user's1.5x threshold. If it passes against
Fast/hybrid, run the remaining credible native competitors before claiming
the fastest-baseline rule passes. Native per-source agreement, operational
failures, resources and source scope still require root self-review. This
does not change workload selection, verifier semantics or the threshold.


## Strong-fallback repair, before a valid complete prototype cohort existed

Code inspection found that the first prototype's failed/unsupported route used
stock instead of the current Fast/hybrid/product baseline. Correct the fallback
to that same strongest prequalified CPU path, including hybrid numeric flags.
This is a constructor/comparator repair, not a new hypothesis or threshold.
The actual Real/Nat preflight preserves all native JSON results and engages both
routes. Keep all old partials as invalid for the intended primary comparison.
Reuse the completed1000reference: its executed Fast/product code did not change;
only the then-unused prototype fallback branch/common-library build changes.
Document this first-pair lineage; later reference repetitions use the corrected
common library. Full comparisons and diagnostics remain pending.


## Qualified strong-baseline attribution update

The pre-result diagnostic now instruments the actual Fast/hybrid/product-reuse
path rather than repeating the stock-only stage pilot as its proxy.
A separate native library passes full parsed-response agreement on four real
mixed Real/Nat sources. The full strong diagnostic runs after primary timing;
the stock pilot remains separately scoped historical evidence. Stage CPU uses
the calling thread, excludes external LP-child CPU and retains residual work.
Concurrent invocation-wall sums are not whole-elapsed fractions. This is an
attribution correction, with no threshold, cohort or performance-trial change.
