# Round 7: complete-paper word-choice review

Started: 2026-10-09T21:57:53Z (first recorded clock reading after required source reads). Completed: 2026-10-09T21:58:05Z (review completed; report written subsequently).

Parent: BOOTSTRAP step-0005-20261009T194100+0000, serial iter-refine-writing-20261009T213300+0000. Objective: independent read-only word-choice review of the entire intended completed submission. Entry source: `docs/paper/main.tex`, SHA-256 `d50b6df22ac6ed4bc763f37223cf5140263f05564d550208d08627b5136b83c7`.

Read `docs/user-instruction.md`, the complete actual filesystem `paper-writing-style/SKILL.md` and `iter-refine-writing/SKILL.md`, and all 236 lines of `docs/paper/main.tex`. No previous review, evidence/canon/code files, Git operation, agent delegation, native execution or compilation was used. The parent applies and validates any accepted suggestion.

Method: sentence-by-sentence review for hidden verbs, inflated or stacked compound modifiers, referent ambiguity, hedge redundancy and verbose phrases. A supplementary Python3 token scan counted 89 hyphenated occurrences across 52 distinct spellings in raw LaTeX, including label strings; these are diagnostic counts, not evidence that all compounds are jargon. Established terms such as copy-on-write, proof-state, prepared-state and resource-bounded carry scientific distinctions and should remain. Searches found zero occurrences of `in order to`, `utiliz`, `due to the fact`, `with respect to`, `in terms of`, `is able to`, `may potentially` or `could possibly`. The first supplementary scan used unavailable `python`; it was rerun successfully with Python3.

## Must-fix

None found within this word-choice scope. Scientific assertions and missing result placeholders are not failures of this BOOTSTRAP review.

## Should-fix

1. **Design / Observable behavior, L117.** Quote: “without inserting preceding alternative-candidate suffixes.” Problem: stacking temporal and compound modifiers makes the reader unpack which history is excluded. Fix only this phrase to “without inserting suffixes from preceding alternative candidates.” This retains the distinction between the original candidate's own history and other candidates' suffixes; keep the next sentence unchanged.

2. **Implementation / Process and resource handling, L159.** Quote: “Wall-time outcomes retain the measured operational scope described in Section~\\ref{sec:behavior} and the evaluation limitations, rather than following from inherited counters alone.” Problem: outcomes do not literally retain scope, and the noun-heavy construction obscures what is qualified. Suggested sentence: “Claims about wall-time outcomes are limited to the measured operational scope described in Section~\\ref{sec:behavior} and the evaluation limitations, rather than following from inherited counters alone.” This keeps the operational limitation and the distinction from inherited native counters explicit; it does not assert deterministic response equality.

## Consider

1. **Evaluation / Heterogeneous execution, L206.** Quote: “a checking-operation improvement alone does not establish a service-frontier shift.” Problem: two compact compounds make an otherwise ordinary causal distinction harder to read. Suggested local replacement: “improving a checking operation alone does not establish an improvement in the service frontier.” Keep the preceding sentence's complete CPU/device paths, RQ3 accounting and matched boundary. This suggestion is optional because “service frontier” is already defined and the current sentence is technically clear.

2. **Related work / Heterogeneous checking, L229.** Quote: “These are direct competitors to representation-only acceleration.” Problem: “These” refers to the two preceding checker implementations but can momentarily look like it refers to integer identifiers or parallel arrays. Suggested sentence: “These checkers are direct competitors to representation-only acceleration.” This names the referent without renaming the mechanisms or weakening the baseline comparison.

## Preservation and disposition

Report only: no paper sentence changed, no fix applied or rejected by this reviewer, and no source/bibliography/build/memory state changed. The only output is this report. All four RQs and quantitative strings, including RTX 5090, remain untouched; no evaluation slot is changed. Preserve original/native preparation and candidate histories, lifetime independence, inherited native resource state versus service accounting, complete source versus post-export measurement, tactic-screen versus declaration acceptance, strongest bounded warm/cache/native CPU baselines, device qualification and online checking costs, fallback, admissions, artifacts and UNKNOWN. No stacked hedge warrants removal; scope-bearing limitations remain protected. Nominalizations used as names of contributions or measurement categories need no automatic conversion to verbs.

No compilation or page evidence is claimed because this assignment is read-only and forbids builds. No external facts were introduced. Remaining concerns are the four local suggestions above, not a request for broad prose rewriting. The alternative of globally removing compounds was rejected because many encode required technical scope. Next node: parent decides and records each suggestion, applies accepted local edits, compiles and verifies preservation, then launches serial Round 8.

Totals: 0 Must-fix, 2 Should-fix, 2 Consider. The three most useful improvements are the explicit alternative-candidate suffix phrase, the scope-bearing wall-time claim subject, and the explicit checker referent.

## Root disposition 2026-10-09T21:59:06.520597+00:00

All four findings accepted: S1 unpack alternative-candidate modifier, S2 explicit wall-time claim subject preserves measured operational limits, C1 plain service-frontier phrase, C2 explicit checker referent. Four local sentence edits, no numerical/technical/RQ scope changes. Diff preserves44citations/23entries/12slots/fourRQ. round-7-build.log exits0/eight pages. No blanket compound deletion or hedge removal. Next fresh Round8 terminology/claim tone.
