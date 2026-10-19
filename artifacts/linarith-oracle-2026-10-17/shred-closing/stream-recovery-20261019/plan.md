# miniF2F service-stall repair within the existing RQ3 comparison

Role: dependency of the admitted whole-population native/SHRED baseline.
This is not an independent experiment, acceleration mechanism or new RQ.

## Observed failure and retained evidence

The existing two-source native capture stopped producing HTTP responses although
both Lean children were waiting for another command. Two host-side read-only
py-spy samples put the service's active main thread in Rich.highlight_regex,
via synchronous response-body logging before REPL release. Its event loop
could not schedule normal HTTP completion/timeout. The same closed server
log contains asyncio LimitOverrunError from long single-line responses
read through the default 64 KiB readline boundary. The original kernel,
process and HTTP records remain intact, including failed attempts.
No new global OOM was inferred from this stall.

## Minimal declared mutation

Keep the retained Kimina fb2393d archive and native Lean/SHRED code. Apply
kimina-transport-logging.patch inside that existing dependency: disable only
Rich's heuristic regular-expression highlighting using NullHighlighter;
preserve message content, log level, syntax logging and traceback settings.
Read stdout in ordinary chunks and preserve exact blank-line-delimited frames
including coalesced following frames and EOF partial lines. There is no new
response size limit and no timeout, solver, memory, cache or kernel change.

Both comparison arms must use this same declared patched application. A fresh
full method starts from source zero; its clocks cannot be spliced into the
interrupted unpatched capture or the older eight-source results. This repairs
service execution, not Lean proof semantics. Previous completed data remain
their own historical application epochs.

## Qualification and continuation

The actual StreamReader test exercises >200 KiB native-style JSON at its
unchanged 65536-byte default limit, coalesced replies and EOF. This is only a
protocol check. The real end-to-end qualification uses the existing official
SDK/HTTP capture, native compiled Lean 4.9 and the existing SHRED integration:
all first32 original miniF2F sources, all literal None controls, the first3
prior HTTP-failure sources and the actual source2518 logging stall.

Run real-preflight-executed.py with the existing Kimina venv Python.
Both arms retain two outstanding sources, CPU4–7, 48 GiB per process, no core
dumps, original300s per-request timeout/retry protocol and fallback behavior.
Compare real returned source identities, complete/rejected/incomplete/
operational outcomes, native responses and completed process retirement.
Existing pathological candidates may still fail resources; expose such
failures instead of demanding their acceptance or calling an HTTP500 a proof.

After qualification reaches terminal status, retain all outcomes and start
the existing full7808-source native/SHRED pair once in fresh outputs, then
the already admitted unfinished CPU matrices in the existing sequential
continuation. Do not duplicate active collectors or start agents/schedulers.
A protocol test, process launch or partial prefix cannot close the full pair.

## Decision and limitations

A repaired real source2518 response and absence of the observed framing/
highlight stall establish only execution engagement. A remaining fault is
reported separately. The full pair, not this selected cohort, determines
RQ3 performance/applicability. All four RQs, the original CPU/GPU criterion,
GPU/Amdahl limitations and systems novelty remain unchanged.
Reviews are root self-review under the user's explicit single-thread rule.
