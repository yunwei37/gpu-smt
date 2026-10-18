# Actual full-population entry repair — root self-review
Attempt1 stops before returning any source because the selected64 all had
matching headers, but complete ProofNet includes sources whose original code
does not begin with the associated header. AssertionError/zero-source failed
cell and exact executed driver remain under failed-attempt1, excluded from clocks.

Use the already-established run-prefix.py rule: if a four-source chunk contains
a nonmatching header, execute each unchanged original full code with its own
imports and no injected adapter/header environment. All three conditions use
the same rule; unsupported/malformed/missing-header sources are preserved,
not repaired into valid sources. Matching headers continue native batches with
the common extra module. No source/dataset/deadline/correctness changes.
The repaired full capture starts from the first original in all conditions.
