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
