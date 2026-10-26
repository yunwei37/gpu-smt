# Executed native stream contract — root self-review

Exact faa2a0f passes engine and benchmark-smoke. Existing pinnedLean4.18 CI
actually executes all4native contracts. The source contract now consumes
completion-order accepted/rejected Init records,checks original indices and raw
native response envelopes,requires Complete(count=2),and checks process retirement.
[Native job log](native-contract.log.gz) and [exact-source receipt](receipt.json)
retain executed evidence instead of local compile/ignored markers.

This supports these small native protocol controls. It does not measure native
stream latency,client-wire delivery,full population parity,source forecasting,
a reliable failure witness or a system contribution. Body/process fixtures and
the old scheduling matrix remain separate evidence at their own scope/resource
points. Root self-review is not independent audit;the sole fullpair stays frozen.
