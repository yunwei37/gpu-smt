# First native OpenAI math sample on phobos-vt

Lean4.34.1 commit5045d005, Mathlibd13f23b7 and its8matching dependency pins.
All raw sources, replay copies, oleans, scripts and logs remain outside Git
under /workspaces/.agent-state/gpu-smt-{workloads,captures}.
Source extraction and cache setup are [separate](../../native-setup4341/README.md).

Four preselected phaseA targets with7internal modules completed:
Laughlin ComputeRow1115Batch17, Ramsey BallSeparation,
Falconer NearPinDeletion, TraceReconstruction Binomial.
All7 compiler exits0, no sorry warnings, no resource interruption observed.
This is4/53targets, not the full probability sample.

New declared replay point:200,000heartbeats, Lean8192MiB memory option,
one Lean process/thread, affinity0–7, autoImplicit=false from original
package options, --profile --stats, olean-only output.
Original sources remain untouched. Replay copies would replace HB0 or
settings above200000; no such source edits occurred in these7modules.
These results do not characterize original unlimited-budget wall time.

Summed individual process wall44.314s. Native collection's own timed loop
44.339s excludes prior dependency-graph loading and environment setup.
Individual wall0.856–35.767s; compiler peak RSS1.67–7.44GiB.
TraceReconstruction Binomial99,800source bytes took35.767s/7.44GiB.
A short2,449byte Ramsey Definitions source still peaked3.61GiB.
Small source does not imply a small imported environment or cheap proof.

module-costs.csv records per-process wait4 CPU and peak RSS, wall measured
with a process-exit event, source/budget/diagnostic fields, PID/birth and logs.
Its RSS is compiler-process peak, not an independent aggregate W-tree peak.
The sampled RSS column is1s and can miss transients; no hard RSS quota claim.
The next batch records aggregate collector/child-tree samples separately.

cumulative-profile.csv contains160reported native phase values. They are
cumulative, may overlap and may exceed the module's wall duration; do not add
them into a disjoint wall partition or global Amdahl bound.
Raw per-declaration profiles are retained. Full tactic-specific attribution
and uninstrumented/profiled overhead are not established by this first pass.
No speedup, full source acceptance or population tail estimate is claimed.

These measured peaks invalidate treating8/24available cores as8/24memory-
admissible jobs under16GiB. Wider native coverage is needed to calibrate
the earlier conditional DAG schedules with real memory admission.
