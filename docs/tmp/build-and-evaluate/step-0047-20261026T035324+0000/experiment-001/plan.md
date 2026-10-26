# Complete original simp_all phase attribution before runtime collection

Fixed RQ2: "Does branching from prepared native state preserve verifier responses
and requested artifacts while isolating candidates and cancellation?"
User direction1 requests original23simp timeout attribution and reliable failure
mechanisms. This implementation dependency does not itself answer RQ2.

Source inspection finds the existing observer leaves assertHypotheses and
tryClearMany unlabelled,and groups all initialization into one interval.
Native progress depends on changed expressions,changed goal identities and a
changed theorem set with fresh origins; an expression hash is not a complete
deterministic transition state. No automatic cycle/failure rule is justified.

Split initialization into collect-hypotheses and ordered initialize-hypothesis
spans;time native reassert/clear calls;label hypothesis subjects and whether a
timed action returned or unwound. Preserve the same native calls/order/results,
bound selection,discharge and progress decisions. Analyzer retains old events
with completion_unknown rather than inventing success.

Preserve the qualified old module/source/receipts. Compile the new definitions
to a different temporary directory under combined own+activefull48GiB monitoring
onCPU11. Do not execute another proof/candidate group. Test analyzer behavior
against existing actual qualification007events and synthetic labelled unwind
records only;synthetic transport checks are not native/RQ evidence.

After the sole fullpair and already-prioritized nightly workload,the original23
prepared sources require native/profile parity and actual phase timing with
full stderr,setup,overhead,resource failures,open phases and source IDs. Whole
native results remain unchanged until that evidence exists. No CPU oracle,
competitor reproduction,early rejection or loop certificate is added.
