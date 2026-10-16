# Prepared-context contribution: source and cohort admission review

Observed 2026-10-16. Root performs a finite claim-oriented source/admission
review after the user rejects ordinary CPU compilation as the contribution
and requests a useful opportunity bound before another narrow GPU backend.
This is selection evidence, not a new positive performance experiment.

## Declared claims and coverage

1. Sharing expensive imports across requests is a new service contribution.
2. Managing several prepared contexts or branching proof state supplies a
   new verification-specific mechanism beyond established services/snapshots.
3. A complete, equal-resource verification service can improve the joint
   behavior/latency/throughput/memory frontier.

Coverage includes the same problem (Lean services), mechanism (warm headers,
native proof state, process snapshots), evaluation boundary (computation versus
whole service), setting (multiple environments/projects and real candidate
attempts), and adjacent accepted systems evidence. The root reads current human
instructions, the full Initial Narrative and four RQs, current paper
contributions, evaluation and the existing closest-work map. No RQ is replaced.

Searches used:
- Lean verification server shared contexts memory cache scheduling Kimina snapshot Axle
- Lean proof state snapshot parallel tactic cache Keep the Proof State Live 2605.25556
- serverless prewarmed snapshot memory working set scheduling SOCK SEUSS Spice OSDI

Search/open records are from 2026-10-16. Official papers, author repositories,
source files and USENIX proceedings were verified; secondary tutorial/search
results are excluded as novelty evidence. Existing work is not rerun simply
to reproduce a published speedup. No new naming repairs overlap.

## Primary-source findings

### Kimina: exact header reuse and ordinary replacement are established

[Official repository](https://github.com/project-numina/kimina-lean-server),
[manager source](https://raw.githubusercontent.com/project-numina/kimina-lean-server/main/server/manager.py)
and [technical report](https://arxiv.org/abs/2504.21230) establish parallel REPL
pooling and import reuse. Current manager source searches free workers for a
matching header and otherwise removes the oldest available worker when the
pool is full. Initialization and worker retirement also exist. Thus generic
multi-header caching, a warm pool or age-based replacement cannot be claimed
as new. Current upstream settings are not substituted for the producer-pinned
capture defaults. The actual measured Python server is the existing private
header-repair copy, identified by its recorded command.

### Snapshot-DSP: deeper elaboration reuse and parallel branches are established

[Primary paper](https://arxiv.org/html/2605.25556v1), sections3–4, captures native
proof states and dispatches tactic arrays through Lean tasks. It shares the
declaration environment while separating metavariable contexts. Its evaluated
boundary includes a tactic-search phase and a small number of complete DSP
runs, with a per-branch build fallback. This supports deeper reuse as a real
mechanism, but does not supply our unchanged-source whole-service comparison.
Moving from import reuse to theorem-body state alone does not create novelty.
The current released artifact status/toolchain must be qualified before a
matched numerical reproduction.

### AXLE: isolation and multiple environments are established

[Primary paper](https://arxiv.org/html/2606.26442v1), sections3,5,7 and appendixA,
already describes preloaded execution, request processes and concurrent Lean/
Mathlib environments. Its comparison normalizes imports, drops external-import
candidates and measures executor computation, excluding broader service logic.
The paper states limitations for arbitrary project dependencies and persistent
proof-search sessions. Those limits identify possible expansion questions,
not an absence of isolated serving or automatic evidence of our superiority.
A private-backend accounting mismatch cannot be turned into a numerical win.

### Adjacent snapshots: generic process restoration is insufficient

[Spice's official OSDI26 source](https://www.usenix.org/conference/osdi26/presentation/holmes)
attributes its system contribution to memory/storage and restore co-design.
Ordinary COW or snapshot restoration alone remains established. A
verification-specific mechanism needs its own discriminating evidence.

## Actual retained workload evidence

The executable offline analysis reuses the actual service's split_snippet
implementation; it introduces no project-authored header parser or native
run. [Commands](analysis-commands.json), [source-location qualifications and
reader failures](splitter-provenance.json), code and outputs remain in this
directory.

| Original cohort | All retained attempts | Actual header-key distribution |
|---|---:|---|
| GoedelWorkbook4.27 | 29,750 | 29,750 use import Mathlib plus import Aesop |
| miniF2F4.9 | 7,808 | 7,790 use that header;18 have an empty parsed import header |

An empty import header is not a different project or proof of zero import
expense inside the body. No source is removed. Current-source inspection and
frozen capture commands are distinguished from proof of immutable source at
capture time. The private server copy has no .git; this node does not fabricate
a freshly verified source revision.

The original complete E033 Goedel server archive supplies source-associated
native lifecycle events, independently of current header parsing:
-29,690 unique source IDs have a started-REPL reuse event.
-60 unique source IDs have a header-command event.
-No duplicate IDs within either category, no overlap, no extra IDs and no
 uncovered input IDs; the partition covers all29,750 original source IDs.

[Exact outputs](goedel-context-scope.json) retain the source-ID partition.
The reuse event fraction is99.798319%, **not a CPU saving, hit-time estimate,
critical-path share or end-to-end upper bound**. These events establish that
the warm-header mechanism already engages; costs of the60 preparation events
and their overlap with useful work are not measured by this count.

The first reader guessed the native REPL directory as the Python server root.
Frozen command metadata resolved the actual shared server cwd. A subsequent
git-revision lookup failed because it is a copied source tree. Both are
offline provenance-reader failures; inputs, native runs and source were not
changed or rerun. Successful analyses and limitations are retained.

## Admission and baseline handoff

Claims1–2 have high same-mechanism risk and do not justify a new implementation
or another tuning matrix. The present cohorts cannot establish a benefit from
multiple expensive competing import contexts: the Goedel cohort has exactly
one actual header key, and the mini cohort supplies one imported root plus an
empty-header minority. A working-set or eviction experiment manufactured by
renaming the same header would not test the intended contribution.

Claim3 remains the ambitious target, unproved. Its baseline families stay:
competent warm/cache serving, native logical/serialized state reuse, and the
strongest compatible complete CPU execution. The original native process is a
behavior/cold control, not the only performance competitor. GPU common-algorithm
CPU execution and component removals are controls, not additional main baselines.

The strongest next experiment must discriminate a real proposed mechanism from
these alternatives. For context placement, first require actual project/context
traffic with expensive distinct preparation and measure its complete costs.
For deeper state sharing, distinguish a full source/declaration outcome from
tactic-only success and compare to native snapshots. For GPU work, establish
useful independent cost/readiness after the competent CPU path before a backend.
Existing aggregate CPU and header counts do not fill any of these missing costs.

A positive result would have to change a complete equal-resource frontier with
a causal mechanism removal. A null/negative result preserves existing reuse
as the sufficient answer for that regime and closes that constructor rather
than expanding a weak grid. If actual data provide no competing working set,
do not run an eviction benchmark or describe that setting as already measured.
Ordinary compilation or a renamed pool is not the fallback contribution.

## Scope and return

This node adds an actual cohort/event qualification that rejects generic
multi-context import caching as a supported new headline on the current data.
It does not answer RQ1 from byte locality, close another RQ, prove a new system,
claim a matched AXLE result, alter the Initial Narrative, or substitute a
smaller measurement paper for the user's system goal.

No new native benchmark, GPU job, profiler, helper service, memory cap, checkout
or scheduler is started. Healthy acquisitions are left intact without row-count
polling. The root updates only its narrative frontier and this unique report.
The OMP literature/paper owner retains canonical file ownership and should
absorb this source/baseline handoff before scientific disposition or writing.
Fresh independent review remains outstanding; root review is not independent.
