# Outer self-audit

# simp_all native-phase prototype — root self-review

The opt-in module preserves the pinned native Lean4.9 simplification loop and
adds begin/end events around initialization,each hypothesis,and target
simplification. A final unmatched begin in a later killed request can identify
the interrupted stage; no event means the request has not entered that hook.
Round count,entry count,hypothesis-update count and type hashes are diagnostic
hints. They do not include complete context/proof/cache/mvar/config state and
are NEVER used to return failure. No builtin replacement.

First compile fails on Nat.toNat and unconstrained helper universe; raw source
and errors retained. Second compile succeeds. Adding a begin event before each
phase fixes the important limitation that end-only logging cannot locate a
phase killed by timeout;third compile succeeds. First end-only12controls stay
as version-specific evidence. Final12controls(6native/profile pairs) all agree:
4accepted pairs,1rejected,1incomplete. All16begin events match
16end events in these controls;phase records are actually emitted,
not merely mocked. Native proofs execute/check. Fallback/admission retained.

Final control lifecycle36.072264s,combined original-owner/test-tree
1s sampled peak43,020,148,736bytes
(40.07GiB),no48GiB pressure or monitor
errors;no fixed AS cap,CPU11 shares the retained full capture. Test clocks
include startup,logging and completion polling;no speedup estimate. Phase
nanoseconds are control-only,instrumented and not the original23sources'
wall-time shares.

Reliable request-level early rejection is still unresolved. A future cycle
criterion must establish a full deterministic repeating state and preserve
enclosing first/try behavior. Native simp already skips unchanged expression
rewrites. Repeated expression hashes,large expressions,commutative lemmas and
source keywords do not prove failure. For interval_cases,the separate closing
continuation controls show local status agreement only;range size is not a
request timeout proof. Original48/23sources remain unmodified and await the sole
population slot. No frozen CPU oracle or comparison reproduction.
Root self-review,not independent audit.
