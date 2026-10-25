# Native hotspot mechanism analysis — root self-review

The83oldtimeouts were fully profiled; source controls retain all7808native outcomes.
No new candidate executed and no runtime/native source was modified.

|Dominant observed tactic|Timeout sources|Distinct tasks|Dominant sampled CPU(s)|
|---|---:|---:|---:|
|simp_all|23|16|6609.025|
|other|12|8|3418.503|
|interval_cases|48|7|13455.672|

|Source pattern (not a failure witness)|All sources|Accepted|Timeouts|
|---|---:|---:|---:|
|mentions_interval_cases|443|132|55|
|mentions_three_or_more_interval_cases|99|17|19|
|mentions_simp_all|2343|666|39|
|simp_all_and_modular_rule_somewhere_in_source|92|35|5|
|simp_all_and_commutative_rule_somewhere_in_source|352|152|7|
|simp_all_and_finite_sum_rule_somewhere_in_source|226|63|4|
|simp_all_and_pow_succ_somewhere_in_source|214|34|6|

## Native source implications

Pinned4.9Mathlib IntervalCases.intervalCases first allocates all cases for
one interval and constructs their bisect proof tree; only its frontend then
introduces/substitutes each goal and returns it to following tactics.
A source range/cartesian count is neither a proof of falsehood nor an exact
300s wall-clock lower bound. Nested tactic evaluation/backtracking matters.

Pinned Lean Simp.simpLoop already stops its post-rewrite recursion when
the expression equals the original (unless other phases recurse). Thus an
unchanged expression after one full root rewrite is already handled by
native Lean; adding that same check is not a new failure mechanism.
Actual time may involve expression growth, multi-step cycles, conditional
discharge or repeated context updates. Current profiles do not distinguish
these; no cycle certificate is inferred from a rule name or CPU category.

Source-pattern accepted controls invalidate blanket rule-name rejection.
Next native hook must retain expression/context/options and whether the
operation is inside a fallback/try/first/discharger before a checked witness
may reject a complete request. Unknown keeps native execution. Keep hooks
off until the existing sole group retires; no shortened timeout is introduced.

The detailed83source/task/timing table is timeouts83.csv. Its observed CPU
denominator is the same profile; original cumulative HTTP/whole-controller
clocks are not substituted. This supporting diagnosis does not close an RQ.
