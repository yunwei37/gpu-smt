# Round 9: language flow and register

Timestamp: 2026-10-08 UTC. Scope: complete `docs/paper/main.tex` and `references.bib`, read-only paper review. Read `docs/user-instruction.md` and `docs/questions-for-author.md` first, then the complete paper-writing-style skill and paper sources. The skill names no required supporting references. This pass focuses on topic/stress position, old-to-new threading, paragraph transitions and academic register. The calling agent applies changes and builds; no paper edits or Git operations were performed.

All suggestions preserve the four exact RQ statements, all twelve result slots, citation coverage, numbers, strongest matched baselines, native behavior qualifications, complete Lean/SMT verification and the RTX 5090 goal. Present-tense descriptions of the intended system are permitted and are not flagged as implementation-status defects. Missing results are not treated as language defects.

## Must-fix (1)

### M1. Evaluation, behavior and isolation, L167: clarify the subject of the fidelity comparison

> “Per-input decisions and artifacts are retained through preceding unrelated attempts, branch cancellation and resource-limit conditions.”

Problem: “are retained” describes storage, while “through preceding” reads as an execution claim. The reader cannot tell whether this means outcomes remain unchanged or raw evidence is retained. This blurs the paragraph's transition from reference execution to interference controls.

Concrete fix: “We retain per-input decisions and artifacts for comparisons that vary preceding unrelated attempts, branch cancellation and resource-limit conditions.” This preserves the evidence-retention meaning without asserting equality before the comparisons finish. Keep the following sentence about native scope/history controls unchanged.

## Should-fix (7)

### S1. Abstract, L12: start from the workload and end on its reuse opportunity

> “Formal verification services check program and proof candidates against formal specifications as proof-generation systems submit streams sharing libraries, declarations and accepted context.”

Problem: “as” makes service semantics and workload locality appear simultaneous rather than causally connected. The first sentence also introduces two subjects before either becomes the paragraph's stable topic.

Concrete fix: “Proof-generation systems submit streams of program and proof candidates that formal verification services check against formal specifications. These candidates share libraries, declarations and accepted context.” The second sentence ends on the state that the next sentence contrasts with independent attempts.

### S2. Introduction, L24: connect the stage definitions to the workload

> “Proof assistants construct and check proof terms. Verifiers translate program obligations into requests to satisfiability modulo theories (SMT) solvers. Proof-generation systems submit streams of attempts that share libraries, declarations and accepted context.”

Problem: three consecutive short subject changes produce a textbook-definition sequence before the service problem emerges.

Concrete fix: “Services use proof assistants to construct and check proof terms, or verifiers to translate program obligations into requests to satisfiability modulo theories (SMT) solvers. Proof-generation systems submit streams of these attempts that share libraries, declarations and accepted context.” Retain the opening service sentence and both citation-bearing sentences/clauses, including Lean and REPL citations.

### S3. Introduction, L30: put the unresolved comparison in stress position

> “The unresolved comparison is whether separating native preparation from candidate execution history improves complete verification, cancellation and total memory across service processes at matched resources after these savings are available.”

Problem: the final “after these savings are available” is the backward link to the paragraph's established reuse mechanisms, but it arrives after the substantive comparison. The strongest baseline condition gets buried in an overlong sentence.

Concrete fix: “With these reuse mechanisms available, the unresolved comparison is whether separating native preparation from candidate execution history improves complete verification, cancellation and total memory across service processes at matched resources.” Preserve the matched-resource scope and every preceding baseline citation.

### S4. Design, heterogeneous checking, L123: group qualification and online measurement into a thread

> “Required online checks are charged to complete verification. Qualification does not imply a second full CPU replay on every request. Response and artifact fidelity follow Section~\\ref{sec:behavior}, including UNKNOWN and responses without artifacts.”

Problem: the paragraph alternates admission qualification, online checking cost and fidelity, then switches again to fallback costs. This obscures the relationship between pre-admission testing and online validation.

Concrete fix for the paragraph's first part: “Supported device work preserves verifier semantics. Before admission, device qualification compares operation outputs with matched CPU references. During execution, enclosing native verification checks the resulting proof or requested artifact, and required online checks are charged to complete verification. Qualification does not imply a second full CPU replay on every request. Response and artifact fidelity follow Section~\\ref{sec:behavior}, including UNKNOWN and responses without artifacts.” Keep all subsequent CPU fallback and complete-cost sentences and their scope unchanged. The explicit before/during links carry the reader between qualification and execution without weakening either.

### S5. Implementation, native adapters, L129: avoid repeating the full grammatical subject

> “It preserves options, scopes, checks and requested artifacts, and compares fresh driver execution with the matched standalone executable. Comparing fresh driver execution separates interface incompatibility from differences caused by branching.”

Problem: the exact phrase “fresh driver execution” repeats immediately, which stalls the otherwise clear progression from preservation to qualification.

Concrete fix: “It preserves options, scopes, checks and requested artifacts, and compares fresh driver execution with the matched standalone executable. This comparison separates interface incompatibility from differences caused by branching.” The referent is the immediately preceding single comparison and therefore remains unambiguous. Keep the rejected-adapter diagnostic and admission restrictions.

### S6. Evaluation, L164/L169/L174/L179: replace recurring status-report endings with claim-facing requirements

> “RQ1 remains unanswered until ...”; “RQ2 remains unanswered until ...”; “RQ3 remains unanswered until ...”; “RQ4 remains unanswered until ...”

Problem: identical progress-report endings disrupt four otherwise claim-organized subsections. They are honest evidence requirements, but their diary register gives the reader project status instead of explaining what establishes each answer.

Concrete fixes, retaining every result slot verbatim and the four exact RQ statements:

- L164: “Answering RQ1 requires complete source-native measurements that establish whether preparation sharing is consequential.”
- L169: “Answering RQ2 requires a recorded outcome for every planned behavior comparison and an explanation of residual differences.”
- L174: “Answering RQ3 requires comparison with the strongest competent services over the complete workload and resource matrix.”
- L179: “Answering RQ4 requires measured complete boundaries that establish a device benefit or a negative opportunity bound.”

These rewrites preserve incompleteness and the full evidence bar rather than suggesting completed results.

### S7. Related work, prepared execution, L197: express the novelty condition in academic register

> “Verification specialization alone supplies no novelty over these systems.”

Problem: “supplies no novelty” reads as a reviewer-directed defensive remark, interrupting the mechanism-to-comparison progression. The technical condition itself is essential and should remain.

Concrete fix: “A contribution beyond these prepared-execution systems requires more than specialization to verification.” Keep the preceding SOCK/SEUSS citation and following sentence specifying the native-behavior and bounded-sharing test. This changes register while preserving the novelty condition.

## Consider (2)

### C1. Introduction, L36: reduce the nested actor structure

> “We present a verification service that retains immutable prepared states in a parent performing no candidate verification and executes disposable independent branches with their own responses, mutable state and cancellation.”

Problem: the nested parent clause separates retention from branch execution, the sentence's main parallel actions.

Concrete fix: “We present a verification service whose parent retains immutable prepared states and performs no candidate verification. The service executes disposable independent branches with their own responses, mutable state and cancellation.” Accept if the extra sentence improves the paragraph at typeset width; reject if the current paragraph already wraps cleanly and this creates another run of short statements. All technical content is retained.

### C2. Background, L48: put the boundary distinction before its example

> “Post-export checker replay begins after the source frontend has already run. These boundaries distinguish savings in candidate construction, library setup and proof checking ...”

Problem: the paragraph shifts from kernel checking to post-export replay before telling the reader why these stage boundaries matter.

Concrete fix: “These stage boundaries distinguish savings in candidate construction, library setup and proof checking~\\cite{leanArena,repl}. In particular, post-export checker replay begins after the source frontend has already run.” Keep the preceding Lean stages and Lean citation. Accept only if the caller prefers an explicit example transition; the current order is also coherent.

## Review disposition and verification

Totals: 1 Must-fix, 7 Should-fix, 2 Consider. Top three changes are clarifying evidence retention in RQ2 (M1), moving the established-baseline condition to the start of the unresolved comparison (S3), and replacing repeated evaluation status endings with claim-facing evidence requirements (S6).

No sentences were changed in the paper. All findings remain suggestions for the root. No compilation was run by this read-only reviewer; the root is responsible for applying accepted fixes, checking the diff for preserved content/citations and compiling. No recommendation removes a result slot, changes an exact RQ, substitutes a weaker baseline, or narrows the Lean/SMT/RTX 5090 goal.

## Root disposition, build and preservation

M1 applied: explicitly retains evidence for controlled comparisons, avoiding an unsupported parity implication. S2,S3,S4,S5 applied as local threading/grammar changes; all native stages, strongest reuse/equal resources, qualification versus online costs and adapter restrictions retained. S7 applied the positive statement of the same substantive non-novelty condition; no novel-mechanism assertion is added. S1 rejected: its two-sentence abstract opening would change the strict entry role-unit correspondence while the current as-clause supplies context without claiming experimental causality. S6 rejected for the same recorded Round8 phase-policy reason: explicit unanswered endings are mandatory in BOOTSTRAP, with full evidence conditions intact. C1 rejected because splitting exceeds the deliberately rebuilt five-sentence overview limit; actor ownership already explicit. C2 retained current chronological stage-to-post-export sequence, which supports the boundary distinction directly. Every finding disposed; no number or slot edits.

Root directly compared user instructions, full scope and all changes. Paragraph-sized diff inspected. Exact4RQ strings/12slots and multiset of34cite expressions/quantities match entry d224cd2d991439940e5b4b108b55b53c6a1b8525; bibliography unchanged. make exit0, PDF8pages, no fatal or undefined-reference errors; layoutwarnings remain. Source SHA2564f7b985614b67d0d9b7dcb5f7c697e342affd4ae3ed3f24754a120f27e343ea5. Completed 2026-10-08T01:26:42.021293+00:00. Exact child start/end times were not captured in its report; only review-date and root-observed completion are recorded, not invented. Next Round10 citation Pass3 unless unverified/missing bib annotations are actually found.
