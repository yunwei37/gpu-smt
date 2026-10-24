# First worker-stream qualification failure

The client sent a literal backslash-n rather than newline, leaving both owned
workers waiting for input. Only the exact qualification client and its children
were terminated after PID/command ownership verification; the original
full-observation tree was untouched. The lifecycle controller retained the
failure and performs normal graceful provider exit and exact-UID Job cleanup.

The failing client source is reconstructed from the exact two-line escape
correction and retained as failed-client-reconstructed.py.gz. This was not
captured before execution and is labelled accordingly. Raw watchdog/provider/
lifecycle records remain; no GPU kernel execution, witness result or performance
is claimed from this failed attempt.
