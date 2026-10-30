# Mechanism prior-work audit (self-review, 2026-10-30)

This is a claim map, not a reproduction or an independent review. Installed Lean
is 4.9.0-rc1; current upstream APIs are not silently assumed to exist there.

| Mechanism | Primary evidence | Consequence |
|---|---|---|
| Coq STM | [Barras, Tankink, Tassi](https://www-sop.inria.fr/members/Enrico.Tassi/stm.pdf) | Document dependencies and independent opaque proofs already support asynchronous parallel execution. A DAG and worker pool alone are not contributions. |
| Isabelle PIDE / futures | [Wenzel, PIDE for Coq](https://arxiv.org/abs/1304.6626), [implementation manual](https://isabelle.in.tum.de/doc/implementation.pdf) | Managed asynchronous proof work and document versions are prior art. Tactic-level merging still needs effect and ordering semantics. |
| OR-parallel Prolog | [Santos and Rocha, SLATE 2013](https://drops.dagstuhl.de/entities/document/10.4230/OASIcs.SLATE.2013.9) | Environment copying and alternative-branch parallelism predate this project. Bindings, cuts and search-order effects matter. |
| Thread-level speculation | [Estebanez, Llanos, Gonzalez-Escribano, survey, 2016](https://uvadoc.uva.es/handle/10324/29109?show=full) | Read/write tracking, conflicts, rollback and ordered commit are established techniques. Include their actual costs. |
| Lean.Elab.Parallel | [Official upstream source](https://raw.githubusercontent.com/leanprover/lean4/master/src/Lean/Elab/Parallel.lean) | Ordered/completion-order collection, state snapshots, errors and cancellation already exist. The 2025 module is newer than our pinned SDK. Saved states alone do not establish safe shared-metavariable merging. |
| LeanTree | [Kripner et al., 2025](https://arxiv.org/abs/2507.14722), [author implementation](https://github.com/Kripner/leantree) | Independent-goal factorization and parallel white-box search are closest prior art. Syntax case counts cannot establish independence or novelty. |
| Reflection and vm_compute | [Rocq documentation](https://rocq-prover.org/doc/V8.15.1/refman/proofs/writing-proofs/equality.html), [MirrorShard](https://arxiv.org/abs/1305.6543) | Verified reflection and specialized evaluation are established. Ordinary Lean kernel reduction differs from trusting an external native evaluator. |
| lean-egg | [Author repository](https://github.com/marcusrossel/lean-egg), [POPL 2026 paper](https://goens.org/publications/rossel-popl-26/lean-egg.pdf) | External Rust search followed by Lean proof reconstruction exists already. Current deprecation in favor of grind does not erase the prior contribution. |
| LeanGraphSearch | [Named 2026 preprint](https://arxiv.org/abs/2610.22339), [author page](https://pluslabnlp.github.io/LeanGraphSearch/) | The identified work concerns graph retrieval and prover feedback. Name similarity establishes neither overlap nor novelty for an execution engine. |
| SHRED | [Author package](https://pypi.org/project/shred-lean/0.2.0/), [repository](https://github.com/memo-ozdincer/shred) | Exact prefix and successful closing-step reuse are prior art. Another key must establish dependency sufficiency, failure state, heartbeats and diagnostics, then useful coverage. |

## What current data decide

The retained 200-source census lacks a complete timed metavariable dependency
graph. Average parallelism above or below 1.3 remains unknown. Goal IDs alone
are insufficient: follow metavariables in target and local-declaration types,
local values, assignments and produced goals. Disjoint reachable sets are
necessary but insufficient for effect independence. Name generation,
environment extensions, messages, options, caches and exception backtracking
must also preserve serial behavior. Failed alternatives may consume work
without leaving successful InfoTree nodes.

The digits prototype changes a computational representation while preserving
its mathematical meaning. It is not a general verified computable-fragment
compiler. Even if validated, reflection itself is prior art. End-to-end cost,
proof construction and checking, and original candidate semantics determine
whether there is a new systems result.

The memory matrix rejects unconstrained fixed-pool timing as a compliant
baseline at every modeled budget. It does not prove a shared-parent gain:
observed peaks include parent contributions and no simultaneous COW discount
has been established. Dropping resource-failing jobs changes terminal coverage.

## Updated evidence boundary

- Digits equivalence,count and no-sorry axioms are actually checked by the
  ordinary kernel; the warm declaration recheck is8.5572s. See step003.
  This completes the small certificate prototype,not a general extraction IR.
- Software maps/native-symbol checks distinguish plain Mathlib CLI from the
  prepared backend's dependency-loaded native libraries. See hot-tactics.md.
  Native-qualified small software residence points now exist;see
  software-profile-result.md and genuine-timeout-prefix-result.md. They do
  not provide whole-workload CPU fractions or precompile speedup.
- The400 diagnostic controls show trace.profiler changes7 error flags.
  C profileit callbacks qualify on small controls;the fixed200 comparison
  has completed with observed flag/diagnostic parity and rawHB differences.
  The restored-budget50pass point exposes opportunity hidden by the
  diagnostic budget. Complete merge-safe work/span is not established.
- Memory simulation now retains fit-subset results via exclusive retry,
  instead of presenting dropped hard cases as throughput. Actual warm retries
  change11 resource failures into timeouts at the same aggregate budget.

## Upstream state contract, rechecked2026-10-30

Official Lean.Elab.Parallel source was reopened. CoreM/MetaM/TacticM par
collect snapshots and restore the caller's original state; iterator variants
expose states in input or completion order. parFirst chooses a successful
completed result and can cancel others. These APIs are not a proof that
arbitrary successful goal states can be merged without conflicts,that
parallel failure diagnostics equal serial diagnostics,or that budgets charge
identically. This reinforces the need for an explicit effect/merge contract.
It does not supply novelty to a new task queue.

Primary sources reopened:Coq STM author PDF;LeanTree2507.14722 authors/title/
independent-state factorization;LeanGraphSearch2610.22339 retrieval graph
and feedback-loop scope;lean-egg author repository. No competitor reproduced.
The GraphSearch name denotes lemma retrieval here,not a measured execution DAG.
