# Actual failure cost relative to the arithmetic hook

Root self-review of the already-retained immutable snapshot. No new native
run or external-system comparison is made. The existing native SDK classifies
4048currently returned original source responses as1541valid,2446Leanerrors,
19timeouts and42resource failures. No repeated response or missing result is
observed. The full7808observation remains unfinished and in-flight requests
are outside this currently-returned subset.

## Cost and coverage

| Current response | No arithmetic entry | Unsupported entries only | At least one supported entry |
|---|---:|---:|---:|
|Lean error|1298|880|268|
|Timeout|13|5|1|
|Resource failure|41|1|0|
|Valid|940|145|456|

The corresponding source identities, HTTP spans, first-entry delays and
supported-entry-to-response tails are in response-entry-costs.csv.
Failed responses that have a supported entry account for cumulative
548.075916s of13350.250439s failed-response HTTP spans
(4.105%). These spans overlap and include
waiting/transport. This fraction is conditional entry coverage in a partial
instrumented cohort, not a whole-verification Amdahl bound, eligible GPU
compute, avoided time or a full-population result.

Five timeout cases reach only unsupported expressions. Their original
reasons include variable exponentiation, Nat.gcd and divisibility. The old
observer also lacks GE aliases, while later source support is compiled only
for future runs. Thirteen timeout cases never reach this hook, which does not
prove a different hook could not help or identify the underlying slow phase.

The one supported timeout is minif2f-806, with948entries.945are closed
numeric contexts from interval_cases expansion. Full-context exact checking
finds no counterexample there. Its initial goals repeat given digit bounds,
and inconsistent branch hypotheses admit no refuting point. Expensive proof
failure is not equivalent to a false supported arithmetic goal.

## Implemented consequence

Across the entire snapshot2349supported entries from27sources are closed,
39.66%of5923supportedentries.2333have at least one false exact hypothesis,
and16have allhypotheses true and a true goal. None is exactly refutable.
The future worker evaluates a closed supported AST once onCPU rather than
send4096identical points toGPU. A possible exactlyrefuted closed target still
returns the same ordinary tactic failure. Unsupported/nonclosed handling
and native fallback remain unchanged. This is semantic constant evaluation,
not a new CPU solver, competitor, cache or sampling threshold.

The real2349entry worker replay forces modegpu without a provider endpoint.
Allanswers use cpu_closed, allagree with exact verification, and no fallback
or network request occurs. Combined exactclassification/control elapsed is
0.084486s. This is a functional data replay, not claimed speedup or complete
Lean native-outcome equivalence. The active observer retains its old frozen
worker; only future qualification/pairs use the change.

Joint monitoring sees peak15363866624bytes,
max2actualREPLs and0kills/errors. No third REPL, new full group, deviceJob,
quota/permission change or Agent is created.

## Root disposition

The decisive gap is coverage of costly failures, not GPU point throughput.
Finish the approved full observation, then qualify the existing own off/on
native path and measure its full effect on the original candidates. Keep
unsupported/no-entry/no-witness separate. Do not expand operators, broaden
the hook, create more narrow kernels or label this partial analysis a GPU
impossibility proof. AllfourRQ and the OSDI-quality research goal stay open.
