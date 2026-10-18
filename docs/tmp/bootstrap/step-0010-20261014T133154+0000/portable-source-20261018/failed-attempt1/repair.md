The first complete dependency compile reaches699native import libraries,
then fails compiling the POSIX clock shim with Lean's bundled compiler:
time.h is not in its default sysroot. No proof result is counted.
Forward repair compiles the unchanged POSIX/zlib host shims using host cc
with the discovered Lean include path, then links them using leanc.
No source, mathlib cache or binary used by active captures is modified.
The next full builder invocation uses the same separate output and recompiles
the source; no incomplete manifest or unvalidated binary is substituted.
