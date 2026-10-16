# Independent bounded source and claim review: constraint-evidence reuse

Observed 2026-10-16 UTC. Reviewed literature-20261016T1650/report.md. This is a finite source/novelty/evidence-boundary audit, not a new thesis/RQ adoption, whole-paper review, cache experiment or implementation assignment. I reread the canonical human instruction log, preserved Initial Narrative/four RQs, current paper abstract/introduction and the report. I inspected the relevant pinned Mathlib frontend lines and the E032 cross-input analysis's declared scope/mapping metadata. I opened the necessary primary sources below. The other independent reviewer owns exhaustive recomputation of the new trace associations/counts; I do not duplicate or certify that numerical audit here.

Only this source-review.md is written. No OMP/canonical/native file, Git state or active acquisition is changed or queried. No experiment/build/test is run.

## Judgment

**No blocking source or scientific-claim error identified in the report's present qualified conclusions.** Its high-risk judgment for generic exact-result caching, normalization/canonicalization, semantic implication indexing and untrusted arithmetic oracles is supported by primary sources. Its proposed larger complete-system claim remains unproved, not low risk or adopted. The report neither proves all reuse/GPU acceleration impossible nor converts this narrow existing-trace analysis into a completed paper/RQ.

This is selection pressure on a candidate mechanism, not a defensible novel mechanism or measured benefit by itself. Retaining the distinction between a reusable numeric solver result, a certificate that can be bound to the current Lean hypotheses, and complete verification cost is essential. The report mostly makes that distinction explicit, including its statement that certificate reuse/reconstruction has not executed.

## Primary-source verification

### KLEE: reuse and validation precede this candidate

I opened the [OSDI08 full primary text, section 3.3](https://www.usenix.org/legacy/event/osdi08/tech/full_papers/cadar/cadar_html/paper.html). It describes expression/constraint simplification and independence; a counterexample cache storing assignments plus an unsatisfiable sentinel; subset/superset lookup; and direct substitution to check whether a cached assignment still satisfies a larger query. It also describes separate/together cache/independence comparisons on deterministically replayed matched work.

Those facts support the report's generic-mechanism overlap and reusable measurement pattern. They do not establish Lean certificate compatibility, modern comparative performance or a mandatory five-minute setting. In particular, validating a reused satisfying assignment in KLEE and reconstructing a Lean contradiction from an unsatisfiability witness are different operations. The report does not conflate them as interchangeable implementations; the novelty pressure is at the broad reuse/validation level. No historical speed or CPU number is transferred.

### Green: canonical cross-analysis persistence is established; full PDF remains unread

The [official Green repository README](https://raw.githubusercontent.com/GreenSolver/green/master/README.md) explicitly describes simplification, canonization and caching results/intermediate computations in shared storage. The [author's indexed publications page](https://cs.sun.ac.za/~jaco/PAPERS/index.html) supplies the primary-authored abstract and FSE2012 bibliographic entry; that abstract describes persistence across runs, analyzed programs, analyses and locations.

The direct [author-hosted PDF](https://www.cs.sun.ac.za/~jaco/PAPERS/vgd12.pdf) was not accessible through my web open. I have not read or verified its full technical/evaluation text. Root's disclosure of failed PDF retrieval is therefore appropriate; I do not independently assert the exact number/reason of root's earlier attempts. The available primary abstract plus official README are sufficient for the stated broad overlap, not a detailed reproduction or numerical claim.

One citation-precision limitation is non-blocking: the report links the unavailable PDF while describing its indexed abstract. The indexed author-page link above makes the accessible evidence boundary clearer. An indexed author abstract must not be narrated as a newly downloaded full paper.

### GreenTrie: logical reuse, with publication status held to the actual record

The [primary arXiv record 1501.07174](https://arxiv.org/abs/1501.07174) names GreenTrie as a Green extension using logical implication, with reduction and logical subset/superset lookup through its index. Its comments state submission to ISSTA2015; that is not proof of acceptance. The report's preprint-only wording is correct.

This is sufficient evidence that implication-based reuse is not automatically a new claim merely because the frontend is Lean. It supplies no executed Lean baseline, certificate conversion, current artifact compatibility or independent verification of the preprint's measured gains. No such claim is made.

### Mathlib: the trusted reconstruction boundary is already source-native

I opened [official linarith frontend documentation](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Tactic/Linarith/Frontend.html) and read the actual pinned local Frontend.lean lines 41–49 and 98–110. Both describe an untrusted coefficient oracle, normalization/proof reconstruction and a replaceable oracle. The pinned API returns coefficients keyed by comparison indices; the certificate is converted to a proof term of False rather than accepted as an oracle verdict.

This supports the report's rejection of “untrusted accelerator plus Lean validation” as a standalone new architecture. The official latest documentation is not silently substituted for the pinned workload source. Neither source establishes useful GPU work, cheap certificate transport/rebinding, whole-query cache coverage or a current implementation of cross-original reuse.

## Claim distinctions

**Candidate claim 1: exact numeric-query reuse between original proofs.** Generic exact result reuse is established. The new original-input association may resolve an empirical ambiguity about where repeated numeric queries arose; it does not turn caching into a new mechanism. The report correctly labels an earlier same-input success separately from a different-input success, without equating same input with one oracle invocation or assuming an input-local cache is implemented.

**Candidate claim 2: canonicalization/semantic relations.** Green and GreenTrie directly threaten this mechanism-level claim. Numeric query equivalence is also not a certificate binding proof. Comparison order, variable/term association, strictness and exact coefficients must retain their actual meaning for Mathlib's current reconstruction. The existing report's “not cache compatibility for every trace record” qualification is appropriate. This is a limitation of present evidence, not a request to build a new correctness campaign or another semantic index.

**Candidate claim 3: shared evidence plus heterogeneous complete verification.** Neither the cited precedents nor the current analysis establishes the proposed differentiated complete resource frontier. Prior mechanisms do not logically rule out a larger contribution; combining them also does not establish one. The report correctly leaves the system-level claim unproved and avoids a new acronym, narrow adopted thesis or claimed OSDI readiness.

These judgments strip away names and frontend branding. Generic caching/normalization/implication, a GPU wrapper and native compilation cannot supply missing novelty on their own.

## Numerical/evidence scope, without duplicating the assigned full audit

The new analysis declares itself existing-data source association and screening, not executed cache/GPU/verifier evaluation. Its metadata describes exact logged-source/body equality to the actual service splitter output, a covered-source population smaller than the original 29,750 inputs, parsed versus malformed rows and a profile-specific denominator. I have read those declarations and their limitations; exhaustive reproduction remains with the separate numerical reviewer.

The report states that the cross-input-only sum is 275.541315451 seconds of logged call elapsed intervals and compares it numerically with 13,346.049945904 seconds of that same profile's whole clock. Its stated approximately 2.0645908% ratio is not presented as CPU savings, measured cache speedup or a strict Amdahl ceiling. That restriction is scientifically necessary: summed overlapping call intervals do not identify paid critical-path removal, publication/worker identities are unavailable, callback logging has ordering limits, and no reusable-certificate construction/lookup/recheck path was executed.

“Earlier logged success” does not prove that another worker could have consumed the evidence at the needed instant. Exact original-source association does not establish stable worker/cache identity, absence of unlogged calls, availability for every original input or evidence portability. These uncertainties remain visible in the report rather than being replaced by a perfect-cache implementation claim.

The Fast/hybrid profile is a different actual route from separately sampled compiled-original Meta/oracle CPU observations or a composed product candidate. The report correctly prohibits multiplying those cross-route fractions into the human-requested end-to-end independent-argument GPU bound. The exact-query slice also cannot disprove all semantic reuse, all proof reuse or all GPU acceleration. A small scoped descriptor is not a theorem of global impossibility.

## Baseline provenance and feasibility

The report appropriately assigns KLEE, Green and GreenTrie as citation-level mechanism precedents. Official source availability does not make their symbolic-execution constraints, interfaces, resource models or results a drop-in Lean oracle/certificate system. None has been reproduced as a compatible numerical Lean comparator here. Counting an incompatible or avoidably failing translation as a Lean baseline loss would be invalid; the report does not do so.

Mathlib's actual pinned oracle/proof-construction path and the strongest matched runnable CPU composition are source-native competing positions. A hypothetical perfect cache remains an opportunity/control construction, not an executed main-baseline cell. The stated matched-work ablation precedent comes from actual KLEE methodology, not an imported timing cap or a requirement to collect decorative baselines. This is a fair distinction between scientific overlap and numerical comparability.

No additional baseline execution or experimental task is assigned by this review.

## Human objective, report authority and retained uncertainty

The canonical user instructions still require real Lean-first acceleration, formal workloads, strong competent service/cache/snapshot comparison, meaningful RTX5090 evidence, SMT scope and a complete research/paper process. The intact Initial Narrative explicitly treats result caching, fork/COW and metadata reuse as prior mechanisms. This report is compatible with that research contract: it pressures a possible larger mechanism without replacing the original four RQs or declaring a narrower measurement paper complete.

The ordinary cache decision in “Root disposition” is a scoped current scientific judgment, not proof that every evidence-sharing route is exhausted. RQ1 native preparation, RQ2 supported behavior/artifacts/history/cancellation, RQ3 complete service resource frontier and RQ4 useful heterogeneous execution remain open. This source audit neither adopts another thesis nor overrides those goals.

Canonical OMP paper/background/evaluation edits and independent numerical verification are distinct deliverables. The current manuscript's existing prospective claims are not validated by this source handoff. There is no warrant here for a new feature, experiment quota, correctness program, language-level limitation or full-paper verdict. Preserve the report with the numerical review when it arrives and keep its exact source/denominator boundaries visible in any eventual claims.
