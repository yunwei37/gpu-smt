# Experiment004 independent result review

Review date: 2026-10-09 UTC; independent raw recomputation began at 15:40:54 UTC. Reviewer read `docs/user-instruction.md`, the complete research-experiment-design skill, and the approved plan before inspecting results. No solver was run, no raw output or runner was edited, and no desired verdict was supplied. Scope is the fresh native frontend constructor discriminator supporting RQ2: **Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?** This run does not itself exercise branching or cancellation.

## Separate judgments

- **Run status: valid.** Complete declared native matrix, with legitimate native error outcomes preserved. The initial derived model-availability readout was defective; the raw results remain valid and independent raw recomputation supplies the corrected interpretation.
- **Tested hypothesis: supported for the matched-source construction-order effect; strict release response identity contradicted by version metadata.** Lazy matches the rebuilt native CLI on every non-statistical response. Ordered checks and model bytes also match the original release, but its version strings differ. Full exact release qualification under the plan is therefore unresolved/does not pass; it must not be reported as unconditional byte identity.
- **Research value: supporting.** A local causal discriminator resolves a specific fresh-interface uncertainty; completion and provenance are not independent scientific contributions.
- **Paper impact: mechanism or workload boundary.** Additional evidence toward one prerequisite of RQ2, without a direct thesis challenge or RQ closure.
- **Next paper decision:** retain the lazy CLI-owned context as the matched-source frontend candidate; reject eager construction as response-preserving on this cohort. Explicitly retain release build-metadata differences in qualification. Move scientific effort to the predeclared decisive native-state branching/service evidence instead of repeating this constructor run or promoting it to a performance result.

## Completion, command and provenance audit

Full-run provenance was written at 15:34:46.740598 UTC and completion at 15:39:39.499520 UTC (filesystem timestamps, not independently authenticated wall-clock measurements). Raw root is `artifacts/native-frontend-2026-10-09/full`; preflight is separate. The provenance command agrees with the approved full command: original retained input directory, release/source/native driver binaries, CPU8, three repetitions, and `full` output. All 156 retained input bytes were independently compared against their original files and matched. Runtime binary, runner, C++ source and parser provenance hashes remain exact. The original full-run analyzer hash matches the initial snapshot `executed-source/analyze_native_frontend_probe.py`; it does not match the current analyzer, which changed after native execution for analysis-only repair. The final analyzer is retained as `executed-source/analyze_native_frontend_probe-final.py`. Initial and universe-only failed derived JSON and intermediate analyzer source are also retained. This provenance clarification updates the same completed review and does not constitute a new run or review. The source commit is `ddb49568d3520e99799e364fb22f35fc67d887b1`, with build commands and toolchain retained in the artifact root. The executed-source copies show one lazy/eager factor: `ctx.m()` before solver-factory/command installation, using the same executable and owned native context. No manager reconstruction, budget subtraction, additional solver call or API-manager baseline is present.

Recomputed unique matrix is 156 × 4 × 3 = **1,872 terminal process cells**, with no duplicate or missing cells. Every process row is terminal and every observed affinity is `[8]`. Each condition/repetition supplies **440 ordered checks, 1,751 get-info requests, five get-model requests, and 2,196 delimited responses**: **5,280 checks and 26,352 response frames overall**. Independently splitting every raw stdout at the native DONE delimiter found every expected frame nonempty, no extras and no trailing unframed output. All stderr files are empty. Release/source/lazy have zero native errors/nonzero exits. Eager has exit1 on streams49,73,90,103 in each repetition: **12 nonzero process outcomes**, all retained, with a native model-unavailable error in each. These are completed negative outcomes, not infrastructure exclusions. No stream was filtered. Forward/reverse/forward condition ordering is implemented; CPU affinity does not establish isolation.

## Independently recomputed response contrasts

All numbers below are per repetition and recur identically in all three repetitions. Independent analysis compared ordered request positions and raw frames, rather than only status counts.

| Contrast | Ordered checks | Other non-statistical frames | Interpretation |
|---|---|---|---|
| lazy versus source | 440/440 identical | Every frame identical | Fresh frontend qualifies against this rebuilt CLI on this cohort |
| source versus release | 440/440 identical | 440 version frames differ; all other non-statistical frames identical | Rebuild control exposes metadata difference; no observed check/model difference |
| lazy versus release | 440/440 identical | Same 440 version differences | Strict byte identity fails; substantive check/model parity is narrower |
| eager versus lazy | Six checks differ on six streams | Five model frames and five reason-unknown frames differ; seven streams differ in total | Constructor timing affects native responses/artifact availability locally |

Release/source/lazy each yield **434 UNSAT, six UNKNOWN, zero SAT**. Eager yields **436 UNSAT, four UNKNOWN, zero SAT**. The aggregate net gain of two UNSAT hides two regressions and four changes in the opposite direction, so it is not a quality or speed win.

| Stream | Command index (zero based) | Lazy/source/release | Eager |
|---|---:|---|---|
| 28 | 901 | UNSAT | UNKNOWN |
| 46 | 5696 | UNSAT | UNKNOWN |
| 49 | 421 | UNKNOWN | UNSAT |
| 73 | 509 | UNKNOWN | UNSAT |
| 90 | 498 | UNKNOWN | UNSAT |
| 103 | 726 | UNKNOWN | UNSAT |

The four UNKNOWN-to-UNSAT streams replace reason `"(incomplete (theory arithmetic))"` with `"unknown"` at commands424,512,501,729 respectively, then their original model requests return native errors. Stream116 has unchanged ordered decisions but changes command6509 reason from `"canceled"` to `"(incomplete quantifiers)"`; this is an additional observable response difference and does not demonstrate externally requested cancellation behavior. No further non-statistical lazy/source or eager/lazy differences were found.

Each release version frame is `(:version "4.16.0")`; source/lazy/eager emit `(:version "4.16.0 - build hashcode ddb49568d3520e99799e364fb22f35fc67d887b1")`. There is one such request per check. These differences affect all156 streams, and remain strict differences under the approved metric. They were not normalized away. Statistical differences are diagnostic and do not establish performance.

## Requested models, correctness and analysis limitation

Raw model responses for streams28,49,73,90,103 are populated native model lists for release/source/lazy, exactly byte-identical across those three conditions and stable across repetitions. Their byte sizes are respectively53,682;30,246;33,560;33,216;52,844. Eager retains a populated model for stream28 of52,861 bytes, differing from the reference; streams49,73,90,103 each return a54-byte native model-unavailable error. Thus release/source/lazy return **five populated model objects per repetition**, eager **one**. Stream28's get-model request is command746 and precedes the later changed check901; its differing model does not arise from requesting a model after that later check. Model requests on the other four streams are commands426,514,503,731.

The initial analyzer falsely marked all models unavailable. It required the original commented text to equal the comment-stripped parsed list, and restricted the first list content to define-fun/model although these native models begin with universe declarations and cardinality constraints. Independent raw examination found one complete balanced native list containing definitions in every populated model frame, with no native error; the four eager error lists are distinct. This defect invalidates the initial derived model-availability fields, not the native run or its byte comparisons. A readout correction on unchanged raw data is analysis repair, not a changed correctness oracle, solver rerun, or new result-review round. Initial derived data must not supply paper availability numbers.

A returned model after UNKNOWN is an artifact, not proof of satisfying the formula. Neither byte identity nor availability establishes semantic soundness; the differing stream28 models were not independently validated. Consequently no semantic-equivalence claim for differing models, no accepted-job increase, and no solver-correctness conclusion follows. Native status/frame comparisons use independent reference paths and retained input request positions, rather than circularly defining success from the proposed frontend's output. No proof/core requests occur, so those artifacts have no coverage.

## Fairness, uncertainty and causal interpretation

The release is the native behavioral reference, source is a rebuild control, lazy is qualification, and eager is a factor ablation. None is a headline speed competitor. Each uses identical original bytes, stdin descriptor semantics, affinity and solver-option budgets; same-executable lazy/eager comparison avoids a build-difference explanation for its local effect. The native reference/control paths engage their intended mechanisms without avoidable interface failure. Eager's model errors accompany changed legitimate solver decisions and are negative observations rather than an invalid baseline exploited as a win.

No post-plan input/budget/solver/correctness-path change was found. File-backed stdin differs from prior pipe delivery but was already declared and equally applied here. Build metadata differences were anticipated by the source control and must constrain claims. All non-statistical raw frames are stable within each condition over three repetitions; this is descriptive repeat stability, not a population confidence interval, hardware-independent determinism, or external validity over fresh candidates. Prior cohort knowledge motivated the factor, but no response-based input filtering occurred. These are retained public proof-replay streams, not new end-to-end candidate-service traffic.

Construction order is sufficient to change responses in this matched implementation; it is not established as the sole cause of prior API discrepancies, and no changed check establishes an incorrect mathematical answer. The strict hypothesis is mixed because the release byte-identity clause does not hold for version metadata even while the constructor-effect clause holds. This finding should narrow the frontend claim without rewriting the hypothesis to fit the result. Prepared-state branching, fork isolation, service fairness/benefit, cancellation isolation, Lean acceleration, RTX5090/GPU checking and all four full RQs remain outside this supporting experiment. No runtime or speed figure is approved by this review.

Final derived-output crosscheck completed at 2026-10-09T15:43:15.570838+00:00. The corrected `full/analysis.json` and `full/summary.json` agree with the independently recomputed terminal matrix, complete checks/frames, and five-versus-one model-object availability in every repetition. This is the sole completed result review of this native run.
