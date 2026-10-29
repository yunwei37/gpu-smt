# Shared-node collection guards — engineering dependency,root self-review
Scope:only the finite diagnostic collector/tests/docs. Never mutate,suspend,
delete or manually trigger any cluster CronJob,including agent-duties/backups/
dump/archive. No scheduler,Workspace,permission or security change.

Before native spawn,check hostMemAvailable>=6GiB and prove PID/groupSIGKILL with
small finite owned controls. Use only existing Pod credentials for /readyz;
missing observability fails closed. Poll readiness on one background request so
RSS parent does not wait for HTTP. API failures/stalls or host memory below6GiB
stop the whole capture,retire owned native work and retain operational evidence;
no candidate rejection/resource retry from a host stop.12GiB stays unchanged.

Unit tests cover startup refusal,healthy/bad API outcomes,nonblocking pending
probe,stalled probe,shared memory floor and continuation eligibility of stopped
sources. Actual G10 guarded startup must stop after its short denied control,
withzero expensive native launches. This is not a full collection or native
semantic/performance result. Keep raw failures and all captured records onPVC.
