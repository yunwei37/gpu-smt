# Native arithmetic oracle experiment

Status: experimental, not a production Lean service or demonstrated GPU speedup.
See the [predeclared decision rule](../../../artifacts/linarith-oracle-2026-10-17/plan.md).

- `build-stages.py`: copies the pinned Mathlib control/reconstruction functions into an instrumented namespace, records sequential thread CPU and invocation wall, and builds native code. Original Mathlib is unchanged.
- `Oracle.lean` / `oracle.rs`: one export of supported real/rational comparison expressions, native polynomial/product generation and LP, coefficient/provenance return, selected proof construction and one weighted contradiction check. Unsupported or failed cases restore state and run the original path.
- `Baseline.lean`: established Farkas Fast plus invocation-local product-application reuse with native hybrid/HiGHS certificate search.
- `run-stages.py` / `run-comparison.py`: use the existing Kimina native batch collector; preserve all source outcomes, costs and raw streams.
- `build-oracle.py`: rebuilds the native experiment from the retained sources and dependencies. No original repository or installed runtime is modified.

The scripts currently use the retained owning-Workspace dependency paths (Lean4.27, matching Mathlib/Farkas/Kimina), not a portable installer. Their pinned versions and original build procedures live in the reproduction guide and `artifacts/lean-modern-native-compilation-2026-10-14/`. Build outputs and long-run raw files use `/tmp/gpu-smt-linarith-oracle-20261017/`; publish completed evidence back to `artifacts/linarith-oracle-2026-10-17/`.

In the owning Workspace, with no active build using the same output filenames:

```bash
python3 bench/lean-native/linarith-oracle/build-stages.py
python3 bench/lean-native/linarith-oracle/build-oracle.py
/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python   bench/lean-native/linarith-oracle/run-comparison.py   --out /tmp/gpu-smt-linarith-oracle-20261017/new-preflight   --limit 24 --methods fast-hybrid oracle
```

Use fresh output directories. A preflight is qualification, not a full speedup claim.
Do not rebuild libraries that active experiment workers still use. Main performance
trials disable diagnostic telemetry. Whole clocks include native preparation,
packing/IPC, oracle work, checking, fallback and process retirement.
