# Plan — expose measured task memory through existing executable

99709ec implements optional TaskMemory and81fe7cc qualifies actual pinned4.18
native feedback controls. Add one opt-in existing --policy choice,task-memory,
to check/measure/serve,wrapping FIFO. Defaults,runtime resources and current
frozen full pair remain unchanged. Reuse existing measurement Capture.policy;
no new schema,logger,collector,workflow,daemon or compound policy matrix.

Extend the existing executable capture/compare lifecycle test with this option
and same-task distinct sources. Before implementation,the added case must fail
on unknown scheduling policy. After implementation,it must preserve both native-
fixture outcomes,one physical attempt per source,retirement,capture policy label
and identity comparison. Fixture is Python,not Lean;real TaskMemory backend
qualification remains the earlier declared4.18context. Compile/Clippy/format
and relevant executable/measurement/HTTP tests useCPU11 under existing combined
own-tree48GiB support sampling. No native proof group or release rebuild.

Update API/benchmark/example docs to make the method runnable in a matched
future native preflight only after the active group retires. No claim of a
throughput gain,novelty,fullMathlib parity or independent audit. Commit/push
source and retained red/green evidence on main.
