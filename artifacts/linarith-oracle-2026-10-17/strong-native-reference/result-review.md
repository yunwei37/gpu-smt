# Completed strong native reference — root self-review

Frozen1000heavy-source Goedel cohort, native Fast/hybrid plus product reuse,
logicalCPU12–15, original source order/width4/native defaults as declared.
All1000original sources return:992complete/8rejected, zero operational failures.
Whole2282.741330131seconds includes native preparation, verification, logging
and normal EOF/exit0. This is a baseline observation, not acceleration evidence.

Raw complete native JSON, clocks, source ids, process events and resources are
preserved. Reference computation/code is unchanged by the subsequent fix to
the unused direct-oracle fallback branch. The reference is reused; later
paired reference repetitions use the corrected common library. First-pair
build/epoch lineage must remain explicit, not silently called identical builds.


## Resource and batch-latency analysis

The closed reference has2,387.679575sobserved collector/waited-child CPU and
8,724,948,992bytes peak sampled PSS including the collector. Its250original-order
four-source batch observations have P50=5.477865328s, P95=25.845076767s and
max=111.771771764s. Whole-run2282.741330131sremains the primary denominator.
Batch latency includes a shared wait for every source in the batch; these are
not individual proof times or online serving SLOs. Process accounting covers
the collector's observed waited-child boundary, not an assertion that every
external-grandchild CPU second was accounted. Complete raw resources remain.
Exact values are in cell-summary.json.

The revised comparison analyzer requires unique original source ids, their
frozen order and complete native responses across both methods. Qualification
uses the actual mixed Real/Nat four-source outputs and the separate strong
profile, with zero full-native-JSON differences. No timing win follows from
that diagnostic equality check or from an unfinished prototype.
