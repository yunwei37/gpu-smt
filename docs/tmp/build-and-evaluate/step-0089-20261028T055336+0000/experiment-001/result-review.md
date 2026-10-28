# Retained native crash diagnosis — root self-review

No new proof request was run. Two private cores of minif2f-2325, first prepared
and then fresh fallback, are readable with their actual explicit executables.
Both stop at SIGABRT through C++ failed_throw and the interpreter check_system.
The pinned upstream source converts stack_space_exception to a throwable
containing an interpreter stacktrace. The fresh executable disassembly places
the observed return PC immediately after that throw. Existing completed
fresh/prepared captures for2325and3209 preserve670/672frames per truncated stderr tail,ending at interpreter
frame6845/6960,and dominated by native Mathlib simplex frames; the original untruncated beginning
was not retained. This identifies a shared native interpreter stack-exception
termination path,not a COW-only fault or an oracle optimization opportunity.

The first automatic-image LLDB attempt had no executable images and failed;
its raw output is retained. Explicit-file attempts both exit0 and produce the
actual frames. Guard receipt separately records51,413,577,728B combined sampled
peak against51,539,607,552B,no pressure abort/error. This is close to the budget,
not extra native capacity. Temporary derived core copies were removed and the
original private compressed bytes remain. Public output contains symbols,not
locals,argument values,environment or core memory. Source and existing-public
error copies are losslessly compressed with decompressed byte comparison.

Why historical warm returned structured rejection instead remains unproven.
The retained warm and fresh REPLs have known source differences;their ordinary
runCommand is unchanged in the compared source,while the prepared host is a
different executable. Pending matching qualification includes all six prior
status divergences. Do not change stack/heartbeat settings,turn crashes into
Lean rejection,or claim a proof of falsehood/nontermination from these traces.
No arithmetic CPU oracle path is run or modified. Current FIFO stays frozen.

Source: https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/library/compiler/ir_interpreter.cpp
Raw commands and individual failures/successes:diagnosis-explicit-receipt.json,
retained-core-traces/,explicit-core-traces/,and diagnosis.json.

Raw debugger/disassembly files with trailing formatting whitespace are retained
as .gz after full decompressed byte comparison;their bytes were not trimmed.
