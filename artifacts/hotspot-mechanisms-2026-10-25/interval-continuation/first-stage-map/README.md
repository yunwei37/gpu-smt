# On-demand interval leaves with surviving first-stage goals

Observed2026-10-26. Root-only implementation/self-review; no independent audit.

The old closing callback right-nests every closer and refuses unsolved leaves.
The new opt-in IntervalMap.lean reuses the retained native Methods/traversal,
executes only the first subsequent tactic and collects surviving goals. Later
native stage suffix bytes remain outside. No native interval tactic or active
service is replaced. No early failure/rejection certificate is established.

## Executed scope

- Definition compile against actual retainedLean4.9rc1 and Mathlib:exit0.
- Original48source native parse:48sources/116map sites,0parse errors,
 0candidate body elaborations.
- Native AST validates variable order,one nested first stage and untouched
 later-stage kinds; exact original bytes restore through inverse edits.
-19norm_num,17omega,12simp_all first stages.19sources retain later suffixes.
- Default close-mode original/import-control/lazy/parser input files remain
 byte-identical to the previous preparation. Existing data/module stay intact.
-22small native/map control sources parse,0proof executions. Expectations are
 plans, not observed accepted/rejected results.

[Structural receipt](parser-validation.json), [source preparation](original48-preparation/preparation.json),
[successful compilation/parser](compile-parse-003/receipt.json),
[control parser](control-parser-validation.json),
[default compatibility](default-close-backcompat.json).

The compiler/parser controller samples its own tree plus the active fullpair
every1s; all receipts have0pressure/monitor errors. Successful original48parse
combined peak40,257,093,632B; control parser47,179,034,624B; all below
51,539,607,552B. This is sampled RSS,not a hard kernel quota or isolated timing.
CPU11 contention is diagnostic overhead alongside the still-active fullpair;
recorded timestamps do not become extra performance samples.

## Retained invalid attempts

compile-parse-001 failed because Lean's root default excluded the source path.
compile-parse-002 fixed the root, then found the actual TSyntax namespace type
mismatch. compile-parse-003 fixes the type and both commands succeed.
All commands/source/log/RSS receipts are preserved,not overwritten.
The initial structural assertion counted equal-span parser wrappers as distinct
tactics; selecting actual tactic/paren nodes resolves it without new parsing.
The control-only copied driver retained a two-command terminal assertion and
returned1after its sole native parser succeeded. The outer caller checked the
actual command exit0and saved the22-source output. This is a wrapper defect,
not failed native parsing or clean runtime qualification. No rerun was needed.

## Pending interpretation

The11native/map pairs cover open Nat/Int leaves,partial nested pruning,
remaining outer goals,try-survivors,inconsistent bounds,rollback,recovered
errors,unsolved goals,admitted proofs and expression generalization. Run actual
controls only after the sole fullpair retires,then original48comparison with
full preparation,wall,RSS,reaping and status-set evidence. Official lean-mlir
body measurement remains next in the pre-existing collection order.

Neither compile/grammar nor failed speculative leaves proves that an original
request fails or times out. Shared metavariables/recovery/diagnostic differences
and retained proof memory remain risks. No speedup,coverage fraction,novelty
or complete native parity is claimed. Engine detector remains disabled.
