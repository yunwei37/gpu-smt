# Pinned native simp_all phase instrumentation

Opt-in profile_simp_all simp_all [...] keeps the Lean4.9 native simplification
algorithm and wraps initialization, each hypothesis and target phase with
monotonic timing and diagnostic JSON on stderr. Original copyright/license
retained. No global tactic replacement or active-source rewrite.

This is instrumentation to distinguish slow per-expression normalization from
repeated full-context passes in the 23 simp_all-dominant timeouts. Type hashes
are investigation hints only: they omit proof/cache/mvar/context/config state
and cannot establish a cycle. No early failure, timeout prediction, semantic
equivalence or speedup is claimed. The native simplifier already detects an
unchanged post-rewrite expression, so that existing behavior is not our method.
Measured timings include diagnostic overhead and keep their own denominator.

The future testable rejection condition would require a proven repeating
complete deterministic transition state and preserved enclosing fallback
behavior. Neither a keyword nor expression hash meets that condition.

Begin/end pairs expose the phase in progress if a request is later killed.
[Native qualification](../../../artifacts/hotspot-mechanisms-2026-10-25/simp-all-profile/result-review.md)
now executes6native/profile pairs;all statuses match,including rejected and
incomplete controls. It does not run the23original timeouts or establish a
safe rejection predicate. Exact original-source profiling is the next runtime
node once the retained full acquisition releases the slot.

## Original-source attribution preparation

The hook now emits invocation_byte and an argument/context-elaboration phase,
with the inner tactic parsed at binding power2 so trailing <;> stays outside
the wrapper. A too-restrictive max-precedence attempt was caught and retained.
[Exact native sites and23prepared originals](../../../artifacts/hotspot-mechanisms-2026-10-25/native-sites/result-review.md)
map48static simp_all sites to instrumented positions. Final7native/profile
development pairs agree,including a trailing-combinator case. This does not
establish original23runtime behavior or early failure. The newest events use
stderr and need a declared diagnostic capture;they are not an unchanged
NativeLean frontend payload.

## Internal native progress attribution

The opt-in wrapper now delegates the native pre-method result unchanged and
records process-wide progress snapshots at most once per second, including native step
counts and theorem origins already used. Default pre/post/dpre/dpost/discharge
behavior remains selected by the same simprocs. This is diagnostic overhead.
The last observed origin is not proof that the origin is stuck; used origins
are cumulative within the invocation. Hashes are hints, never cycle witnesses.

Run analyze.py with --diagnostics DIR and optionally --preparation pointing
to the exact23-source preparation.json to join original call byte positions.
Missing/unterminated phases remain explicit. This analyzer never rejects a
candidate. The qualification-006 artifacts contain14actual native invocations,
seven matched pairs, with zero status mismatches; this is not execution of
the23original timeouts. Do not infer their bottlenecks or cycle coverage yet.

The progress observer now serializes native Origin.key and tagged Origin repr
directly. qualification006 lazy MessageData names are invalid attribution;
qualification007 is the repaired seven-pair control. The analyzer requires the
exact preparation/terminal source inventory and excludes memory sidecars.
See progress-repair-result-review.md in the existing artifact directory.

## Phase completion update (native runtime qualification pending)

The current source splits initialization into disjoint collect-hypotheses and
ordered initialize-hypothesis spans,and adds the previously unlabelled native
assertHypotheses/tryClearMany spans. Hypothesis names/IDs identify subjects;
action_completed distinguishes returned actions from exception unwinding.
Analyzer max_elapsed_ns exposes the worst observed repeated phase;legacy ends
without the new field remain completion_unknown. An open span stays censored.

[Source/compile/analyzer evidence](../../../artifacts/hotspot-mechanisms-2026-10-25/simp-all-profile/phase-completion-20261026/README.md).
Definition compilation and four diagnostic analyzer tests pass. The old
qualification007source/olean stay retained;its seven native/profile pairs
qualify that older observer,not this update. The changed observer has executed
zero candidate proofs. Native comparison and original23phase timing remain
pending the sole collection slot. No cycle predicate,automatic rejection or
per-lemma causal conclusion is added. Individual phase sums omit untimed loop,
outer logging and service costs and are not an end-to-end denominator.

## Process-wide snapshot cadence (original23 runtime still pending)

The completed480 native diagnostic, restricted to the fixed23 simp_all timeouts,
contains two different observed patterns:9last-open inner simp calls span
143.82–299.86seconds;14span9microseconds–48.87milliseconds after thousands of
completed calls. Eight of the latter sources also have thousands of completed
outer simpAll calls. These are cumulative source counts and censored,
non-atomic final observations,not per-invocation rounds or a cycle certificate.
[Recomputation and retained rows](../../../artifacts/hotspot-mechanisms-2026-10-25/simp-all-profile/process-cadence-20261026/README.md).

The current observer shares only a timestamp across calls. Its mutex is released
before native simplification,hashing and output;it never serializes solving.
Expensive used-origin/entry-hash JSON is emitted on that process-wide cadence,
rather than resetting a timer at each call. Entry hashes describe the entry
state at the start of the currently observed simp call,not completed phase
states. All lightweight begin/end events and measured native action costs stay.
They can still be numerous and add overhead;sampling does not make this
instrumentation free. Hashes and repeated origins never authorize rejection.

Compilation and a clock-only IO control are dependency checks. They do not
qualify native proof behavior or the23original instrumented inputs. The older
seven-pair qualification applies only to its retained source. Actual native
differential qualification and original23phase attribution remain pending.
