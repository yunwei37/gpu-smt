# Execution-budget erratum and forward correction

M;2026-10-30UTC;self-review. The six-cell native timing matrix consumed
3081.952716seconds (51.365879minutes) in native-cell wall time alone.
This exceeds the user's30minute collection bound at whole-group scope.
The per-native1500s bound did not make the overall collection compliant.
That execution error is acknowledged; no data erased,no time rescaled and
no retrospective approval claimed. Individual memory/CPU limits held,but
they do not excuse the group duration. Original controller version and all
receipts remain in prior commits and the PVC capture.

Forward correction:run_native_cohort.py now computes each next native's
internal self-alarm from the remaining1800s whole-group window,clipped by
the existing1500s per-cell ceiling. It stops after a native failure,partial
return or group deadline and writes an explicit partial terminal. It no
longer resets a full25minute allowance for every queued cell. Five offline
checks include600s already spent and near-expired windows. No existing
capture is restarted or rewritten.

This is a cooperative/internal-alarm bound with retirement/I/O overhead;
it is not an external kill guarantee or a hard kernel execution quota.
The real external-signal restriction remains unchanged. Future planned
groups must fit the whole30minutes; partial output is preserved on expiry.

Subsequent short PC-qualification,median representative and closed-certificate
groups each take under3minutes of native time. All natives have retired.
No other branch's processes,files or scheduling were changed.
