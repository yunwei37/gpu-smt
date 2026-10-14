# Kernel Arena source boundary refresh

Question: does the established framework provide a real full-kernel workload and
an official dependency-selected export path, distinct from our source-candidate
replay and narrow Meta beta/zeta integration?

Primary source inspected: [official Lean Kernel Arena repository]
(https://github.com/leanprover/lean-kernel-arena),2026-10-14.
The official framework compares kernel implementations on declared export tests
and includes real-world corpora, bugs, corner cases, performance and tutorial
cases. Its module/file specifications allow export-decls to select declarations
with their dependencies. It supports downloaded source/module assets and static
export files. This provides an established kernel boundary; it does not validate
our modified source frontend or convert Meta reduction into full kernel GPU work.

Decision: finish the admitted complete ProofNet/miniF2F source-native comparison.
Do not add another small adapter variant just to approach the same native CPU
clock. A later kernel-route experiment must use official full proof/declaration
assets and account for dependency extraction/export separately from complete
source checking. An all-environment export panic does not justify dropping a
context or labeling native fallback as an external checker success. Existing
E018 repair preserves and exposes that coverage limit. Published selectable
roots are a future adapter lead, not an implemented repair/performance result.
No RQ,Initial Narrative,claim or baseline family changes; no new checker installed.
Root direct source disposition is not an independent research audit.
