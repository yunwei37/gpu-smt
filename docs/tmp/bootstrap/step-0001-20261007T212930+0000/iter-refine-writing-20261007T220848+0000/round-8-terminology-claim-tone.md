# Round8: terminology-claim-tone

Started 2026-10-07T22:22:02.107Z; reviewer returned 2026-10-07T22:23:20.875Z; root completed 2026-10-07T22:24:37.015898+00:00. Parent step0001 WRITE_GATE. Source diff baseline 5b66cd7e698f5d8a60fae2b67bbb02b42727a09e; original entry tree remains0cf6486e5a40cc0d7740462ddfb69d2e945144a5. Fresh read-only reviewer gpt-6.1-sol loaded full paper/bib and requested full skill sources through filesystem adaptation (no Skill tool). No reviewer edits/Git/build. Evidence/source journal rollout-2026-10-07T22-22-02-01a11875-9777-7661-ba8d-2bbb84757e50.jsonl.

## Root dispositions and verification

Applied all3 Must-fix: independently expand SMT in abstract/Intro, expand community REPL in Intro, use full copy-on-write instead of undefined COW. Applied all4 Should-fix: inline frontier definition (keep other standard uses), replace unexplained protected adjective with responses/artifacts or observable behavior, define proportional/fleet memory at first design use, explain duplicate completion as result reuse for exact duplicate attempts (root contract explicitly includes exact result caches). All3 Consider individually rejected: fallback/UNKNOWN caveat and both snapshot/COW novelty boundaries are clear substantive scope, not apologies; proposed tone rewrites risk changing novelty into an unsupported affirmative claim. Human honesty prevails. Four numbered RQs verbatim, no technical content removed. Root confirms user-file wrapper read and findings align with all direct instructions.

Root reviewed subsection-sized apply_patch edits and source diff. make -C docs/paper exits0. Pages:           7; citation commands 27, never decreased; four RQs match entry tree verbatim; no quantitative value invented or changed. Scope conditions and negative/mixed-result permission protected. Paper SHA256 da3857760cd7eaa618283ae5a2c9d6d922c88d02e8d372a4812c4d71fbffff3b. Intended incomplete submission, not final venue compliance or answered RQs. Next serial round after this full compile/check.

## Verbatim independent reviewer return

Read-only Round 8 completed. Read the full user instructions, `docs/questions-for-author.md`, paper, bibliography, and both requested dependency skills. Applied the J → C → F → X review sequence, followed by claim-tone review. No edits, Git operations, or builds.

**Must-fix**

1. **Abstract, L19; Introduction, L24 — C2/J6: SMT never expanded.**  
   “SMT-backed verification” assumes neighboring-field terminology.  
   Fix first abstract use to “verification backed by satisfiability modulo theories (SMT) solvers.” Independently expand SMT at first introduction use because the abstract should stand alone. Preserve the four RQs.

2. **Introduction, L30 — C2: REPL never expanded.**  
   “The community REPL” appears without explaining the interface.  
   Fix to “The community read–eval–print loop (REPL)” or “The community read–eval–print loop (REPL) interface.” Retain its backtracking and pickling capabilities and citation.

3. **Design / Bounded placement, L116 — C2: COW never introduced.**  
   Background uses the full “copy-on-write,” but its abbreviation is not established.  
   Minimal fix: use “copy-on-write sharing” at L116. No abbreviation is needed elsewhere.

**Should-fix**

4. **Introduction, L34; Evaluation, L146; Conclusion, L204 — J1/C2: “resource frontier” lacks a definition.**  
   “The service’s resource frontier” and “equal-resource service frontier” ask readers to infer the relationship between latency, throughput, and memory.  
   At L34, explain it inline: “These requirements connect compatibility to the latency and throughput achievable within a fixed CPU and memory budget.” At L146/L204, use “equal-resource latency, throughput and memory tradeoff,” preserving all three dimensions. Alternatively define “frontier” explicitly at first use without changing the evaluation.

5. **Motivation, L68; Design, L71 — C2: “protected responses / protected observable behavior” precedes the interface definition.**  
   “Protected” could suggest an additional unnamed policy, while the actual comparison is explained at L104.  
   Fix L68 to “A speedup from a path that changes the verifier responses or requested artifacts is excluded…” and L71 to “preserve the native verifier’s observable behavior.” Keep the artifact-equivalence rules at L104; do not imply byte identity.

6. **Evaluation / Setup, L159; Process handling, L140; RQ3, L174 — J6/F9: proportional memory is not explained.**  
   “Fleet proportional memory” does not tell readers how shared pages contribute to total fleet cost.  
   At its first measurement use, explain that proportional memory attributes each shared page across the processes sharing it, and that fleet memory sums these attributed amounts. Use the same phrase consistently afterward. Do not invent a measurement implementation.

7. **Evaluation / RQ1, L162 — J1/F9: “Exact duplicate completion” is ambiguous.**  
   It could mean duplicate inputs, duplicate outputs, or completed duplicate jobs.  
   Suggested wording, **if it matches the intended control**: “Reuse of results for exact duplicate attempts, sharing of ordered native prefixes, and sharing of native environments are analyzed separately.” Confirm the intended meaning from the root’s scientific contract; do not silently reinterpret it.

**Consider**

8. **Design / Observable behavior, L108 — claim-tone mechanics.**  
   “Fallback follows interface compatibility, rather than treating every UNKNOWN response as a detector of divergence” preserves an essential boundary but reads defensively.  
   Possible rewrite: “Fallback is selected by interface compatibility. An UNKNOWN response alone does not identify divergence.” Keep the following UNSAT-versus-UNKNOWN explanation.

9. **Related work / Prepared execution, L198 — self-attack phrasing with substantive novelty boundary.**  
   “Verification specialization alone supplies no novelty over these systems” addresses reviewers directly. The boundary must remain.  
   Possible rewrite: “Our contribution beyond these systems must lie in preserving native verification behavior and improving bounded service performance, rather than in preparation sharing itself.” Retain the following matched-comparison sentence and citations.

10. **Related work / Persistent state, L192 — claim-tone mechanics.**  
    “This distinction requires matched evidence, rather than a novelty claim for snapshots themselves” carries a necessary scope boundary.  
    Possible rewrite: “Matched evidence must establish the value of independent execution, cancellation and bounded fleet resources beyond existing snapshots.” Preserve the explicit distinction from snapshot novelty either here or in the neighboring sentence.

**Concept inventory**

Locations below cover first establishment and subsequent use families; ordinary systems terms are distinguished from paper-specific concepts.

| Concept family | Establishment / clarification | Use locations |
|---|---|---|
| Verification service; program/proof candidate; attempt stream | L12, L24 | Abstract, Introduction, Motivation, Design, Implementation, Evaluation, Discussion, Conclusion |
| Native preparation / prepared state | L16–18; native prefix defined L55; boundary L99 | L26–43, L54–71, architecture, L96–118, L130–174, L192–204 |
| Native execution history; logical context; scope/history effects | L14; examples L28; prefix/configuration L55–57 | L32–41, L65–71, L99–108, L133, L167–169, L195, L204 |
| Independent branch; prepared parent; child; candidate lifetime/cancellation | L18; L36; detailed ownership L96, L110–113; Linux mechanism L138 | Architecture, L99–118, L130–140, RQ2/RQ3, L192–204 |
| Candidate suffix | First use L36; defined L99 | L104–106, L133, L138, L167 |
| Supported native boundary; quiescence; adapter qualification | L17, L36; clarified L101 and L130–135 | Architecture, Design, Implementation, L182–186 |
| Native resource state/counters; separate service accounting; resource-bounded behavior | L14, L18, L28; distinction L57 and L106 | L34–36, L108, L138, L159, RQ2, L182 |
| Verifier behavior/fidelity; decisions/responses; requested artifacts | L14; stages/outcomes L50–52; interface definition L104 | L41, L68–71, L108, L125–143, RQ2, Discussion, Conclusion |
| Lean environment; proof state; elaboration; kernel checking; admissions | L24, L28–30; stages and acceptance boundaries L48–55 | Design, adapters, Evaluation, Discussion, Related work |
| SMT session; SAT/UNSAT/UNKNOWN; model/proof/unsatisfiable core | SMT unexpanded; outcomes enumerated L50; behavior L104 | Abstract/Introduction, Motivation, adapters, RQ2, Related work |
| Persistent environment; REPL; snapshots; backtracking/pickling; bounded warm service | L15, L30; background references L55 | Motivation, Implementation comparison, Evaluation baselines, Related work |
| Copy-on-write/COW; private dirty pages; proportional memory; retention/placement; concurrency/fan-out | Copy-on-write L57; placement/memory L116; process behavior L138–140 | Architecture, Motivation, Design, setup, RQ3, Discussion |
| Resource/equal-resource frontier | First use L34, undefined | L146, L174 placeholder, L204 |
| Heterogeneous checking; device operation; CPU fallback; complete verification | L19, L36; boundaries L48; detailed costs L120–127 | Implementation device path, RQ4, Discussion, Related work |
| Expression graph; binder environment; instantiated constant; dynamic work | L123, with causal explanation | L177–179, L201 |
| Resident primitive / metadata primitive; representation construction; delayed substitution / integer identifiers | L127; implementation L143; metadata primitive L188 | RQ4, Discussion, Related work |
| Candidate latency; throughput/completed attempts; makespan; CPU time; fleet memory; affinity | L159 metric enumeration; affinity distinguished from isolation | RQ3, Conclusion; proportional-memory definition missing |
| Exact duplicate completion; native prefix/environment sharing; unrelated-work control; preparation depth | L162–164 | RQ1; duplicate-completion wording ambiguous |
| Startup-only branches; mechanism ablations; warm workers; offered-load/concurrency sweep | L172–174, explained in context | RQ3 |
| Source verification versus post-export checking; strongest measured CPU path | L48; baseline boundary L157; RQ4 L177 | Abstract, Design, Evaluation, Discussion, Related work |
| VeruSAGE/Verus; Mathlib; Lean Kernel Arena; Kimina; Nanoclo; SOCK/SEUSS | Introduced with citations and roles | Setup and Related work; no rename needed |

J0 frequency audit found no excessive core-concept budget: most hyphenated phrases are meaningful standard modifiers. Low-frequency qualifiers generally carry scope and should remain.

No additional F/X blocker was found. The preparation → boundary → branch → observable behavior → lifecycle → resource accounting → heterogeneous-cost sequence remains coherent. “Branch,” “child,” and “parent” describe process roles consistently; “proof-state branching” remains distinct from process branching. The figure’s “immutable native prefix” is understandable through L55 and the surrounding design, although “immutable prepared state” would align more directly with the body.

**Scientific-contract concerns, separately:** no newly discovered scientific defect requiring a writing-round mechanism or RQ change. Final measurements, qualified boundaries, strongest matched baselines, and workload identities remain explicitly missing. These are protected evidence gaps, not tone defects. Preserve every unanswered-RQ sentence, negative-result boundary, resource-limit caveat, supported-boundary restriction, post-export distinction, and artifact-equivalence qualification.

Totals: **3 Must-fix, 4 Should-fix, 3 Consider.** Most useful changes are expanding abbreviations, replacing or defining “resource frontier,” and explaining proportional memory.
