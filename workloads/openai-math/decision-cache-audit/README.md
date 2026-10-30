# decide +kernel: source occurrences are not kernel cache misses

Lean4.34.1 commit5045d0056413266e57c625dcd7c365b10e377c52 already caches
auxiliary lemmas. Its type key also distinguishes privacy/defeq tagging and
requires matching ordered universe parameters. The cache is local to an
environment branch and is not serialized in olean. Counting identical text
across modules is not counting stock-cache hits.

Primary sources:
- https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/Lean/Elab/Tactic/Decide.lean
- https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/Lean/Meta/Tactic/AuxLemma.lean

The complete pinned-source pass covered5848files/655,100,740bytes and all
1,354,379 lexical occurrences.881,548 occurrences have a directly preceding
explicit target annotation. Their within-file distinct annotation-text sum
is625,786, with255,762 textual repetitions; global unqualified text count
489,445.472,831 occurrences have an inferred/intermediate target that this
source-only parser does not reconstruct.

**None of these numbers is the distinct elaborated goal count.**
Namespaces resolve identical strings to different constants, local contexts
and options can alter elaboration, and proof branches can have separate caches.
For example PlanarPacking HighMoments0_0 repeats the text
chunk0,0=s0_0 sixteen times; equal name resolution has not been established. Ramsey decode numerals
also repeat, but actual branch sharing must be observed natively.
Thus true kernel computations and stock-cache misses remain unknown.
The naive625786+472831 proxy is not a valid bound or native cost estimate.

The scan took168.36s/358,716KiB peak; zero lexical errors. Comments are erased,
strings retained, whitespace normalized outside literals. CSV column calls
means source occurrences, not reached tactic executions.
All raw logs, launch/summary and the scanner moved to the owning PVC outside
the checkout: gpu-smt-captures/workloads/source-target-text-v1.
No production cache or tactic behavior was changed.
