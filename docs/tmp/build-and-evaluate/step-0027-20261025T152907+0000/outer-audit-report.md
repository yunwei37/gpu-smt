# Outer self-audit

# Full Mathlib derived children — root self-review

Actual matching Lean4.9 host loads5,545Mathlib modules once, reports one parent
thread and no import errors. Six small source controls are each executed by
stock fresh REPL and an actual fork child: arithmetic/ring/private definition
accepted, false proof/unknown sibling declaration rejected, sorry incomplete.
All6paired status comparisons match. A declaration made by one child does not
appear in the next. Two further children are both alive before either request
is sent, then independently complete the arithmetic/ring proofs. All8children
are retired/reaped, and the one parent exits0 and is absent after EOF.

Raw inputs, fresh stdout/stderr, child responses, PID/birth and retirement
records retained. Total development lifecycle17.859913s, combined original
collection plus qualification tree sampled peak20,323,041,280bytes(~18.93GiB),
no48GiB pressure or monitor errors. No fixed process AS limit. SharesCPU10/11
with old acquisition; not an isolated performance test. No full-population
throughput pairing, memory-saving estimate or universal Mathlib/FFI fork-safety
claim. Wait4 child high-water RSS excludes the parent and is not total RSS.

This closes the previously missing actual full-Mathlib child execution path for
these controls. Engine integration has separate native CI; this direct native
host test does not substitute for full engine/population semantic differential,
cancellation-pressure qualification or dynamic resource-point throughput.
Root self-review, not independent audit. Original first-original/first-short
collection remains sole full acquisition; CPU oracle frozen.
