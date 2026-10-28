# Step0113 — distinguish a simplifier warning from a failure certificate

2026-10-28UTC; BUILD_AND_EVALUATE; root only, self-review.
This is a bounded primary-source mechanism inspection while the one native
resource pair continues. It is not a new native run, an answered RQ, a complete
novelty survey, or a throughput result.

## EXPERIMENT_GATE

### E113.1 — source question and inspected boundary

Parent: step0108's six repeated-inner-round observations and step0112's completed
resource-contract repair. Read the complete current user-instruction.md and
questions-for-author.md, the latest step report, and the native implementation.
The latest instruction permits simp_all mechanism analysis during collection;
resource parity remains ahead of enabling failure or scheduling gains.
The four frozen RQs and their evaluation promise are unchanged.

Question: can an abstract rewrite-rule cycle or unchanged local-hypothesis
observations certify that the concrete candidate cannot pass? Before building
such a detector, inspect the official implementation and its own contrary cases.
The inspected boundary is the installed4.9 simplifier/target-replacement source
and official Lean issue/PR bodies, not a replay of another system.

Actual searches used GitHub web search and the primary GitHub issue API:
repo:leanprover/lean4 with simp_all+loop, simp_all+target+modified, and
simp_all+infinite. Raw complete selected primary bodies, exact query/result
counts, timestamps and installed source are retained in
[primary-source-observations.json.gz](primary-source-observations.json.gz).
A web fetch of PR8865 timed out; its authenticated read-only primary API body
was actually retrieved. No comments were posted.

### E113.2 — contradiction and method disposition

[Official PR8688](https://github.com/leanprover/lean4/pull/8688) proposed abstract
right-hand-side dependency-cycle detection. Its author explicitly documents
false positives on successful concrete simplifications: another concrete rule
can terminate a putative abstract cycle. This PR is closed and unmerged.

[Merged PR8865](https://github.com/leanprover/lean4/pull/8865) instead warns when
simplifying an abstract rule RHS fails. It is normally disabled, is potentially
costly, and can warn on successful calls. This is a known diagnostic mechanism,
not our new method or a full-candidate failure witness.
[Original RFC5111](https://github.com/leanprover/lean4/issues/5111) links the
same concrete-term escape problem; the stronger initial proposal and the
merged implementation must not be conflated.

[Issue8300](https://github.com/leanprover/lean4/issues/8300) additionally gives
dependent-context examples where repeated simplification makes new progress.
That is not a reproduced failure in our23 sources and does not prove their
observed inner loops terminate. It contradicts a general assumption that a
second call cannot matter. [PR11172](https://github.com/leanprover/lean4/pull/11172)
removed a slow looping suggestion path from try?; avoiding a search branch is
not evidence of an acceptance-preserving whole-candidate early rejection.

The installed SimpAll loop marks progress when simpTarget returns a different
MVarId. replaceTargetEq constructs a fresh goal even when proof-based
replacement does not establish semantic novelty; replaceTargetDefEq separately
checks structural target equality. None of the retained sampled hashes is the
complete target/context/Meta-state. Hypothesis-stable rounds therefore do not
establish the recurrence needed for a sound detector.

Disposition: do not implement abstract-rule-cycle rejection or ID/hash-based
rejection on these23 sources. No native candidate was rejected or accelerated
by this inspection. Continue the concrete-state/continuation question using
the existing source and records; do not add another observer or claim that all
loop-detection research is closed. The broader literature skill was loaded,
but its full-paper reading and full coverage procedure were not completed:
this bounded node must not be labeled that skill's completed novelty map.

Native empirical work remains the already running frozen13d4606 resource pair.
At18:00:44UTC both exact controller529177/birth162169119 and warm child529178/
birth162169125 were live; no terminal existed. Retain that version and its
resource-composition limits. No local compilation, native subprocess,
additional acquisition, watcher or queue was started by this step.

## WRITE_GATE

Targeted update only: link this method boundary from the existing simp23 artifact
README and append today's existing substantive-progress thought. No scientific
authority, narrative, claim, RQ, evaluation number or paper source is edited.
The canonical background/design files remain foreign dirty and untouched;
this is an evidence node, not a second canonical literature map.
The source inspection changes no established paper claim, so no result
propagation or fresh compilation is asserted. The unchanged paper's existing
step0100 compile receipt remains its last actual receipt. Full writing is
excluded by the current phase; milestone review is excluded by open RQs.

## REVIEW_GATE — root self-review

[Outer audit](outer-audit.md) checks this evidence boundary. No independent
review was performed; the user prohibits other executors. Raw primary statements
support rejecting the proposed abstract warning as a sufficient failure
certificate. They do not establish a concrete cycle, corpus coverage,
novelty absence for every alternative, or resource-layer throughput.

Direction: unchanged four RQs, Lean/SMT/OSDI objective and four continuing
directions; no new name or central contribution. Efficiency: this source
question removes a potentially unsound/known detector branch. It does not count
as a new native result. The actual progress diagnostic warns that nine step
directories have appeared since evaluation.md changed. That warning remains
material; do not silence it by touching evaluation.md or call engineering/notes
an answered RQ. Source112's73Rust/6native/38Python controls remain separately
attributed software qualification; no new tests were needed for this read-only
source decision.

Maintenance: no rule, helper, CI job, runtime switch, parser or logger added.
Current ordinary-frontier retry order already has regression/CI coverage, but
does not parallelize its tail. Do not infer a peak memory cap from censored data.
Keep daily notes in their existing owner and preserve foreign paths.

Ranked open issues: (1) full matched warm/native elapsed and accepted/status sets;
(2) resource-composition/retry-order attribution and current source qualification
versus frozen acquisition; (3) original42 solo result at its declared point;
(4) a sound concrete-state/whole-candidate failure witness; (5) broader novelty,
other workload evidence and eventual independent audit remain missing.

Route: retain the healthy full capture until its existing exit event, review and
commit its complete raw/population/resource results, then the fixed42 solo point.
No automatic extra cohort or policy matrix resumes. The goal stays active.
