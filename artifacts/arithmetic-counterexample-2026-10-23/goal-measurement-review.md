# Offline goal measurement and comparison-alias repair

The first complete qualification is closed: all32original outcomes agree
(28complete/fourrejected); final13actual arithmetic entries are supported.
Our4096-point vectorized rational-grid proposal pass finds0exact witnesses,
with0proposal errors, in0.030789seconds. This is one theorem's candidate block,
not full-population coverage and not a GPU timing.

The first reviewed full-observation prefix has261arithmetic entries from125
source IDs,123supported entries from75sources,0witnesses and0proposal errors.
It is a partial, nonrepresentative original-order prefix. No-witness means
unknown. Raw unfinished observation remains live and will not be staged until
closed; the derived prefix record is labelled partial.

## Ordinary comparison coverage

Native Lean4.9 Init/Prelude.lean lines1114–1117 defines GE.ge a b as
LE.le b a, and GT.gt a b as LT.lt b a. The frozen first-observation exporter
handles LT.lt/LE.le but misses these unreduced abbreviations. Its raw reasons
include unsupported proposition GT.gt: x > 0; those are extraction gaps,
not evidence of valid goals or unavailable counterexamples.

The next exporter source now translates these two native aliases by swapping
operands, with the existing local-instance rejection. This source-only change
is **not yet compiled or qualified**. The active full-observation .olean,
native library, source snapshot and worker remain unchanged. After that run
retires, qualify the repaired exporter and observe only the affected original
source IDs if full coverage warrants it; retain each version's denominator.
Do not declare the full census complete for the expanded exporter.

Variable division, inverses, transcendental terms, quantifiers and opaque
functions remain unsupported. No unconstrained atom abstraction or discarded
ordinary hypothesis was added to inflate coverage.

## Measurement implementation and scope

point_proposals.py uses existing NumPy only to propose finite grid points.
It invokes no LP solver or external system. Floats cannot authorize failure:
each proposed point is reconstructed from the rational grid and checked by
our worker's exact interpreter against every exported assumption, the negated
goal and Nat/Int domains. Sampling recipes are proposals, not discharged
equations; exact checking repeats them. Errors and no-witness remain fallback.

analyze-goals.py refuses unfinished data by default; an explicit partial
mode reads only newline-complete records and labels its output diagnostic.
Witnesses retain source/entry identity, full typed AST and exact point.
Historical failed-request spans are associations and can overlap, never
current whole-wall savings or Amdahl fractions. A witness in an ultimately
successful candidate can belong to an abandoned branch. Only the current
arithmetic tactic may fail early; outer alternatives must continue.

No GPU prototype or off/on speedup is admitted yet. Next decision is complete
actual-goal coverage, especially failed/timeout sources. Root self-review,
not an independent audit.
