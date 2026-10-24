# Batched point-evaluator prototype — compilation and CPU qualification

## Admission and scope

The first two exact counterexamples establish a real, limited functional
opportunity. Their associated native requests are cheap, so they do not
establish a useful GPU payoff. While the full own observation continues,
root implements the point evaluator and qualifies its packing against those
actual contexts. Device execution and end-to-end promotion still depend on
complete coverage/cost results. No second full acquisition or GPU Job starts.

## Implementation

points.cu is a single fixed arithmetic/Boolean stack interpreter, compiled
once rather than generating/compiling a new kernel per goal. Each thread
evaluates one point; the grid's second dimension selects its own goal program,
variable domains and sample array. Source and entry identities stay attached
to each host-side batch member. An offline replay batch is not evidence of
online overlap between candidates.

The supported operators match the frozen typed AST: rational constants,
variables, arithmetic, bounded natural powers, truncated Nat subtraction,
equality/order and propositional connectives. All ordinary exported
hypotheses are conjoined with the false goal. Pack-time validation rejects
unsupported programs and stack depths above64; this is an implementation
fallback, not a claimed whole-population coverage bound. The observed maximum
stack depth is6 and program length106instructions.

GPU values are floating proposals. The CPU reconstructs each proposed grid
point from its rational pool/index/assignment recipe and checks every
hypothesis, goal and Nat/Int domain exactly. Numeric error or unsupported input
cannot itself authorize a proof acceptance or an arithmetic rejection.

The CUDA driver wrapper owns its context, allocations, upload, synchronized
kernel, download, free and destruction. These phases have separate clocks;
cold setup, preparation, queuing/RPC and fallback must additionally be included
by the eventual whole-flow collector. No per-kernel time is a speedup claim.

## Actual compilation

The existing CUDA12.8 minimal SDK compiles the kernel successfully for
compute_120, producing8447bytes of PTX in0.527871seconds. Compiler peak child
RSS is99676KiB. This is CPU compilation only; no device was allocated or used,
and no active Lean binary/library/worker was modified.
point-cuda-build.json and point-cuda-build.log preserve the command/exit.

## Actual functional qualification

The exact identities from the reviewed839-entry prefix select474supported
queries from169source IDs, copied to
point-evaluator-qualification-input.jsonl. At4096points each, this covers
1,941,504point evaluations. CPU bytecode execution and the separate nested
array evaluator yield **zero proposal-mask differences**. Both recover the
same two exactly checked witness entries. Packing takes0.147705seconds,
nested reference0.049864seconds, exact checking0.181448seconds; the entire
functional check takes0.618259seconds. These are CPU diagnostic clocks, not
GPU timings or native candidate speed ratios.

The first qualification fails while constructing its output dictionary
(duplicate source_id keyword), after evaluation. Its driver log and exact
source are retained under point-bytecode-cpu-qualification. A forward source
repair removes the duplicate fields; the complete successful run is separate
under point-bytecode-cpu-qualification-v2. No failed record was overwritten.

## Root self-review and next action

This is self-review, not independent audit. Source/batch ownership, domains,
stack bounds, exact-check boundary and context/allocation cleanup were checked.
Hardware launch, numerical behavior on RTX5090, transport, normal Lean
fallback/backtracking and paired end-to-end costs remain unverified.
A CPU interpreter cannot qualify those device properties.

Keep one full observation running under the existing resource contract.
After its terminal record, finish coverage/cost accounting, qualify pending
comparison aliases, then execute the own finite GPU functional check and
Lean screening integration. No additional external system, LP variant,
persistent service or Agent is introduced. All four original RQs remain open.
