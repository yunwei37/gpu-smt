# Official SHRED closing-certificate baseline

This fills an existing-method comparison gap. Earlier root prefix executors
use SHRED's parser/trie rules; they are not the complete official
closing-certificate executor.

- [Plan and admission](plan.md)
- [Unchanged official CLI qualification](qualification-result-review.md)
- [Executed qualification adapter](qualify.py)
- [Official paired report](qualification-official-report.json)
- [All original/cached source pairs](qualification-pairs.jsonl.gz)
- [Complete native wire replies](qualification-wire.jsonl.gz)
- [Service integration and charged preparation](run-kimina.py)
- [Closed HTTP qualification and response differences](http-result-review.md)
- [Actual full-workload launch](full-launch.json)

The first original32 sources return 28 complete/four rejected in each
method, no operational failure and four cache hits. This is functional
qualification, not a population or HTTP speed result. Full raw responses
include env-handle and informational-message differences; only native
verdict agreement is established.

The unchanged official cache module compiles against the already-retained
matching Lean 4.9.0-rc1/Mathlib archive. The archive metadata callback and
wire recorder do not change cache selection/checking. Failed attempts and
all original data are preserved. No OMP or subagent is used.

## Execute in the owning Workspace

The build receipt names the actual retained SDK/module paths. The source
of every original candidate is the existing prefix-opportunity input
archive. qualify.py reconstructs source bytes and uses the official CLI;
run-kimina.py uses the same module/wrapper through the official HTTP app.

```sh
python3 artifacts/linarith-oracle-2026-10-17/shred-closing/qualify.py --out /tmp/shred-cli-replay
/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python \
  artifacts/linarith-oracle-2026-10-17/shred-closing/run-kimina.py --out /tmp/shred-http-replay
```

Each recipe creates a fresh experiment output; preserve existing outputs
rather than overwriting or mixing lifecycles. These are executed owning-
Workspace recipes, not a clean-machine installer. Full population and
equal-resource service claims await the matched real measurements.

For the complete requested baseline, use the same HTTP recipe with --full
and --datasets proofnet minif2f, choosing another fresh output directory.
The actual complete acquisition is running, with no full result claimed.
Source/header preparation and all native fallback are included; opaque
environment handles are recorded rather than normalized away.

Executed-source provenance: qualification-executed.py is the successful
original CLI recorder; http-preflight-executed.py records the first HTTP
source, and http-full-executed.py plus http-capture-executed.py freeze the
actual full-population driver/transport. The supplemental positive ProofNet
run used the intermediate preflight version before --full/closed-cell
archival support; its exact source file was not separately snapshotted.
Its actual commands, all original requests/replies and resource receipts
are preserved. Current preflight mode retains the same positive-control
selection and upstream wrapper semantics.

## Complete ProofNet result

The [full 5,952-source HTTP pair](proofnet-full-result-review.md) is closed:
native356.37s, SHRED373.22s,4.73% more elapsed in this observation.
Both genuinely complete413sources. SHRED changes20rejections to sorry-bearing
incomplete outcomes; SDKvalid must not be counted as verified proofs.
[All outcomes](proofnet-full-comparison.json) and
[cost-weighted events](proofnet-cache-costs.json) preserve every failure.
The full miniF2F comparison continues; there is no whole-family gain claim.


## miniF2F memory recovery

The eight-source full miniF2F native condition is interrupted by actual
host global OOM at03:13:19Z, with eight REPLs totaling114.95GiB anonymousRSS.
All remain below48GiB individual address-space limits. Partial HTTP/server
bytes, kernel receipt and pending source IDs are preserved in
[memory recovery](memory-recovery-20261019/plan.md).
The new matched native/SHRED point uses --concurrency 2, fourCPU4–7,
48GiB per process and unchanged original7808sources. It does not complete
or inherit the failed eight-source observation. The default remains8;
no upstream app/manager or infrastructure setting is patched.
