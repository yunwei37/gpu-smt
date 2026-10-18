# Executable-source boundary, root self-review

All29copied Rust/Lean/C source bodies are traced to retained executed source,
with provenance comments only; Cargo files remain byte equal. The measured
CPU HiGHS support file is copied unchanged. No algorithm tuning, native
library rebuild in an active capture, alternate checkout or agent exists.
The pinned upstream Apache2license is included; NOTICE at that exact
upstream revision returns404. No root-project license is invented.

Fresh locked numerical release builds all3binaries. All4existing rational
tests pass. All15local Lean modules typecheck, and699dependency C libraries
compile; those results alone do not establish load compatibility. The first
real load fails due to omitted package-native prefixes. Root verifies the
actual Lean.ModuleSetup serializer and Lake.Package.id? source and tests the
correct expected symbol with package=mathlib. Current complete rebuild and
first64real-source qualification are active, event-driven after build exit.

The portable builder derives source roots from Lake/Lean and package names
from the manifest. Its logs record exact commands; it does not overwrite the
existing Mathlib cache. Host C shims use host cc, then leanc links them.
No private Workspace path is embedded in public implementation source.
Python syntax and local README links pass. This is compatibility/artifact
work, not a paper-valued performance experiment or a whole WRITE/REVIEW gate.
README labels functional qualification pending, not passed.

Failure attempts1--3 retain original source, logs and receipts. Compilation
success, load success, exact proof results and benchmark timing are distinct.
Root self-review cannot provide the independent audit the user has forbidden
delegating. All4RQs and novelty remain open.
