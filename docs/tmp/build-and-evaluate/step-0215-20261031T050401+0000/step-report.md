# Step0215 — import latency and resident-page composition
Phase BUILD_AND_EVALUATE; self-review (自审), not independent review.
Current characterization contract and four RQs preserved.

## EXPERIMENT gate: completed read-only analysis
Question RQ2: does the fresh compiler floor reflect substantial imports, and
does per-process RSS imply rebuilt mutable memory?
Reviewed O957feb9/e25fd64/fd348df startup matrix and Mcf49a93historical summary.
Root independently reads81native records,81stdout/stderr,78exact source/control
texts,81PID/births,81artifact sets and39smaps series. No new native process,
sampling campaign, privilege/host/CronJob mutation or other-lane file edit.
Startup6476terminal iscompleted; actualPID absent;81native identities retired.
Preflight1is excluded.39builds/39imports/3Mathlib return0without stop.
13targets are conditional historical<5s within26completed A draws,
not an independent probability sample or the whole source population.

The raw-derived summaries match O published CSV medians. Median import/build
0.682098 and ratio of module-median sums0.677724 remain distinct.
Import0.711834/1.354781/3.195465s min/median/max;Mathlib3.001778s.
39import controls medianRSS3,264,128KiB;sampledPSS3,251,007KiB;
median file fraction92.88898%;anon243,472KiB;majorfault total0.
All sampled components use the same per-run RSS-peak sample; median components
are not combined as one fictitious process. Private_Clean is not a proof
that mmap pages cannot share. Actual multiworker sharing remains missing.
NativeCPU205.945162s/native-wall194.168151s;observer+phaseCPU54.044838s
is visible and not subtracted. Low-overhead calibration is pending.
Root recomputation0.042s/maxRSS14796KiB
on22–23;0native launches. Healthy native/profile queues preserved.

Historical26systemCPU concentration independently recomputed: top2=84.11266%,
top3=89.38815%; comparable highRSS control haslow systemshare.
No getrusage/allocator/futex causal profile or no-M speedup promoted.

## WRITE gate
Added measured instrumented13module import controls and a simultaneous-sample
memory table to existing finding5. Preserved the original whole-process floor
and missing low-overhead calibration/cold-cache/retained-environment controls.
Added descriptive historical systemCPU concentration under existing finding4.
Updated pending result language precisely; no new title/RQ/story change.
No total-build extrapolation from conditional imports or claimed removable67.8%.

## REVIEW gate and outer routing
Self-review checks source provenance, all denominators, startup-only terminal,
hardware/artifact settings, heavy observer cost and mapped-page interpretation.
A completed submatrix does not mean O'sreplay/perf/calibration chain completed.
P-core serialization holds native timing; root paper compilation/analysis on
Ecores22–23 does not acquire/start a second native capture.
M/O/W paths are read-only. Existing40GiB/root4GiB allocation remains.
RQ2 is partially answered, causal and calibrated results remain open.
Next integrate actual final calibrated import/kernel/perf data, not another
status loop or duplicate native run. Complete data/failures remain onPVC.

## Actual verification/publication
Compilation, visual inspection and owned-path publication append actual receipts.
Before push pull--rebase without autostash; preserve foreign dirty work.
Normal push only if fetched remote is ancestor; no force/reset/amend.


## Actual completed verification

Root reanalysis takes 0.042 s and peaks at 14,796 KiB. No native verifier runs. Full Tectonic0.17.0 compilation exits0 in 2.164 s; sampled own-tree peak is 188,796,928 bytes on CPUs22–23, below root4GiB. All citations resolve and no overfull boxes appear; underfull warnings remain. The compiler retires naturally. No new speedup or visual/publication acceptance is claimed.

## Completed visual/source verification
Full source compiles with all citations resolved and no overfull boxes.
PDF8pages/110,952bytes; updated evidence pages3–4 rendered and visually
inspected. Tables fit, memory units/median distinctions and pending
calibration caveat remain legible, with no overlap/clipping. Existing RQ
meanings, section hierarchy and citation sequence exactly match7cf0d75.
Tracked main.pdf refreshed from this build; no stale PDF delivered.
Root starts0native verifiers. Main native timing lock/other-lane work untouched.

Initial Git diff-check catches default csv.writer CRLF line endings as
trailing whitespace before any commit. The two root-produced CSVs are
normalized to LF and parsed row contents verified unchanged. Initial
failure receipt is preserved; no native rerun or paper-content change.
