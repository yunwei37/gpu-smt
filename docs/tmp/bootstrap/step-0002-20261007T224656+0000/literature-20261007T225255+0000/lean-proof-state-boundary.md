# Exact Lean4.9 proof-state boundary

Finite read-only primary-source information node, BOOTSTRAP step0002, 2026-10-07 UTC. First directly reread `docs/user-instruction.md`, full `docs/idea-story.md`, and full research-literature-novelty skill. No build, native execution, measurement, dependency/Git action, canonical edit or paper edit. Scope: retained REPL Main/Snapshots/InfoTree and directly called Lean tactic/meta/declaration/kernel path. This addresses baseline guarantees, not a new RQ answer or novelty verdict. The existing Goedel `ast=false` whole-proof cost study remains unchanged.

## Finding

**`runProofStep`/`ProofSnapshot.runString` does not automatically assemble or kernel-check the original declaration when goals close.** It parses and elaborates tactics, synthesizes pending synthetic metavariables, and returns a new state plus goals, new messages/traces and syntax-derived sorries. Empty goals do not certify a closed, sorry-free original proof. Some tactics may internally invoke checking or create declarations, but the REPL closure path itself has no mandatory final `addDecl` for the theorem.

There is a source-native route from a retained complete proof expression to ordinary declaration kernel checking, without re-elaborating the source theorem. It requires preserving the original declaration type/value skeleton, universe parameters, binder order and declaration finalization context before completion. This is not an already exposed “validate original theorem” operation in the exact old REPL. A generic root-goal-to-lambda theorem check proves the captured goal; it does not automatically certify the complete original declaration or its feedback.

The strongest compatible baseline is therefore the existing immutable ProofSnapshot tactic branch **plus explicit complete-declaration assembly/finalization and checking where supported**, with full-source fallback. Merely comparing a new deeper branch mechanism to whole-theorem re-elaboration would omit existing nonnovel proof-state reuse.

## Exact pins and source verification

Retained upstream manifest pins `xinhjBrant/repl` to `3334a97b268ecc67beb36a75787f7e831208a724`; its `lean-toolchain` is `leanprover/lean4:v4.9.0-rc1`. Official Lean tag refs API resolves that tag to commit `be6c4894e0a6c542d56a6f4bb1238087267d21a0`. Local release archive provenance is `download-metadata.json`: official release URL, SHA-256 `b4a3898970dd9980f1a59fb399d3ed447c9c622f7c69639eb6ca9435d55fa6f8`. Selected retained REPL/Lean bytes were fetched individually from the exact official commits and matched byte-for-byte; this avoids inferring a source pin from executable filenames. Kernel C++ files absent from the distributed release source were fetched individually from the matching official tag, retained under `lean-source/`; no checkout or build.

## Mandatory versus absent behavior

| Boundary | Source facts | Guarantee/gap |
|---|---|---|
|REPL `runProofStep`|`REPL/Main.lean:269–279` loads a saved proof state, calls `runString`, then `createProofStepReponse`.|No automatic original theorem declaration finalization. Exceptions are converted to Lean error text.|
|Tactic continuation|`REPL/Snapshots.lean:142–151` runs Term/Tactic monads and `Term.synthesizeSyntheticMVarsNoPostponing`;174–183 invokes `evalTactic` after parsing category `tactic`.|Real Lean tactic elaboration, rather than a mocked goal transition; no mandatory original-declaration `addDecl` or proof-expression no-sorry scan.|
|Response|`Main.lean:129–154` emits new messages, traces, new info-tree sorries, a new snapshot handle and pretty-printed goals; `ast := none`.|Goal and feedback handles, no checked proof term or completed original declaration returned.|
|Sorry reporting|`REPL/Lean/InfoTree.lean:29–34` recognizes exact syntax strings for explicit tactic/term `sorry`;170–188 selects corresponding InfoTree nodes;201–207 returns their context/position.|Direct explicit syntax can be reported. Not an expression/dependency scan; implicit recovery sorry or other admitted expression routes cannot be certified absent from this list. The `TODO detect sorries?` above Main269 does not imply there is no direct-syntax reporting.|
|Snapshot reconstruction|`Snapshots.lean:193–212` restores Core/Meta state through InfoTree context, sets `termState := {}`, `termContext := {}`, tactic goals and anonymous elaborator.|Saved original Term elaborator continuation and declaration finalization metadata are not preserved in these reconstructed snapshots.|
|Ordinary declaration checking|Lean `AddDecl.lean:11–25` calls `addDeclCore` through `Environment.addDecl`, logs warning if `decl.hasSorry` and no prior errors, and throws kernel errors.|Kernel validity and no-sorry policy are separate. Ordinary Lean permits sorry; warning is not rejection.|

## What kernel checking actually does

The foreign primitive is declared in `Lean/Environment.lean:248–249` with `@[extern "lean_add_decl"]`. Matching `src/kernel/environment.cpp:295–300` sets the heartbeat scope and calls `environment.add`; `environment.h:108` defaults `check=true`. The theorem path at `environment.cpp:218–231` checks that the type is a proposition, checks the declaration name/universe parameters/type, rejects metavariables and free variables in the proof, infers/checks the proof value's type and checks definitional equality to the declared type. This is ordinary theorem kernel checking; goal-count inspection has none of these final-declaration guarantees.

`Lean/Util/Sorry.lean:24–34` implements `Expr.hasSorry` by finding `sorryAx` constants and `Declaration.hasSorry` by folding over declaration expressions. This catches direct and synthetic sorry terms in the assembled declaration after metavariable substitution. It does **not** recursively inspect all referenced theorem bodies: a proof using an already admitted theorem can contain only that theorem's constant. If the intended policy includes dependency-level admission, it needs an explicit dependency policy/check rather than claiming the built-in scan establishes it. Native Mathlib axioms and original warning behavior must remain distinguished from a stronger no-admission policy.

Lean `Elab/Tactic/Basic.lean:12–23` shows unsolved-goal reporting can both log an error and assign synthetic sorry. `Elab/SyntheticMVars.lean:327–363` ordinarily executes a `by` tactic, synthesizes synthetic metavariables, reports remaining goals, and under recovery admits metavariables on exceptions. The REPL runs `evalTactic` in its reconstructed context rather than replaying the full original declaration's enclosing `by`/term finalization continuation. Lean `Elab/Tactic/ElabTerm.lean:235–263` explicitly documents error-to-sorry differences, including that `exact`/`refine` can elaborate large terms with recovery. Therefore retain messages/errors as well as scan the assembled expression; neither an empty-goal result nor empty explicit-sorry list alone is enough.

## Source-native assembly route and its limits

For a supported simple theorem whose entire value is the captured root tactic metavariable, retain that **original** root expression independently of the shrinking tactic goal list, retain its original local context/binders and original full declaration type/universes/name, run candidate tactics in the snapshot, synthesize remaining synthetic metavariables, and `instantiateMVars` on the original value/skeleton. Close binder/free-variable structure with native `Meta.mkLambdaFVars` (`Lean/Meta/Basic.lean:915–919`) and the corresponding original type, instantiate levels and reject unresolved metavariables. Then use a `Declaration.thmDecl` carrying the original universe parameters and full type/value and call `Lean.addDecl` in a fresh appropriate environment before the original declaration was added. Explicitly classify sorry using `Declaration.hasSorry`, and preserve accumulated elaboration errors. This is a feasible proposal, not an implemented/qualified baseline.

For a tactic state inside a nested proof or later proof step, its current goal is only a subproblem. A saved `MVarId`/target is insufficient unless the original complete value skeleton and assignments linking that subgoal to it were retained. For multiple holes, all connected holes must be accounted for. A term-mode sorry snapshot creates a **fresh** metavariable from the expected type (`Snapshots193–199`); this is not automatically wired back into the original theorem value. A theorem already installed with sorry cannot simply be added again under the same name: ordinary kernel checks names. Renaming a wrapper theorem can check the proof term but changes the original declaration/name/context contract.

Ordinary source finalization does more than `addDecl`: `Lean/Elab/PreDefinition/Basic.lean:95–129` abstracts nested proofs, constructs the theorem/definition/opaque declaration, checks it, records term info, applies after-typechecking attributes, noncomputability metadata and potentially compilation/after-compilation attributes. To preserve original declaration behavior, capture a native predefinition/term continuation before theorem completion and resume these steps, or explicitly restrict the supported class and compare the missing behavior to full-source execution. It is not source-backed to assume the InfoTree ProofSnapshot has that continuation.

## Feedback/options/context retained and dropped

Native `Lean/Elab/InfoTree/Main.lean:98–111` reconstructs Core execution with `info.options`, namespace/open declarations, environment, name generator and metavar context, so those are **retained** in an in-memory snapshot. It substitutes filename `<InfoTree>` and default file map; original source positions/file diagnostics are **not** preserved by that reconstruction. `ProofSnapshot.create` defaults Term.State/Term.Context and anonymous tactic elaborator, so declaration name context, section-fvar bookkeeping, auto-bound implicit/auxiliary declaration mapping and term elaborator caches/continuations are not the original saved ones. The original full-command response can include original-source messages, tactic extraction/InfoTrees and optional AST processing; proof-step response omits AST and returns only incremental logs and state handles. Tactic source is parsed separately in category `tactic`, so surrounding command syntax/attributes and final-source diagnostic positions are absent.

Pickled snapshots further omit caches/logging and closures as documented in `Snapshots.lean` CompactableCoreState/MetaContext/TermContext; they should not be conflated with the in-memory snapshot baseline. The in-memory proof-state option context is still real Lean configuration, but reconstructed resource/context histories and source feedback need independent native qualification.

## Baseline and future experiment handoff

Existing old REPL already exposes immutable root reuse and proof-state backtracking; these are nonnovel. The compatible competitor represents the position that native logical proof-state reuse, with honest complete-declaration validation and full-source fallback, captures useful theorem preparation. If it matches the proposed mechanism, deeper preparation alone cannot support a new speed claim.

The newly clarified opportunity is narrower than “tactics skip kernel checking”: a complete original-declaration continuation that preserves feedback, admission classification and finalization may differ from this reconstructed InfoTree interface. Whether it saves substantial cost or enables a better bounded service is a hypothesis; no measurement here answers it. The existing whole-proof cost study still measures its declared boundary and must not be reinterpreted as proof of this deeper mechanism.

Next qualification proposal only: finite simple-theorem cases covering valid proof, direct sorry, implicit recovery/error, unresolved goals, nested subproof, name/section/universe/attribute-sensitive declaration and timeout. Compare full source, old native ProofSnapshot plus complete assembly/check, and any new continuation; retain original errors/sorries/options and complete theorem identity. Use fallback for unsupported context instead of counting zero goals as acceptance. Root chooses whether to admit this experiment. Declared source coverage complete; feasibility of full original continuation and numerical benefit remains unresolved. No RQ/thesis/novelty/canonical change adopted.

## Primary provenance

Official REPL base: https://github.com/xinhjBrant/repl/tree/3334a97b268ecc67beb36a75787f7e831208a724 . Official Lean base: https://github.com/leanprover/lean4/tree/be6c4894e0a6c542d56a6f4bb1238087267d21a0 . Fetches and retained source reads occurred on2026-10-07 UTC. Tables below record bytes used; official individual URL = base repository raw commit path. Selected byte comparisons to official sources were true for Main/Snapshots/REPL InfoTree, Lean AddDecl/SyntheticMVars/Util Sorry. Remaining Lean files were read from the exact archived release source; kernel files were official matching source fetches.

| Source path | SHA-256 |
|---|---|
| REPL `REPL/Main.lean` | 534ac2691f90d5a8145cbf4d0975a09b41088150faaa000d91210fd72c82caee |
| REPL `REPL/Snapshots.lean` | 8149b58d2013e6c346e10eb4393588a6afeb70475a5819ccf91b674d018ce78f |
| REPL `REPL/Lean/InfoTree.lean` | 3601909bfe4b902c8250efc7cf0d9a55236357e6a38d7a7c61fe3821e734e211 |
| Lean `src/Lean/AddDecl.lean` | 3fbf06aaa766ffe2d7bc93748509dbd34bffa18429b27feb0f65a66d5ea85b4b |
| Lean `src/Lean/Environment.lean` | 90eeb8708c42ee5434e1ed4e35af72beec1fad31bffa27a2c01732ebe578776b |
| Lean `src/Lean/Util/Sorry.lean` | fa6ff601afd27e50a8a3ae655174f53fdcd429c6680389a2b3eecf02e446b780 |
| Lean `src/Lean/Elab/SyntheticMVars.lean` | df27812844bdc88fc7684241f0980e8c2c75da7cdbcc3a6c493f2c6d61f18ac0 |
| Lean `src/Lean/Elab/Tactic/Basic.lean` | 0adb496125f47cf24d129fa5f492a1d6cada3255f9b1092ab44db82e2b2f45fc |
| Lean `src/Lean/Elab/Tactic/ElabTerm.lean` | 41f32b18b95a10fbe751e28b85c9ea5676d9db7ef78ab77609081149a42f01c5 |
| Lean `src/Lean/Elab/BuiltinTerm.lean` | 0da27fa025e34a7dd17bc415c726137fc480b07740d0b93cfd1ca64c4e1654a6 |
| Lean `src/Lean/Elab/PreDefinition/Basic.lean` | 6076f3e0c18261dda9f9aa42862c8bf4cab4040593da8ad07e17875de8910439 |
| Lean `src/Lean/Elab/InfoTree/Main.lean` | 45dcdc124feb4b19895e595742b94e0a3ce46ef5c63243211e24a6e1be05efc8 |
| Lean `src/Lean/Meta/Basic.lean` | 2b2a866a2f972f8f9025d3d811a73c48feb2f6ae0cef45f95dc957c28186339e |
| [Lean src/kernel/declaration.cpp](lean-source/declaration.cpp) | 5f61103e9d0b1472cb6e0351ae1b5a7bca155fd23a2f3bfda10e01825894e98a |
| [Lean src/kernel/environment.cpp](lean-source/environment.cpp) | 8a46945cee66f91a3316dec4cc1baf3d9a6b19c0d0328bacf29f37effc21c177 |
| [Lean src/kernel/environment.h](lean-source/environment.h) | 635e91b9f809583b1260f646dee47af9a21b767b353fd0def44736ebbbe44bad |
| [Lean src/kernel/type_checker.cpp](lean-source/type_checker.cpp) | bed7528a5dc64b7d1319ccf72b9cea7e836d2c894dc93042c56ba72db17a4ed6 |


## Follow-up: current stock Lean4.34.1 already reuses declaration headers and tactic state

2026-10-07–08 UTC; first directly reread user instruction and full current idea story. This finite official-source follow-up appends to the same node. No execution, timing, dependency/build/Git action, canonical edit, thesis adoption or new experiment. Official `v4.34.1` tag refs API resolves to commit `5045d0056413266e57c625dcd7c365b10e377c52`. Individual source files at that exact commit are retained in `lean-modern-source/` below. The obsolete guessed `src/Lean/Elab/Snapshot.lean` returned404; official tree/source imports resolved the actual snapshot types in DefView/Language and TermElabM. Read complete relevant functions, not search-result snippets.

### Competitor fact and same-claim consequence

**Yes: current stock Lean has intra-command declaration-header reuse and tactic-prefix reuse through native saved elaboration states, followed by ordinary original-declaration finalization.** This is stronger than old4.9 REPL reconstruction and stronger than merely remembering whole completed command environments. A hypothetical system preserving an original theorem's elaborated type and continuing a changed proof body overlaps directly with these stock paths. The old REPL gap above is a version/interface fact, not modern novelty. Bare “retain type, rerun proof and check the declaration” has high same-mechanism risk.

This source result does not establish a service's equal-resource frontier, arbitrary independent concurrent branches, universal diagnostic/resource identity or numerical benefit. It establishes a mandatory compatible native competitor or explicit version-compatibility limitation. No claim that current Mathlib/Lean is a drop-in replacement for the exact4.9 workload is made.

### Concrete source path for changed body

- `Lean/Language/Lean.lean:603–617` detects that a command's syntax changed, cancels subsequent old commands, and explicitly delegates partial reuse of the current command to its elaborator rather than discarding that whole command. At682 it passes the current old command's elaborator snapshot into `doElab`; `741–770` constructs `Command.Context.snap?` and calls `elabCommandTopLevel`.
- `Lean/Elab/MutualDef.lean:1518–1572`, full `Command.elabMutualDef`, builds a full declaration header reference from modifiers plus header syntax. It permits the old `HeaderProcessedSnapshot` when elaboration context/state and all earlier headers are unchanged and `fullHeaderRef.eqWithInfoAndTraceReuse` succeeds. The proof body is not part of this header comparison.
- Full `Term.elabHeaders`, `MutualDef.lean:209–357`, retrieves `old.view` and `old.state` at224–247 and passes them to `withRestoreOrSaveFull` at252–255. The skipped action otherwise elaborates attributes-before-elaboration, declaration name, universe names, binders, target type, synthetic metavariables, auto-bound implicits, full forall type and header checks. Thus an unchanged header has its elaborated type and native Term/Meta state restored even when the proof body differs.
- `Lean/Elab/DefView.lean:59–79` defines the retained header snapshot: `DefViewElabHeaderData`, `Term.SavedState` including environment additions, body syntax and body task, top-level tactic syntax/task, diagnostics and additional snapshot tasks. `DefViewElabHeaderData` contains declaration names, elaborated type, level names, binder IDs and parameter count; these are not just goal strings.
- `Term.elabHeaders` separates `reuseTac` from `reuseBody`: previous headers/bodies must be reusable for a tactic start to be reusable; body result reuse additionally requires unchanged whole body syntax. On a changed body it cancels the old body's terminal async work, including kernel/codegen, while forwarding eligible old tactic snapshots (`230–245`). Whole old proof acceptance is not incorrectly carried over to a changed proof.
- Full `elabFunValues`, `MutualDef.lean:516–593`, restores a whole previous value/state only under the stricter unchanged-body invariant. Otherwise it elaborates the new body in the retained declaration/header context with `tacSnap?`, synthesizes metavariables, instantiates the value and closes original binders with `mkLambdaFVars`. This proceeds into native declaration finalization, not a stand-alone REPL goal handle.
- `MutualDef.lean:1267–1342` shows native asynchronous theorem processing: original signature/universes committed; `finishElab #[header]` runs for the proof; resulting constant and checked environment are committed; native attributes and deriving handling remain part of the path. Changed proof work is re-elaborated and rechecked as required. This is not a captured arbitrary call-stack continuation: it is stock persistent saved state plus native elaboration control flow.

### Tactic reuse and retained state

Full `Lean/Elab/Tactic/BuiltinTactic.lean:36–156` (`evalSepTactics`) creates finished/inner/next snapshot promises per tactic. If the preceding state and trimmed tactic syntax match, it restores the old finished native state and skips that tactic; changed tactic or separator stops subsequent sequential reuse. Eligible nested incremental tactics receive the inner snapshot. New diagnostics/info tree/state and async tasks are attached to finished snapshots. A changed first tactic can still reuse the declaration header, even when there is no unchanged tactic prefix to reuse.

`Lean/Elab/Tactic/Basic.lean:115–132` saves/restores tactic state plus Term.SavedState. `Lean/Elab/Term/TermElabM.lean:417–456` saves/restores Term state plus Meta saved state and explicitly propagates tactic snapshot promises on restoration. The native declaration pipeline supplies context via its original declarations and syntax paths; it does not rebuild a fresh default Term.Context from InfoTree as old REPL4.9 does. `SyntheticMVars.lean:474–537` runs original `by` tactic synthesis/recovery with pending-mvar handling and native scope/exporting rules. It still allows recovery sorry and needs ordinary admission/error policy, just like full-source Lean.

This is selective reuse, not arbitrary term editing reuse: the top-level tactic path is recognized for simple `:= by ...` bodies. `MutualDef.lean:326–357` excludes `where` bodies from that tactic snapshot recognition; headers can still be separately reusable. `Term.lean` marks participating elaborators with incremental attributes; `Tactic/Basic.lean:305–316` disables nested snapshot access for unsupported tactic elaborators. `TermElabM.lean:481–550` narrows syntax/preceding-context reuse and provides explicit disabling guards. Neither a logical-equivalent header nor a changed source location automatically meets exact native syntax/context comparisons.

### In-memory and disk snapshots: actual distinction

In-memory frontend/LSP reuse retains the native command and child elaborator snapshot tree and supplies the previous tree to processing. The library interface `Lean/Elab/Frontend.lean:99–124` (`IO.processCommandsIncrementally`) accepts prior `IncrementalState`, invokes `Language.Lean.processCommands` with prior input/snapshot, and collects diagnostics from all snapshot nodes plus complete command info trees. This supports complete native declaration processing with partial reuse, beyond old proof-step output.

**Current full disk snapshots are not restricted to completed whole-command boundaries.** `Frontend.lean:282–290` defaults `internal.cmdlineSnapshots` to false when full saving, specifically to retain enough information for resumption. `314–343` loads a retained `InitialSnapshot` and passes it to the same `Language.Lean.process`; `351–368` serializes that full snapshot graph with `CompactedRegion.save(... allowClosures := true)` after resolving cancellation promises. No child-elaborator truncation occurs for full save. Consequently eligible declaration header/tactic child snapshots are part of the saved native graph, rather than a separate implemented-from-scratch disk proof-state mechanism. `370–372` explicitly truncates only header-only save to import preparation.

Option qualification matters: `Language/Lean.lean:763` sets `Command.Context.snap? := none` when `internal.cmdlineSnapshots` is true, and686–691 drops command metadata. A harness seeking intra-command reuse must retain/use full snapshot mode with this option false; explicit enabling defeats that deeper reuse. This source inspection establishes available code paths, not that every default CLI invocation/load combination or custom initializer behaves identically. No loaded snapshot was executed here.

Official [PR13965](https://github.com/leanprover/lean4/pull/13965), merge `b8b35fcd1b8705abb9cb0592d84a640645ef2cb1`, introduced experimental save/load/header-save plumbing. Its body describes caching in-process elaboration state across invocations and requires the caller to verify unchanged imported modules. The modern implementation above is stronger evidence than interpreting the PR's abbreviated “after each command” wording as a whole-command-only guarantee. `Frontend.lean:322–329` also explicitly records a possible behavior divergence from unusual module initializers on snapshot load. Therefore disk validity and initializer/context qualification remain obligations, not automatic universal transparency.

### Disposition for parent

A whole-command disk snapshot baseline understates current stock Lean. Before admitting a new preserved-declaration continuation experiment, include stock incremental declaration-header plus supported tactic reuse, via compatible in-memory or full disk frontend paths, and native completion/checking with all errors/admissions retained. If workload/toolchain cannot move from4.9, document that limitation; do not turn absence in the old REPL into novelty against modern stock Lean. Service-level branching/placement/resource behavior may still be open differentiated questions, but this node makes no adopted thesis or performance claim. Exact numerical usefulness, corpus compatibility, supported-case coverage, and independent branch/cancellation guarantees remain unresolved.

### Follow-up primary provenance

All files below are individually fetched from `https://raw.githubusercontent.com/leanprover/lean4/5045d0056413266e57c625dcd7c365b10e377c52/<source-path>` on2026-10-07–08 UTC. The PR JSON is from official GitHub API `/repos/leanprover/lean4/pulls/13965`; it records full primary PR description and merge metadata. No secondary literature/source summary used.

| Retained source | SHA-256 |
|---|---|
| [pr13965.json](lean-modern-source/pr13965.json) | c1bfd4341995a9275b47d7bd7f8ceeeb2c24859f7bfecc8366cbb4cd295eeea0 |
| [src_Lean_Elab_Declaration.lean](lean-modern-source/src_Lean_Elab_Declaration.lean) | 88d46c4d24bff00043c9c4cc019c633e2c0d6b9bf25ec5ba6d7a83648cb7ef8b |
| [src_Lean_Elab_DefView.lean](lean-modern-source/src_Lean_Elab_DefView.lean) | cde03097a238b437031c9d00ca437e3fc4f10a6f51667b0eb7b851d09cb412c6 |
| [src_Lean_Elab_Frontend.lean](lean-modern-source/src_Lean_Elab_Frontend.lean) | e3e9037222c00308edc4fed589da83a80620bf5b35108779564fc485d8c17774 |
| [src_Lean_Elab_MutualDef.lean](lean-modern-source/src_Lean_Elab_MutualDef.lean) | 73a278e79b6fa2a355c3076c40eec8f0cd607c8b68f21e1fa344b56d14e6c3b9 |
| [src_Lean_Elab_SyntheticMVars.lean](lean-modern-source/src_Lean_Elab_SyntheticMVars.lean) | e33b9ec83b5ca5108b910419fda0492a36a7837cb205d7594429fb6ed9ea22fc |
| [src_Lean_Elab_Tactic_Basic.lean](lean-modern-source/src_Lean_Elab_Tactic_Basic.lean) | 6b27a02d50681f2d14c9e50be6e28f822eea4f2118da10b23cb50a9f3e80d9ac |
| [src_Lean_Elab_Tactic_BuiltinTactic.lean](lean-modern-source/src_Lean_Elab_Tactic_BuiltinTactic.lean) | 21e8b53aec5ff85dd19e15b5ba2eed56d9da9883fdc09b1c410c77b0d1f567b4 |
| [src_Lean_Elab_Term.lean](lean-modern-source/src_Lean_Elab_Term.lean) | 0d3047f9e1e3160a52eba27400b12eeab0ca9a08092e5bcd530f8ea2b87fa8fc |
| [src_Lean_Elab_Term_TermElabM.lean](lean-modern-source/src_Lean_Elab_Term_TermElabM.lean) | 8c68695702df566dc44c7c2da8cdd8735cac6bd5dcafec7537efdb18c616b87f |
| [src_Lean_Language_Basic.lean](lean-modern-source/src_Lean_Language_Basic.lean) | a6aca4bca50ae1477eeab77696a199c029ae41a8d178fc86dc5d83767dea3236 |
| [src_Lean_Language_Lean.lean](lean-modern-source/src_Lean_Language_Lean.lean) | f2bca1a2f1d2e435dd9996417245be987368a6e3465cf48fc6cbd1ce938d10cc |
| [src_Lean_Language_Lean_Types.lean](lean-modern-source/src_Lean_Language_Lean_Types.lean) | 17dc57647a274ed317493de4262d3779b1244b1152a3b2d562e96c0d21ccd0f2 |
