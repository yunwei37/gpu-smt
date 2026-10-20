# Arithmetic source comparison and baseline implications — root self-review

Observed UTC: 2026-10-20T06:17:54.013329+00:00. Client date:19October2026(America/Los_Angeles).
This is a bounded follow-up to the existing novelty map, not a new paper story,
independent review, full literature milestone or performance experiment.

## Claim questions and coverage boundary

The unchanged RQ4asks when heterogeneous execution improves complete verification
after preparation reuse over the strongest measured CPU path. Read the current
evaluation, user/author constraints, original narrative and arithmetic method/
evaluation/related-work statements before accepting any wording change.

Three hypotheses are checked without coined names:
1. Is external arithmetic search with native checking a new mechanism here?
2. Which part of the current direct certificate route differs from the pinned
   competing implementation, including its expression/type coverage?
3. Does the strongest measured4.27adaptation establish superiority to an
   unchanged latest upstream implementation or to every solver?

Coverage is exact Farkas baseline source and official protocol, Mathlib's
oracle/verifier interface at the measured revision, and the official LP tactic
family as a direct-certificate same-mechanism threat. No GPU-impossibility claim,
new RQ, workload replacement, solver grid or new full collection is admitted.

## Search node

Queries used:
- site:github.com/lucifer1004/farkas "power" "Fast"
- site:github.com/lucifer1004/farkas "proof" "reconstruct"
- site:leanprover-community.github.io/mathlib4_docs "linarith" "oracle"

Indexed Farkas queries were sparse; switch to its known pinned primary repository
and documented lean/ subdirectory. Initial guessed root Fast.lean/toolchain and
docs/design.mdURLs returned404, not evidence that the implementation is absent.
Correct pinned files below resolve. Mathlib reference docs and LP official source
provide independent architecture/fragment checks. Secondary search hits and
unrelated same-word results are excluded from source conclusions.

## Primary-source verification node

| Primary source | Verified fact used |
|---|---|
| [Farkas README at5a38a7e](https://github.com/lucifer1004/farkas/blob/5a38a7e8502213cb644faa2e11a15429f0cf0f9a/README.md) | External exact search, numeric hypothesis selection and restricted native reconstruction pre-exist this project. |
| [Pinned Fast.lean](https://github.com/lucifer1004/farkas/blob/5a38a7e8502213cb644faa2e11a15429f0cf0f9a/lean/Farkas/Fast.lean) | parseForm/parseCastFormhandle literal exponents0/1/2and otherwise use opaque atoms; numeric nonlinear products precede restricted stocklinarith. |
| [Pinned toolchain](https://github.com/lucifer1004/farkas/blob/5a38a7e8502213cb644faa2e11a15429f0cf0f9a/lean/lean-toolchain) | Upstream targets Lean4.31.0; our recorded build is4.27.0/db93fe16. |
| [Pinned protocol](https://github.com/lucifer1004/farkas/blob/5a38a7e8502213cb644faa2e11a15429f0cf0f9a/docs/protocol.md) | External daemon coefficient requests/replies are an existing interface, not a new service abstraction. |
| [Mathlib measured-source Frontend](https://github.com/leanprover-community/mathlib4/blob/a3a10db0/Mathlib/Tactic/Linarith/Frontend.lean) | Untrusted coefficient search and native contradiction proof reconstruction are already separated. |
| [LP tactic README at8663429](https://github.com/leanprover/lp-tactic/blob/86634295a1fa2b45110a680215e208b16f40cd33/README.md) and [Atomic.lean](https://github.com/leanprover/lp-tactic/blob/86634295a1fa2b45110a680215e208b16f40cd33/LPTactic/LP/Atomic.lean) | Direct external-certificate-to-kernel-checked proof construction is available in another established tactic family; its input fragment differs from arbitrary nlinarith bodies. |

GitHub public commit metadata is checked live, not inferred from directory names:
Farkas HEAD is still5a38a7e8502213cb644faa2e11a15429f0cf0f9a,
committer time2026-07-05T05:29:08Z; LP tactic HEAD is86634295a1fa2b45110a680215e208b16f40cd33,
committer time2026-08-26T13:00:43Z. These are code identities, not publication
or acceptance dates. Current Mathlib reference documentation is not substituted
for the measured-source revision. No dependency/toolchain is upgraded.

## Local source comparison

[PowerOracle](../../../../../bench/lean-native/linarith-oracle/reproduction/lean/GpuArithmetic/PowerOracle.lean)
exports literal natural powers as an ASTnode, and the
[untrusted Rust frontend](../../../../../bench/lean-native/linarith-oracle/reproduction/native/src/bin/arithmetic-batchd.rs)
expands rational polynomials and returns selected coefficient/origin records.
PowerOracle.realize/checkCertificate reconstruct referenced assumptions,
squares or products, build their weighted sum, invoke the native arithmetic
discharger and assign the resulting contradiction proof. Equality goals may
need two branches. It does not remove kernel checking or imply a single
check per whole source.

The direct solve explicitly restricts its carrier to Real/Rat. The shared
[IntegerPowerOracle wrapper](../../../../../bench/lean-native/linarith-oracle/reproduction/lean/GpuArithmetic/IntegerPowerOracle.lean)
and fallback include the existing omega/CostBaseline path. Therefore the
natural-exponent direct coverage is not a strict semantic or type-coverage
superset of the competing implementation. Unsupported cases remain paid work.

The source-level contrast is returning a usable selected certificate/origin
description rather than using it only to select a restricted proof-producing
run. That run can repeat normalization/search; the source
establishes a restricted stock call, not a fixed count of completed oracle
invocations on every input.
The former unconditional paper wording is corrected to this conditional fact.

## Coverage, contradiction and novelty decision

Generic external search, exact checking, numeric preprocessing and lazy
construction have high same-claim risk. The current local composition's
incremental data do not establish a novel systems principle, new arithmetic
logic, first external oracle, or first deferred proof construction.
Literal-power support extends this direct fast path; it is not the first time
Lean can prove such polynomial goals. Native fallback already matters.

The plain systems ambition remains unchanged: consequential independent
verification beyond competent warm/cache/snapshot execution at equal resources,
with meaningful measured heterogeneous benefit where it exists. This review
does not replace that ambition with an easier solver/compilation claim.
A differentiated service mechanism and complete all-RQevidence remain missing;
a selected-cohort CPU win cannot fill them.

## Baseline/experiment handoff

Keep the already admitted matching native-reference family and original29,750
protocol. The exact4.27adaptation, native product reuse, omega and numerical
configuration must remain visible. Its1.70059xselected1,000and1.05863xDSV2
results retain their original contexts. They are not ratios to upstream's
published4.31clocks or an unchanged execution of that release.

LP tactic is a citation-only mechanism precedent, not an extra numerical
main baseline: its tactic syntax/fragment and types differ, and a direct
nlinarith substitution is not established. Do not create a reimplementation
or weak failing row just to increase baseline count.

The completed four-way block already compares native/reference backend,
native/candidate backend, old direct and natural-power direct. Its component
ratios remain informative, with old instrumentation/recording limits; it does
not causally isolate every part of the final reduced-diagnostic/new-resource
implementation. Existing all-call gaps and absent demonstrated extraGPUgain
remain. Do not invent another local kernel or close all GPU routes from this check.

Next decisive action is the already-running whole-population service
comparison. No new acquisition follows this literature node. On completion,
consume its full outcomes/whole clocks and actual resource boundary, rather
than treating this source comparison as final research acceptance.

## Canonical updates and limitations

Append only this root-owned short source-comparison pointer to the existing
background file; preserve all pre-existing unrelated author modifications
unstaged through partial-index staging. Add a concise provenance pointer and
the official LP artifact citation; correct only the local conditional-search
and coverage wording in the existing manuscript sections. No title,
Initial Narrative, RQ, thesis or contribution changes.

All checks and decisions are root self-review, not independent audit.
Primary source inspection verifies the described code paths, not execution
cost, code reachability frequency on every input or an accepted venue result.
