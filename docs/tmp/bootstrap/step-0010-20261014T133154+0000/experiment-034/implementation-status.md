# Native independent-argument batch integration

Observed 2026-10-16T08:07:09.984991+00:00. Root personally writes/builds; no delegate or GPU performance
claim. Build/integration work is dependency-only within the proposed experiment.

Actual repository source:
- bench/lean-gpu/NativeMetaBatch.lean collects corresponding nonidentical,
  closed argument pairs of the same application head and exports the true-result
  MetaM ABI compiled by this exactSDK.
- bench/lean-gpu/meta-batch-native.c keeps retained candidate pairs over native
  continuation, and consumes positive answers only at matching native calls.
  Assignment/instance-synthesis order and all unsupported cases remain native.
- bench/lean-gpu/meta-batch-native.h defines the borrowed provider input and
  explicit unknown/positive result boundary. No Lean pointer enters GPU memory.

The private4.27REPL links successfully at /tmp/gpu-smt-meta-batch-20261016/repl-meta-batch.
Actual module/hook/private-original-equality/privateMain compilation and link
all return0. [Build commands/attempts](native-build-records-20261016.json) retain
the initial rawclang missingstddef failure, successful officialleanc module,
leanc hook missingstdlib failure and successful existing systemcc hook path.
No active SDK, originalREPL source/library/binary or original experiment changes.
PrivateMain imports the new module for actual initialization; the generated
original equality implementation is renamed at its definition only, preserving
native calls through the new entry. This is a private build, not an extra checkout.

[Actual symbols](native-private-all-symbols-20261016.txt) show the strong exported
equality entry, private original and compiled result helper. Provider linkage is
currently weak/unresolved: this binary falls back to native execution.
No GPU kernel/provider, useful batch engagement, real device preflight or full
performance acquisition has completed. No matched speedup, RQ answer, novelty
or acceptance follows from compiling the bridge.

Next implementation is the CPU/device common packed normalization/comparison
engine and native definition/universe/constructor/recursor/projection boundary,
followed by actual5090native preflight. Merely widening old unsupported scalar
beta packets is insufficient. Concrete capture/Job commands remain to be wired
before any fullrun. Existing defaultGC paths/complete source inputs are reused.
Root plan review is self-review; independent audit is still absent.


## Reproducible private build and native fallback smoke

bench/lean-gpu/build-native-meta-batch.py now reconstructs the real upstream
Lake link command, compiles private module/hook/original equality/Main and
links without modifying the SDK or upstream REPL. The explicit optional
provider-object input can link the future engine; absence remains fallback.
The actual fresh /tmp/gpu-smt-meta-batch-repro-20261016 build returns0;
[command](repro-build-command-20261016.json) and [log](repro-build-20261016.log)
retain the invocation. Two direct accepted/rejected smoke sources return the
same native JSON as stock, with provider_linked=false and zero engagement.
[Smoke output](build-smoke-20261016.json) retains both stdout/stderr and the
initial line-reader failure for the pretty multiline rejection response. The
offline reader is corrected without another native run. This is build/interface
qualification, not formal performance acquisition, a GPU result or an RQ answer.
