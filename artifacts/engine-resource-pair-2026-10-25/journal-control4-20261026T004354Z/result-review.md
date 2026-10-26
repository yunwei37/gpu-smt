# Durable per-attempt native evidence — root self-review

The previous reusable pair example wrote its complete Capture at cell end.
SIGINT retained results,but a parent failure before cell end could lose
completed native outcomes. Add an example-local backend decorator that flushes
each physical attempt's native Outcome,source/task identity,remaining attempt
timeout,retry kind and backend elapsed time before returning it to the engine.
Final Capture still owns queue/cancellation/consumer clock and full provenance.
Flush is process-interruption persistence,not power-loss/fsync durability.

Delegate identity,prepared-state readiness,ordinaryverify,exclusive resource
retry andshutdown to the original backend. No scheduler/admission/native
decision change. Journal I/O errors are retained and prevent a complete
evidence terminal;full rawCapture remains. Journaling costs are included in
both actual resource-pair conditions. It is not source/semantic caching.

New persistence regression reads two flushed resource-failure attempt rows
before any final Capture exists. Fullordinary fmt/Clippy/tests/docs/CLI pass,
releasebuild passes. Real four original sources(0,1,5,10),including twoaccepted/
tworejected,execute freshnative/prepared at the same48GiB/fourCPU point.
Each side writes exactly4journalrows whose native Outcomes equal final Capture;
native/prepared statuses and accepted sets match,zerojournalerrors,
allattempt/parent/driverprocessesretired. Raw small-run clocks arequalification,
not whole-population performance or strongestwarm-baseline benefit.

The earlier actual24qualification and interrupted failure remain untouched.
No newfullgroup has overlapped it. Ready to launch7808sameoriginal source
resources pair after this source boundary iscommitted. Userorderedlean-mlir
follows afterfullpair;originalfailurehooks/old42reruns remain pendingseparately.
Rootself-review,not independent audit;noveltyandallRQanswersstillopen.
