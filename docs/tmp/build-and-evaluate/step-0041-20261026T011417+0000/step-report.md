# Step0041 — preserve original compiler context
Observed 2026-10-26T01:26:16.211645+00:00; BUILD_AND_EVALUATE. Root thread only; reviews below are self-review.
This is an implementation dependency, not an answered research question.

## EXPERIMENT_GATE
Entry reads docs/user-instruction.md and docs/questions-for-author.md. Current
human direction keeps the four research directions and Rust engine, prohibits
other agents, and preserves the sole full acquisition. Step0040 is still in
progress at implementation42659a8; this step does not replace its result review.

### Node: source-context implementation and qualification
Question: how can the next original lean-mlir source measurement preserve its
upstream --tstack=400000 without changing ordinary defaults or cache context?
Native root lakefile.toml declares this at lines4–5; source/SDK stay pinned
b8c4a771/nightly2025-12-01 with correct root package prerequisites.
[Plan](experiment-001/plan.md) declares exact argv, source-byte, identity and
retirement checks. Implement NativeLean::with_args via a private delegating
backend and repeated CLI --lean-arg; keep public struct fields and empty-argv
identity unchanged. Unsupported REPL flag use returns an interface error.

[Result self-review](experiment-001/result-review.md) links both ordinary
validation attempts and final combined RSS. Final39 tests pass; four native
contracts remain explicitly ignored locally but compile, including accepted and
rejected configured-argv proofs added to the existing native CI test.
The source fixture is not Lean. No new native workload ran concurrently.
The active release executable is not rebuilt or replaced. Actual full data,
including incomplete attempts/failures, stay with Step0040 and are not staged
midcollection. Native CI execution remains distinct from compile evidence.

The transient ready-API failure and raw caption defect are retained in the result
review; neither is evidence that the native collection stopped. Final sampled
combined owned RSS16,018,681,856B, no development withdrawal. Concurrency/source
and memory protocol of the full pair did not change.

Decision: dependency complete for declared compiler argv; RQ coverage and major
system contribution remain open. No competitor method, CPU-oracle extension,
new scheduler, altered timeout or paper narrative is introduced.

## WRITE_GATE
Entry rechecks user instructions and author questions. Targeted API/implementation,
evaluation frontier and workload README updates only; document argv and context
limits, clarify that historical scheduling is complete and full resource pair
is active. Prepared Batch300s is an engine default, not upstream authority.
No docs/paper source or frozen RQ/claim/Initial Narrative changes; prior unchanged
paper compile from Step0037 remains applicable. No full writing refinement or
milestone review: final evidence and paper-level RQ answers are absent.

## REVIEW_GATE
Scientific-contract-unchanged audit: engine context support is a supporting
implementation, not novelty, not a performance result, and not a substitute for
Mathlib full-population evidence or actual code-verification profiling.
[Outer self-audit](outer-audit-20261026T012800+0000.md) is performed by this same
thread under the explicit no-delegation instruction. No independent review is
claimed. Meta-review distinguishes protocol testing, native CI, actual workload
and RQ results; repeating unchanged measurements is avoided.

Ranked outstanding objections: (1) fresh/derived full parity and complete
throughput not collected; (2) original simp23/interval48 attribution and reliable
failure certificates unmeasured; (3) original lean-mlir native file/stdin and
SAT/LRAT profile pending; (4) resource-failure isolated retry and multi-node service
evidence pending; (5) novelty versus ordinary resource/scheduling techniques
unresolved. These are not resolved by39 passing tests.

## Routing and persistence
Keep Step0040's sole live full pair, collect terminal outcomes once available,
then original lean-mlir qualification/profile at current48GiB dynamic/4CPU point.
Preserve all raw invalid/failed attempts. Continue source/analysis work that does
not create a competing native group. Daily project maintenance/reflection was
already recorded in Step0038; no duplicate maintenance entity is created.
Publish this completed implementation boundary directly on main; actual hash,
push and CI receipts are observed after commit and reported separately.
