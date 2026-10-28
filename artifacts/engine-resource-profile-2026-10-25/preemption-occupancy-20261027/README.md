# Native preemption occupancy — complete analysis

[Result/self-review](result-review.md) joins all7852native physical births.
44initial preempted spans have3514.05s union,44exclusive retries9479.74s.
These are occupied intervals,not removable elapsed orAmdahl inputs.
The actual32FIFO/task-memory pair remains unchanged and in progress.
Run python3 analyze.py to recompute. Root self-review only.

[Later sampled-headroom analysis](retry-headroom-20261028.md) distinguishes
exclusive policy from continuous memory saturation and states why tail movement
does not eliminate exclusive computation. It is retrospective accounting,
not a measured resource repair gain or a real-system Amdahl bound.
