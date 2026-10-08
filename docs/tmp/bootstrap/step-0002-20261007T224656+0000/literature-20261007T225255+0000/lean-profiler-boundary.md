# Pinned Lean4.9 CLI profiler boundary

Source-only E7 prerequisite, BOOTSTRAP step0002, 2026-10-08 UTC. First directly reread user instruction, complete idea story/evaluation, and full research-literature-novelty skill. Finite question: what can ordinary exact Lean4.9 CLI `--profile` discriminate on complete real Mathlib module source? No executable invocation, measurement, build/dependency/Git action, canonical/paper edit, chosen hypothesis or replacement of experiment002. All primary source below is pinned to `be6c4894e0a6c542d56a6f4bb1238087267d21a0` (`v4.9.0-rc1`). Native files absent from the release source were individually fetched from official matching source; retained Lean bytes also match the selected release source used in earlier qualification.

## Qualification verdict

**Stock `--profile` is useful for a coarse, normal-source component profile; it is not an exact preparation/elaboration/kernel partition or GPU feasibility result.** It enables the existing profiler without changing the `addDecl` checking path. It can report import, parsing, residual command elaboration, tactic execution, type checking, compiler/attribute/linting and initialization category elapsed times when those instrumented paths execute. Keep complete diagnostics and terminal exit status: successful collection is not necessarily successful checking, and ordinary Lean accepts sorry with warnings.

Use the simple stock path if parent admits this question. Read category totals as measured component elapsed times under profiler overhead and observed thread configuration; do not rename residual elaboration “theorem preparation,” interpret cumulative totals as CPU seconds, sum overlapping cross-thread times into makespan, or infer dynamic operation readiness from category names. There is no need for custom phase instrumentation to answer the first coarse question.

## CLI and normal-source boundaries

- `src/util/shell.cpp:247,598–599` maps `--profile` to `opts.update("profiler", true)`. The option help at224 says elaboration/typechecking times, but actual granularity is determined by instrumentation below. Profile does not set a skip-check, parse-only or proof-as-sorry option.
- `shell.cpp:464–466` measures `lean::initializer` with steady clock;649–651 adds that time under `initialization`. This excludes later option parsing, file reads and task-manager setup. CLI default thread count is hardware concurrency in multithreaded builds (`477–480`); `-j` changes it (`510`). Profile does not force a serial run or disable tasks.
- `shell.cpp:725` calls normal frontend with original complete source contents;764 displays cumulative profiling on stderr. Optional `.olean` serialization and C/LLVM emission get distinct native categories at738–760. Thus output options affect measured work. Source reading/options/output/teardown are not all enclosed in a universal timer; standalone end-to-end wall time and resource usage remain separate quantities if an experiment later measures them.
- Exact `Lean/Elab/Frontend.lean:151–191` uses its ordinary old command-line driver (`if true`): parse header, `processHeader`, then `IO.processCommands` on complete source commands, report messages and optionally write `.ilean`. It does not use the alternate snapshot processor merely because profile is enabled. Per-command parser category is `Frontend.lean:67`; import/header parsing is not all part of that parser timer. The extra imported trace inserted at175–185 belongs to the separate `trace.profiler.output` Firefox exporter, not the stock cumulative category mechanism. Do not mix those APIs' quantities.

## Exact quantities, aggregation and threshold

`Lean/Util/Profile.lean:12–25` declares `profiler=false`, and default `profiler.threshold=100` milliseconds. `threshold.getSecs` at31–33 divides by1000. `profileit` at36–37 is implemented by native `lean_profileit`;40–51 wraps EIO/monadic actions. Native `library/profiling.cpp:17–21` receives that value as a seconds-duration (the local name `ms` does not change its units).

Full native `library/time_task.cpp:44–77` constructs a `time_task`, times `apply_1(fn, box(0))`, and uses thread-local `g_current_time_task` as the nesting parent. `util/timeit.h:52–87` uses `std::chrono::steady_clock::now` and a `std::chrono::duration<double>` in seconds. It records **elapsed wall-clock duration**, including descheduling/waiting inside the scope, rather than thread/process CPU time, cycles, instructions, heartbeats, allocations or memory bandwidth.

At destructor `time_task.cpp:61–68`, each enabled scope:

1. Reports its elapsed duration minus excluded child durations into the global category total.
2. Subtracts its full inclusive elapsed duration from its active **same-thread** parent's timer.
3. Later timer destruction prints an individual entry only if its exclusive elapsed duration meets the threshold.

So same-thread nesting is exclusive by construction; the unprinted small scopes still accumulate and are still excluded from their parent. Changing the threshold controls individual output, not sampling or whether category totals include short calls. The accumulator (`time_task.cpp:14–30`) is a process-global `map<string, second_duration>` protected by mutex and sums by **category only**. Declaration/tactic name can appear on individual messages but is not a separate cumulative key. No count/distribution/per-input record is accumulated here. Totals persist for this initialized process and are displayed at normal CLI completion, not reset per theorem.

`util/timeit.cpp:12–19` prints with three significant digits, in milliseconds below one second and seconds otherwise. Preserve raw unit strings and precision; displayed totals cannot support finer claims than their rounding. Individual scopes have threshold suppression; cumulative categories do not. Timers take slightly different `now()` samples for aggregation, child exclusion and printing, so printed entries/totals need not form an exact algebraic sum.

## Threads, nesting and profiler overhead

`time_task.cpp:16` declares the parent pointer with `LEAN_THREAD_PTR`; matching `runtime/thread.h:180–185` uses thread-local storage. No parent/child propagation to a different thread appears in this profiler. Therefore an instrumented worker scope is accumulated globally but is not subtracted from a parent active on another thread. If the parent waits while worker work runs, scope totals can overlap; worker elapsed times can also overlap one another. Conversely task work without instrumented scopes is not invented into its own category. The profiler identifies instrumented scope time, not a complete scheduler/task critical path.

In this exact frontend the ordinary top-level command wrapper is synchronous. That does not imply every tactic/compiler/plugin/FFI operation is serial; CLI creates a task manager and source extensions can run tasks. No cross-thread task behavior or degree of overlap was measured here. The report should retain actual `-j`/runtime options and avoid claiming universal async exclusivity.

Overhead is concrete but unquantified: enabled scope construction invokes clock reading, allocates/stores timer/category/callback state, creates thread-local nesting, and each finished scope acquires the global mutex to aggregate. Entries over threshold format and write trace output. Child timer/report overhead is not generally all removed from enclosing measured work; reporting times/clock samples occur during nested timer lifetime. Profiling may perturb wall time, contention and scheduling. No numerical overhead bound is source-backed. It is a normal-check **profiled** run, not an uninstrumented performance oracle.

## What the categories actually enclose

| Stock category | Exact source boundary | Interpretation |
|---|---|---|
|`initialization`|shell464–466,649–651|Lean initializer elapsed time; not all process setup.|
|`import`|`Lean/Environment.lean:870–878` `importModules`|Recursive compiled-module read/load plus import finalization/extensions/initializers in that operation; not rechecking all imported proofs.|
|`parsing`|Frontend67|Current source command parser; not all frontend/file/header work.|
|`elaboration`|`Lean/Elab/Command.lean:448–470` full `elabCommandTopLevel`|Command processing/recovery/messages/linters excluding instrumented same-thread children. It is residual elaboration, not just theorem header preparation.|
|`tactic execution`|`Lean/Elab/Tactic/Basic.lean:149–151` and complete `evalTactic`|Tactic elaborator scope; nested tactic calls and other instrumented same-thread children excluded. Individual name is tactic syntax kind, not necessarily theorem name.|
|`type checking`|`Lean/AddDecl.lean:18–25`|Whole addDecl wrapper, including sorry detection/warning and tracing/error wrapper plus ordinary native kernel insertion/check; not pure reduction or a count of operations.|
|`attribute application`|`Lean/Elab/Term.lean:758–759`|Attribute application wrapper, nested instrumented time excluded.|
|`linting`|Command253|Native linter wrapper, when run.|
|`compiler new`|`Lean/Compiler/Main.lean:14`|Native compilation wrapper; not proof checking.|

Only categories actually reached appear. Auxiliary declarations generated while elaborating tactics/definitions also pass `addDecl`; the type-check total is not exclusively the top-level source theorem's final proof. Uninstrumented Meta inference/reduction/unification during tactic elaboration can reside in tactic/residual elaboration time. The profile does not split dynamic closure/conversion, type inference and reduction into GPU-ready kernels.

## Kernel checking and import trust

`Lean/AddDecl.lean:11–25` uses `Environment.addDecl` and foreign `addDeclCore`; `Lean/Environment.lean:248–249` binds it to `lean_add_decl`. Native `kernel/environment.cpp:295–300` calls `environment.add` under the heartbeat scope; `kernel/environment.h:108` defaults `check=true`. The theorem path `environment.cpp:218–231` checks proposition type, names/universes, closed type/value, proof type and definitional equality; definition path186–215 likewise checks the native body/type under safety rules. No trust-level test bypasses these ordinary `addDecl` checks in the inspected path. Profile alone preserves that path.

CLI default trust is `LEAN_BELIEVER_TRUST_LEVEL +1` (`shell471`), and `-t` can change it (`566`); record the exact option rather than treating an arbitrary default as a fully rechecked dependency library. Import loading is a separate boundary: `Environment.lean:769–775` reads compiled module data, recursively visits imports and stores compacted regions; full `finalizeImport` at812–866 constructs maps from retained `ConstantInfo` objects and environment extensions. It does **not** call kernel `addDecl` on every imported declaration. The header stores supplied trust level, imports, module names/data and compacted regions. Real selected module source is elaborated/checks its new declarations; transitive compiled dependencies are loaded/reused. A source profile of module A is not a profile of fresh checking all Mathlib transitive proofs, even with trust0.

Ordinary Lean's admission contract remains: `AddDecl21–22` warns when a declaration has sorry and no prior errors; it does not reject it as an invalid kernel declaration. Complete errors/warnings/source identity and terminal status must therefore accompany any normal-check profile. Profile totals alone cannot establish no-sorry fidelity or whether recovery created placeholder proof values.

## Useful finite discrimination for parent

A real admitted complete-module CPU profile can determine whether normal module checking spends substantial instrumented elapsed time in import preparation, tactics/residual elaboration, compilation, or native declaration checking, and whether a few expensive native checks/tactics dominate visible entries. That can guide where further dynamic profiling is justified. Large import/residual time supports investigating preparation costs; large type-checking time establishes a costly ordinary kernel boundary deserving deeper analysis. Neither observation alone proves shareability, novelty, cross-candidate locality, GPU-ready parallel dependence, transfer feasibility or speedup.

If type-checking is small, the stock result can bound how much that measured normal-check component matters in that module/profile configuration; it does not refute all heterogeneous checking or different warm workloads. No percentages, chosen route or timings are inferred here. Parent chooses whether to admit a stock `--profile` source-library study alongside the existing active work; this source node neither runs nor redesigns it.

## Provenance and closure

Declared finite boundary complete: official CLI option, stock Lean Profile/AddDecl/frontend, native time_task/clock/category accumulator and direct import/kernel paths inspected. Missing guessed `src/Lean/Shell.lean` and `src/util/thread.h` were404; official tree resolved `src/util/shell.cpp` and `src/runtime/thread.h`. No broader literature branches opened. Every retained file below is from official raw URL `https://raw.githubusercontent.com/leanprover/lean4/be6c4894e0a6c542d56a6f4bb1238087267d21a0/<path>`; filename uses underscores for `/`. Fetch/read date2026-10-08 UTC. Runtime object file was inspected as a possible primitive location, but the actual primitive is time_task; no inference uses unrelated runtime code.

| Primary bytes | SHA-256 |
|---|---|
| [src_Lean_AddDecl.lean](lean-profiler-source/src_Lean_AddDecl.lean) | 3fbf06aaa766ffe2d7bc93748509dbd34bffa18429b27feb0f65a66d5ea85b4b |
| [src_Lean_Compiler_IR_CompilerM.lean](lean-profiler-source/src_Lean_Compiler_IR_CompilerM.lean) | 114751f0b893b4452b6e50b65d690307d6ad4e56d38dd8276a6de15cb34d7c41 |
| [src_Lean_Compiler_Main.lean](lean-profiler-source/src_Lean_Compiler_Main.lean) | ef863e5038565cfaed533f0eb07f4fc7b494932e4ca08c3c4244bb6e5dcdaa2f |
| [src_Lean_Elab_Command.lean](lean-profiler-source/src_Lean_Elab_Command.lean) | 3168b55f4763b56bb80ccc2d6c33272277abc8f1752768f2a9ea4cb8a81d836d |
| [src_Lean_Elab_Frontend.lean](lean-profiler-source/src_Lean_Elab_Frontend.lean) | f23ae1f3c5eff2f6cc2f4a9fdf33b8ccf524e8e656b40b70b0b716c44049dcf1 |
| [src_Lean_Elab_Import.lean](lean-profiler-source/src_Lean_Elab_Import.lean) | 0460ae2353a7c02f1bee7f927ac093df640f113d6d00a8ca2b1d885b3882b0e7 |
| [src_Lean_Elab_MutualDef.lean](lean-profiler-source/src_Lean_Elab_MutualDef.lean) | 6f2ea0cc28ce50568247428058da17cc243a5982923c73d579aa997f3d20d693 |
| [src_Lean_Elab_PreDefinition_Basic.lean](lean-profiler-source/src_Lean_Elab_PreDefinition_Basic.lean) | 6076f3e0c18261dda9f9aa42862c8bf4cab4040593da8ad07e17875de8910439 |
| [src_Lean_Elab_PreDefinition_Main.lean](lean-profiler-source/src_Lean_Elab_PreDefinition_Main.lean) | 0cf518de32e70c295143760cea0567f81f20180a2314e452c3fda5f38584ec9b |
| [src_Lean_Elab_Tactic_Basic.lean](lean-profiler-source/src_Lean_Elab_Tactic_Basic.lean) | 0adb496125f47cf24d129fa5f492a1d6cada3255f9b1092ab44db82e2b2f45fc |
| [src_Lean_Elab_Term.lean](lean-profiler-source/src_Lean_Elab_Term.lean) | 8d8f0fe5e0335a70e43a84adda2d07105ce45342a103c93ca9f4bb0e0c22ecca |
| [src_Lean_Environment.lean](lean-profiler-source/src_Lean_Environment.lean) | 90eeb8708c42ee5434e1ed4e35af72beec1fad31bffa27a2c01732ebe578776b |
| [src_Lean_Util_Profile.lean](lean-profiler-source/src_Lean_Util_Profile.lean) | e49b40c437dbae29d004fbbf2256dc3e982c4503db2d30c59f8cdfd80aa2c6a6 |
| [src_kernel_environment.cpp](lean-profiler-source/src_kernel_environment.cpp) | 8a46945cee66f91a3316dec4cc1baf3d9a6b19c0d0328bacf29f37effc21c177 |
| [src_kernel_environment.h](lean-profiler-source/src_kernel_environment.h) | 635e91b9f809583b1260f646dee47af9a21b767b353fd0def44736ebbbe44bad |
| [src_library_profiling.cpp](lean-profiler-source/src_library_profiling.cpp) | 1d05c2e82ae1b9155c3a842f6142b741f62f093acbb0a43e75ca07432dfbc575 |
| [src_library_profiling.h](lean-profiler-source/src_library_profiling.h) | 2cdc1c9ede0f93c49f0c0ca2065ea39fc21141ba56c503c3f55f7cd89a323dbb |
| [src_library_time_task.cpp](lean-profiler-source/src_library_time_task.cpp) | 0614afed9022c5bdab531b6202d6318d26fe4e3340b07b06c223e538b8922d10 |
| [src_library_time_task.h](lean-profiler-source/src_library_time_task.h) | 0ac6f6ea6ead59ec7b5a973062e17dfe550a9dd03b837817468946aaef1152db |
| [src_runtime_object.cpp](lean-profiler-source/src_runtime_object.cpp) | fa3959dfee75706f8d3b1717aab7bc033f3c6c50ce69294f783e20078a1ec48d |
| [src_runtime_thread.h](lean-profiler-source/src_runtime_thread.h) | 33395abbc8518d04ca3a60732999719c7780f78114bf1aeaee5a98a39ff33a29 |
| [src_shell_lean.cpp](lean-profiler-source/src_shell_lean.cpp) | b311e6363d689e7b6d2e717c53981c59c63104892dc1d0cb308d977d6c6d943a |
| [src_util_message_definitions.h](lean-profiler-source/src_util_message_definitions.h) | 88596e223ad97d50e4c03d90d1823c34773adf6b93a6f4b298bbeec9150bffec |
| [src_util_shell.cpp](lean-profiler-source/src_util_shell.cpp) | 523f424ea090affe55591d619446af609dc538fe8dce6f650988dc13a69633de |
| [src_util_timeit.cpp](lean-profiler-source/src_util_timeit.cpp) | b51f5b1f4b689f24d346c4ce9d2c767aa6b552cb0c344c779e79afac9011a6a5 |
| [src_util_timeit.h](lean-profiler-source/src_util_timeit.h) | a7fee823023a0de2e25a6424db74a8badb9f6af9c4224fd7873e4f499a6c627b |
