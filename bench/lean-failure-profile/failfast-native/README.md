# Experimental native fail-fast wrapper

NativeFailFast.lean defines failfast_native followed by a tactic sequence.
It composes existing Term.withoutErrToSorry/Tactic.withoutRecover to investigate
continued work after native recovery records an error. No log,timer,source
predicate,global elaborator or service detector is added.

Definitions compile on pinned Lean4.9. Accepted-set/status parity is unqualified:
keep this outside production. Recovery-dependent custom tactics and nested
elaboration need real differential tests;do not infer semantic equivalence from
compilation. Existing first/try backtracking must remain intact. This is not a
novel primitive or a predictor of nontermination.

[Original23inputs,review and compile evidence](../../../artifacts/hotspot-mechanisms-2026-10-25/failfast-native-20261026/README.md).
Zero proof candidates executed;the declared native collection slot is pending.
