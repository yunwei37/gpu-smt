# GPU SAT certificates and real Lean assets — source eligibility, root self-review

Observed2026-10-20UTC, within the open RQ4 evidence search and unchanged
Initial Narrative. All work is root-thread work. This is source/asset
qualification, not measured feasibility, a new mainline or an independent audit.

## Questions and declared coverage

Could a credible existing GPU solver replace substantial native search in a
complete Lean verification path, instead of building another narrow LP kernel?
Does an established real software-verification corpus supply that path and
the multiple contexts missing from the original single-header cohort?

Check the pinned Lean external-solver/checker contract, one proof-producing
GPU solver, its established proof converter, official real-world Lean cases
and the released repository-scale dataset. Stop when proof-format compatibility,
workload/producer scope and runnable prerequisites can be distinguished.
Generic external search plus native certificate checking must not be
reintroduced as a new contribution. The original selected1000criterion and
currently running whole29750protocol remain unchanged.

## Actual versioned proof interface

[Lean4.27 External.lean](https://github.com/leanprover/lean4/blob/v4.27.0/src/Lean/Elab/Tactic/BVDecide/External.lean)
invokes a CaDiCaL-compatible executable with CNF/proof paths, LRAT/binary
selection and its UNSAT-oriented options. It expects the recognized SAT/UNSAT
stdout format, not arbitrary solver banners. It owns interrupt/timeout handling.
[The native LRAT frontend](https://github.com/leanprover/lean4/blob/v4.27.0/src/Lean/Elab/Tactic/BVDecide/Frontend/LRAT.lean)
loads the certificate after solving; its parser handles the proof bytes.
[LRAT actions](https://github.com/leanprover/lean4/blob/v4.27.0/src/Std/Tactic/BVDecide/LRAT/Actions.lean)
include RUP, RAT, empty-clause and deletion operations. Therefore it is wrong
to reject this version on an assumed RUP-only parser.

The [official Lean bitvector reference](https://lean-lang.org/doc/reference/latest/Basic-Types/Bitvectors/)
also makes the trust boundary explicit: the verified checker executes as
compiled native code, and its result relies on Lean's native-computation
axiom. A prospective adapter must preserve that existing path and must not
describe it as recomputing the entire certificate solely in the kernel.
The GPU is not thereby trusted; no debug skip-check setting is proposed.

[ParaFROST553817f693fba75fb459c754d5717c12bfeedf7f](https://github.com/muhos/ParaFROST/tree/553817f693fba75fb459c754d5717c12bfeedf7f)
is an existing GPU-inprocessing SAT solver. Its pinned src/gpu/options.cpp
declares DRAT proof output and a proof-output path, not the required LRAT CLI.
Its proof.hpp describes clause additions/deletions. A direct sat.solver
substitution is therefore not yet compatible.
The existing
[drat-trim2e3b2dc0ecf938addbd779d42877b6ed69d9a985](https://github.com/marijnheule/drat-trim/blob/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c)
provides LRAT output through -L and compressed output through -C.
These sources support a possible translation chain; no actual GPU-produced
proof has been converted or accepted by Lean in this project.

The primary [FMSD2023paper](https://doi.org/10.1007/s10703-023-00432-z)
already contributes certified GPU SAT inprocessing and evaluates proof
generation. Neither proof-producing GPU search nor adding an existing
certificate checker is our new primitive. Contemporary native Lean/CaDiCaL
whole verification would be the numerical comparator, not the paper's older
sequential solver times or a weaker CPU ParaFROST-only denominator.

## Real assets and current-cohort applicability

The versioned official
[bv_decide_realworld.lean](https://github.com/leanprover/lean4/blob/v4.27.0/tests/bench/bv_decide_realworld.lean)
contains the original32-bit popcount and parity verification obligations
sourced from LNSym. The official bench tree additionally has inequality,
large-AIG, modulus, multiplication and rewriting files; the latter are
benchmark controls, not automatically a real candidate traffic population.
The two complete real-world obligations could qualify a future interface.
Two cases alone cannot establish a whole-verifier/system result.

[VeriSoftBench's primary paper](https://arxiv.org/abs/2602.18307) and
[released artifact8f5e8b36ab5fbdec6fd8d8f4ee0580d29647097a](https://github.com/utopia-group/VeriSoftBench/tree/8f5e8b36ab5fbdec6fd8d8f4ee0580d29647097a)
offer actual software-verification repository contexts.
[inspect-assets.py](inspect-assets.py) reads all500released records and pinned
repository metadata, retaining [every task's source identity/toolchain](verisoftbench-task-metadata.csv)
and [the complete derived counts](asset-analysis.json).
There are23repository roots and19declared toolchain strings; none is4.27.
Ground-truth text contains an explicit bv_decide token on IDs125,322,350 only.
Those are lexical mentions, including possible comments/strings, not measured
tactic execution or cost. The supplied ground-truth proofs are not released
generated failed/successful candidate streams. The inspected public tree has
no results/cache evaluation-output directory.

The same streaming lexical check covers all29750original Goedel sources and
the selected1000, with no explicit bv_decide token. This does not rule out
indirect tactic invocation; it establishes no GPU coverage fraction or
Amdahl bound. There is no evidence that replacing this SAT interface would
accelerate the current arithmetic comparison. Do not select the three
reference tasks as though they were a representative500-source GPU result.

A future repository-context benchmark must use the pinned real projects and
their own toolchains, not compile filtered prompt snippets containing stubs
or silently migrate everything to4.27. Declared imports and repository count
alone do not establish removable preparation cost. The upstream full-image
recipe reports roughly110GB; it is not installed on the current small volume.
No model inference/evaluation API is called; public GitHub reads supply the
source metadata. No new container, Workspace or storage change is performed.

## Disposition and next empirical dependency

The code-level format chain is a **candidate**, not a working backend.
Defer implementation/admission as a replacement mainline: there is no own-clock
native cost opportunity or representative current-cohort engagement yet.
This neither closes the arithmetic GPU route nor replaces the original four
RQs with a small bitvector benchmark.

If revisited after the sole current capture retires, first use original
official real-world source cases and the unchanged native Lean/CaDiCaL
baseline to establish complete native verification and paid solver/check
cost. Only an actual favorable complete-cost preflight could admit a larger
comparison. GPU initialization, CNF export, proof emission/conversion/transfer,
native checking, fallback, waiting, cancellation and process retirement are
charged; a DRAT checker timing is not complete Lean verification.
Do not implement an unmeasured solver/allocator/parameter grid.

The owning Workspace currently exposes no /dev/nvidia device. Its existing4.27
SDK does contain bundled CaDiCaL2.1.2, confirmed by its own --version. The
installed4.27frontend uses Lean.ofReduceBool at the reflection boundary,
consistent with the official trust description above. The later official
[Lean4.34release](https://lean-lang.org/doc/reference/latest/releases/v4.34.0/)
already documents stronger preprocessing; a pinned4.27comparison would not
establish a global current CPU optimum. Future actual5090execution
must use the existing authorized finite GPU benchmark path, with combined
owned-resource monitoring, shared-device memory behavior and cleanup verified;
this source check allocates nothing and changes no provider or quota.
No additional Lean process is started alongside the active two-REPL group.

## Search and checks

Queries: ParaFROST GPU SAT solver proof DRAT LRAT Lean bv_decide; official Lean
BVDecide external-solver benchmarks; GPU SAT certified proof; bv_decide LLVM/
AliveInLean benchmarks; verified bitvector decision-procedure artifacts.
Primary coverage: versioned Lean code and official docs, pinned solver and
converter sources, FMSDpaper, official original real-world bench, and released
VeriSoftBench paper/data/metadata. Secondary search hits are leads only.
An obsolete Lean/Meta source path and a guessed bench subdirectory fail;
the actual4.27tree resolves them to Lean/Elab and six bench files.
The first source-fetch command has a quoting syntax failure before network/
mutation; the corrected command supplies the inspected code.
No source is changed because of external instructions.

At this node closure the original driver23039/birth1792486754.32 is still
live with two REPLs, a0.749s-old watchdog sample of18,253,963,264owned RSSbytes
and no terminal cell. Available project bytes are2,234,183,680. These are
operational observations, not new performance results.\n\nRoot rechecks all500IDs/23roots/19toolchains and both original Goedel
populations; source labels and dynamic-cost claims remain separate.
The public arithmetic reproduction docs already distinguish standalone
functional checks from budgeted research captures, so no speculative public
CLI/resource fix is made. Current source, binaries and the active matrix are
untouched. The paper's original contract and results need no rewrite/compile.
This is a completed bounded eligibility node, not another whole experiment,
a useful GPU result, independent audit or submission acceptance.
