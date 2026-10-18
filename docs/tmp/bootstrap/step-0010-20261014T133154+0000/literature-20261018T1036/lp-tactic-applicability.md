# Existing LP tactic and certificate-assembly applicability

Primary-source follow-up, root self-review,2026-10-18. Repository
https://github.com/leanprover/lp-tactic at86634295a1fa2b45110a680215e208b16f40cd33, committed2026-08-26.
Its README describes a backend registry and kernel-checked arithmetic proof
reconstruction; its package separates solver dependencies. Pinned
[toolchain](https://github.com/leanprover/lp-tactic/blob/86634295a1fa2b45110a680215e208b16f40cd33/lean-toolchain) is Lean4.33.1.
[CarrierCertificate](https://github.com/leanprover/lp-tactic/blob/86634295a1fa2b45110a680215e208b16f40cd33/LPTactic/LP/CarrierCertificate.lean)
contains precomputeSpine, proveMerge and proveCertificateIdentity, so generic
specialized certificate assembly is also existing work.

This is a relevant CPU competitor/design precedent, not a measured speedup
over the project's4.27 workload. Do not replace candidates' versions or claim
drop-in comparability without a matched build/functional experiment. Do not
promote historical issue#40's proposed Boolean checking design into a claim
about every current carrier's implemented proof path. The current source
receipt records actual symbols and revision. Generic untrusted solvers,
certificate checking, sparse supports or precomputed proof spines alone do not
supply a new systems contribution. Existing full captures remain untouched.

Next mechanism selection must address complete current proof construction and
fallback cost against such established alternatives. No new numerical/support
objective or GPU provider is admitted merely from an observational correlation.
