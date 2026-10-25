# Measurement integration self-review

All six formatting/Clippy/test/documentation/help commands pass. There are
25 passing unit/integration/subprocess/HTTP/comparison checks; the local native
differential test remains explicitly ignored to preserve the sole collection.
The prior pushed152103c has successful exact-head native and Rust CI, recorded
separately. This follow-up needs its own exact-head CI after push.

Four paired-accounting tests check accepted identity changes despite equal
counts, mismatched source/environment/resources, cancellation versus RL parity,
and operational/preemption/tail accounting. A real subprocess executable fixture
checks measure output, all rows and native process retirement. It is not Lean,
not a full workload and not an acceleration result.

Native COW/state preparation, real new-resource population parity,42isolated
reruns and measured full throughput remain pending. Root self-review only.
Earlier failed compile/lint receipts are preserved.
