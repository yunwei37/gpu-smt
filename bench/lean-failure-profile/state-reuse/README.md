# Native tactic-input reuse measurement

Research-only Lean4.9 observation; not part of the Rust service or result cache.
No proof result is substituted. No timeout, memory failure or interrupt is
converted to a reusable strategy failure.

StateReuseMeasure parses each original source with Lean, transforms only outer
native tactic-sequence units for nlinarith, interval_cases, simp_all and norm_num,
and elaborates the original command through Lean's front end. Source coordinates
and children are retained. It does not apply old extractor offsets: 51,198 of
51,199 retained unit spans do not index original source coordinates.

StateReuseProfile observes all goals, ordered typed local declarations and let
values, local instances, native options, tactic syntax/name resolution and Meta
configuration. ExprStructEq compares actual expression structure including binder
annotations. Names have recursive tagged encoding. Environment equality compares complete pinned native Environment values using
environment-equality.cpp:shared subgraphs exit immediately,immutable constructors/
arrays/strings/scalar arrays compare structural data. Distinct closures,refs,
tasks,thunks,external objects and MPZ values remain conservative misses.
Strong references avoid address-reuse aliases;different processes are not mixed.
No candidate environment is modified or canonicalized. Opaque equality and
hidden elaborator state still limit interpretation.
Unsupported metavariables/custom contexts are reported separately.

An observed input match is **not complete replay qualification**. Hidden
elaborator state, fresh-name effects, heartbeat availability and diagnostic replay
still require validation. No constant-count/hash/pretty-goal comparison certifies
equality. Native ordinary errors, normal returns with open goals, logged errors,
resource-limit exceptions and unfinished invocations remain distinct.

The wrapper observes and rethrows the original exception, including runtime
exceptions; it does not catch an operational failure as a successful return.
Capture cost and tactic wall/heartbeats are separate. Measurement allocations
still affect execution and require import controls/native differential tests.
Definition compilation is not a native proof test or performance measurement.

prepare.py selects entire repeated-text groups within original task/header/
statement boundaries and writes unchanged candidate sources. It never inserts
wrappers. The literal statement delimiter is the retained cohort boundary,
not a replacement proof parser. miniF2F: 2,045 sources/503 groups/2,504 occurrences,
2,001 repeats; ProofNet:632 sources/218 groups/804 occurrences,586 repeats.
These counts are not full-state hits or time savings. Syntax-outer coverage
excludes expensive tactics nested inside compound units.

Step0128 compiles definitions;step0130 validates the native observer. Raw failed compiles,
aggregate-support abort and preparation mistakes are retained. After fixed42actual retirement,30controlled elaborations preserve status/raw
diagnostics,match duplicate ordinary failures and distinguish changed target/
context/options. Six actual rejected-source and fifteen mixed real/control
elaborations also preserve all three modes'raw diagnostics/status. A changed
simp environment remains distinct. The unresolved-local case fails before the
observer and does not qualify metavariable support. These are qualification
checks,not population evidence or enabled failure reuse.
Use the existing 48GiB sampled aggregate watchdog/no fixed AS/CPU8–11 contract.
No interval_cases parallel implementation, oracle optimization or new competitor
reproduction is introduced.

## Reproduction and scope

Use the exact matching SDK/project/native library recorded in step0130's command
receipts. Compile Profile with its directory as --root,then compile its generated
C with the SDK leanc using -c -fPIC -DLEAN_EXPORTING. Compile environment-equality.cpp
with the host C++17 compiler and SDK includes;link both objects using that same
C++compiler so GNU container symbols resolve. Import the resulting
libStateReuseProfile.so via --load-dynlib before --run StateReuseMeasure.lean.
The original/import-control/observe modes preserve original code/positions.

run.py owns a finite serial measurement with one-second48GiBaggregate watchdog,
300sper-native-candidate deadline and no fixed AS. Only one collection is launched
by the owning thread. It records every mode/result/raw stream/segment and reaps
the unreaped leader's owned group before starting another segment. Resource
preemptions retry fresh and alone after the ordinary frontier;timeout/resource
attempts are operational,never ordinary tactic failure. CPU8–11are eligibility,
not four busy cores or a four-worker throughput result.

analyze.py joins begin/end events within one process segment and counts only
completed,typed-input ordinary-error repeats against an already completed
producer. It reports capture and action cost separately. Cross-segment equality,
unreached/unsupported/open calls and complete replay qualification stay distinct.
Neither these counts nor the controlled66msduplicate demonstrate a system gain.
Whole-source rejection caching in the Rust engine is a separate existing feature.

The failed whole-environment ShareCommon canonicalization is retained:it used
375.89CPU seconds and22.02GBRSS before the first tactic,and was explicitly
cancelled as an unusable development control. Generic sharing is upstream prior
work: https://raw.githubusercontent.com/leanprover/lean4/v4.9.0-rc1/src/runtime/sharecommon.cpp
The final observer compares existing values and does not use that path.


The population collector uses the plain program argument ack(Lean4.9consumes
option-looking arguments itself). It admits one request over the existing child
stdin,starts its300sclock before ACK,and never lets the native producer run ahead.
Late payloads stay raw and operational;retirement precedes another process.
Cold preparation memory exhaustion belongs to its caller;idle over-budget cache
may retire without assigning a semantic verdict. One fresh exclusive retry
follows the ordinary frontier. Safe test-local128MiBinjection actually killed
four owned workers and exercised two queue-tail retries;full collection remains
48GiB. Normal24real sources x3modesmatch status/raw diagnostics with nominal
one-second sampled own peak9.24GB. NativeREPLfour-sourceblackboxagrees(2accepted/
2rejected),not an all7808certificate.

Before population capture,the frontend is aligned with pinnedREPL/Frontend:
info trees enabled,pre-parse command start,parser/elaborator message order,
terminal command elaboration and original container sourceinfo. The early
self-consistency controls did not by themselves establish this alignment.
The exact native tactic span text is part of the input key. Goal creation indexes
are recorded separately and compared as a replay qualifier;do not conflate
metavariable-generation identity with the target expression or assume it
irrelevant. Local declaration indexes remain part of the strict local context.
Unreached/unsupported/resource/open observations are not zero reusable failures.
The SDK--runmeasurement driver is a diagnostic frontend with compiled Mathlib
provider;its setup/memory and serial execution are not a warm4REPLbaseline or an
end-to-endgain. NativeREPLperformanceconfirmation remains required.

## Analyze completed captures

Use the existing result analysis after the native collector actually retires:

    python3 bench/lean-failure-profile/state-reuse/analyze.py --collection /path/to/run --out /tmp/state-result.json

For one retained process stream, --raw accepts raw.log or raw.log.gz. Plain and
losslessly compressed archived layouts are supported. The selected2677-source
three-mode capture is not a whole7808candidate throughput comparison.

The collection analysis retains each resource attempt and exclusive retry, final
per-mode/dataset outcomes, actual watchdog-kill events, late replies and
unresolved native process exits. It compares source-mode classifications and
unaltered diagnostic lists. Memory, heartbeat, recursion and interruption
diagnostics are conservative exclusions from ordinary-error cost credit, not
proof that a statement is false. Late native completion cannot erase a timeout.
A complete marker with missing planned cells remains incomplete.

Only already completed producers in the same process segment can match.
Input keys with observed outcome changes receive no ordinary-failure cost credit.
Report within-source and cross-source repeats separately. Keys reset at native
process restart; never combine their numeric IDs across segments. No hidden-state,
post-error,heartbeat or diagnostic replay certificate is implied by a match.
Tests include the actual retained positive-control stream and real low-threshold
watchdog injection; existing benchmark-smoke CI discovers them without a new job.

Coverage analysis also reports per-kind capture/completed-action nanoseconds,
input-eligibility reasons,and completed non-operational/non-limit sources with
wrappers but no runtime observation. A source with zero wrapped units is separate
from a wrapped-but-unreached source. Partially reached units inside a source are
not inferred by subtracting runtime calls from Syntax counts:one unit may run
many times,and the current record has no complete per-unit inventory. Open calls
retain unknown action completion;none of these counts certifies failure replay.

## Native failure and continuation

A source that begins but exits without a reply is native_process_failure,not a
logical/tactic rejection. The process group retires before another source starts;
the raw panic/exit remains. Existing timeout/resource causes take precedence.
Pre-source driver/library failures still stop the collector for repair.

After actually retiring a failed run,use the same original input/context with
--resume-from /path/to/failed/run and a new --out directory. The collector refuses
a live prior controller/native worker or changed input/context. It copies raw
prefix bytes,keeps old attempts,continues segment IDs and restores deferred
fresh/solo resource retries. Old files are never edited. An admitted prior
retirement lacking a result is explicitly labelled derived_from_prior_retirement,
with native exit code and unknown elapsed;it is not a fresh native response.

Memory gzip retains its original members and appends a new member with phase
identity. seconds restarts for each phase;terminal seconds_scope describes only
the new controller phase,not the pause or a fresh uninterrupted whole-run clock.
The selected input-match/error-cost study can finish across these declared
phases,but it cannot become an end-to-end speedup by summing convenient clocks.
Actual proofnet-5879panic plus minif2f7 in all3modes qualifies retirement and
continuation after a native exit;all6results retain their raw distinctions.


## Capture durability

Keep population inputs, frozen source/modules and run output under the existing
PVC-backed /workspaces/.agent-state/gpu-smt-captures directory. Container /tmp
is disposable scratch and does not survive Workspace replacement. The root
records a live launch and actual node/CPU context; a prepared recovery directory
does not mean a collector is running. No new storage service or timer is needed.

The2026-10-29 ephemeral-storage eviction lost the unarchived /tmp continuation.
The retained2640-row prefix remains available;at least1273 later observed ledger
entries are currently unavailable and the eviction-time total is unknown.
See step0140 for raw event evidence, exact recovery scope and prepared input.
Do not label missing/evicted data as ordinary tactic failures or pool clocks
across node changes. Rebuild frozen native modules only at the approved resource
point before resuming the finite plan.


## Ordinary failure replay boundary

The pinned dispatcher can rethrow an ordinary exception with its failed
post-state. Our runtime-exception observer does not itself roll back that state.
An observed input match and identical exception text do not certify replay.
Full snapshots with heartbeat debit already exist upstream,with explicitly
approximate overhead accounting. See [source audit and unexecuted control](../../../docs/tmp/build-and-evaluate/step-0141-20261029T182000+0000/experiment-001/source-analysis.md).
No producer snapshot may be transplanted across candidates without compatible
entry state/identity mapping. Complete the selected measurement before claiming
failure-reuse coverage or benefit;this control is not workload evidence.
