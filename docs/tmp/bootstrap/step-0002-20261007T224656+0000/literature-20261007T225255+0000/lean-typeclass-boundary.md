# Exact Lean4.9 typeclass inference and cache boundary

Finite source-only E9 node, BOOTSTRAP step0002, 2026-10-08 UTC. First directly reread user instruction, complete idea story/current evaluation and full research-literature-novelty skill. Read the complete SynthInstance module in focused consecutive ranges, and directly called cache/state/instance/reduction/defeq/instantiation/check interfaces. Exact release source pin `be6c4894e0a6c542d56a6f4bb1238087267d21a0` (`v4.9.0-rc1`); retained individual primary bytes and provenance below. No native call, build, GPU action, Git, paper/canonical edit, new empirical experiment or chosen hypothesis. The parent-supplied profile observation is a motivation, not a numerical result independently audited here.

## Verdict

**The category encloses context-sensitive elaborator instance synthesis, including native cache lookup and validation, tabled search, type inference, reduction, unification/assignments and result checking. It is not a kernel fraction.** Stock synthesis already caches successful and failed queries in Meta.State and tables shared subgoals within each search. Native saved Meta states can retain those caches. Fresh command-level Meta invocations normally start empty; retaining an import-only command environment does not retain every previous theorem's Meta query cache.

Category elapsed time and source/expression bytes are insufficient to choose safe cross-candidate reuse or a GPU operation. They do not reveal hit/miss rates, reset losses, repeated keys under compatible environments/local contexts, dynamic subproblem dependencies, operation width, transfer cost, or whether long work is indexing/search versus reduction/unification. Explicit native cache semantics and resets are part of the competitor, not an optimization to discard by intuition.

## Category work: exact call boundary

`Lean/Meta/SynthInstance.lean:708–779`, complete `synthInstance?`, is wrapped by `profileitM Exception "typeclass inference"`, with individual declaration label taken from the **input type's application head constant**. That label is not necessarily the enclosing theorem. The wrapper includes:

- Option lookup (`synthInstance.maxSize` or explicit max-result-size), trace setup and instance-specific Meta configuration: transparency `.instances`, stuck exceptions enabled, first-order/context approximation enabled, constant/universe approximation disabled, and `inTypeClassResolution=true`.
- Reading local instances, recursively substituting assigned metavariables, preprocessing via reducing forall telescope/WHNF, then constructing/looking up the persistent synthesis-cache key.
- On hit: tracing the cached answer; for success, infer its type and unify with the requested type using default transparency and assignable synthetic opaque parameters (`assignOutParams`). A hit can still do inference/defeq/assignment work. `none` is a cached failure; exception/stuck behavior is separately handled.
- On miss: enter a new metavariable depth with allowed level assignments, replace out-parameters by fresh metavariables, and run tabled resolution; reopen abstract metavariable result, check/unify output parameters, instantiate the answer and `Meta.check result` to propagate universe constraints lost across the temporary depth, then cache success/failure.

`trySynthInstance` at783–786 catches stuck exceptions as `LOption.undef`; `synthInstance` at791–800 turns missing/stuck answers into synthesis failure. `synthPendingImp` at803–829 can call synthesis recursively while assigning pending metavariables, under the `synthPendingDepth` guard. Successful synthesis may change metavariable assignments; an expression answer is not the whole state effect of the operation.

Existing profiler semantics apply: same-thread-exclusive elapsed scope time, accumulated by category, not CPU work; nested instrumented calls are excluded from their same-thread parent and counted separately in the category accumulator. Therefore recursive synthesis is not interpreted as repeated inclusive runtime; typeclass scopes can still include uninstrumented Meta work and wait/descheduling. This node does not infer total calls, cache effectiveness or kernel costs from the measured category.

## Search is native tabled resolution, not independent lookups

Complete `SynthInstance.main:635–649` allocates a fresh root mvar/key and runs `SynthM` with **new empty search state**. `State:194–198` holds generator stack, resume stack, table entries and result. Per-problem heartbeat default is20000 thousands of small allocations (`18–21`,36–37); max instance-result size128 (`23–26`), with configurable morally-canonical-instance pruning (`28–32`,575–598). Actual work depends on these options/limits and interrupt checking at203–205/614–625.

`getInstances:219–252` reads local instances before extending the telescope; it queries the environment's global discrimination tree by unification, stably sorts priority, filters erased instances, makes fresh universe metavariables and appends applicable local-instance fvars with synthesis order. This is both environment and local-context dependent. `tryResolve:358–377` builds argument metavariables/subgoals, reducing telescopes as needed, unifies instance result type against goal and unifies/assigns the resulting instance term. `tryAnswer:382–389` reopens an abstract answer in a consumer's metavar context and unifies it.

`MkTableKey:99–166` structurally normalizes assignable expression/level metavariables into `_tc` auxiliary variables/level params according to current depth; it is not arbitrary definitional equivalence or context-independent canonicalization. The source explicitly says definitionally equal but structurally different goals can still be revisited. `consume:499–551` shares table answers/waiters, removes assigned subgoals and can remove unused arguments; `addAnswer:425–439` deduplicates answers structurally and wakes waiters. Generator/consumer scheduling and assignment dependencies are sequential state transitions. Source membership in a search tree does not prove parallel independent tasks suitable for a device.

## Cache ownership, exact keys and lifetimes

| Native structure | Key/value and dependency boundary | Lifetime/reuse fact |
|---|---|---|
|Global instance index|`Meta/Instances.lean:93–97` scoped environment extension;214–218 returns discrimination tree and erased set. Priorities, attribute visibility and synthesis order matter.|Environment/import/prepared-root reuse retains indexed global instances. It is not the per-query solution cache.|
|Synthesis result cache|`Meta/Basic.lean:215–225`: key `{localInsts, type, synthPendingDepth}`, `PersistentHashMap` to `Option Expr`; `SynthInstance708–779` instantiates/preprocesses type before lookup.|`Meta.State.cache.synthInstance`; success and failure reuse across calls in retained Meta state. Keys are native structural expressions/local IDs, not printed bytes or alpha-renamed source. Environment/options are not explicit fields in this key; correct native lifetime is therefore essential.|
|Search table|`SynthInstance194–198` normalized goal → answers/waiters plus stacks.|Fresh per top-level cache miss/main search (`645` run' `{}`); shares subgoals inside that search, not a persisted global cross-candidate table.|
|Type inference|`Basic227,246–248`, `InferType168–194`: expression→type.|Meta cache; selected expression kinds cached only when both expression and inferred type have no metavariables. Direct fvar/mvar inference uses current contexts.|
|WHNF|`Basic229,249–250`, complete `WHNF921–968`.|Only terms without fvars/expr-mvars, no custom canUnfold hook, and transparency `.default`/`.all` use these caches. Synthesis primarily uses `.instances`, which does not directly use these two caches, although helpers switch transparency.|
|Definitional equality|`Basic235–252`, `ExprDefEq1936–1990`: expression-pair cache partitioned by transparency and transient/permanent kind.|Aggressively reused **inside** a valid equality invocation; resets sharply limit persistence, as below.|
|Instantiation traversal cache|`MetavarContext547–621` structural traversal reads assignments and can compress assignments.|Fresh `MonadCacheT` run in `instantiateMVarsCore`; `instantiateMVars642–649` writes resulting mctx. Not a persistent answer independent of mctx.|

Native `MetaM.run`/`toIO` defaults to empty Meta.State (`Basic434–442`). Ordinary `Command.liftTermElabM:531–544` invokes `x.run mkMetaContext {}` and discards returned Meta state after carrying Core state through command elaboration. `runTermElabM568–588` uses that helper and elaborates scoped binders. Thus multiple theorem/command calls are not automatically a process-global cache, even in a warm REPL command environment. Repeated compatible queries inside the same Meta invocation are already reused.

`Basic306–309,412–428` saves the complete Meta.State (including cache) with Core state. `withRestoreOrSaveFull` explicitly restores full saved Meta state. Ordinary `SavedState.restore` only restores mctx/zeta-delta/postponed fields, leaving cache/diagnostics in current state. This distinction matters: native backtracking is already designed to retain useful caches under controlled contexts; it is not equivalent to full state resetting after every tactic. Existing proof-state snapshots that retain Meta.State can retain its caches; branching from a saved root inherits only queries done before that root, not later sibling cache additions. Old InfoTree-reconstructed roots cannot be assumed to contain all original Meta caches.

## Invalidation and correctness restrictions

`Meta.Basic:405–407` implements environment modification by clearing both Core and Meta caches. Retain this boundary when instances/declarations/attributes change; a synthesis cache entry is not valid merely because the query prints the same. Local-instance changes are represented in the explicit key. `withLCtx1533–1534` itself uses a reader replacement and does not flush the cache in its actual implementation; the adjacent old `MVarId.withContext` docstring claiming a flush must not override that implementation fact. Different local-instance arrays select different keys; fvar types/assignments and local context still matter.

`withNewMCtxDepth1496–1502` restores original mctx/postponed state in `finally` but does not globally clear caches. `savingCache975–982` explicitly saves/restores cache around scoped work. `withConfig929–930` changes context, not all caches by itself. This is **not** a guarantee that arbitrary external option/local-context changes are safe with a copied cache; the native control-flow assumptions remain part of its correctness boundary.

Most decisively, full `checkpointDefEq1816–1845` clears transient defeq cache at1829 because different calls can have different configuration and metavariable contexts. Full `isExprDefEq1854–1876` also clears the permanent cache at1875; its source explains that expression-level absence of mvars can be insufficient when local variable types contain mutable constraints or are changed. Do not propose removing this reset merely because its field is called permanent. `ExprDefEq1939–1943` selects transient kind for mvars/custom unfolding, cache retrieval partitions transparency; transient insertion at1984–1990 first instantiates assignments so backtracking does not leave invalid keys. Caching occurs only if no additional postponed constraints arise (`2064–2067`).

The synthesis-result key lacks explicit maxSize/heartbeat/option/environment fields. Native state/lifetime and caller conventions carry those assumptions. It is not a sufficient universal cross-worker cache key, and a missing result under a budget is not automatically a timeless semantic impossibility. Even a closed class query can change chosen native answer with instance visibility/priority/environment/options; local answers carry fvars/metavars and need mapping/state effects. Preserving logical validity is weaker than preserving native result/diagnostic/resource behavior.

## What this permits parent to conclude

Stock caches already cover exact compatible closed **and local** synthesis queries within retained Meta execution and tabled subgoals during a search. They do not guarantee that expensive repeated work between fresh theorem Meta invocations or independent candidates is already captured, nor that such repeats exist. Current source facts support investigating that distinction, not implementing an unsafe broader cache. Bare tabled resolution, result caching, closed-term caching or state inheritance is prior/native mechanism, not a new contribution.

The parent profile's substantial category is a useful place to look for costly elaborator work. A causal follow-up, if separately admitted, would need exact native query/context identities, success/failure/stuck/budget behavior, native cache hit/miss/reset causes and cost-weighted recurrence across real candidates; operation-level call cost/dependency evidence would be needed to distinguish indexing, search scheduling, defeq/reduction, instantiation and result checking. GPU consideration additionally needs independent ready-work width, complete representation/transfer/check/fallback costs and strongest CPU/native-cache comparator. These are unresolved evidence needs, not a new experiment executed here or an adopted hypothesis. Category cost plus bytes cannot supply them.

## Primary provenance and closure

All retained files are copied byte-for-byte from the previously pinned official Lean4.9.0-rc1 distributed source, under `/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux/src/lean/`; exact release archive provenance SHA-256 `b4a3898970dd9980f1a59fb399d3ed447c9c622f7c69639eb6ca9435d55fa6f8`. Corresponding official source URL is `https://raw.githubusercontent.com/leanprover/lean4/be6c4894e0a6c542d56a6f4bb1238087267d21a0/src/<path>`; underscore local names encode `/`. No missing primary file needed fetching for this node. Profiler native semantics are source-pinned in sibling `lean-profiler-boundary.md`. Finite source boundary complete; no canonical/novelty/target change. Root owns disposition.

| Source path / retained bytes | SHA-256 |
|---|---|
| [Lean/Meta/SynthInstance.lean](lean-typeclass-source/Lean_Meta_SynthInstance.lean) | 6b98cf421ecaac62e1dcd3ae7f5f6d44ccd65917222281372883f4d41fd0d8b3 |
| [Lean/Meta/Basic.lean](lean-typeclass-source/Lean_Meta_Basic.lean) | 2b2a866a2f972f8f9025d3d811a73c48feb2f6ae0cef45f95dc957c28186339e |
| [Lean/Meta/Instances.lean](lean-typeclass-source/Lean_Meta_Instances.lean) | c5370657436ce5a89fe1b1a011c802fdc70dab5fbcb1552c3c330b178d9f0cb4 |
| [Lean/Meta/WHNF.lean](lean-typeclass-source/Lean_Meta_WHNF.lean) | 062692cd4cbfa424ca61b34950ba5e8e4319a17b3e1c2c080012aa660d6cbf71 |
| [Lean/Meta/ExprDefEq.lean](lean-typeclass-source/Lean_Meta_ExprDefEq.lean) | 06bdfe2fcf608868db3795b8aa810630dbcc54ecc53b86b37a8d3981b21e05b4 |
| [Lean/Meta/Check.lean](lean-typeclass-source/Lean_Meta_Check.lean) | e258f8ea30fb2dff06398c29c1feca781c6d0a3aafc472e8da3a9cd5442c1c7a |
| [Lean/Meta/InferType.lean](lean-typeclass-source/Lean_Meta_InferType.lean) | e0d4b33477f573120bfd8bd57b03bf98b1ece70bba28366a99aa00ff88b46696 |
| [Lean/MetavarContext.lean](lean-typeclass-source/Lean_MetavarContext.lean) | a6477c0b34018693d91a4e8ede9292b6888fdf8d382840dc6056d57be31bc2a8 |
| [Lean/Elab/Command.lean](lean-typeclass-source/Lean_Elab_Command.lean) | 3168b55f4763b56bb80ccc2d6c33272277abc8f1752768f2a9ea4cb8a81d836d |
| [Lean/Util/Profile.lean](lean-typeclass-source/Lean_Util_Profile.lean) | e49b40c437dbae29d004fbbf2256dc3e982c4503db2d30c59f8cdfd80aa2c6a6 |
