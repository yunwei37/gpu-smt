# Native simp internal-progress attribution — root self-review

The source-native phase observer now also reports progress from within native
simp, with original call mapping, hypothesis/target slot, iteration, used
theorem origins and native step count. Every custom pre callback returns the
unchanged default pre result; other native methods are preserved. This
observes proof work rather than substituting a solver or adding a failure rule.
The initialization phase may not reach the progress callback. A nonreturning
native reduction after the last snapshot remains unattributed beyond that
phase. Cumulative origins are not individually timed/blamed and repeated
hashes do not certify a rewrite cycle.

Compile007 failed on MessageData.pretty; actual source/log retained.
Compile008 succeeds with the pinned API. qualification006 executes14native
frontend invocations (seven pairs), all matching expected statuses including
rejection, fallback, admitted and trailing-combinator controls. Seven profiled
controls emit12internal progress snapshots. Combined owned RSS peaks at
14,217,093,120bytes during these controls, with no monitor error or pressure
kill. This includes the untouched existing acquisition, is sampled1s rather
than a hard kernel guarantee, and is not an isolated speed measurement.
The attribution analyzer consumes those real logs with zero malformed,
unmatched or open phases; exact per-control theorem sets are retained.
Earlier raw source/attempts and qualifications are preserved.

The23original sources and48instrumented simp invocations are already prepared
by source-native byte offsets; none is newly executed here. No original23
stage/lemma distribution or certified failure fraction can yet be claimed.
Only one population collection runs; do not overlap that group to obtain
the missing diagnostic data. The closed-tail0/71rule remains frozen.

Next actual collection order is the user's latest: after current complete
scheduler pairing, collect/push, then native/prepared four-worker48GiB dynamic
population pair, then actual lean-mlir bv_decide. Original simp/interval
diagnostics remain pending runtime nodes, not completed by these controls.
No CPU oracle, external system variant, subagent, new scheduler or resource
quota is introduced. Scientific contract and four directions unchanged.
