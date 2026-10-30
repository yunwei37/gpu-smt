# Native artifact-scope controls

Five short naturally retiring compiles at the phobos-vt W point. Lean4.15:
the publisher-invalid amoeba_xor_function original/annotated source both
still pass with -i requested (2.202/2.188s actual values in CSV). This does not
reproduce LeanInteract tactic tracing or identify the publisher's missing
per-row Mathlib/options/full-source provenance. It rules out merely asking
the CLI to serialize an .ilean as sufficient to reproduce the old failure.

Lean4.34.1: three frozen probability targets with prepared dependencies
successfully emit .olean/.ilean/.c. Exact original source, package
autoImplicit=false,8threads/M8192,120s self timer, no HB override.
Artifacts/bytes and costs recorded. These measurements are a separate scope
from .olean-only observations. Three single compiles are not an A/B overhead
estimate and are not all42costs or a complete Lake build.

Pinned SDK Lake/Build/Actions.lean:29–108 uses --setup/--json, artifact flags
and potentially postponed IR compilation; Module.lean:981–998 defines this
job. Driver, setup, optional backend artifacts and external-package build
costs remain unmeasured; do not label this pilot full Lake wall/CPU.
Combined1Hz W own tree+old13733 peak11.69GiB;capture21.025s. No hardquota
or permission workaround. Raw outputs/logs/source/terminal outside Git:
/workspaces/.agent-state/gpu-smt-captures/workloads/native-artifact-scope-controls.
