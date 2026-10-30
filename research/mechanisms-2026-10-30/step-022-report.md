# M step022 — candidate-preserving certificate hooks and native qualification

自审,2026-10-30. This is the implementation/qualification boundary of the user's recovery census, not its completed result. The previous turn changed authoritative source, checked complete grid certificates and audited coverage: classified as progress. Current scope remains M only; root paper/engine is untouched.

Hypothesis: replacing the actual closed computation step, while retaining original preceding/following proof commands, can recover some of the49historical operational failures. A target-only theorem does not establish this. Correct failures/false intermediate assertions must remain errors; a fallback must restore state. The result changes how many of the static49can honestly be reported as recovered sources.

Implemented in CertificateMethods.lean: checked digits/grid family declarations plus closed-cardinality rfl and interval_cases wrappers. A failed certificate attempt uses saveState/restore and disables error recovery **only inside that new attempt**; original fallback tactics retain normal recovery semantics. This is not global native-failfast. All accepted full candidate proofs will be audited for sorryAx. No production engine option is enabled.

## Qualification and failed attempts

- Buildv1: Lean-o source/root mismatch; corrected root declaration for this M module.
- Buildv2: nonexistent liftIOidentifier; corrected to the pinned SDK's liftM.
- Buildv3compiled, but the first49census attempt exposed an unsafe Expr.getArg! before shape validation. Seven native trials emitted a recognizer panic and later reached the finite self alarm; these are **engineering failures**, not seven rejected candidates. The group is partial and scientifically invalid; all raw results retained.
- Own collector SIGTERM remained errno13. To stop safely without changing security, the next never-started own output was reserved with an interruption record; existing finite runner refused it before launching Lean. Controller and all seven native trials actually retired. That reservation is not a native result. The corrected collector also checks its own STOPfile between candidates.
- Buildv4avoids unsafe indexing. Its positive control exposed a second issue: a membership omega subproof failed but ordinary Lean error recovery still let evalTactic return. Native exit1prevented acceptance; a printed HIT was not qualification. The new attempt is now atomic, and membership proof uses propositional decomposition plus arithmetic bounds.
- Buildv5and controls are qualified: one unsupported/reflexive list equality and both correct digits/grid goals return0; both wrong goals fall back and reject. The negative original-tactic/import-control returns1with **exact same diagnostics**, after normalizing only source paths and removing measurement markers. The failed v4control remains intact. No independent review or generic cache/semantic equivalence is claimed.

All new native runs have source maxHeartbeats200000, finite native flags, M8192cooperative process-RSS checking, an internal self wall limit and original-kernel checking. Own outputs are on existing PVC. No security settings, templates, other lanes or upstream code changed. Modules/binaries stay outside Git.

## Recovery49protocol (running, counts pending)

Only the closing standalone rfl token or interval_cases token is replaced. Other original source bytes/comments/tactics remain, apart from importing the checked module, setting a finite200000HB point, and appending an axiom report. Errors in an earlier have block are not discarded. The49ids are fixed from step020, not selected by whether the new method succeeds.

Fresh serial phobos-vt point: CPUs8–11, one native process, -M8192within M16GiB, per-case28s self wall, group1750s/stop before next case after1710s. This is a **different diagnostic resource point** from the historical48GiB/4worker/300s pair. Original outcomes/physical-attempt costs are matched by id and retained; no cross-hardware speedup ratio will be computed. Counts of accepted transformed candidates establish actual proof recovery under this new finite point; still-budgeted cases are censored, not false proofs.

The collector freezes its source/module pointer and retains each candidate/source/receipt/stdout/stderr, partial rows and eventual terminal. Final recovery counts must wait for actual terminal/retirement. No baseline-original rewrite is represented as an unchanged native source result.

## Other requested work while the census runs

Remaining37opportunities correspond to11target-specific proof bridges, not37independent new algorithms. coverage/remaining37-bridge-estimate.csv lists each target, ids, original worker-attempt cost, required mathematical obligations, possible enumeration reductions and rough engineering effort. Estimates are not implemented results, promised schedules or kernel time predictions. Bounds that amount to solving a substantial part of the original theorem remain explicitly high risk.

Next: collect the complete49census; then evaluate automatic routing/misclassification with near-miss fallback controls; then sample typed-distinct openai/math computations with their own Lean4.34.1toolchain. No formal OpenAI native experiment is started before completing the recovery stage.
