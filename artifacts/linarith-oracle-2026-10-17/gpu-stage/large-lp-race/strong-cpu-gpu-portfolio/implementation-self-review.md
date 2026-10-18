# Root implementation self-review

Private baseline-native source copy preserves original arithmetic/products,
FP LP formulation, exact positive support repair, negative-ray reconstruction,
parent exact recheck and Lean modules. Coordinator changes fixed two children
to a vector, adding CPU-HiGHS child only when the finite GPU method prepares its
socket. That child's process-local environment selects existing CPU HiGHS proxy;
GPU continues using original numeric socket. Native hybrid remains active.
Positive certificates are rechecked against original hypotheses in parent.
External negative rays are accepted only by the existing exact negative check.
Normal native-no-certificate authority is unchanged. Logs identify each child
PID, winner, wait/kill outcome and an explicit extra-child spawn failure.

Both CPU and GPU conditions use this private numeric build. CPU leaves the
additional-child socket unset, so its exact two-sided portfolio is preserved.
GPU owns the additional existing HiGHS proxy under an outer Runner; setup and
retirement are added to whole elapsed after the original GPU proxy cost. The
socket/process is removed on exit, all losers killed/waited. This adds no new
persistent service, numerical parameter, candidate count or CPU eligibility.
No strict no-slowdown guarantee is claimed: overhead/contention can lose.
Rust release/offline/locked build succeeds. Complete generated CLI --help passes.
Actual same64source engagement, exact/native result parity and retirement still
required; compilation is not performance admission or independent audit.
