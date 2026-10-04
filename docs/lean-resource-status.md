# Lean acceleration delivery and resources — 2026-10-04

The previous worker committed its draft as `00400a8` before takeover. No staged
or unstaged changes were present when Codex inspected `research/lean-acceleration`.
The draft's quantitative/causal claims required correction; its history is kept.
The independent `/tmp/clean_timings.sh` run finished at 09:51 UTC with
`CLEAN_DONE`. All benchmark processes had exited at takeover; it was not rerun.

Raw records, selected commands and provenance are now retained under
`artifacts/lean-2026-10-04`. The large original export inputs, checkouts and
builds remain under `/tmp/lean-kernel-arena` on the owning workspace.

The selected next implementation is persistent official CPU replay, described in
`docs/lean-acceleration-plan.md`. It does not depend on GPU access.
Completed: repeated small-fixture trials, paired normal/skip-check frontend
profiles, and exact official decision parity on 215 fixtures (197 definitive
expectations, 18 either). Heavy-pass times were excluded from speedup claims
because sampled memory pressure changed substantially. See the continuation
report for complete validation and timing results.

GPU execution is not requested for the previous whole-checker sketch: no such
prototype entrypoint exists. No GPU acceleration result is claimed. Once a
specific hot operation/subset has a CPU reference and ready GPU executable,
coordinate a bounded job through the existing Kubernetes NVIDIA device-plugin
and runtime. The job needs an assigned GPU and matching driver libraries, with
this Workspace/PVC and other projects' processes preserved. Host sysfs/proc/dmem
visibility is insufficient evidence of assignment. Do not manually probe or add
host devices or modify production model placement.
