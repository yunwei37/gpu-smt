# OpenAI math: source coverage and native stratified measurements

Pinned repository: [openai/math](https://github.com/openai/math/tree/4eaee87548250b2682affda7d05d947c05554bae),
commit4eaee87548250b2682affda7d05d947c05554bae (2026-10-30T00:35:35Z).
Lean4.34.1; Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612.
The root and lean licenses are Apache-2.0; third-party dependencies retain their
licenses. Every manifest dependency revision is in static-4eaee875/dependencies.csv.

## Latest archived native evidence

Lean4.34.1 and pinned Mathlib cache are prepared on the same PVC. The W027
snapshot has536distinct compiled module artifacts across explicitly separate
budget/observation points, not full library acceptance.

| Evidence | Scope |
|---|---|
| [Whole Amplitudes](amplitudes-native-complete/) |180.276s,100kHB/j8 replay point|
| [Whole Grid](grid-native-complete/) |634.280s,its100kHB/j8 replay point|
| [Unchanged-source target costs](authored-sample42/) |19/42probability endpoints;6/21complete cells at W027|
| [Retained-type census](native-type-keys-363/) |363objects,42,610global Expr types; not population count|
| [Source/helper unit audit](native-type-attribution/) |multi-goal expansion breaks site/check equivalence|
| [Artifact controls](artifact-scope-control/) |3targets emit .olean/.ilean/.c; separate cost point|
| [Build-cost estimator](native-build-cost/) |full CPU-hours/95%CI still unavailable|

The42probability targets span21source-size/import-depth/kernel-token strata.
Purposeful targets and compiled dependencies get no extra population weight.
The finite group continues23remaining targets; [W state](../W-status.md)
records launch ownership. Source options remain unchanged, with child self
timers despite denied parent signals. W16GiB includes separately censored
old EPFL process13733; sampled RSS is not a hard kernel quota.

Current uniform costs emit .olean only. Missing/censored/budget-exceeded
targets are not zero. Complete-stratum HT/variance calculation is implemented;
incomplete cells do not produce an invented full interval. Standard Lake
artifacts/setup and external-package work remain separate. Earlier static
work/span scenarios are assumptions, not calibrated forecasts. No clocks or
costs are pooled across HB/SDK/thread/profiling/artifact configurations.

## Complete source coverage

163,097 .lean files /1,785,499,363bytes are enumerated and content-scanned.
The recursive Git tree was truncated; partial entries were discarded and
discipline subtrees enumerated completely. The old53,554/474MB observation was
a lower bound, not corpus size. Files are source blobs, not accepted proofs.

| Source group | Files | Source bytes |
|---|---:|---:|
| OAI/Combinatorics/Ramsey |444|222,614,562|
| OAI/Analysis/MutuallyUnbiased |3,386|205,200,466|
| OAI/Analysis/PlanarPacking |562|141,680,548|
| OAI/MathematicalPhysics/Transonic |466|83,494,755|
| OAI/Algorithms/SubexponentialSAT |3,977|35,509,858|

The inventory has744 source-directory groups, not744 independent Lake projects.
The publisher supplies one large library. Median file size is4,400bytes;
p99 is80,781bytes. The largest1.6%of files (2,610files) account for40.11%of
source bytes. This is a size statistic and says nothing about73%of runtime.

## Computation and tactic identifiers

Counts exclude nested comments and string literals; they are lexical
occurrences, not executed calls or checked theorem counts.

| Identifier/form | Occurrences | Files |
|---|---:|---:|
| decide (including +kernel) |1,686,012|16,766|
| decide +kernel |1,354,379|5,848|
| native_decide |0|0|
| bv_decide |0|0|
| direct ofReduceBool |0|0|
| simp |675,366|96,034|
| rfl |520,550|80,335|
| norm_num |183,572|35,471|
| omega |169,870|31,343|
| grind |650|128|

The number of theorems with transitive ofReduceBool axiom dependence is
**unknown**: zero direct tokens does not prove zero dependency through imports,
macros or generated proof terms. It requires version-matched compiled
#print axioms or equivalent native dependency inspection. The static stage did not build;
the later native subset has not established full axiom closure.

This release exposes much more source-level kernel-evaluation work than the
old arithmetic-proof corpus. Whether it dominates native time remains to be
measured; identifier density is not a speedup opportunity in seconds.

## Import graph and reuse exposure

The graph resolves the pinned Lake srcDir override for HodgeConjecture.
All163,097 modules are topologically ordered;370,864internal import edges.
The longest unit-weight chain has451modules. The largest same-depth layer has
9,225modules; this is structural width, not safe CPU/RSS concurrency.
The OAI root reaches130,834modules /1,397,800,941source bytes.
External dependency sources/timings are excluded. The initial path-only graph
is preserved in summary.json as a superseded calculation.

25,264cross-group fingerprints cover78,473 lemma/theorem source occurrences.
These compare exact comment-masked declaration bytes using lexical boundaries.
They are candidates for inspection, not elaborated theorem equality, duplicate
kernel work, matching dependencies or safe cross-context proof reuse.
Namespace/options/attributes and dependency obligations are not certified.

## Files and reproduction

- inventory.py enumerates complete Git trees and metadata for an immutable pin.
- scan.py streams the public archive without extracting the1.785GBsource tree.
- static-4eaee875/files.csv.gz and projects.csv contain paths, sizes and groups.
- static-4eaee875/content/ contains compressed per-file metrics/import edges,
  small project/tactic/size summaries, critical path, duplicate candidates,
  complete receipt and the interrupted first-attempt log.
- [Representativeness and native sampling](../../docs/workloads-audit.md).

Use inventory.py --pin with the full revision and --out for metadata, then
scan.py --inventory with that metadata directory and --out for content metrics.
Only small derived tables are committed. Complete source journals remain on
the existing PVC; no upstream candidates are generated or rewritten.

## Execution and limitations

The first G10 attempt was interrupted by Workspace replacement after52,000
logged files, without a completed metric artifact. Its raw progress is retained.
The same Workspace/PVC later appeared on phobos-vt; W made no placement,
credential, security or quota change. A distinct static-only second attempt
completed in697.87analysis seconds with2,140,936KiB process peak RSS; these
are parser costs, not Lean verification times, and clocks are not combined.
The second attempt checkpoints1,000-file compressed journals.

The original static stage stayed below its W5GiB allocation and ran no Lean
or inference. Later partial native work uses W16GiB/8cores, a separate point.
No full project build has completed.
The only observed public workflow is lock-prs.yml; no public build CI was found
at the pin. Whole-project acceptance/axiom closure and the population1.6%/73%runtime
hypothesis remain unknown; native costs exist for the stated subset.
Review is same-chat self-review, not an independent audit.
