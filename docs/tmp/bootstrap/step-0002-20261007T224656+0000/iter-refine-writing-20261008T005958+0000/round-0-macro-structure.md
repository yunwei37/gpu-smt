# Round 0: Macro structure review

Parent gate: WRITE_GATE / orchestrated BOOTSTRAP.
Start: 2026-10-08T00:59:58Z (parent round dispatch directory timestamp; direct reading preceded first explicit clock observation).
End: 2026-10-08T01:00:18Z (review completion clock observation; report written immediately afterward).
Entry baseline: d224cd2d991439940e5b4b108b55b53c6a1b8525. Parent confirmed canonical paper and bibliography equal HEAD despite unrelated dirty files. No Git commands, stash, copied paper baseline, canonical edits, or builds were performed by this reviewer.

## Procedure and read evidence

Direct filesystem reading, without a Skill tool: first read complete `docs/user-instruction.md` and `docs/questions-for-author.md`; then read complete `docs/paper/main.tex` (208 numbered lines), complete `docs/paper/references.bib` (196 lines, reread as 1–150 and 151–196 to remove combined-output truncation ambiguity), full `/workspaces/.agent-state/codex/skills/check-paper-structure-flow/SKILL.md`, its complete `references/full-paper-12p.md`, and complete `/workspaces/.agent-state/codex/skills/rewrite-abstract-intro/references/abstract-intro-structure.md`. The paper was reread separately with line numbers after the combined read was truncated. Reviewed Level 1 macro structure only; paragraph-role and sentence-flow review are reserved for subsequent rounds.

OSDI full-paper conventions apply because the target is a full systems paper, despite the parent-confirmed current seven-page seed. This is submission-shaped BOOTSTRAP writing, not a final submission. Intended completed implementation in present tense is authorized. Missing empirical data/plots and explicit unanswered RQ blocks are permitted here and are not scientific or writing blockers. The four RQs, full Lean plus SMT scope, and RTX 5090 constraint must remain unchanged.

## Findings

### Must-fix

None that blocks the authorized bootstrap writing gate. All principal sections exist; the main section sequence is sound, Background and Motivation are separate, Design and Implementation are separate, and the four explicit numbered RQs are followed by matching primary evidence blocks. Missing results are explicitly represented rather than fabricated.

### Should-fix

1. **MACRO — Discussion and limitations, main.tex:181–188.** The current combined section places evaluation validity and operating-range limitations after Evaluation and provides no distinct broader-implications discussion. Almost every paragraph here states a limitation: supported runtime boundaries, wall-time variability, replay arrival validity, backend/extensions coverage, and GPU measurement boundaries. **Concrete fix:** place these limitations in a final `Limitations` subsection of Evaluation after RQ4, preserving all qualifications; add a separate short `Discussion` section for implications of separating preparation from speculative execution and what extending supported boundaries would require. Do not imply that absent result data are a gate blocker. This is a section-organization correction, not a request to expand claims.

2. **MACRO — Full-paper depth allocation, main.tex:129–143, 154–179.** Implementation has three plausible component subsections but very little concrete mechanism detail, while Experimental setup is packed into three broad paragraphs and each RQ is only two paragraphs. As a seven-page bootstrap this is permissible, but it does not yet provide the explanatory space expected of the intended full systems paper. **Concrete fix:** establish an explicit full-paper budget as the draft matures: about 2 pages Introduction, 1 Background, 1 Motivation, 2–3 Design, 1 Implementation, 3–4 Evaluation, and concise Discussion/Related Work/Conclusion. Prioritize filling Implementation's adapter qualification, branch lifecycle/error paths, bounded placement mechanism, and device-operation integration; reserve the evaluation expansion for setup details and subordinate evidence within the existing four RQs. Do not add RQs or pad the seed to hit twelve pages now.

### Consider

3. **MACRO — Architecture overview, main.tex:73–96.** A first Design architecture figure and typical-operation walkthrough are present, satisfying the structural requirement. The diagram is primarily a linear decision/data flow, however, so it does not visually distinguish the retained parent from branch-owned state or the manager's retention/cancellation responsibility. **Concrete fix:** when improving the figure, show the bounded service manager, immutable parent, multiple disposable children, and native fallback as separate components, marking ownership and the verifier authority boundary. Keep the CPU/device split subordinate to supported branch work. Alternative: retain the current flow chart and add ownership annotations rather than another figure.

4. **MACRO — Implementation closing, main.tex:142–143.** The section ends with the device path rather than a concise integration summary. The full-paper template expects a final summary of language, platform, integration modes, and code size. C++ and Linux appear elsewhere, but integration is scattered. **Concrete fix:** append one concise Implementation paragraph collecting the concrete integration modes, languages and platform; include code size only when available from the implementation, without inventing it. This is an optional completeness improvement for the current seed.

## Passing checks and preserved structure

- Introduction precedes neutral Background, followed by distinct Motivation, Design, Implementation, Evaluation, Related Work, Conclusion.
- Background has two load-bearing technology/state subsections. Motivation has two distinct problem-evidence areas, with honest measurement placeholders.
- Design opens with three named, motivation-derived goals, an overview, the architecture figure, and a typical operation. Its five subsections each cover an identifiable design decision or execution component.
- Implementation has its own native-adapter, process/resource, and device-path subsections.
- Evaluation opens with exactly RQ1–RQ4 and maps them to goals/contributions. Setup is outside that count. Four noun-phrase evidence subsection titles correspond to the RQs and each block explicitly states its RQ and closes with an unanswered evidence condition. No extra experimental question is promoted to a fifth RQ.
- Related Work uses four topic groups rather than a paper-by-paper list. Conclusion is one paragraph and introduces no future-work section.
- Subsection titles are descriptive noun phrases, with no question headings or redundant repeated system names.

## Alternatives and remaining uncertainty

Keeping `Discussion and limitations` combined is a defensible compact-seed choice, but splitting it is preferred for the intended full-paper organization and costs little even before data arrive. The page-budget finding is a planning/depth concern, not an assertion that the current seven-page bootstrap must be padded. Actual rendered subsection balance and figure placement were not independently compiled or inspected in this read-only reviewer; the parent's build/diff audit should record those facts. Citation correctness was outside this round; reading the full bibliography supplied context without re-verifying external sources. No finding narrows Lean/SMT/device coverage, changes the fixed RQs, or withholds authorized present-tense implementation writing. Parent should append disposition, build and diff audit after applying any accepted changes.

## Root disposition and round completion

Completed 2026-10-08T01:01:50.247704+00:00. Direct scope comparison preserves full user Lean/SMT/5090 objective and intended bootstrap present tense. Applied Should-fix1: move the intact limitations under Evaluation afterRQ4, add separate Discussion deriving behavior/cancellation/fleet-memory implications solely from existing Design. Applied the actionable Should-fix2 organization concern; deeper mechanism and evaluation data are deferred to accepted research implementation, since inventing internals or padding is forbidden. Consider3 ownership-diagram expansion deferred: current walkthrough/caption define ownership; a concrete mechanism figure belongs with qualified implementation rather than another speculative drawing. Applied Consider4: move existing Linux integration summary from Implementation opening to its closing, collecting already stated C++ integration. No code-size number invented.

Root used subsection/paragraph-sized apply_patch edits and inspected cumulative paper diff. make -C docs/paper exit0, PDF7pages, no undefined references or fatalTeX error; existing underfull-box layout warnings remain. All4RQ strings and12result placeholders exactly equal entry baseline; citation expressions34 unchanged, bibliography unchanged, quantitative values untouched. Final paperSHA256 1de396949f306e2ecae48ef92153759c30c7e8c0b003b55771f575ae1e5eadfc. No technical qualification deleted. Alternative leave combined section rejected for clearer evaluation-scope placement; no scientific-contract change. Tree remains W1 serial expression refinement; next Round1 micro/paragraph roles.
