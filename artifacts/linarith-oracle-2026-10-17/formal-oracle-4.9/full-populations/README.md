# Complete formal candidate populations

[Experiment plan](plan.md), [driver](driver.py), [launch](launch.json),
[one repaired entry failure](repair-review.md), [closed-cell reader](analyze.py).

This finite capture evaluates all original ProofNet and miniF2F candidates.
It runs the stock native frontend, native preprocessing with the same numerical
oracle, and the direct checked oracle. The current run is incomplete; there
is no complete-population speed ratio yet. It is a source-native REPL benchmark,
not an entire upstream Kimina or SHRED service.

The first entry failure returned zero candidates and is retained under
failed-attempt1. Five original ProofNet records contain the literal None
placeholder. The repaired collector preserves those original invalid inputs
using the same full-command fallback as run-prefix.py; it does not repair or
drop them. All resource and incomplete outcomes remain in the population.
