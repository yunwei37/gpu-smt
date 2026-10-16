# E038 independent native setup/result audit

Observed 2026-10-16. One read-only audit of the genuinely new integrated setup, including the source repair and binding receipts produced during this audit. No experiment, implementation, baseline, resource policy, OMP file or Git state was changed by the reviewer. Only this report is authored.

## Judgment

- **Run status:** valid limited real-input setup; complete service experiment remains incomplete.
- **Tested hypothesis:** native runtime integration and the small awaited reference/task witness are supported by actual execution. The RQ3 latency/throughput/memory advantage and general isolation/lifetime hypothesis remain **inconclusive**.
- **Research value:** dependency-only independently; useful setup inside the admitted mechanism experiment, not a new paper result.
- **Paper impact:** an executable implementation boundary has advanced. No new superiority, general isolation, complete RQ, GPU benefit, novelty or venue-readiness claim follows.
- **Next decision:** continue substantive service/performance integration with this real native path, fixing concrete integration defects and completing the matched protocol. Do not launch the full matrix yet or return to another symbol-only/correctness-only program.

This setup is substantially stronger than a toy ref benchmark: the unchanged first actual Goedel4.27 proof goes through the original REPL frontend and native verifier with imported native libraries. It is substantially weaker than a complete concurrent service result: there is one real source per fresh process, no service concurrency/throughput comparison, no fleet-memory result, no qualified unsupported-effect fallback and no matched rebuild reference.

## What was independently checked

Read the admitted plan/review, current native header/support implementation, full upstream runtime patch and setup harness, actual private patched io.cpp/object.cpp, compile/link/source/dependency records, all setup1–5 terminal/stdout/stderr records, original transport and source, v1 archive, and setup4/5 process maps.

Read-only tools additionally checked native symbols, ELF dependencies/flags and disassembly. Both the actual executable and the actual rebuilt shared runtime call gpu_smt_resolve_ref from lean_st_ref_get. Reverse patch dry-run against the private source succeeds. These are source/binding checks, not additional native experiments or proof tests.

The retained upstream tar member named by setup-original-input.json independently matches its code byte for byte: Proof_00000, 1,282 UTF-8 bytes. The transport uses the actual Mathlib/Aesop header and env0; its body exactly equals that source with import lines blanked, preserving line positions. There was no selected proof rewrite, relaxed native check, skipped fallback failure or substituted exported expression.

## Actual raw results and boundaries

Every successful setup below exits0 with empty stderr. The original executable emits header {env:0}, then candidate {env:1}. Every off/on setup emits the same parsed native payloads. Empty messages/sorries fields are the original protocol encoding here; this is a native accepted-command observation on this source, not merely a device return.

| Observation | Whole process seconds | Internal response-ready seconds | Through endBranch return seconds |
|---|---:|---:|---:|
| setup3 original native REPL | 6.834092548 | not separately recorded | not separately recorded |
| setup3 v1 off | 7.031539352 | 3.378218144 | 3.378273664 |
| setup3 v1 on | 7.033305367 | 3.286247567 | 3.441643779 |
| setup4 v1 off, maps receipt | 6.932477778 | 3.220171199 | 3.220216156 |
| setup4 v1 on, maps receipt | 7.132771036 | 3.371788903 | 3.519912857 |
| setup5 v2 off, cleanup-scope repair | 7.577852943 | 3.737856122 | 3.737903815 |
| setup5 v2 on, cleanup-scope repair | 6.826949013 | 3.064243684 | 3.214825004 |

These are individual integration observations, with changed instrumentation/build stages and substantial drift. They are not ordered whole-corpus performance repetitions, confidence intervals, a thread/concurrency optimum or a reliable speedup/regression estimate. In particular, the last lower on time is not evidence of a branch acceleration.

Each enabled candidate records exactly 8,905,059 ref operations,43 ref versions,1 thunk operation/version and245 admitted descendant tasks. Disabled candidates record0 ref/thunk operations/versions and244 tasks. The one-task difference is retained; the logs do not establish an isolated causal explanation. Counters measure this instrumented mechanism, not whole CPU fractions or an acceleration upper bound.

The separate witness after each real source records initial0, task37; off returns root37, on returns root0. On records3 ref operations,1 ref version and1 descendant task for that witness. This establishes the small prepared-ref/awaited-asTask behavior and actual branch-context propagation on that path. It does not prove overlapping candidates, cancellation, detached descendants, arbitrary aliases/effects or every native async path.

### Timing qualification that changes interpretation

The harness takes responseAt after constructing the JSON string but prints RESPONSE only **after endBranch returns**. “response” in TIMING_NS is therefore an internal response-ready timestamp, not measured HTTP/client latency or even the actual output-emission time.

For setup3 on, endBranch adds **155.396212ms** after that internal timestamp; for setup4 on,148.123954ms; for setup5 on,150.581320ms. The reported drain_seconds values are only approximately28–32 microseconds for these on runs. Source formats that counter before destroying held versions and the Context. Consequently drain_seconds is not cleanup time. The complete timestamp correctly includes that destruction; subtracting the tiny wait from response time or calling it all teardown would hide real cost.

Whole process includes setup/library loading/preparation, the candidate, witness, printing and process finalization. The original executable has no added witness or branch harness. Its6.834s cannot be treated as a matched candidate-service denominator for a paper effect. Source/build/transport time, internal ready time, emitted response and final release must stay distinct in the actual service protocol.

## Native engagement and build composition

This is a genuine integration rather than an assumed LD_PRELOAD hook:

1. The exact producer REPL remains the source of runCommand/processInput and response construction.
2. A private modified libleanrt.a replaces native static io/object runtime objects in the setup executable.
3. A complete private libleanshared.so is linked from the actual SDK Lean/Std/Init/C++ archives and rebuilt runtime objects, with SYMBOLIC binding retained.
4. Both actual binaries have imported gpu_smt hook symbols; disassembly of each lean_st_ref_get calls the helper.
5. Actual setup4 and setup5 process maps contain /tmp/gpu-smt-native-ref-branches-20261016/libleanshared.so and a single helper DSO path.
6. Also-mapped SDK libleanshared_1.so/libleanshared_2.so/libLake_shared.so do not themselves define the inspected ref/task core primitives. Their presence does not negate the demonstrated primary runtime replacement.

These facts establish the real loaded/patched path and executed helper activity. They do not independently attribute every logged operation to a particular DSO or prove interception of arbitrary native globals/FFI.

The build uses official Lean4.27 source and the installed SDK compiler/runtime archives, LLVM19.1.7 libc++ headers with the SDK19.1.2 ABI19 family, host glibc headers and SDK static libc++/libc++abi/unwind. Header-family compatibility is sufficient for this observed successful setup; it is not exact original build identity or evidence that performance composition is matched. The private shared runtime rebuild and source overlay do not alter the original SDK. A matched rebuilt native reference is still required before using original-versus-candidate times as an implementation effect.

No GPU is invoked or needed for this runtime experiment. The only permitted later GPU family remains RTX5090, but the present setup supplies no device-work admission.

## Concrete implementation findings

### Early retirement defect found and repaired in this audit

In v1, deactivate_task_core notified gpu_smt_task_retired **before** releasing dependent task objects and dec_ref(c). A queued/non-running task may have no active execution scope. Its final token could therefore reach zero while its owned closure/dependency destruction still runs. A concurrently waiting endBranch could release Context too early. The awaited witness did not test that scenario.

Root preserved v1 source/patch/build records under implementation-v1 and made a forward repair: a gpu_smt_task_scope branch_cleanup_scope is acquired on entry to deactivate_task_core. It retains the owner and installs that task's context across retirement, dependent/closure destruction and lock reacquisition. The static object and rebuilt shared object/link records succeed. Current source contains that scope, and setup5 exercises the rebuilt real-input path successfully.

Source inspection supports that this fixes the specific early-release ordering identified; setup5 alone does not test cancelled/queued-task interleavings or prove all finalizers/effects safe. Do not present v1 setup3/4 as evidence for v2's repaired concurrent retirement guarantee. No extra standalone cancellation matrix is demanded by this audit: the existing service integration must implement and proportionately exercise its actual supported lifetime.

### First access, not first write

Current resolve_ref clones a prepared cell on its **first access**, including get, and reuses that clone thereafter. The plan's initial read-base-until-first-write description is not literally this implementation. This is a recorded implementation deviation/cost distinction, not evidence of a wrong result. Do not claim that only mutated cells were copied from the43 versions, or infer mutation rate/memory savings from that count.

The actual primitive still acquires an owned value through native ref_get, constructs a native cell, promotes it to MT, and retains the original identity. Native ref operations then run on the resolved cell; ptrEq remains identity of the original refs rather than replacement payload addresses. Candidate-created cells are identified by owner and remain direct on access.

### Known unsupported behavior is real, not resolved by a comment

Unresolved in-flight prepared thunks explicitly return the original thunk at resolve_thunk's unsupported case. The code does not choose a pre-contamination native fallback there. Prepared thunk cloning, ref versioning and task hooks cannot make arbitrary native globals, external objects, promises or OS IO private. Branch-end held-value destruction runs after clearing current, so effects created by unsupported finalizers are not automatically admitted descendants either.

These are limits of the declared supported runtime boundary. The code and implementation-status already disclaim general isolation. They block a full transparent arbitrary-source service claim, not further meaningful supported service implementation. A real fallback must take effect before unsupported state can contaminate another candidate; matching this single accepted proof cannot establish that property.

### Cost risks to measure in the service, not optimize blindly

Each enabled ref access updates a counter, consults the process registry under a global mutex, and may consult the context table under its mutex. Preparation promotes live root refs; first access retains base/value ownership; final release destroys versions. Those are actual new costs, with global contention potentially relevant under concurrency. The150ms-class release interval is already visible in this native source setup.

There is no measured memory result, contention attribution, throughput gain or cost decomposition establishing which implementation change would help. Do not revive narrow kernel tuning or add an arbitrary table/worker grid on this evidence. Complete the intended supported service comparison and use its actual costs for the next decision.

## Failure retention and reproducibility

Retained setup1 off/on fail before verification with libLake_shared.so missing. Setup2 off/on fail before verification when a spawned lean executable cannot find lean_main. Those unsuccessful rows remain visible and cannot be counted as native proof failures or silently removed from setup history. Final library-search/LEAN_SYSROOT repair is a legitimate dependency fix; no original SDK was modified.

Build/source/dependency/link records and raw successful stdout/stderr/terminal/maps are present. Earlier compiler failures and the missing-header/incompatible-default compile attempts also remain in the directory. Root disclosed that some early same-name build logs were overwritten while repairing the dependency/link path. The reviewer cannot reconstruct those overwritten bytes; do not claim a complete raw build-failure archive. A truthful dated failure/deviation summary is appropriate, without rerunning failed builds to manufacture lost provenance.

At initial inspection setup-environment.json recorded library paths but not final LEAN_SYSROOT/PATH or each run's branch-off/maps overrides, and launch.json named only binary/cwd/pid/policy. These effective repairs/overrides need ordinary launch provenance, with reconstructed portions identified honestly. This is a records fix, not a reason to repeat real verification. A setup3 old binary also differs from the later maps-enabled harness; keep that instrumentation change explicit.

No exact matched fleet PSS, exhaustive CPU, service-policy/deadline implementation or repeated throughput record exists yet. A policy string saying300seconds in launch metadata is not, by itself, execution evidence for all native timeout/cancellation paths.

## Next actual boundary

Do not stop at this completed setup or expand it into another correctness-only project. Root should integrate the real supported command path into candidate execution with actual native fallback/effect handling and branch lifetime, preserve native resource/response policy, and prepare a matched rebuilt warm/native comparator plus the declared branch-off component control.

The next real service/performance preflight must use preserved original input and complete response/release accounting, make actual concurrent reuse/resource behavior observable, and include the proportionate controls needed for that implemented supported boundary. Only then can the same plan freeze real commands/cells/repetitions and admit its complete source-cohort comparison. No additional author approval, numerical speed target, agent budget or new infrastructure layer is introduced.

This audit is one review of new evidence, including one concrete repair. It does not restart the plan-review cycle, bless a full collector, certify arbitrary effects or complete the paper. The full Lean-first/SMT/service/RTX5090/four-RQ goal remains intact.

## Record closure within this same audit

Root subsequently added build-failure-history.md. Its explicit account of overwritten early compiler/linker receipts agrees with the disclosure made during review; it does not pretend to recover the missing raw bytes. The reviewer read that record. Current v2 patch also passes reverse dry-run against the actual private source.

At the final read, setup-result.md named launch-environment-reconstructed.json, but that file did not yet exist. Finish that promised honest reconstructed record before publication; do not describe it as an original captured process environment. A setup4 rounding transcription in the root prose was also reported: exact terminal values are6.9324777780566365s(off) and7.132771036005579s(on), already used correctly in this audit's table. These are documentation fixes only, with no new run needed.

### Post-hoc record item closed (same audit, no new run)

The six files were subsequently located at their actual per-run paths: setup3-branch-{off,on}, setup4-branch-{off,on}, and setup5-branch-{off,on}, each named launch-environment-reconstructed.json. All six parse as UTF-8 JSON, identify their post-hoc reconstruction, record LEAN_SYSROOT/PATH prefix and branch/maps overrides, and explicitly leave uncaptured inherited environment unknown. The earlier root-directory lookup did not find them because they live under those run directories. This closes that publication-record item; it does not turn them into contemporaneous environment dumps. Root setup4 prose now rounds the actual times correctly to6.932478/7.132771seconds. No verification was rerun for this closure.
