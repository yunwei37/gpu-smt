# E1078 — formal-version oracle integration and real qualification

## Admission and user authority
Root-thread-only implementation under the user's Lean-first, real benchmark,
strong-baseline and CPU/GPU continuation instructions. Research remains
BOOTSTRAP/unfrozen; the Initial Narrative and all four RQs are unchanged.
RQ4: After preparation reuse, when does heterogeneous execution improve complete
verification over the strongest measured CPU path?

This adapter is a dependency of the full-workload RQ4 experiment, with zero
standalone scientific contribution. Goedel4.27 gains do not establish that the
same mechanism runs on the actual miniF2F/ProofNet Lean4.9.0-rc1 population.
The current strongest useful action while E1077 runs is to make that actual
path executable rather than another solver/kernel/parameter sweep. Positive
qualification admits matched complete-population evaluation; mismatch or no
engagement means fix/retain that technical result, no performance claim.

## Fixed setup and comparison
Retain original4.9 SDK, Mathlib, native compiled linarith library, kernel-checking
REPL and SHRED client. Upstream4.9 default is simplexAlgorithm (verified
Verification.lean), not Fourier–Motzkin. Add a version-specific adapter shared by
all three modes: stock (no interception), native preprocessing with the very same
external numerical backend, and Power AST export/native certificate checking.
The native-only mode is a component control, not a fully ported4.27 Fast baseline.
Unsupported direct paths restore tactic state and try native preprocessing;
that also failing restores and delegates to unchanged upstream tactic.
Custom tactic configurations remain upstream. Natural exponents over Real/Rat
are supported; this is not Nat-carrier support or a new GPU implementation.

Private .olean/.so build links the existing native Mathlib library. Keep all
private Rust binaries frozen from E1074; no Rust rebuild, GPU service or existing
collector mutation. CPU12–15/four CPUs, four-command native batch width, original
48GiB/300s upstream client defaults, cores0; shared host disclosed.
One private CPU HiGHS support process per condition; setup, imports, commands,
fallback and normal quit are all timed. Trace-enabled qualification clocks
are descriptive only, not a general benchmark speedup.

## Workload and completion
Two complete original32-candidate groups, selected before this adapter's timing:
among groups with no previous operational/incomplete outcomes, maximize the
number of previously complete sources containing a linarith/nlinarith token;
tie earliest original group. miniF2F3168–3199 (32complete), ProofNet256–287
(12complete20rejected). All64 remain, including failures; the selection is
deliberately engagement-biased and cannot measure population performance.
No source/tactic rewrite. Only add the adapter import to the prepared header,
blank original header in body preserving line positions. All conditions share
the same extra import and compiled library.

Run stock→native→direct. Completion is all64 originals/condition, normal native
quit, every raw request/response retained; per-source verdict and all non-message
JSON compared, warnings separately. Require actual direct checked events and
native-only checked events. A whole-source complete includes native kernel
checking. Auxiliary trace cert-return events alone do not imply acceptance.
Any operational loss or verdict difference is retained, no transparent-speedup
claim. No full matrix until this actual path qualifies.

Command: pinned Kimina venv Python qualify.py (this directory). Raw output
qualify-{stock,native,direct}/, terminal.json and source input here; runtime
private build under /tmp/gpu-smt-linarith-oracle-20261017/formal-oracle-4.9.
Review is self-review only; independent audit is unavailable by user instruction.
