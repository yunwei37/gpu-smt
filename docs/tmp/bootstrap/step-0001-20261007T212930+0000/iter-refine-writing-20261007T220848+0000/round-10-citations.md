# Round 10 — Full citation verification

Started: 2026-10-07 22:24 UTC. Parent: bootstrap step-0001, WRITE gate. Review only: root applies paper and bibliography fixes. Complete user instructions, questions-for-author, main.tex, references.bib, iter-refine-writing skill and research-workflow-dependencies/check-paper-citations skill read. All 15 bibliography entries lack annotations, requiring full mechanical verification and manual Passes 1, 2, 2.5 and 3.

## Mandatory initial mechanical precheck

Actual command: `python3 /workspaces/.agent-state/codex/skills/research-workflow-dependencies/check-paper-citations/scripts/verify_bib.py docs/paper/references.bib`. Initial attempted `python` command failed because executable absent; the actual python3 run completed with exit 1. Raw output below.

```text
Found 15 bib entries (15 active)
repl: No API match; URL HEAD HTTP 200; SKIP metadata comparison (API unavailable)
leanSnapshot: Querying arXiv 2605.25556; OK title; OK year; SKIP venue; ERROR MISMATCH author count: bib=0 api=2; ERROR MISSING author field
z3api: No API match; URL HEAD HTTP 200; SKIP metadata comparison (API unavailable)
z3params: No API match; URL HEAD HTTP 200; SKIP metadata comparison (API unavailable)
fork: No API match; URL HEAD HTTP 200; SKIP metadata comparison (API unavailable)
leanArena: No API match; URL HEAD HTTP 200; SKIP metadata comparison (API unavailable)
mathlib: No API match; URL HEAD HTTP 200; SKIP metadata comparison (API unavailable)
verusage: No API match; URL HEAD HTTP 200; SKIP metadata comparison (API unavailable)
nanoclo: No API match; URL HEAD HTTP 200; SKIP metadata comparison (API unavailable)
nanocloFortran: No API match; URL HEAD HTTP 200; SKIP metadata comparison (API unavailable)
leanIncremental: No API match; URL HEAD HTTP 200; SKIP metadata comparison (API unavailable)
kimina: No API match; URL HEAD HTTP 200; SKIP metadata comparison (API unavailable)
boogieCache: No API match; URL HEAD HTTP 200; SKIP metadata comparison; ERROR MISSING author field
sock: No API match; URL HEAD HTTP 200; SKIP metadata comparison; ERROR MISSING author field
seuss: No API match; URL HEAD HTTP 200; SKIP metadata comparison; ERROR MISSING author field
Total entries checked: 15
Errors (must fix): 5
Warnings (should review): 0
FAIL: 5 entries have errors that must be fixed (add url/doi, fix metadata, etc.)
```

The output is retained above without terminal decoration; HTTP reachability establishes existence only. No entry has been marked VERIFIED. Root promptly notified of missing author fixes grounded in arXiv, Microsoft PDF, USENIX and SEUSS PDF first pages. Manual passes await root corrections and a successful rerun.

## Corrected mechanical precheck

Root applied four author repairs plus CAV and SOCK published metadata. Actual same script rerun completed exit 0: 15 active entries; 0 errors; 0 warnings; all 15 still unannotated. arXiv returned matching snapshot title/year/two authors; Crossref returned matching Boogie title/year/two authors/venue; DBLP/Semantic Scholar returned matching SOCK title/year/seven authors/venue. The other twelve passed reachable-URL fallback and explicitly SKIPPED metadata comparison. This is permission to begin manual verification, not evidence that URL fallback checked metadata.

## Pass 1 — Primary-source existence, metadata, and annotation-ready content

All original 15 references are real; none is hallucinated. For software and documentation, venue/pages/DOI are not applicable unless a published paper is separately cited. Institutional attribution denotes the artifact organization, not a complete academic author list. The software/documentation year 2026 should be explicitly identified as access/version year using `note={Accessed 2026-10-07}`; it is not an independently verified creation year. No source reports a venue or DOI for the artifact itself. Root owns annotation insertion after the final mechanical check. All rows below are REAL: yes and have VERIFIED date 2026-10-07 eligible only after the corresponding entry passes the mechanical check.

| Key | Primary source and metadata | PDF | ABSTRACT (annotation-ready) | USED_FOR (annotation-ready) |
|---|---|---|---|---|
| repl | https://github.com/leanprover-community/repl; Lean community artifact. README command/tactic/pickling sections read. | not available (software documentation) | Lean REPL exposes persistent environment and proof-state identifiers, diagnostics and admissions. It supports backtracking and pickling relative to imported environments. | Persistent Lean environments, backtracking, pickling, and admission diagnostics. |
| leanSnapshot | https://arxiv.org/abs/2605.25556; Austin Shen and Yunong Shi; 2026; arXiv v2; DOI 10.48550/arXiv.2605.25556; no published venue/pages identified. | docs/reference/lean-snapshot-2605.25556.pdf | Captures elaborated Lean language-server proof state once and reuses it across parallel tactic branches, avoiding repeated import loading and theorem-body elaboration. | Existing proof-state reuse and parallel tactic branching baseline. |
| z3api | https://z3prover.github.io/api/html/group__capi.html; Z3 contributors; API documentation. Z3_eval_smtlib2_string and Z3_mk_solver sections read. | not available (API documentation) | Documents native SMT command evaluation that retains state between calls, solver outcomes and artifact interfaces. The combined solver can change solving modes with incremental use. | Native ordered SMT evaluation, requested artifacts, and Z3 combined-solver scope behavior. |
| z3params | https://microsoft.github.io/z3guide/programming/Parameters/; Z3 contributors; parameter documentation; rlimit/timeout/proof/model/core entries read. | not available (documentation) | Documents solver configuration including resource limits distinct from elapsed-time limits and optional artifact generation. | Internal work limits and configured output support. |
| fork | https://man7.org/linux/man-pages/man2/fork.2.html; Linux man-pages project; Linux system-call documentation. | not available (manual page) | Describes Linux process duplication and copy-on-write memory, inherited file descriptions, reset process accounting, noninherited timers and restrictions after multithreaded fork. | Process sharing, branch-owned communication and runtime/resource handling requirements. |
| leanArena | https://github.com/leanprover/lean-kernel-arena; Lean contributors; artifact README test/export/checker sections read. | not available (software documentation) | Runs alternative Lean kernel implementations on exported declarations, including library workloads, soundness regressions, corner cases and performance tests. | Post-export checker workloads and benchmark boundary. |
| mathlib | https://github.com/leanprover-community/mathlib4; Lean community; artifact README read. | not available (software documentation) | Provides the community Lean 4 mathematical library and source development corpus. | Source/library workload provenance, not generated-attempt locality. |
| verusage | https://raw.githubusercontent.com/microsoft/verus-proof-synthesis/cbf9c0c6337b224fd8e5b7cb4e01ae65c0f98bc1/benchmarks/VeruSAGE-Bench/README.md; Microsoft Research artifact at the cited revision. | not available (artifact documentation); origin paper docs/reference/verusage-2512.18436.pdf separately | Provides standalone proof tasks extracted from real Verus systems with source mappings and verified ground-truth solutions. | Repository-derived systems verification task provenance; not a native candidate-stream trace. |
| nanoclo | https://arena.lean-lang.org/checker/nanoclo/; page attributes modifications to Sebastian Graf directing Claude; artifact version a2aa37e at review. | not available (software documentation) | Lean kernel checker uses delayed substitutions and closures over interned environments; conversion and parser components derive from existing checkers. | Existing delayed-substitution representation and alternative CPU checker. |
| nanocloFortran | https://arena.lean-lang.org/checker/nanoclo-fortran/; version b3a13ef at review. | not available (software documentation) | Fortran translation of nanoclo stores kernel objects in parallel arrays referenced by integer identifiers, with immutable exported expressions and private worker contexts. | Existing integer-indexed representation and alternative CPU checker. |
| leanIncremental | https://lean-lang.org/doc/reference/latest/releases/v4.32.0/; release July 13, 2026; Lean contributors. | not available (release documentation) | Experimental CLI flags save full or import-only elaboration snapshots and reuse saved state up to syntactic differences on a later invocation. | Native incremental elaboration snapshots baseline. |
| kimina | https://github.com/project-numina/kimina-lean-server; Project Numina; README plus server/manager.py and settings.py read. | not available (software artifact); associated paper docs/reference/kimina-2504.21230.pdf separately | Serves parallel Lean REPL processes and reuses warmed import headers. Manager bounds pool size and retires exhausted workers using configured use and memory controls. | Bounded warm service, environment reuse and worker retirement baseline. |
| boogieCache | https://www.microsoft.com/en-us/research/publication/fine-grained-caching-verification-results/ plus published metadata https://dblp.org/rec/conf/cav/LeinoW15; K. Rustan M. Leino and Valentin Wüstholz; CAV Part I 2015; pp.380–397; DOI 10.1007/978-3-319-21690-4_22. | docs/reference/boogie-cache-krml245.pdf | Instruments Boogie programs with cached verification information and dependency tracking to avoid rechecking unaffected program regions after changes. | Established fine-grained verification-result caching. |
| sock | https://www.usenix.org/conference/atc18/presentation/oakes; Edward Oakes, Leon Yang, Dennis Zhou, Kevin Houck, Tyler Harter, Andrea C. Arpaci-Dusseau and Remzi H. Arpaci-Dusseau; ATC 2018 pp.57–70; publisher USENIX; no DOI listed by publisher. | docs/reference/sock-atc18-oakes.pdf | Optimizes serverless container initialization and caches prepared interpreter/library state using generalized Zygotes to reduce provisioning costs. | Prior prepared execution and memory-sharing mechanism. |
| seuss | https://handong32.github.io/docs/3342195.3392698.pdf; James Cadden, Thomas Unger, Yara Awad, Han Dong, Orran Krieger and Jonathan Appavoo; EuroSys 2020; 15 pages; DOI 10.1145/3342195.3392698. | docs/reference/seuss-eurosys20.pdf | Deploys serverless functions from unikernel snapshots and shares pages across the software stack to avoid initialization and increase cached execution density. | Prior prepared execution and page-sharing mechanism. |

Eight public primary PDFs were downloaded with urllib and read through pdftotext (abstract and introduction, including source first pages). SOCK initially returned HTTP403; a public browser User-Agent retry succeeded, without credentials. No inaccessible content was claimed read. URLs for downloads are the original bib/PDF URLs above, plus https://arxiv.org/pdf/2504.21230, https://arxiv.org/pdf/2512.18436, https://lean-lang.org/papers/lean4.pdf and https://matthias-brun.ch/assets/publications/verus_oopsla2023.pdf. No source checkouts were created.

## Pass 2 — Every existing cited claim

All existing citation occurrences were inspected in complete main.tex. The following exhaustive grouped mapping records every cited sentence (source line numbers refer to the entry paper, and root additions can shift them).

| Entry paper location | Cited keys | Result and precise source support |
|---|---|---|
| Introduction line24 persistent environments | repl | Supported: README `env` identifier selects earlier environment. Add original Lean reference separately. |
| Introduction line30 REPL, snapshot, incremental, bounded workers | repl; leanSnapshot; leanIncremental; kimina | Supported: README backtracking/pickling; snapshot PDF abstract/intro; release incremental compilation flags; Kimina manager pool bound and exhausted-worker closure. Add Kimina paper for scholarly origin. |
| Background line48 frontend/kernel/post-export | leanArena; repl | Arena supports export boundary; REPL supports elaboration interface. These are insufficient original references for complete Lean architecture: add Lean4 original and retain Arena for post-export boundary. |
| Background line50 SMT statuses/artifacts | z3api | Supported by solver outcome and model/proof/core interfaces, with existing backend-support qualifier protected. |
| Background line55 persistent prefix/proof states | repl; leanSnapshot | Supported by environment IDs and elaborated proof-state reuse; does not prove arbitrary process cloning safe. |
| Background line57 command state, limits, fork runtime | z3api; z3params; fork | Supported: command-evaluation interface retains previous state; rlimit is distinct from timeout; fork manual covers COW/timers/thread/descriptors. Exact bounded status history remains own empirical question. |
| Motivation line63 environments and parallel snapshots | repl; leanSnapshot | Supported without extrapolating snapshot speedups to this service. |
| Implementation line130 command evaluation | z3api | Supported precisely by Z3_eval_smtlib2_string. |
| Implementation line138 Linux private pages | fork | Supported by COW semantics; branch isolation of external shared descriptors still requires design handling. |
| Implementation line143 existing integer/delayed layouts | nanoclo; nanocloFortran | Supported; source page explicitly names each representation. |
| Setup line155 VeruSAGE, Mathlib, Arena | verusage; mathlib; leanArena | Supported as task/library/export workloads; none establishes ordered generated attempt traffic. Existing final stream identity TODO preserves this limitation. Cite original Verus at first named use. |
| Setup line157 warm/cached/prepared competitors | kimina; repl; leanIncremental | Supported, respective roles clear in surrounding sentences. Retain strongest baseline configuration TODO. |
| RQ4 line179 parsing/reduction can dominate parallelism | nanoclo; nanocloFortran | Should-fix: artifact descriptions establish differing algorithms and implementations, not a universal causal dominance result. Say `The comparison includes tuned alternative CPU checkers with different parsing and reduction algorithms...`; reserve measured dominance for profiling evidence. |
| Related work line192 persistent state | repl; leanSnapshot; leanIncremental; kimina | Supported; avoid treating snapshots as new. Add Kimina scholarly origin beside artifact. |
| Related work line195 command histories/caching | z3api; boogieCache | Supported: evaluator state and Boogie unchanged-region instrumented caching. |
| Related work line198 prepared execution/density | sock; seuss | Supported by actual systems mechanisms, abstract/intro; neither is evidence of verifier compatibility. |
| Related work line201 representations | nanoclo; nanocloFortran | Supported directly by checker descriptions. Generic initial `GPU and CPU checker representations` sentence is paper framing and attributes no borrowed GPU result. |

## Pass 2.5 — Integrity

Exact-title publication and retraction searches were run for the original four scholarly references (snapshot, Boogie, SOCK, SEUSS), and for proposed original Lean4, Verus and Kimina references; VeruSAGE origin was checked separately. No retraction notice was found. This is a recorded search outcome, not proof no notice exists. Snapshot remains a 2026 preprint: arXiv v2 and author's site both identify it as a preprint; no published replacement found. Boogie is CAV2015 PartI, SOCK ATC2018, SEUSS EuroSys2020. Verus is the published PACMPL/OOPSLA1 version, not its extended arXiv version. Kimina is accepted to the 5th MATH-AI Workshop at NeurIPS2025, not the NeurIPS main conference; primary arXiv v3 and workshop PDF corroborate. OpenReview forum browser challenge prevented reading forum metadata, while its PDF and author publication page were available.

No identity-leaking self-citation, ghost citation or unexplained claim-specific string citation was found. Multi-source representation/persistent-state sentences explain distinct supporting sources. Secondary citations were not substituted for original mechanisms: SOCK and SEUSS are cited for their own designs, Boogie for its own instrumented caching; original Lean and Verus additions repair tool-origin gaps. VeruSAGE official Verus projects page lists a December2026 NeurIPS version, which is future-dated relative to October7; retain verifiable arXiv identity until published metadata becomes available, rather than invent proceedings/pages.

## Pass 3 — Missing citations and findings

**Must-fix M1 — Bibliography authors and published metadata.** Initial mechanical errors were fixed by root. Complete SEUSS published metadata (EuroSys2020; 15 pages; DOI10.1145/3342195.3392698), and snapshot DOI/arXiv designation. Full academic author lists above were confirmed from primary first pages. Root must mechanically check final additions before adding VERIFIED annotations.

**Must-fix M2 — Background and first Lean mention.** Add original `lean4` CADE2021 reference at first named Lean use and frontend/elaborator/kernel explanation. Published title `The Lean 4 Theorem Prover and Programming Language`; Leonardo de Moura and Sebastian Ullrich; CADE28; pp625–635; DOI10.1007/978-3-030-79876-5_37; URLhttps://lean-lang.org/papers/lean4.pdf. REAL yes; PDF docs/reference/lean4-cade21.pdf; ABSTRACT: Reimplements Lean in Lean with extensible parsing, elaboration and proof automation and efficient native compilation; describes its trusted kernel and extensibility architecture. USED_FOR: Original Lean4 frontend and kernel architecture. Abstract/intro and kernel sections read.

**Must-fix M3 — First Verus mention in Experimental setup.** Add original `verus` PACMPL7 OOPSLA1 article85 (2023), 30pages, DOI10.1145/3586037. Full nine authors and source URL supplied above to root. REAL yes; PDF docs/reference/verus-oopsla2023.pdf; ABSTRACT: SMT-based Rust verifier uses linear ghost permissions and a mode system distinguishing specification, proof and executable code. USED_FOR: Original Verus verification architecture and systems tool provenance.

**Must-fix M4 — Introduction factual scope claim.** Cite Z3 C API for the combined-solver switch and qualify example as Z3 behavior; do not assert all SMT backends share it. Source Z3_mk_solver states push/pop or further assertions after checking switch modes. The prior-history/resource-response claim needs retained regression evidence and remains an empirical causal TODO, not something generic documentation verifies. Concrete suggestion: `For Z3's combined solver, incremental scopes can select a different solving path...` with z3api immediately attached. Add repl/Lean4 for elaborator state sentence without claiming mutable extensions are universally clone-safe.

**Should-fix S1 — RQ4 causal attribution.** Replace `because their parsing and reduction algorithms can dominate parallelism alone` with `with different parsing and reduction algorithms`. The cited source describes representations; dominance is an experiment outcome. This preserves competitor selection and avoids inventing a measured result.

**Should-fix S2 — PSS definition in Bounded placement.** Add `procMemory`, Linux kernel contributors, `The /proc Filesystem`, URLhttps://docs.kernel.org/filesystems/proc.html, access date2026-10-07. REAL yes; PDF not available; ABSTRACT: Documents proc memory accounting including smaps proportional set size and private/shared dirty pages. USED_FOR: Definition of proportional memory attribution and measurement source. Primary source explicitly divides pages across mapping processes. Cite after the PSS definition, not as evidence of this service's measured memory.

**Should-fix S3 — Kimina original paper.** Add `kiminaPaper` alongside artifact for reuse design origin, with workshop venue accurate. Title `Kimina Lean Server: A High-Performance Lean Server for Large-Scale Verification`; nine authors in arXiv order: Marco Dos Santos; Hugues de Saxcé; Haiming Wang; Ran Wang; Mantas Bakšys; Mert Ünsal; Junqi Liu; Zhengying Liu; Jia Li. 2025; 5th MATH-AI Workshop at NeurIPS2025; URLhttps://openreview.net/pdf?id=orPt2nxLoC or arXiv2504.21230; DOI10.48550/arXiv.2504.21230 denotes arXiv, not a workshop DOI; pages not assigned. REAL yes; PDF docs/reference/kimina-2504.21230.pdf; ABSTRACT: Parallel Lean REPL service uses LRU import-header reuse and client batch feedback for large-scale proof verification. USED_FOR: Established parallel warm service and import reuse baseline. Worker retirement supported by artifact manager, not attributed to paper alone.

**Should-fix S4 — Version/access provenance.** Document 2026 as access year for live software pages using note field; pin runnable benchmark versions in existing setup TODO. Nanoclo page explicitly credits Sebastian Graf-directed development, so consider author attribution `Sebastian Graf` for checker modifications instead of treating Lean Kernel Arena as creator; preserve inherited algorithm attribution and avoid fabricated person lists for community artifacts.

**Consider C1 — VeruSAGE origin paper.** Add `verusagePaper` alongside pinned artifact. Chenyuan Yang; Natalie Neamtu; Chris Hawblitzel; Jacob R. Lorch; Shan Lu. Title `VeruSAGE: A Study of Agent-Based Verification for Rust Systems`; arXiv2512.18436 (2025; v2 April2026); DOI10.48550/arXiv.2512.18436. REAL yes; PDF docs/reference/verusage-2512.18436.pdf; ABSTRACT: Studies agent proof generation on tasks extracted from real Verus Rust systems and introduces VeruSAGE-Bench. USED_FOR: Original dataset construction and task provenance. Do not interpret fixed tasks as measured generated-attempt locality.

Design, implementation and the four unchanged RQs mostly describe this paper's own mechanism and evaluation, so citation density there is intentionally lower. Background paragraphs gained precise original/tool documentation citations; Introduction needs source citations at the actual factual premises above, not mechanical citations on every design-argument sentence. Result placeholders, RTX5090 requirement, resource qualifiers, fallback limits, workload scope and present-tense intended submission narrative are protected. No unfinished implementation was treated as a writing contradiction; no numerical source results were imported.

## Review-only boundary and next step

Only this report and downloaded public primary PDFs were written by this review agent. No .tex/.bib edits or Git mutations. Root owns concrete fixes, annotations, final actual mechanical check, compilation and page count. Report is a required round node record, not a separate maintained citation ledger. Final additions remain ineligible for VERIFIED until root's final mechanical run passes them.

## Final full-bibliography mechanical output

```text
Found 20 bib entries (20 active)

--- repl (line 1) ---
  Verified: unknown
  No API match; checking URL: https://github.com/leanprover-community/repl...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- leanSnapshot (line 5) ---
  Verified: unknown
  Querying arXiv: 2605.25556
  OK title
  OK year
  OK author count (2 vs 2)
  SKIP venue (not available from API)

--- z3api (line 9) ---
  Verified: unknown
  No API match; checking URL: https://z3prover.github.io/api/html/group__capi.html...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- z3params (line 13) ---
  Verified: unknown
  No API match; checking URL: https://microsoft.github.io/z3guide/programming/Parameters/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- fork (line 17) ---
  Verified: unknown
  No API match; checking URL: https://man7.org/linux/man-pages/man2/fork.2.html...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- leanArena (line 21) ---
  Verified: unknown
  No API match; checking URL: https://github.com/leanprover/lean-kernel-arena...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- mathlib (line 25) ---
  Verified: unknown
  No API match; checking URL: https://github.com/leanprover-community/mathlib4...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- verusage (line 29) ---
  Verified: unknown
  No API match; checking URL: https://github.com/microsoft/verus-proof-synthesis/tree/cbf9...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- nanoclo (line 33) ---
  Verified: unknown
  No API match; checking URL: https://arena.lean-lang.org/checker/nanoclo/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- nanocloFortran (line 37) ---
  Verified: unknown
  No API match; checking URL: https://arena.lean-lang.org/checker/nanoclo-fortran/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- leanIncremental (line 41) ---
  Verified: unknown
  No API match; checking URL: https://lean-lang.org/doc/reference/latest/releases/v4.32.0/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- kimina (line 45) ---
  Verified: unknown
  No API match; checking URL: https://github.com/project-numina/kimina-lean-server...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- boogieCache (line 49) ---
  Verified: unknown
  Querying CrossRef: 10.1007/978-3-319-21690-4_22
  OK title
  OK year
  OK author count (2 vs 2)
  OK venue

--- sock (line 55) ---
  Verified: unknown
  Querying DBLP by title
  Querying Semantic Scholar by title
  No API match; checking URL: https://www.usenix.org/conference/atc18/presentation/oakes...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- seuss (line 61) ---
  Verified: unknown
  Querying CrossRef: 10.1145/3342195.3392698
  OK title
  OK year
  OK author count (6 vs 6)
  OK venue

--- lean4 (line 68) ---
  Verified: unknown
  Querying CrossRef: 10.1007/978-3-030-79876-5_37
  OK title
  OK year
  OK author count (2 vs 2)
  OK venue

--- verus (line 74) ---
  Verified: unknown
  Querying CrossRef: 10.1145/3586037
  OK title
  OK year
  OK author count (9 vs 9)
  OK venue

--- kiminaPaper (line 81) ---
  Verified: unknown
  Querying arXiv: 2504.21230
  OK title
  OK year
  SKIP venue (not available from API)
  ERROR: MISMATCH author count: bib=2 api=9

--- procMemory (line 87) ---
  Verified: unknown
  No API match; checking URL: https://docs.kernel.org/filesystems/proc.html...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- verusagePaper (line 91) ---
  Verified: unknown
  Querying arXiv: 2512.18436
  OK title
  OK year
  OK author count (5 vs 5)
  SKIP venue (not available from API)


============================================================
Total entries checked: 20
Errors (must fix): 1
Warnings (should review): 0

ERRORS:
  - kiminaPaper: MISMATCH author count: bib=2 api=9

FAIL: 1 entries have errors that must be fixed (add url/doi, fix metadata, etc.)
```

Exit status: 1

## Updated paper inspection and new-entry alignment

Root-added references and modified main.tex were read in full again. First Lean citation, explicit original stage citation, admission citation, combined-Z3 scope qualification, artifact+paper Kimina attribution, proc PSS definition, and separate VeruSAGE/Verus origins all align with primary sources. New five references were subjected to Pass1 (primary metadata and PDF abstract/intro where applicable), Pass2 (exact new claims), Pass2.5 (published version and integrity searches), and Pass3 (original named-system gaps). All proposed summaries above remain usable.

The first 20-entry mechanical run exited1 solely for Kimina author counting: the actual nine-author field was preserved, but the supplied script's count_bib_authors partial regex split after the nested accent brace counted two segments and bypassed its plain-split fallback. This is a parser formatting limitation, not an incorrect author list. Source-correct Unicode diacritics were recommended to root to remove ambiguous nested accent braces without deleting authors. No entry marked VERIFIED during this failing run.

The final inspection retains one pending Should-fix causal-overattribution sentence in RQ4 (S1). Source pages establish differing parsing/reduction designs; the paper's experiments must establish dominance. Root was notified to apply the precise replacement above. The snapshot DOI is a scholarly identifier completion, not a new result. No additional missing mandatory system/benchmark citation remains after root additions.

## Corrected final 20-entry mechanical run

```text
Found 20 bib entries (20 active)

--- repl (line 1) ---
  Verified: unknown
  No API match; checking URL: https://github.com/leanprover-community/repl...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- leanSnapshot (line 5) ---
  Verified: unknown
  Querying arXiv: 2605.25556
  OK title
  OK year
  OK author count (2 vs 2)
  SKIP venue (not available from API)

--- z3api (line 10) ---
  Verified: unknown
  No API match; checking URL: https://z3prover.github.io/api/html/group__capi.html...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- z3params (line 14) ---
  Verified: unknown
  No API match; checking URL: https://microsoft.github.io/z3guide/programming/Parameters/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- fork (line 18) ---
  Verified: unknown
  No API match; checking URL: https://man7.org/linux/man-pages/man2/fork.2.html...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- leanArena (line 22) ---
  Verified: unknown
  No API match; checking URL: https://github.com/leanprover/lean-kernel-arena...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- mathlib (line 26) ---
  Verified: unknown
  No API match; checking URL: https://github.com/leanprover-community/mathlib4...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- verusage (line 30) ---
  Verified: unknown
  No API match; checking URL: https://github.com/microsoft/verus-proof-synthesis/tree/cbf9...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- nanoclo (line 34) ---
  Verified: unknown
  No API match; checking URL: https://arena.lean-lang.org/checker/nanoclo/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- nanocloFortran (line 38) ---
  Verified: unknown
  No API match; checking URL: https://arena.lean-lang.org/checker/nanoclo-fortran/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- leanIncremental (line 42) ---
  Verified: unknown
  No API match; checking URL: https://lean-lang.org/doc/reference/latest/releases/v4.32.0/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- kimina (line 46) ---
  Verified: unknown
  No API match; checking URL: https://github.com/project-numina/kimina-lean-server...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- boogieCache (line 50) ---
  Verified: unknown
  Querying CrossRef: 10.1007/978-3-319-21690-4_22
  OK title
  OK year
  OK author count (2 vs 2)
  OK venue

--- sock (line 56) ---
  Verified: unknown
  Querying DBLP by title
  Querying Semantic Scholar by title
  No API match; checking URL: https://www.usenix.org/conference/atc18/presentation/oakes...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- seuss (line 62) ---
  Verified: unknown
  Querying CrossRef: 10.1145/3342195.3392698
  OK title
  OK year
  OK author count (6 vs 6)
  OK venue

--- lean4 (line 69) ---
  Verified: unknown
  Querying CrossRef: 10.1007/978-3-030-79876-5_37
  OK title
  OK year
  OK author count (2 vs 2)
  OK venue

--- verus (line 75) ---
  Verified: unknown
  Querying CrossRef: 10.1145/3586037
  OK title
  OK year
  OK author count (9 vs 9)
  OK venue

--- kiminaPaper (line 82) ---
  Verified: unknown
  Querying arXiv: 2504.21230
  OK title
  OK year
  OK author count (9 vs 9)
  SKIP venue (not available from API)

--- procMemory (line 88) ---
  Verified: unknown
  No API match; checking URL: https://docs.kernel.org/filesystems/proc.html...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- verusagePaper (line 92) ---
  Verified: unknown
  Querying arXiv: 2512.18436
  OK title
  OK year
  OK author count (5 vs 5)
  SKIP venue (not available from API)


============================================================
Total entries checked: 20
Errors (must fix): 0
Warnings (should review): 0

INFO: 20 entries still unverified:
  - repl
  - leanSnapshot
  - z3api
  - z3params
  - fork
  - leanArena
  - mathlib
  - verusage
  - nanoclo
  - nanocloFortran
  - leanIncremental
  - kimina
  - boogieCache
  - sock
  - seuss
  - lean4
  - verus
  - kiminaPaper
  - procMemory
  - verusagePaper

OK: No VERIFIED entries have mismatches
```

Exit status: 0

## Completion and applied-finding audit

Completed: 2026-10-07 22:33 UTC. Corrected final actual20-entry script exits0 with0errors and0warnings; full unabridged output retained above. All20 entries now qualify for REAL:yes / VERIFIED:2026-10-07 annotations after manual primary-source inspection. Twelve live documentation/artifact entries have no PDF and correctly say `not available`; eight scholarly PDFs are retained. URL-only verification was never presented as metadata checking.

Root applied M1–M4, S1–S3, access provenance S4, and C1. RQ4 now says alternative checkers have different parsing and reduction algorithms, removing unmeasured causal dominance without changing RQ4 or competitor scope. Root confirmed Unicode author names compile successfully. CAV/SOCK/SEUSS scholarly metadata, snapshot DOI and full author lists are corrected. Nanoclo institutional artifact attribution is retained with explicit modification credit rather than assuming collection ownership implies creator authorship; this is a reasonable handling of the optional attribution suggestion. Updated source placements are supported; no remaining Must-fix or substantive Should-fix citation defect identified.

The citation gate verifies20 real entries, finds0 hallucinated references, repairs initial5 mechanicalerrors plus published metadata, adds5 missing sources, and corrects1 causal-overattribution sentence plus1 solver-scope qualification. It does not validate missing experiment results or a universal clone-safety claim. Retained empirical TODOs, all4RQ meanings, numerical values, wall-time/resource qualifiers, unsupported-boundary fallback and workload limits remain protected. No Git operation or paper/bib mutation was performed by this agent. Root next inserts20annotationblocks, checks mechanicalscript on annotatedbib, compiles/checkspages, then proceeds Round11 meaningpreservation audit.

## Root final disposition and compile

Completed 2026-10-07T22:34:27.917777+00:00. All M1–M4 and S1–S4 applied; C1 origin reference accepted. Five original-reference author/metadata errors repaired,5 primary references added,8 PDFs retained. Exact sources above; no hallucinated citations. Root inserted20 complete VERIFIED/REAL/PDF/ABSTRACT/USED_FOR blocks only after corrected actual20entrypass and manualpasses. Nanoclo collection attribution retained with explicit Claude/SebastianGraf modification credit and upstream provenance; no sole-full-authorship assertion. Unicode Kimina names preserve exact9authors and avoid provided checker's separator-parsing bug; no verifier source altered. Actual final annotated-bib script exits0 with0errors/0warnings. Seven additional citation commands (27→34); no originalcitation deleted. One source-unsupported causal algorithm-dominance clause replaced with documented algorithm difference (S1); no numeric result or RQ changed.

make exits0 and pdfinfo7pages, no undefined references/citations. PDF is a bootstrap draft, not venue-ready format. Source diff against78a5c4ecfb2fadb63ea70365269a0345d6321487 inspected. Paperscope/APIexample bounded; native history outcome cause remains own empirical question. Complete final annotated-check stdout:

```text
Found 20 bib entries (20 active)

--- repl (line 6) ---
  Verified: 2026-10-07
  No API match; checking URL: https://github.com/leanprover-community/repl...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- leanSnapshot (line 15) ---
  Verified: 2026-10-07
  Querying arXiv: 2605.25556
  OK title
  OK year
  OK author count (2 vs 2)
  SKIP venue (not available from API)

--- z3api (line 25) ---
  Verified: 2026-10-07
  No API match; checking URL: https://z3prover.github.io/api/html/group__capi.html...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- z3params (line 34) ---
  Verified: 2026-10-07
  No API match; checking URL: https://microsoft.github.io/z3guide/programming/Parameters/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- fork (line 43) ---
  Verified: 2026-10-07
  No API match; checking URL: https://man7.org/linux/man-pages/man2/fork.2.html...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- leanArena (line 52) ---
  Verified: 2026-10-07
  No API match; checking URL: https://github.com/leanprover/lean-kernel-arena...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- mathlib (line 61) ---
  Verified: 2026-10-07
  No API match; checking URL: https://github.com/leanprover-community/mathlib4...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- verusage (line 70) ---
  Verified: 2026-10-07
  No API match; checking URL: https://github.com/microsoft/verus-proof-synthesis/tree/cbf9...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- nanoclo (line 79) ---
  Verified: 2026-10-07
  No API match; checking URL: https://arena.lean-lang.org/checker/nanoclo/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- nanocloFortran (line 88) ---
  Verified: 2026-10-07
  No API match; checking URL: https://arena.lean-lang.org/checker/nanoclo-fortran/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- leanIncremental (line 97) ---
  Verified: 2026-10-07
  No API match; checking URL: https://lean-lang.org/doc/reference/latest/releases/v4.32.0/...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- kimina (line 106) ---
  Verified: 2026-10-07
  No API match; checking URL: https://github.com/project-numina/kimina-lean-server...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- boogieCache (line 115) ---
  Verified: 2026-10-07
  Querying CrossRef: 10.1007/978-3-319-21690-4_22
  OK title
  OK year
  OK author count (2 vs 2)
  OK venue

--- sock (line 126) ---
  Verified: 2026-10-07
  Querying DBLP by title
  Querying Semantic Scholar by title
  No API match; checking URL: https://www.usenix.org/conference/atc18/presentation/oakes...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- seuss (line 137) ---
  Verified: 2026-10-07
  Querying CrossRef: 10.1145/3342195.3392698
  OK title
  OK year
  OK author count (6 vs 6)
  OK venue

--- lean4 (line 149) ---
  Verified: 2026-10-07
  Querying CrossRef: 10.1007/978-3-030-79876-5_37
  OK title
  OK year
  OK author count (2 vs 2)
  OK venue

--- verus (line 160) ---
  Verified: 2026-10-07
  Querying CrossRef: 10.1145/3586037
  OK title
  OK year
  OK author count (9 vs 9)
  OK venue

--- kiminaPaper (line 172) ---
  Verified: 2026-10-07
  Querying arXiv: 2504.21230
  OK title
  OK year
  OK author count (9 vs 9)
  SKIP venue (not available from API)

--- procMemory (line 183) ---
  Verified: 2026-10-07
  No API match; checking URL: https://docs.kernel.org/filesystems/proc.html...
  OK URL reachable via HEAD (HTTP 200)
  SKIP metadata comparison (API unavailable)

--- verusagePaper (line 192) ---
  Verified: 2026-10-07
  Querying arXiv: 2512.18436
  OK title
  OK year
  OK author count (5 vs 5)
  SKIP venue (not available from API)


============================================================
Total entries checked: 20
Errors (must fix): 0
Warnings (should review): 0

OK: No VERIFIED entries have mismatches

```

Downloaded public primary PDFs and SHA256:

- docs/reference/boogie-cache-krml245.pdf 9d377aeea50b3b27f80af759b11b3f5a29ac1698d7b13c6cf8e96412423e8c42
- docs/reference/kimina-2504.21230.pdf 8199a3c1c1877e7468d3149034a7b5740fde1a4ce681d16b6e8b194d723a4b4d
- docs/reference/lean-snapshot-2605.25556.pdf 127f5797d9c06cda0f4db328d851a49cc05ef8df5b351e08f922e7caa063882a
- docs/reference/lean4-cade21.pdf 2b907e98552f5ff4fe77be717f9423311a4d6bf4ac866b143d99f34e83f39c4d
- docs/reference/seuss-eurosys20.pdf 5c03186cbaed4ecd19fa05e87e6a356b5ca778e515f531ffb4670a61aa27dddd
- docs/reference/sock-atc18-oakes.pdf 46eaf854117d01586437ec82fd76e397dae178d2c3c2dd97f597551c0b463d93
- docs/reference/verus-oopsla2023.pdf 03147944a3934c08e2da40c59e2f9e15b63ada56260ddb4fc26d76a1dd72550a
- docs/reference/verusage-2512.18436.pdf 54ef4cd725d479eed3a803c23d187964798c2e2a5f7924372e92207b290ad42a

Next Round11 fresh entry-tree meaning audit; no citation ledger added.
