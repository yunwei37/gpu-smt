# Lean acceleration delivery and resources — 2026-10-04

The previous worker committed its draft as `00400a8` before takeover. No staged
or unstaged changes were present when Codex inspected `research/lean-acceleration`.
The draft's quantitative/causal claims required correction; its history is kept.
The independent `/tmp/clean_timings.sh` run finished at 09:51 UTC with
`CLEAN_DONE`. All benchmark processes had exited at takeover; it was not rerun.

Raw records, selected commands and provenance are now retained under
`artifacts/lean-2026-10-04`. The large original export inputs, checkouts and
builds remain under `/tmp/lean-kernel-arena` on the owning workspace.

The first continuation implementation was persistent official CPU replay, described in
`docs/lean-acceleration-plan.md`. It does not depend on GPU access.
Completed: repeated small-fixture trials, paired normal/skip-check frontend
profiles, and exact official decision parity on 215 fixtures (197 definitive
expectations, 18 either). Heavy-pass times were excluded from speedup claims
because sampled memory pressure changed substantially. See the continuation
report for complete validation and timing results.

The following continuation is validated in this owning branch:

- Real Mathlib source replay: 52 complete proofs plus controlled reject/sorry
  variants, 1404 decisions in nine complete runs. Eight original full runs and
  59 interrupted responses were preserved; only the missing full fresh-command
  pass was rerun separately. Established REPL backtracking supplies the warm
  baseline. Full timing variation, source contexts and state-lifetime memory
  failure are retained in `artifacts/lean-state-2026-10-04`.
- Real VeruSAGE run: 100 tasks, 57 passing, 37 failures before SMT and six reaching
  SMT; 156 sessions, 440 queries. All raw sources/logs/traces are hash-verified
  in a repository archive. Scope/history ablations explain the 31-session
  prefix-pool fidelity failure. No prefix-pool serving speedup is validated.
- Actual GPU execution: Job `coder/gpu-smt-lean-dag-5090-20261004`, Pod
  `gpu-smt-lean-dag-5090-20261004-npq9w`, node lab, assigned RTX 5090 through the
  existing NVIDIA plugin/runtime. Runtime evidence records exit 0 and seven
  arrays matching official Lean on all 6,132,277 expression nodes. Resident
  metadata execution is 0.853 ms median; this does not verify proof types or
  establish whole Lean acceleration. Raw JSON/runtime, exact input/reference,
  executable snapshot, PTX and hashes are retained. No GB300 computation ran.

Outer infrastructure coordination owns cleanup of the temporary GPU Job. The
standard-dev Workspace was not changed to request a GPU, and the same owning
PVC/branch/history are preserved. No manual host-device probing/mounting,
production model change or interruption of another project was required.

Reports: `results/2026-10-04-lean-mathlib-state-reuse.md`,
`results/2026-10-04-lean-gpu-dag.md`, and
`results/2026-10-04-verusage-real-traces.md`. This is a meaningful research
checkpoint; actual candidate streams, version-aligned broader VeruSAGE coverage,
and integration of useful resident GPU operations into a real checker remain
unfinished. See the branch's Git history for delivery state and checkpoint ID.
