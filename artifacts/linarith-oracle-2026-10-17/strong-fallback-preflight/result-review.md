# Correct strong fallback qualification — root self-review

Actual frozen-cohort sources: Proof00009/00027 and Nat-heavy03101/03444
(original proof ids in input.jsonl). All four return complete, with zero full
parsed-native-JSON differences. Fast/hybrid77.304s; corrected direct
oracle78.354s, a diagnostic preflight without a measured gain.

The direct path engages8times.507unsupported/missed invocations go through the
same Fast/hybrid/product-application fallback as the reference; actual fast/
product telemetry confirms that fallback runs. The private oracle remains
untrusted and successful coefficients are checked natively once.

The previous prototype's stock fallback was an implementation/comparator defect,
not evidence that the arithmetic mechanism fails. Preserve its partial data,
do not mix its clocks with the corrected prototype, and do not rerun the valid
completed1000source native reference. Corrected full prototype is now running.
