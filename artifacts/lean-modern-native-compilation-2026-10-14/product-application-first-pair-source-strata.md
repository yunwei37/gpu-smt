# Source-text strata in the complete first product-reuse pair

Root direct offline diagnostic/self-review; this reuses the complete first29,750-source pair rather than running another benchmark. Reproduce with python3 analyze-product-application-source-strata.py. No source or outcome is removed from the primary whole result.

| Source-text group | Files | Reference p50 s | Reuse p50 s | Reference p95 s | Reuse p95 s | Reference p99 s | Reuse p99 s |
|---|---:|---:|---:|---:|---:|---:|---:|
|text nlinarith|19539|0.752938|0.594593|3.717141|3.012858|8.284233|6.624923|
|neither tactic name in source text|7025|0.110610|0.104124|1.752222|1.685510|31.912730|33.661761|
|text linarith without nlinarith|3186|0.204330|0.198240|2.072273|2.087457|17.129235|17.454199|

The largest observed p50/p95 improvements occur in the19,539sources containing nlinarith text. Sources with neither tactic name also have lower p50/p95, while their p99 worsens; linarith-only p95/p99 also worsen. This is consistent with a nonuniform effect and does not justify assigning the entire9.82%whole elapsed difference to the product builder. These are different source populations under shared background, not a controlled interaction experiment. Names may occur in comments, indirect tactic invocation is possible, and only the planned separate runtime profiles can establish actual per-source engagement.

All ten basic/native outcome differences stay in the table and raw JSON. A separate same-basic sensitivity table is included in JSON with explicit retained counts; it does not replace primary results. Latency quantiles are closed-loop request observations, not CPU time, offered-load queueing or addends of whole makespan. Repetitions and stronger matched CPU methods remain incomplete.

Decision: continue the original full repeated acquisition; do not start a selected-source retest or claim that text strata prove a causal speedup. This is supporting interpretation of the existing whole-pair observation, not an additional paper contribution or RQ answer.
