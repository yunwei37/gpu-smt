# RQ4 projection cost: complete native result

All5952 original ProofNet candidate records completed.5534rejected,413complete,
4incomplete and1operational exactly match the complete native control.
5951source begin/end timer pairs are monotone; original operational source5879
remains unpaired/censored. No invalid or missing input is removed.

Observed native miss exclusive calling-thread CPU:232.678006s.
Seven exact named projection/instance-wrapper definitions together:
16.910503s (7.268% of this measured miss scope).
Generic projection expressions:44.087492s.
Other miss expressions:171.680011s.
Inclusive counters overlap and cannot be summed into wall time. Name tagging,
nested instrumentation and asynchronous checkpoints limit attribution; no
whole-verification fraction, GPU ceiling, timing comparison to E015 or speedup
claim follows.

Decision: high source/call frequency did not imply a dominant expensive operation.
Individual named operations average only a few microseconds in this instrumented
run; per-operation GPU dispatch is a poor granularity to pursue. Reject another
projection-only GPU extension as the next implementation. The measured broader
contextual/native-miss boundary and strong CPU caching remain more consequential.
Keep full GPU/Lean/system research goal; this bounds a proposed fragment, not RQ4.

Next bounded implementation experiment: examine why pure no-context misses do
not use native caching, use native configuration/environment scope and native
unchanged-state checks for any candidate reuse, compare real end-to-end results
against the current warm CPU path and treat existing modern dependency-aware
caching as prior art. No arbitrary GPU gain or cache novelty is assumed.

Direct root result review, not independent audit. Original source/data/timers,
every candidate outcome and all failed/partial attempts remain under this
experiment. Full named/context buckets are in named-source-cost-analysis.json.
