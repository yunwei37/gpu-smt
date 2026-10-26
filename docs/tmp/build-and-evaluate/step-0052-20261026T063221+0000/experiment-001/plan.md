# Preserve retired consumer outcomes before whole-cell completion

FixedRQ2 evidence-retention dependency;not a new performance experiment.
The running source42659a8pair has physical attempts but no finalcapture until
all7808return. A backend Cancelled outcome can later become enginePreempted/
ResourceExhausted and retries;physical records cannot substitute finalconsumer
results. Preserve current healthyrelease unchanged.

Scope:modify the existing resource_pair example only to consume the already
implemented publicEngine::verify_stream API,flush each BatchEvent to a per-cell
results.jsonl,and collect the same original-orderVerification vector for final
Capture. No new queue/policy/service/schema/coreAPI/recordclass. InputIDs and
count must match;EOF withoutComplete remainspartial. Complete meansconsumer
delivery,not prepared-parent retirement or full cell/lifecycle completion.
Existingphysicaljournal and sampledRSS remain. Include journalingI/O in own
cellclocks and do not pool futuredriver with currentone.

All new error/signal paths must await engine shutdown. HandleSIGTERM alongside
existingSIGINT in this example through the same shutdown/drain path;do not
rebuild/replace active release. An outputwrite failure cancels its stream and
still retires ownedwork before propagation. Keep source/timeouts/resources.

Controlledbackend tests prove one finalresult is readable while a slowpeer
is held,completion preserves originalorder and allcallerrows,and abort/write
failure leaves an explicitly incompleteprefix with noComplete. Backend honours
cancellation;actualownprocess tests/whole-Rust validation remain in the existing
suite. These are fixture retention tests,not Leanparity or nativeperformance.
Use CPU10–11and48GiB combined monitor;one nativegroup stays the preservedpair.
Update example/benchmark reference scope,root self-review,then commit/pushmain.
