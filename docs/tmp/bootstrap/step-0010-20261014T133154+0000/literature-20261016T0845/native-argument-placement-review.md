# Native argument-frontier placement: performance admission review

Observed 2026-10-16 by root, which owns Lean/GPU implementation. This is a source-grounded review of the existing unlinked E034 interface, not a new backend, performance run, independent audit, or completed RQ. It leaves active captures and every specialist's author files untouched.

## The implementation point and the actual competitor

The current bridge in bench/lean-gpu/meta-batch-native.c interposes the exported lean_is_expr_def_eq entry. With a linked provider and an explicitly enabled mode, it calls GPUMetaBatch.collect before continuing into gpu_meta_batch_original_defeq. The collector accepts different, closed argument pairs of same-head applications; it has no native function-parameter classification, cache-miss result or knowledge of which arguments the continuation will actually compare.

The current default/unlinked build returns directly to native equality before collection. Thus the following costs are risks of the proposed enabled path, not measured overhead of an engaged provider or evidence that a GPU ran.

The matched Lean 4.27.0 source already does substantial work avoidance:

| Native source location in Lean/Meta/ExprDefEq.lean | Behavior relevant to useful offload work |
|---|---|
| 2110–2114, isExprDefEqAuxImpl | Quick equality and proof irrelevance precede expensive reduction/comparison. |
| 2150–2153 | Weak-head reduction can change the terms and recurse before the application path. |
| 2163–2179 | Native cached true/false results bypass isExprDefEqExpensive. |
| 2060–2101 | Native permanent and transient defeq caches already distinguish context/configuration cases. |
| 2031–2058, isExprDefEqExpensive | Eta, projections, reduction, native/natural/offset/delta procedures precede or condition application comparison. |
| 255–288, isDefEqArgsFirstPass | Some proposition arguments are skipped; explicit/easy cases run first while implicit and higher-order cases are postponed. |
| 290–320, isDefEqArgs | Work can stop after an earlier failure; pending instances and different inference configurations occur in later passes. |
| 1995–2004, application path | Arguments are checked under the native checkpoint and function/level comparison ordering. |

Source: the installed SDK's src/lean/Lean/Meta/ExprDefEq.lean. A direct read of the official v4.27.0 raw source returned HTTP 200 and matched all installed source bytes. This is ordinary provenance evidence, not an added download/startup/acceptance gate. The web reader's two cache-miss failures are retained in the companion receipt; direct primary-source access succeeded. No full third-party source copy is added to the repository.

## Performance consequence

An early collector's offered width can include pairs that native Lean would never pay to reduce: the parent may be solved by a quick check, a native cache hit or an earlier argument failure, and proposition arguments may be skipped. Parent weak-head reduction can also change the argument problem. Running those pairs in advance adds speculative work even when their answers would be valid.

Consequently neither offered-pair count nor the outer-call no-metavariable percentage measures the expensive native work that this interface replaces. Nor can positive-answer count alone establish benefit: a useful answer has to be consumed on a comparison the matched native baseline actually reaches, and its saved computation must outweigh extraction, representation transfer, launch, synchronization, cache lookup and other extra work.

The current bridge also allocates an answers array and scans retained positive pairs on native continuation. These are additional proposed-path costs. Their absolute cost is unmeasured and is not guessed from the source.

The E032 inclusive isDefEqArgs subtree is 23.16% of sampled CPU, and the entire sampled Meta defeq subtree is about 35%. Those are broad opportunities, not this collector's coverage. E033's 23.609% outer observed CPU without expression/universe metavariables is a different, instrumented denominator. These percentages must not be multiplied into a claimed measured end-to-end bound or equated to the candidate pairs inside a parent.

The published E034 ceiling analysis remains authoritative about its conditional arithmetic and missing q. This inspection explains a concrete reason why useful q could be much smaller than offered work. It does not measure q, batch width or an end-to-end speedup.

## Implementation disposition and remaining scientific question

Do not fill this early-entry interface with a GPU provider and present offered pairs as an admitted acceleration opportunity. Keep its reproducible unlinked native fallback and negative/partial status; no enabled provider, device engagement or performance claim is added.

A useful successor would have to replace work that survives native quick/cache/proposition/ordering shortcuts, expose enough independently ready expensive work, and compare its complete costs against those engaged native shortcuts. Moving collection later may reduce speculative work but can also collapse the available batch. Relocating a hook alone is not a novel system contribution and is not implemented as another proxy milestone here.

The larger-cost question remains candidate-body Meta computation, including context-dependent reduction/comparison, with a concrete differentiated algorithm and complete formal-workload evaluation. Existing header reuse, native caches and ordinary compilation remain strong baselines. The source result closes the unsupported inference from early offered width to saved time; it neither closes all GPU methods nor supplies the missing system, novelty or complete experiment matrix.

## Validation and limits

Root inspected the current published interface/collector and the matching SDK source; [source-reading receipt](native-argument-source-receipt.json) records version, paths, access and the relevant locations. No native source, running workload, GPU owner, model setting or capture input was changed. No acquisition row count was polled. This is the implementation owner's own review; the separate opportunity reviewer and complete independent paper/step audit remain outstanding.
