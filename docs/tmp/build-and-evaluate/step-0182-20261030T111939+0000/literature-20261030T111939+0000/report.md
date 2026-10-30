# Native Lean negative-query caching and incremental replay

2026-10-30 UTC; bounded primary-source audit; root self-review. Parent: step0181.
This is source evidence for RQ1/RQ2 mechanism overlap and replay obligations,
not a native benchmark, thesis replacement or production-cache qualification.

## Questions and completion boundary

1. Is storing a failed expensive query a new primitive, relative to the actual
4.9.0-rc1/4.34.1 Lean frontends used by our measurements?
2. Does native Lean already narrow cache keys using observed dependencies or
normalize contexts, and at what verified source version?
3. What separates those caches and native snapshot reuse from arbitrary tactic
exception replay with identical states, diagnostics and resource behavior?

Three threat branches are covered: negative query caches; dynamic dependencies
and contextual equivalence; incremental state/heartbeat and asynchronous
diagnostics. Each ends in implementation evidence with an explicit reuse unit.
This finite audit does not repeat the whole Salsa/Adapton/Boogie/SHRED survey
already retained in the repository. It cannot adjudicate a new paper claim
which the user has not selected.

## Search provenance and source discipline

Exact web queries, issued 2026-10-30 UTC:
- site.github.com/leanprover/lean4 "withRestoreOrSaveFull"
- site.lean-lang.org incremental elaboration snapshots errors heartbeat reuse
- site.github.com/leanprover/lean4 "cacheResult" "cacheKey none"
- site.github.com/leanprover/lean4 "SynthInstanceCache" "recordedDeps"
- site.lean-lang.org "withRestoreOrSaveFull" heartbeat

Parent branch 1 starts from saved-state primitives, branch 2 follows cache
callers into SynthInstance, and branch 3 follows the dependency types and
upstream history. Mutable master search hits are leads only. The official
GitHub API resolved master to 0f852cc822d54d32c5cb0ef158562796088ce4dc (committer 2026-10-30T09:56:07Z).
Pinned files, release-tag files and relevant commit patches were then read
directly. source-check.json independently records ten successful raw-file
retrievals, byte counts and symbol line locations. Browser UI was not used.

The source families are official Lean source, in-source API documentation,
official implementation history and adjacent incremental-computation precedents
already in background-related-work.md. The thesis search lead was not opened
and supplies no claim here. No secondary summary supplies a conclusion.
Line ranges below refer to raw source, not the HTML renderer's line numbers.

## Verified mechanisms and scope

### 1. Negative typeclass queries already exist in the measured older release

[4.9.0-rc1 SynthInstance](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Meta/SynthInstance.lean) lines729–778 looks up a contextual key and
stores the optional result, including none. Lines780–798 distinguish a failed
search from a temporarily stuck metavariable query and convert a failure into
the usual synthesis error. This is a negative query cache inside typeclass
resolution, not proof that an arbitrary goal is false. Its unit is not a
complete candidate or general TacticM exception.

[4.34.1 SynthInstance](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Meta/SynthInstance.lean) lines943–950 explicitly inserts none for
unsuccessful results. [4.34.1 Meta.Basic](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Meta/Basic.lean) defines the corresponding
contextual key and optional-result map. Generic claims that Lean only caches
successful computations therefore conflict with released native code.
These source inspections do not measure its hit rate or suppressed time.

### 2. Full state plus heartbeat charging is an existing native primitive

[4.9.0-rc1 CoreM](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/CoreM.lean) lines221–246 documents and implements full-state
reuse with IO.addHeartbeats. Its own documentation says wrapper/reuse overhead
is omitted from that approximation. The fresh path awaits act before saving;
it does not itself catch every thrown exception into a reusable result.
Consequently neither arbitrary failure replay nor exact wall/RSS preservation
follows from this primitive.

[4.34.1 tactic dispatch](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Elab/Tactic/Basic.lean) lines216–246 retains selected exceptions
together with their failed states while trying elaborators, restores the
appropriate failed state, and rethrows. Unsupported syntax and internal
exceptions have distinct paths. This local fallback mechanism must not be
described as an already measured cross-request tactic cache.

### 3. Current native typeclass reuse already tracks observed dependencies

[Pinned current Meta.Basic](https://github.com/leanprover/lean4/blob/0f852cc822d54d32c5cb0ef158562796088ce4dc/src/Lean/Meta/Basic.lean) lines357–437 describes optional negative
or positive query results with RecordedDeps. Options, instance/unification-hint
generations and declaration changes validate entries. Unobserved inputs do not
partition this cache. Context-free entries also persist in the environment
across commands; applicable context keys normalize free variables.

[Pinned current SynthInstance](https://github.com/leanprover/lean4/blob/0f852cc822d54d32c5cb0ef158562796088ce4dc/src/Lean/Meta/SynthInstance.lean) normalizes the query and reachable
local-instance type closure, with explicit unsupported cases, records and
merges nested dependencies, and validates hits. It also has a debugging
recomputation option. This audit did not execute that option or prove general
arbitrary-metaprogram dependency completeness. The source establishes a strong
same-mechanism precedent for dependency-keyed positive and negative queries,
not the opportunity size of cross-candidate expensive tactic reuse.

The implementation history was inspected through official commit patches:
- [904eaf4, 2026-09-25](https://github.com/leanprover/lean4/commit/904eaf47172cef9a77ab9c18878c2ff63f9672ae): record option dependencies during synthesis.
- [d8c07ad, 2026-10-04](https://github.com/leanprover/lean4/commit/d8c07ade4ff2e44f5cd00062bfb3a9e89134297d): persist eligible typeclass entries across commands.
- [2c2a96f, 2026-10-04](https://github.com/leanprover/lean4/commit/2c2a96f3404e851106c716e5fbbb4649dfa6226b): normalize free-variable contexts and query results.

These selected dates are verified change metadata, not a claim that any one
commit introduced every piece of the current design. Features were present
upstream before this project's October7 history; they are not attributed to
the older measured release tags or to our implementation.

### 4. Composition, tracing and async messages remain explicit obligations

[Pinned current CoreM](https://github.com/leanprover/lean4/blob/0f852cc822d54d32c5cb0ef158562796088ce4dc/src/Lean/CoreM.lean) lines573–586 rejects full-state restoration
while dependency recording is active, because it would roll back the dependency
accumulator. Existing primitives cannot simply be composed without handling
this condition. Its heartbeat approximation remains documented.

[4.34.1 CoreM](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/CoreM.lean) documents that asynchronous elaboration can place
diagnostics in snapshots/tasks; cmdState alone is insufficient when async is
enabled. CLI/LSP override the nominal async default. [4.34.1 Language.Lean](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Language/Lean.lean)
uses position-aware syntax and explicit incremental/cancellation rules.
These are source contracts; no latency, cancellation or full artifact parity
was measured by this audit.

## Claim disposition and experimental handoff

| Plain candidate claim | Same-claim/mechanism risk | Root disposition |
|---|---|---|
| Cache failed expensive queries | High at primitive level | Native negative typeclass caching is mandatory citation-level context. Generic negative caching is not a standalone contribution. |
| Key reuse by actual observed dependencies, normalize contexts | High at mechanism level | Native current synthesis, plus established incremental computation, already implements these principles. A new name does not create a distinction. |
| Reuse arbitrary expensive tactic failures across candidate requests while preserving requested native behavior and complete cost | Unresolved; native pieces overlap but reuse unit differs | Require actual workload opportunity and native semantic/cost evidence. This audit neither establishes that method nor rules it out. |

Competing position: native caches and native incremental execution already
remove the proposed repeated work. If they account for an apparent hit, an
external cache's gross opportunity is not its incremental benefit. Existing
producer-completed, process-segment and failed-state distinctions stay intact.
Relevant baselines are the native frontend at its actual pinned version and
options, with existing caches left enabled. Current-master source is a
citation-only precedent, not an unrequested new runnable baseline or SDK
upgrade. No new competitor reproduction is authorized or proposed here.

A decisive future comparison, if opportunity data supports it, must establish
work beyond existing native reuse, account for failed-state/diagnostic replay
and show complete matched service cost. Read-set capture costs must be included.
That is a handoff of evidence obligations, not a newly launched experiment,
resource policy or instruction to W/M. Heartbeats, OS-memory pressure and wall
timeouts are distinct; an optional synthesis failure is not a resource verdict.

## Canonical update, preservation and remaining uncertainty

The canonical background-related-work.md already has another owner's dirty
changes. The user's ownership instruction overrides this skill's default
canonical write path: this node preserves the detailed result here and root
links it from its own evaluation.md. No foreign text is staged or overwritten.
Canonical related-work merging is deferred to ownership-safe integration,
not an approval gate or a reason to stop independent paper work.

No paper mainline, four RQs, hypothesis or frozen Related work is rewritten.
No native verifier, profiler, cache, SDK upgrade or production feature is run
or enabled. Whole-goal negative-result closure is not inferred. Source-native
controls and complete W/M captures remain necessary; broad arbitrary-tactic
coverage, hidden dependency completeness, native differential parity and
incremental speedup are all unresolved.
