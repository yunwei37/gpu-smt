# Plan root self-review

Executor/reviewer are thisthread,not independent. Reuse BatchEvent and the
existing stream API instead of a second eventframework/controller/checkpoint
schema. A per-consumer row is not interchangeable with a physical backend row;
retain both scopes. Final Capture and terminal remain whole-cell authorities.
Validate IDs/index/count before acceptingComplete. Flush is not fsync/power-loss
durability. Keep partialfiles on I/O/cancellation and alwaysawait ownedcleanup.

Changing observation I/O has actualcost;retain it in futurecell/lifecycle clocks.
No currentcapture hotpatch or claims about old results being retroactively
recoverable. No sourceforecast/model/reliablefailure predicate is added, and no
frozenroute/competitor work resumes. The single native slot is respected.
