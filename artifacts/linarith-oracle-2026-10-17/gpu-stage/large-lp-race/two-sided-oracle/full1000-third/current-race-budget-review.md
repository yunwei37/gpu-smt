# Remaining numeric work on the current two-sided CPU clock

Root analysis/self-review, 2026-10-18. Reuse the completed third full1,000 pair;
no new capture, counter transfer, favorable-source selection or GPU execution.
Native Fast/hybrid takes691.359191064s; CPU two-sided oracle464.579050137s.
Their actual ratio is1.488141127x. The three-pair aggregate remains1.508619170x;
one below-threshold pair is not hidden.

There are1,888 unique source/call-ID race records, all matched to native candidate
spans. Whole race durations sum to101.540133002s, including worker startup,
positive/negative exact repair and verification, cancellation and wait. These
are not pure LP timings or a disjoint21.856%whole-wall fraction. Legacy winner
label 'gpu' means CPU HiGHS in THIS CPU-only capture;399positive/335exact-negative
external wins,275CPUpositive and879CPU-no-certificate wins.

The numerical proxy has935parsed HiGHS calls, with9.250980854solver WALL seconds
summed across calls,0.613799433s model-build wall and6.153121071s calling-thread CPU.
There are also467unparsed/aborted connections, preserved rather than assigned
invented LP outcomes. Parsed connection intervals occupy a26.613638757sunion
including receive/build/serialize/waits, not GPU-replaceable work. This entire
view belongs to the464.579050137s acquisition; older stacked-header, hybrid
diagnostic and2,234.69s reference counters are not substituted into this clock.

## Fixed-lane deletion sensitivity, NOT a global Amdahl proof

The critical observed lane finishes at460.437240691s relative to the first
candidate. Its race stages sum to14.109276663s; its parsed HiGHS solver calls
sum to1.882051468s. Keeping observed assignments, non-race durations and gaps,
and deleting ALL race work (including CPU repair/launch/retirement), models a
450.469773474s whole pipeline, only1.031321251x beyond the CPU oracle but
1.534751568x relative to its own native reference. Thus even this deliberately
optimistic model does NOT exclude the requested1.5x threshold.

Deleting only the parsed external HiGHS search models462.696998669s and
1.494194242x versus native. The actual third pair would need3.672922761s less
elapsed to reach1.5x, more than that lane's1.882051468s parsed floating LP search.
This narrow calculation cannot close the GPU route: it omits complete current
product/small-LP attribution, exact-shadow replacement, altered support quality,
contention and changed future scheduling. Race timestamps contain durations,
not complete absolute start/end regions. No scheduler-independent theorem or
measured zero-LP run follows.

## Consequence

Do not spend a full matrix merely accelerating already-fast HiGHS calls.
Further GPU admission must show that its chosen mechanism changes expensive
remaining work after CPU dual certificates, while charging batching, support
repair, Lean proof construction, fallback and retirement. A different
certificate can change proof cost, so faster numerical search alone is not the
only possible mechanism; no benefit from such a mechanism has been demonstrated.
The independent-stream allocator candidate stays rejected; no pool/buffer/
thread grid is admitted. The full29,750 component capture continues frozen.
All four RQs, generality and systems novelty remain open, and this is self-review.
