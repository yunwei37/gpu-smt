# Round 11 — cumulative meaning-preservation audit

Reviewer: fresh read-only child `/root/step5_writing_round11`; parent `/root`, BOOTSTRAP step 0005, writing run `iter-refine-writing-20261009T213300+0000`. Objective: audit every cumulative deletion/replacement against the entry paper, including W1 additions and all writing rounds, rather than relying on earlier round verdicts. Initial instruction/source read occurred before the first instrumented clock, 2026-10-09 22:07:18 UTC; exact earlier start was not captured. Review completion clock: 2026-10-09 22:08:01 UTC; final report serialization follows. No model introspection is claimed.

## Inputs, identities and method

Read `docs/user-instruction.md` FIRST, then the full actual `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md`. No Skill tool is available; actual filesystem reads implement the procedure. Read complete current `docs/paper/main.tex` and `references.bib`, recovering truncated output through smaller reads. Read complete round 0–10 reports, including their root dispositions, in this run directory; smaller rereads recovered truncated portions. Ran read-only `git diff 5553bfc67409dd57cdc202ff53d61bf59bce4d40 -- docs/paper/`, and read the baseline main.tex and bibliography using `git show`, without creating a paper snapshot or invoking stash.

Baseline main.tex SHA-256: `4466ec82f8e8977685cc3731cf6c83fd93e396f22ec49d1357c1780be6c058f7`. Reviewed current main.tex SHA-256: `12661aa8ce59a9b7ba68764c0165d39d6406e5652424493813031da0924ff2f4`; bibliography SHA-256: `97cae70d34ddd11566b9ef9d18c63488d79fc9a9956cb5643035a1d174e552e3`. Baseline is the clean pre-W1 paper supplied by the root; consequently the cumulative diff includes new LeanPolish paragraphs/citations, not merely round 0–10 edits.

Read the retained step5 literature report `literature-20261009T202400+0000/report.md`, including its exact declaration-finalization follow-up. Inspected relevant retained primary LeanPolish source passages at `docs/reference/leanpolish-70cda81-LeanPolish.lean` (in particular complete runTacticString), and the retained manifest's provenance. Read `runtime-citation-check.log` and complete `docs/reference/nvidia-container-toolkit-a672e37-README.md`. The LeanPolish PDF is retained at `docs/reference/leanpolish-2609.38384v1.pdf`; this audit uses the earlier grounded literature record rather than claiming a fresh whole-PDF/source-authenticity verification. No external lookup, native execution, build, code edit, canonical edit, Git mutation, or agent delegation occurred.

Method: inspect every changed diff hunk; map deletions and replacements to an explicit round finding/rebuild plan or retained redundant statement; compare native reference, supported-boundary and parent ownership semantics; separate qualification, execution and accounting; compare exact RQs, cited keys, number strings and result slots. Present-tense intended BOOTSTRAP system prose is authorized and is not delivered-implementation evidence. Missing results remain protected.

## Must-fix

**M1 — Abstract methodology, main.tex line 21: restore the explicit after-preparation-reuse qualifier.** The baseline states, “After preparation reuse, we assess remaining heterogeneous checking …”. Current combined methodology instead says, “… then assess remaining heterogeneous checking …”. “Then” expresses sequence after the preceding comparison; it does not explicitly identify preparation reuse as the cost boundary. “Remaining” has no explicit preparation-reuse antecedent within that sentence. This is a small cumulative scope loss in the abstract even though Introduction, Design, RQ4 and its evidence block retain the correct condition.

Round 1 S2 orders combining the two methodology sentences **while preserving** their measurement boundaries; Round 4's rebuild plan likewise protects heterogeneous assessment after reuse. Neither authorizes removing this scope qualifier. Concrete restoration only: change the connecting phrase to “then, after preparation reuse, assess remaining heterogeneous checking”. Retain all comparator, complete-verification, RTX 5090, setup/transfer/CPU fallback and result-placeholder text. This introduces no new claim or polish. Root should compile and perform the required one-time restoration audit afterward.

## Should-fix

None within this restoration-only audit. Round 3's deferred concrete placement-policy specification is an existing scientific-contract follow-up, not cumulative writing loss; do not invent its missing policy here.

## Consider

None. Additional polish is outside Round 11.

## Complete deletion/replacement tracing

The following groups cover every changed source hunk; unchanged intervening passages were read for preserved meaning.

| Deleted/replaced material | Authority and surviving content | Audit finding |
|---|---|---|
| Abstract background/problem/cause/reuse/insight/challenges wording | Round 4 role map/rebuild, deriving abstract last; native history, equal-resource uncertainty, lifetime separation, quiescence/resources/bounded memory retained. Dropped isolated “native” before “preparation” remains defined by native-state mechanism and original preparation throughout. | No scope loss apart from M1. |
| Two methodology sentences merged; abstract result slot extended | Round 1 S2 and Round 2 C1; all comparison/device costs retained and existing measured-device-scope placeholder aligned. | M1 identifies the one qualifier requiring restoration. No result invented. |
| Seven introduction prose paragraphs reordered/rephrased | Round 1 S1/C1, Round 2 S1 and explicit Round 4 paragraph-by-paragraph plan. Streams/interfaces, repeated imports/parsing/objects, cancellation example, Z3 scope/heuristics/counters, Lean mutable state, every reuse capability, matched uncertainty, costs/pages, timers/descriptors, budget/frontier, branch responses/communication/accounting and fallback all survive. “Executes independently” is redundant with independent attempts and explicit absence of other-candidate history/lifetime influence. Preparation changing remaining cost distribution survives in Design heterogeneous opening and intro after-reuse boundary. | No untraced technical deletion. Contribution list unchanged. |
| Background proof-verification policy and behavior cross-reference shortened | Round 1 S3 moves policy to Experimental setup; neutral distinction remains in Background and exact outcomes remain in Observable behavior. | Admissions, unfinished obligations and diagnostics preserved, rather than silently compressed away. |
| W1 finalization paragraph and LeanPolish comparison added | W1 retained primary source/literature follow-up; Round 1 S3 relocates policy; Round 6 S3/S4 splits clauses; Round 8 C1 replaces negative novelty aside with established-baseline classification. | Tactic-screen success never becomes original declaration acceptance. Both new citations remain. |
| Prepared-state additive conjunction and two local Z3 attributions | Round 9 C1, Round 10 S1/C2. Native ordered options/declarations/assertions/scopes and internal-work-versus-time distinction retained. | No semantic drift. |
| ASCII boxed architecture and caption replaced with TikZ | Round 0 S1 and root diagram disposition; same stream/configuration→placement→supported boundary→prepared prefix→independent branches→CPU/supported-device→responses path; native fallback stays separate. Explicit cancellation and teardown display existing semantics. Round 6 S1 changes punctuation only. | Parent no-verification restriction remains explicitly **after selected boundary**, not before preparation. All previous flow information survives. |
| Design overview ownership/dispatch wording combined then split | Round 6 S6 and Round 9 S1/root alternative. | Supported branches own mutation/lifetime and use CPU/device; unsupported boundaries use native execution. No arbitrary unsupported branch implied. |
| Observable behavior reference clarification and punctuation | Round 3 S1, Round 6 S2, Round 7 S1. | Accepted original preparation retained; preceding alternative suffixes excluded; candidate's own native session history retained. Original suffix executes once, no extra scope/warm check. |
| Device lifetime/accounting sentence added | Round 5 S1. | Candidate attribution until completion/cleanup clarifies original independent lifetime/full-cost goal; no new preemption or broker mechanism. |
| Resident-device operation sentence rewritten | Round 6 S5. | On-device data condition remains explicitly scoped to operation speedups separately from complete checking. |
| Fresh “driver” renamed “adapter”; EOF expanded; source-adapter connection clarified | Round 8 S1/S2 and Round 1 C2. | Same original standalone interface, same-source executable, diagnostic rejected adapter boundary, parser split controls and narrower session replay boundary retained. |
| Process communication/reaping/accounting clauses joined | Round 6 C1. | Quiescence, no candidate suffix in parent, separate descriptors, response/cancel/failure reaping and counter/accounting distinction survive. |
| Wall-time scope subject rewritten | Round 7 S2. | Measured operational limit becomes more explicit; no inference of deterministic equality from inherited counters. |
| NVIDIA runtime identified; fidelity and cost clauses joined | Round 10 S2/root source check; Round 6 C2. | Container runtime identification, not CUDA API/version inference. RTX 5090, matched operation identity, native artifact fidelity, CPU fallback/runtime costs and existing representation caveat retained. |
| Setup metrics paragraph split and outcome policy inserted | Round 1 S3/C3, Round 6 S3. | Original raw outcomes/repetition order, every cost stage, fleet memory, throughput versus latency and native enclosing proof acceptance rule remain. |
| RQ4 accounting bridge and plain phrase | Round 3 C1 and Round 7 C1. | Complete costs connect to RQ3 matched boundary; primitive improvement does not establish service improvement. |
| Stock snapshots/Kimina sentences combined | Round 6 C3. | All capabilities, bounds and citations survive. |
| Caching transition, checker demonstrative clarified | Round 9 S2 and Round 7 C2. | Original session-history distinction and strongest alternative representation/checker comparison remain. |
| Bibliography | Cumulative diff appends two W1 LeanPolish entries and Round 10 NVIDIA entry only; existing 21 entries and annotations are unchanged. | No citation metadata or quantitative evidence removed. |

## Protected meaning and mechanical checks

Exact canonical four RQ strings match baseline byte-for-byte. RQ1 independence qualifier appears in the opener too; Round 5's proposed change was correctly logged as already satisfied. All four evidence blocks retain unanswered endings and measurement requirements. Twelve result placeholders remain twelve; only the abstract placeholder gains the already existing measured-device-scope requirement. No measured number appears.

Baseline has 40 cite commands/21 bibliography entries; W1 adds four cite commands/two entries, giving the 44/23 recorded during rounds 0–9; current has 47/24 after Round 10. No baseline cite key/group was removed. Existing bibliography entries are unchanged. Numeric source-token differences are TikZ sizing/diagram layout replacing boxed-diagram dimensions; hardware RTX 5090 occurrences and substantive numbered goals/RQs are unchanged. No scientific quantity was revised.

Native preparation retains ordered configuration and runtime state, original accepted context, scopes and requested output. Parent carries no learned/elaborated post-boundary candidate state. Supported quiescent point/no pending work/no external effects remain; arbitrary native-process cloning is explicitly excluded. Inherited native solver resources remain distinct from service CPU/elapsed charging and changed process timers/descriptors. Qualifications compare fresh adapter against original interface before branches or performance; complete/split parser controls, rejected diagnostic-only paths and residual differences remain explicit.

Full Lean source versus post-export kernel replay versus menu screening remain distinct. Lean admissions/unresolved obligations remain outcome controls. SMT SAT/UNSAT/UNKNOWN, requested model/proof/core artifacts, semantic artifact validation rather than byte identity, and UNKNOWN-to-UNSAT client difference all remain. Unsupported boundary/artifact native fallback is distinct from unsupported device operation CPU fallback. UNKNOWN is not a universal divergence detector.

Device offline qualification, enclosing native checks where an artifact exists, charged required online checks, no universal full CPU replay, artifactless outcomes, CPU fallback, representation/setup/upload/download/queueing/synchronization and candidate cleanup accounting remain protected. Strong bounded warm/cache/native logical/serialized reuse and strongest complete CPU checker remain competitors. Wall-time equality is explicitly measurement-scoped in Design, Implementation and Limitations. Negative/mixed results, mutable-extension/version deployment scope and real-traffic-versus-replay limitations remain intact.

LeanPolish remains a preprint/actual attempt source and established native-reuse comparison, not proof that all menu alternatives were fully checked declarations or complete historical service traffic. Retained literature appendix substantiates the success/finalization distinction. NVIDIA mechanical log establishes URL reachability and explicitly skips unavailable API metadata; manual primary README identification is recorded in Round 10, not misreported here as an API metadata match or installed-version proof.

## Disposition, validation limits and next node

Raw findings: one Must-fix, zero Should-fix, zero Consider. No restoration was applied by this read-only child. Alternative of relying on the body to supply the abstract's lost after-reuse qualifier is rejected because the audit explicitly protects each claim's scope; restoring the few original words is sufficient. No broad rewrite is warranted.

Only this report was written. No paper or canonical source, memory, native evidence, Git state or runtime was changed. Earlier round reports record successful eight-page builds, but this reviewer did not build or inspect a fresh rendered PDF and makes no independent compilation claim. This is a meaning-preservation audit, not empirical implementation validation or fresh all-citation verification. Root owns M1 restoration, compilation and the required one-time confirming audit; final delivery remains pending those actions.

Report completed: 2026-10-09 22:09:24 UTC (final instrumented clock). The 22:08:01 observation above marked the evidence/check stage; finding assessment and serialization continued until this completion.

## Root restoration 2026-10-09T22:09:50.547320+00:00

M1 accepted and restored explicitly after preparation reuse in abstract methodology, retaining the one combined method sentence and every comparator/device/full-cost qualifier. This was a scope-bearing omission introduced during prior sentence combination, not merely optional polish. No other changes at Round11. round-11-build.log exits0/eight pages;47citations/24entries/12slots/fourRQ unchanged. Requested one-time confirming audit from same fresh cumulative reviewer, append to this report; completion not claimed before return.

## Required one-time confirming restoration audit

Started: 2026-10-09 22:09:59 UTC. Completed: 2026-10-09 22:10:05 UTC. Same reviewer `/root/step5_writing_round11`, parent `/root`, same step/run and baseline `5553bfc67409dd57cdc202ff53d61bf59bce4d40`. This is the authorized confirming audit, not another writing cycle.

Read the updated source and reran read-only cumulative `git diff` against the same baseline, including source/bibliography and the rebuilt PDF binary difference. Recovered truncation with a decisive read-only identity check: replacing only the exact restored phrase in memory with the pre-restoration phrase reproduces the previously reviewed whole-source SHA-256 `12661aa8ce59a9b7ba68764c0165d39d6406e5652424493813031da0924ff2f4`. Thus the sole source change since the full cumulative audit is precisely M1's restoration. No paper snapshot was created. Current source SHA-256 is `2d8aca34ae25b53eca9cd8ca18793a63671da08a07554349c2e4acfa66f38a1d`; bibliography remains `97cae70d34ddd11566b9ef9d18c63488d79fc9a9956cb5643035a1d174e552e3`.

**M1 confirmed restored:** Abstract methodology explicitly says “then, after preparation reuse, assess remaining heterogeneous checking”. The original preparation-reuse cost boundary is again explicit in the abstract and agrees with Introduction, Design and RQ4. Complete verification, strongest matched native/warm competitors, RTX 5090, full setup/transfer/CPU fallback and the honest results placeholder remain unchanged.

**Must-fix:** None remaining. **Should-fix:** None within restoration scope. **Consider:** None. No new counterfinding or cumulative loss identified. All earlier deletion tracing and preservation findings remain valid. The identity check establishes that scoped post-boundary parent ownership, supported quiescence, original preparation/suffix/history, interface qualification, native counters versus service accounting, full source/post-export/menu boundaries, UNKNOWN/artifactless outcomes, supported artifact validation, fallback and wall-time measurement qualifiers have not changed. Exact four RQs still match the baseline, cite commands remain 47, bibliography entries 24, and result slots 12; no empirical value or device success was inserted.

Read the retained `round-11-build.log`: actual latexmk output reports `main.pdf (8 pages, 187983 bytes)` and all targets up-to-date. Root separately reports make exit 0. The retained log contains underfull-box notices, with no fatal compilation error. This reviewer did not execute a build or inspect rendered pages and does not equate successful compilation with empirical verification. The binary PDF difference is expected from the root rebuild, not an unexplained source edit.

Only this confirmation was appended to the existing report. No source/bibliography, Git, canon, memory, code or native data mutation occurred. No polish, new result or scientific claim was proposed. Required restoration audit is complete; the cumulative meaning-preservation gate now has no unrestored loss. Root retains final PDF delivery and broader scientific-contract ownership.
