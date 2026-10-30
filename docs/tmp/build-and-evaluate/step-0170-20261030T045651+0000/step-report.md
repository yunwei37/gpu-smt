# Step0170 — AutoVerus frontend/SMT cost from retained full native matrix

BUILD_AND_EVALUATE; all analysis and review by this chat (self-review).
Direct user asks program-verification cost and function reuse opportunity; do not
repeat negative SMT prefix experiments or train source-cost predictors.

## EXPERIMENT_GATE
Hypothesis: solver-only cross-candidate reuse may be limited by frontend cost.
Use all 21,396 retained native cells: 3,566 saved candidates x direct/capture x
three repetitions, already run with --time --time-expanded --output-json.
No native process or new collection is launched. Input is the lossless archived
cells.json.gz, not the reclaimed raw working directories. Matrix identities are
checked for completeness and uniqueness.

Pinned Verus 33269ac source main.rs:176-303 explicitly subtracts SMT from AIR.
Rust total and VIR total are nonoverlapping; VIR child fields are nested.
Unreported timing JSON stays unknown; absent SMT fields stay unknown. Residual
holds unreported work and millisecond truncation. SMT-run is elapsed host time
around solver interaction, not a measurement of pure Z3 CPU.

Direct passes (all-candidate external denominators):
|repeat|external s|native covered s|Rust s|VIR s|AIR excluding SMT s|SMT init s|SMT run s|residual s|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|0|639.238|589.028|80.200|225.126|138.364|19.907|43.213|82.218|
|1|631.215|581.347|79.343|224.564|136.075|19.524|42.162|79.679|
|2|632.607|582.244|79.901|224.489|136.098|19.566|42.239|79.951|

Rust+VIR+AIR is 75.33–75.68% of covered native time. Reported SMT init+run is
9.77–9.87% of all external candidate time; eliminating only these reported
components would yield 1.108–1.110x on this replay denominator. This is neither
a strict application Amdahl bound nor a same-run generation/verification ratio.
SMT-run alone accounts for about 6.7% of external time.

Per pass 17 exit101 candidates have no timing JSON; 341 JSON-bearing candidates
omit SMT fields. They are preserved, not assigned zero solver cost or erased.
Accepted means exit0, not verification-results.success alone. Accepted and
nonaccepted components are separately included in summary.json. Capture passes
remain separate: their AIR cost is larger; no instrumentation denominator is
silently substituted for direct execution.

## WRITE_GATE
New per-cell compressed table and per-pass/group summaries under
artifacts/autoverus-stage-costs-2026-10-30. Standalone reproducible analyzer and
five timer-contract regressions added. Exact source timer definitions archived.
The first opportunity conclusion: caching SMT results alone cannot eliminate the
dominant measured Rust/VIR/AIR work. Function/dependency reuse and generation
ratio require their own source/order audits next; no production cache enabled.

## REVIEW_GATE — self-review
Five regressions and the entire actual retained matrix complete successfully.
No nested total-verify, verification.total, or VIR child is double-counted.
Unknown JSON/SMT data, residual, external startup gaps and repetitions remain
explicit. Current G10 only performs offline analysis, not a hardware comparison.
Source-cost predictor, CPU oracle and closed SMT prefix routes remain frozen.
Preserve unrelated dirty files, raw results and old failure records. No other
agent, UI, security/cron/schedule change or formal collection.
