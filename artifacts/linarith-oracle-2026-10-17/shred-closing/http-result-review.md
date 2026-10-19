# SHRED through official Kimina HTTP — root qualification self-review

## Actual closed cohorts

Use unchanged official Kimina app/SDK and the existing Lean 4.9.0-rc1
kernel-checking REPL with the same compiled Mathlib linarith library.
Both methods have eight outstanding sources, four eligible CPUs 4–7,
48 GiB per process and the upstream request timeout. All observed owned
descendants join; no surviving owned process remains.

| Functional cohort | Sources | Native valid/rejected | SHRED valid/rejected | Native complete clock s | SHRED complete clock s |
|---|---:|---|---|---:|---:|
| miniF2F first32 plus all18 unavailable-source placeholders | 50 | 28/22 | 28/22 | 8.432219244 | 15.078467892 |
| ProofNet first32, complete32 block containing first known accepted source, all4 placeholders | 68 | 12/56 | 12/56 | 8.529718206 | 15.200294754 |

Every per-source verification status agrees, with zero operational failures.
ProofNet's additional original block256–287 is chosen to test real accepted
proofs, using the earliest success in the already-closed stock control,
not by timing or cache-hit gain. The earlier first36 ProofNet cohort, which
accepts none in either method, remains separately preserved.

There are non-message differences in the opaque env handle field:
11 miniF2F sources and 16 ProofNet sources. These and all cache/info/warning
messages remain in the full replies and summary. Independent worker
allocation/import paths are not identical session histories. This establishes
verification-result agreement, not transparent snapshot/protocol semantics.

## Actual costs and engagement

SHRED preparation, including the real unchanged native parser and wrapping,
takes 6.8638 s for miniF2F and 6.9702 s for the positive ProofNet cohort.
Both complete clocks include that work, module imports, HTTP transport,
queueing, native checking, fallback and retirement. The cached method is
slower on these small cohorts; no claim hides or amortizes its measured setup.

miniF2F replies expose 25 misses, 24 captures and one hit. ProofNet replies
expose 44 misses, 22 captures, 15 rejected captures and one uncacheable event.
These native information messages are not a complete CPU/LP profile.
The separate single-worker official CLI's four hits must not be substituted
for the actual HTTP pool's one observed hit or treated as causal scaling proof.

The original contexts remain intact. Only the SHRED import and upstream
supported last-tactic wrapper are added. No new namespace is opened.
Unsupported extraction/wrapping, registered syntax exclusions and literal
unavailable-source values follow original native execution and remain
visible. Actual SDK version is discovered from the retained compiler; no
4.27 label is reused for the 4.9 process.

## Full requested baseline

The complete existing-method comparison is genuinely launched: all 5,952
ProofNet originals and 7,808 miniF2F originals in preserved order, native
then SHRED once per dataset, 27,520 source-runs in total. It has no result yet.
This is a requested prior-method baseline; it is not another proposed
CPU-runtime/GPU tuning variant promoted from a losing small preflight.

The source records real preprocessing, every failure/fallback and both
complete wrapper and service clocks. Only after a measured cell retires,
its raw text is losslessly archived to conserve the near-full volume;
the data export is separate from verification clocks. No original record
is discarded or active writer altered. One shared-host fixed order cannot
establish stable global speed, peak aggregate memory or OSDI novelty.

## Reproduce and limits

analyze-http.py reads complete plain/gzip SDK records and receipts; the
published summary names both actual cohort paths. Failed metadata and
driver-name attempts are retained, as are executed-source snapshots.
The public recipes now require a fresh --out directory to preserve runs.

Root self-review checks source identities, all outcomes, returned env/message
differences, real cache events, SDK/native library/resources, charged parser
cost, original contexts and actual retirement. Reviews remain self-review;
no subagent/OMP, independent audit, GPU closure, all-RQ completion or new
cache contribution is claimed.

## First full native condition closes — no paired conclusion yet

All 5,952 ProofNet sources return in the native condition. SDK labels are
417 valid, 5,534 Lean errors and one server error. The native message/sorry
check gives **413 complete, 5,534 rejected, four incomplete and one
operational**, not 417 complete. The SDK treats the four sorry-bearing
responses as valid; raw SDK labels remain intact and derived analysis
exposes native outcomes separately. Earlier functional subsets contain
no such incomplete cases; their per-source agreement still holds.

The incomplete IDs are 2913, 2928, 2933 and 2934. Source5879 has three
recorded HTTP500 JSON-decode errors followed by the SDK's retry failure.
It is counted as an operational failure; memory exhaustion is not inferred.
The complete wrapper clock is356.367363s and warm sweep349.794376s.
All observed owned processes retire. The cached condition remains active;
this single native condition is not a speed ratio or final full experiment.
