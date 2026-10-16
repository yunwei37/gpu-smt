# Independent result review: completed Full/Fast primary CPU matrix

Observed 2026-10-16. Reviewer: fresh Codex result-review subagent. Repository main at a654807 at entry. Read the owning research-experiment-design skill in full, human docs/user-instruction.md and docs/questions-for-author.md, the original full plan/review, collector/environment source, raw primary ZIPs, native comparator source/qualification captures, executed integration scripts, and prior/delta publication manifests. This review changes only this file; it does not edit acquisition, policies, analysis code, paper, runtime, or Git.

Selected RQ4 remains: **After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?**

## Disposition

- **Run status: valid completed primary submatrix; full experiment incomplete.** All 12 primary conditions (three rotated blocks × Full/Fast × hybrid/HiGHS) contain all 29,750 original source attempts. Four separate resource profiles have no terminal result at review. This is 12/16 completed planned conditions, not final 16-condition acceptance.
- **Tested hypothesis: inconclusive for a stable Fast whole-verification benefit.** Both solver families show sign reversals across whole-run repetitions. The stronger assertion that Fast uniformly improves complete verification is contradicted by the measured cells. HiGHS is slower in all six matched same-block solver comparisons, but this is a qualified observation on this CPU composition/workload, with outcome differences; it is not universal solver superiority.
- **Research value: supporting.** This measures an established, competent CPU alternative after preparation reuse. It strengthens the CPU frontier evidence; it is not merely acquisition/packaging progress and does not establish a novel system.
- **Paper impact: additional RQ evidence and a mechanism/workload boundary.** It bounds preprocessing restriction and numerical oracle substitutions on released Goedel proofs. It does not directly challenge the heterogeneous-execution thesis, answer all of RQ4, or show GPU benefit.
- **Next paper decision:** retain the primary matrix and negative/mixed effects, preserve hybrid as the stronger observed solver side of this matched matrix while keeping Full/Fast uncertainty explicit, and complete the already planned profiles through the unchanged acquisition path. Do not select an apparently winning Fast cell as the sole CPU denominator, add tuning variants to obtain a win, or promote this supporting comparison into the contribution. The remaining paper decision is whether the proposed heterogeneous system improves complete verification over a matched strong CPU path after all its costs and failures are included.

## Independent recomputation and completion

I used a separate in-memory Python analysis rather than accepting the integration analyzer's successful exit as evidence. For every primary ZIP I read all result rows and raw HTTP responses, checked exact input.jsonl bytes against the canonical file, reconstructed ordinal/source mappings and the basic classifier, recomputed elapsed seconds from admitted/response nanoseconds, checked every request lies inside its terminal interval, and recomputed whole seconds from begin/end nanoseconds. All 357,000 rows have unique source ordinals per cell, exact complete source coverage, no cell failure, expected=returned=29,750, and terminal counts equal independently classified raw responses. No partial prefix supplies a timing denominator.

I also opened the original producer archive at /workspaces/.agent-state/gpu-smt-deps/goedel-workbook-lean427-3c2afe6b.tar.gz. The full sorted GoedelProofs filename population equals the canonical input filenames, and every code field encoded to UTF-8 equals its original .lean member bytes: **29,750 files, 41,564,450 source bytes**. Original ok/warn/error/timeout producer statuses are retained; they are metadata, not a substitute for verification outcomes or a full generator trace. Independent metadata recomputation also confirms 29,750 present and distinct author.problem_id values, with source multiplicity histogram {1: 29750}. This population has one released source per problem: it cannot demonstrate repeated same-problem statement/prefix reuse or reproduce generator verifier arrivals. That is a workload limitation, not a measured preparation-reuse cost.

All primary summary times, returned-attempt rates, positional latency values, basic-difference source sets, and full normalized-response difference source sets match primary-analysis.json. The native comparison excludes only each backward adapter response.time field; direct server/routers/backward.py inspection confirms that field is injected from check_response.time. Warnings, errors, diagnostic positions, native identifiers, operational bodies and other fields remain observable.

## All primary cells

Whole seconds include all original outcomes. Returned attempts/s is not successful proofs/s. Latencies below use the executed analyzer's **zero-based sorted x[round((n-1)q)] positional estimator**.

| Block | Method | Whole s | Attempts/s | Complete / rejected / operational | q50 s | q95 s | q99 s |
|---|---|---:|---:|---|---:|---:|---:|
| 0 | full-hybrid | 12303.065066 | 2.418097 | 27319 / 2376 / 55 | 0.580926132 | 3.518741490 | 11.930771916 |
| 0 | fast-hybrid | 11746.460523 | 2.532678 | 27321 / 2376 / 53 | 0.502482485 | 3.483655202 | 10.755535151 |
| 0 | full-highs | 13590.780054 | 2.188984 | 27318 / 2376 / 56 | 0.684495384 | 4.024763798 | 12.889696316 |
| 0 | fast-highs | 14659.921385 | 2.029342 | 27318 / 2377 / 55 | 0.715717466 | 4.608998515 | 13.674396829 |
| 1 | full-hybrid | 12335.037322 | 2.411829 | 27320 / 2376 / 54 | 0.586610451 | 3.462266214 | 11.527212951 |
| 1 | fast-hybrid | 13383.149816 | 2.222945 | 27319 / 2376 / 55 | 0.604863552 | 4.065916337 | 13.461330158 |
| 1 | full-highs | 15435.903051 | 1.927325 | 27318 / 2377 / 55 | 0.819387516 | 4.742859041 | 14.425583874 |
| 1 | fast-highs | 16380.283824 | 1.816208 | 27317 / 2377 / 56 | 0.828278839 | 5.406756281 | 15.617945647 |
| 2 | full-hybrid | 11298.861809 | 2.633009 | 27319 / 2376 / 55 | 0.517986101 | 3.079336844 | 10.378026843 |
| 2 | fast-hybrid | 10726.288423 | 2.773560 | 27321 / 2376 / 53 | 0.441045675 | 3.089017306 | 9.716792148 |
| 2 | full-highs | 12656.196354 | 2.350627 | 27319 / 2377 / 54 | 0.635772917 | 3.580968610 | 11.234769358 |
| 2 | fast-highs | 12094.531072 | 2.459789 | 27318 / 2377 / 55 | 0.552351473 | 3.617570972 | 10.808237703 |

The JSON field called median_request_seconds is this positional q50, not the conventional median of the two middle values for n=29,750. This is a nonblocking reporting/naming issue, not a native-data defect: for the new last cell it is 0.441045675 s versus conventional median 0.441055261 s. A paper must state the estimator or use a conventional median recomputed offline; no acquisition rerun or collector change is warranted.

## Primary effects and retained response changes

Positive changes below mean the candidate took longer. Counts are exact differences after removing only the backward response timer.

| Block | Fast versus Full | Whole change | Basic differences | Native/full response differences |
|---|---|---:|---:|---:|
| 0 | hybrid | -4.524113% | 10 | 684 |
| 0 | HiGHS | 7.866666% | 11 | 453 |
| 1 | hybrid | 8.497035% | 15 | 688 |
| 1 | HiGHS | 6.118079% | 13 | 455 |
| 2 | hybrid | -5.067532% | 10 | 684 |
| 2 | HiGHS | -4.437868% | 9 | 451 |

Fast/hybrid spans -5.067532% to +8.497035%; Fast/HiGHS spans -4.437868% to +7.866666%. These are observed whole-pair ranges over three blocks, not confidence intervals. Fast/hybrid is fastest in blocks 0 and 2; Full/hybrid is fastest in block 1. The plan rotates order but three blocks do not fully balance all four method positions. Sequential acquisition, time-varying shared CPU/memory/cache/I/O activity, and native variability are competing explanations; the evidence does not identify an uncontaminated causal interaction estimate.

Under hybrid, same-basic differences are 653/652/653 warning/info-only message changes plus 21 changed error-message cases per block. The remaining 10/15/10 differences are operational↔complete: 6→complete and 4 reverse, 7 and 8, then 6 and 4. Under HiGHS the same-basic differences are 409 warning/info-only and 33 changed error-message cases in every block; the remaining transitions are 5 complete→operational, 5 reverse, and 1 operational→rejected in block 0; 7 and 6 in block 1; 5 and 4 in block 2. There is **no direct complete↔rejected transition in the Full/Fast pairs**. This does not imply response identity: unused-hypothesis warnings can change when Fast selects fewer hypotheses, and all changed native diagnostics remain retained.

| Block | HiGHS versus hybrid | Whole change | Basic differences | Native/full response differences |
|---|---|---:|---:|---:|
| 0 | Full | 10.466619% | 14 | 1271 |
| 0 | Fast | 24.802883% | 11 | 1391 |
| 1 | Full | 25.138681% | 12 | 1269 |
| 1 | Fast | 22.394833% | 14 | 1395 |
| 2 | Full | 12.013020% | 14 | 1271 |
| 2 | Fast | 12.755975% | 9 | 1389 |

Every one of these six oracle comparisons contains source **19124: hybrid complete → HiGHS rejected**, directly traced to the retained maximum-recursion-depth diagnostic in the HiGHS response. That observed resource/constructor boundary is not an unsoundness finding, and it must not be hidden or converted into a transparent drop-in equivalence claim. Other transitions are retained operational changes (plus rejected→operational in block-0 Full). Same-basic error-message changes number 40 for Full and 37 for Fast in each block; warning/info changes number 1,217 and 1,343, respectively. Block-1 Fast also contains one changed operational envelope. No native diagnostic or operational field was normalized away.

Across the matrix there are **485 native/service timeout responses and 171 HTTP 500 responses**, all charged to their cells and retained in raw data. Direct 500 examples are stock-service {"detail":"JSON decode error"}; these are operational failures, not proof rejection or a proposed-method win. Counts/rates must continue to include these failures. Complete outcomes are the stock Lean/native response classification, including sorry/error checks; original author migration statuses are not an independent correctness oracle.

## Independent baseline and mechanism audit

This is a real complete-source comparison, not a bytecode/cold/null baseline. run-farkas-fast427-full.py composes run-highs-native-cpu.py and run-gc-repaired-header.py. All four methods use the same Kimina service command/cwd, four HTTP requests in flight, CPU eligibility 16–19, native Mathlib load manifest, Lean 4.27/producer source, stable dependency root, private Fast-module path, stock per-process 12 GiB address-space behavior, pool/default reuse and 300 s legacy timeout. Per-cell command records agree for command/cwd/backend/affinity/stock_defaults/api. The relevant tracked runner and Instrument source paths are clean at review; no tuning/policy mutation was introduced here. This does not establish exclusive physical cores or eliminate shared host effects.

The full source is preserved verbatim; Farkas instrumentation is added at the REPL import-header path, rather than rewriting original proof text. Full and Fast both import the private Fast module, charging that common import/composition overhead fairly. Fast enables FARKAS_USE_FAST=1; Full clears it. hybrid selects the native binary plus FARKAS_EXTERNAL_CPU_HYBRID=1; HiGHS selects highs-certificate-oracle.py, clears hybrid, and uses highspy 1.15.1 with only output_flag=False to keep the existing JSON-line transport valid. The adapter formulates the numerical support LP, returns support to the native exact-repair engine, and retains full exact fallback. It does not accept floating-point answers as Lean proofs. The Rust server verifies exact certificates before returning them; absent/failed native routes retain stock tactic fallback.

I inspected Fast.lean and Instrument.lean, not just method labels. Fast probes numeric forms, maps selected certificates to source hypotheses, invokes stock proof-producing linarith on the selected set, and restores saved state before the full native/stock path on misses or errors. Explicit custom configs delegate to the original elaborator. Preserved Fast and Instrument snapshots are byte-equal to their measured source files. Real qualification ZIPs independently show Fast hits **9**, probe misses **8**, native-route fallback **8**, and **17** successful nonempty native certificates for Fast/hybrid and Fast/HiGHS. Their Full comparators show **17** native routes/certificates. This confirms actual engagement and fallback on real sources; it is not a claim that the whole population has those frequencies.

Primary telemetry is deliberately disabled, and inherited relevant driver telemetry/method variables are absent; profiles enable the existing instrumentation separately. Thus a primary-wide Fast hit rate, exact solver-internal success/fallback census, causal stage breakdown or resource dominance cannot be inferred yet. This limitation is planned and does not invalidate the complete primary elapsed comparison. I found no evidence that HiGHS was simply unengaged, transport-broken across the workload, or intentionally weakened; its source-19124 recursion outcome and the preserved operational failures remain limitations on outcome equivalence, not credits toward heterogeneous-system superiority.

## Costs, shutdown and uncertainty

Summed primary whole elapsed is **156610.478697967 s (43.502911 h)**; the first-primary-begin to last-primary-end interval is **156938.141034968 s (43.593928 h)**. The difference includes between-cell/archive work. These are elapsed acquisition costs, not CPU-hours, energy, an exclusive-hardware bill or statistical independent-trial counts.

The source collector clock starts before input persistence, then includes stock server startup/readiness/import/native loading/preparation, numeric/proof/kernel/HTTP work, raw/log capture, replacements, process termination/wait and gzip-stream drain/EOF. Native software build/install and ZIP finalization after the clock are excluded and must remain declared. Overlapping request durations must not be summed as a wall-clock decomposition. Closed-loop four-in-flight request percentiles are not offered-load/queueing or interactive-stream tails.

All primary servers have return code -15 after the collector's requested termination, failure=null and full returned population. Each retained stdout log reaches manager cleanup, application shutdown complete and finished-server markers. Stock manager cleanup schedules asynchronous REPL closures and the collector waits for server/drain EOF; fewer “Closed REPL” than “Closing REPL” lines mean those logs alone are not an exhaustive descendant-reaping receipt. A current read-only /proc check found no surviving matching CPU16–19 REPL/oracle process predating the last primary end; observed matches belong to the ongoing profile epoch. Therefore this review found no demonstrated surviving primary workload, while avoiding a stronger historical all-descendant lifetime/CPU-accounting claim.

Four resource profiles remain unfinalized; no primary resource files were falsely substituted. Resource superiority, exact complete-tree CPU work, independent resource replication and full 16-condition acceptance remain open. The recorded 29.901585 s integration analysis and this review are offline reuse after primary completion, not native reruns.

## Publication audit and integration boundary

The only newly published cell is **goedel427-rep2-fast-hybrid**, 29,750 attempts, 10726.288423000 s, 27321 complete / 2376 rejected / 53 operational. Its (group,label) is absent from both earlier publication manifests; the other eleven primary cells retain their earlier homes. I decompressed the published results file and compared it byte-for-byte with the complete ZIP's results.jsonl. For every published raw-response row I checked ordinal, source index, member name and HTTP status, then decoded body_base64 and compared every byte against its ZIP member. All 29,750 match. The published command matches the ZIP command and the terminal record matches the original terminal bytes. This is a genuine new terminal-cell publication, not an earlier raw capture relabeled as new.

The executed scripts and primary-analysis.json are reusable entry points; raw original ZIPs remain under artifacts/lean-modern-native-compilation-2026-10-14/farkas-fast427-full1/. The new terminal manifest and published-cells directory are beside this report. Prior publication manifests remain at ../completed-cpu-cells-20261016/published-completed-cells.json and ../cpu-terminal-update-20261016T155034Z/new-terminal-cells.json.

No material completion, timing-recomputation or publication-fidelity defect blocks publishing this **completed-primary checkpoint with the qualifications above**. This review does not certify a new contribution, full matrix, RQ completion, GPU/system win, or paper readiness; it supplies an independent result review for precisely the completed primary submatrix. No new protocol, redundant experiment, policy gate or tuning run is required by these findings.
