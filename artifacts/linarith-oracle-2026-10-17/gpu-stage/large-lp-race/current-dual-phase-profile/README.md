# Current two-sided oracle phase profile
RQ4, experiment E1066. Sole executor/reviewer is the root thread.

[Plan](plan.md), [plan self-review](plan-self-review.md), [request coverage repair](request-coverage-repair.md), [closed 64-source result](qualification-result-review.md), [reproducible qualification analyzer](analyze-qualification.py), and [machine-readable qualification](request-qualification-analysis.json).

The completed qualification archives retain uninstrumented CPU, original diagnostic and request-complete diagnostic observations. Six private build stages succeeded after the retained root-path failure. Exact original source/result fidelity holds. The additional request metadata covers both successful and failed direct calls plus native fallback requests. It is coefficient-space metadata, not automatically the scaled floating model.

The full thousand-source diagnostic pair has completed through the retained driver and private source tree, using eight static queues, four eligible CPUs and 48GiB per-process address space. See [complete result and scope](full1000-result-review.md), [paired analysis](full1000-paired-phase-analysis.json), and [reproducer](analyze-paired-phases.py). Its logging/scanning/compression costs belong to its own clocks. It does not replace primary performance pairs or close GPU research. Original full-population and prefix acquisitions stay untouched.

## Accounting boundary
Lean phase CPU and elapsed intervals overlap when nested. Native numerical roundtrip includes IPC and child waits; direct arithmetic reply timers are elapsed, not CPU. Parsed HiGHS timers are a narrower solver boundary. Cancelled worker internal compute is unknown unless explicitly sampled. No sum or interval-union is silently treated as a removable end-to-end fraction. Any zero-cost model states its fixed-path/scheduling assumptions.

All review is self-review. No subagents, OMP or native Codex sessions are used.

Large raw gzip files in full1000-raw use numbered byte chunks described by each raw-archive-manifest.json. Concatenating numeric parts restores the exact original stream. analyze-current-phases.py reads these parts directly. Analyzers prefer the published artifact directories. No primary ratio or strict GPU impossibility follows from diagnostic envelope models.
