# Independent result review: native prefix bootstrap discriminator

Reviewed 2026-10-07T22:03:43Z. This is the fresh experiment RESULT REVIEW, not execution or the outer audit. Read the complete research-experiment-design skill, docs/user-instruction.md, docs/questions-for-author.md, docs/idea-story.md, docs/evaluation.md, current paper RQ2, approved plan and plan review, the executed C++/Python adapters, and analysis code. No solver measurements, source/paper changes or Git actions were performed by this reviewer.

RQ2, unchanged: **Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?** This experiment covers the narrower necessary decision-preservation condition on the retained 156 real VeruSAGE streams, not complete RQ2.

## Separate judgments

- **Run status: valid.** Complete terminal negative discriminator, with retained execution failures. Negative native API outcomes are observations of the tested path, not dropped matrix cells or evidence of superiority. Fresh API, split and branch paths fail qualification against the original executable. Branch transparency relative to the original remains inconclusive because the fresh adapter already fails.
- **Tested hypothesis: contradicted.** The expectation that all three native API paths recover original decisions without added scopes/history is false on five retained streams. The narrower expectation of no additional decision changes from segmentation or fork is supported on this finite corpus, including failing streams; this does not qualify the original-interface contract.
- **Research value: supporting.** Independent causal boundary evidence identifying a driver/interface obstacle and recovery of the old scope/history regressions. Not a headline result, service experiment, smoke-test contribution or final frozen-version evidence.
- **Paper impact: mechanism or workload boundary.** Bounds this stock-library command-evaluation constructor. It does not directly challenge the thesis that some qualified native boundary can improve service performance.
- **Next paper decision:** do not qualify this adapter or proceed to claim a transparent service using it. Route to source-grounded investigation of the CLI/API behavioral difference or a qualified native interface, weighing that work against dynamic Lean profiling. Keep supported fallback/native execution and all failures visible. A rerun or redesign is not authorized by this review. All four paper data RQs remain unanswered by this bootstrap probe.

## Completion, commands and independent recomputation

The exact full execution command, release and hashes are retained in [provenance](../../../../../artifacts/native-branch-2026-10-07/full/provenance.jsonl). Entry point matches plan: `python3 bench/verus_native_branch_probe.py /workspaces/.agent-state/gpu-smt-verusage-20261004/mixed100 --z3 /workspaces/.agent-state/gpu-smt-deps/z3-4.16.0/z3 --libz3 /workspaces/.agent-state/gpu-smt-deps/z3-4.16.0/libz3.so --driver /workspaces/.agent-state/gpu-smt-deps/z3-4.16.0/native-z3-branch --cores 8 --repeat 3 --out artifacts/native-branch-2026-10-07/full`. Full runner terminal exit 0 was supplied by execution handoff; reviewer independently confirms the terminal twelve-condition log and all expected files/status records. Runner exit 0 means collection completed, not solver parity.

Recomputed raw decision outputs using `python3 tools/analyze_native_branch_probe.py artifacts/native-branch-2026-10-07/full`, then independent Python read-only scans of decisions.jsonl, every referenced stdout, processes.jsonl, original/full/prefix/suffix inputs and prior session-replay/runs.json. The independent scan extracted line-anchored SAT/UNSAT/UNKNOWN identities from raw stdout, checked expected source check counts, output and original hashes, source-byte equality, command reconstruction, repeated identities, child statuses, stderr and prior per-input identities. Every stored decision array and stdout SHA-256 agreed with raw recomputation. All six provenance hashes match current executable/library/adapter/analyzer bytes. Original executable hash `e583c4186a45e72411fa2cb2048401eed03f0f8e5f24694676a8f6271a50b765` equals prior replay config, version 4.16.0. No post-run metric/oracle changes were found.

There are exactly **1,872 stream cells** (156 × 4 × 3), **5,280 decision responses**, and **1,410 process records** (468 executable, 468 fresh, 468 split, six branch parents). All 440 source checks are present in every path/repeat, with no missing or short decision sequences. Each of six branch parent logs has its full 106- or 50-child sequence. The middle repetition reverses mode order. The one-stream [preflight](../../../../../artifacts/native-branch-2026-10-07/preflight/summary.json) is separate and establishes only executability; it is not pooled into the result.

## Raw decision table

Counts below are identical in each of three repetitions; all three repeats were independently checked.

| Path | Streams / checks per repeat | UNSAT / UNKNOWN / SAT | Changed streams / checks versus original | Execution failures per repeat |
|---|---:|---:|---:|---|
| Original-byte executable | 156 / 440 | 434 / 6 / 0 | 0 / 0 | none |
| Fresh API | 156 / 440 | 437 / 3 / 0 | 5 / 5 | four exit-2 processes, API stderr/model errors |
| Split API | 156 / 440 | 437 / 3 / 0 | 5 / 5 | same four exit-2 processes |
| Branch API | 156 / 440 | 437 / 3 / 0 | 5 / 5 | four exit-2 children; parents return 0 |

Raw paths: [decision records](../../../../../artifacts/native-branch-2026-10-07/full/decisions.jsonl), [process records](../../../../../artifacts/native-branch-2026-10-07/full/processes.jsonl), [inputs](../../../../../artifacts/native-branch-2026-10-07/full/inputs), [complete log](../../../../../artifacts/native-branch-2026-10-07/full.log). Raw stdout resides in executable-N, fresh-N, split-N and branch-N directories under the full artifact root. No failed or negative row was excluded.

The five changes occur at these source indices/check positions (positions are one-based); every API path/repeat has exactly the same change:

| Index / task | Check | Original → API | Additional observation |
|---|---:|---|---|
| 46 / AC__vreplicaset_controller__proof__liveness__proof__lemma_from_scheduled_to_init_step | 1 | UNSAT → UNKNOWN | complete output, exit 0, no stderr/error |
| 49 / MA__bin_sizes__lemma_div_is_ordered | 3 | UNKNOWN → UNSAT | model unavailable error; exit 2 |
| 73 / MA__bin_sizes__result_sbin | 5 | UNKNOWN → UNSAT | model unavailable error; exit 2 |
| 90 / MA__bin_sizes__pfd_lower_le_upper | 5 | UNKNOWN → UNSAT | model unavailable error; exit 2 |
| 103 / MA__bin_sizes__size_of_bin_mult_word_size | 4 | UNKNOWN → UNSAT | model unavailable error; exit 2 |

For concrete raw comparison see [original 49](../../../../../artifacts/native-branch-2026-10-07/full/executable-0/49.stdout), [fresh 49](../../../../../artifacts/native-branch-2026-10-07/full/fresh-0/49.stdout), [fresh stderr](../../../../../artifacts/native-branch-2026-10-07/full/fresh-0/49.stderr), and [original 46](../../../../../artifacts/native-branch-2026-10-07/full/executable-0/46.stdout) versus [fresh 46](../../../../../artifacts/native-branch-2026-10-07/full/fresh-0/46.stdout). Four model-request errors say `model is not available`. API stderr starts `API_ERROR 4`; its error message includes extensive command output, so stderr is not empty noise. Across repetitions fresh/split have 24 nonzero process records; branches have 12 failed child statuses, raw wait status 512 (normal exit 2). Each affected 106-member parent reports those four failed children, while returning 0. The 50-member group has none. Three branch group stderr files are nonempty. Original executable stderr and process failures are zero.

## Cause, regressions and correctness scope

Fresh, split and branch raw decision sequences match one another on every stream and repetition. No stream changes with repeat order; CLI itself is stable in all 468 executions. Therefore neither call segmentation nor fork adds an observed decision difference to the already different API behavior. This is a causal discriminator, not proof of universal fork safety or native transparency. Error-free decision qualification is 151/156 streams, not 156/156; the fifth difference fails despite exit 0. Complete response coverage cannot cancel either mismatches or model errors.

Compared prior [session replay](../../../../../artifacts/verusage-2026-10-04/session-replay/runs.json) by exact captured trace identity. Its prefix_pool row contains 31 affected streams and 31 changed checks per repeat; these are genuinely both counts, not an assumed equivalence. **All prior 31 recover original decisions in every new API path/repeat. None overlaps the five new changes.** Matching indices are 17,30,31,32,33,34,44,51,52,53,54,57,62,75,76,77,78,79,92,93,94,95,96,101,105,106,107,108,109,113,116. Old cold and warm_reset rows match their expected decisions. This supports removal of the old scope/history perturbation, while exposing a distinct adapter difference. It does not erase prior failures or establish that all behavior now matches.

All 156 retained originals equal the source bytes and declared hashes; reconstructed full command sequences equal each original sequence; an exact retained prefix plus each suffix reconstructs that sequence. The original executable actually consumes original copies, preventing shared reconstruction errors from defining the oracle. Source commands comprise 440 checks, 5 get-model requests, 1,751 get-info commands and 2,196 echo commands; no artifact request was stripped. Original resource-option commands and original scopes remain intact. The corpus's echoes do not create fake decision lines. Command reconstruction changes whitespace/formatting and is therefore not byte identity; it is not separately tested by running a reconstructed CLI. Resource counters, API manager ownership/defaults and frontend treatment remain candidate explanations, not established causes. No stronger causal attribution is justified from these measurements alone.

All five model-request streams are indices 28,49,73,90,103. Original CLI outputs contain no `(error ...)`; the original UNKNOWN reason at these requests is incomplete arithmetic. The four changing model-request streams expose an artifact failure beyond the decision change. Models were retained but not independently validated; the absence of an API error at index 28 is not model-fidelity proof. There are no SAT outcomes and no proof/core requests here, so the corpus cannot substantiate general SAT/model/proof/core coverage.

## Fairness, engagement and limits

The four rows are behavioral controls, not main performance baselines. Their matched release, executable identity, CPU affinity 8, untouched resource options and no added check/scope are fair for the declared decision discriminator. The branch constructor engages native fork from a prepared stock-Z3 context: each of six parents reports one thread immediately before branching, refuses multithreaded branching, and never evaluates candidate suffixes. Two groups have 108- and one-command prefixes; each candidate gets a disposable child, reaped sequentially. This establishes observed quiescence and separation from prior child mutations, not concurrent candidate isolation, cancellation recovery or arbitrary runtime fork safety. Affinity is not CPU isolation. Timings/memory are diagnostic only; no speedup, frontier or device conclusion is reviewed or permitted.

The finite repeated retained published-task replay is not real ordered generated candidate traffic, not a frozen final dataset/version, and not an equal-resource service comparison. Three repeats show observed stability only; no broad confidence bound or universal correctness inference follows. Driver failures cannot be counted as branch wins, and the unqualified driver prevents original-interface branch qualification. This valid negative supporting result narrows the constructor boundary and informs the next scientific choice; RQ2 and every other final data RQ remain open.
