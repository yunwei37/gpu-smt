# First exact arithmetic counterexamples — partial observation

## Evidence and boundary

This node answers feasibility only. The reviewed snapshot has839 actual
arithmetic entries from363 source IDs,474 supported entries from169 source IDs.
Two entries have exact witnesses. Both source IDs failed in the retained
native run. Neither was a 300-second timeout. Their historical reported bodies
sum 2.922152 seconds and overlapping request spans sum 3.052911067 seconds.
These are associations, **not eliminated work or current whole-wall savings**.
The full 7,808-source observation and current final outcomes are pending.

Raw query entries are copied verbatim into first-witness-entries.jsonl.
The original typed AST, exact points and entry/source identities are retained
in partial-coverage.json; first-witness-exact-recheck.json records a second
root exact recheck of every hypothesis, domain and false goal. This is
self-review with the same interpreter, not an independent/kernel audit.

## Two concrete goals

minif2f-379 has Real variables x, z, y. Set
x=625/7, z=25, y=250/7. All exported assumptions hold, including x!=0,
2*x=5*y,7*y=10*z,x=5*y/2,y=10*z/7.
The attempted intermediate conclusion x=25*z/14 is false: its right side
is 625/14. This is a false arithmetic subgoal, not a declaration that the
original benchmark theorem is false.

minif2f-802 has Nat variables b, a, c. Set b=3,a=1,c=4.
All are distinct digits in 1..9; a+b=c, truncated(11*a-b)=2*c,
c*b=12*a and a=1 all hold. The attempted goal b=2 is false.
Native Nat subtraction is interpreted as truncated subtraction, not integer
or real subtraction. Only this tactic may fail early; outer alternatives stay.

## Sampling quality and interpretation

The same4096point proposal pass now records numeric domain/full-hypothesis
and counterexample-proposal counts.281of474 supported entries have no
floating proposal satisfying all hypotheses, including 75 entries associated
with historical failed sources. These are float-filter counts, not exact
feasibility proofs. Equalities such as a^2+b^2=1 and arithmetic roundoff can
make a grid miss satisfying assignments. Therefore no-witness is unknown.

The snapshot emits 7,917 float counterexample proposals; 5,770 undergo exact
checking before per-entry early success, yielding two exact witnesses.
No proposal error is recorded. This is a small CPU characterization pass,
not GPU execution, throughput or a new external baseline.

The full per-source ledger preserves all 7,808 expected IDs, with unobserved,
unsupported-only, supported-no-witness, proposal-error and witness classes.
No-observed-entry includes not-yet-observed and already processed sources
without an entry; it must not be used as a completion-progress counter.

## Disposition

Keep the full own-method observation running with frozen source and the
existing 48 GiB total / 2 × 24 GiB budget. The two cheap failures establish functional
opportunity but do not yet justify a useful device-speed claim. Complete
coverage/cost accounting, especially expensive failures/timeouts, then
qualify comparison-alias extraction and measure the own GPU screening path.
No external-system reproduction, new full acquisition or Agent is started.
