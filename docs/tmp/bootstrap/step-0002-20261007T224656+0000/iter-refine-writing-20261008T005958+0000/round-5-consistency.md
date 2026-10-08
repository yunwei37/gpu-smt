# Round 5 — paper consistency diagnostic

Parent: `/root`, serial BOOTSTRAP step 0002 writing workflow.
Actual start: 2026-10-08 01:10:15 UTC. Actual end: 2026-10-08 01:10:33 UTC.
Scope: report only; scientific meaning, paper, canonical documents and Git unchanged.

Inputs directly read: `docs/user-instruction.md`, `docs/questions-for-author.md`; complete check-terminology-infoflow SKILL.md and references/paper-consistency.md; entire `docs/paper/main.tex` (including its only inline figure/caption) and `docs/paper/references.bib`; `docs/idea-story.md`, `docs/evaluation.md`, `docs/design.md`, `docs/lean-resource-status.md`; experiment003 complete independent result review; selected native-boundary source-report anchors; entire historical `paper/main.tex` as a sibling comparison. No standalone figure source exists in the current docs/paper file inventory; the architecture is inline LaTeX.

Method: extract preparation, adapter qualification, resource, artifact, lifetime, fallback and GPU anchors; compare abstract/introduction/design/implementation/RQs/limitations/conclusion and architecture; inspect citation keys/cross-reference definitions; distinguish intended completed prose from actual final evidence. Missing results and unfinished implementation are explicitly not objections in this review. No numeric final results appear: four RQs, three design goals and RTX 5090 are structural/hardware scope, not unsupported measured claims. Preliminary numbers are kept outside the current paper. No absence-of-experiment claim is made, so no historical Git operation was needed or performed.

## 1. Inconsistencies found

### Must-fix

None established. Native fallback, inherited native solver counters versus separate service costs, untouched scopes, qualification before admission, Lean admission/completeness controls and RTX 5090 restrictions agree across the current paper. Four contributions and four RQs align with the three stated design goals. All current reference targets and citation keys have definitions.

### Should-fix

1. **Complete SMT-backed verification boundary is insufficiently connected to the implementation boundary** (major clarification; Background L50, Introduction L36, Implementation L126–129, setup L153–157). Background includes frontend translation in SMT-backed verification, and the introduction promises complete Lean and SMT-backed candidate verification. Implementation describes original SMT command evaluation and retained solver state, but never says how the SMT-backed source frontend participates in a source-to-result service interval. This is not evidence that the intended frontend is absent; it is a boundary ambiguity in the prose.

2. **Accelerator qualification conflates operation equality and enclosing native validation without specifying their different roles** (major clarification; Design L123 versus Observable behavior L104, Implementation L139 and RQ4 L175–177). L123 says supported device work preserves semantics through both matched operation comparisons and native checking of the enclosing proof/artifact. L104 allows alternative valid artifact representations; L139 requires per-operation output identity. These can coexist, but the text does not state whether native checking is offline qualification, measured online validation, or full CPU replay, nor how UNKNOWN/no-artifact responses fit the proof/artifact formulation. The mechanism is not contradicted; the reader cannot determine the charged validation boundary.

### Consider

3. **Historical sibling paper can be mistaken for the active scientific account** (minor document-routing issue, not a requested paper rewrite). `paper/main.tex` claims transparent unmodified frontends, normalized/content-addressed contexts and five different RQs, while `docs/paper/main.tex` deliberately requires native adapter qualification and four RQs. Current canonical idea-story/evaluation explicitly preserve legacy synthetic artifacts, so historical divergence is intentional. The old file's own title/header does not establish its archival relationship to the active draft. Consider a repository navigation or historical-file notice if readers can encounter both. Do not copy old numbers or mechanisms into the current paper.

## 2. Why each matters

1. Solver-session acceleration is narrower than full SMT-backed program verification, and can exclude translation/candidate construction costs. Without a bridge, the implementation appears to operate after the boundary promised in the introduction. RQ4 already handles source versus post-export Lean boundaries carefully; analogous SMT boundary precision would make the full-workload claim assessable.

2. Operation output identity, semantic artifact validity and exact native response fidelity are distinct checks. If native verification runs per request, its cost belongs in the complete interval; if it is qualification-only, that should be explicit. The prose should retain CPU fallback and authority without implying an unimplemented redundant checking mechanism or assuming every response carries a proof.

3. A reviewer or reproducer following the legacy path could infer a rejected compatibility contract and obsolete RQ set. This is a navigation concern, not a reason to rewrite historical scientific evidence.

## 3. Exact fixes or replacement wording

1. Add a short implementation/setup bridge naming the real evaluated source frontend and adapter boundary, once root selects it. Safe boundary-only wording: `For SMT-backed source verification, the measured interval also includes the native frontend's translation and its original solver interaction; solver-session replay alone is reported at its narrower boundary.` If intended full source integration differs, root must resolve that scientific choice rather than adopt this sentence mechanically. Alternative: explicitly qualify individual solver-session experiments and retain the full source-verification evaluation promise elsewhere.

2. Root should state the actual role of enclosing native validation and whether it is charged online. Suggested edit instruction: qualify L123 as offline adapter/device qualification or online validation according to the real design, say that required online validation is included in complete verification costs, and tie response/artifact comparison to Section~\ref{sec:behavior}. Preserve exact per-operation comparison; do not demand byte-identical alternative valid artifacts and do not introduce a GPU proof-producing checker. Hypothesis: L123 refers to qualification evidence, not complete native replay on every request. Verification step: root checks the intended device algorithm and experiment boundary before choosing wording.

3. Prefer a navigation notice outside the scientific body identifying `docs/paper/main.tex` as active and `paper/main.tex` as historical, if no existing entrypoint already makes that clear. This round does not authorize editing either file or repository navigation.

## 4. Broader follow-up checks

- When concrete adapters are admitted, replace generic boundary descriptions with their actual source/solver entrypoint and check complete setup/cost accounting across abstract, setup and RQ3/RQ4.
- When a device operation is selected, distinguish offline qualification from online validation and preserve UNKNOWN, rejection/admission and no-artifact paths.
- On final results insertion, trace every number to the frozen source records and recheck abstract/introduction/conclusion/RQ scopes; current placeholders are valid intended prose.
- No architecture/caption conflict found: unsupported native execution is shown before independent branches; the caption correctly excludes candidate suffix verification in the parent. The figure abbreviates shared retention/resource/qualification details already supplied in the body.

Summary: 0 Must-fix; 2 Should-fix boundary clarifications; 1 Consider archival-navigation issue. Highest-impact changes are the full SMT source-boundary bridge and explicit device-validation accounting. No scientific mechanism adoption, evidence invention, global terminology rename or paper edit occurred.

## Root disposition/build/diff audit

Applied both Should-fix clarifications: native frontend translation/original interaction stays charged for source-to-result SMT experiments, while session replay retains narrower scope. Device operation/CPU comparison is offline qualification before admission; enclosing native proof/requestedartifact checking and any required online validation stay charged, with original UNKNOWN/no-artifact response fidelity. This expresses already separate qualification-before-admission and complete-native-checking obligations; it adopts no actual device algorithm, certificate or novel production runtime. Actual path/scope still must be chosen and qualified beforefreeze. Consider historical sibling routing is a maintenance finding: preserve paper/ legacy unchanged; root will add navigation to active paper entrypoint rather than overwrite oldscientifichistory. No oldRQs/numbers imported. make exit0/7pages, no undefinedreferences/fatalerrors; layoutwarnings remain. Full user Lean/SMT/5090 goal,4RQstrings/12resultslots/citations34/bib/quantities preserved. SHA256 8645be8548a410b66dc2a4d3230eb508524532f866cac0286e5a0bc4af6b8c91. Completed 2026-10-08T01:12:41.217564+00:00. Next serial Round6 sentence language.

Consider navigation resolution: root inspected existing README.md Currentstatus; it already identifies docs/paper/main.tex as sole current paper and explicitly calls paper/ legacy. No second notice or historical rewrite is needed. The suggestion’s condition fails; retaining existing navigation is the final disposition.
