# G10 development signal failure — self-review
A finite two-second /usr/bin/python3 child was spawned by its Python parent under UID0; /proc child status reported UID0, Seccomp0, CPUs0–7. signal0 succeeded; SIGTERM15 and SIGKILL9 returned errno13 PermissionDenied. The child exited normally after two seconds. No credential, permission, security, scheduling or Workspace setting changed.

The existing Linux retired-descendants unit test failed at child.0.kill().unwrap() (linux.rs:209) with the same errno13. Its Drop waited for the helper to naturally retire; all owned processes subsequently retired. Initial workspace validation: 15 engine unit tests passed, 1 failed; later targets were not executed. The eight new failure-cache unit tests passed in that run and in a separate targeted run. This is a development-environment limitation, not evidence that the watchdog works on G10 or that full regression passed.

Keep the test and full CI invocation unchanged. A local rerun may exclude this exact signal-dependent regression and must report the exclusion. Formal Lean collection remains stopped awaiting approved hardware placement.

The final all-target run also encountered existing Lean lifecycle controls:
malformed-retirement assertion mismatch and owned-group preemption not
interrupting its target. The second directly matches the denied-signal symptom;
the first is observed in that environment, not independently localized beyond
its recorded assertion. Raw logs are authoritative; CI remains unchanged.
