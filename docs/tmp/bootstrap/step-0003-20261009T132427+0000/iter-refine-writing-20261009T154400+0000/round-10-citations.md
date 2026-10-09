# Round 10 — Citation gate, Pass 3 only

Parent: bootstrap step-0003 / iter-refine-writing-20261009T154400+0000. Serial review after root reported Round9 source fixes, build exit 0 and eight-page PDF. Root owns paper/bib changes, Git and build.

Actual inputs read in full: docs/user-instruction.md, /workspaces/.agent-state/codex/skills/check-paper-citations/SKILL.md, current docs/paper/main.tex and references.bib. Filesystem skill invocation/adaptation was used; no Skill-tool call is claimed. No interruption occurred. Precise start time was not separately captured. Completion appears below.

Entry main.tex SHA-256: 9036cf8aa3af3b3462d472488c846bbe74ae5489b07c8bf01b7d7459a767a099. Entry references.bib SHA-256: 5c76f124f744cdd62d7ea5ed6d8312bc89599c2d763bcacc02388c7c602b0835. Protected counts: four numbered RQs, 12 result slots, 37 citation commands, 20 bib entries.

## Gate scope and annotation readout

All 20 entries have nonempty VERIFIED, REAL, PDF, ABSTRACT and USED_FOR annotation fields, with REAL: yes and VERIFIED: 2026-10-07. Entries checked: repl, leanSnapshot, z3api, z3params, fork, leanArena, mathlib, verusage, nanoclo, nanocloFortran, leanIncremental, kimina, boogieCache, sock, seuss, lean4, verus, kiminaPaper, procMemory, verusagePaper. No missing or unverified annotation triggers a full verification run.

Under the iterative-writing special gate rule and the skill's final “When Called from iter-refine-writing” section, only Pass3 was performed. No repeated metadata/API verification script, 20-entry PDF authenticity run, retraction search or unchanged novelty survey was performed or claimed. The annotations remain the sole verification-state authority; this is the mandated round report, not a separate citation ledger. PDF: not available on documentation/artifact entries is an explicit field, not incomplete annotation.

Method: scan every existing narrative claim and named system/dataset/benchmark for missing support; check first mentions and section citation density, distinguishing common systems knowledge and the paper's own design/methodology from externally sourced facts. Abstract citation omission is conventional; introduction/body cite Lean, Z3, REPL and named baselines. All evaluation dataset names have provenance citations. RQ methodology, own design and limitations do not require literature padding.

## Must-fix

None. No uncited benchmark origin or indispensable named-system source was found.

## Should-fix

1. Background / Verification stages and outcomes, L50: “SMT-backed verification includes frontend translation, solver setup, parsing, preprocessing and solving.” Problem: this stage decomposition is external background, but its nearest citation supports session responses/artifacts rather than visibly grounding the frontend stage. Concrete fix: append \cite{verus,z3api} to this first sentence, retaining all wording. Existing verus primary paper describes generation of verification conditions and their submission to Z3; z3api covers native solver command/session work. Do not attribute all frontend stages to the solver interface alone.

Actual source check for this gap: opening the bibliographic Verus PDF URL through web returned a timeout, which is not evidence of a false reference. The already retained primary PDF docs/reference/verus-oopsla2023.pdf was read through pdftotext stdout. Its section 2 explains weakest-precondition generation of a verification condition and submission to Z3, and describes direct translation of specification function calls into SMT function calls. The official source repository https://github.com/verus-lang/verus was also opened successfully and confirms static Rust verification through solvers. No new source or bib entry is needed; no PDF was downloaded or annotation changed.

## Consider

1. Background / Verification stages and outcomes, L48: “Kernel checking validates proof terms against the dependent type theory.” Problem: this is a neighboring-field factual explanation; the first sentence already cites lean4, but repeating the citation here would make the precise kernel attribution easier to locate. Concrete fix: append \cite{lean4} to this sentence. This is optional because the same paragraph already cites the Lean architecture and the claim is standard proof-assistant background; no fresh all-paper verification is warranted.

## Preservation and disposition

Summary: 0 Must-fix, 1 Should-fix, 1 Consider. Both proposals reuse existing verified bib entries; source and bib edits remain pending with root. No missing citations were actually added, no inaccurate claims were changed, and no hallucinated citation was identified. Annotation completeness checked: 20; newly fully metadata-verified entries: 0, as mandated by gate scope. No unverifiable entry was newly discovered. The primary PDF fetch timeout was resolved by reading the retained PDF for the narrow new gap.

No criticism of missing BOOTSTRAP results is issued. Exact four RQs, 12 result slots, all numbers, scope-bearing hedges, honest unanswered and negative outcomes, complete source/post-export distinction, warm/native baselines and RTX5090 full setup/transfer/fallback costs remain protected. Direct-user Lean+SMT acceleration, RTX5090-only hardware, gpt-6.1-sol preference and full OSDI research intent remain intact. No idea skill or scientific reframing occurred. No paper/bib edits, Git operations or builds occurred; only this round report was written.

Next: root records each finding's disposition, adds accepted existing-source citations without technical wording changes, compiles and checks preservation, then starts serial Round11 meaning-preservation audit against the original entry baseline.

Completed: 2026-10-09T17:53:09.899510+00:00

Root disposition —2026-10-09T17:53Z: Should and Consider applied, two existing-source citation expressions added without wording/number changes. Both address background claims rather than decorate own design. Citation count39 versus37entry, bibunchanged20fullyannotatedentries, all4exactRQ/12slots unchanged. Compileexit0/PDF8pages; intended completed prose remains distinct from actual unimplemented branching. No new novelty or device claim. Next fresh independent Round11 cumulative meaning audit.
