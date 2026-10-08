# Round 10: citation gate (Pass 3 only)

Timing: first recorded UTC checkpoint 2026-10-08 01:26:59 UTC, after initial prerequisite reads; the earlier task-start time was not instrumented and is not fabricated. End UTC: 2026-10-08 01:27:53 UTC.

Files read in full: docs/user-instruction.md; docs/questions-for-author.md; docs/paper/main.tex; docs/paper/references.bib; /workspaces/.agent-state/codex/skills/check-paper-citations/SKILL.md. Initial combined output was truncated, so main.tex was reread separately in full; the bibliography block was available in full. The skill directory contains scripts and tests, without further reference instructions.

Method: applied the skill's iter-refine-writing gate exception. Programmatically checked all five mandatory annotation fields for every bibliography entry: all 20 are complete, REAL: yes, VERIFIED: 2026-10-07. All 20 keys are cited and all cited keys resolve. Consequently no redundant verify_bib.py or full existence/alignment/integrity passes were run. Scanned the entire paper for missing factual, technique, system and workload attribution and section citation density. Directly opened primary evidence for targeted suggestions: https://lean-lang.org/papers/lean4.pdf ; https://arena.lean-lang.org/checker/nanoclo/ ; https://docs.nvidia.com/cuda/cuda-runtime-api/index.html . These were read as primary sources, not search snippets. No paper/bib edits, builds or Git operations occurred.

## Must-fix

None found in this missing-citations pass. Named evaluation sources VeruSAGE, Verus, Mathlib and Lean Kernel Arena have origin citations. Remaining unspecified candidate streams are explicitly result placeholders; their identity/provenance must be filled with their eventual retained measurements rather than invented now. This gate does not certify future sources or rerun the prior authenticity pass.

## Should-fix

1. Introduction, established reuse paragraph (main.tex:30): the first claim that verification result caches avoid repeated completed work has no adjacent attribution, although boogieCache appears later in Related Work. Add \cite{boogieCache} after the result-cache clause. This reuses the already annotated original verification-caching source without implying that cached decisions replace native behavior qualification.

2. Design / Heterogeneous checking: the factual explanation that expression graphs alone omit context-dependent reduction has no local source. The primary nanoclo page explicitly describes closures over interned environments and binder-dependent environment extension; the Lean 4 paper explains reduction and definitional equality. Add \cite{lean4,nanoclo} to the semantic explanation, keeping the actual dynamic-work characterization as this paper's own required measurement. Do not attribute a measured GPU opportunity to either source.

3. Implementation / Device path: “existing NVIDIA runtime” is the first named runtime mention without an origin citation or precise runtime identity. Once the actual used runtime is known, cite its versioned official documentation; if it is CUDA, the primary CUDA Runtime API manual above is the appropriate source. This is an attribution suggestion, not permission to infer CUDA or change hardware/runtime facts.

## Consider

Introduction (main.tex:34): process creation changing timers/descriptors is a technical premise with its source currently deferred to Background and Implementation. Add existing \cite{fork} at that sentence to make the introduction's premise independently traceable. The section's uncited design goals and own argument do not need artificial citation density padding.

Outcome: 20 complete existing verification annotations accepted by the gate; 0 full-source re-verifications; 0 hallucinated entries identified in this pass; 0 inaccurate claims changed; 0 missing citations added (report-only authorization). Existing documentation entries with PDF: not available are explicitly annotated and do not trigger a full run. All four RQ strings, the 12 result placeholders, numbers and Lean/SMT/RTX 5090/native/fallback/strong-reuse scope remain untouched.

## Root disposition and completion

Applied S1,S2 and C1: three local citation expressions use already verified boogieCache, lean4/nanoclo and fork entries. No new reference/technical claim or bibliography change. Exact native reduction/source and established attribution already support these claims; local citations improve access, not a measured GPU inference. S3 deferred until the final device adapter/runtime is chosen: outer NVIDIA container allocation is not evidence of a CUDA Runtime API implementation; current primitive uses the driver path. Do not invent the eventual runtime or a versioned reference in writing. Final artifact/version slot must record the actual evaluated device path; this nonblocking attribution suggestion remains linked here.

Root directly compared user instructions and all findings; no narrower scope/weak baseline/device outcome introduced. Paragraph diffs inspected. Exact4RQs,12result slots, quantitative tokens and bibliography unchanged; cite expressions increase34→37 with all original citations retained. make exit0, PDF8pages, no fatal/undefined references; layoutwarnings retained. Source SHA2565f2e8f3396ff4b5b0c0e78127454890deb95b398b4ce30217302add1982b74a5. Completed 2026-10-08T01:28:48.288007+00:00. Next fresh Round11 entry-baseline meaning audit.
