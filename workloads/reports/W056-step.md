# W056: distinguish advertised fields from released trajectory payloads

## EXPERIMENT
Checked all16025detailed-table rows: generate_prompt,fix_prompts and debug_files
are each empty strings in every row. Schema documentation did not establish
released prompt content. Corrected W054's README wording; raw tables remain
unchanged. Final code and verifier-feedback observations remain valid.

Made Lean snapshot counts reproducible in a small table: primary626unique
texts, scripts1503files/1490unique, byte-intersection626, union1490. Repository
source totals now include full trees, separate from selected output scopes.

Read all12official Vero issue/PR threads and comments without posting or
modifying anything. Localized diagnostic/code fences and reference/spec repair
proposals exist, but no complete model-run bundle/trajectory link was identified.
External reports were not locally proved and fragments are not counted as
complete candidates. Main revision is not silently replaced by a proposed PR.

## WRITE
Added trace-field completeness, exact-byte uniqueness, repository-source and
public-thread audit CSVs. README explicitly corrects the prior schema-based
prompt statement and scopes absence/access limitations. No source data removed.

## REVIEW: self-review
Field-value completeness is checked across the full45table payload, not one
example. No prompts, verification attempts or missing failures are reconstructed
or generated. Issue content does not establish model provenance or licensing of
a runnable candidate; only small metadata is committed. No new native, lock
take, additional agent, infrastructure or other-lane work.
