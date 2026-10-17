# Complete miniF2F native-batch reference — root self-review

All 7,808 original source indices appear once in original order: 2,992 complete,
4,497 rejected and 319 operational. Raw compressed inputs already reside in
the prefix-opportunity artifact. This is complete acquisition, not complete
adjudication of every source:319 verdicts remain operationally unknown.
Whole elapsed 28673.003207251 seconds includes original failures and retirement.
The final native worker exits normally; 82 earlier forced retirements still
censor recorded 7110.958396 CPU seconds. That CPU counter is not total native CPU.

The 82 failed native requests comprise 60 timeouts and 22 read/transport errors.
The returned source-level counts are 234 timeout and 85 read-error outcomes;
request batching explains why these are not request counts. 21 of 22 read-error
request stderr records include std::bad_alloc; the remaining cause is unknown.
The client reports pseudo-terminal EIO on those failures. That message alone
does not establish a project-volume I/O failure or host outage.

The complete caller log pairs every request with one response/failure, with
zero pairing defects and zero overlapping request intervals. Native successful
response roundtrips total 7998.279622034 seconds; failed-request roundtrips total
20672.973233287 seconds, or 72.09908597247705% of the whole clock. This is measured
sequential caller waiting/roundtrip wall, not native CPU, a simplex fraction,
or an internal tactic-stage partition. Cleanup outside each request interval
remains charged by whole elapsed. Thus any eventual observed prefix timing
difference must be reported with failure/verdict transitions; it cannot be
attributed automatically to avoiding repeated successful proof work.

The existing driver 5256 automatically advances to exact prefixes. No second
driver, workload filter, resource value, timeout or native implementation is
introduced. All methods retain the pinned upstream 48 GiB verifier default,
width 4 and the original 300-second request timeout. Exact/unit and ProofNet timing remain
pending; there is no completed reuse speedup comparison. This capture neither
reopens the failed 1.34668x arithmetic route nor supports GPU acceleration.

The observer websocket disconnected at 13:26Z. Live reads confirmed the same
Pod UID 6abd56c1-3d94-489a-ab2b-355c104cdbd0, zero container restarts and the
same live driver. Only the observer was reattached; this reference was never
restarted or clock-spliced. Closed raw files were copied byte-for-byte after
terminal capture and their complete gzip streams were read successfully.

Reproduce caller accounting with analyze-prefix-runs.py on this directory.
Its added cell summaries are exercised on this actual full capture; missing
comparison cells remain pending, never fabricated. This is root self-review,
not independent audit, submission readiness or OSDI acceptance.
