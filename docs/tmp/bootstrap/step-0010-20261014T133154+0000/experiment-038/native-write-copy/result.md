# E038 first-write copy: implemented native result

Root implements the previously missing first-mutation distinction in the actual Lean runtime hooks. Native get resolves a retained shared base until take/set/swap first creates a private MT cell. An observed original is retained through branch drain, including a read-only one; a release/acquire write-generation invalidates other admitted tasks' cached base resolution. Stable private clones retain the existing fast cache. These are E038 algorithm details, not a new RQ, plain compiler optimization, GPU kernel or asserted novel copy-on-write primitive.

## Actual build and original native input engagement

The existing source-native builder creates /tmp/gpu-smt-native-write-copy-20261016/build without changing the running frozen-v1 paths. All50commands exit0; elapsed38.160862465s/waited compiler CPU40.502266s are finite build costs, not verification performance. build.commands.jsonl, build-logs/ and built-source/ retain exact source and compiler/link invocations.

The actual installed Kimina Repl client prepares the unchanged Mathlib/Aesop header and submits one native naive batch containing unchanged original Proof_00000 and Proof_00004 bodies. New plain and private return exactly equal complete native response objects: accepted empty response and rejected source with11errors/3warnings, including unchanged positions/text. Both workers finish normal EOF and exit0. No all-source equivalence follows from two engagement cases.

Private first-source metadata records43observed prepared refs, only4true copies,244descendant tasks and no fallback; second source records45observed refs,4copies,252tasks and no fallback. Thus39/41observed keys remain un-copied in these respective contexts. Counts do not measure saved cost, CPU fraction, latency or speedup. ref_read_ops includes branch-local and already-private reads; ref_versions now means true copied cells, unlike old eager-on-read versions. Versioned counters cannot be pooled.

## Proportionate native ref control and retained failures

The generated run_cmd witness attempt1 has unknown liftIO diagnostics and never exercises its intended read/write. Attempt2 removes that syntax error, but native Lean aborts because an init declaration cannot be evaluated in the same module. Driver/native stderr and raw failed outputs remain. Neither successful process plumbing nor the first invalid witness counts as passing the intended control. This same-module fixture route is closed; no broad native-correctness campaign follows.

The replacement native-ref-witness.c invokes actual rebuilt native get/set and branch APIs. Read-only observes0with0copies; first mutation reads7with1copy; the shared root and a subsequent branch read0. Native compile and execution exit0. Initial missing SDK system headers and missing libm link attempts remain recorded separately. This direct primitive control adds no benchmark source or performance cell, and does not exercise arbitrary interleavings/FFI.

## Independent review and scope

Root reads the full independent review.md, including ownership, exact native hook/ABI, first-write publication, cache generation/ABA, task drain and counter meanings. The initial source review finds no delta-specific blocker. Its closing checks actual source/build/native receipts, rather than interpreting source approval as dynamic results. These scoped checks do not complete full-paper review or prove arbitrary source/process equivalence.

Run status: finite build/client/native-control engagement complete; failed generated fixture route preserved. Research value: dependency-only implementation within the admitted E038 mechanism. Hypothesis/performance: the complete RQ3 hypothesis remains inconclusive; no new speedup. Paper impact: implementation now matches the intended first-write mechanism on the exercised native boundary. Existing full frozen-v1 acquisition remains associated with its old eager-copy code; no new full capture is started or pooled. All four RQs, full Lean/SMT/service/RTX5090 scope, missing defeq wall-cost quantity and paper gates remain open.
