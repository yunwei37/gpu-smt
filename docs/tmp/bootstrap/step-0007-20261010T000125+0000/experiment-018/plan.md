# E018 — Complete native verification versus a prepared independent CPU checker

## RQ and paper-value admission

RQ4 verbatim: After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?

Role: supporting CPU boundary selection within that RQ, not heterogeneous execution or a headline GPU result. The uncertainty is whether faster independent closure checking remains valuable once normal frontend construction, a reusable imported prefix, standard export, candidate parsing/checking, fallback and cleanup are charged. A published post-export checker ratio cannot answer this; E87's two accepted overlays and E88's resident backend merely qualify an interface. Existing complete formal miniF2F/ProofNet experiments remain the main service workload; this source-native Mathlib comparison cannot replace them.

Hypothesis: independently verifying the imported prefix once and checking only candidate overlays can make the independent closure algorithm competitive with complete native full-snapshot verification. The strongest competing explanation is that native command reuse and expensive frontend work leave too little avoidable checking, while export/representation/branch costs outweigh the cheaper algorithm. Positive complete results would select this boundary as a stronger CPU reference before implementing device checking. Contradictory results would reject this implemented boundary as an accelerator and prioritize work inside expensive frontend/kernel normalization calls. Mixed results retain context-specific boundaries. A negative result cannot rule out all GPU Lean checking: frontend tactics still call native kernel reduction despite skipKernelTC, and neither dynamic device work nor transfers are measured here.

The largest credible story it unlocks is complete verification with a separately checked resident library and independent candidate state, evaluated against competent native reuse before a device claim. Prefix reuse, closure reduction, fork/COW and NDJSON are established mechanisms, not novelty. This adds actual whole-boundary costs to a comparison that published Arena metrics and current service experiments do not supply. It outranks another resident metadata/hash pass because it executes complete declaration checking and includes source construction. It is not sufficient for the ambitious four-RQ system/paper by itself.

## External assets and version boundary

Reuse all 14913 released and reconstructed LeanPolish edits from 24 originally selected Mathlib contexts, including native rejection and incomplete outcomes. Same original Lean4.21.0/6741444a63ee, Mathlib308445d, exact base filenames and candidate bytes, trust0, maxHeartbeats800000, proofAsSorry=false, ordinary runtime. The public producer's tactic-screen labels are not truth; complete native results are the oracle. Dataset selection and scope are already fixed in inputs-corrected/summary.json and prior E008; no accepted-only filtering or new sample after seeing performance.

Official lean4export c77b4f275cb7 produces standard NDJSON3.1.0. Independent checker is sokonanoda7645b1e1fcac; nativeCPU/PGO training on the retained4.21 Init.Prelude, native Nat/String extensions, four checker threads and allow-all axiom policy follow the pinned Arena recipe. This does not reproduce Arena4.34.1 results. Local error/sorry screening remains mandatory; permit-all axioms cannot certify an admitted proof. Source/recipe links: prior E84–E87 and artifacts/lean-cpu-checker-2026-10-13/official-build/official-pgo/recipe-scope.md. Standard whole elapsed/throughput follow official Kimina service benchmarking; Linux proc/PSS semantics govern sampled memory. No instruction-derived Arena factor is transplanted to wall time.

Necessary glue: bench/LeanCompleteBackend.lean runs official native APIs and exporter; bench/sokonanoda_prefix_service.rs adds a prefix/suffix entry around unchanged declaration algorithms; bench/run_lean_complete_backend.py acquires finite conditions and basic outcomes. Original checker source/binary remains retained and restored; no active SDK replaced. Builds and one existing-overlay qualification are dependencies, not independent research results.

## Strongest fair comparator and implemented paths

One main comparator, native-full: ordinary complete native command snapshots from the original checked module, genuine post-import state, complete candidate command/declaration finalization. It represents the competing position that existing logical preparation is sufficient. It needs matched timing on these exact sources; neither cold REPL data nor Arena exports settle it. No cold-launch/uncached-kernel baseline is added.

External-prefix: normal Lean frontend from the genuine imported state with final kernel checking deferred, standard candidate export against immutable imported exporter state, resident CPU prefix parsed and independently fully checked once, and disposable child parser/checker for every new overlay. Every newly added declaration receives the unchanged checker. Imported IDs cannot be rewritten and candidate mutations are not returned to the parent. The parent verifies the prefix and waits for scoped checker threads before branch admission. This is a scoped Linux adapter, not generic arbitrary-FFI fork safety.

Both paths prepare/check the same original public module and use the same success-only exact-source result cache. A cache hit returns an already completely verified result; failures are not cached. Original preparation is charged in each whole condition. The independent prefix contains imported dependencies; actual original-local name intersection is reported instead of the older intent-only field. Export omissions (e.g. unsafe local declarations) and checker declines use stock complete native fallback. Internal/transport failures remain operational outcomes, never proof rejection. Any basic accepted/rejected/incomplete discrepancy invalidates superiority for that comparison; no diagnostic-string campaign or universal equivalence claim is required.

CPU affinity13–16 applies to both complete paths and four external checker threads. Ordinary Lean runtime defaults remain unchanged, LEAN_NUM_THREADS unset. Affinity is a resource boundary, not isolation; E015/E017/E008 and external activity/load remain disclosed. Do not run a second heavy miniF2F worker or disturb another owner. This experiment is version-separated from4.9 formal performance.

## Matrix, metrics and interpretation

One full condition contains all24 contexts/all14913 attempts, with each context in a fresh process so library/candidate lifetime is charged. Three primary paired repetitions, rotated method order native/external, external/native, native/external. Two additional whole conditions acquire one sampled memory/CPU profile per method. Total8conditions, 192context cells, 119304 terminal attempt outcomes. Profiles are not uninstrumented repetitions. Original source order and all duplicates are preserved; no RNG/proving-accuracy inference.

Primary metrics: complete process-start-to-exit elapsed summed over the sequential context processes, terminal attempt throughput, measured whole CPU; candidate elapsed distributions are serial closed-workload service costs, not offered-load p99 claims. Separate whole profiles report total own-tree sampled PSS/private with missing/disappearing process observations, not guaranteed peak. Report paired whole effects and individual repetitions; three repetitions do not support broad population significance by themselves.

All frontend, original preparation, prefix verification, export, parser/representation construction, child setup/checking, fallback and final EOF/teardown remain in the boundary. Lossless witness gzip collection is synchronous and included in observed primary elapsed; timed archival pauses are reported separately. It is observer overhead, not a benefit of the checking algorithm. Do not claim fundamental algorithm superiority or a negative GPU ceiling from archive-inclusive time. If interpretation depends on archival cost, the observed comparison is inconclusive for production speed; a separately timed archive-subtracted optimistic bound can identify a cost floor but is not substituted for measured wall performance. Keep stage times distinct and never sum overlapping thread timers into wall time.

Valid positive: basic outcomes agree and repeated full-boundary costs consistently favor the external path beyond variation/collection ambiguity. Valid negative: the implemented path is slower, with stage/archival limitations disclosed; this bounds this path only. Mixed/inconclusive: workload-specific tradeoff, small/variable effect, operationally invalid comparison or dominant collection uncertainty. No result answers allRQ4, proves GPU benefit or establishesOSDI novelty/acceptance.

## Execution, real preflight and completion

Current built producer: /workspaces/.agent-state/gpu-smt-deps/lean421-complete-backend/build6/LeanCompleteBackend (receipt complete-interface/build6/binary.json). Prefix backend: artifacts/lean-cpu-checker-2026-10-13/persistent-prefix/build4/sokonanoda-prefix, SHA73a3d9ae656169618746af211038bc1ada6dbe2f9e531feaaefda42f2a7868ea. Build failures and prior dependency invocation126 remain raw; empirical plan review1/3 approved and integrated preflight0/3 before actual launch.

Real preflight: original indices143→0→143, two complete ordinary paths, original accepted/rejected/accepted outcomes. It establishes actual preparation/export/backend/EOF engagement only. No manufactured proof mutation, extra thread teardown or diagnostic-string oracle. The plan uses a three-row inputs directory prepared from the original jobs.jsonl, not the old synthetic interface input labels. This is this integrated experiment's preflight, not another attempt of a closed earlier qualification.

Full command (absolute paths; from /workspaces/repository):

```sh
python3 bench/run_lean_complete_backend.py \
  --inputs /workspaces/repository/artifacts/leanpolish-native-2026-10-09/inputs-corrected \
  --native /workspaces/.agent-state/gpu-smt-deps/lean421-complete-backend/build6/LeanCompleteBackend \
  --backend /workspaces/repository/artifacts/lean-cpu-checker-2026-10-13/persistent-prefix/build4/sokonanoda-prefix \
  --sysroot /workspaces/.agent-state/gpu-smt-deps/lean421-native/lean-4.21.0-linux \
  --workspace /workspaces/.agent-state/gpu-smt-deps/lean421-native/mathlib4 \
  --lean-path-file /workspaces/repository/artifacts/lean-cpu-checker-2026-10-13/complete-interface/lean-path.txt \
  --cpus 13,14,15,16 --repetitions 3 --profiles \
  --out /workspaces/repository/artifacts/lean-cpu-checker-2026-10-13/experiment018/full1
```

Full completion requires every declared cell terminal, every source index accounted for, exact input bytes, complete frontend/backend EOF, metrics and basic paired outcomes, followed by one fresh independent result review. Resume only terminal successful complete cells on the same executed version; interrupted cells remain retained and restart whole in a fresh directory. Neither prefix records nor acquisition-completed alone establish validity.

Existing ownPVC has about1.7GB free; plain witnesses are immediately losslessly compressed and native core limit0 is set before every launch. Complete storage demand is not measured yet. Preserve all raw/partial data if capacity is insufficient and report a real resource dependency; no blind deleting other data, invented filesystem threshold or new scientific budget. Runtime has no new memory quota/deadline. Source heartbeat policy is unchanged; operationally stuck/interrupted native execution remains incomplete and is not presented as a rejection or a speed result. No resource request or RTX5090 computation is needed for this CPU comparison; GPU work follows a genuinely useful subsequent experiment.

## Source-preserving PGO repair before empirical preflight
Round1 independently approves supporting admission/executability with the initial profile caveat. Build2 borrowed the original stock profile; LLVM reports27 control-flow mismatches/counts discarded. Keep it as interface qualification, not a fully reprofiled strongest-CPU claim. Instrumented build3 uses identical adapter/parser/range source; the same official4.21 Init.Prelude training file checks1672declarations/exit0, and llvm-profdata merge exits0. Finalbuild4 against that freshly matching profile exits0 with zero hash-mismatch warnings, binary73a3d9ae656169618746af211038bc1ada6dbe2f9e531feaaefda42f2a7868ea. All logs and original sources/stock binary are retained; no scientific input/matrix/metric/oracle change or counter reset. Full/preflight commands now reference build4. Modified suffix entry itself is not represented in zero-candidate library training; shared checking/parser algorithms are trained, and no global optimal-PGO assertion is made.

## Actual integrated preflight and full execution entry
Review1/3 approved. Integrated preflight1/3 retained native completion then a stage-JSON string/int analysis failure, with backend unstarted. Ordinary analysis int conversion repaired it without changing stage meaning, oracle or source. Preflight2/3 completes both whole paths on original143→0→143, all3 indexed basic outcomes equal independent E008anchors (accepted/rejected/accepted), backend EOF and normalprocess exit. Ready only, no mainperformance claim. Actual full1 starts2026-10-13T04:55UTC PID13440 at declared13–16; all192contextcells/119304outcomes remainrequired. artifacts/lean-cpu-checker-2026-10-13/experiment018/full1.launch.json is a command receipt, not a gate/state interface.
