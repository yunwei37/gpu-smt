# Round 11 — cumulative meaning-preservation audit

Parent: `/root`; reviewer: `/root/step2_writing11`. BOOTSTRAP step 0002, WRITE_GATE/W1, serial iter-refine-writing audit. First observed UTC checkpoint: **2026-10-08 01:28:59 UTC**, immediately after initial required instruction/skill reads. Earlier dispatch/read start was not instrumented and is not fabricated. Final review checkpoint: **2026-10-08 01:29:32 UTC**. Report creation follows that checkpoint; the final file-write timestamp is recorded below.

Entry baseline: `d224cd2d991439940e5b4b108b55b53c6a1b8525`, as recorded in Round 0 and explicitly confirmed by parent to contain the exact entry paper/bibliography despite unrelated dirty files. No stash, checkout, new baseline copy, build, paper edit or Git mutation was performed. Read-only `git diff <baseline> -- docs/paper/` and `git show <baseline>:docs/paper/{main.tex,references.bib}` were used. Current source SHA256: `5f2e8f3396ff4b5b0c0e78127454890deb95b398b4ce30217302add1982b74a5`.

## Files, sources and method

Directly read `docs/user-instruction.md` and `docs/questions-for-author.md` first, followed by the full `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md`. Read the entire current `docs/paper/main.tex` and `references.bib`, the cumulative baseline diff, and all eleven Round 0–10 reports including raw findings and appended root dispositions in this directory. Several combined tool responses truncated; separate complete paper, bibliography, diff-part and report reads recovered all missing portions, including the Round 0 disposition and Round 7 findings. No tool invocation was simulated as a Skill tool.

Method: inspect every removed/replaced source sentence in the cumulative diff; match it to an explicit accepted finding/rebuild plan or a retained equivalent elsewhere; inspect surviving technical constraints and scope-bearing qualifiers in context; independently compare exact RQ strings, result-marker strings, citation-expression multisets, numerical-token multisets and bibliography bytes. Intended present-tense completed-system prose is allowed during BOOTSTRAP. This audit checks cumulative preservation, not experimental completion, new scientific framing or further polish. No external browsing is necessary for this internal baseline audit; Round 10 supplies attribution dispositions without a new citation-verification run.

## Raw findings

### Must-fix

**None.** No unrestored technical loss, weakened protected qualifier, changed RQ meaning, changed quantity, lost citation or unexplained substantive deletion was found against the entry baseline.

### Should-fix

**None within meaning-preservation scope.** No further prose revision is requested.

### Consider

**None within meaning-preservation scope.** Deferred implementation, evidence and attribution work already belongs to its recorded research/finalization nodes; this round does not reopen it.

## Cumulative deletion/rewrite trace

| Section / removed or replaced content | Accepted finding or disposition | Preservation assessment |
|---|---|---|
| Abstract background: “related”, “streams of attempts”, and missing explicit declarations | Round 4 background-role derivation from Introduction | Relatedness is still explicit through shared libraries/declarations/accepted context; program/proof candidates and workload remain. No subset expansion or exclusion changes. |
| Abstract cause sentence: native history phrased as tradeoff dependency | Round 4 cause mapping from Introduction | Native scope, heuristics, runtime objects, counters, logical-context distinction and need for behavior arguments remain. |
| Abstract established-reuse requirement expressed as unresolved equal-resource comparison | Round 4 existing-reuse derivation and same-round equal-resource restoration | All four reuse classes, existing savings and equal resources remain; no empirical answer invented. |
| Abstract baseline phrase “established bounded warm and branching services” | Round 4 methodology mapping, using already explicit Evaluation competitors | Competent bounded warm services and native logical/serialized reuse remain established competitors; strongest matched-service result slot and equal-resource qualifier survive. |
| Introduction proof-assistant/SMT explanatory sentence | Round 4 background rebuild, Round 6 Should-fix 3, Round 9 Should-fix 2 | Proof construction/checking and SMT translation remain distinct stages; Lean/REPL citations preserved. |
| Introduction tradeoff/cause topic sentences and “instead” | Round 4 problem/cause rebuild | Preparation replication, isolation, native history and cancellation example remain; only connective/redundant wording removed. |
| Introduction unresolved-comparison sentence | Round 2 Should-fix 2; Round 8 Consider 2; Round 9 Should-fix 3 | Complete verification at matched resources after existing savings remains; cancellation and total process memory clarify existing lifetime/frontier scope. |
| “Realizing” replaced with “Implementing” in Abstract/Introduction | Round 7 Consider 4 | Same separation and safety/configuration/resource/bounded-memory requirements remain. |
| Introduction eight-sentence system overview consolidated | Round 1 Should-fix 1, Round 2 Should-fix 3, complete Round 4 rebuild plan/disposition | Parent ownership/no suffix verification, disposable children, responses/mutation/cancellation, supported quiescence, untouched suffixes, native fallback, bounded retention, inherited native resource state, separate accounting, complete Lean/SMT streams and RTX 5090 full costs remain. Repeated ownership statements are consolidated, not dropped. |
| Background workload-role sentence removed from outcome paragraph | Round 1 Should-fix 3 relocation; Round 8 Consider 4 consolidation | Published/invalid/incomplete behavior controls, failed generated attempts in candidate-stream evaluation, and non-evidence of locality remain in setup and RQ1. |
| Figure “no candidate verification” narrowed to selected post-boundary suffix | Round 3 Should-fix 1 | Clarifies the original preparation-boundary contract; accepted preparation context and no speculative suffix state remain. This does not weaken suffix exclusion. |
| Fallback subject clarified | Round 6 Consider 8 | Interface compatibility, UNKNOWN behavior, unsupported artifact/boundary fallback and mismatch invalidation remain verbatim in substance. |
| Proportional/fleet memory definition moved within placement paragraph | Round 1 Consider 4 | Full definition/citation remain; observed reuse, creation/retention costs, CPU/memory concurrency limits and dirty-page/full-replication cases remain. |
| Placement compressed cost phrase expanded and cross-reference added | Round 7 Should-fix 2; Round 3 Consider 4 | “Observed” and “often enough” survive; no threshold/policy algorithm introduced. |
| Heterogeneous short paragraphs combined, unconditional savings made conditional | Round 1 Should-fix 2; Round 3 Consider 3 | Dynamic binder/constant dependencies, strongest CPU comparison and all cost/representation/synchronization clauses remain; conditional wording restores compatibility with low-locality cases. |
| Device semantics sentence expanded into qualification/online validation explanation | Round 3 Should-fix 2; Round 5 Should-fix 2; Round 6 Must-fix 1/Should-fix 2 and root semantic-claim restoration; Round 9 Should-fix 4 | Original semantic-preservation claim remains explicit. Matched outputs, enclosing proof/artifact validation, UNKNOWN/no-artifact fidelity, required online costs and CPU fallback remain; qualification is distinguished from a second full CPU replay. Accepted clarification does not create a per-operation certificate claim. |
| “Resident primitive speedup” replaced by data-resident checking-operation definition | Round 8 Should-fix 4 partial disposition | Device-resident timing remains separately reported from complete checking; all initialization/representation/upload/download/queueing costs survive. Result slot was deliberately retained pending metric definition. |
| Implementation “both paths” qualification rewritten | Round 7 Should-fix 1, rooted in existing RQ2 protocol | Fresh adapter/original-interface comparison and branches/reference comparison remain, before reuse measurement; unsupported/rejected adapter admission restriction survives. |
| Implementation integration sentence moved from opening to closing | Round 0 Consider 4 | Linux, C++, native SMT evaluation, Lean context reuse and matched CPU/device execution remain explicitly collected; no code-size value invented. |
| Native-adapter repeated comparison subject replaced by “This comparison” | Round 9 Should-fix 5 | Same directly preceding fresh-driver/standalone comparison; original options/scopes/checks/artifacts and branching/interface distinction remain. |
| Device output-identity and established-checker wording rewritten | Round 6 Should-fix 5; Round 8 Consider 1 | Exact identity for each supported checking operation remains, distinct from alternative valid whole-artifact representations; delayed substitution/integer layouts attribution and no-new-algorithm qualifier remain. |
| Evaluation “paper-level questions”, RQ1 passive analysis and RQ3 compressed creation phrase rewritten | Round 7 Consider 6, Round 6 Should-fix 4, Round 7 Should-fix 3 | Four exact RQs, three reuse categories, failed/incomplete attempt coverage and all creation/replacement/cache costs remain. |
| RQ2 “retained through” rewritten as evidence retention for varied comparisons | Round 9 Must-fix 1 | Per-input decisions/artifacts, preceding unrelated attempts, cancellation and resource-limit conditions remain; equality was never established by the baseline wording and is still tested. |
| Combined Discussion/limitations heading removed; limitations relocated/grouped | Round 0 Should-fix 1; Round 1 Consider 5 | Every original supported-backend/runtime, resource-bounded, wall-time/deterministic-work, negative/mixed-range, replay-arrival, corpus fan-out and GPU-boundary limitation survives. Added Discussion derives existing sharing/mutation/lifetime/qualification implications; no result claim added. |
| Related-work caching paragraph reordered | Round 1 Consider 6 | Fine-grained caching, warm comparison, native incremental artifacts/history and assertion-equivalent reconstruction caveat all remain with citations. |
| “Verification specialization alone supplies no novelty” reformulated positively | Round 9 Should-fix 7; Round 8 rejection of stronger replacement | More than specialization is still required; native behavior/bounded sharing test and SOCK/SEUSS attribution remain. Snapshot and representation non-novelty guards survive. |

All remaining cumulative additions are explicit accepted clarifications: quiescent safety in Introduction (Round 2 Must-fix 1), complete source-native SMT frontend interval versus narrower session replay (Round 5 Should-fix 1), and three local citations (Round 10 Should-fix 1/2 and Consider). These do not delete baseline technical content or claim measured results.

## Independent mechanical checks and protected scope

| Check | Baseline | Current | Outcome |
|---|---:|---:|---|
| Exact numbered RQ statements | 4 | 4 | Exact strings equal; no changed/additional/removed question. |
| Exact result-marker strings, including macro marker | 12 | 12 | Equal multisets; no result or evidence obligation invented/deleted. |
| Citation expressions | 34 | 37 | No baseline expression lost. Added one each of `\\cite{boogieCache}`, `\\cite{fork}`, `\\cite{lean4,nanoclo}`, explicitly ordered in Round 10. |
| Numerical-token multiset | 12 | 12 | Equal; includes hardware/structural/layout tokens, no changed measured quantity. |
| Annotated bibliography | Baseline bytes | Current bytes | Byte-identical; no entry/annotation/reference change. |

Manual checks retain complete Lean and SMT-backed verification, original ordered prefix/suffix/options/scopes, no inserted logical scope or warm heuristic check, inherited native solver state with separate service costs, supported quiescent runtime restrictions, branch-owned cancellation/failure, bounded retained memory and proportional fleet accounting, native fallback and artifact-support restrictions, UNKNOWN/resource-bounded behavior caveats, strongest competent service/CPU baselines, matched CPU/memory/admission information, full setup/transfer/fallback costs, post-export/source distinction, negative GPU-opportunity outcome, and RTX 5090. No broad-scope request was narrowed to a metadata primitive or GPU proving workload. The four explicit unanswered endings remain.

## Disposition, artifact evidence and next node

Reviewer-applied fixes: none. Reviewer-rejected fixes: none; no findings require root restoration. Only this report is written. Paper/bibliography/canonical documents and Git remain untouched. Baseline diff also lists regenerated `docs/paper/main.pdf` (155257 to 157240 bytes); binary changes are not independently inspectable by a textual meaning audit. Root's Round 10 log records make exit 0, eight pages, no fatal/undefined-reference errors and retained layout warnings. This reviewer does not claim independent compilation or rendered-PDF inspection. Earlier build evidence is reported as root evidence, not rerun.

Alternative: request cosmetic edits or repeat external citation verification. Rejected because this round only restores cumulative losses, and none was found. Round 10's NVIDIA runtime attribution suggestion remains deferred until the actual evaluated path/version is chosen; that does not represent a lost baseline citation or changed runtime fact.

Decision: **meaning-preservation audit passes with zero unrestored losses**. Next node: parent records disposition and delivers the authorized writing artifact or resumes its outer research node. The skill requires one rerun if restorations are made; this audit requests no restorations.

Report written and completion observed: **2026-10-08 01:30:47 UTC**. No paper changes occurred during this audit.

## Root handoff verification

Accepted the fresh cumulative preservation audit after direct comparison with user scope, full paper and baseline. No restoration requested or made; therefore no unchanged-paper rerun. Root corrects one mechanical-table label: the12 protected strings are actual RESULT invocations; the macro definition is not an extra result slot. All4RQ strings,37citation expressions (34original plus3attributed additions), numerical tokens and bib bytes pass root checks. make exit0 at 2026-10-08T01:32:15.573393+00:00; PDF8pages, no fatal/undefined-reference errors, existing underfull layout warnings. Source SHA2565f2e8f3396ff4b5b0c0e78127454890deb95b398b4ce30217302add1982b74a5. Full12round writing node complete, not a scientific-freeze/submission/acceptance claim. Next paper verify and BOOTSTRAP root audit, then fresh independent step outer audit.
