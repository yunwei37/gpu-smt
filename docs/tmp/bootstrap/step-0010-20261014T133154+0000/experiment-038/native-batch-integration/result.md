# E038 matched native batch integration and real preflight

Root, observed2026-10-16. Same open RQ3/BOOTSTRAP experiment; not the full matrix or a speedup claim.

## Implemented and executed

Both methods now use the identical retained Kimina4.27 GC/header-repaired native REPL.Main and result extraction. Candidate uses its gc=true path over env0; stock uses its existing runBatchVerify naive path. Candidate returns the same ordered native response array with the same blank-line framing; branch metadata goes to separately drained stderr. This removes the earlier streaming/array and snapshot-extraction differences. Stock is the main competitor; off is only the component control.

Frozen binaries/DSOs are batch-frozen-v1/{plain,private}; frozen-paths.json, actual build/relink scripts/JSON and native-lake-env-compatibility.json retain the exact toolchain/source/link/environment evidence. Both shared runtimes include the same original shell.cpp for native lake env. The first link failed on an encoded module initializer; generated actual symbol fixed relink. That failure remains in build-driver.log and original executed build script. Later per-command same-name entry/link receipts reflect the repaired relink; the first private-link JSON was overwritten, so the driver log and original build script are its surviving failure evidence.

## Actual failed preflights

Preflight1 is FAILED collector setup: _read_response returns bytes but write_text expected str. No proof batch ran. Its three missing responses comparing equal printed True, which is explicitly invalid evidence. The byte capture and complete-array predicate are repaired in preflight2/3; originals retained.

Preflight2 is FAILED native-policy setup: all three real24-input batch paths abort134, failed to create thread, after env0 preparation. Core mapping evidence puts stock's12,879,224,832 virtual bytes within5,677,056bytes of the existing12GiB RLIMIT_AS. The cgroup process ceiling was distant. No candidate win is inferred. Core dumps remain at the recorded private /tmp paths; repository evidence includes original native stderr, terminal data, driver and parsed mapping observations rather than gigabytes of dumps.

Common finite repair: before unchanged Repl.start, all methods inherit the current parent RLIMIT_AS(-1,-1). No thread/default flag, batch width, source, persistent settings or resource service changes. This is explicitly a matched native-batch experiment under inherited Workspace address space; it is not default12GiB Kimina service-policy equivalence.

## Preflight3 completed real original-source batch

All24 original source IDs are retained, common import lines blanked with original positions preserved, no selected successes. All three full native response arrays match exactly, including error/warning/sorry payloads. Each path returns24 elements, exits0 and reaches ordinary stdinEOF/native finalization. No private fallback occurred. Private metadata proves actual engagement:62,678,594ref accesses,1,061versions,5,616descendant tasks. Off reports zero ref versions. Counters do not themselves establish arbitrary source isolation.

| Method | Complete seconds | Batch seconds | Waited-tree user CPU s | Waited-tree system CPU s | Sampled peak PSS bytes |
|---|---:|---:|---:|---:|---:|
| stock native batch |18.187631345|13.894735747|34.882652|1.951628|1,980,578,816|
| private runtime branches |26.865098890|22.560584338|55.618291|81.207349|1,990,606,848|
| branches off |18.596853699|14.431149537|36.383443|2.815159|1,990,184,960|

One finite preflight observation: private whole time47.71% slower, batch62.37% slower, with no visible memory advantage. Whole includes native lake env, imports, all responses, stderr/resource handling and normalEOF. CPU is actual RUSAGE_CHILDREN waited totals per method; it is not proven exhaustive for arbitrary detached descendants. PSS/RSS are one-second process-tree samples, not exact peak bounds. Native preflight bytes/default and effective policies remain separate in raw terminal JSON.

The62M-class global-registry lock path and much higher system CPU motivate a contention explanation, but this preflight has no causal futex attribution. It provides no population/repetition uncertainty, full-corpus success rate, joint frontier, service concurrency coverage, GPU gain, novelty proof or completed RQ. Do not promote24inputs to a formal complete benchmark result.

## Disposition and remaining execution

Root accepts the independent protocol follow-up's stronger baseline, grouped-emission contract and common address-space repair. The actual third preflight now satisfies its complete-array/EOF condition. The OMP-owned full runner must still be delivered/read and its effective policy, failure retention, CPU/PSS and full source coverage inspected before the already declared29,750×3methods×3rotated blocks start.

Preserve this unfavorable setup; no narrower GPU kernel or CPU-compiler claim follows. Full trusted-corpus results will decide this constructor under the stated contract, with all operational and native outcomes retained. General FFI/extensions/global state and persistent interactive handles remain unqualified. The complete Lean-first/SMT/RTX5090/research-paper goal and allfourRQs remain active.

## Public collector source integration — 2026-10-16T23:20Z

Root directly takes up the retained, unpublished OMP-authored bench/lean-native/run-native-batch-comparison.py; no OMP/model/session is resumed. The original authored source is preserved as cli-author-input.py. Static comparison with the exact executed full-command finds three real public-CLI defects: --orders remained a JSON string instead of nested method orders; a cell exception bypassed terminal.json because its write followed the finally block; preflight recorded booleans without comparing native responses. Root decodes JSON in argparse, persists the cell terminal inside finally and compares the complete index/ID/native-response tuples after rejecting missing/operational responses. A one-method preflight says comparison not tested. This changes no running acquisition code, frozen runtime or native policy.

Import/help/actual nested-order parsing pass using the existing Workspace Python; cli-help.stdout/stderr and cli-validation.json retain receipts. Source parsing and lifecycle/control-flow inspection are self-review. No new native preflight or full collector was launched while the original full acquisition runs, and this CLI has not independently completed its native full matrix. Do not transfer results from the one-off command as if the CLI itself had run. No new performance conclusion or independent review follows. The public script remains experimental and tied to declared frozen-v1 composition, not the newer first-write implementation or a clean-machine reproduction claim.

## Completed original stock cell — 2026-10-17T00:11Z

The preceding preflight/future-launch wording is historical. The exact already-running one-off matrix now has one terminal stock condition:29750rows,23292.792530s,26499complete/2291rejected/960operational. All40operational batches hit the original300srequest deadline;960grouped response rows are censored, not individually rejected proofs.40owned workers end−9through failure cleanup; the last reaches normalEOF0. [Complete raw/control reconstruction](../../completed-native-and-profile-20261017T001153+0000/README.md) preserves every file and original launch/input association. Other methods/repetitions remain in the original valid acquisition; no full-matrix ratio/result is inferred.

Source-native batchVerifyParrallelNaive directly executes runCommandGCAux; the BatchCommandstructure lacking gcdoes not make stock a non-GC or snapshot-accumulating baseline. No source/runtime restart follows from that ruled-out explanation. Collector CPU and waited-child CPU are measured scopes, not exhaustive cost of40killed descendant trees. Heavy observerCPU cannot be subtracted to manufacture native performance; sampled PSS has no unsampled-peak guarantee. The completed cell is frozen eager-v1, not current first-write code or public-CLI execution. Full result review and independent audit remain missing.
