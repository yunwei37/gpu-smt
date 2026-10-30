# openai/math: seven typed-deduplicated Int/list row goals — 自审

Locked source4eaee87548250b2682affda7d05d947c05554bae, Lean4.34.1 and W's locked Mathlib cache. No project rebuild or cache mutation.
W's135compiled-module type export exposes45distinct decide-shaped auxiliary goal types. We select7distinct integer-row types, from ComputeRow1115Batch17; this is availability/type biased, not a representative sample of1,354,379source annotations.
The fresh scripts import only RowCompute definitions, never the original row-answer theorem. Plain original checks each published row goal with decide+kernel.
Untrusted Python evaluates2503scalar terms using exact integers and emits per-row scalar-sum claims. Every claim is checked with decide+kernel; List.ext_getElem and a proved finite index case split assemble the original statement. The emitter is outside the TCB: corrupting one emitted value is rejected by stock kernel.
No native_decide or new axiom; all14plain final statements depend only on propext/Quot.sound.

## Results
All7 original and7 certificate plain sources accepted. Original13.317706s wall/13.108858s CPU; certificate23.936857s wall/24.262333s CPU.
Single observations, whole-source import/construct/check costs, one SDK process at a time; source200k heartbeats, recursion10000,8GiB cooperative native check,16GiB M tree budget, CPU8–15/j1.
Additional explicit kernel rechecks include ALL newly created theorem declarations and auxiliary proofs, not only final wrappers: original2.327609s, certificate5.757960s.
Each row is slower by both measures. Certificate assembly adds24–58declarations vs2original, duplicates reduction/context work, and makes large List.getElem case proofs. This candidate batching mechanism is not supported as a serial acceleration on these rows.
It does not refute the digits equivalence rewrite or compressed grid checker: those change the computational algorithm. Splitting an already suitable structural list computation alone does not do that.
No parallel speedup is measured here, and no throughput inference from SDK j1 to a warm service.

## Honest failures and censoring
Initial emitter had indentation/length-simplification mistakes; two failed preflights retained. Corrected v3 completes all7same goals.
Observer v1 used raw1,000,000kernel heartbeats, equivalent to1000user-facing units, rather than source200000. Three certificate observers hit this artificial deterministic budget; first-check results still passed.
SDK Lean/CoreM.lean:getMaxHeartbeats multiplies source setting by1000; Lean/AddDecl.lean passes that raw value to addDeclCore. Matched v2 uses the same source options and all14observers complete. Plain proofs were not rerun or edited.
The broad45-type baseline at raw1m returned7successful/128failed rechecks; these are diagnostic-budget failures, not invalid source proofs.
At matched200m,16types finish3rechecks,1type finishes1,28types are not reached before a60s self-alarm. This is partial/censored, not a45-type cost distribution. No kernel_error returned before that interruption.
All controllers/native processes retired. Maximum sampled own tree4.981GB, no16GiB violation. Parent1s samples are not a hard RSS quota; no external signals sent. All outputs PVC.

## Reproduction and scope
prepare_openai_row_certificates.py retains untrusted arithmetic/emitter, run_openai_native.py the finite SDK boundary, run_openai_sample.py the initial point, run_openai_recheck.py the corrected observer point.
The immutable raw captures record exact scripts, stdout/stderr, args, receipts, RSS and process identities; generated-inputs.tgz preserves all versions. Paths derive from the shared W cache; scripts deliberately refuse to overwrite existing output directories.
Cold-first full checks, extra observer rechecks and Python emission (about3.4ms) are separate quantities.
Proof by reflection, certified equivalence and independent proof chunks are prior art. This sample supplies feasibility/negative timing evidence, not novelty or a general extractor.
