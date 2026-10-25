# Step0017 — native source-file backend on the Rust resource engine

Previous turn progressed:502a4d3/5e34b29retain source-memory attribution,
measurement provenance and passing actual native CI. Initial Narrative/fourRQ
and four continuing directions remain open. Root thread only; CPUoracle frozen.

## EXPERIMENT_GATE

This is a prerequisite implementation node for original code-verification
workloads, not a new performance experiment. The legacy Verina driver retains
the superseded fixed24GiBAS/max2resourcepoint. A reusable stock Lean CLI backend
will pass the exact full source through --stdin/--json under the existing Rust
CPU/RSS admission, cancellation and retirement path. There is no need to port
every new Lean toolchain's REPL or retain a second Python resource scheduler.

Keep CLI backend identity distinct from REPL/prepared identities. Retain actual
stdout/stderr/exit and diagnostic JSON; explicit sorry stays incomplete, native
errors rejected, transport/unknown/signal faults operational. An empty successful
native diagnostic stream is valid; unknown non-JSON output cannot establish
acceptance. No outputs/modules/files are written into the source project.
This is stock frontend checking, not an axiom audit of imported dependencies.

Tests cover protocol/status distinctions and actual native Lean differential,
timeout/cancellation retirement in CI. Workspace builds only while existing
full7808owner remains; do not run a second local proof collection.48GiB total,
no new quotas or host changes. Real full-workload throughput remains pending.

## WRITE_GATE

Document the public native CLI backend and optional executable choice without
claiming Kimina/REPL output parity, Mathlib throughput or source-model accuracy.
Retain all failed attempts and final code/test evidence.

## REVIEW_GATE

Root self-review of native output, ownership, identity, cancellation and resource
path. Never independent audit. Goal stays active; no closure/performance gate.

## Implementation result


Own engine implementation node, not a repeated baseline system or new full
collection. NativeLean sends the byte-exact full source to the pinned stock
Lean --json --stdin; the same Rust process ownership/CPU/RSS admission/watchdog/
retry applies. No source or module file is emitted in the original project.
No per-workerAS/memory/trust/heartbeat overrides added.

The unmodified fresh/prepared REPL identities and original native7808group
remain. Source frontend response keeps exit/stdout/labelledstderr/messages;
unknown output is operational, sorry is incomplete. Stdin path semantics differ
from original filename invocation, as documented in docs/api.md. Neither native
exit0 nor the adapter audits imported axioms or source filesystem effects.

validation-20261025T124554 retains the initial Clippy identical-branches failure;
the consecutive condition was combined. validation-20261025T124625 passes all
six checks:format,formatcheck,Clippy,ordinary tests,docs,CLIhelp.34ordinary tests
pass,3real native tests intentionally ignored locally while the retained full
collection owns the slot. Actual pinned native CI must still qualify the new
backend and its raw frontend accept/reject/admitted/info/timeout/retirement cases.

Root self-review only. CLIselection is additive (--lean alternative to --repl);
prepared import parent remains REPL-specific. The shared current-RSS helper
moves existing observation code without changing its meaning. New backend is
roughly200lines with no new dependency/resource-controller layer.
No whole-Mathlib performance, new throughput benefit, trained source predictor,
independent audit or completed systems contribution follows from these checks.
