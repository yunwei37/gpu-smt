# gpu-smt

A research prototype for **low-latency and high-throughput verification serving**.

The long-term goal is a transparent runtime that accelerates existing formal verification workloads without requiring changes to Z3/cvc5/Lean or to the applications that use them. The first milestone is to characterize real solver traces and quantify how much state can be reused across otherwise independent verification jobs.

See `docs/research-plan.md` once the initial research branch lands.
