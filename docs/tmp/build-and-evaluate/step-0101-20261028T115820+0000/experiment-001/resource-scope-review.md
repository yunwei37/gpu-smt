# Resource-context support — root self-review

This support inspection runs while the unchanged real24 qualification owns the
only native collection slot. No additional profiler, log hook, thread parameter
or admission policy is introduced.

The one-shot native-resource-snapshot is explicitly non-atomic. Its only live
candidate at that instant is the existing exclusive1885 process, about21.55GB
RSS/PSS, one live thread on CPU8. That is neither a whole-run peak nor a safe
reservation: the existing42 resource observations grow towards the full budget.
It does not justify speculative backfill or replacing the user's RSS accounting
with PSS. The four allocated logical CPUs map to four distinct reported core IDs
in this container's exposed topology; that observation is not a host isolation
guarantee.

Earlier live workers were also observed with one thread. Pinned Lean runtime
source and local ELF disassembly show that initialization consults
LEAN_NUM_THREADS and otherwise hardware concurrency. Actual one-thread
candidate execution does not establish a universal fixed runtime limit.
Primary source: https://raw.githubusercontent.com/leanprover/lean4/v4.9.0-rc1/src/runtime/object.cpp
(lines808–827). No thread setting changed.

retained-boundary-candidates.json derives compact sizes/counts from the
preserved full native payloads without changing their messages.2507 returned
11,884 messages (~4.2MB compact UTF-8) at298.29s in warm;7230 returned3 messages
at288.51s. Engine timed both out.3086 passed in both, near the same300s boundary.
Those observations cannot prove that parsing, retirement or hardware variation
caused the differences. The current source repair is still under native
qualification; full raw results and the same300s budgets remain required.
