# Robust GPU support-search prototype
Historical CPU stage remains1.34668x. Admitted GPU mechanisms have completed without a valid speedup; corrected CPU pairs remain active. Final decision is best(CPU, GPU)>1.5x on the frozen 1000 sources. No CPU-only project closure.

The initial GPU target omitted NVIDIA runtimeClass and failed before requests; the corrected upstream target initializes CUDA device0/RTX5090 with the same 48GiB cap. The HTTP proxy returned a NaN serialization error for the first real LP and hung on a later retrieval; the invalid attempt was stopped, its remote request cancelled, and evidence retained. It is not performance evidence.

The current backend uses official pinned protobuf definitions and blocking WaitForCompletion/GetResult/DeleteResult on gRPC5001, without HTTP result polling. No cuOpt GPU package is installed in the source Workspace. The first real scaled certificate LP (73 rows,231 columns,1385 nonzeros) returns PDLP_OPTIMAL,66 iterations,0.104 seconds reported solver time; exact Rust repair/verification accepts its returned support. This is interface/mechanism qualification, not end-to-end acceleration.

Implementation: cheap pinned CPU FP search remains a fast filter. At an exact-search fallback, robust support search uses either matched HiGHS1.15.1 or GPU cuOpt PDLP with crossover. The later separately failed direct-feasibility model enabled infeasibility detection. Direct AST mode can decline to strong Lean fallback; the native fallback retains exact tiered search on all misses. GPU floating values never establish a proof. Both CPU and GPU variants use the same policy. Independent candidate calls can issue concurrent numeric jobs; there is no artificial batch waiting. The upstream single-GPU server's actual overlap/queueing must be measured, not presumed.

New Lean modules clone the pinned native/Fast/cached-product route into an experiment namespace, use per-call child lifecycles and wait through actual exit, and keep the selected certificate Lean check. The old primary binaries/data and running Lean4.9 prefix experiment are retained.

A 24-source native preflight was launched. An initial lifecycle output-directory collision occurred after its reference cell, before either prototype cell; the failed orchestration is preserved and a corrected separate-backend-artifact run was launched. No invalid cell is treated as fast. Full1000 admission requires a valid matched native preflight with actual backend engagement, matching verification verdicts, and measured benefit. Then compare on the same fixed1000 and report individual heavy tails, using the added native per-source task timing side channel. Reference/GPU whole clocks retain packing, IPC, queue, Lean checking, fallback and retirement; per-cell host proxy startup/retirement are added explicitly. Warm upstream server startup is reported separately and cannot be silently excluded from a cold-system claim.

Self-review: no subagent or OMP. Exact support repair is the existing upstream method and verifier; source namespace and process-lifecycle integration must qualify on real native sources. Current build succeeds, first real numeric GPU support qualifies, native preflight is pending. This is experimental code, not a completed GPU result or independent audit.


## Phase-I correction and actual batches
Pure feasibility PDLP stalled on an82x152/968-nonzero LP known to have no certificate; a single server worker then blocked three other candidate requests. The interrupted native capture and all four cancellations are retained. CPU reference24/24 and HiGHS control24/24 completed; their clocks alone are not a paired GPU result.

The GPU model now appends positive/negative artificial slack for each row, minimizes total slack, and is always feasible/bounded below. PDLP need not prove the original certificate system infeasible. GPU support remains untrusted even when phase-I objective is nonzero. Original coefficient coordinates are sliced back from each independent component and undergo unchanged exact repair/verification; a miss triggers native fallback.

Actual ready-queue batching drains only requests already waiting when the previous solve completes. There is no artificial batch timer. Eight real previously-exact-fallback requests produced four GPU batches of sizes1,3,1,3, all PDLP_OPTIMAL, with87/203/52/133 iterations and reported shared solve times0.097/0.055/0.026/0.079 seconds. Sum batch solve time once per unique batch, not once per member. Four of five original positive requests repair exactly; index4 declines and must be recovered by Lean fallback. Three original no-certificate requests decline. A pre-readiness zero-engagement smoke is preserved as invalid, not counted. Numeric certificate selection equivalence is not claimed.

A fresh24-source native GPU preflight is active against the already-complete same-source native reference. The final full1000 comparison and heavy-tail analysis remain pending. This repair is a change of GPU formulation on demonstrated infeasibility/head-of-line behavior, not a grid of speculative kernel variants.

## Completed phase-I full capture, 2026-10-18
The preceding pending/preflight descriptions are historical. First full1000GPUattempts finished3374.147306631s with8operationalfailures; the target was retired and CPU controls continue. [Completed result](../full1000-phase1/result-review.md). Generic iteration fields were not PDLP loop counters: actual late-job trace reaches22.86Mloops/443.789s then crossover0.00s. The next draft uses originalfeasibility, upstream infeasibility detection/firstprimalfeasible and defaultcrossoverfalse; it is not installed in the frozen trial and not yet qualified. FinalGPUdecisionremainsopen.

## Direct-feasibility repair rejected, 2026-10-18
Current source is retained experimental failure code, not an admitted final GPUvariant. First four archivedrealrequests alltimeout300.10s, includingtwopositive. Rootstoppedremainingpartialprobe, preserved8numericrecords/5closedcaseobservations, anddeletedtarget. No native24/newfull1000starts. [Failure andlimits](direct-feasibility-result-review.md). MatchedCPUcontrolscontinue; finalbestCPU/GPUdispositionpending.

## Current corrected-header qualification
Actual module lookup exposed stacked legacy/new elaborators, and a source-only
launcher correction now selects a single intended family. Native24 qualification
preserves complete full responses with native46.054s, originalCPUoracle37.513s,
robustHiGHS56.828s. No newHiGHSfull is admitted. Current backend restores the
measured phase-I/crossover model with the owner-EOF cancellation already written,
records full matrices/jobIDs and treats any finite primal only as an untrusted
support subject to exactrepair/Leanchecking. Original-feasibility remains closed.
[Corrected GPU preflight plan](arithmetic-header-corrected-gpu-preflight-plan.md)
uses client plus server CPUeligibility0--3 for fair capacity, a fresh server
without syntheticwarmup, and separate startup/retirement accounting. Existing
legacyfull controls are now closed and their raw data preserved. Prefix collection remains unchanged. CorrectedGPU24 and three corrected fullCPU pairs are active; no correctedGPUresult yet.

## Terminal corrected GPU qualification, 2026-10-18T02:19Z
Family-only imports and owner cancellation still take630.367s for24attempts,
16complete/8operational vs46.054s/24complete reference. Actual104singleton
GPUbatches/106calls engage the backend, two abandonedjobs cancel; no newfullGPU
matrix or numericgrid follows. All serverthreads actuallypermitCPU0--3.
[Full raw native review](../header-correction-preflight24/result-review.md).
GPUstdout/exactlifecycle stopwatches are missing from a Windowsarchiveoverflow;
clientmodels/replies/batchevents/Leanresponses remain complete. Fresh cleanup
confirms no ownJob/Pod/sourcechildren, otherGPUWorkspaceRunning/labReady.
ThethreecorrectedCPUfullpairs now determine remaining matchedbestvalid threshold.
No independent audit or paper acceptance is claimed.
