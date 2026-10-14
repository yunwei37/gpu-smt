# Original native warm comparator source

Exact byte snapshots of the measured original helper/host/worker source. Original
measurement executable is artifacts/lean-service-lifecycle-2026-10-13/build1/Lean49PreparedBranches,
with unchanged commands in every capture ZIP. Pinned SDK/Mathlib/REPL and owned
runtime object dependencies are recorded in ../build/build-terminal.json and the
repository reproduction guide. Lean module name remains Lean49PreparedBranches.

To reconstruct in the owning Workspace, generate C from this Lean source using
the pinned lake env lean -R baseline-source -c build/Lean49PreparedBranches.c,
compile with pinned leanc -O3 -c, compile this host with gcc -std=gnu11 -O3 and
the same SDK include, then link with the two original owned-runtime objects and
libREPL.a as in original-host-link-commands.json. Use fresh output directories;
never overwrite active binary/results. This source snapshot was retained after
measurement for public reproducibility; no acquisition was reconfigured/rerun.
