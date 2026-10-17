# Successful versus unsuccessful LP paths — 24-source diagnostic

This is a real small qualification, not a 1,000-source result or GPU prediction.
The raw all-call data make the earlier success-only omission visible:

| Path | Calls | Floating LP CPU s | Exact LP search CPU s |
|---|---:|---:|---:|
| Direct, ultimately checked branch |110|0.4010|3.2021|
| Direct, no certificate/error |5|0.0503|0.6567|
| Native fallback service, certificate |5|0.1460|2.3853|
| Native fallback service, no certificate/error |5|0.0512|3.1050|

Exact LP search is NOT exact support repair. Repair CPU in these observed
branches is only about 0.0075 seconds combined. The direct checked pool alone
does not cover failed attempts or the native fallback service. A GPU float
solver must also find usable supports on the cases where the current floating
simplex falls through to expensive exact search; speeding the already cheap
floating simplex alone does not remove those exact solves.

The complete capture will determine how often this pattern occurs, including
heavy tails, scales and concurrent ready requests. No continuation/closure
decision follows from 24 sources. Source state, raw counters and classifications
remain in cost-by-return-state.json. Root self-review only.
