# Root outer self-audit

Checked source bytes against the prepared batch, unchanged default300s and
root400000 stack setting, actual environment-query exit, no proof invocation,
and no dependency update. The source/control distinction stays explicit.

The script does not wait for the old group or launch itself; all old controller/
CLI births must retire before invocation. A fresh CLI build happens only after
that boundary. It forwards existing backend flags rather than adding a recorder.
Full profiler messages can add overhead; missing exports stay censored and
nested stages are not summed into a false Amdahl ceiling.

Existing one-second combined monitoring records a34.827GB peak, not a hard
48GiB guarantee. CPU query overlap is disclosed. No native collection or
scientific result is claimed. Only this thread executed and reviewed.
