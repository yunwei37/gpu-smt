# Public arithmetic-source functional qualification

Root self-review, 2026-10-18. This is executable-artifact qualification,
not a new performance experiment or independent audit.

The actual public build.py completes with Lean4.27.0:
699dependency native libraries,15local Lean modules and3locked Rust
executables. The existing4rational tests pass. Host shims use host cc;
regenerated dependency C receives package identity discovered from Lake's
manifest through Lean's actual module-setup format. Mathlib's existing
OLean cache is read without rebuilding it. Source bodies remain the measured
implementation, with provenance comments; active capture binaries are untouched.

The public check.py verifies the same first64real selected Goedel sources
through standard Lean CLI. All64return:63exit successfully and Proof_00710
fails with the same reference rejection. Every source's completion/rejection
classification matches the frozen reduced-diagnostic reference. No sorry
declaration warning appears. Thirty warning diagnostics and the one expected
error remain. This is not a claim of identical REPL response payloads or
a whole1,000/29,750-source performance reproduction.

Actual engagement records34races:24legacy-gpu winners,7external-infeasible,
2cpu-no-certificate and1cpu. Here legacy gpu means CPU HiGHS; no GPU executes.
Twenty-seven sources have support records;31complete LP models are parsed,
and3backend error records remain. Those are retained, not silently counted
as completed solves. All64support processes leave retirement records.
These observations establish executable oracle engagement beyond library load.

The wrapper inherits fourCPU20--23,48GiB and core0 for this finite
qualification. Standalone per-source setup differs from the warm measured
harness, so no new speed ratio is reported. The build/proof source and
protocol, all candidate sources, diagnostics, support/race data and exact
commands remain linked in this directory. Reproduction requires the
documented Linux toolchains and matching4.27Mathlib OLean cache; this was
not tested as a dependency-free clean-machine installer.

Failed attempts1--3 remain: absent host headers, omitted native package
prefix, and incorrectly escaped generated setup probe. They produce no
successful proof rows or timing claims. Their forward fixes are exercised
by the final complete build and64source run.

This closes the public-source functional dependency. Full current Goedel
and miniF2F captures remain active, ProofNet component is already negative,
GPU overall upper-bound/benefit and systems novelty remain open.
No RQ or full paper lifecycle gate is declared complete by this result.

Individual .gz files are lossless raw archives; decompress to inspect their original bytes. All128source/command-metadata archives have byte-equal roundtrip receipts. No raw diagnostics are trimmed.
