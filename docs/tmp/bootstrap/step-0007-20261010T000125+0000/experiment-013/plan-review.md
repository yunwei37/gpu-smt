# Experiment013 plan review discussion

## Round 1 of 3: public-header implementation

Observation: 2026-10-12T18:21:12.461633+00:00. Fresh independent reviewer; no native candidate execution, implementation edits, experiment-plan edits, or Git publication actions. This is the first review of the public-header/native-default implementation, not another round of E010 or E012.

**Verdict: no blocking scientific or executability defect identified. Proceed to the declared real preflight, then the planned complete performance comparison if it executes.** Compilation is setup evidence only; this review supplies no performance result or arbitrary fork-safety guarantee.

### Material read

Read the complete research-experiment-design skill, docs/user-instruction.md, current thesis/RQ contract in docs/idea-story.md, docs/evaluation.md, docs/background-related-work.md, E013 plan, Lean49PreparedAPI.lean.inc, lean49_prepared_parent.c, lean_capture_prepared.py, build_lean49_prepared_parent.py, current lean_capture_snapshot.py and Lean49NativeSnapshots.lean. Also read the outcome interpreter and ResourceCapture implementation and the relevant E008/E010 plans to distinguish existing evidence. Verified the isolated build command/receipt and actual source assets by filesystem reads. Primary source checks opened the pinned Lean frontend, Linux proc documentation, SOCK and SEUSS linked below.

The latest user instruction is “不需要正确性这么纠结”. The plan preserves basic stock proof outcomes and known countercases without reopening diagnostic-name equality or a cancellation campaign. That is consistent with the requested focus on acceleration. Existing E010/E012 criteria and findings are historical; this experiment states a different, narrower performance contract rather than retrospectively changing them.

### Does it test RQ3 and add decision-relevant evidence?

RQ3 is: **How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse?** The proposed path prepares published imports/options/open commands only, passes the stock incremental header snapshots into disposable children, and never prepares a candidate body in the parent. The actual Lean API calls processCommandsIncrementally with the original post-import state and stock previous snapshot tree; it does not adopt a candidate terminal environment as the next initial environment. Header-ineligible sources are checked through the native fresh-root fallback rather than omitted.

The comparison therefore tests a real consequence of shared header preparation plus disposable candidate execution against persistent native reuse. It is narrower than theorem-prefix preparation or a full bounded service. It can be decisive for whether to retain this concrete mechanism, while providing scoped additional RQ3 evidence. Neither a positive nor negative result alone settles the whole thesis, service frontier, SMT scope, or RQ4.

The admission argument holds. E008 tests different preparation-depth reuse on LeanPolish serial edits, and E010 uses the import-only parent with the old forced one-thread setting. Those paths do not settle the new header snapshots with ordinary native scheduling. E012 preflight/thread-ownership evidence does not quantify throughput or memory. A complete matched run can select or reject this mechanism; another standalone cleanup/string investigation would not. The plan's strongest competing explanation is meaningful: file-backed imports and deeper native snapshot reuse may already capture preparation, while per-child startup, COW mutation, and repeated runtime setup may erase the proposed benefit. A matched baseline win would reject superiority for this mechanism/workload, and a reproducible throughput/private-memory tradeoff would justify further service evaluation.

### Baseline, assets, correctness and fairness

The single main baseline is credible and strong for the pinned workload. The current baseline source retains per-header previous native command/child snapshot trees, reuses genuine post-import state across headers, and continues through persistent stdin workers. DATASET_SIZE retirement means healthy workers are retained throughout each whole condition; failure disposal is visible. It is not an import-only or cold-start strawman. A numerical comparison is necessary because functionality/published measurements cannot determine the complete costs of these exact candidate bytes. No extra baseline is required for this admitted same-version mechanism comparison. The background map's current modern serialized reuse, Kimina and other service competitors remain relevant to later broader superiority claims; this experiment does not claim to beat all of them.

Actual assets are present. ProofNet's complete projection contains 5,952 code records and 186 tasks, with 17 published headers, at artifacts/lean-generated-2026-10-07/proofnet-full-pool-20261011T220000+0000/{to_inference_codes.json,selected_tasks.json}. The retained miniF2F recovery segments contain 832 and 6,976 candidates (26 and 218 tasks respectively), totaling the stated 7,808/244 cohort. The plan correctly treats these as generated-candidate verification replay and discloses segmented generation; it does not turn replay elapsed time into proving accuracy or uninterrupted generation time. The finite driver must use the exact previously reconciled complete order, as already required by the plan.

Both sides use the same pinned source, dependencies and owned runtime objects. The isolated build1 receipt confirms Lean4.9.0-rc1/be6c4894e0a6, the declared Mathlib dependency path, and successful compiler/link commands. Prepared capture removes LEAN_NUM_THREADS under --native-runtime-default, and the C child calls lean_init_task_manager(), rather than forcing a one-worker manager. Snapshot capture inherits the launch environment, so the plan's explicit removal of inherited overrides before both launches is necessary and sufficient. W is job/CPU-budget width, not a promise that each Lean process has one native thread. Same condition CPU masks, original source bytes, failure policy and native defaults give a fair complete-cost comparison; runtime thread counts may differ as a consequence of different process architectures and must be reported rather than equated by assumption.

Outcome checking is sufficient for this scoped performance claim. The unchanged native frontend still elaborates and invokes stock proof checking; the source-native accepted/rejected/incomplete rule is based on actual errors/sorries, not transport success. Per-input identity, all operational failures and outcome differences remain visible. Reusing the collected baseline plus retained producer anchors is reasonable; exact error spelling/metavariable numbering is not needed to veto this outcome/performance comparison. Genuine acceptance/incompleteness disagreements or method-specific lost work would invalidate the affected speed comparison. Nothing in this review requires a new full fresh oracle stream, diagnostic-string campaign or cancellation campaign.

### Metrics, costs, real commands and completion

The complete wall-time/throughput, waited CPU and sampled process-tree memory measurements have standard primary sources: [SOCK ATC2018](https://www.usenix.org/system/files/conference/atc18/atc18-oakes.pdf), [SEUSS EuroSys2020](https://handong32.github.io/docs/3342195.3392698.pdf) and [Linux proc documentation](https://docs.kernel.org/filesystems/proc.html). The mechanism uses the [pinned Lean incremental frontend](https://github.com/leanprover/lean4/blob/be6c4894e0a6/src/Lean/Elab/Frontend.lean). No project-weighted score replaces a standard metric.

The existing capture CLIs expose every required plan argument. Whole taskset/GNUtime/capture command wall time includes setup, inputs, preparation, candidate work, transport/persistence, replacements and final cleanup. Prepared C waits for owned children; snapshot capture uses graceful EOF and waits/reaps disposed workers. This supports waited descendant CPU accounting. Baseline per-request fsync has been removed, so only the baseline is not penalized with a forced persistence operation. Capture formats still differ, but complete command cost is an implementation measurement, and neither side is allowed to substitute its narrower native interval as end-to-end time.

The actual sampler is 1 second on both sides and includes the acquisition root and native descendants, with process identity/allowed CPUs/threads/error records. The plan correctly calls these sampled peak PSS/private values, discloses gaps, and separates resource profiles from uninstrumented throughput; it does not infer a simultaneous Pareto frontier from separate campaigns. Candidate admission-to-terminal latency is correctly labeled closed-loop response cost. Three whole repeats support individual values and ranges; they do not justify invented significance or production queueing tails.

The 36 uninstrumented plus 12 resource-profile conditions all test the same mechanism relation and are sufficient for the declared CPU-width replay comparison. The preflight uses real first-task candidates and prior real nested-task countercases at widths1/2 and does not inflate setup into research progress. The complete terminal rule preserves original denominators and excludes partial-prefix throughput. Affinity/OOM/transport defects retain raw failures and require affected whole reruns; current build success does not bypass those checks. Exact argv and concrete combined-input paths are to be retained before acquisition as the plan requires; an ordinary finite driver implementing those commands is acquisition glue, not a new service or control gate.

### Actionable blocking defects

None identified. Run the declared preflight; repair any concrete execution failure within the existing protocol. This review is not contingent on added baselines, a larger workload matrix, equal diagnostic strings or a further cancellation test.

### Optional suggestions and interpretation limits

- In the result table, show normal-response throughput as well as terminal-attempt throughput and all outcome counts. A fast crash or timeout is not useful verification throughput. This is already implicit in the plan's separate counts and is a reporting suggestion, not an execution blocker.
- State CPU budget and observed native thread counts together. A width4 pool may contain substantially more than four native threads under stock defaults; this does not make CPU affinity4 unfair, but calling it four threads would misdescribe the experiment.
- Keep header-preparation event/reuse counters alongside results, so a null result can distinguish a small prepared prefix from large COW/startup costs. Existing native output already supplies this evidence; no additional instrumentation campaign is requested.
- Keep the current inference limits explicit: shared-host contention, dynamic allowed masks, coarse memory sampling, separate resource profiles, closed-loop candidate dispatch, no exact-result cache condition, and no newest-version cross-toolchain numerical claim. Do not promote a narrow replay improvement to generic service superiority.

### Return

Plan admitted for the specified real preflight and complete performance acquisition. Expected research value: decisive for selection of the concrete public-header mechanism; paper impact: additional scoped RQ3 evidence or a mechanism/workload boundary. Actual run validity, numerical effect and paper numbers remain for the independent result review after completion.


## Follow-up round 2 of 3: synchronous public-header preparation

Observation: 2026-10-12T18:28:00.562444+00:00. Narrow review of the actual preflight1 failure and the changed parent preparation path. Read current Lean49PreparedAPI.lean.inc, C prepare_native and native-manager/guard call sites, the plan amendment, build2 receipt, preflight1 analysis/comparison summaries and the three actual refusal events. No native candidates, further experiments, implementation/plan edits or Git publication actions executed by this reviewer.

**Verdict: no new blocking scientific or executability defect identified in this repair. Proceed to the already declared preflight2, then the unchanged complete matrix if it executes.** The operational failure in preflight1 remains real and retained; build2 compilation alone does not establish successful execution.

### Evidence and scope

All six snapshot baseline conditions returned their expected responses. Three of six branch conditions refused before any candidate launch: miniF2F first32 W1/W2 each report live_tids=2 and foreign_fds=0; ProofNet first32 W1 reports live_tids=5 and foreign_fds=0. The other three branch conditions returned all36responses with no source issues and matched baseline outcomes: ProofNet first32 W2 rejected32, miniF2F countercases complete1/rejected1, ProofNet countercases incomplete1/rejected1. The three failed conditions retain missing_result32 each; these 96 missing results cannot become verification throughput or a superiority result. This supports the amendment's retained-execution-failure disposition and does not establish the cause or lifetime of any residual thread.

The current prepare_native installs/finalizes an ordinary task manager only for historical mode=full. In E013 mode=header, preparation uses the parent zero-worker manager already initialized before dynamic imports. The Lean API still executes process full on input.header only and retains stock header incremental snapshots. It never executes candidate bodies or adopts a candidate terminal state in the parent. Serial and concurrent children still use lean_init_task_manager() and finalization; the native-default candidate comparator and baseline remain unchanged. The one-TID and descriptor ownership refusal checks remain in place. This is a concrete change to execute the admitted mechanism, not a guard relaxation, changed oracle, expanded cancellation claim or different selected RQ.

Synchronous parent preparation and default-threaded candidate execution are intentionally different stages of the proposed system. This does not invalidate matched candidate-resource comparison: all preparation/runtime setup and subsequent checking costs are charged in whole-command time/CPU, and both methods receive the same CPU entitlement and native-default candidate scheduling. It does mean any observed effect belongs to the complete public-header/synchronous-parent/disposable-child implementation, rather than COW in isolation. The amendment explicitly discloses that configuration, so no extra scheduling ablation is necessary for this plan's whole-system claim.

The strong persistent full-snapshot baseline, actual corpus, original headers, source-native outcome rule, CPU widths, completion denominators, primary metrics and expected/contradictory paper decisions are unchanged. The second preflight repeats the same12real conditions and counts as attempt2/3 without resetting the budget. That is the right execution check for this repair. No further diagnostic-string equality, thread-lifetime study, wider matrix, baseline or cancellation campaign is needed before the planned performance acquisition. If the actual second attempt still fails, preserve and handle that concrete failure under the existing protocol rather than interpreting omitted work as a win.

### Actionable blocking defects

None identified in the amended plan/implementation path. This follow-up does not claim that the still-pending preflight2 succeeded.

### Nonblocking factual correction and optional suggestion

- The amendment's phrase “observed5parentTIDs” is incomplete for the retained raw evidence: miniF2F W1/W2 observed2, while ProofNet W1 observed5. Correcting it to observed2/5 is sufficient; there is no need to investigate thread histories to report the actual failure accurately.
- In eventual result prose, describe the parent as synchronous header preparation and candidates as native-default scheduling. Several old C comments still say one-worker/import-only; they are stale comments rather than the behavior of the executed call sites and do not block execution. Existing runtime/config receipts supply the authoritative evidence.

### Return

Retain round1's scoped admission. This repair permits the declared second real preflight; full RQ3 numerical interpretation remains conditional on complete matched acquisition and independent result review. Prior failed build1 conditions remain excluded from performance superiority and visible as operational evidence.


## Final follow-up round 3 of 3: stock synchronous command-state preparation

Observation: 2026-10-12T18:37:30.533911+00:00. Reviewed current Lean49NativeSnapshots.lean, Lean49PreparedAPI.lean.inc, builder checkpoint injection, final plan amendment, completed build3 receipt and retained preflight2 summaries/assertion output. Also read the pinned Lean Frontend.lean definitions and actual producer REPL/Frontend.lean call sites. This is the final plan follow-up in the same discussion. Reviewer performed no native candidate execution, implementation/plan edit or Git publication action.

**Verdict: no new blocking scientific or executability defect identified in the final source-native repair. Proceed to the declared third/final real preflight; complete the same48-condition performance matrix only if that path executes.** This source review and build receipt do not count as successful preflight or performance evidence. If the third attempt cannot execute, close this public-header proposal incomplete under its existing protocol; do not reset the review or preflight count.

### Retained failure and actual source-native boundary

All12preflight2conditions terminated. Every branch condition returned no candidate result and asserted g_task_manager; the six normal baseline conditions retained their expected outputs. This is an actual operational failure, not negative verification or fast service completion. The old zero-manager/incremental-parser proposal was unexecutable. Round2's source-only admission did not establish that path ran, and the recorded failure supersedes any executability inference for build2 without rewriting its reviewed rationale or raw evidence.

The pinned frontend confirms IO.processCommands executes the ordinary Frontend.processCommands loop and returns complete State with commandState/parserState. IO.processCommandsIncrementally instead invokes Language.Lean.processCommands and consumes snapshot tasks. The installed official REPL's processCommandsWithInfoTrees calls IO.processCommands. Build3 therefore changes to a real source-native synchronous interface, rather than inventing a parser/checker or weakening an assertion.

The parent now executes IO.processCommands on input.header only, using original root.parser/root.initial, then saves state.parserState and state.commandState in optional Root.headerParser/headerState. It never runs the candidate body. processHeader/trust0/post-import sharing remain original. makeRoot explicitly clears both optional fields, as well as previous, when it constructs a distinct header from shared imports; header options/open scopes cannot leak through that sharing shortcut. Eligibility still requires exact recorded header/source prefix and matching import bytes. Ineligible candidates retain the source-native rootless fallback. Each child invokes stock incremental checking from the stored header position/state and the ordinary native task manager. Candidate final state is discarded with that child.

The builder's changed checkpoint injection wraps the actual incremental child call while preserving its parser/state arguments. The compiled build3 receipt records the isolated binary and successful stock compiler/link commands with the existing owned runtime objects. The strong persistent baseline remains its existing full-snapshot binary with original post-import initial state and genuine candidate-to-candidate snapshot retention; optional public fields are not set by the baseline path. No comparison input, CPU width, candidate scheduler, source-native outcome rule or matrix has changed.

### Scientific consequence

This remains the admitted RQ3 hypothesis: does sharing real public preparation plus independent disposable candidate execution change complete latency/throughput/memory compared with competent warm native reuse? It now uses a stock complete public Command.State, not a parent incremental command-snapshot tree. That is a disclosed implementation mechanism change within the same expected/contradictory decision, rather than a new RQ or a separate experiment. Complete throughput/private-memory selection remains consequential even if a generic incremental-tree novelty claim is unavailable.

The public header's parsing/elaboration is paid once in the parent, including its actual synchronous implementation costs. Candidate parsing/elaboration/proof checking remain stock and default scheduled. The full baseline is permitted to exploit more retained native snapshot state and candidate history, as intended. Different preparation routes are the competing systems being measured, not an unequal submitted-proof or CPU budget. Any eventual gain belongs to the complete command-state-preparation/disposable-child design; it cannot be attributed exclusively to COW or intra-command snapshot reuse without additional evidence, which is not required for this whole-system experiment.

The finite final preflight is the appropriate existing check that the resumed parser position reaches the actual candidate bodies and native proof outcomes. The already planned first32cohorts include complete and rejected proofs, and real countercases include incomplete behavior, so a hypothetical empty/header-only response path would not qualify via transport success. No extra diagnostic-string equality, fresh oracle campaign, baseline, wider workload or cancellation exercise is scientifically necessary. Earlier E010/E012 protected-feedback criteria/findings remain preserved and do not turn this narrower comparison into an exact arbitrary API-transparency claim.

### Actionable blocking defects

None identified in the final amended source-native path. Actual completion, outcome equivalence and mechanism engagement remain observations for the declared third preflight; an assertion or guard refusal is not excused by this verdict.

### Nonblocking reporting corrections and optional suggestion

- The original opening paragraph still says parent preparation produces “stock incremental snapshots”. The latest amendment is explicit and controlling; revise that opening wording to stock synchronous public command-state preparation for consistent result reporting. Do not claim parent child-snapshot-tree preparation from build3.
- Branch old_snapshot_supplied and reused_command_snapshot_prefix may correctly be0 because its preparation is now a Command.State. Use the already emitted public_header_state_supplied, public_header_only/preparation_frontend and source-native output outcomes to report actual engagement. An old snapshot-tree counter alone is no longer the branch engagement test; no new experiment or instrumentation campaign is requested.
- Keep all build1/build2 refusals/assertions and missing work visible, and report build3 configuration/raw commands as the eventual evaluated method. Do not stitch failed-prefix timing into completed performance cells.

### Final return

All three plan-review rounds are now recorded. The final proposal remains admitted for its final real preflight and, if executable, the same complete48-condition matched performance acquisition. Expected impact remains scoped additional RQ3 evidence or a concrete mechanism/workload boundary, with no generic fork novelty, complete service frontier, GPU result or whole-thesis conclusion. Independent result review still determines actual validity and numerical claims after terminal acquisition.
