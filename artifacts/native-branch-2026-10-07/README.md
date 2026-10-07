# Native Z3 branching discriminator

This is a complete bootstrap compatibility experiment, not final frozen-version
paper evaluation or an end-to-end serving speedup. All156 retained real VeruSAGE
streams/440 checks run in four conditions, three repeats, with the middle
condition order reversed. Original-byte executable execution is the oracle.
The complete matrix terminated normally, preserving API errors and child failures.

| Condition | Ordered decisions per repeat | Compared with original CLI |
|---|---|---|
| Original Z3 executable | 434 UNSAT, 6 UNKNOWN | stable on all440 checks |
| Fresh library command driver | 437 UNSAT, 3 UNKNOWN | five stream/check differences; four streams with API/model errors |
| Same driver with split calls | 437 UNSAT, 3 UNKNOWN | same differences and errors |
| Native prefix parent and disposable children | 437 UNSAT, 3 UNKNOWN | same differences and errors |

All5,280 planned decision responses are retained. The differences already occur
before branching. The library driver is therefore not a faithful replacement
on this corpus, and these timings do not establish transparent acceleration.
The independent result review and interpretation live in
[experiment-001](../../docs/tmp/bootstrap/step-0001-20261007T212930+0000/experiment-001/result-review.md).
No model/core/proof validity, cancellation, concurrent service or complete Verus
speedup claim is made by this probe. Some original UNKNOWN paths request models;
their raw API errors must not be hidden by a matching response-count total.

Code: bench/native_z3_branch.cpp and bench/verus_native_branch_probe.py.
Recompute: `python3 tools/analyze_native_branch_probe.py artifacts/native-branch-2026-10-07/full`.
Pinned build/run commands and source-native oracle protocol are in the plan.
The official Z3 release archive is
https://github.com/Z3Prover/z3/releases/download/z3-4.16.0/z3-4.16.0-x64-glibc-2.39.zip
(SHA-256 7288c49a5bd6dbafd7b0b0d1f65956b91672da24b08f09242919af159be3418e).
Its executable e583c4186a45e72411fa2cb2048401eed03f0f8e5f24694676a8f6271a50b765
matches the prior Verus baseline exactly; library hash
11f030cbec893022acd2b348aae925e40a6543eb86c744429c65e2128444a9f7.
Compiler: g++ Debian14.2.0-19; Linux7.3.0-070300rc3-generic. Affinity8 was in
the observed3.2GHz maximum-clock group, distinct from CPUs0–7 at3.7GHz.
Affinity is not isolation; no performance ratio against earlier runs is claimed.

`preflight/` is a separately retained one-stream engagement check. `full/`
contains exact original and derived command inputs, raw output/error files,
parent/child statuses, sampled smaps, commands/hashes and per-input identities.
Portable archives were produced after independent review; uncompressed
working evidence remains in the owning Workspace. Earlier31 pooling regressions
and the original task/source archive remain under artifacts/verusage-2026-10-04.

For a fresh checkout, first extract both retained archives here with
`tar -xzf full.tar.gz` and `tar -xzf preflight.tar.gz`, then run the analyzer above.
Extraction is unnecessary in this owning Workspace, where both raw directories
remain intact and ignored only to avoid duplicating 161 MiB in Git.
SHA-256: full.tar.gz `135709a9624de2366577d768711f29c059eb53395cc0e68ec9da9eb096a2bf7a`;
preflight.tar.gz `82f8f3b05f2ff9c65a450adff4afd52ab405fb5587fe398aadbd73846dbb7b6c`.
Raw record paths remain relative to each extracted artifact root; no lost /tmp
build is needed to recompute completed decisions. Re-execution requires the pinned
Z3 release and the input traces described in the experiment plan.

To restore the runner's source input on a fresh clone, create a new empty input
folder, extract `artifacts/verusage-2026-10-04/mixed100-raw.tar.gz` into it,
and copy `artifacts/verusage-2026-10-04/mixed100/runs.jsonl` to that folder's root.
The older archive contains `inputs/`, `traces/` and logs but not `runs.jsonl`.
Pass this folder as `run_dir`. Release ZIP members are
`z3-4.16.0-x64-glibc-2.39/bin/z3`, `.../bin/libz3.so` and `.../include/`.
The build/run plan uses those files copied into the retained agent-state
`z3-4.16.0` directory. An equivalent installation can use different absolute
paths, with matching include/library/rpath arguments and the recorded hashes.
Choose a new empty `--out` for every re-execution; the runner refuses overwrites.
Its historical `full` command identifies the executed run and must not be reused
against the retained result directory.
