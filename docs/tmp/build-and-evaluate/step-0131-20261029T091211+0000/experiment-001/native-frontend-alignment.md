# Native frontend code audit correction
PinnedLean4.9Frontend.processCommandandREPL/Frontend.processCommandsWithInfoTrees
are read in the Workspace. Earlier instrument modes agreed with each other,
but that alone did not prove REPL parity(as already stated). Align the actual
native contract before population measurement:
- enable info trees as the installed REPL does;
- pass pre-parse command start,not next parser position;
- integrate parser messages before elaboration in original order;
- elaborate terminal command before ending;
- retain prior command syntax as the nativeFrontenddoes;
- native newline normalization default(selected2677sourcescontainnoCR).
Original/profile/source bytes unchanged;observer result reuse remains disabled.
This is a forward repair,not rewriting old control receipts as stronger evidence.
