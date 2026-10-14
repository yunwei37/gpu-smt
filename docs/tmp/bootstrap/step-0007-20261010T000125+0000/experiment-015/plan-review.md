# E015 PLAN REVIEW

Round 1 — fresh independent review, 2026-10-12T21:57:58.164149+00:00

## Verdict

**Admit as supporting RQ4 cost characterization. One concrete executability repair is required before the planned real preflight: compile the profiler shim with the pinned Lean toolchain's libc++ ABI rather than host g++'s default libstdc++ ABI.** The scientific scope and matrix need no expansion. This review is diagnostic evidence, not authority to add work. No benchmark, build, Git operation, source/plan/paper edit, or E014 process mutation was performed; this is the sole review artifact.

RQ4 remains verbatim: “After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?” E015 can locate observed residual native costs and select the next consequential operation. It does not itself answer whether a GPU improves complete verification.

## Admission and decision value

I read the user instruction, idea story, current evaluation, closest-work/baseline map, E015 plan, builder, thin shim, native frontend/API, host and capture cleanup, pinned profiler/timer sources, E014 build5 receipt and archived executed source files, and both original input pools. Existing E011 observed 442 arithmetic-oracle calls totaling 3.8909 seconds; those traces do not cover the remaining complete warm native frontend/kernel work. E014 supplies whole CPU performance/resource comparisons without native stage timers. The earlier resident Expr primitive and cold profiles do not supply the missing scope. Reanalysis cannot reconstruct timers never acquired.

The hypothesis is meaningful: substantial observed kernel checking would justify considering a kernel operation; expensive frontend/search with little observed kernel work changes operation selection; workload/outcome differences justify a scoped next mechanism; missing/ambiguous coverage remains inconclusive. These outcomes change the next experiment while preserving all RQs and the full Lean/SMT/RTX5090 objective. Characterization before implementation is a stronger immediate use of the available effort than optimizing an unmeasured kernel primitive. Supporting is the correct role; it is neither a dependency-only build result nor a headline acceleration result. It need not await a favorable E014 result.

## Baselines, workload, metrics and fairness

This is descriptive characterization of the existing strongest compatible optimized warm snapshot path, not a new superiority comparison. Profiling off/on on the same diagnostic binary are instrumentation controls, correctly not main baselines. No extra competing service, arithmetic method or kernel baseline is scientifically required for this acquisition; the later GPU comparison still needs the best relevant CPU algorithm and full boundary.

The exact original pools exist: ProofNet 186 contexts/5952 candidates and miniF2F 244 contexts/7808 candidates in experiment014/inputs. All generated candidate outcomes remain in their original order and denominator. I read both pools and found no profiler, skipKernelTC or trustLevel strings in their candidate/header fields. Source-local options remain honored by the native frontend. Build5's archived frontend, appended API and C host match the current files; current builder changes are the diagnostic option injection, separate host/shim object and receipt additions. Native processHeader keeps trustLevel 0 and the existing kernel path.

Metric definitions have an appropriate official source: [pinned Lean Profile.lean](https://github.com/leanprover/lean4/blob/be6c4894e0a6/src/Lean/Util/Profile.lean), [time_task.cpp](https://github.com/leanprover/lean4/blob/be6c4894e0a6/src/library/time_task.cpp), and [timeit.h](https://github.com/leanprover/lean4/blob/be6c4894e0a6/src/util/timeit.h). I inspected the corresponding retained pinned source locally. Native type checking is instrumented in src/Lean/AddDecl.lean:18-25; import, parsing, elaboration, tactic execution, librarySearch and discriminator initialization also have stock timers. These are source-native exclusive elapsed intervals, not CPU work or a complete partition of wall time. The thread-local parent stack subtracts nested same-thread intervals, then aggregates durations globally. Cross-thread waits and overlaps remain possible. Official textual formatting has three significant digits, so terminal category totals are preferable to adding rounded individual lines.

The plan correctly forbids zero-filling missing/open timers, converting summed thread durations to wall fractions/Amdahl limits, or treating incomplete profile coverage as a GPU impossibility. Full input completion and timer completeness are separate. Per-request/outcome strata are valid only with actual attribution; the profiler format itself has no source index or thread identifier. No new attribution substrate is needed to publish honest whole-session categories and coverage limits.

One full pass per cohort is sufficient for this descriptive route-selection role; it cannot estimate a repeat-level performance effect or assert a stable small difference. Whole instrumented timing/resource data are context, while E014 remains the uninstrumented numerical performance experiment. Concurrent host activity and logging overhead bound quantitative interpretation. The live effective affinity was 0–23 at review, so planned 4–7 is currently legal. Disjoint masks do not imply dedicated cores or absence of shared-memory/storage interference. These are limitations, not reasons to interrupt E014 or enlarge E015.

## Executable instrumentation finding

**Blocking finding B1: C++ standard-library ABI mismatch in the proposed shim compile.** bench/build_lean49_prepared_parent.py currently compiles bench/lean_native_profiler.cpp using `g++ -std=c++17 -O3 -c`. That ordinary host compiler uses the libstdc++ ostream type. The pinned official toolchain instead supplies libc++ headers/libraries, and its lib/lean/libleancpp.a has the actual exported signature:

```
lean::display_cumulative_profiling_times(std::__1::basic_ostream<char, std::__1::char_traits<char> >&)
```

This signature was verified with read-only `nm -C` on the existing archive; the sysroot contains libc++.a/libc++abi.a. The shim's declaration using host `<iostream>` names a different symbol, so the planned final leanc link cannot resolve this call. This is an executable linkage defect, not a request for a new timer or comparison. Repair the diagnostic shim compilation to use the pinned toolchain's matching C++ headers/ABI and retain the existing official function call. The exact compiler invocation is an implementation choice for the owner. The planned real off/on preflight will establish actual linkage and timer engagement after the repair; I did not build or run it.

Other inspected pieces are aligned with the plan. Profiling options are inserted into processHeader and Command.mkState in makeRoot, so newly imported roots and their reused options carry profiler=true/threshold=0; rootless candidates use the same path. The C host replacement targets snapshot_stream_main's existing task-manager finalization, then dumps stock global cumulative times before returning. Existing capture uses direct file-backed stderr and graceful stdin EOF for normal retirement/shutdown, so stock `tout()` records (kernel/trace.cpp:133-135 uses io_eprint) and the explicit std::cerr dump do not contaminate JSON stdout. The capture waits for normal process exit and preserves stderr. A killed/crashed session lacks terminal cumulative dump; individual completed timers can remain raw while uncovered work stays unknown. Plan already treats those as partial observations.

The build/capture flags correspond to existing interfaces. Concrete sysroot, Mathlib, dependency path and owned runtime object paths are available in E014 build5-command.json/build5.json. The original source paths are available in experiment014/inputs. This suffices to instantiate the plan's placeholders without introducing another runner. Same diagnostic executable off/on is the necessary preflight control; rejected, complete, incomplete and known search inputs are adequate actual engagement coverage. This review does not ask for an exact diagnostic-string comparison or lifecycle campaign.

## Completion and interpretation

Both whole original pools must reach terminal input accounting, preserve full input/response mapping plus all session profile streams, and reconcile missing/failed/open profile scope before a whole-cohort table is reported. Process exit and cumulative dump must be checked independently of a response. Preserve known crashes/deadlines and any instrumentation-induced operational differences. No accepted-input filtering or stitched partial-run timing is valid. The planned fresh result review should recompute category totals at their official scope and inspect outcome coverage.

No scientific blocking defect beyond B1 was found. Optional command expansion, formatting or additional citations are not execution gates. Once the shim ABI is corrected, proceed with the existing real preflight and two full characterization conditions. A profile dominated by frontend/search selects the expensive observed operation; a kernel-rich profile selects a candidate kernel mechanism. Neither outcome proves complete GPU acceleration, a universal kernel ceiling, RQ4 closure or OSDI acceptance. E014's existing executable, matrix, order and running owners remain intact.


## Round 2 — concrete B1 dependency repair review

Fresh follow-up to the same reviewer, 2026-10-12T22:02:24.472167+00:00. Scope is the B1 compiler ABI repair, the object-path ordering correction, and actual saved build2 evidence. This does not restart the scientific review counter or expand E015.

**Verdict: B1 resolved. No remaining execution-blocking defect is established by this follow-up; the declared real profiler off/on preflight may proceed.** The supporting admission, full two-cohort matrix, native source/outcome policy and timing limitations from round 1 remain unchanged.

I independently read the current builder and plan disclosure, experiment015/build2-command.json, build2.launch.json, build2.log and build2.json, the exact referenced experiment012/build4.json compiler receipt, and build2's archived executed source files. The diagnostic compiler prefix before `-c` equals that E012 receipt's prefix byte-for-byte as a string list. It now uses the existing pinned clang, `-nostdinc++`, and the retained LLVM15 libc++ headers, so this is reuse of the already linked runtime ABI, not a new runtime/header installation or an ostream compatibility shim.

Read-only symbol inspection confirms the concrete repair:

```
# build2/lean_native_profiler.o
U lean::display_cumulative_profiling_times(std::__1::basic_ostream<char, std::__1::char_traits<char> >&)
T gpu_smt_native_dump_profile
# build2/Lean49PreparedBranches
 t lean::display_cumulative_profiling_times(std::__1::basic_ostream<char, std::__1::char_traits<char> >&)
 T gpu_smt_native_dump_profile
```

The object's requested profiler signature now matches the pinned library, and the actual 91,366,808-byte linked binary contains the resolved profiler implementation and C wrapper. Saved log contains the shim compile, Lean generation/object compile, C-host compile and final leanc link; the receipt was produced after those checked subprocesses completed. Build2's archived builder, shim, frontend, appended API and C host all equal the current corresponding source files. Generated host lines 549–551 retain task-manager finalization followed by the enabled official dump, then return. This establishes actual dependency/linkage completion only, not native candidate behavior, timer engagement, full profile completeness or performance.

The separate build1 ordering failure is preserved in build1.log: strict resolution of the not-yet-created shim object failed while assembling commands. The new builder keeps the absolute output-object path without premature strict resolution, while still resolving existing runtime objects. The complete saved build2 demonstrates that this path-order defect is repaired. No additional experiment is needed for that dependency correction.

The plan now discloses both dependency failures and the potentially material acquisition cost, including miniF2F's known 126 real 300-second deadlines. It keeps every original candidate and the same deadline rather than introducing deadline shortening or an elapsed budget. That cost does not change the scientific interpretation or create a reason to alter E014. The earlier illustrative build1 line does not include the new required receipt argument, but the exact runnable build2 command and concrete receipt path are preserved in build2-command.json and build2.launch.json and described in the plan's repair section. Updating the illustrative line would be ordinary documentation polish, not a gate or another review round.

No candidate input, benchmark, build or Git command was executed in this follow-up; only existing files and object/binary symbols were read, and this discussion was appended. E014 and all owners remain untouched. Continue the existing planned real preflight; do not treat successful compilation as a paper result or add baselines, lifecycle probes or an exact-diagnostic campaign.


## Round 3 — official-default observer-overhead repair

Final permitted plan follow-up, 2026-10-12T22:09:09.231814+00:00; same reviewer and scientific scope. I inspected the updated plan/builder, build2-to-build3 executed-source difference, actual saved build3 command/log/receipt and generated Lean source, preflight1 raw streams/inputs/analysis/terminal records, original full-pool projection, E014 full2 ProofNet rep0 W2 snapshot anchor, pinned Profile.lean/time_task.cpp/timeit.h, and the corrected session-count expression.

**Verdict: no result-invalidating defect found in the threshold/default or session-count repairs. Proceed with the already declared identical-input preflight2, then the two full cohorts on that qualified path.** This completes plan review round 3; it does not authorize another review cycle, widen E015 or change E014.

The exact compiled-source difference from build2 to build3 is removal of `.setNat profiler.threshold 0` from the injected enabled options. Shim, native frontend, appended API and C host are unchanged. Build3 generated source has profiler=true without a threshold override, and its archived builder equals current source. Existing build3.json and the complete five-command log now demonstrate a separately linked 91,366,528-byte binary; I did not build or run it. The previously repaired pinned clang/libc++ prefix remains in use.

The change preserves the primary cumulative categories. Pinned Profile.lean:20-24 sets the official default threshold to 100 milliseconds and explicitly describes filtering individual reports. In time_task.cpp:61-68, every enabled timer's destructor calls report_profiling_time with its elapsed duration and excludes nested same-thread elapsed duration from its parent without any threshold condition. The xtimeit destructor in timeit.h:59-63 applies the threshold only to the logging callback. Therefore below-threshold completed intervals are still accumulated in the terminal stock dump; individual below-threshold lines are intentionally absent. These lines must not be reconstructed as complete per-declaration/request data, but that is already outside the declared attribution policy. This is a source-grounded observer-overhead repair, not a weakened timer, altered kernel check or changed outcome criterion.

I independently reconciled preflight1's four exact header/code inputs against original ProofNet sources 0/257/359/2913 (only transport indices remapped to 0/1/2/3). Both modes retain all four native responses, no source issues, and the same rejected/complete/complete/incomplete basic projection as the full E014 anchor. The off/on terminal records are 14.963004561 and 27.257710159 seconds. The on session preserves 988,210 stderr bytes and one cumulative dump with small categories, including type checking 7.96 milliseconds; off stderr is empty. These establish actual instrumentation engagement and the measured dependency observation, not full-corpus correctness or a performance effect. Logging burden is a plausible avoidable observer component, but the single off/on observation does not uniquely quantify its causal share or prove build3's eventual overhead.

Preflight1's saved analysis says zero sessions because it previously counted only worker-prefixed directories. Its actual raw directory has exactly one session-00000000 in each mode. The current session-* plus worker-*-session-* expression returns the correct one for this serial path; this correction changes metadata accounting, not raw execution, source mapping or the native oracle. Original preflight1 evidence remains intact. The updated plan discloses the observation and mutation, preserves all four preflight inputs and full 5952/7808 cohorts, and retains native defaults, original 300-second policy, all failures, complete termination/cumulative coverage reconciliation and the scoped interpretation.

Preflight2 is the already planned real qualification of the changed observation setting, not another scientific comparison or a fourth plan round. It will establish actual final-path timer engagement and basic outcomes; build3 completion alone cannot establish that. No new baseline, timer substrate, lifecycle/thread campaign, diagnostic-string condition or quantitative overhead gate is needed. Whole timed observations remain instrumented and cannot replace E014's numerical performance evidence or be summed into wall-time fractions/GPU ceilings. No benchmark, candidate run, build, Git, source/plan/paper edit or owner/process mutation was performed by this reviewer; only this final discussion was appended. E014 remains untouched.


**Contemporaneous preflight2 addendum within round 3:** while this final review was completing, the declared final-path off/on preflight terminated. I read both saved analysis/terminal scopes and the actual stderr streams: off 14.551459638 seconds/on 15.410091003 seconds, both exit 0, four basic outcomes each equal the E014 full anchor, zero source issues and one observed session each. On stderr is 521 bytes and contains the terminal cumulative categories, including below-threshold attribute application 0.00662 milliseconds. This directly confirms the official-default acquisition still records small completed category totals. The four-source times remain dependency evidence. The earlier round 3 disposition stands: no remaining blocking defect; the planned full two-cohort acquisition can proceed on build3 without another plan review or diagnostic expansion.
