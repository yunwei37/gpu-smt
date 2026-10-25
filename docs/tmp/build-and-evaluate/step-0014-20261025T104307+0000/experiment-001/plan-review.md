# Plan self-review

The fixture is not a Lean performance experiment. It tests scheduler order under
legal prediction latency, a real public-policy contract. Source order is not
assumed from final result order. Cache/in-flight tickets and preemption priority
are the primary repair risks. Main/capture/source preservation boundaries hold.
