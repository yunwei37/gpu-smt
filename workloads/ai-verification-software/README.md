# Public AI-generated verification software

Pinned public workloads inspected 2026-10-31. No candidate generation, agent
invocation, native verification or P-core measurement. Preparation/analysis ran
on E8-15 within W's16GiB allocation. Specifications, scaffolds, model programs
and reported outcomes are separate observation units.

## Available outputs

| Source | Public input | Public model output in inspected artifacts |
|---|---|---|
| [Vero](https://github.com/sunblaze-ucb/vero/tree/0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09) |43multi-module instances,743APIs/2705specs;640active Lean files/2,942,815B |No current evaluation candidates/trajectories found in complete main tree or release assets; legacy13-file BankLedger solution has unestablished model provenance |
| [Vericoding data](https://github.com/Beneficial-AI-Foundation/vericoding-benchmark/tree/387cd69996792d452ead7b0460f36ee4c5cdd148) |12504specs:7141Lean/2334Verus/3029Dafny |3342program snapshots, separately55397outcome-only records |
| [Vericoding code](https://github.com/Beneficial-AI-Foundation/vericoding/tree/b265a3b2bce31e09d264306f419e810d02f98f44) |Same benchmark family |1503model-tagged Lean snapshots;45Verus/Dafny tables with16025final outcomes and14109nonempty programs |
| [AlgoVeri](https://github.com/haoyuzhao123/algoveri/tree/8e313b0e8110a781009d4b67ca93b3771b5dc9db) |77aligned tasks with3language specs |No model outputs in inspected main tree, official HF files or release assets |
| [LKV](https://github.com/facebookresearch/lean_kernel_verify/tree/129e65bfd8efbf6c45710732d205c941ef65928c) |90concrete KIR fixtures/481125B;12Lean checker files/189413B |Released checker inputs, not an identified LLM candidate stream |

Vero's live project site returned HTTP403 from the Workspace: its downloadable
output audit remains incomplete. The scoped finding above is not an
Internet-wide absence claim. Six Vero test-fixture Lean files are outside the
listed scaffold/reference scopes. Its1456Git blobs include a17-byte symlink;
the archive mirror has1455regular files, not a lost Lean source.

## Outcomes and overlap

The55397v1outcomes cover6336task IDs and9models:16404publisher successes and
38993failures. They contain neither code bodies nor per-request durations.
They are final experiment outcomes, not every repair/verification call.

The45detailed tables contain Verus3839rows (527success/3312failure),
3819nonempty programs; Dafny12186rows (9254success/2932failure),
10290nonempty programs. They expose final code, feedback and prompts, not a
complete intermediate-candidate history. No Lean table was found. Empty
outputs are missing, not zero-cost jobs. Selected runs cannot be weighted as
all55397experiments. Diagnostic keyword classes are descriptive; zero matching
budget keywords does not establish zero timeout cost.

The1503Lean snapshots contain1490distinct byte strings. All626primary Lean
program texts are included, so do not add these collections. Primary1754Dafny
and962Verus snapshots exactly duplicate the corresponding code-repo copies.
TaskID+model associates1354Lean files with a publisher success;149lack a
matching row. This is not native acceptance. Some sources contain sorry/unsafe
tokens, retained explicitly. Primary filename-only joins also retain missing
and failure-only associations; they cannot determine one snapshot's verdict.

## Static structure and method

scope-summary.csv separates role/language/unit, with bytes, size quantiles and
scan coverage. The1503Lean model snapshots contain simp3672occurrences in1220
files, rfl967/693, omega168/71, decide152/87, native_decide5/4, grind4/4;
bv_decide and decide+kernel are0. These are identifiers, not executed tactics
or CPU fractions.

Vero's active internal import chain reaches35files; LKV reaches7. Independent
Lean snapshots have within-input depth1. External Mathlib/Std closure depth
is excluded, so this does not mean one-module total builds. Each candidate is
a separate graph context; models are not linked by task name.

Lean masking reuses the existing scanner; Verus/Dafny masking removes nested
C-style comments and ordinary strings. This is lexical, not a compiler parser;
raw/verbatim string corner cases are a limitation. Unterminated-comment scans
retain errors/missing counts rather than native-failure or zero-token labels.

LKV has0masked-code native_decide identifiers but1raw source occurrence in its
generated-proof template. No wrappers were generated here. Its checker FAIL
can be a successfully established violation, distinct from Lean rejection.
The prior complete same-pin90-fixture inventory was re-parsed. No model origin,
native timing or compiled axiom closure is inferred.

## Versions, licensing and preparation

Vero's43active instances pin Lean4.29.1. Seven share Mathlib
5e932f97dd25535344f80f9dd8da3aab83df0fe6;36areMathlib-free. All9exact dependency
source packages are prepared on PVC; compiled Mathlib caches are not prepared.
Official Lean4.34.0 and4.29.1 SDKs were extracted on PVC and version CLI confirmed.
That proves SDK preparation, not workload acceptance. LKV needs only core/Std.

Vericoding's code repo declares Lean4.23.0-rc2/Mathlib
90c0e186fd333cbdddbe0e5148aa3cd2d24dcf9a, not proven original settings for every
model run. Original exact Verus compiler build remains unknown. AlgoVeri
declares Lean4.25.0-rc2, Verus0.2025.01.13.da1c777 and Dafny4.11. Its official
HF pin a220ba993dc735fa9250168c44ad895e7d2b4d02 has77rows/language with only
problem_id/nl_desc/spec. Git/HF Lean trie_search differ:76/77Lean and all77
Verus/Dafny specs match exactly. An alternative gcd Lean spec is not task78.
Choose a fixed mirror for replay.

Root licenses are Vero/AlgoVeri Apache-2.0 and Vericoding/LKV MIT.
Vero Flocq/portion retain LGPL-3.0-or-later; Huffman LGPL-2.1-or-later.
Upstream attributions remain; root licensing is not a new claim about every
inherited source. Only small derived tables and analysis are committed here.

## Reproduction and limits

Raw metadata, complete trees, README/licenses, release lists, source receipts,
programs, final tables, failures and compressed per-observation journal:
    /workspaces/.agent-state/gpu-smt-captures/workloads/ai-verification-software-20261031
Source mirrors: matching directory under /workspaces/.agent-state/gpu-smt-workloads/.
SDKs are in toolchains/; Vero packages in vero4291-dependencies/.
All output is on PVC, outside the core engine and container/tmp.

    taskset -c8-15 python3 workloads/ai-verification-software/characterize.py --assets ASSETS --evidence EVIDENCE --out OUTPUT

sources.csv pins5repositories; each dataset's inventory/commit/tree JSON and
archive receipt remain in EVIDENCE. The analyzer starts no upstream harness
or verifier. Preliminary joins/transport errors are retained; final joins use
non-mutating dictionary lookups. No native CPU-hour estimate, acceptance,
slow-tail share or speedup follows from this static audit. M/O keep P-core
priority; future timing waits for actual completion. Review is self-review.
