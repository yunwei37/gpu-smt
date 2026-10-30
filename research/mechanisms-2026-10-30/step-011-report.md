# Step011 — software PC resolution and qualification preparation

2026-10-30UTC;M;self-review. No additional Lean process launched.

EXPERIMENT: resolved the existing standalone200ms C control's100 CPU timer
samples against its actual /proc/self/maps and ELF64 PT_LOAD segments.99
resolve to named native functions,1 remains unresolved. No overflow. This
checks address-bias arithmetic rather than incorrectly treating virtual PCs
as file offsets. Counts are CPU instruction residence,not cycles or PMU data.

WRITE:analyze_pc_samples.py retains unknown modules/symbols and separates
interpreter residence,explicit cold refcount helpers,allocation helpers,
name-identifiable hash tables and kernel routines. Inlined work stays in its
caller; those RC/allocation/hash fractions are lower bounds,not total cost.
Prepared PCMeasureControls.lean for a future native on/off differential after
the current serial cohort retires. It starts the sampler after initialization
and tags only measured bodies. Boxed and unboxed UInt64 FFI phase entries
are both defined; no native qualification yet.

REVIEW: existing C control naturally exited. ELF reader and analysis execute
without Lean or PMU/ptrace. Native sampler must actually engage and preserve
observed diagnostics/flags/InfoTrees/HB before any workload fraction is used.
The active C-timing cohort sources,binary and collector are unchanged.

A133.7ms native C shared-library rebuild exports all boxed/unboxed FFI
entries. Four-case Lean qualifier is prepared but not executed; it refuses
to start until every existing cohort native PID/birth is retired. Native
qualification uses stock,loaded-but-off and on cells with identical source.
