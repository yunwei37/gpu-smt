# Official SHRED first-block qualification — root self-review

The unchanged upstream closing-certificate executor runs the first original
miniF2F block, 32 sources in retained order. Both modes return 28 complete
and four rejected sources, no timeout/process error, and identical
per-source verdicts. Cached mode instruments 29 sources, records 22 misses,
21 captures and four hits. Parser exclusions remain original native fallbacks.

| Upstream reported source spans | Original | Cached |
|---|---:|---:|
| Sum of source wall seconds | 3.312049658 | 3.127602234 |
| Sum of source CPU seconds | 3.258839212 | 3.069977219 |

The complete paired upstream worker takes 10.570750 s; outer driver takes
10.679189 s. Source sums exclude some setup/lifecycle boundaries and are
not complete per-method HTTP throughput. This first block is a functional
qualification, not the full miniF2F/ProofNet performance result or a claim
that generic certificate reuse is our contribution.

## Source, environment and fidelity

The retained SDK archive provenance matches Lean 4.9.0-rc1 and Mathlib
2f65ba7f1a9144b20c8e7358513548e317d26de1. The exact existing SHRED revision is
a6616e99534ce777dcebfd56566eaaffb63997a8. Its Lean cache module and Python
selection/wrapping/checking/fallback code are unchanged. Only the outer
recorder and archive-provenance callback adapt the execution environment.

All original input bytes reconstruct exactly through the official C0 parser.
The input header has one extra blank line after the official C0 context;
that line is retained in the statement portion. Original unit byte ranges
remain aligned. The group ID is an execution label, not a renamed Lean
declaration. expected_correct is null because this source adapter does not
retain generation labels; actual native outcomes are recorded directly.

The kernel-checking REPL is the existing qualified integration, not a claim
of a byte-unmodified upstream binary. Both methods use the same SDK, module
and REPL, four eligible CPUs 4–7, 48 GiB and upstream 300 s request timeout.
The host is shared. All complete native responses and lifecycle-close
observations remain in qualification-wire.jsonl.gz.

Full wire responses are not byte-identical: all 32 source responses differ.
31 sources differ in the non-message env handle field, reflecting the
official cached mode's extra event-query commands. Cache informational
messages and other message differences are retained. This is native
verification agreement, not transparent protocol/snapshot equivalence.

## Real failures and repair

The first attempt also completes all 32 pairs, 28/28 accepted and four hits,
then the upstream reporter fails when asking git for the SDK source
archive's revision. Preserve its complete pairs, wire and exception under
failed-metadata-attempt1. The repair reads that archive's existing setup
metadata for that exact path; real checkout queries remain upstream.
No fake Git repository, commit, solver change or altered cache key is used.
The repaired official CLI exits zero with a complete report.

A subsequent HTTP integration launch fails before any server/native cell
starts because our filename http.py shadows Python's standard-library http.
The driver is renamed run-kimina.py, and the zero-condition failed attempt
is preserved under failed-http-name-attempt1. This was an avoidable driver
error; it did not interrupt other captures.

## Next experiment

The official paired CLI component cannot be relabeled a complete Kimina
service comparison. The actual HTTP qualification now runs through unchanged
Kimina app/SDK, preserving each dataset's original header. The real native
parser and source wrapper execute inside its charged condition clock;
module imports, queueing, checking, fallback and owned retirement remain
charged. First32 per dataset and every literal unavailable-source placeholder
are retained. Full population admission depends on actual returned fidelity.

Root self-review checks all 32 source reconstructions, native parser
exclusions, every response, cache events, errors, SDK archive identity,
resource settings and source-span versus whole-clock scope. This is not
independent audit, all-RQ completion, GPU acceleration or OSDI acceptance.
