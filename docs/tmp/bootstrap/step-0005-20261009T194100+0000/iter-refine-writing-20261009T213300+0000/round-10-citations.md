# Round 10 — citation gate (independent read-only review)

Started: 2026-10-09T22:03:51Z (first recorded clock; initial reads preceded this clock). Completed: 2026-10-09T22:05:03Z. Parent: BOOTSTRAP step-0005-20261009T194100+0000; writing run iter-refine-writing-20261009T213300+0000. Objective: annotation gate followed by Pass 3 missing-citation review; scientific contract, implementation and paper sources remain read-only.

Entry SHA-256: main.tex `396c38b7c13cfaadef10c75bdb7a5de5c9d043416c8d955ba6305c50caf209d4`; references.bib `f55c6af75bd07eb090c76c243a82a703719be50e682edeea64f1be77fbd9ceb2`.

## Sources and procedure

Read docs/user-instruction.md first, full docs/paper/main.tex and docs/paper/references.bib, and the full actual filesystem skills /workspaces/.agent-state/codex/skills/check-paper-citations/SKILL.md and /workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md. Large combined output was supplemented with numbered paper reading and the middle design passage. No old reports, canon, implementation, Git, build artifacts or experiment files were consulted.

The special “When Called from iter-refine-writing” procedure applies: all 23 bib entries contain nonempty VERIFIED, REAL, PDF, ABSTRACT and USED_FOR blocks and all REAL values are yes. Consequently this reviewer ran Pass 3 only, not the full mechanical metadata verification, Passes 1/2/2.5, or a redundant citation ledger. Annotation completeness is a gate state, not fresh proof that the sources are real or correctly characterized. Existing annotated entries informed context only.

All 23 keys are cited: repl, leanSnapshot, z3api, z3params, fork, leanArena, mathlib, verusage, nanoclo, nanocloFortran, leanIncremental, kimina, boogieCache, sock, seuss, lean4, verus, kiminaPaper, procMemory, verusagePaper, cpuAffinity, leanpolishPaper, leanpolishSource. There are 44 cite commands. Examined factual claims, named systems/workloads, first-use provenance and borrowed mechanisms, then inspected section density in context of author-owned design and explicit result placeholders.

Actual external lookup was limited to actual gaps: opened official [Z3 C API](https://z3prover.github.io/api/html/group__capi.html), whose Z3_mk_solver documentation explicitly distinguishes incremental and nonincremental execution, and searched/opened official [CUDA 13.0.1 driver/runtime documentation](https://docs.nvidia.com/cuda/archive/13.0.1/cuda-runtime-api/driver-vs-runtime-api.html), which identifies runtime initialization and context/module management. Search also returned the current official [CUDA device management reference](https://docs.nvidia.com/cuda/cuda-runtime-api/cuda_runtime_api/group__CUDART__DEVICE.html); that search result was discovery, not a claim of verified metadata or installed runtime version. No new bib entry was created or annotated. Any NVIDIA source adopted by the root must pass the skill's mechanical source-entry check before a VERIFIED annotation; the archival documentation is not evidence of the installed version.

## Findings

### Must-fix

None in the current identified benchmark/workload first-use provenance. VeruSAGE, Verus, Mathlib and Lean Kernel Arena are cited in the setup. The still-unidentified source-native candidate streams remain explicit RESULT placeholders; their identities, versions and origin citations must be filled together when real sources are selected. This is a future evidence requirement, not permission to invent traces or substitute task corpora for native traffic.

### Should-fix

1. **Motivation, Scope and history effects, main.tex:70.** The factual statement “Scope effects can select a different solver path even in a fresh process” has no local citation. The introduction supplies z3api, but this central motivation paragraph should carry its own attribution. Concrete fix: append `\cite{z3api}` to that sentence, keeping the history-control result placeholder and causal distinction. Official Z3_mk_solver documentation describes switching from solver1 to solver2 for incremental use (push/pop included), so the existing source supports the scope-path point. Do not treat this source as a measured status-difference result or as proof of every possible prior-history effect.

2. **Implementation, Device path, main.tex:164.** “the existing NVIDIA runtime” names a borrowed runtime without identifying or citing its interface. Concrete fix: when the actual adapter API is established, name that API and cite its official documentation at this first runtime mention, preserving RTX 5090 and complete cost accounting. The official CUDA driver/runtime page above is a real primary candidate if the path uses CUDA Runtime API. Do not assume CUDA versus Driver API from vendor hardware, and do not claim its documented version is the experiment version. New entry verification remains a root prerequisite before annotation; no entry has been verified by this reviewer.

### Consider

1. **Introduction, main.tex:26.** The initial generic proof-generation statement about related attempts and accepted context has only Lean/REPL citations later in the paragraph. Adding the existing leanpolishPaper citation to that sentence would make candidate-stream motivation directly attributable without a new entry. This is optional: the paragraph already introduces concrete persistent tools, and the statement is qualitative rather than an unsupported numerical measurement. Keep attribution restricted to the released proof-improvement setting.

2. **Background, Prepared native state, main.tex:59.** This four-sentence paragraph has one cite command (two keys), below the literal one-per-two-sentence density heuristic. The opening sentence defines this paper's native prefix; the following sentences instantiate that definition. Consider adding existing z3api to the SMT sentence only if it is intended as a claim about a concrete native interface. Do not add citations to the author-owned definition merely to satisfy a count.

## Density and preservation

| Section | Cite commands | Assessment |
|---|---:|---|
| Introduction | 10 | Dense precedent paragraphs; uncited paragraphs mostly author-owned argument and design requirements. Optional opening attribution above. |
| Background | 12 | Specific Lean/SMT outcomes, source-checking boundaries and process properties have provenance; one definition paragraph has low literal density. |
| Motivation | 2 | Own measurements are explicitly missing; local solver scope attribution should be added. |
| Design | 2 | Own design dominates; PSS and reduction-dependency concepts cite existing sources. |
| Implementation | 3 | Copy-on-write and checker representations attributed; named runtime gap above. |
| Evaluation | 6 | Named available workloads/competitors and affinity cite provenance; missing results are not disguised external facts. |
| Discussion | 0 | Synthesis of this paper's design and evaluation contract. |
| Related work | 9 | Paragraphs attribute named mechanisms; caching paragraph has two separate citations, other groups multiple sources. |
| Conclusion | 0 | Paper-owned synthesis with explicit missing findings. |

Counts: 23 complete annotation blocks; 0 incomplete/unverified blocks; 0 newly mechanically verified entries; 0 hallucinations established (not a full authenticity audit); 0 inaccurate claims fixed; 0 missing citations added; 2 Should-fix and 2 Consider findings; 0 Must-fix findings. New source candidates: one runtime documentation family, conditional on actual API. Citation omissions requiring a new entry are not silently marked verified.

No paper, bib, scientific-contract, code, native tool, Git, build or experiment work was performed. Only this report was written. Four RQs, all evidence slots/result placeholders, full source/native checking, strongest matched competitors and RTX 5090 scope are unchanged. BOOTSTRAP present-tense system descriptions are treated as authorized intended submission prose, not implementation evidence. No numbers or results were invented, no claims were weakened, and no baseline was removed.

Fixes are unapplied because the caller owns paper edits. The root should decide the optional findings, add existing-source local citations where accepted, and identify/verify the runtime source if accepted. Compilation, page-count evidence and post-edit preservation checks belong to the root after fixes; none was run in this read-only review. This report is a round finding record, not a substitute verification ledger. Next node: root fixes and Round 11 meaning-preservation audit.

## Root disposition 2026-10-09T22:07:01.027839+00:00

S1 accepted existing z3api local citation; C2 accepted source attribution for concrete SMT command order rather than paper-owned prefix definition. C1 declined: generic domain framing is already illustrated with Lean/REPL; adding LeanPolish to all proof-generation streams would risk over-attributing its narrower symbolic proof-improvement setting. S2 accepted with actual interface distinction: paper says NVIDIA container runtime, not CUDA RuntimeAPI. Prior retained actual GPU runtime receipt has RuntimeClassnvidia/containerd/deviceplugin; pending new Job has no execution. Official NVIDIA overview retrieval returned82bytes containing only a quote; it is preserved as nvidia-documentation-failed-response.html and used for no claim. Optional bs4 import failed after retrieval; stdlib inspection establishes unusable body. Official NVIDIA repository pinned README a672e378ef91bea7dfe92c0ed274847fa1cb9236 retrieved2366bytes/SHA48b02fc0ee30add5cdb875f4be08a108c80b05ab377c0e0007f98b15d48b0d73 explicitly describes container runtime library/utilities. Retained docs/reference/nvidia-container-toolkit-a672e37-README.md. Mechanical single NEWentry check runtime-citation-check.log exits0/URLHEAD200 before annotation, API metadata unavailable is not promoted to metadata proof; manual primary title/author/source/access-year verification completes actual non-paper source. New annotated source nvidiaContainerToolkit, no installed version or device API inferred.

Updated count47citationcommands/24completeannotations;12slots/fourRQ/quantities unchanged. No citation removed. round-10-build.log exits0/eight pages. Remaining sources retain their existing verified records; scoped gate did not repeat full metadata passes. This is citation/documentation refinement only, not a new GPU result or scientific contribution. Next fresh Round11 cumulative audit against5553bfc including W1/round0–10.
