# Native context extraction repair — root self-review

The first two32-source observations preserved all28complete/4reject but
every one of13actual arithmetic entries was markedunsupported. This was an
extractor limitation, not zero falsegoals. Source-native diagnostic on original
minif2f-4 identifies the currenttheorem's recursive auxiliary declaration
mathd_algebra_478, kindauxDecl, as the unsupported universal proposition.

Lean4.9 LocalContext.lean documents auxDecl as a recursive-call placeholder,
invisible to tactics/typeclass search, not an ordinary user hypothesis.
The exporter excludes only kindauxDecl and explicitly logs their names. All
ordinary and other implementation-detail propositional locals remain required.
Default-kind induction hypotheses and unsupported constraints are not dropped.
The original goal and original tactic execution stay unchanged.

Also restrict syntactic rational decoding for Nat/Int to integer literals;
Nat/Intdivision remains unsupported, and Nat subtraction stays truncated.
Non-dependent propositional implication/negation is represented as Boolean
implication. Unsupported binders/functions/metavariables retain fallback.
Failedfirstcompiler versions, the library-path diagnostic failure and original
observation bytes are retained. Repeat real32qualification after this repair
before full goal characterization. No GPU acceleration is claimed.
