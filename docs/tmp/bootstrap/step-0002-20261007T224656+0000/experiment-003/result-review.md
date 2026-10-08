# Experiment003 independent result review — 2026-10-08 UTC

Run status: **valid** for the admitted ordinary source-module coarse profile.
Tested hypothesis: **contradicted** for a kernel-dominant interpretation of these measured module costs; the plan's descriptive route-selection uncertainty is resolved locally toward frontend/meta/tactic work. No preregistered numeric kernel-dominance threshold existed, so this is a directional local interpretation, not a threshold test.
Research value: **supporting**.
Paper impact: **mechanism or workload boundary**, adding supporting RQ4 evidence without answering RQ4.
Next paper decision: retain this complete normal-check negative opportunity discriminator; prioritize source-grounded deeper profiling of typeclass inference, simplification and interpretation/frontend work over a kernel-only GPU route on these six modules. Do not infer a full-device bound or revise the central service thesis. Actual prepared/warm residual costs, dynamic dependencies and strongest measured complete CPU/device comparisons remain necessary.

## Review scope and reproducibility

At start directly read `docs/user-instruction.md`, complete idea story/evaluation, full research-experiment-design skill, approved plan and round-one review, and exact paper RQ4: “After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?” Read the full capture/analyzer and E7 report, then independently inspected retained official time_task/timeit, AddDecl, thread-local, shell option, kernel and import source. No native/profile/GPU run, Git action or canonical/paper edit occurred. This is the one fresh review of this completed matrix, with no desired verdict supplied.

Raw authority: `artifacts/lean-module-profile-2026-10-08/{full,preflight,environment-observations.json,executed-source}`. The stale running README is not terminal evidence. Recomputed both analyses offline using preserved executed analyzer into `/tmp/independent-profile-{full,preflight}-review`; both summary objects match released full/preflight-analysis exactly. A separate raw-only calculation parsed cumulative stderr rows, checked every native command, status, wall delta and raw-file hash, and independently computed the component shares and pairs below; it did not consume analyzer category outputs.

Reproduction: `python3 artifacts/lean-module-profile-2026-10-08/executed-source/analyze_lean_module_profile.py --input artifacts/lean-module-profile-2026-10-08/full --out <new-directory>` (analogously preflight). Raw category seconds are displayed number /1000 for ms, unchanged for s; shares below divide by the sum of all displayed categories, with non-import shares subtracting only import. Pair ratio is profile invocation_wall_ns / normal invocation_wall_ns. Medians/ranges use three full repeats only. Preserve raw three-significant-digit native displays in the existing tables, rather than interpreting derived digits as measurement precision.

## Completion, path and correctness audit

Full matrix contains exactly six declared modules × two paths × three repeats =36 terminal cells/18 pairs in normal/profile, profile/normal, normal/profile order. Separate real preflight contains2 terminal cells and is not reused as a full repetition. Full capture lifecycle makespan is261.732027688s; separate preflight7.066994147s. Both event sequences, result receipts, retained sources and shutdown indices are complete; no missing/excluded/duplicated/interrupted cell, no supervisor signal, no raw hash/size discrepancy and no source change. Offline analyzer issues are empty. All38 native process and GNUtime exits are0; stdout contains no diagnostic record or malformed output. All18 full pairs and the preflight pair have identical empty stdout and diagnostic lists, and identical exit outcomes. There are no observed Lean JSON warning/sorry/error admissions to hide. Raw stderr in every cell additionally retains seven identical Lake manifest source-kind warnings for batteries, Qq, aesop, proofwidgets, Cli, importGraph and REPL: the archived vendor git/path packaging adaptations are present in both paths, not silent pristine-manifest evidence. The analyzer outcome label covers Lean stdout and does not mean stderr is warning-free. No dependency update or reconstruction occurred during this run. This verifies the requested ordinary CLI outcome boundary, not theorem-level semantic equivalence or no-sorry status of the imported library.

Commands use exact retained Lake/Lean executables with `env lean -j1 --json <module>` and only `--profile` added on the profiled path; GNUtime `-v -o <time.txt>` wraps that native command. No skip-check, trust override, timeout or emitted olean/ilean/C artifact option appears. CPU affinity0 is recorded for supervisor/children, LEAN_NUM_THREADS=1, LC_ALL=C and exact release PATH/cache are recorded. Environment receipts identify Lean4.9.0-rc1 commit be6c4894e0a6c542d56a6f4bb1238087267d21a0, Mathlib2f65ba7f1a9144b20c8e7358513548e317d26de1, GNUtime Debian1.9-0.2 and Intel Core Ultra9 285K. All recorded executable/config/source provenance still matches retained/live bytes. Executed capture SHA256 is9d24976b448ef635ce480463b086dfb67bb9bc9cf6497d990aca5037d1a5cbae; analyzer SHA256 is2f3441b87c90a2ce95d077a2fa5985af356e0945e6595ba693a636d90e261dd3, equal to current code. No scientific deviation or repair is observed. The approved time/taskset prose correction is reflected in actual commands and does not change comparisons.

Normal/native execution is the observer-overhead control; it is not a competing accelerator/main baseline. Both modes engage original complete current-file frontend/declaration checking with compiled imports. The source confirms profile enables timers without replacing addDecl checks. Correctness diagnostics are independent of category values and are not a circular success oracle. Compiled imports load existing declarations and do not recheck all transitive proofs. These are fresh ordinary modules, not native prepared-state execution; subtracting import categories descriptively does not simulate warm checking.

## Recomputed category findings

Abbreviated module names below retain the six declared source paths from the plan. Category seconds and percentages are medians [min,max] across three repeats. Percentages are descriptive accumulated-scope shares only.

| Module | Type checking s | Type checking share % | Non-import type checking share % | Largest median category (s) |
|---|---:|---:|---:|---|
| Mathlib/Algebra/Group/Basic.lean | 0.173 [0.172, 0.175] | 5.063 [5.052, 5.080] | 5.412 [5.390, 5.414] | interpretation: 1.2 |
| Mathlib/Algebra/Polynomial/Basic.lean | 0.311 [0.310, 0.311] | 4.366 [4.365, 4.380] | 4.618 [4.616, 4.635] | typeclass inference: 2.92 |
| Mathlib/Data/Nat/Prime.lean | 0.093 [0.092, 0.094] | 3.847 [3.842, 3.858] | 4.355 [4.350, 4.361] | simp: 0.637 |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 0.600 [0.600, 0.617] | 5.441 [5.431, 5.497] | 5.679 [5.673, 5.734] | typeclass inference: 6.65 |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 0.399 [0.398, 0.402] | 3.804 [3.804, 3.815] | 4.004 [4.002, 4.016] | elaboration: 2.98 |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 0.360 [0.357, 0.362] | 4.066 [4.048, 4.079] | 4.364 [4.342, 4.375] | typeclass inference: 3.9 |

The native AddDecl category is only3.804–5.497% of observed accumulated categories across individual full cells, and4.002–5.734% when excluding import. It includes checking auxiliary declarations plus wrapper/tracing/admission work, so it is not pure reduction. Larger frontend/meta boundaries consistently dominate the reported categories. Kernel operations executed within typeclass inference/simp/meta work are not identified by these totals; a small AddDecl category cannot rule out a heterogeneous algorithm operating inside those larger scopes.

Every additional native category is retained. Median category seconds follow; categories absent from a module are marked absent, not fabricated zeros.

| Category | Group | Polynomial | Prime | FiniteDimensional | Trigonometric | IntervalIntegral |
|---|---:|---:|---:|---:|---:|---:|
| aesop | 0.0208 | absent | absent | 0.0225 | 0.608 | absent |
| attribute application | 0.00465 | 0.0218 | 0.00187 | 0.0119 | 0.0125 | 0.00444 |
| compilation | 0.00261 | 0.096 | 0.00818 | 0.00103 | 0.071 | 0.0688 |
| dsimp | absent | absent | absent | 0.00817 | 0.00186 | 0.000711 |
| elaboration | 0.372 | 1.84 | 0.282 | 0.89 | 2.98 | 0.678 |
| import | 0.214 | 0.389 | 0.284 | 0.464 | 0.523 | 0.6 |
| initialization | 0.0233 | 0.0233 | 0.0232 | 0.0233 | 0.0232 | 0.0232 |
| interpretation | 1.2 | 0.712 | 0.367 | 0.674 | 1.98 | 1.14 |
| linting | 0.0316 | 0.0339 | 0.0301 | 0.0497 | 0.102 | 0.045 |
| norm_num | absent | absent | absent | 0.000142 | 0.362 | 0.00122 |
| parsing | 0.0473 | 0.0425 | 0.0284 | 0.037 | 0.0525 | 0.0486 |
| ring | absent | absent | absent | absent | 0.167 | absent |
| simp | 0.424 | 0.472 | 0.637 | 0.764 | 0.631 | 1.43 |
| tactic execution | 0.207 | 0.247 | 0.251 | 0.848 | 0.497 | 0.55 |
| type checking | 0.173 | 0.311 | 0.0927 | 0.6 | 0.399 | 0.36 |
| typeclass inference | 0.689 | 2.92 | 0.404 | 6.65 | 2.06 | 3.9 |

These extra categories (including interpretation, typeclass inference, simp, aesop, dsimp, norm_num and ring) prevent treating tactic execution/residual elaboration alone as all frontend work. Their raw values and all three repetitions are in `full-analysis/tables.md`; no thresholded individual scope messages were summed into categories. Official source uses steady-clock elapsed time, global aggregation and same-thread child exclusion; cross-thread overlap and uninstrumented work prohibit a CPU/wall partition, critical path, Amdahl ceiling or operation-level GPU-width inference.

## Paired whole-invocation costs and resources

All exact full pair walls/deltas are retained in `full-analysis/tables.md`. Below each ratio list is repeats1/2/3; medians/ranges are descriptive. Driver invocation time includes Lake/env/import/source completion plus launch/event capture and up-to20ms polling; it excludes later fsync/result serialization/hash work. It is not a native phase timer.

| Module | Profile/normal wall ratios (r1,r2,r3) | Median delta s [range] |
|---|---|---:|
| Mathlib/Algebra/Group/Basic.lean | 1.040508, 1.022136, 1.047496 | 0.141 [0.078, 0.162] |
| Mathlib/Algebra/Polynomial/Basic.lean | 1.014389, 1.008493, 1.008224 | 0.061 [0.060, 0.104] |
| Mathlib/Data/Nat/Prime.lean | 1.057959, 1.032046, 1.074500 | 0.141 [0.079, 0.182] |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1.064145, 1.064736, 1.078578 | 0.684 [0.677, 0.832] |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1.055284, 1.060064, 1.068068 | 0.605 [0.559, 0.687] |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1.054131, 1.055868, 1.045902 | 0.467 [0.398, 0.479] |

Every full profile invocation is slower than its matched normal control; observed ratios span1.008224–1.078578. This is instrumentation plus cache/scheduling/system variability, not a pure causal profiler-overhead estimate. Alternation reduces but does not eliminate order effects; three repetitions do not justify a tail estimate or inferential confidence bound. Observed full-run one-minute load receipts span0.99–1.95; affinity is not host isolation.

GNUtime user CPU spans2.25–10.31s normal and2.36–11.07s profile; system CPU0.14–0.32s normal and0.13–0.31s profile. MaximumRSS across full cells spans720964–1850284kbytes. These native receipt diagnostics are separate from scope elapsed totals and driver wall; maximumRSS is not aggregate fleetPSS or evidence of a service memory frontier. Raw time receipts and parsed per-cell resource values remain available; no performance claim filters negative pairs or slow cells.

## Leakage, alternative explanations and paper use

Modules were selected purposively by six domains before cost inspection; all declared modules/repeats remain. No train/test claim, winner selection, accepted-input filtering, fabricated failures or tuning advantage appears. Shared compiled imports and filesystem cache may correlate repeats, and the preflight primes the first module; these are retained constraints, not independent warm-service evidence. Three repeats and one version/library cannot establish a library-wide distribution, real generated-candidate traffic, cancellation/isolation, prepared-state reuse, CPU SOTA superiority or RTX5090 benefit. Native source trust and ordinary admission policy remain unchanged.

No proposed paper figure or number beyond this local component/overhead table was supplied. The recomputed descriptive numbers above and the full raw-category/pair tables are justified at this boundary, with stock rounding and scope labels. Calling the3.8–5.5% share a complete-verification CPU fraction, proving no-sorry equivalence from empty diagnostics, claiming a5% universal GPU speedup ceiling, or presenting these as post-preparation measurements would invalidate that use. RQ4 remains open. This result meaningfully narrows the next local profiling target and is neither a direct thesis challenge nor merely setup readiness.
