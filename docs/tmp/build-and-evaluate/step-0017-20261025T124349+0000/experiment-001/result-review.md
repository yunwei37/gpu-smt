# Native source frontend backend

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
