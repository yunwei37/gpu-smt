# Actual retained Lean4.9 adapter build

The reusable engine module compiles against the existing miniF2F native
Lean4.9.0-rc1/REPL API. The engine-owned C host and generated Lean C compile,
and the complete prepared-host links successfully against a private archive
of the unchanged retained REPL object files. No dependency archive/source/bin
in the active project is written. The 11 input objects retain their original
size/mtime. Source snapshot/copyright headers and exact commands are retained.

The normal native/lean/build.py path builds the dependency's static facet.
This diagnostic instead reads already-built objects into a private /tmp archive
to avoid mutating the project currently used by the sole original collection.
It is a recorded diagnostic build, not another supported installation mode.
The frozen CPU oracle and its implementation are not changed or used as an
acceleration method; this only embeds the existing plain native REPL dependency.

Both build drivers sample their own tree plus the verified existing research
tree every1s. Total sampled peaks are13,896,527,872bytes (module compilation)
and25,148,940,288bytes (compile/link commands), below48GiB. No fixed AS cap
was installed, and no pressure kill was triggered; only the new build would be aborted
on aggregate pressure to preserve the live collection's frozen old settings.
Samples are not a kernel hard quota or an isolated performance measurement.
CPU eligibility stays8–11. Logs/receipts retain preparation costs.

The resulting /tmp/gpu-smt-lean49-compile-20261025/prepared-host is **not executed**.
No Mathlib import-parent engagement, native accepted-set parity,42resource
rerun or throughput result follows from linking. Execute the actual qualification
only after the existing original7808group has retired; first isolate the42old
resource failures at the new uncapped48GiB point. Do not pool its clocks with
the old2worker/24GiB-AS capture.
