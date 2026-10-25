# Public Lean code-verification assets — primary-source review

Root thread alone,2026-10-25UTC; research-literature-novelty and experiment
design used for workload preparation, not another system reproduction.

## Questions, searches and source boundary
Find released code-verification inputs/reference proofs with native tactic
work that mathematical miniF2F may miss. Determine exact source/toolchain and
admission/stub status before measuring. Source/tactic tokens do not answer
runtime concentration or GPU opportunity. Candidate scheduling and external
certificate interfaces are established mechanisms, not novelty claims.

Queries: 'Verina Lean program verification benchmark github',
'miniCodeProps Lean benchmark github', 'FVAPPS Lean dataset github',
'CLEVER Lean code verification benchmark github', 'FVAPPS official github
dataset Lean Galois', 'lean-mlir benchmarks bv_decide Lean official github'.
Primary GitHub/HuggingFace/readmes, Lean official documentation and exact
GitHubAPI commits/trees are checked. Secondary search hits are only leads.
Coverage is these public assets and actual toolchain/interface availability,
not an exhaustive novelty survey or a theorem-prover reproduction.

## Verified assets and decision
| Official asset | Exact commit | Native toolchain | Preparation finding |
|---|---|---|---|
| [Verina](https://github.com/sunblaze-ucb/verina) |66b3ce5014edafb20cb26b87c681e7f31847249f|4.18.0|189actual task files;46lack explicit admission tokens; typedchecking still required|
| [miniCodeProps](https://github.com/cmu-l3/minicodeprops-eval)|58e3dd999e7d2dbdf09a39dba2f9bf97e457c7e8|4.9.0;bundled REPL test references4.9rc1|Definitions/Properties/Sorts/Solutions and released JSONL present; library/test files are not201checked proofs|
| [CLEVER](https://github.com/trishullab/clever)|8348039a7ff7730a126d761e71d0439735eeb3e2|4.27.0|Many human_eval files retain proof/spec stubs; sample proofs can engage native checking but do not prove full benchmark solved|
| [lean-mlir](https://github.com/opencompl/lean-mlir)|b8c4a771319a044854a4bbb49b8821381ef86ff8|nightly-2025-12-01;subprojects carry distinct pins|Real compiler refinement goals and bv_decide/grind/omega paths; many sorry-bearing generated files, do not call all complete proofs|

[FVAPPS dataset](https://huggingface.co/datasets/quinn-dougherty/fvapps)
currently requires agreeing to contact-information sharing for file access.
Its public card pins4.12.0 and primarily offers proof stubs. No access agreement
is accepted and no gated data is fetched. Continue accessible assets instead
of blocking or requesting user credentials.

[Official BVDecide documentation](https://lean-lang.org/doc/api/Lean/Elab/Tactic/BVDecide.html)
distinguishes preprocessing, bitblasting/CNF, external SAT, LRAT checking and
reflection; an input mentioning bv_decide is not evidence that SAT dominates.
[Lean4.34 release](https://lean-lang.org/doc/reference/latest/releases/v4.34.0/)
also changes preprocessing and grind interaction; keep each benchmark's exact
version rather than borrowing its newer performance claims.

## Actual acquisition, coverage and preservation
All four official commit/tree metadata are saved, trees untruncated.
Selected original UTF8 source/license/toolchain/build manifests are retained
losslessly in artifacts/lean-code-verification-2026-10-25/*-sources.jsonl.gz,
not rewritten as proof candidates. No alternate checkout/Workspace, verifier
run, model baseline or new service starts. The compressed files total about
2.1MB. Preparation has joint memory evidence covering the live480root.

The comment-stripped census is source filtering only: lean-mlir has18files
with bv_decide tokens and24with grind;92files without explicit admissions
contain at least one target token. Verina has46such files; CLEVER4and
miniCodeProps3include auxiliary/library/test sources. Countscope is explicit:
definitions, inactive alternatives and macros can still contain tokens.
No token count is a dynamic tactic count, completion or timing result.

## Next actual work and novelty boundary
Prepare matching SDK/dependencies in the owning Workspace's temporary storage,
then profile real reference files at their own native versions when the sole
current group retires. Measure actual invocations/statuses and stage wall/CPU,
including incomplete and failed proofs, SAT/LRAT byte/call statistics, setup
and cleanup; no search for a GPUkernel until actual work supports one.
The three directions continue without an admission threshold or deadline.
A useful systems mechanism and a fair paired result still must be shown.
No new external implementation/benchmark baseline is reproduced.

The canonical related-work file already has foreign dirty edits; preserve
them. This owned node and evaluation link record the source findings without
staging or overwriting that file. User instructions/completeInitialNarrative
and latest scope are respected. This is self-review, not independent audit.
