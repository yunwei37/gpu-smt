# What the observed counterexamples actually refute

Root-only supporting source/measurement analysis,2026-10-24UTC.
Uses the already-published fixed10325entry partial snapshot, its13exact
positive witnesses and11original candidate files. No new candidate, proof,
GPU run, random search, external reproduction or altered native execution.

## Decision question and actual findings

The human asks how many failed requests contain arithmetic goals that are
actually false. A false current proof obligation and a false original theorem
are different. Relating the already-found witnesses to their original source
resolves that distinction for these positives without pretending to know the
full false-goal population.

All13retained points recheck against the complete captured supported AST.
They come from11failed candidates but only5underlying theorem names:

| Original task | Candidate sources with a witness |
|---|---:|
|mathd_algebra_33|1|
|mathd_numbertheory_430|5|
|mathd_algebra_137|1|
|mathd_numbertheory_5|1|
|amc12b_2002_p7|3|

Of13witnessed obligations,9are wrong auxiliary equalities,3are false/overstrong
introduced bounds, and1uses the original conclusion after the proof has
weakened its context. Ten points satisfy both the original assumptions and
the original conclusion. Three points fail an original existential premise.
Thus **none of these13points refutes its original theorem statement**.
This does not prove every original theorem universally or every failing
candidate sound; it characterizes precisely these known positives.

All11current responses are ordinaryLeanerrors,0timeouts. Count each candidate
once even when it has several witnesses: their cumulativeHTTP21.557487377s
ranges from0.315583888to5.973943029s per source. These overlapping response
spans are associations, not time proved removable or an Amdahl bound. They
are the current observation's clocks, not the earlier historical native sum.

## Concrete source/point explanations

- Source379 asserts the wrong intermediate equality x=25*z/14.
  Its point x=625/7,y=250/7,z=25 satisfies the original equations and
  z/x=7/25. It refutes that auxiliary equality rather than the theorem.
- Sources802,812–815 claim wrong digit values in auxiliary facts.
  The valid original assignment a=1,b=3,c=4 satisfies the original natural
  subtraction/multiplication/distinct-digit premises and a+b+c=8.
- Source938 strengthens a needed bound to575<x using apply le_of_lt.
  The point x=575 satisfies the enrollment equation and original conclusion
  but makes that stricter intermediate bound false.
- Sources2982,2988,2993 claim a=3or5 for consecutive positive integers.
  The point a=4,b=5,c=6 satisfies product=8*sum and the original sum-of-squares77,
  while refuting their guessed auxiliary value.
- Source2323 executes simp only[hx,ht]at* after opening square/cube witnesses.
  The captured contexts contain hx/ht asTrue and omit their original equations.
  Points with n=10or63 then refute introduced lower bounds or64≤n.
  Neither n is a perfect square, so these points fail the original square
  existence premise and are not counterexamples to the original statement.
  The retained native error response itself prints hx ht:True and shows
  subsequent obligations after the earlier arithmetic error.

The machine origin key unsupported_derived_lower_bound in raw analysis means
an unjustified/false auxiliary bound, **not an unsupported exporter case**.
All13are drawn from supported captured arithmetic. No source-family count
is an independence claim about11different mathematical tasks.

## Method and provenance

[Executed analysis](analyze-executed.py) reads original source and the exact
stored rational points. It evaluates each captured AST with the existing
exact verifier, then independently spells out the five original statements'
arithmetic as read from their source. For the existential case it proves the
tested n is not a square using integer isqrt, sufficient to falsify the
original conjunction of premises. This is manual original-statement
interpretation, not a general Lean parser, a Lean proof term or an independent
audit. It does not infer theorem truth from comments or generated prose.

[All11original candidate sources](selected-original-sources.jsonl.gz),
[all13point/origin records](witness-origins.jsonl.gz),
[unique-source ledger](sources.csv), [computed result](result.json),
[actual native2323diagnostic](native-2323-response.json) and
[command/exit](command.json) retain the complete provenance. Current cost rows
come from the already-frozen failure-entry analysis; the original full census
remains untouched. One jointRSSsample records10,009,382,912bytes/max2REPLs,
0kills/errors. It is not a complete peak or hardquota proof.

## Result review and root disposition

Run status: valid supporting source analysis of all known13positives in this
snapshot. The hypothesis that these points refute current proof obligations
is supported. The stronger attribution to false original statements is
contradicted for these exact points. Overall prevalence, full timeout coverage,
native off/on outcomes and end-to-end device benefit remain inconclusive.

Scientific value: supporting characterization withinRQ4, no new algorithm
or performance result. It changes interpretation of the earlier hit count:
hits are concentrated in wrong proof steps across5tasks, not11false theorems
or demonstrated removals of expensive timeouts. Root self-review confirms
the original equations, natural-number domains/subtraction, point bindings,
unique candidate cost denominator and native changed-context diagnostic.
Do not reject every proof of an original theorem from one such witness.

Continue the active original7808observation, collect its complete denominator
once actually closed, then the approved own native24/fulloff-on comparison.
No hook/operator/grid expansion or another point-only run is admitted.
Do not extrapolate this finite partial subset to a global GPU impossibility
claim or close the overall Lean/SMT/OSDI objective.
