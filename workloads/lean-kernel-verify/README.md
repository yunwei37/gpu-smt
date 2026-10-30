# Released GPU-kernel verification workload: LKV

Source: [facebookresearch/lean_kernel_verify](https://github.com/facebookresearch/lean_kernel_verify)
at129e65bfd8efbf6c45710732d205c941ef65928c (commit2026-10-28).
MIT license. Upstream specifies Linux,Python3.10+,Lean4.34.0,core/Std only;
no Mathlib or Lake. Full Git tree is not truncated:173files,
12Lean source files/189,413bytes,92JSON assets including90already released
KIR fixtures/481,125bytes (997-13,567bytes each).

The90KIR JSON fixtures were all downloaded and parsed; no new kernels,
candidate proofs,or input cases generated. source-census.csv counts raw
lexical occurrences including documentation/strings,not elaborated tactics.
Direct ofReduceBool references0 in these scanned sources; compiled axiom
closure is unknown. Source count is not proof count.
released-kir-fixtures.csv records role/parameter/tensor counts and concrete
grid fields,not runtime event counts or costs.

This broadens the audit beyond Mathlib arithmetic candidates:finite GPU-kernel
models evaluate address arithmetic,barrier ledgers,coverage and TMEM access.
The upstream checker emits native_decide proof wrappers over concrete KIR.
No public failed LLM candidate stream or precompiled Lean proof collection was
identified in this pinned tree. These are released verification fixtures,
not evidence for RL training arrival distributions.

Important acceptance distinction:upstream PASS/FAIL/ERROR/UNDECIDED are checker
verdicts. A FAIL can mean a successfully established concrete violation;
it must not be mapped to ordinary Lean proof rejection. Upstream command exit1
and compiler acceptance are different observations.
Axiom/trust audit must include native_decide and the chosen phase-ledger model;
do not treat this as decide+kernel or all-shape kernel correctness.

The public check command can consume checked-in KIR directly. The upstream
run/export frontend still depends on Meta's monorepo at this revision,so full
kernel-to-report reproduction from the public clone is not qualified.
README example0.4/0.5s numbers are upstream examples,not our measurements.

No native build/replay performed:W's existing EPFL process is still blocked,
and the one-Lean rule is preserved. Current installed4.34.1 is not silently
substituted for this required4.34.0. Future native admission should use exact
SDK,serial KV build and PVC outputs (upstream /tmp defaults must be overridden).
No GPU is needed by the released checker; no whole-project build estimate
or native time/peak-memory result is fabricated.
Raw source/metadata:/workspaces/.agent-state/gpu-smt-captures/workloads/
lean-kernel-verify-static (outside Git).
