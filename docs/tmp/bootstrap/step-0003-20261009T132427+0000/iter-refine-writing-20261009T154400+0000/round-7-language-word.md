# Round 7 — Word choice reviewer report

Parent node: bootstrap step-0003, iter-refine-writing-20261009T154400+0000. Objective: read-only word-level review of the complete paper; root owns source fixes, compilation and Git.

Recovery and timing: this reviewer previously returned a chat report against an earlier paper, followed by an authoritative-user-file check. On the current resume, the requested report file did not exist. The earlier chat response is not evidence of a completed persisted report for this step. This report reviews the current paper afresh. No interruption occurred during the resumed review. Current review completed at 2026-10-09T17:46:23+00:00; the precise start time was not separately captured and is not reconstructed.

Actual inputs read: full docs/user-instruction.md; full /workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md; entire docs/paper/main.tex, with additional section reads to recover truncated combined tool output. The earlier session also read references.bib, the iterative-writing skill, and questions-for-author.md; those are historical reads, not new citation verification. Current main.tex SHA-256: a77aa236d017a6f55028b4d9a0d001eb7f6d79d9da20eec02b324c43380c145b.

Method: sentence-by-sentence review for nominalizations, unclear pronouns, compound density, jargon inflation, unnecessary adverbs, stacked hedges and verbose phrases. A case-sensitive lexical source scan found 90 hyphenated tokens across 51 forms, including LaTeX labels and result placeholders. Frequent forms were prepared-state (9), SMT-backed (5), copy-on-write (5), proof-state (4), end-to-end (4), and equal-resource (3). This is a density check, not a requirement to eliminate established technical terms.

## Must-fix

None. No unambiguous pronoun error, stacked hedge or word-choice defect changes the scientific meaning.

## Should-fix

1. Introduction, L41: “an observable-behavior argument.” The compound compresses an ordinary description into a term. Suggested local fix: “an argument about observable behavior.” Preserve the rest of the contribution and its section reference.
2. Implementation / Native adapters, L133: “using an unmodified same-source executable.” The one-off compound obscures the build relationship. Suggested local fix: “using an unmodified executable built from the same source.” Preserve the distinction between build metadata and other response differences, and preserve the requirement that every observed difference remains visible.
3. Implementation / Process and resource handling, L142: “Supported-boundary qualification covers.” A compressed compound nominalization hides the activity. Suggested local fix: “Qualification of supported boundaries covers.” Preserve all native-resource and wall-time qualifications.

## Consider

1. Design / Branch lifetime and cancellation, L111: “should not force retention of the shared parent.” Suggested local fix: “should not force the service to retain the shared parent.” This exposes the actor without changing the retention-policy condition or the isolation requirement.
2. Design / Bounded placement and execution, L118: “high-sharing workloads.” Suggested local fix: “workloads with substantial preparation sharing.” The longer phrase identifies exactly what is shared; retaining the compact original is also defensible.
3. Evaluation / Preparation sharing, L170: “an unrelated-work control.” Suggested local fix: “a control with unrelated work.” This removes a one-off compound while preserving the control.
4. Related work / Verification caching, L200: “Assertion-equivalent reconstruction.” Suggested local fix: “Reconstruction with equivalent assertions.” Preserve the distinction from original native execution history.

## Preservation and decisions

No source sentence was changed. Findings are suggestions for root review, so applied/rejected-fix decisions and compilation/page evidence remain pending with root. No paper edits, Git operations, builds, idea-skill invocation or scientific changes occurred. Only this report file was written.

All four exact RQs remain protected, as do numbers, citations, UNKNOWN handling, requested artifacts, unsupported-boundary fallback, setup/transfer/CPU fallback costs, complete versus post-export boundaries, failed/incomplete attempts and negative findings. No instruction to remove honest limitations or unanswered-result markers is issued. The user's Lean and SMT acceleration research, RTX 5090-only GPU preference, gpt-6.1-sol preference and complete OSDI-level research intent are preserved; no conflict was found. Present-tense intended system descriptions are permitted in BOOTSTRAP.

Most earlier chat findings have already disappeared from the current source and are not repeated as live defects. Clear referents such as “This tradeoff,” “These requirements,” and “This comparison” need no forced expansion. “Actual dynamic work” and “actual context-sensitive dependencies” carry the distinction from static graph width and should remain. No stock verbosity phrase or redundant hedge stack was found.

Summary: 0 Must-fix, 3 Should-fix, 4 Consider. The most useful changes expand observable-behavior, same-source and Supported-boundary into ordinary phrases. Next node: root evaluates these local suggestions, applies accepted changes subsection by subsection, compiles and verifies preservation before serial Round 8.

Root disposition —2026-10-09T17:47:50Z: all three Should-fix and four Consider suggestions applied individually in the named subsections. Plain descriptions improve actor/build/control clarity without introducing concepts. Seven source sentences changed; no quantitative change. Actual post-recovery apt restoration completedexit0 (retained log `/workspaces/.agent-state/gpu-smt-tex-restore-20261009.log`); this is dependency work, not evidence. Round7 compileexit0/PDF8pages. Cumulative diff has37citation expressions, four exactRQ strings and12unchanged result slots (the macro definition is separate, not subtracted from invocation count). Existing read-only raw/bib/protected boundaries are preserved. User intent matches; no smaller verifier/GPU objective substitutes for complete research. Next serial Round8.
