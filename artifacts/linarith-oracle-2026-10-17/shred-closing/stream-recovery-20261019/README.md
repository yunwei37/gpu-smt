# Declared Kimina transport and logging repair

This directory preserves an actual interrupted miniF2F collector and the
minimal application repair used by subsequent fresh captures. It does not
claim a Lean/GPU speedup or an unchanged upstream application.

* [Plan and source/metric scope](plan.md)
* [Root plan self-review](plan-review.md)
* [Actual stalled Python stack](stalled-python-stack.txt)
* [Stopped owner scope](interrupted-owner-processes.json) and [retirement](stop-receipt.json)
* [Closed partial summary](interrupted-summary.json) and [lossless archival](interrupted-raw-archive.json)
* [Exact dependency patch](kimina-transport-logging.patch), [source receipt](patch-receipt.json), [MIT license](kimina-LICENSE)
* Before: [repl](repl-before.py), [logger](logger-before.py), [HTTP handler](check-before.py)
* Executed: [repl](repl-executed.py), [logger](logger-executed.py), [package versions](dependency-versions.json)
* [Exact protocol check](framing-check-executed.py) and [result](framing-check.log)
* [Real source selection](failure-source-selection.json), [qualification command](real-preflight-executed.py) and [launch](real-preflight-launch.json)

The retained dependency lives at
/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d.
It is an archive without Git metadata; fb2393d is its recorded archive pin,
not a newly verified checkout revision. From that existing directory, apply
the patch using:

    patch -p1 < /workspaces/repository/artifacts/linarith-oracle-2026-10-17/shred-closing/stream-recovery-20261019/kimina-transport-logging.patch

Only apply when the before-source versions match. The current retained
dependency already has the patch; do not apply it twice or patch a running
collector.

Run the protocol check using the existing dependency's .venv/bin/python.
Run the real qualification script with that same Python from the owning
Workspace. It writes a fresh real-preflight directory and refuses overwrites.
Its terminal files, rather than a live PID or this README, establish completion.
The frozen executed snapshots and original sources make the declared mutation
reviewable; no dependency installer, persistent helper or new service is added.
