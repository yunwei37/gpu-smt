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
annotations. Names have recursive tagged encoding. Environment equality is a
conservative process-local identity with strong references including opaque
extensions; different environment objects/processes are not declared equal.
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

Step0128 compiles both definitions with the matching SDK. Raw failed compiles,
aggregate-support abort and preparation mistakes are retained. Native controls
and actual state/cost capture follow the sole fixed42 collection's retirement.
Use the existing 48GiB sampled aggregate watchdog/no fixed AS/CPU8–11 contract.
No interval_cases parallel implementation, oracle optimization or new competitor
reproduction is introduced.
