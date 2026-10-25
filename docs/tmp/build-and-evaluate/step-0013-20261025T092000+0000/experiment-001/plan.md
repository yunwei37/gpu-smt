# RQ2 implementation/qualification plan

RQ2: Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?

The current component is dependency work folded into the complete native/engine experiment. It cannot answer RQ2 or RQ3 by itself. Candidate code and results remain original; only the prepared import boundary and OS ownership change. Strong reference is the pinned actual native frontend/serializer. Existing warm/native measurements remain the eventual strongest service comparison; a fresh-process comparison alone cannot establish superiority over warm reuse.

Current preflight: official Lean4.18 plus pinned stock REPL, actual compiled Lean+C host and Rust PreparedRepl. Compare full native JSON for accepted/rejected/sorry inputs, declaration name reuse/isolation, different imports, timeout followed by a valid candidate, actual parent survival and final owned-process retirement. Test fixtures/defaultRust checks are not the native preflight. CI is separate from the live lab full group; no new local native collection.

After the original7808group retires: complete the already prepared42isolated uncapped reruns separately, qualify the matchedMathlib/native path and dynamic48GiB/fourCPU point, then execute all original7808inputs with native and engine under the same total resources. Preserve all outcomes, exact accepted sets, raw JSON deltas, parent/child RSS, retries, cancellation, queue, fallback and cold lifecycle. Pass@k task success is separate from every-candidate RL semantics. Repeat/interpret only complete planned cells; no proxy ratio establishes contribution. No new competing-system integrations or frozenCPUoracle runs.
