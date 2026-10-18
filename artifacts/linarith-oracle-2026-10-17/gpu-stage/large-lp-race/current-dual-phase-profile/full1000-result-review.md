# E1066 complete current-build phase profile: root result self-review
Actual acquisition ended2026-10-18T14:26:15Z. Same original1000 sources, eight static queues, four eligible CPUs4--7,48GiB address space, normal proxy setup/retirement and all diagnostic metadata/gzip charged. No GPU runs in this pair.

## Verdict and timing boundary
Native705.408609038s; two-sided CPU oracle459.319875055s. Diagnostic ratio1.535767659, excluded from the three predeclared primary pairs because this is an instrumented acquisition. Both992complete/8reject/0operational failures. Native full JSON exactly matches the retained uninstrumented native; current CPU agrees in every verdict/non-message field but differs from retained CPU on one unused-variable warning for Proof_19219. Native versus current CPU has104 message-only differences. The initial overly strict cross-run warning assertion failed and its raw traceback is retained; diagnostics were neither normalized nor hidden.

Native/all oracle request records are13,230/10,251, respectively, with1000 unique candidate spans each. All expected source/call/check/shape joins hold. Direct oracle4202 requests have3597 checked certificates and605 no-certificate/fallback replies; native fallback6049 requests have5440 certificates and609 no-certificate/error replies. Source-less auxiliary fast/product-application records stay raw but are excluded from source attribution. Observer read errors0/101 prevent a strong memory ranking.

## Phase accounting
These are two distinct units. Calling-thread CPU excludes child compute. Elapsed sums overlap across candidates and cannot be divided into a disjoint whole-pipeline budget.

| Recorded phase | Native calling-thread CPU seconds | CPU-oracle calling-thread CPU seconds |
|---|---:|---:|
| Lean preprocessing |162.193|97.900|
| Lean linearization |87.667|48.210|
| Lean product/proof construction |211.644|104.211|
| Lean LP wrapper |12.295|6.908|
| Native proof construction/check |208.288|80.592|
| Direct coefficient proof check |not applicable|177.775|

Direct AST export is not separately timed by the fallback Lean-stage counters. Product/proof construction is not all replaceable numerical GPU work. None of these rows includes native child LP CPU.

For all direct oracle calls, including failed calls, reply elapsed timers sum:
- successful numerical-search regions29.850499s, failed regions51.984225s;
- polynomial linearization0.316409s;
- numerical products3.720429s;
- direct roundtrips95.161506s including IPC/waits and untimed work.
Native fallback roundtrips add92.030066s. Search-region timers include race/exact-path bookkeeping and retirement, not just pure floating solve. Complete numeric-worker pure-LP CPU, cancelled-child compute and exact-repair CPU are not measured separately here, so subtracting proxy time from these totals would not establish a repair budget.

The current1888 numerical races sum108.876152s. Parsed HiGHS935 calls sum9.344250s solver elapsed,0.655748s build elapsed and10.197226s call elapsed;448 connections abort or remain unparsed. Proxy calling-thread CPU6.563997s is a different metric. Legacy winner label gpu denotes CPU HiGHS in this CPU-only cell, never CUDA.

## LP sizes and actual concurrency
Exact coefficient-space distributions cover all requests, not just successful calls. Native median10rows/20columns/74nonzeros across13230 requests. Direct median43/167/892 across4202, with median120 generated products and149 product columns after equality expansion. Native fallback median4/14/31 across6049. Full p90/p99/max distributions remain in JSON.

Actual935 floating-model HiGHS requests have median82rows/230columns/1752nonzeros, p99 310/861/7477, maxima730/2628/17569. They are not interchangeable with unscaled exact coefficient-space matrices.

93 of935 parsed floating requests overlap another candidate's request lifetime, with at most3 distinct candidates and0.937663s of cross-candidate overlap. All10251 exported numeric requests have at most5 concurrent candidates and29.671134s overlap, but those wider intervals include IPC/lock/wait and are not device-ready batches. More queueing or different scheduling could change supply and owes its own cost. These observations neither prove all935 can batch nor prove a universal concurrency ceiling.

## Own-denominator zero-cost sensitivity
Historical2234.69s has no matching current phase stamps and is not rescaled. This new native clock is705.408609s.

Deleting an intentionally broad observed envelope of Lean product/LP stages and entire numeric roundtrips covers605.285548s of occupied native timeline,85.806% of its whole clock. Many other threads execute concurrently in those windows. With fixed source paths, other durations, gaps and static queue assignments, deleting each source's envelope models447.594681s, or1.575999x against its own native baseline.

For the current CPU oracle, the broad envelope occupies269.914136s,58.764% of459.319875s. The analogous fixed-lane zero-envelope model is401.288837s, or1.757858x relative to this pair's native clock. This over-deletes IPC/repair/wait/retirement and Lean product proof work as well as numerical work.

These are optimistic fixed-path sensitivities, not strict scheduler-independent Amdahl upper bounds or measured GPU speedups. Both remain above1.5, so neither supports the user's GPU-negative closure condition. The actual three primary CPU pairs still sum to1.508619170x on the enriched cohort; no fourth primary pair is added. Overall GPU research/hourly goal remains active. The failed additive64 GPU candidate is not promoted into another full matrix or a kernel-parameter grid.

## Matched heavy tails
Select the same10/100 source IDs by native individual service duration; all IDs and per-source ledgers retained.
- slowest1%: summed native/CPU source spans1044.858834/790.861616s, which overlap and are not whole-cohort elapsed. On the CPU oracle these sources contain only1.203178s of direct numerical-search timers. Recorded fallback preprocessing+linearization101.270045 calling-thread CPU seconds, product/proof work39.764450s and total direct+native proof checking56.090037s remain.
- slowest10%: summed spans2319.471360/1484.348538s; direct numerical search22.952416s, recorded preprocessing+linearization125.795282CPU seconds, products67.801424s and direct+native proof checking102.718890s.
Thus the remaining tail is not explained by the parsed floating LP timer alone. These observations motivate complete workload/component comparison and substantial proof/frontend work, rather than more variants of the current slower numerical kernel.

## Reproduction and decision
Full raw archives are under full1000-raw. Large original gzip streams are split into numbered32MiB byte chunks and reconstructed by concatenation; no record is dropped or rewritten. The analyzer reads chunked gzip directly. Published preflight/pair replay succeeds without temporary-runtime data. Original raw runtime remains retained. All new review is this thread's self-review, not independent audit. Missing pure numerical-worker split and support/scheduling effects are explicit research gaps.
