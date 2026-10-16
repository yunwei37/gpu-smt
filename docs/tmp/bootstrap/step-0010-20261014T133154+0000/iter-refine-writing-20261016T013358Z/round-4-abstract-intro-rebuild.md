# Round4 — abstract/introduction role mapping and rebuild

Started 2026-10-16T01:40:07.428896+00:00; parent
Step0010BOOTSTRAPWRITE. Root performs complete rewrite-abstract-intro procedure
personally, reading both full references and the current complete paper body
as source of truth. No researchdoc supplies a new claim. Entry Round3output;
no independent reviewer or fake Skill invocation.

## Mapping and reorganization plan before editing

| Current intro paragraph | Current/target role | Decision and body source |
|---|---|---|
|1|Background|Keep role; tighten the service-interface sentence, preserving fullSMT definition/citations and proofconstruction/checking/frontend translation|
|2|Problem|Retain: repeatedpreparation/sharedexecution, resourcegrowth/contention/cancellation and concrete sharedLeancontext example|
|3|Rootcause|Retain: nativehistory includes solverheuristics/resourcecounters and mutableelaborator state; needed by insight|
|4|Existingmethods|Retain: resultcache, REPL, snapshots, Kimina, AXLE; no unsupported claim that none already isolates requests|
|5|Insight|Retain verbatim: preparation separated from candidate history/lifetime; value depends on preparation/branch/mutation cost|
|6|Challenges|Retain: supportedquiescence, faithfulnative resourcehandling and boundedmemory; technically required by Design|
|7|System/method/resultslot|Retain: parent/branches, ownedmutable state/resources, nativefallback, wholematchedLean/SMT and5090costs; resultplaceholder staysmissing|
|8|Contributions|Retain four concrete deliverables and sectionlinks; no new insight or novelty|

Required roles are unmerged and in causalorder. Optional rootcause/challenges
are justified by the declared mechanism; the system paragraph answers them.
No concept is needed from outside the paper; no missing result can be supplied
by writing. No content/citation/number is cut or moved into a different meaning.
There is no separate confirmation gate inside this orchestrated writing pass.

## Paragraph-by-paragraph application

Apply one reviewed edit to Backgroundparagraph1: replace verbose 'Services
check these attempts with ... that ...' with the same direct 'Services use ...
to ...' interfaces. Preserve every operation and citation. Inspect paragraphs
2–8 in templateorder and retain them verbatim for the reasons above rather
than force cosmetic or claim-changing rewrites.

Derive the abstract only after that paragraph pass. Existing sentences map
one-to-one: A1→I1background, A2→I2problem, A3→I3cause, A4→I4existingmethods,
A5→I5insight, A6→I6challenges, A7→I7system, A8→I7methodology, A9→I7resultslot.
Tighten A7 to state explicitly that its immutableprepared state is retained
in a parent, already stated in I7 and Design. Retain every other sentence's
same meaning/terminology/order; no newGPU or serviceperformance is invented.
Actualdiff/compilation/selfcheck follow below.

## Completed self-check

Completed 2026-10-16T01:40:10.272895+00:00.
Actualdiff changes the claimed intro/abstract sentences; unchanged paragraphs
are explicitly retained, not falsely reported rewritten. Abstract remains one
paragraph/235whitespace words with nine rolepositions. Each sentence has
its Iparagraph source, the dominant insight remains A5/I5, and the complete
background→problem→cause→competitors→insight→challenges→system→contributions
chain is preserved. Missing resultslot remains missing. No value or citation
occurrence disappears; original numeric/citation multisets pass for each edit.
Compile {'returncode': 0, 'pages': 'Pages:           14', 'pdf_bytes': 177115}; no error/overfull/undefined diagnostic. No sourceoutside
main.tex or experiment is changed. Scientificevidence/submission/independence
remain open. Next Round5 consistency.
