# Independent LP cancellation qualification

This report is a self-review by the root thread.

## Matched 24-source result

| Condition | Whole seconds | Native / condition |
| --- | ---: | ---: |
| Native eight-queue compiled reference | 29.551738559 | 1.000000 |
| CPU AST oracle | 23.475818756 | 1.258816 |
| Independently cancellable GPU jobs | 23.536287725 | 1.255582 |

All 24 sources complete with the same proof IDs, input order, native verdicts
and non-message payloads. The GPU has three warning-only changes on accepted
sources. Actual candidate peak is eight; all processes use CPUs 8–11 and the
48 GiB address-space limit. The GPU is 0.2576% slower than CPU oracle in this
one observation. This does not admit a full 1,000-source GPU matrix.

## Did independent cancellation work?

The pinned cuOpt 26.10 server confirms eight workers sharing one RTX 5090.
Six ready groups each contain two distinct sources and launch 12 single-model
RPC jobs. They are not six fused GPU batches. All six groups have overlapping
client RPC lifetimes, from 0.052 to 0.442 seconds; simultaneous CUDA kernels
were not measured.

Five jobs return results and seven are cancelled. All 12 retire with
DeleteResult acknowledged, and the dispatcher reports zero pending jobs.
In three groups, one job is cancelled while its sibling returns a result.
This demonstrates removal of the original joint-model cancellation coupling.

The 125 labelled races choose 111 CPU certificates, ten CPU no-certificate
answers and four exactly repaired GPU certificates. Of 48 accepted proxy
connections, only 15 contain complete parsed requests: 33 aborted parse
records, ten client-disconnected requests and five PDLP_OPTIMAL replies.
Connections are not LP solves. Cancelled device compute time is unknown.
Returned jobs report 1.465 summed solver seconds, not whole elapsed time.

The complete cold lifecycle is 40.8742343 seconds: 5.8089445 to PodReady,
25.7113788 for the client wrapper, and 9.3520424 for retirement/restoration.
The exact Job UID is deleted; lab is Ready and the other Workspace is Running.
Additional server worker/context memory is not included in client PSS.
Eight workers are a finite benchmark candidate compared with the upstream
default of one, not a retained deployment setting or parameter grid.

## Disposition and next decisive question

Independent cancellation engages but provides no useful end-to-end gain here.
The first 24 sources contain none of the native-selected slowest 1% sources.
The original complete GPU trace contains a fully parsed LP from source 37
waiting 22.548 seconds without GPU submission because the forced two-request
admission gate never finds a companion. This is a concrete admission problem
on a heavy candidate, separate from solver tuning.

The [declared ten-source tail control](tail-admission-plan.md) freezes that
selection, measures fresh matched native/CPU references, and tests immediate
independent admission. It is a tail diagnosis, not another full matrix or
representative final result. Earlier failures remain retained. Neither this
qualifier nor the tail admission record proves GPU acceleration or
impossibility. The GPU route remains open.

The implementation is opt-in. The 24-source run used minimum-ready two.
Later cohort/minimum-ready flag plumbing preserves that default. Actual launch
and job events establish the run's settings; a byte-exact pre-edit runner
snapshot was not captured and is not reconstructed as if it had been.
The default joint-model path and CPU oracle remain unchanged. No independent
audit, full-paper readiness or venue acceptance is claimed.
