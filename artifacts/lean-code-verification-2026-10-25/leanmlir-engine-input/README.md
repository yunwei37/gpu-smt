# Original lean-mlir engine input

One complete original module at b8c4a771319a044854a4bbb49b8821381ef86ff8,
including all definitions, proofs, options and scoped syntax. No theorem or
tactic splitting, no admission/error removal, no source rewrite. All-mode,
reuse=false, unchanged engine default timeout (300s). These are prepared bytes,
not an executed native verification, profile, accepted theorem count or speedup.

Use the pinned nightly-2025-12-01 SDK and original root manifest/native import
paths; its correct Cli revision differs from the LeanMLIR subproject.
The stock frontend backend runs stdin, which has a different diagnostic/module
filename; compare it with original-path CLI before interpreting native outcomes.
The original root --tstack=400000 setting must be retained in both sides.
Profiler runs must preserve their own diagnostic settings/output/overhead,
rather than being pooled with uninstrumented performance clocks.

The retained original7808 candidate group keeps the only acquisition slot.
Do not start this input alongside it. New runs use the Rust dynamic48GiB
actual-RSS/CPU8-11 resource path without fixed per-process AS limits. No extra
AI agent, service, scheduler, CPU oracle or comparison system is invoked.
