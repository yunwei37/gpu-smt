# Step0050 — retire owned attempts on handled CLI termination

BUILD_AND_EVALUATE; root-only implementation and self-review.
Previous goal turn is progress:Step0049published one supporting sensitivity
controlcdaae00,not a native performance answer. This step returns to executable
engine work rather than another join/report variant. Goal remains active.

## EXPERIMENT_GATE

Entry reads currentuser-instruction/questions,architecture/API,CONTRIBUTING,
CLI/library/native shutdown code and nearby subprocess tests. Allfour user
directions remain;no delegation/native AI session/second collection.
Use auto-research-orchestrator and oss-change-workflow. FixedRQ2resource
dependency and allowedscope are in the [plan](experiment-001/plan.md) and
[plan self-review](experiment-001/plan-review.md).

### Source mechanism / real reproduction node
serve installs only ctrl_c;check/measure have no lifecycle signal handling.
SIGTERM bypasses Rust Drop and Engine::shutdown. Actual idle executable exits
-15onSIGTERM,with0backend children. This is measured default termination,not
an experiment that deliberately leaves a live verifier orphaned.
Missing resource retirement is a concrete implementation defect,not a proposed
new scheduling/semantic constraint.

### Implementation / failure repair node
InstallSIGTERM before candidate launch and select it withSIGINT. serve uses
existing gracefulHTTPshutdown;inputmodes await engine shutdown and return an
interruption error. Existinginput errors also await cleanup before exit.
The signal future must own itsstream for the server's static shutdown future;
initialE0373compilefailure/source are retained,then corrected with asyncmove.

A held-body protocol fixture then verifies all3CLI modes and checkSIGINT.
Idle-input testing reproduces a separate shutdown hang:TokioRuntimeDrop waits
for a blockingstdinread to getEOF. Await native retirement first,then use
runtime.shutdown_background instead of waiting for a cancelled input reader.
No native timeout,resource limit,new flag or shutdown deadline is introduced.

ConcurrentCLItesting exposes a test PID-file creation/write race. Publish full
PID readiness by atomicrename;retain failedtest/source. Cleanup inspection
finds0still-live matching fixture processes. A Clippy collapsibleif failure is
also retained and repaired without suppressions. These failures do not become
native performance or GPU conclusions.

### Final validation / resource node
Final7CLItests and51workspaceordinarytests pass;0failed,4realnativecases ignored.
fmt,Clippy-Dwarnings and rustdoc-Dwarnings pass. Actual process tests cover
SIGTERM/SIGINT,held-child retirement,HTTPdrain,nonzeroinput interruption,
no fabricatedcompletecapture,and idleinputexit withoutEOF.
No actual Lean proof is started. The native source/transport is unchanged;
realMathlib4.9lifecycle/population qualification still needs actual collection.
Combined development+oldfull sampledpeak14,982,926,336B<48GiB,0pressure/errors,
CPU10–11. Sampling is not a kernelquota. Originalrelease/host is never rebuilt.
[Result self-review](experiment-001/result-review.md).

### Actual fullpair node
06:00UTC exactPID408739/birth140695363is live;4533physicalattemptrecords,
nativecapture0bytes,preparedcell not terminal. This is journal progress,
not completedconsumerrows,acceptedset or throughput. Source42659a8,release
mtime and inputs/resources remain original. No restart or hotpatch.

## WRITE_GATE

Only API/architecture lifecycle paragraphs change. QuickStart,publicrequest
schema,resourcepoint,dependencies,workflows,defaultnativeverification and
paper/fourRQlines remain unchanged. Publication does not change existing live
runtime. Papercompile/fullwriting/milestonereview skip because no paper source
changes and fullRQevidence remains missing. Resource primitives remain prior
techniques,not novel contributions.

## REVIEW_GATE

[Outer root self-audit](outer-audit-20261026T055030+0000.md) checks measureddefect vs inference,
signal installation,retirement-before-runtime-stop,partial-outputscope,
fixturefailures,resourceownership and codegrowth. No independent audit or
new nativeparity/performance claim. User prohibition overrides reviewer
delegation. The testcohort is controlledprocesses,not a replacement benchmark.

## Meta-review / routing

Direction unchanged:make the requested reusableengine work before using it for
native workload research. A real lifecycle bug merits a boundedrepair. It does
not itself answerRQ2or replace workloadnovelty. Do not add more signal variants,
supervisors,limits or abstractions absent an observed fault.
main.rs net+31lines mostly existingbranchmovement plus handling;219testlines
cover4active/2idlecross-processboundarycases and cleanup in the existing suite.
No newtestframework or executor abstraction. Ownartifact retains each failed/
successful attempt and source without changing foreigndirtyfiles.
DailyOct26maintenance already exists. No newskill/rule/scheduler is added.

Continue the sole preservedfullpair to actual terminal,then originallean-mlir
body/profile and original23/48qualification plus42isolatedreruns in their
declared order/resourcepoint. No minute wait or repeated memoryjoin. Independent
scientificaudit,wholepopulationbenefit,Mathlibqualification and paper remain
open;allfourcontinuousdirectionsstay active.

## Publication boundary

Only CLIcode/tests,API/architectureparagraphs,and this complete step/artifact
are staged onmain. Commit/push output is the actual publication evidence.
No deployment/release/PR is created. ExistingCI may execute the ordinary/native
contracts,but no pendingCI is called a pass. Nativeperformanceclaims wait for
their own complete planned measurements.

Publication check note:the initial whole-index whitespace check reports native
Cargo log blank/trailing whitespace. Preserve those raw bytes. Source/docs/
scripts pass the check with only raw*.log files excluded;no whitespace policy,
attribute or output cleanup is introduced. This is not a code/test failure.
