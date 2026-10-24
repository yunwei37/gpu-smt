# Detached-client lifecycle repair — real24 qualification, root self-review

The failedfullattempt exposed a runtime lifecycle defect, not an admissible
GPUperformance result. The existing finite client now starts once in its
owningWorkspace with durable stdout, PID/birth launch receipt and owner-only
exit receipt. Replayed short launch calls return the same identity and cannot
start anotherclient. The localcontroller only observes thatidentity with
read-only calls of atmost50s; a failed observer read retries observation,
rather than restarts theclient. Provider cleanup requires the matching
durable exit and actualclientretirement. Uncertaintermination retains the
ownedJob forrecovery instead of killing a possiblyhealthy client.

The first repair startup was rejected before dispatch by the existing
kubectl wrapper's single-quote argument restriction. Root verifies no output/
launchreceipt/client existed, preserves the failure and gracefully retires
only that exactprovider Job. This is command-encoding failure, not a Lean
qualification result. Launch/poll now use the repository's base64 transport.
The failedstartup provider exited0; its logs/UID and cleanupreceipt remain.

Actual repaired24 runs19valid/5Leanerrors inbothcells,17real5090requests,
2exactrefutations, no fallbackerrors or accepted/statuschanges. Warmtimes
4.452784686/4.330936878s are functional qualification only. Bothcellsmax2,
24GiBAS each/48GiBaggregate includingprovider, CPUs8–11,0guarderrors/kills,
allnativechildrenretired. Exactclientexit0, providerexit0/contextclosed,
exactUIDJob/Podgone, cleanupErrors empty. During the live qualification,
root resubmits the actualstartupcommand and verifies it returns the original
PID266606/birth129046511 without a secondlaunch. This is a real replay check;
it does not claim every future networkfault has been exercised.

[Closedanalysis](analysis/result.json), rawHTTP/results/goals/memory,
source/build, replaycheck, durableclientstdout/exit and provider lifecycle
are retained. Source changes affect launch/observation/recovery only:
Counterexample.lean, worker.py, numericprovider and GPUkernel are unchanged.

The fullGPU-only repair reruns all7808sources fromzero and reuses only the
completed untouched nativeoff baseline. The existing analyzer verifies all
7808orderedIDs, closednative resources and same native library. It never
splices2214partialGPUresponses or uses observer timings asnativebaseline.
The failedattempt costs remain separate. GPU-only cold accounting includes
its ownprovidercreation/preparation/validation/retirement; it does not subtract
the reusednativeclock from a GPU-onlycontroller clock.

Rootselfreview checks byte-scope, actualtransportreplay, realnative/device
path, unchanged outcomes/resources and complete cleanup. Self-review is not
independent audit; a24preflight is not fullspeed or provenlong-run reliability.
Proceed with the existing fullGPUrerun, no newalgorithm or benchmark matrix.
