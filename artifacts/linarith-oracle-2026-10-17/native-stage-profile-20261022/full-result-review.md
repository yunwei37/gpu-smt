# Original1000 native phase result — root self-review

Both cells completed on2026-10-22 under source2/live2,24GiB address limit per
REPL,48GiB sampled whole-owned-tree RSS and four CPUs8–11. Same original1000,
order, native algorithm and frozen dependency build; profile is opt-in.
Frozen whole1448.917480465s versus profile1450.783580374s (+0.128793% in this
single fixed-order shared-host pair). Warm1442.260113324/1444.227663776s;
preparation6.096869766/6.049635332s. This is its own resource point, not a
rescaling of810.713s,2234.69s or the complete29750 population.

All1000 native outcomes and complete raw responses match:992complete,8reject.
There are4095 pipeline records:4093returned,2failed;995sources enter the
profiled arithmetic path,7enter omega, and every source has at least one of
these records. These overlapping counts do not mean all work is covered.
No unknown source join or interval outside its own HTTP envelope. A returned
arithmetic invocation is not itself a successful full verification.

|Stage|Caller thread CPU seconds|Accumulated wall seconds|
|---|---:|---:|
|Preprocessing|105.752261|105.789579|
|Linearization|107.043815|107.055237|
|Nonlinear products|234.073788|234.128256|
|LP oracle wrapper|9.234549|999.359174|
|Certificate construction/check|229.261474|229.327302|

The LP caller thread blocks while the external helper works. Its9.23CPU
seconds do not imply the solver is cheap;999.36wall seconds include packing,
IPC, exact repair and fallback, not pure LP. Products include native proof
generation. Individual spans can overlap across candidates. Product+LP
per-source interval union sums1233.487430810s; global union966.174307931s,
66.596722% of this instrumented whole clock. Neither is removable critical
path. The fixed-envelope optimistic sum-deletion sensitivity6.676527x is
explicitly not a strict Amdahl bound or a GPU prediction.

The frozen-ranked slowest1% (10IDs, allcomplete) has472.090889s native versus
470.548171s profiled overlapping HTTP, including108.730437s LP,0.727133s
products,56.116505s preprocessing,32.090000s certificate and4.219336s
linearization. Slowest10% (100IDs,98complete/2reject) has1322.364939/
1322.060354s overlapping HTTP, LP478.318783s/products73.716802s/preprocess
71.432277s/certificate80.726771s/linearize52.307717s. These are the same
ranked IDs, not isolated tail clocks or a GPU tail improvement.

All failures and raw outputs/memory are preserved. Native/profile sampled
peak RSS15.431351/15.575275GiB,max2liveREPLs,0watchdog kills/errors,no
owned live descendants after cleanup. The monitor samples every second;
it is not a kernel-hard RSS quota. Closed plain logs are losslessly gzipped
with byte-equal roundtrip receipts; existing compressed stage logs are kept.

## Decision and next empirical boundary

The measurement does not rule out1.5x. Continue the GPU route. Before claiming
a useful GPU opportunity, separate the dominant external-helper envelope into
native FP LP solve, packing, exact repair/verification and exact fallback.
Use existing native phase hooks with the frozen hybrid algorithm: the current
race daemon imports a different race solver, so merely relabeling that binary
as the strong native comparator is invalid. Root source comparison found the
canonical hybrid/tiered/verify core differs from the frozen helper snapshot
only by provenance comments and diagnostic guards; preserve that equivalence
when selecting a reference diagnostic mode. Qualify on actual24plus rejected8
before any further original1000 capture; one protected group only.

Remaining missing coverage includes term elaboration before run, omega,
configured/indirect stock calls and records lost under hard death. No unknown
work is set to zero. This is root self-review, not independent audit, evidence
of end-to-end GPU acceleration, project closure or OSDI novelty acceptance.
