# Step0018 — smoke upload scope repair

Root only,self-review. Prior native source backend and recorded evidence are
committed/pushed. The final smoke job passes validation but uploads all retained
research data rather than its own outputs.

## EXPERIMENT_GATE

Actual tooling fault:2.956GB/13417tracked files enter every smoke upload.
Inspect producer paths and narrow the existing upload, preserving all original
and failed research data. No new native collection, benchmark or runtime delta.

## WRITE_GATE

Keep observation and exact unchanged producer/output list. No paper result.

## REVIEW_GATE

Review small YAML diff; verify every chosen path is generated/validated by the
existing smoke steps and no actual smoke output is lost. Observe next real CI.
This is root self-review, not independent audit; goal/fourRQremain active.
