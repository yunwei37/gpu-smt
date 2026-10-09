# Round 10 — Citation gate

Started: 2026-10-09T19:28:00Z (approximate first-read time). Completed: 2026-10-09T19:31:06Z.
Parent: BOOTSTRAP step-0004-20261009T183603+0000 / iter-refine-writing-20261009T190400+0000. Objective: fresh read-only citation gate; root owns paper fixes, compilation and persistence.

## Instructions, sources and conditional exception

Read `docs/user-instruction.md` first, then the complete actual filesystem skills `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md` and `/workspaces/.agent-state/codex/skills/check-paper-citations/SKILL.md`. No Skill tool was available, so the filesystem procedures were used directly. Read the complete `docs/paper/main.tex` and `docs/paper/references.bib`; repeated the middle source slice to recover any display truncation.

Checked annotation blocks before selecting the verification branch. All 20 entries have nonempty VERIFIED, REAL, PDF, ABSTRACT and USED_FOR fields, all are REAL: yes, and all verification dates are 2026-10-07. The called-from-iter exception explicitly says that when all annotations are present and REAL: yes, “just check for missing citations in the .tex (Pass 3 only).” Applied that exception: did not run the generic mechanical/API precheck or repeat Passes 1, 2 or 2.5 for unchanged already verified entries. This gate does not assert fresh independent authenticity, metadata, publication or retraction verification. No annotation state was modified.

Entry paper SHA256: `531287be822d7d492b082a16f7f72a521c06e5b0fad8697cc74a3867514cea5e`.
Entry bibliography SHA256: `5c76f124f744cdd62d7ea5ed6d8312bc89599c2d763bcacc02388c7c602b0835`.
These content fingerprints identify the reviewed revision without any Git operation.

## Method and evidence

Ran Pass 3 on factual claims, original-source attribution of named systems/techniques/datasets/benchmarks, and section density. Distinguished external factual assertions from the paper's own definitions, design, method, analytical consequences and explicit missing-result placeholders. No arbitrary citation quotas were imposed. Abstract citations were not demanded when the named tool and surrounding claims receive source support in the introduction/body.

Mechanical local citation inventory: 39 cite commands, 20 distinct cited keys, zero undefined citation keys. All 20 bibliography entries are used. This inventory checks key resolution only, not external authenticity.

First mentions and provenance are supported for Lean (`lean4`), community REPL (`repl`), Z3 (`z3api`), result caching (`boogieCache`), native proof-state snapshotting (`leanSnapshot`), stock incremental snapshots (`leanIncremental`), warm services (`kimina`, `kiminaPaper`), native resources (`z3params`), copy-on-write/runtime constraints (`fork`), proportional memory (`procMemory`), Mathlib (`mathlib`), Lean Kernel Arena (`leanArena`), Verus (`verus`), VeruSAGE tasks (`verusage`, `verusagePaper`), alternative CPU checkers (`nanoclo`, `nanocloFortran`), and prepared execution (`sock`, `seuss`). Generic SAT/UNSAT/UNKNOWN terminology, language names and the selected RTX 5090 device do not independently require original academic citations absent an externally asserted performance or capability claim. “Existing NVIDIA runtime” identifies implementation context without claiming a named runtime version; the intentional setup placeholder owns eventual configuration provenance.

Introduction external mechanism claims have nearby citations; its uncited paragraphs introduce the paper's own tradeoff and proposal. Background has local source support for frontend/kernel stages, native artifacts, admissions, prepared state and resources. Design/Implementation mainly describe this paper's mechanism; borrowed process, accounting and checker representations are cited. Motivation's unanswered empirical characterizations remain explicit placeholders; repeated scope/history premises already receive Z3 support in the introduction, so no duplicate citation was demanded simply for density. Related Work paragraphs all cite the systems or methods they compare and explain their relevance. No unnamed completed measurement was mistaken for established external evidence.

One new-source search was needed for the uncited affinity assertion. Searched the official Linux man-pages source and read [sched_setaffinity(2)](https://man7.org/linux/man-pages/man2/sched_setaffinity.2.html). Its Description defines affinity as eligible CPUs and explains that dedicating a CPU also requires excluding other threads; its Notes distinguish affinity from CPU isolation and state that masks are per-thread. This directly supports the existing sentence's distinction. No paper/PDF download was needed for this official HTML manual, and no download was authorized in this review-only task. A future new bibliography entry must complete its own mechanical verification and annotations; this report does not mark a proposed entry VERIFIED.

## Raw findings and concrete suggestions

**Must-fix:** None found in the current Pass 3 scope. The unnamed final candidate-stream identities and versions are intentional BOOTSTRAP placeholders, not named datasets silently lacking origin citations. Root must retain source citation requirements when those identities are eventually filled, but that is not a current prose defect.

**Should-fix — Evaluation / Experimental setup, main.tex line 171.** Problem: “Affinity specifies permitted CPUs but alone does not provide CPU isolation” is a concrete external Linux mechanism claim without a local source. Suggested fix: retain the sentence and add a citation to the official `sched_setaffinity(2)` manual immediately after the isolation assertion (or at the sentence end). Suggested entry title `sched_setaffinity(2) Linux manual page`, corporate author `Linux man-pages project`, URL `https://man7.org/linux/man-pages/man2/sched_setaffinity.2.html`, with an explicitly labeled access date/year. USED_FOR should describe permitted-CPU masks and the distinction from isolation. Follow the full new-entry verification requirements before writing VERIFIED: yes; no existing verified entry needs rechecking merely because this entry is added.

**Consider:** None. Extra repeat citations to already introduced baseline families would add density without correcting a provenance gap.

## Preservation and decisions

All four exact RQs were read and remain protected:

1. How much expensive native preparation can real verification candidate streams share across independent jobs?
2. Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?
3. How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse?
4. After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?

Protected baseline families: competent bounded warm services with cache/environment mechanisms; native logical or serialized prepared-state reuse; fresh native behavior/preparation controls; startup-only and deeper-prefix branches; independent warm workers; strongest runnable complete CPU checker at a matched source or post-export boundary. Protected scope includes native response/artifact fidelity, UNKNOWN, admissions/incomplete attempts, supported runtime boundaries, equal CPU and memory resources, complete setup/transfer/fallback costs, fleet memory, RTX 5090 and honest negative/mixed device outcomes.

No claims, quantities, RQs, baseline meanings, cited sources, bibliography fields or intentional placeholders were changed. BOOTSTRAP prose was evaluated as the intended completed submission; present-tense system descriptions were not flagged because implementation status may be unfinished. Result values were neither supplied nor demanded as citation fixes.

Applied fixes: none, because this subagent is read-only. Rejected fixes: no blanket density additions, no redundant authenticity/API run, no result invention, no future-tense rewrite. Alternative considered: cite existing procMemory/fork references for affinity; rejected because their existing annotated uses concern memory/process semantics and do not specifically source affinity versus isolation. Direct official affinity documentation is clearer.

## Scope, tree changes and handoff

Only this requested round report was written. No paper, bibliography, Git, code, build, reference-download, memory or other report edits were performed. No compilation or page-count check was run; root owns applying the one Should-fix suggestion, verifying any new bibliography entry, compiling and checking page evidence before Round 11. This is an iterative round report, not a standalone verification ledger; `.bib` annotations remain the sole verification-state record.

Counts: 20 previously annotated verified entries accepted for conditional gate eligibility; 0 entries newly externally verified; 0 hallucinations established in this limited pass; 0 inaccurate claims fixed; 0 missing citations added; 1 missing-citation finding with an actual official source identified. No current annotated entry is REAL: unverified. PDFs marked “not available” were accepted as complete annotations under the explicit gate exception.

Next node: root applies/evaluates Should-fix, records its decision and build/page result, then runs serial Round 11 meaning-preservation audit.

## Root citation fix and completed verification

2026-10-09T19:32:11.635815+00:00: S1 accepted. Root opened the complete official sched_setaffinity manual and confirms the source defines eligible CPU masks and separate exclusion of other threads; no new performance assertion. Added cpuAffinity corporate-author/manual entry (accessyear2026/date2026-10-09) and its local cite. New-entry mechanical verifier ran unchanged official verify_bib.py on a temporary one-entry bibliography, exit0 URL fallback; exact log round10-new-entry-verification.log. Temporary input is removed by TemporaryDirectory, no standalone ledger or paper source copy. Only after exit0/manual metadata and claim review was VERIFIED/REALyes written. HTML manual has no abstract/PDF, its description/notes are the primary source; no venue/retraction/selfcitation/secondary attribution applies. Existing20entries unchanged/annotation-gated; newentry1verified, hallucinations0established, inaccurateclaims0, missingcitations1added. Citecommands40distinctkeys21; protected numeric data and exact4RQstrings/12slots unchanged. Fresh make exit0/PDF8pages (round10-build.log). Round11 cumulative meaning audit against entry3b035d29182f676ccfe2eaba8a483af5aa9cd0b3 next.
