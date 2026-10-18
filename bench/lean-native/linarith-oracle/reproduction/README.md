# Buildable arithmetic oracle source

This is the CPU arithmetic frontend used by the E1080 Power condition:
export supported real/rational comparisons, expand literal natural powers,
search outside Lean, and reconstruct a contradiction checked by Lean.
Unsupported expressions and unsuccessful certificates fall back to the native
arithmetic path. Nat/Int goals can first use the same official omega control
as the matched reference.

This experimental component currently has a selected-1,000-source paired
result of **1.70059×**. Full original-population generalization is running.
That result uses a warm native harness and includes fallback and retirement;
the standalone command below is functional verification, not a replacement
performance measurement. No GPU benefit or production-service claim follows.
See [source provenance](PROVENANCE.md) and the
[measured result](../../../../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-without-diagnostics/full1000-result-review.md).

Qualification: all three numerical executables build and the four existing
numerical tests pass. The complete source build compiles699native dependency
libraries and15local Lean modules. The public CLI checks the same first64
real selected Goedel sources:63complete and1rejected, matching every reference
source classification. Failed build/load attempts remain documented.
[Functional results and exact scope](../../../../docs/tmp/bootstrap/step-0010-20261014T133154+0000/portable-source-20261018/result-review.md).
This is separate from warm benchmark timing and full REPL payload comparison.

## Build

Use Linux, Python (validated with3.13), Rust1.88 or newer, a C toolchain with zlib
development files, and a Lean4.27 Mathlib project with its ordinary OLean
cache. Put that project's Lake and the Rust toolchain on PATH. The Mathlib
source revision must match its cache; the measured dependency pins are in
[the retained native compilation evidence](../../../../artifacts/lean-modern-native-compilation-2026-10-14/).

```sh
python3 bench/lean-native/linarith-oracle/reproduction/build.py \
  --mathlib /path/to/mathlib4 --out /path/to/separate-oracle-build
```

The builder discovers import source roots through Lake and Lean, builds the
locked numerical crate, compiles native dependency libraries into the chosen
output, and records the exact commands and load order in build.json.
It reads the Mathlib cache without rebuilding or replacing it.
Use a build output unused by live verification processes.

The numerical source derives from Apache2-licensed Farkas. Local changes and
their provenance are recorded in PROVENANCE.md; they do not establish a new
LP algorithm. The historical snapshots and failures remain under artifacts/.

## Verify a source

The chosen Python needs NumPy and highspy1.15.1. A Python environment containing
them runs the following bounded command; it starts a CPU support subprocess
only for this verification and retires it afterwards.

The Lean input must import GpuArithmetic.IntegerPowerOracle after its normal
Mathlib imports. Its theorem bodies remain unchanged.

```sh
python3 bench/lean-native/linarith-oracle/reproduction/check.py \
  --build /path/to/separate-oracle-build --log-dir /path/to/new-result-directory \
  /path/to/Candidate.lean
```

Lean's exit status and JSON diagnostics are preserved, together with support
and race records. A nonzero exit is retained as failure. The diagnostic names
containing GPU are historical protocol identifiers: this command uses CPU
HiGHS and exact rational repair, with Lean checking the resulting proof.

This package does not recreate a frozen benchmark's machine state, CPU
placement, warm REPL, input grouping, native reference binary, or clocks.
Use the linked experiment's input, paired protocol and whole-time boundaries
for a performance replication. The public build has a separate64-source functional qualification;
it is not substituted into active captures.
