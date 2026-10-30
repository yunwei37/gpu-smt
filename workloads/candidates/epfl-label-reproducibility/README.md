# Stored recursion failure versus fresh native success

Candidate training-rg0-row19776, amoeba_xor_function, dataset e5ff00a8.
Publisher invalid/maximum-recursion diagnostic, but original source text
compiles under native Lean4.15.0 commit11651562caae with official matching
Mathlibv4.15.0 commit9837ca9d65d9de6fad1ef4381750ca688774e608.

Six actual fresh native controls, same machine/cache/CLI-j2/M6144,
CPU0–7,20s self allowance (including0HB variants), one process at a time:
original0HB passes1.875s; published annotated text minus training EOT marker
passes1.893s; source rewritten800kHB passes1.867s.
At0HB, explicit maxRecDepth128 fails2.095s with nested simp recursion error;
256passes1.961s and512passes1.861s. The pinned SDK declares
its defaultMaxRecDepth=512 in Init/Prelude.lean; no default1000 is assumed. No wall interruption/crash/sorry.
Old10k pilot also passed1.881s. Sampling combined9,244,323,840bytes includes
legacy13733; runtime option/sampling are not hard RSS guarantees.
Full original/variant/log/counter files remain on PVC in epfl-label-controls.

Thus our10k cap and mere annotation comments do not explain fresh success.
Recursion configuration can flip this exact released source locally; this
does NOT prove the original producer used128 or had the same failure cause.
Native source and annotated code agree after comments/whitespace removal;
this is source-text comparison, not complete environment equality.

[Publisher paper AppendixB/C](https://arxiv.org/html/2610.21881v1#A2)
reports Lean4.15, an800k collection budget, expected-statement checks and
LeanInteract tactic-traced annotation. It does not provide this row's
Mathlib pin/recursion option/original wall/machine. The800k policy describes
the collection harness; do not assume every training-source reconstruction
used it identically. The paper also notes stored versus fresh annotation
label disagreements elsewhere; those are not this candidate.

[Producer repository pinned f29b3e4](https://github.com/epfl-lara/learning-lean-feedback/tree/f29b3e46f6fc37336e4e1fd2c0e3f0a8f08a42da)
contains only README/license/gitignore and says code coming soon. Consequently
original tactic-trace collection, external target context and exact producer
configuration cannot be replayed from the inspected release. Raw pinned tree,
README,commit and paper are preserved outside Git.

Conclusion: real non-reproduction of the stored failure at the declared
native point. Unique original cause remains unknown; neither label-bug nor
machine-speed explanation is established. It is not a certificate that the
candidate always fails or a safe resource-failure cache entry. Reproducible
workload reports must carry actual native verdict plus budget/toolchain/
annotation/acceptance context, retaining the stored label separately.
