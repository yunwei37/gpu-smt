# Complete ProofNet native/SHRED HTTP pair — root self-review

All 5,952 original sources finish in both methods, 11,904 source-runs.
Native takes 356.367363 s and SHRED 373.219730 s including actual input
preparation: **4.7289% more elapsed time** in this one fixed-order shared-host
observation. Warm sweeps are 349.794376/358.674736 s. There is no speedup
or confidence interval, and failure classes differ.

| Native verification outcome | Native | SHRED |
|---|---:|---:|
| Complete | 413 | 413 |
| Rejected | 5534 | 5514 |
| Incomplete / sorry-bearing | 4 | 24 |
| Operational | 1 | 1 |

The genuine complete-source sets are identical. Twenty sources change from
rejected to incomplete; all twenty have cache-hit messages. None of their
original source files contains a literal sorry/admit token. The SDK instead
labels these twenty as valid, just as it already labels the four original
incomplete responses valid. Raw SDK counts 417/437 valid remain preserved,
but **437 is not a verified-proof count**. Lean still reports the sorry
warnings; this is not evidence of kernel unsoundness. Native outcomes are
derived independently from recorded native errors/sorry information.

All20changed IDs, all5,743non-message env-handle differences and all5,946raw
reply differences are in proofnet-full-comparison.json. Source5879 fails
with recorded HTTP500 JSON-decode responses in both conditions; it is not
attributed to memory without evidence. All observed owned descendants
retire,12per method, and every original ID/error remains.

## Measured method and boundaries

Use unchanged official Kimina app/SDK, matching4.9SDK/Mathlib archive,
the already-qualified kernel-checking REPL and same compiled Mathlib
linarith library. SHRED's cache module/wrapper and registered exclusions
remain unchanged. The HTTP integration distributes requests across actual
warm workers, unlike the upstream single-theorem paired CLI component.
Eight outstanding sources share four CPUs4–7,48GiB per process. This is
eligible affinity, not exclusive resources or an aggregate memory quota.

Both complete clocks charge input reading, source transformation, imports,
queueing, native work, fallback and process retirement. SHRED's actual
native-parser preparation is8.420395s; native preparation is0.069011s.
Each closed cell's raw text is archived losslessly only after measurement.
Export is separate from verification, and no active data are touched.

This is the as-integrated existing-method control, not an unmodified
published SHRED deployment, global CPU optimum or whole-family conclusion.
The full miniF2F comparison continues separately. This negative observed
result does not close GPU work, the original selected-Goedel continuation
criterion, the hourly task or the four-RQ systems objective.

## Cost weighting before another mechanism

Recorded SHRED events are3692miss,1653capture,1126capture_rejected,
186uncacheable,84hit and one application_rejected.
Hits occur on47complete,17rejected and20incomplete sources.
Of1653captures,1333come from sources not complete in both methods.

Recorded wall-timer sums are4.135205s key construction,1.371853s lookup,
801.745555s generation,0.521894s capture and0.152446s application.
These overlap across requests and are not CPU or removable whole wall.
Thrown/failed generators without terminal events are unmeasured, not zero.

Grouping only by reported hash buckets yields99repeated capture buckets,
288capture occurrences and64.676644s of optimistic redundant generation
wall after retaining the cheapest generation per bucket. This is a relaxed
diagnostic, not structural-key/proof compatibility or a scheduling bound.
The largest bucket's71.059618s comes entirely from three incomplete sources
2913/2928/2934. Restricting to sources complete in both methods leaves
52repeated buckets and6.031379s of the same relaxed cumulative-wall proxy.
Both all-outcome and complete-source views remain in proofnet-cache-costs.json;
neither is an Amdahl upper bound or a reason to discard failed records.

The first miniF2F32 component's four CLI-hit IDs have the same decision-key
sequences under HTTP, but only one is an HTTP hit. That observation alone
does not prove a major placement opportunity: duplicate captured-generation
wall in the tiny HTTP cohort is0.245074s, and keys are hash observations.
No new cross-worker cache/placement prototype is admitted from these counts.

The large generation sum on ultimately failing sources motivates a narrow
diagnostic question: was an error already visible before that final tactic?
It does not prove that ordering. Lean's error recovery is enabled by default
and its no-recovery primitives already exist; using them is not new systems
novelty. Any continuation-suppression control must first show real matched
preflight benefit and retained native outcomes before another full matrix.

## Review and reproduction

analyze-http.py reproduces every source classification and exposes SDK/env/
message differences. analyze-cache-costs.py reproduces all event sums and
relaxed hash-bucket views from public closed records. No source is excluded.

Root self-review checks5952unique original IDs, per-source complete sets,
twenty changed incomplete outcomes, all retries/failures, actual resource
and retirement receipts, fully charged clocks and event-timer limitations.
This is self-review only. No independent audit, OSDI acceptance, new cache
contribution, strict GPU impossibility or completed RQ1–RQ4 claim is made.
