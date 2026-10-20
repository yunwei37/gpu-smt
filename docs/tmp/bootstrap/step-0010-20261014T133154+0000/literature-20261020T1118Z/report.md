# Existing in-process concurrency: bounded source admission, root self-review

Observed2026-10-20UTC. This is an implementation-opportunity check within the
open RQ1/RQ3/RQ4 experiment, not another performance experiment or a new
scientific contract. The original user instruction log and complete Initial
Narrative/current evolution were consulted; no author prompt or narrative is
edited. All execution and review remain in this thread.

## Question, coverage and decision rule

Would implementing independent candidate tasks inside one Lean process,
sharing its imported environment, provide an absent system mechanism or a
stronger unmeasured baseline? Would that alone justify a new GPU batch route?
Check the actual retained native REPL, the currently used HTTP service, the
version-matched official Lean parallel API, and the closest published snapshot
work. Stop after their execution and state boundaries can be distinguished.
Do not start another capture, revive E038 or claim performance from source.

The plain candidate claim is parallel checking of independent candidates over
one prepared environment with separate task-local state. It is **not an absent
primitive**. Reject implementing it again as a new contribution. No new
native/GPU implementation or full matrix is admitted by this check.

## Actual local execution interfaces

The [published native REPL snapshot](../../../../../artifacts/lean-modern-native-compilation-2026-10-14/source-snapshot-20261015/native-repl/REPL/Main.lean)
contains batchVerifyParrallelNaive at330, batchVerifyParrallel at345 and
runBatchVerify at367. The first schedules native IO tasks over a common initial
Command.State; the bucketed path schedules sequential lanes over the same state.
The entry resolves the saved environment once before selecting the path.
The spelling parrallel is the actual existing protocol value.

The currently executed recovery-tree REPL has the same runBatchVerify section
byte-for-byte as that published snapshot. This compares that section only:
it does not claim whole-source/binary equality or concurrency measurements.
Its candidate timing wrapper elsewhere is local instrumentation.

The [existing native-batch driver](../../../../../bench/lean-native/run-native-batch-comparison.py)
already submits the naive BatchCommand with env0 and original candidate arrays
(lines271–275). The [arithmetic driver](../../../../../bench/lean-native/linarith-oracle/run-comparison.py)
already adapts the upstream sequential-bucket interface. Earlier complete
arithmetic comparisons therefore cannot be described as exclusively one
process per proof. These historical drivers retain their historical resource
points; this source check does not authorize running an old unlimited/48GiB-
per-worker collector under today's aggregate budget.

In contrast, the pinned official
[Kimina HTTP check route](https://github.com/project-numina/kimina-lean-server/blob/fb2393de/server/routers/check.py)
runs a per-snippet operation, borrows a REPL, prepares it, sends a body and
releases the REPL; the request gathers these operations.
The [manager](https://github.com/project-numina/kimina-lean-server/blob/fb2393de/server/manager.py)
tracks busy/free workers. An HTTP request containing multiple snippets is
therefore not, by that fact alone, the native shared-state BatchCommand path.
Our declared resource/lifecycle repairs are separate from upstream source.
This is an interface distinction, not a measured opportunity or proof that
either implementation is globally faster.

## Primary external evidence and coverage review

Queries used on2026-10-20:
- Lean REPL parallel commands same process CoreM Task environment Kimina Pantograph
- Lean Snapshot DSP asynchronous parallel tactics shared environment
- AXLE Lean verification server multi threaded parallel process environment
- Keep the Proof State Live arxiv

The version-matched
[Lean4.27 parallel implementation](https://github.com/leanprover/lean4/blob/v4.27.0/src/Lean/Elab/Parallel.lean)
already provides CoreM/MetaM parallel jobs, saved-state results, original-order
and completion-order collection, and cancellation hooks. The installed4.27
SDK contains that source. This supports using upstream machinery rather than
inventing another task/state abstraction. It does not prove safe lifetime
isolation for arbitrary IO extensions, independent memory reclamation or
end-to-end benefit.

[Snapshot-DSP's primary paper](https://arxiv.org/abs/2605.25556)
already studies elaborated proof-state reuse across parallel tactic branches.
Its published benchmark setting differs from finished whole-file candidate
streams. Neither that difference nor adding an LP queue establishes novelty.
No reported paper speedup is imported into our denominator.
Pantograph's official protocol and AXLE's official documentation were search
leads, not evidence of their uninspected internal scheduling.
Two guessed public REPL raw URLs returned404 and were excluded; the actual
published local source supplies the REPL evidence instead.

Same-mechanism and same-claim risk is high for the bare shared-environment/task
claim. A larger surviving claim would require a consequential end-to-end
heterogeneous service advantage beyond those native alternatives, including
real device-ready supply, equal resources, certificate work and retirement.
That remains an unresolved requirement, not an accepted replacement thesis.

## Existing service result and next action

The [E023 complete ProofNet review](../../step-0007-20261010T000125+0000/experiment-023/result-review-proofnet.md)
already covers30cells/178560outcomes and rejects unconditional superiority of
the tested disposable-lifetime policy. The actual experiment023 directory has
full1-proofnet and its review; no full-minif2f block is present. Do not report
an uncollected completed60-cell result or silently restart the old resource
protocol. This check adds no new latency result and does not redo that review.

The current sole29750collector remains PID23039/birth1792486754.32,
confirmed live11:17:53Z with a0.305s-old watchdog record and no full terminal.
Its existing six-cell protocol and resource point stay unchanged.
The actual terminal/paired population remains the next empirical dependency.
New mechanisms need an identified substantial cost absent from strong
competitors and a beneficial matched real preflight; merely wrapping existing
parallelism is not sufficient.

## Root disposition and limits

This check rejects a redundant implementation before code/acquisition.
It does not advance an RQ to answered, establish new system novelty, provide
an Amdahl bound, close GPU or claim an independent review. The current
manuscript already names native in-process batch as a competitor, so no new
paper number, narrative rewrite or compile is warranted.
The author's dirty background-related-work.md remains untouched; this
detailed source node is linked from the clean current evaluation authority.
The repeated orientation/search cost is not counted as performance research
progress. Do not rerun this unchanged source question on later goal turns.
