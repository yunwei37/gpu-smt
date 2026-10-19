# Root plan self-review

This is self-review, not independent review or an additional research gate.
The selected RQ is the existing end-to-end baseline comparison (RQ3).
The two changes address observed service failures, not speculative tuning.
The raw stack establishes a live event-loop stall; the separate large-line
trace establishes a transport limit. NullHighlighter preserves log payloads;
chunked framing preserves following messages rather than discarding excess
bytes. Exact source snapshots, patch and upstream MIT license are retained.

The real qualification includes the actual stalled source and earlier
failures, rather than only easy accepted proofs. Its selected timings have
no corpus-performance meaning. Resource failures remain visible; equal
within-pair resources and a new declared application epoch are necessary.
No new cache admission, agent, server deployment or research controller is
authorized or introduced. The whole-population native/SHRED comparison stays
incomplete until both methods actually finish, with semantic differences
retained. No standalone paper result follows from this dependency repair.
