# Source occurrences versus retained proof-helper units

Reconciles the completed363-object native census with the exact source.
The1,354,379whole-tree decide+kernel total is lexical, not a count of
kernel computations. In the363compiled modules there are42,886lexical
occurrences and45,661retained helpers matching our auxiliary-name/proof-head
predicate. Native Expr grouping gives42,610globaltypes/44,164summed per-file
types. The population count and compute time remain unknown.

Two concrete source-side multipliers:
- Jet50:944explicit kernel sites;3,938matching helpers, all3,938distinct
native Exprs. Source lines343–346 use interval_cases followed by<;>decide.
- Canonical240:114explicit kernel sites;600matching helpers,600distinct
Exprs. Source line22 nests fin_cases on two indices before<;>decide.
A single source tactic site can act on many instantiated goals. Branch
syntax is observed; the exact per-event/helper correspondence was not traced.
AuxiliaryGram has1matching helper but0explicit kernel occurrences, so the
retained shape predicate is not an exact attribution to explicit kernel
syntax. Other tactic/elaboration paths cannot be excluded by this census.

Native counts are retained declarations after elaboration/cache use. They
are not pre-cache requests, cache-miss events, actual kernel timing or full
failure-replay keys. Equal types across modules do not establish dependency,
private/exporting/universe/state/budget equivalence. In particular, neither
45,661/1,354,379 nor a global type reduction is a justified cache hit ratio
or speedup. The modulo-type census cannot replace a runtime work measure.

All rows small derived data; original native census/raw sources remain on
PVC. Source pin4eaee875; examples:
https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/lean/OAI/MathematicalPhysics/Transonic/Certificates/Jet50.lean#L343
https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/lean/OAI/Analysis/MutuallyUnbiased/PairSemantics/Canonical240.lean#L22
