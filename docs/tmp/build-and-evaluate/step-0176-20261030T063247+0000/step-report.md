# Step 0176 — integrate W's static corpus with a version-aligned native baseline

BUILD_AND_EVALUATE. This report and its outer audit are same-thread self-review.
Input is the completed W artifact at daffefc, pinned to openai/math revision
4eaee87548250b2682affda7d05d947c05554bae. Root edits only paper, evaluation, and
this step's reports. No W, M, or O implementation is modified.

## EXPERIMENT_GATE — completed derived-table check

The retained script independently aggregates W's frozen file and import CSVs
and reconstructs the graph with integer-indexed Kahn traversal. It does not
rerun W's source parser and is not a second full source audit. It confirms:

- 163,097 distinct Lean source files and 1,785,499,363 bytes;
- 1,354,379 lexical decide +kernel forms in 5,848 files;
- 370,864 internal import edges, all modules topologically ordered, a longest
  unit-weight chain of 451 modules, and a largest same-depth layer of 9,225;
- 130,834 OAI-root reachable modules, with 1,397,800,941 source bytes;
- the largest 2,610 files contain 40.1098588% of source bytes.

The check takes 2.361 s and peaks at 140,664 KiB. It launches zero native
verification processes. Token occurrences, source-byte skew, unit graph depth,
and layer width are not executed calls, runtime-tail shares, a timed critical
path, or safe parallelism. The tables establish no native acceptance, timing,
transitive axiom closure, or cache-hit rate.

Official pinned publisher README/toolchain/Lake sources and exact Lean 4.34.1
Decide/AuxLemma implementations were read. The publisher distinguishes research
artifacts with different verification status and one large library. The actual
decision frontend routes kernel mode through mkAuxLemma. AuxLemma's default
cache checks type, privacy/defeq flags, and universe parameters in the local
environment branch before adding a declaration. Its lookup table is not
serialized in .olean. This is existing native reuse, not a measured hit rate or
cross-request service cache. Literal tactic names also miss decide +native and
imported axiom dependencies. A new mechanism must separate cache hits from
additional removable work rather than count every lexical occurrence as a new
expensive kernel reduction.

## WRITE_GATE — completed evidence integration

Evaluation adds the corpus's static quantities and explicit coverage limits.
Related work adds the version-aligned native cache baseline with primary-source
citations. The evidence index records the independent calculation and its
limits. All text before Evaluation and the four RQ descriptions are unchanged;
no cross-proof-reuse thesis, method adoption, or novelty claim preempts W/M
results or the user's decision.

Tectonic 0.17.0 finishes with exit 0 and a PDF on the existing PVC. Root uses
CPUs 0–1; sampled own-tree peak is 198,283,264 bytes, below its 4 GiB share.
The 3.27 s build is a development check, not a verification benchmark.
The complete log retains underfull-box warnings; no undefined citations,
unresolved references, or overfull boxes are observed. No visual-layout
perfection or conference acceptance is claimed.

## REVIEW_GATE — self-review completed

Numeric totals and graph invariants match the frozen W tables; the primary
source links match the corpus's Lean version. Native caching is distinguished
from lexical repetition, source coverage from proof acceptance, and internal
consistency from an independent source scan. No native experiment, new agent,
placement/security/CronJob change, or other-writer edit is introduced.
The root does not repeat the migration signal test or claim its denial has
changed. Current four-lane resource allocations remain untouched.

Before push, attempt pull --rebase. Preserve shared dirty work without stash.
If it refuses because another lane has uncommitted work, fetch origin/main
and permit a normal push only when origin/main is an ancestor of HEAD; no
rewrite is then necessary. The actual outcome is retained on the PVC in
step0176-git-persistence.json. No reset, amend, force push, or other-author
staging is permitted.
