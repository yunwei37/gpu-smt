# E032 follow-up: existing-cache and exact-query screening

This is read-only hypothesis screening from already acquired full real data,
not a new native benchmark or an admitted proxy-only paper result. All four
RQs and the full Lean/SMT/end-to-end/device/system/paper goal stay intact.

The installed Lean4.27 Meta cache already contains permanent and transient
definitional-equality maps, with Expr/config keys. ExprDefEq chooses transient
state for metavariables or nonstandard unfolding and validates assignments;
typeclass synthesis already caches by local instances/type/pending depth.
Relevant source: Meta/Basic.lean 320-386, 647-667; Meta/ExprDefEq.lean 2060-2101,
2163-2178; Meta/SynthInstance.lean 770-806. This rejects blind addition of a
second generic Meta cache. The 35% inclusive path does not measure cache hits
or missed reuse. Meta query arguments are absent from the CPU callchain data.

The completed Fast/hybrid reference profile contains a closed502,329,013byte
oracle.jsonl alongside all29,750 original inputs. Its Instrument.lean logs
each wrapped oracle's exact maxVar/hyps and successful certificate or error.
Native.lean requestLine uses the same integer-coefficient protocol. Start and
elapsed fields use IO.monoNanosNow around the oracle, before telemetry emission.
Fast-path metadata records share the file and must not be counted as LP queries.

Hypothesis to screen: exact repeated numeric oracle problems may offer shared
work worth measuring in a later implemented system. Analyze the entire closed
archive, preserving all problem fields and coefficient precision; no selected
proofs, row/variable reorder or mathematical normalization. Count success and
failure, exact source associations, structural repeats, and prior-completed
successful occurrences. Preserve all grouped/record-level derived evidence.

Counts and logged call intervals are not actual cache hits, performance gains,
CPU/wall decomposition, observed GPU readiness, live LLM arrival traces or a
whole-system acceptance result. Their route differs from E032's original
compiled arithmetic. Worker identity/publication delay and telemetry omissions
remain limits. The source code catches telemetry errors, so archive coverage
does not establish complete oracle/Meta coverage.

Use the result to choose or reject subsequent implementation, against existing
caches and strong CPU baselines. Do not re-open the failed scalar GPU/placement/
SMT-prefix constructors or launch a cache/solver/GPU tuning variant on a count
alone. No active capture, SDK, logger, deadline, resource setting or writer is
changed. Root implements and analyzes personally; independent audit stays open.
