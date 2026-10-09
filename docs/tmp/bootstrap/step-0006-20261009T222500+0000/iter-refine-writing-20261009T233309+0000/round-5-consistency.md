# Round 5 — paper consistency (read-only reviewer)

Review started during this delegated turn; the first captured clock checkpoint is 2026-10-09T23:40:32Z (the exact earlier start was not recorded). Completed: 2026-10-09T23:41:13.572408+00:00. Parent: BOOTSTRAP step0006 WRITE_GATE, serial iter-refine-writing Round5, after Round4. Objective: diagnose architecture/workflow, figure alignment, claim/number/RQ consistency and interface/mechanism fidelity without changing science.

## Actual skill provenance and sources

Complete filesystem-loaded instructions: `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md` (SHA256 647b2676d953c16c69755b93872e1c31a530d338576f3e1040b05e4be9f8b75a), `/workspaces/.agent-state/codex/skills/check-terminology-infoflow/SKILL.md` (c688b995fd38022d6c0d5589f94efc5a8d3a7030d2f046d2ea455475df9cadb6), and its complete `references/paper-consistency.md` (c0ebdb733a72df59129f1351ffad04d6476e0d4b152a785d8158eb8f1abb74b5). No Skill invocation tool is available; these are the actual root versions read, not similarly named dependency copies.

Read `docs/user-instruction.md` first successfully after resolving the supplied extensionless path (that initial path does not exist). Read complete CURRENT `docs/paper/main.tex`, `docs/paper/references.bib`, `docs/design.md`, `docs/evaluation.md`, `docs/implementation.md`, and `docs/idea-story.md`; current step report for gate context; complete experiment007 result review and artifacts/leanpolish-native-2026-10-09/README.md. Checked raw preflight3 terminal.json, fork-P1 receipt.json and stderr.bin against the review. Large initial combined reads were followed by smaller paper/canonical reads to recover truncated portions. Paper entry SHA256: 912af66c204f183705956b96613a23a4edb2b17321f691a82f7886f59c269d46; bibliography: 97cae70d34ddd11566b9ef9d18c63488d79fc9a9956cb5643035a1d174e552e3.

Method: extract ordered-prefix, immutable-parent, qualified-boundary, original-interface, resource-accounting, cancellation and device-check anchors; compare every section and Figure1 with the canonical four-RQ contract and current supporting evidence. BOOTSTRAP completed-submission framing is honored: present-tense mechanisms are not defects merely because implementation is unfinished. No final result is inferred from dependency evidence.

## 1. Inconsistencies found

### Must-fix

None found. There are no new quantitative performance claims to reconcile with experiment007, and its failed fork preflights are not promoted into the paper. Missing numerical evidence remains explicit. Four numbered RQs match the canonical scientific meanings and their evidence blocks.

### Should-fix

- **S1 — Figure1 omits placement rejection routing (minor figure/text workflow mismatch).** `main.tex` L84–98 draws placement directly into boundary qualification, with fallback reached only from the unsupported-boundary decision. L109 explicitly says requests without a retained state use native execution; L131–133 independently describe cost/locality-based retention rejection. The diagram does not display that route or state its omission.

### Consider

None. No additional science or placement optimizer is proposed.

## 2. Why each matters

S1: readers using the overview diagram can infer that native execution is selected only for incompatible boundaries, even though low sharing value and nonretention also select it. This is a small diagram completeness issue rather than a contradiction in the prose; the newly clarified routing deserves a matching caption or edge.

## 3. Exact fixes or replacement wording

S1: minimally add this sentence to the Figure1 caption: `Requests without a retained prepared state also use native execution.` Alternatively draw a placement-to-native-execution edge labelled `no retained state`, provided it fits without obscuring the supported-boundary decision. Preserve all existing node semantics and caption content. The caption sentence is the smaller fix and does not introduce a new mechanism.

No source edits were applied or rejected by this reviewer. Parent owns dispositions and any application.

## 4. Broader follow-up checks

The following cross-checks passed:

- Abstract, introduction, design, discussion and conclusion consistently separate preparation from candidate execution history and lifetime. Supported branches inherit ordered native preparation; parents do not execute suffixes.
- Original interface qualification precedes branch comparison; split parsing distinguishes EOF effects; fallback is compatibility-based, not triggered solely by UNKNOWN. Native requested artifacts and bounded outcomes remain part of fidelity.
- Full frontend/check-environment completion is explicitly insufficient for runtime quiescence (L154), consistent with raw fork refusal and the current source-backed finding. No safe arbitrary multithreaded clone is claimed.
- Cancellation compares completed responses separately from externally terminated progress, cleanup and survivor isolation (L196). L159 does not confuse post-progress reaping with interruption inside solving.
- Device qualification versus online verification is explicit (L138,166,206): exact CPU reference comparisons occur during qualification, required online checks are charged, and no duplicate complete CPU replay is silently promised.
- Preparation characterization supports contribution1/RQ1; observable behavior and independent lifetimes support contribution2/implementation contribution3/RQ2; bounded execution and equal-resource comparison support contribution3–4/RQ3; the heterogeneous causal component of contribution4 maps to RQ4. Three goals and four RQs are compatible; no one-to-one cardinality requirement applies.
- Strong native logical/serialized state reuse, bounded warm services and caching remain the comparison family across introduction, setup and related work. Cold execution remains a control.
- Source verification and post-export checking stay distinct; goal closure does not become complete declaration acceptance; admissions/incomplete work remain visible.
- Wall-time operational qualifiers, native versus service resource accounting, fleet proportional memory, and complete transfer/setup/fallback accounting persist. No preliminary measured number has migrated into a final result slot.

Summary: 0 Must-fix, 1 Should-fix (figure/workflow), 0 Consider. The most useful change is the one-sentence figure caption alignment; no further independent changes are justified. No build, native execution, Git operation, paper/source/canonical edit, or other round occurred. This report is the sole write. Compilation/page verification and fix application belong to the parent. Next node: parent Round5 disposition, then serial Round6.

Root disposition: sole Should-fix accepted by localFigure1caption sentence stating alreadydescribed no-retained-state native placement. No mechanism/algorithm/numeric/RQ change. Existing selectedpreparedbranch diagram retained. Reviewed diff,47cites/12slots/4RQ preserved; make exit0/build-round5.log,8pages. All resultplaceholders stillhonest; no measuredbranch/GPU claim imported. NextRound6sentence review.

Root page-count correction: the preceding8pages statement was erroneous. build-round5.log actually records9pages/189307bytes, and pdfinfo independently confirms9. Additional caption text moves references onto a ninth page; no venueformat/submission readiness is implied. Earlierrounds0–4 remain8pages per their actual logs. Preserve all technical content; pagebudget/layout evaluated at final evidence/template stage.
