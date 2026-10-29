# REPL malformed-diagnostic correctness regression

Root-only OSS correctness work while the single frozen native collection runs.
The public classifier currently checks only the outer messages array. A payload
with env=0 and messages=[null] can be reported Accepted and become cacheable.
Reproduce before changing production classification. Consult both retained
upstream REPL/JSON.lean Message declarations: severity trace/info/warning/error,
data String. Validate only fields used for verdict decisions, preserve raw JSON.
Exercise unknown/missing/wrong-type fields, an earlier error followed by malformed
diagnostics, and all four valid severities. A process fixture must show two
sequential identical malformed requests execute twice rather than cache.
No new native collection, production setting, dependency or cache identity.
Validation uses approved CPUs10–11, combined owned/support RSS sampling48GiB;
a support overrun aborts support work. These are fixtures, not native proofs,
throughput or scientific evidence. Existing native CI remains required.
