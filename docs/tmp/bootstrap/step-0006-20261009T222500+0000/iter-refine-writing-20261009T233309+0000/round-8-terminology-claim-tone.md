# Round 8 — terminology and claim tone

Started during this delegated turn; first captured UTC checkpoint: 2026-10-09T23:45:26.760177+00:00 (exact earlier start not recorded). Completed: 2026-10-09T23:46:32.023837+00:00. Parent: BOOTSTRAP step0006, serial WRITE run iter-refine-writing-20261009T233309+0000, after root Round7 application/compile. Scope: complete J/C/F/X terminology-infoflow review and claim-tone/self-attack review. Read-only diagnostic subagent.

## Full actual provenance and entry

Read docs/user-instruction.md first and the COMPLETE current docs/paper/main.tex, lines1–238; an overlapping125–154 read recovered the middle span omitted by the long tool display. Source SHA256: 27601bb50fbf88634cd0b0518f40abd4df9d796ce2d6059835cf8702d3215e6d. Read current Round7 report to avoid resurrecting resolved findings.

Reread FULL actual root `/workspaces/.agent-state/codex/skills/check-terminology-infoflow/SKILL.md`, SHA256 c688b995fd38022d6c0d5589f94efc5a8d3a7030d2f046d2ea455475df9cadb6, including J0–J6, C1–C7, F1–F9 and X1–X7. Read FULL actual root `/workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md`, SHA256 e28b057233d8f5a184219b589b7e28c73e5819e57ec5fd0555b7c51ea977d668, including protected hedges and self-attacking sentence tests. Root iter-refine-writing complete instructions remain loaded from this agent's Round5. No Skill invocation tool exists; filesystem reading is the actual loading mechanism. Round5's consistency reference is not used as a substitute for this full J/C/F/X pass.

Method: read every sentence; perform read-only term frequency/location scans; map definitions and dependency order; check near-synonyms, captions, titles, RQ blocks and claim scope. Treat paper as intended completed submission per parent BOOTSTRAP contract. Missing results remain explicit; internal implementation status does not trigger a tense downgrade.

## Concept inventory and frequency evidence

Raw-source scan includes labels/placeholders, so counts are diagnostic rather than invented-term counts. Frequent words: native78, preparation58, candidate57, execution52, state52, verification47, service47, reuse31, memory31. Frequent two-segment hyphen matches: prepared-state9, proof-state4, equal-resource3, fan-out3, resource-bounded3, per-input3; regex splits longer compounds, so copy-on5 and end-to4 are portions of ordinary copy-on-write/end-to-end, not coined terms. One-off modifiers such as branch-owned, context-sensitive, post-import and source-native specify real distinctions. No core-concept budget excess or project run/script vocabulary is found.

| Concept family | Establishment/definition | Uses checked |
|---|---|---|
| Candidate / independent attempt | Abstract14–18, introduction26–34 | motivation65–72; design75,105,109–128; implementation143–168; evaluation173–208; discussion216/conclusion234 |
| Native prefix / preparation / prepared state | abstract18–20 plain account; formal prefix59; immutable branching point75; matching conditions112 | intro34–38; diagram89,105; design109–133; implementation143–163; RQ1/3 and related work191–203,220–228 |
| Candidate suffix | intro38 first term; exact definition112 |117,121,157,196 |
| Branch / parent / mutation / lifetime | abstract19–20, intro34–38; design75 and diagram89–105 |109–133,143–163,174–175,196–203,220,234 |
| Quiescent boundary / adapter | systems-standard quiescence19,36; operational conditions114; concrete adapter143–154 |105,109,121,157,161,191,211,216 |
| Native behavior / fidelity / outcomes / artifacts | problem16,30; stages50–56; interface definition117–123 | motivation70–72; device138; implementation148–166; RQ2/4 and limitations196–211 |
| SMT / SAT / UNSAT / UNKNOWN | SMT expanded21 and26; outcome labels52 |119,123,138,198 |
| Lean admissions / service admission | proof admissions54; device admission138; state admission131 |119,182,184,198 |
| Resource frontier / equal resources | explicit definition36 |171,175–176,182,201–208,234 |
| Copy-on-write / proportional fleet memory / private dirty memory | COW process sharing61 and157; proportional/fleet definition131 | placement131–133; implementation163; metrics186; RQ3/ discussion203,216 |
| Qualification / online checking / fallback | boundary109,114,123; device138–140; adapters143–154 |161,166,196–208,216 |
| Source verification / post-export checking / tactic screening | stages50–56 |152,180–184,206–213,222 |
| Warm service / logical or serialized reuse / caching | introduction17,32; prepared native state59–61 |67,182,191,201–203,220–225 |
| Heterogeneous checking / device work / dynamic dependencies | abstract21; design136–140 |implementation166–168; RQ4 block206–208; limitations213; related231 |

Prefix/state/context are distinct: prefix denotes ordered preparation operations plus native runtime/configuration; retained state is their prepared realization; logical environment is narrower. Branch/process are not globally normalized because native logical proof-state branching is a baseline distinct from process branching. Preparation/verification/elaboration/checking refer to different stages, not loose synonyms. No invented system name appears; descriptive title does not create a hardcoded named-system violation.

## Must-fix

None. No semantic term contradiction, qualifier loss, claim inflation or scientific-contract change is needed.

## Should-fix

### S1 — Design, Heterogeneous checking, L138 (J5/C1)

Quote: `Before admission, device qualification compares operation outputs with matched CPU references.`

Problem: admission already denotes Lean acceptance of unproved obligations (L54,119), and also prepared-state/service entry (L131,182). The unqualified noun at the key qualification boundary leaves the object implicit. Readers can infer device operation admission, but making it explicit prevents confusion between offline implementation qualification and per-request service admission.

Concrete local fix: `Before a device operation is admitted, device qualification compares its outputs with matched CPU references.` Preserve the remaining sentence about enclosing native verification, online costs, and no mandatory full CPU replay. This names the existing admitted object and does not add a new check or change qualification frequency.

## Consider

### C1 — Background, Verification stages and outcomes, L52 (J6/C2)

Quote: `Solver responses include SAT, UNSAT and UNKNOWN`.

Problem: these standard SMT outcome labels are not glossed for the requested systems audience. This is audience calibration, not an invented-term blocker: readers outside verification may mistake UNKNOWN for rejection or understand UNSAT as universal proof acceptance.

Concrete local fix: `Solver responses include SAT for satisfiable queries, UNSAT for unsatisfiable queries, and UNKNOWN when the solver does not decide the query` followed by the existing model/proof/core request clause and citation. Keep the distinction between solver query outcomes and complete frontend verification outcomes. Existing text is acceptable if the parent considers these labels sufficiently standard.

### C2 — Introduction system paragraph, L38 (C2/F8)

Quote: `untouched candidate suffixes`.

Problem: suffix is formally defined only at L112, whereas introduction38 uses the term in a compact mechanism summary. The preceding preparation narrative supplies enough intuition, so no blocker exists, but inline reader language would remove the short definition-order IOU.

Concrete local fix: replace this occurrence only with `untouched candidate operations after preparation`. Keep `candidate suffix` in the formal definition and subsequent mechanism paragraphs. This preserves the full operations sequence, its ordering and untouched-input guarantee, without introducing a synonym as a new named concept.

## Claim-tone and negative findings

J: low-frequency modifiers are descriptive and scope-bearing; no undefined internal metric/policy/run identifier leaks into prose. Section titles use reader language, four RQ meanings remain unchanged, and technical terms are either standard or locally explained. C: prepared state/prefix, resource frontier, original interface, proof-screen versus finalization, and native versus service accounting stay distinct; caption terminology matches the body, including Round5 placement fallback clarification. No symbol/case/spelling drift demands normalization.

F: topic sentences convey the claim/procedure, motivation precedes the native mechanism, dependency order is preparation→boundary→branch→resource/device execution. Each RQ block names its question, procedure and metrics, with explicit missing setup/results rather than invented evidence. The RQ4 paragraphs connect operation speed to the complete service frontier. No remaining flow defect calls for restructuring.

X/claim tone: abstract/introduction/conclusion maintain the same bounded thesis. Prior-work and complete-boundary cautions delimit novelty and measurements rather than apologize for weak work. Keep `supported`, `where one is produced`, `at a matched boundary`, `strongest measured CPU path`, measured wall-time operational scope, and post-export restrictions. The statements that fork/COW or representations do not by themselves establish novelty protect the scientific contract and are not self-attacks. The four `RQ remains unanswered` statements and result slots are required honest evidence boundaries; do not delete them under the project-report rule. No gratuitous apology or stacked hedge was found. Structural absolutes (no candidate suffix in parent, no additional inserted scope) express invariants and should stay. No performance numbers, missing-value fills, new GPU scope, or future-tense status downgrades are proposed.

## Summary and disposition

| Category | Must-fix | Should-fix | Consider |
|---|---:|---:|---:|
| J5/C1 admitted-object clarity |0|1|0|
| J6/C2 systems-audience outcome gloss |0|0|1|
| C2/F8 introduction definition order |0|0|1|
| Other J/C/F/X and claim-tone checks |0|0|0|

Top three improvements: name the admitted device operation; optionally gloss solver outcomes for systems readers; optionally inline the introduction's suffix meaning. Pattern: only local audience/definition clarity remains, with no vocabulary inflation or unsupported claim-tone problem.

Applied/rejected fixes: none by reviewer; root dispositions each item. Sentences changed:0. Only this report is written. No paper/source/canonical/Git/build/native changes or executions. No compilation/page success is claimed; parent performs that required check after its dispositions. All proposed fixes preserve citations, numbers, result placeholders, four RQs, qualification versus online-checking distinction, protected boundaries and completed-submission tense. Next node: root Round8 fix/disposition and compile, then serial Round9.

## Root disposition and completion

2026-10-09T23:50:03.303144+00:00 — S1 applied: names the admitted device operation, preserving qualification frequency and online native checks. C1 applied: systems-audience SAT/UNSAT/UNKNOWN gloss preserves solver versus frontend outcomes. C2 applied only in introduction: ordered untouched operations after preparation clarify the later formal suffix term. Three local paragraph edits; no numbers, RQ meanings, protected qualifiers or technical content removed. Initial failed narrow patch matched no whole line and changed nothing; corrected reviewed whole-paragraph patches applied. Complete paper build-round8.log exit0; pdfinfo9pages. Citation calls47 and result slots12 retained. Actual reviewer scope and edits match verbatim user intent; no GPU or service success invented. Next serialRound9.
