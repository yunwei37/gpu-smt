# Existing-error continuation control — root plan self-review

## Evidence and question

The complete ProofNet native/SHRED HTTP baseline is negative: 356.37/373.22s,
413 genuine completions each, 20 rejected-to-incomplete changes. Of 1,653
cache captures, 1,333 come from ultimately noncomplete sources. Recorded
generation wall sums 801.75s, overlapping across requests and excluding
some failures. This does not establish an error was visible at tactic entry.

Test one narrow hypothesis: can a last supported tactic skip expensive
continuation when Lean's current message log already contains an error,
without changing the observed native verification outcomes?
Do not simultaneously change recovery, compilation, cache keys, threads,
buffers or LP solvers. Existing Lean no-recovery APIs are prior features,
not a contribution. This is not the closed E038 runtime-branch route.

## Real preflight and resources

Choose from the closed 5,952 native ProofNet records: every genuinely complete
source, every incomplete source, the operational source, first original32,
all literal unavailable-source placeholders, and the three longest native-body
rejected sources. Preserve original index order and record actual unique count.
Selection provides success/failure and expensive-work coverage, not a new
population result or a subset chosen after this control's speed is known.

Run fresh native then guard through unchanged official Kimina app/SDK,
same 4.9 SDK/compiled Mathlib/kernel-checking REPL, eight outstanding sources,
four eligible CPUs16–19,48GiB and upstream300s timeout. Real original parser/
wrapper work and every preparation/queue/check/fallback/retirement cost
stay charged. The native control is fresh, not rescaled from an old run.
All source errors, sorry cases and operational failures remain.

Only the supported final tactic receives the guard; unsupported syntax and
registered source boundaries take original native execution. It reads actual
Core message state and emits prior_errors/skipped plus elapsed wall; it does
not introduce a deadline, solver or permission rule. Output/error messages
differ, so no full protocol transparency is claimed.

## Falsifiable decision

If prior_errors is rare or charged preflight has no useful gain, do not start
a full matrix or another suppression variant from this signal.
Real gain plus retained native verification outcomes can admit full-source
measurement. Accepted/incomplete/rejected/operational changes are exposed,
not masked. No local result redefines the original1000 CPU/GPU continuation
criterion or closes the project/hourly task.

This diagnostic is not OSDI novelty or a new cache system. Original four
RQs/Lean+SMT/native-behavior obligations remain. Root only, self-review only.
Do not alter any active source/build/collector; this module has its own
ordinary build directory in the same owning Workspace.
