# Read-set reuse: closest work and evidence boundary

Self-review; primary sources read 2026-10-30. No competitor reproduced.

- [Salsa algorithm](https://salsa-rs.github.io/salsa/reference/algorithm.html):
  tracked queries record dependencies and validate their revisions before reuse.
  Our smaller key is not new merely because it contains dynamically read inputs.
- [Adapton, PLDI2014](https://matthewhammer.org/adapton/adapton-pldi2014.pdf),
  DOI10.1145/2594291.2594324: demanded computation graphs support reuse across
  changed contexts and ordering. Dynamic dependency tracking/reuse is established
  prior work; do not claim it as our algorithmic invention.
- [SHRED pinned a6616e9](https://github.com/memo-ozdincer/shred/tree/a6616e99534ce777dcebfd56566eaaffb63997a8):
  source README describes exact rooted prefixes and successful closing proof
  reuse under an exact elaborated environment/target/local-context match,
  followed by native type checking. Our proposed ordinary-failure transition
  replay is a different output contract, not automatically novel or qualified.
- [Lean4.9rc1 rfl extension source](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Meta/Tactic/Rfl.lean):
  non-equality reflexivity queries the scoped refl environment extension and
  performs native metavariable operations. A list of constant values alone
  cannot stand for all extension lookups. This source is not evidence that
  the selected equality rfl necessarily reads every local hypothesis.

## Required read-set meaning

Track reads of goal/other metavariable declarations and assignments, hypotheses
and local instances, environment constant definitions and extensions, options,
transparency and strategy text. A lookup returning no result, enumeration order
and search-domain membership are also dependencies: inserting a new hypothesis,
instance or rewrite lemma can change a previously failing search even if all
previously returned declarations remain unchanged. Unknown/untracked operations
must run natively. No claim that all simp/norm_num without star have empty local
reads follows from their spelling or an apparently closed source goal.

The checked semantic transition is separate from the key. Ordinary exceptions
must re-enter original failure/backtracking; goals/assignments/diagnostics and
remaining native budget need compatible replay. A first run killed for RSS or
wall timeout has no completed ordinary-failure transition. A semantic read set
does not prove RSS budget monotonicity: retained heap, allocator and preparation
state are outside that equivalence. The proposed key cannot relabel these
operational outcomes as ordinary Lean rejection.

## Current data disposition

The complete selected96-source audit has95native-Syntax records and79historical
profiles, but zero actual dynamic-read traces. This is missing coverage, not a
negative hit-rate measurement. The narrow source-rewritten closed-target shape
matches19sources and yields one repeated5-source group. All five final outcomes
are resource_exhausted. No completed ordinary-failure producer or certified read
set is known, so qualified hits and saved seconds remain unknown.

Conditional removal of four later whole-candidate physical-attempt envelopes
would expose1210.66–1221.00s depending on first producer; these envelopes include
prefixes, retries and other calls. Historical rfl/eqRefl-family CPU exposure is
354.44–355.46s for those four sources, on a separate profiled clock and including
other/internal calls. Neither is a measured saving, current call duration or
global bound. No production read-set cache is enabled from these proxies.
