# Released GPU-kernel checker: workload units and native result semantics

2026-10-30 UTC; root self-review. Parent W6b95284/W009; no reproduction.
The finite questions are whether released cases are usable workload inputs,
what the evaluator's result unit means, and which native trust/cost boundary
a future comparison would have to preserve. This supports RQ1/RQ2 workload
admission; it is not an adopted mechanism or RQ answer.

## Search and verification

Query: github facebookresearch lean_kernel_verify native_decide PASS FAIL.
The GitHub tree web fetch fails; mirrors in search results are excluded as
scientific sources. Official pinned raw README, emitter, Lean checker and
Python result parser are opened instead. CLI independently retrieves those
four primary files and checks equality with W's retained copies. The source
pin is129e65bfd8efbf6c45710732d205c941ef65928c, official initial commit
2026-10-28. The complete official tree/commit metadata and all90 fixtures were
already retained by W outside Git; root rereads the actual files.

[Publisher README](https://github.com/facebookresearch/lean_kernel_verify/blob/129e65bfd8efbf6c45710732d205c941ef65928c/README.md)
specifies Lean4.34.0, core/Std, CPU-only KIR checking, and scope restricted to
concrete cases. Its public kernel-to-IR run/export path still needs the
publisher's monorepo. The phase-ledger method is argued sound, not formally
proved. No complete kernel-to-report reproduction follows from fixture
availability. Upstream example timings are not our measurements.

## Complete static input check

Root validates the nontruncated173-file tree,12Lean files/189413bytes,
92JSON assets, and90KIR files/481125bytes against W's CSV and raw files.
Per-fixture role/parameter/tensor counts, grid fields and sizes agree.
All native-cost/outcome fields remain unknown/not_run.

The fixtures comprise67P0 and23P1 inputs at the file level. They contain184P0
and66P1 concrete input entries. The pinned emitter's five P0 specifications
and one P1 specification imply920+66=986positive theorem-wrapper obligations
if emitted over these inputs. These are static counts derived from the
emitter, not986executed proofs,90candidate requests or measured runtime.
No fixture generation, Lean build, dynamic proof inspection or source budget
change occurs.

## Three result boundaries

[Emitter](https://github.com/facebookresearch/lean_kernel_verify/blob/129e65bfd8efbf6c45710732d205c941ef65928c/frontend/emit_lean.py)
prints an evaluation report and generates positive KV.Holds theorem wrappers
closed by native_decide. A false positive-property wrapper can therefore
produce Lean's native_decide false-proposition error. It does not generate
an accepted negation proof for every checker FAIL.

[Lean checker](https://github.com/facebookresearch/lean_kernel_verify/blob/129e65bfd8efbf6c45710732d205c941ef65928c/lean/KV/Check.lean)
separates the boolean property, concrete issues and certainty. Lack of a
certain counterexample may instead mean UNDECIDED. Model evaluation errors
also have distinct kinds. The source is explicit about compiler trust.

[Python parser](https://github.com/facebookresearch/lean_kernel_verify/blob/129e65bfd8efbf6c45710732d205c941ef65928c/scripts/lkv.py)
checks that Lean errors are exactly the recognized refuted wrappers and that
its exit status agrees; unrelated errors become tool failures. It reconciles
the report with the theorem result. Application PASS/FAIL/ERROR/UNDECIDED and
process exits are distinct observations; UNDECIDED can exit0, while a certain
violation can exit1. The optional P1 strictness also changes run-level
adjudication. Exit0alone is therefore not all-spec acceptance, nor is exit1
alone an ordinary candidate rejection/timeout.

## Disposition and handoff

This is a real additional released computational verification asset, within
the existing public-program-verification scope. Its released fixtures do not
supply an LLM candidate stream, RL arrival distribution, all-shape correctness
or a useful GPU acceleration result. Native_decide is not silently substituted
for the ordinary decide+kernel math-library point.

A future native workload should record application verdicts, Lean wrapper
errors, process terminal state, options, preparation and exact toolchain
separately. The source-native4.34.0 fixture checker is a workload, not a new
competitor-system reproduction. Native execution/axiom closure and stage costs
remain pending with W; root does not launch them or change W's queue.

Canonical background/prior-art have foreign dirty work and stay untouched.
Root records this finite source audit here and links it from evaluation.md.
The paper adds a local setup/result-scope paragraph and one pinned source
citation, leaving all scientific framing, four RQs and Related work fixed.
