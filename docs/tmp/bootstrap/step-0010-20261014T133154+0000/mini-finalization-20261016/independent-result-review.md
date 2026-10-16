# Independent result review: complete producer-version miniF2F CPU acquisition

Observed UTC: 2026-10-16T11:04:09.157213+00:00

Reviewer: native Codex, independent of the OMP authors and the root's earlier self-reviews. This is one retrospective result review of the completed original acquisition. I inspected the existing owning Workspace through the established infrastructure transport and wrote only this report. I did not run Lean, a verifier, a build, a GPU operation, a new capture, Git, a restart or cleanup; I did not change the plan, implementation, paper, canonical documents, runtime or other acquisitions.

## Disposition

| Judgment | Result |
|---|---|
| Run status | **Valid, complete** for the admitted eight-condition comparison, with operational failures and changed responses retained. Valid acquisition does not mean every source verified successfully. |
| Tested hypothesis | **Supported within this measured block:** selective native arithmetic compilation has lower complete-corpus elapsed in all three primary pairs against the producer-compatible original GC path. Transparent behavior, uniform latency improvement and a causal memory benefit are not established. |
| Research value | **Supporting.** This adds complete evidence for a compatible CPU denominator on the promised miniF2F cohort; it is more than a build/qualification dependency, but is not the central systems contribution. |
| Paper impact | **Additional RQ4 evidence with a producer/workload boundary.** It does not answer RQ4, close another RQ or directly challenge the central thesis. |
| Next paper decision | Replace pending mini acquisition/resource wording with the completed qualified CPU evidence, including behavioral differences, mixed primary p99 and profile regressions. Retain this comparator for an appropriately matched future heterogeneous comparison. Do not automatically expand the matrix or reopen failed implementations. |

The supported statement is lower observed full-population wall time for this implementation and protocol, not equivalent responses delivered faster for every input, a globally strongest CPU implementation, task-solving improvement, GPU benefit, or scientific novelty.

## Contract, admitted method and reviewed inputs

I read the complete `research-experiment-design/SKILL.md`, its plan template and technique catalog; the owning [human instructions](../../../../user-instruction.md), [idea story and unchanged four RQs](../../../../idea-story.md), and current [evaluation contract](../../../../evaluation.md); the original [mini plan](../mini-gc49-native-cpu-plan.md), [qualified launch](../mini-gc49-qualified-full-launch.md) and [source comparison](../mini-gc49-qualified-source-comparison.json). The prior [first-pair review](../../../../../artifacts/lean-native-compilation-2026-10-14/gc49/first-pair-result-review.md) is historical context, not this verdict.

RQ4 is: **“After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?”** The admitted immediate uncertainty is whether selective native arithmetic compilation improves complete producer-version miniF2F verification under competent GC reuse. This is a supporting CPU comparison before any matched device comparison. RQ1 preparation expense, RQ2 branching/native artifacts/cancellation, and RQ3 equal-resource service behavior retain their original meaning and remain open, as does RQ4. Ordinary CPU compilation is explicitly outside the claimed new systems contribution.

The population is all **7,808 original source attempts**, 244 tasks × 32 in the owning contract, using Lean **4.9.0-rc1** and the original Mathlib/Aesop dependencies. Counts are source attempts, not task-level pass@32. Both methods use the same producer-compatible GC-capable REPL and Python HTTP backend. The candidate additionally loads the existing `libMathlib-Tactic-Linarith-1.so` native dependency closure. It does not compile all Lean work or establish a universal CPU optimum.

The admitted design is three complete alternating pairs, in orders **original/compiled, compiled/original, original/compiled**, followed by one separately instrumented original/compiled resource pair. All methods retain four in-flight closed-loop requests, CPU eligibility 0–23, stock 12 GiB per-native address-space limit, 300 s native allowance, default pool 23 and unlimited reuse. Shared eligible resources are not reserved or exclusive hardware.

Primary evidence is in `artifacts/lean-native-compilation-2026-10-14/gc49/` (abbreviated Q below):

- [Original launch](../../../../../artifacts/lean-native-compilation-2026-10-14/gc49/full1-launch.json), [driver](../../../../../artifacts/lean-native-compilation-2026-10-14/gc49/run-gc49.py), all eight terminal records and ZIPs in [Q/full1](../../../../../artifacts/lean-native-compilation-2026-10-14/gc49/full1/), and `acquisition-completed.md`.
- [Retained input](../../../../../artifacts/lean-native-compilation-2026-10-14/gc49/input.jsonl), compared byte-for-byte with `artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs/minif2f/input.jsonl` and every archived cell input.
- [Actual built REPL source](../../../../../artifacts/lean-native-compilation-2026-10-14/gc49/source-built-gc49.tar.gz), retained build failures/compatibility records, successful `build4-terminal.json`, and qualification outputs in `Q/preflight1/`.
- [Offline entry point](../../../../../artifacts/lean-native-compilation-2026-10-14/gc49/analyze-completed-cells.py), its imported loader `artifacts/lean-modern-native-compilation-2026-10-14/analyze-gc2.py`, [current full analysis](../../../../../artifacts/lean-native-compilation-2026-10-14/gc49/complete-cells-analysis.json), and this directory's `analysis-command.json`, `analysis.stdout`, `analysis.stderr`, `complete-analysis.json` and retained prior partial analysis.
- The actual existing backend's `server/repl.py`, `server/settings.py`, `server/routers/backward.py`, and `ResourceCapture` in `artifacts/lean-gpu-checking-2026-10-13/experiment022/source1/lean_capture_warm.py`.

The recorded original launch is `/tmp/gpu-smt-kimina-header-repair-20261014/.venv/bin/python -u Q/run-gc49.py`, cwd `/workspaces/repository`. The analysis command is `python3 Q/analyze-completed-cells.py`, same cwd; the retained finalization stdout reports eight valid cells and three qualified pairs, stderr is empty. These are inspected historical commands; I did not rerun either entry point.

## Independent validity checks and baseline audit

I independently read all eight raw ZIP populations and their **62,464 response files**, reconstructed row order, parsed every retained response, and compared sources and metrics without invoking an acquisition or writing another analysis artifact. The substantive checks were:

1. Original input and Q's retained input are exactly equal: 15,135,693 bytes, 7,808 rows and 7,808 distinct source indices. All eight archived inputs equal those bytes. Every archived row's ordinal and source index matches the original ordered population; no missing, duplicate, filtered, migrated or reordered source was found.
2. Every condition has exactly 7,808 result rows and response members. Reclassification from HTTP status and native/error/message/sorry fields agrees with every stored basic outcome. Counts match the terminals. All terminal `failure` fields are null; all whole times equal `(end_ns - begin_ns)/1e9`. Thus the completed source-attempt population includes failures rather than excluding them.
3. Every request duration agrees with its recorded admission/response clocks. Recomputed medians and order-statistic p95/p99 agree with the current analysis. The quantile convention is sorted value at `int(q*(n-1))`; these are descriptive empirical quantiles, not estimated confidence intervals.
4. Recorded command objects match between methods in every primary pair and the profile pair after excluding only method/PID. Monotonic cell boundaries confirm the admitted alternating chronology, followed by the separate profiles. I recomputed primary reductions directly from terminal whole times, not request-duration sums.
5. The retained source archive pins `leanprover/lean4:v4.9.0-rc1`, contains GC/detached-response support and loads `LEAN_SERVER_NATIVE_DYNLIB` in `main` when supplied. The actual Python reuse route sends `env=0, gc=True` for reused non-header work, and the shared source implements the GC path. This is a competent GC reuse comparator, rather than the earlier ignored-GC/NoGC or unrestricted failed epoch. Empty-header/first-use native behavior remains the common implementation's behavior.
6. Qualification terminals record actual native soft/hard `RLIMIT_AS` of 12,884,901,888 bytes in both methods, not merely a settings string. The compiled qualification's raw per-case records contain native mapped-library observations, including the Linarith dependency closure. The full driver uses this same conditional load path. This supports mechanism engagement; it does not quantify how much work used compiled arithmetic, prove every full-cell child's mappings independently, or measure its isolated contribution.
7. Native comparison excludes only the inserted `response.time` field. Actual `server/routers/backward.py` extends `check_response.response` with `check_response.time`; raw timers and JSON remain in the archives. I independently compared the remaining response/error payloads and obtained exactly the recorded primary difference indices, plus the profile differences below. Errors, environment-related fields and diagnostics were not otherwise normalized.
8. Recomputing from both raw resource streams gives exactly the retained sample counts, incomplete counts, maximum aggregate PSS and maximum private totals. The observer source explains the non-atomic process-tree walk and getrusage counter; its limits matter below.

The same REPL/SDK/backend/source population/deadline/default resource behavior applies to both methods; the declared experimental change is the native library load and its needed library search path. No avoidable baseline interface failure exclusive to the original method was found. Both have substantial operational errors; their shared occurrence does not make them successes. In particular, source 663 is retained as HTTP 500 `JSON decode error` in **all eight cells**. I do not assign it an unobserved OOM cause in this new epoch.

This is not a clean-room reproduction. Recorded command JSON does not serialize the entire inherited environment, venv or per-cell binary identity; the REPL source archive is not the full SDK/Mathlib/native-library/Python dependency installation. Producer pins, the existing native build paths and retained source records must accompany reproduction. Current source plus qualification and unchanged recorded full commands support the intended comparison, without proving the absence of every historical environmental drift. The qualification itself used direct stock `run_checks`, not HTTP; the complete full cells provide the actual HTTP-path evidence. I found no documented mid-run plan change, deadline change, selective retry or source filter in the reviewed driver/terminals. This review is not a claim that every external dependency has been independently rebuilt or every worker lifecycle/cancellation property tested.

## Whole-corpus timing and request observations

Whole time starts before input persistence and server startup and ends after returned requests, explicit server termination/wait, log-drain EOF and observer closure. It charges startup/import/native loading, HTTP, verification, raw/log capture, replacement and shutdown. Software construction and subsequent ZIP archival are excluded. All eight server return codes are **-15**: the driver explicitly calls `terminate()` after responses, waits and drains before ending its clock. These are complete captures with planned termination, not eight native/server exit-0 proofs or verified graceful-cleanup experiments.

| Primary pair / execution order | Original whole s | Compiled whole s | Lower whole time | Original / compiled attempts/s |
|---|---:|---:|---:|---:|
| 0 / O→C | 12689.277611079 | 11723.450893959 | 7.611360920% | 0.615323 / 0.666015 |
| 1 / C→O | 12539.743054951 | 11192.977850911 | 10.739974481% | 0.622660 / 0.697580 |
| 2 / O→C | 11914.914090759 | 9893.716240379 | 16.963595667% | 0.655313 / 0.789188 |

The arithmetic mean of the three within-pair percentage reductions is **11.771643689%**, with observed range **7.611360920–16.963595667%**. It is a descriptive mean/range, not a confidence interval, pooled independent-request estimate or a universal causal effect. Both original and compiled clocks drift substantially over the sequence; alternating order helps expose order dependence but three nonrandom whole pairs on shared hardware do not remove time/background effects. I cannot attribute the entire difference solely to arithmetic execution or partition the saving by cause.

| Primary pair | Median s, O→C | p95 s, O→C | p99 s, O→C |
|---|---:|---:|---:|
| 0 | 0.444358621→0.459717619 | 12.852154549→9.761435721 | 247.849324991→275.352912759 |
| 1 | 0.445448270→0.402207064 | 12.738322636→8.711796753 | 251.141015319→253.276302702 |
| 2 | 0.399087761→0.314407512 | 11.960956896→7.424169799 | 224.267571889→209.717643986 |

Primary p99 worsens in the first two pairs and improves in the third; first-pair median also worsens. Thus lower whole-corpus elapsed does not imply uniform request/tail improvement. The throughput numerator counts all terminal attempts, not successful checks. Four outstanding requests overlap and are replenished on completion, so durations cannot be summed into whole-wall/CPU components. These closed-loop observations are not measured verifier arrivals, offered-load capacity, production SLOs or the full RQ3 service frontier.

## Native outcomes and response differences

| Condition | Complete | Rejected | Operational |
|---|---:|---:|---:|
| Primary original, each of 0/1/2 | 3008 | 4657 | 143 |
| Primary compiled 0/1 | 3008 | 4659 | 141 |
| Primary compiled 2 | 3008 | 4660 | 140 |
| Profile original | 3008 | 4657 | 143 |
| Profile compiled | 3011 | 4660 | 137 |

No incomplete category is observed in the acquired full populations under the retained classifier. Its absence is an observation, not proof that incomplete-proof semantics were exhaustively exercised. The qualification includes incomplete controls, separately.

Primary basic changes are original 300 s operational timeout→compiled native rejection at **2325 and 3209 in every pair**, plus **4869 in pair 2**. There is no primary complete↔rejected flip. Native payload differences after excluding only the adapter time are:

| Pair | Difference indices | Remaining exact matches |
|---|---|---:|
| 0 | 2325, 3209, 4993, 7205, 7212, 7213, 7216, 7218, 7226, 7231 | 7798 / 7808 |
| 1 | 2325, 3209, 7230, 7521, 7530, 7533, 7537 | 7801 / 7808 |
| 2 | 2325, 3209, 4869, 7217 | 7804 / 7808 |

Beyond the basic changes, all these primary differences are operational→operational exchanges between a timeout body and HTTP 500 `JSON decode error`. They remain failures and retained differences, not normalized parity. Timeouts becoming rejections are useful returned outcomes under this budget, but establish changed observable behavior. No requested theorem proof artifact or cancellation/history equivalence is established by basic counts or this narrow payload boundary.

The profile has **12 basic changes**: operational→rejected at **2325, 2507, 3209, 4869, 5001, 5399**; rejected→operational at **2590, 2591, 2596**; operational→complete at **3077, 3086, 3095**. It has **16 native payload differences**: those 12 plus operational-body changes at **7202, 7217, 7224, 7230**. The other 7,792 payloads match after the same timer exclusion. The extra three complete classifications occur only in this separately instrumented pair; they do not establish improved task-level solving or uniform behavior.

The final profile contains severe request regressions that should accompany its favorable aggregate metrics. Compiled **2507** returns native rejection after **1785.317825365 s**, with **11,884 error messages**; original returns a timeout after **300.018328084 s**. Compiled **2590/2591/2596** return operational timeout bodies after **1509.715990660 / 1506.767364732 / 1505.895133436 s**, whereas original returns rejections after **40.162307855 / 39.049452597 / 0.143830531 s**. These are raw observed request times, not trimmed outliers. The nominal 300 s native allowance is therefore not an end-to-end HTTP deadline. The cause and causal coupling of this episode are not established here; a large response, timeout body or shared load alone does not prove an explanation. This profile cannot support a bounded-tail or transparent-service claim.

## Separate resource profile: observations and limits

| Profile observation | Original | Compiled |
|---|---:|---:|
| Whole time, s | 11667.404590308 | 10590.304427555 |
| Attempts/s | 0.669214815 | 0.737278145 |
| Median / p95 / p99 request s | 0.355265734 / 10.978714741 / 222.847363013 | 0.288971529 / 6.994611461 / 187.027784611 |
| Maximum request s | 303.303265462 | 1785.317825365 |
| Sampled aggregate peak PSS, KiB | 34116090 | 33843334 |
| Sampled aggregate peak private, KiB | 30631608 | 30345756 |
| getrusage-derived CPU counter, s | 21837.747522 | 21417.507820 |
| Samples / incomplete samples | 7258 / 106 | 6994 / 92 |
| Median actual sampling gap, s | 1.582007130 | 1.494905565 |
| Maximum actual sampling gap, s | 2.924036606 | 2.376390487 |

The single profile pair has 9.231703199% lower observed whole time, 0.799493729% lower sampled peak PSS, 0.933192929% lower sampled private peak and 1.924372931% lower recorded CPU counter. These arithmetic differences are descriptions of this pair, **not evidence of a replicated memory/CPU saving**, and the profile is not a fourth primary timing repetition.

The nominal one-second observer waits then walks the process tree and reads `smaps_rollup` sequentially; raw maximum individual observation durations are 1.914906021 s and 1.376090443 s. Sampling can miss peaks, miss short-lived/reparented processes and encounter disappearing processes; incomplete samples are retained. Summed process memory is non-atomic, and shared-file PSS depends on other mappers. Its aggregate tens-of-GiB value is not a violation or redefinition of the per-native 12 GiB address-space setting. The getrusage difference includes observer CPU and waited-child accounting; it was not independently validated as exhaustive CPU for all descendants. Background CPU, memory and I/O remain uncontrolled. Different profile outcomes and the long compiled episode further prevent interpreting these small resource deltas as like-for-like causal resource efficiency.

## Research consequence and next owner contract

This full-source result independently fills the admitted producer-version mini CPU evidence gap. The observed primary benefit survives all three planned whole comparisons, while mixed p99 and operational/native changes bound its interpretation. It should be retained as a competent compatible CPU comparator and supporting evidence; build availability or archived-file counts are not separate scientific contributions.

The result does not establish native-state branching advantage, preparation-cost saving, multi-context service novelty, artifact/history/cancellation transparency, an equal-resource service frontier or heterogeneous acceleration. It cannot inherit Goedel 4.27 whole-library timings, earlier NoGC/native6 clocks, metadata-kernel gains or another workload's GPU denominator. It does not rehabilitate closed GPU/shared-placement/SMT constructors. All four RQs, strongest matched complete-cost device evidence, causal mechanisms, full manuscript and whole-step/paper independent audits remain open. Positive CPU timings do not finish the paper.

**Root owns integration and publication.** Integrate this review with all eight raw terminal/ZIP records and the full analysis, update pending counts and accurately scoped paper/evaluation numbers, and preserve negative outcomes and the long-profile episode beside any aggregate figure. The raw ZIPs, failed earlier epochs, actual built-source/version provenance and prior partial analysis remain evidence. This review authorizes no new experiment, tuning grid, runtime/model change, cleanup, restart or matrix expansion. Existing OMP ownership and other acquisitions remain preserved.

The next substantive paper decision belongs to the root under the unchanged contract: use this completed baseline evidence when selecting the highest-value admitted work for the full Lean/SMT/service/device story. A follow-on device claim needs its own matched complete-cost comparison against the relevant competent CPU route; this report neither selects nor admits it. Additional reruns of this completed matrix or a new explanation-only profiling experiment are not automatic consequences of these findings. If the root investigates the profile episode using existing retained evidence, report its actual explanation separately without modifying these acquired observations or presenting a repaired response as the original result.
