# Completed original CPU acquisitions: result and publication update

Observed 2026-10-16 UTC. BOOTSTRAP, supporting evidence for RQ4: After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path? This node analyzes terminal data from existing admitted acquisitions; it launches no experiment, changes no population/solver/settings, and creates no new tuning matrix. The full original Lean/SMT/service/RTX5090/paper objective and all RQs remain open.

## Main decisions

The original HiGHS comparison has completed all12conditions (three three-way primary blocks plus three separate profiles). Its native FP64 hybrid alternative has longer whole time than native tiered in all three primary blocks. HiGHS has two losses and one gain. This complete result does not justify a universally faster sparse-LP replacement or another narrow GPU kernel selected from one winning block.

The original-solver product comparison has completed all8conditions (three alternating pairs plus two profiles). Primary whole effects remain mixed. Ordinary invocation-local product reuse is a useful CPU control with bounded evidence, not our novel system contribution.

The GC/native compilation comparison now has its third complete primary pair. Its two separate resource profiles remain unfinished. The three primary observations consistently favor native library loading under their own protocol. That makes native compilation an essential competent denominator; it is prior art, not a new contribution or a measured GPU benefit.

Full/Fast remains incomplete. Only newly finalized terminal data are published; no complete-matrix conclusion is drawn for it. Existing healthy acquisitions are not restarted or row-polled.

## Primary end-to-end observations

Every primary condition verifies all29,750 original Goedel4.27 sources, retaining rejected, incomplete/operational cases and original order/options. Whole clocks charge input persistence, service readiness/import/native loading, native verification, HTTP/logging/raw capture, replacements and observed shutdown/drain. Software builds and post-clock ZIP are excluded.

| Existing comparison | Pair1 | Pair2 | Pair3 |
|---|---:|---:|---:|
| GC original -> native libraries, elapsed reduction | 51.934410% | 52.381851% | 59.522208% |
| tiered -> hybrid, elapsed increase | 10.612935% | 5.224932% | 23.432264% |
| tiered -> HiGHS, elapsed increase | 11.830231% | -11.451553% | 21.467193% |
| original solver -> product reuse, elapsed reduction | -0.586076% | 5.109767% | 14.303137% |

Different rows have different commands, baselines and CPU eligibility. They do not rank methods across rows. Three observations and their range are descriptive, not confidence intervals, isolated causal effects or IID samples. Profiles are not additional primary repetitions.

New GC third-pair clocks are32,484.597840s versus13,149.047983s. Original counts are27,316complete/2,376rejected/58operational; compiled27,319/2,376/55. Exactly23 basic/native changes are10complete->operational and13reverse, with no direct complete/rejected flip. Request medians0.735318->0.521893s, p9516.023529->4.385423s and p9976.435077->16.567240s are closed-loop observations, not offered-load capacity or a wall-time decomposition.

HiGHS native responses are not transparent duplicates of tiered: primary blocks retain1,301/1,305/1,306native differences and8/12/13basic differences, including rejected outcomes; the profile has71operational results and one complete->rejected change. Product primary differences11/10/10 are operational/complete transitions; its profile has8. Raw diagnostics/internal identifiers remain rather than being normalized into equal results. Independent review recomputes the full envelopes excluding only the pinned adapter's injected response.time.

## Complete separate resource observations

| Group/method | Samples / incomplete | Sampled peak aggregate PSS KiB | Recorded rusage counter s |
|---|---:|---:|---:|
| tiered | 5905 / 28 | 7005488 | 10031.249406 |
| hybrid | 5721 / 22 | 7668612 | 8972.480160 |
| HiGHS | 6582 / 1448 | 8723814 | 8861.636122 |
| stock | 7947 / 20 | 7486707 | 20509.652282 |
| products | 6442 / 22 | 8005904 | 11821.742785 |

The original summary field named whole_process_tree_cpu_seconds is a RUSAGE_SELF+RUSAGE_CHILDREN observation including the observer, not validated exhaustive descendant CPU. PSS sampling is once per second, non-atomic and affected by outside shared mappings/disappearing processes. HiGHS's1,448incomplete samples are substantial. One profile per method cannot establish a replicated memory/CPU advantage. Instrumented profile elapsed effects are not pooled with primary results.

The service capture ends the completed service via terminate/wait/drain; server returncode-15 is expected under that common protocol. It is not a claim that every native background task exits naturally. The newer native direct-batch experiment has its own EOF boundary and cannot supply these runs' missing semantics or denominators.

Independent audit locates a malformed oracle telemetry line in original profile-tiered/oracle.jsonl at line9976, byte offset59,498,527. The exact10,782bytes are retained in profile-tiered-oracle-line9976.raw with source location. Some telemetry integers also exceed default Python digit parsing. This is not a full route census and does not invalidate completed native HTTP results. No route/hit-rate claim, new correctness campaign or rerun follows. Full original oracle streams remain in the original retained ZIPs; the isolated bad-line publication does not replace them.

## Raw publication and reproducibility

analyze.executed.py is the actual offline command. It uses the existing original native loader and source-native ZIP/result/command records. execution.json records its real UTC/CPU as concurrent offline analysis load, not a benchmark observation. Existing valid primary evidence is explicitly reused in reused-primary-evidence.json; it is not presented as new execution.

Against the earlier52-cell source-attempt publication snapshot,9additional terminal records are persisted here, totaling245,808attempts. This extends that defined snapshot to61conditions/1,639,214attempts; this count excludes other observation/profiling experiments and is neither RQ completion nor a scalar research-progress score. The delta includes previously finished miniF2F output that was reviewed separately; no new mini performance conclusion is claimed.

published-cells/ includes each new attempt row, exact raw HTTP response bytes (lossless base64 in gzipped JSONL), command, terminal and available raw resource series/summary. Each record links its complete original ZIP still retained in the owning Workspace. No original archive or failed case is deleted/moved. Original source input bytes are checked against the previously qualified same-cohort archive, with full order/index/count reconciliation.

## Figure and canonical handoff

gc-native-primary-pairs.pdf/png and plot-gc-native-primary-pairs.py draw all three original/native whole-corpus observations directly from the result data. Caption: Complete elapsed verification for three alternating29,750-source Goedel4.27pairs using the same GC REPL with original versus native library loading, CPU8-11 and four HTTP requests in flight. All primary observations are shown; native loading reduces elapsed time in each, with operational differences and shared-background/shutdown costs retained. Profiles are excluded and unfinished; this is a competent CPU control, not new compiler/system novelty or GPU performance.

The plot uses the current paper's serif/colorblind-safe style and measured243bp column width; the PDF box is243x183.6bp and minimum text7.5pt. Visual inspection repaired a clipped label and overlapping legend. It is a figure handoff, not inserted into the active OMP paper or a compiled-paper QA claim.

The existing OMP owner must reconcile docs/evaluation.md, paper data/figures and the stale fe13c12/unpushed/partial CPU statements against this actual result. Root does not overwrite active author files. Accepted independent result-review.md recomputes all22scoped terminal cells and five full resource streams. Its bounded mixed/negative conclusions are adopted; it requests no additional experiment.

## Disposition and next scientific work

Run status: complete12-condition HiGHS and8-condition stock-products acquisitions; complete GC primary pairs but incomplete resource matrix; Full/Fast incomplete. Hypotheses: HiGHS/product whole benefits mixed; hybrid replacement contradicted on the measured native tiered blocks; ordinary native compilation supported on three primary blocks. Research value: supporting CPU evidence/necessary strong denominators, not a standalone contribution. Paper impact: bounds tested arithmetic/product choices and forbids a weak CPU denominator for future device claims; no all-RQ/thesis acceptance.

Close further plain sparse-solver/FP64 mode tuning for this measured scope. Preserve the completed range, adverse outcomes and profiler limits; finish already running declared acquisitions. Select future work from a useful verification-native end-to-end opportunity beyond the strongest relevant CPU method, rather than more kernel/descriptor counts. Full native branch results, meaningful preparation/service workloads, supported lifetimes/artifacts, complete heterogeneous costs and canonical paper gates remain required.
