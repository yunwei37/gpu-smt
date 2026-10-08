# Stock module profile observations

profile categories are rounded exclusive same-thread elapsed scopes, potentially overlapping across threads; shares are accumulated-category descriptions, not CPU/exact wall fractions; type checking includes addDecl/auxiliary declarations; import loads compiled dependencies, not transitive proof rechecking

| Module | Repeat | Normal wall (s) | Profile wall (s) | Delta (s) | Diagnostic identity |
|---|---:|---:|---:|---:|---|
| Mathlib/Algebra/Group/Basic.lean | 1 | 3.440295971 | 3.581293684 | 0.140997713 | True |

| Module | Repeat | Cumulative category | Original display |
|---|---:|---|---:|
| Mathlib/Algebra/Group/Basic.lean | 1 | aesop | 21.9ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | attribute application | 4.72ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | compilation | 2.56ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | elaboration | 373ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | import | 211ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | initialization | 23.2ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | interpretation | 1.2s |
| Mathlib/Algebra/Group/Basic.lean | 1 | linting | 31.6ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | parsing | 47.7ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | simp | 423ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | tactic execution | 208ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | type checking | 173ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | typeclass inference | 688ms |

Raw display units/values, unknown categories, CPU/maxRSS, all failures and diagnostics remain in `cells.jsonl`; counts, completeness, issues and paired repeated values are in `summary.json`. RSS is not PSS. No correctness, GPU readiness, Amdahl bound or service-speed claim follows from category totals.
