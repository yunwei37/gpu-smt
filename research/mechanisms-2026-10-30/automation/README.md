# Automatic two-family proof repair — self-review
Source routing uses theorem-header structure and literals, not task names or proof-body equality.
The runtime hook checks the actual elaborated target/local context, constructs a checked proof from pre-proved equivalence lemmas, forces synthesis, and falls back on any mismatch.
The templates are specialized to digits10/count100 and product2005/sum406. This is automatic dispatch/rewrite for two known mathematical families, not a general computation compiler.

Offline released7808 scan:63 routes (32digits/31grid),0 routes outside these two task-label families.
64 task-frame sources include malformed7206 literal None, safely unsupported. Routing coverage63/64 task-frame,63/63 sources with actual matching theorem headers.
The63 automatic output sources are byte-identical to those used in native tests; malformed source also kept identical.
All64 family sources were native-paired (128invocations). Final31 accepted/29lean_error/4budget limits; native original0accepted,51budget/13lean_error.
The extra15 add no passes. See native64/paired64.csv, all原始 and memory data retained.
Header matches are not proof acceptance: unrelated-range wrong target is a deliberately routed false positive, typed bridge rejects and original rfl runs.
An explicit false prefix remains rejected even when the final goal is true. Both adversarial controls match original diagnostics after mapping the one added import line and source filename.
This supports tested fallback safety, not a universal misclassification rate or diagnostic/heartbeat equivalence theorem.
No production engine enablement. Acceptance changes (31 recovered proofs/two tasks) are reported separately from result-preserving acceleration.
Native whole-source point finite16s/200kHB, includes module loading; not warm-service throughput. Original timers are censored.
