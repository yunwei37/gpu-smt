# Exact native tactic sites for timeout diagnostics

HotspotSites.lean uses the pinned Lean4.9 parser and environment to record actual
simp_all / interval_cases Syntax ranges and parent syntax nodes. It processes
only native namespace-opening setup; candidate declarations and proofs are not
elaborated. Other commands/options are recorded and not executed. Arbitrary
source-defined syntax,namespace/section changes or dynamic notation are not
qualified by this preparer. Failures stay in the output.

prepare.py produces three separate all-mode diagnostic inputs for the23original
simp_all-dominant timeout sources: exact original, added-import control, and
added-import plus opt-in profile calls. It checks every native UTF8 span and an
inverse edit back to the original bytes. It leaves all48interval source programs
untouched: closing-continuation integration is a separate semantic task.

[Actual preparation and limits](../../../artifacts/hotspot-mechanisms-2026-10-25/native-sites/result-review.md)
retain73parser inputs(71original+2parser controls),raw errors,all source mappings,
and prepared inputs. Parser success is not a native proof,semantic equivalence,
runtime profiling result or safe early failure predicate. Do not run these
original diagnostic inputs alongside the retained sole full collection.

The profile emits explicit stderr events and must be run through a declared
diagnostic capture which associates the candidate and retains that stream.
Unmodified NativeLean intentionally classifies nonempty stderr operationally;
do not feed these instrumented sources to that backend and count a backend
fault as native logical rejection. Event invocation_byte addresses the
instrumented keyword;the manifest maps it to its original source position.
Original,import-only and instrumented clocks retain separate denominators.
