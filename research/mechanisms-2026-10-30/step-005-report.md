# Step 005 — qualified dependency capture and bounded 200-source plan

2026-10-30 UTC; M branch; self-review.

The SDK-only dependency probe now compiles and runs two native controls.
Constructor-created True/True goals have disjoint expression-metavariable
closures; existential witness/proof goals share the witness metavariable.
The latest control exits0 in0.86654s, kernel leader high-water286,560,256bytes.
The C thread-CPU clock wrapper is exercised by each candidate. Trace threshold
zero now retains all Elab.step timings.

A naive full trace/InfoTree join fails: the independent control has18 tactic
Info nodes versus28 trace nodes; the coupled control has6 versus9. Speculative
and expansion work is retained differently. No global critical path or true
average available parallelism follows from these sequences.

## Next actual point

Fixed200-source stratum from step002; control/observe pairs =400 diagnostic
units. Header imports Mathlib/Aesop are loaded once. Original top-level
maxHeartbeats0 is replaced by3000 in both modes, with changes retained in an
input audit. These are bounded diagnostic executions, not the original300s
candidate outcomes or production throughput.

One Lean process, CPU8-11 affinity, one Lean thread. Native -M8192 allocator
setting plus one-second RSS observations; M's actual budget remains16GiB.
The allocator setting is not a hard RSS quota. Output/source/input remain
on the existing PVC. Internal wall alarm1500s leaves margin below the requested
30-minute ceiling; its tiny Lean control is qualified, but uninterruptible I/O
can delay response. No external kill/watchdog capability is assumed.

No full project build. Expected ordinary resident memory starts around the
observed3.5GiB Mathlib point, with body allocations bounded by the native
setting; record actual RSS and failures. Previous cold import took2442.7s,
so this finite run may time out before producing candidate rows. That outcome
would be a collection failure, never zero parallel opportunity. Do not loop
restarts or increase its deadline to force a result.

The narrow initial model will consider only uniquely corresponding allGoals
nodes with matching branch counts and goal identity order. It may aggregate
connected components of conservative metavariable closures; nodes with
unresolved universe effects remain unsupported. All remaining work is serial
in that model. Have/case/first opportunities are separately unknown, and
name generation, diagnostics, cache and hidden-state merge correctness are
unproved. Even a model above1.3 is not a measured engine speedup.

The before/after states overapproximate local-context reads. The model is
therefore not the main thread's dynamic read-set cache key.
