# Native Z3 frontend construction-order experiment

Owning BOOTSTRAP [step0003](../../docs/tmp/bootstrap/step-0003-20261009T132427+0000/step-report.md), [experiment004 plan](../../docs/tmp/bootstrap/step-0003-20261009T132427+0000/experiment-004/plan.md) and [independent result review](../../docs/tmp/bootstrap/step-0003-20261009T132427+0000/experiment-004/result-review.md). COMPLETE declared156×4×3 native matrix:1,872 terminal processes/5,280 checks/26,352 native response frames, plus separate4cell real preflight. Native errors remain completed negative outcomes.

| Condition | Ordered outcomes per repetition | Native requested responses |
|---|---|---|
| release |434UNSAT/6UNKNOWN|Five model objects; version response has no build-hash suffix|
| source |434UNSAT/6UNKNOWN|Same checks/models/reasons as release;440 version frames differ per pass|
| lazy |434UNSAT/6UNKNOWN|Every non-statistical frame equals source; same explicit release version differences|
| eager |436UNSAT/4UNKNOWN|Six changed checks, five changed models and five changed reasons across seven streams; four model errors/exit1 per pass|

All three repetitions show the same non-statistical behavior. Eager changes checks28/9,46/1,49/3,73/5,90/5,103/4 (ordinal check indices one based); reason request116 additionally changes without a changed check result. Its single returned model28 differs and precedes that stream's later changed check. Models returned after UNKNOWN are native artifacts, not proofs of satisfying assignments. No differing-model semantic validation was done. Strict release byte identity fails at requested version metadata; no normalization hides it. Same-source lazy qualification is narrower than universal release compatibility.

Final [observations-summary.json](observations-summary.json) is recomputed by [summarize.py](summarize.py) from final raw analysis. Initial and intermediate model-shape readouts are retained and invalid for model availability: native universe declarations/comments were wrongly excluded. Final analysis on unchanged raw output observes five model objects per release/source/lazy pass, one eager object plus four errors. Original run provenance identifies the initial analyzer source; [executed-source](executed-source) retains initial/intermediate/final analysis separately. Other runtime source/binary hashes are unchanged. This is a readout repair, not a changed oracle, input or solver rerun.

Original input authority is `artifacts/native-branch-2026-10-07/full/inputs/*.original`: all156 exact captured VeruSAGE streams/440checks. Published proof replay is not generated candidate traffic. No full source frontend, branch isolation, cancellation, service acceleration or GPU claim follows from this comparison.

## Build and identities

Official Z3 source archive URL, exact commit and archive SHA256 are in [source-provenance.json](source-provenance.json). Source extracted to `/workspaces/.agent-state/gpu-smt-deps/z3-4.16.0-source` remains available on the owning PVC. `source.tar.gz`, exact linked executables and object are retained locally but excluded by this artifact's `.gitignore`; they have not been deleted. Existing official release binary is `/workspaces/.agent-state/gpu-smt-deps/z3-4.16.0/z3`; release archive provenance and recovery are in the [prior artifact](../native-branch-2026-10-07/README.md).

From a restored official source archive:

```bash
cd /workspaces/.agent-state/gpu-smt-deps/z3-4.16.0-source
python3 scripts/mk_make.py --staticlib --githash=ddb49568d3520e99799e364fb22f35fc67d887b1
cd /workspaces/repository
bash artifacts/native-frontend-2026-10-09/build-driver.sh
```

The script builds unchanged stock CLI and links the thin [CLI-owned driver](../../bench/native_z3_frontend.cpp) to the same static library and official generated registration objects. [config.mk](config.mk), [toolchain.txt](toolchain.txt), complete configure/build/link logs and three official generated registration sources retain configuration. [binary-hashes.txt](binary-hashes.txt) identifies actual products; a rebuilt binary can differ bytewise, so each run separately captures actual hashes. Only `ctx.m()` timing differs between lazy/eager driver conditions. This is not an API-context repair or a fork implementation.

## Execution and analysis

Use the exact preflight/full commands in the plan; one script evaluates original bytes through four native paths, with no command reconstruction. `--out` requires a new directory. All three complete repetitions are required; separate preflight is not included in the full result. The analyzer's command is:

```bash
python3 tools/analyze_native_frontend_probe.py artifacts/native-frontend-2026-10-09/full
```

Each run retains copied inputs/hashes, native raw stdout/stderr, command/exit/elapsed records, actual permitted CPU affinity, topology/load, source/tool hashes and completion observation. Native `<<DONE>>` echoes align requested responses; exact non-statistical frame comparisons and per-request model responses remain tied to raw byte offsets. Statistical time/memory variations are diagnostic. Elapsed process duration is not per-request latency or service performance. Affinity is not host isolation. The analyzer supports relocated raw directories; preserve original bytes on any reanalysis.

For the executed run, all1,872 observed affinities are[8]. Load observations span2.57/2.82/3.31 before and5.26/3.85/3.58 after (1/5/15minute averages); they do not establish an isolated host. Full native launch was15:34:46–15:39:39UTC as recorded file timestamps, not authenticated timing. No performance ratio is inferred. Independent review reproduces exact response identities and all12 eager nonzero outcomes.

The pending RTX5090 candidate generation Job and all earlier negative/partial measurements are separate, unchanged artifacts. This CPU experiment requires no GPU allocation.

Portable raw archives are retained in Git after independent review; uncompressed working directories remain on the owning PVC and are ignored only to avoid duplicating137MiB. On a fresh checkout, extract `tar -xzf full.tar.gz` and `tar -xzf preflight.tar.gz` from this artifact folder before analysis. Initial and intermediate failed derived readouts are included. SHA256: full.tar.gz `8632d04b957052bd70d52a41d1e83ec90ecb646a69236b7f72d1faf8979e143e`; preflight.tar.gz `4358a570f0fa9f89679243bfaf0018d09a29c25be8a40fca29bf76f0ebaf245f`. Final analyzer snapshot SHA256 is `b9fc82a60d2c3a0e719a852c647b4f0ed492f216daa27c9bcf94a5c620e3d943`. Analysis needs neither the runtime binaries nor lost/tmp dependencies. Original captured input authority for re-execution is recovered by extracting the prior native-branch/full.tar.gz in its original folder; pass its inputs directory to the new runner and choose a new `--out`.
