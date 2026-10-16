# Independent native single-command protocol repair review

Observed 2026-10-16 UTC. Scope: E038/native-command-protocol only. This is a review of a concrete client protocol repair, not an additional experiment, performance comparison, full service qualification or paper gate. I read the before/after Lean source snapshots, actual target-file diff, client-check.executed.py, original Kimina Repl.send/_read_response source and the completed before raw/client/terminal receipts. I did not run a build/test/experiment, inspect or poll active capture, change implementation/OMP files or perform Git writes. Only this report is authored.

## Reproduced defect independently verified from retained evidence

The before command uses the actual installed Kimina server.repl.Repl.send, not a custom response normalizer. The driver sends the import header via is_header=true, then the unchanged original candidate bodies for Proof_00000 and Proof_00004 with only the two shared imports replaced by blank lines, as in the existing supported path. I independently compared the two archived original JSONL records with original input.jsonl positions 0 and 4; they match exactly.

Kimina Repl.send emits ordinary native cmd requests, adds env=0/gc=true after preparation, reads a blank-line-framed native object, json.loads it and returns that object unchanged as the response. It does not unwrap a project-specific branch/timing envelope. The completed before worker returns header env0, exits 0 and reaches normal EOF, so this is a real protocol-shape defect rather than merely a failing launch.

The retained before/private/stdout.gz contains:
- header {"env":0};
- Proof_00000 as an outer object containing branch/timing/fallback metadata plus response:{};
- Proof_00004 as the same envelope, with native error/warning messages nested under its inner response field.

The actual client response records retain exactly that outer envelope. The rejected original has 11 error messages and 3 warnings inside response.messages, rather than messages at the native command-response object's top level. I verified this in the complete raw payload, including original diagnostic source positions. The defect therefore matters to ordinary native consumers that look for top-level messages/error/sorries. The evidence does not independently demonstrate a downstream HTTP verdict being misclassified; do not invent that stronger observation.

## Source change and scope judgment

The entire inspected before/after target-file diff replaces:

    emitLine (← execute base enabled initial query).compress

with:

    let result ← execute base enabled initial query
    emitLine ((result.getObjVal? "response").toOption.getD Json.null).compress

**This net increase of one line is justified and minimal.** It changes the ordinary-command stdout projection to the existing execute result's final native response, including a native replay result when the existing fallback path supplies one. It does not bypass execution, branch drain/destruction, fallback or the timing boundary; execute still completes before the selected field is emitted.

The earlier execute implementation unconditionally constructs its result with a response field; the defensive getD Json.null is therefore not evidence that a missing payload was observed. The repair introduces no new protocol/schema/parser, persistent entity, setting, resource quota or correctness program. An explicit local binding keeps evaluation single and makes the selected output clear.

The batch dispatch/body and batch metadata-on-stderr code are unchanged in this diff. Native runtime/ref/task code, input options, supported env0 regime, resource policies and frozen v1 capture paths are outside this edit. The single-command path no longer exposes branch metadata in stdout; that is precisely the intended native payload compatibility repair, not permission to claim a richer telemetry or interactive API. Native batch behavior is not retrospectively invalidated by the separate ordinary-command envelope bug.

## Status before after-build receipts

The retained before defect and source-level repair are verified. At this review point, successful compilation of the changed source and the actual after-client comparison have not yet been supplied; source plausibility is not compiled execution evidence. Root's planned clean build to a separate test-local output, followed by the same actual client and the same original accepted/rejected source pair on plain/private, is a proportionate regression check of this repair. No additional generated suite or broad correctness campaign is requested.

The after check should retain actual compiler/entry/link/terminal receipts and compare complete native response values without normalization. The necessary concrete observation is the native top-level command response for both cases, including the rejected messages and positions, plus actual worker terminal status. Timing numbers from this tiny protocol check cannot establish acceleration or an RQ3 frontier. A successful repair also does not prove arbitrary persistent REPL handles, FFI isolation, all command forms or full corpus behavior.

This same report will be closed by appending the actual build/after source and raw-result verification when root supplies those receipts. No new plan/review/preflight cycle is needed.


## Additional actual before-client consequence and clean build receipts

Root supplied client-analysis-before.executed.py, its complete stdout/empty stderr, and before-client-analysis.json. I inspected the executed code: it imports the installed official kimina_client.ReplResponse, constructs that object directly from each preserved Repl.send response, calls its analyze() method, and separately applies that same method to the inner native response. There is no root-authored outcome classifier or removed diagnostic field in this comparison.

For Proof_00004, official analysis of the actual old outer wrapper reports status valid; analysis of its complete nested native payload reports lean_error. Proof_00000 is valid in both. This is stronger concrete client-impact evidence than the earlier caution that only a possible downstream top-level consumer mismatch had been shown. It demonstrates this installed official client analyzer's misclassification of this one rejected original response. It still does not prove that a deployed HTTP service or all clients issued the same verdict.

I also inspected build.terminal.json, all 50 recorded build-command statuses and the built-input receipt. The clean separate output build exits 0, with 36.834643531 seconds observed wall and 39.030859 waited child CPU seconds. The retained source-identity receipt states the built backend/runtime snapshots match the intended inputs and identifies the actual generated initializer. These are actual compilation/link receipts, not performance comparison numbers. The build's finite co-run overlap is explicitly retained. The after-client terminal/native-value comparison remains the final item for this same review, not a reason to run another suite.

The full frozen v1 batch path already selects inner response values in batch(); this separate single-command wrapper defect therefore does not by itself invalidate that existing batch matrix or unrelated earlier formal CPU data. Any wider invalidation would require evidence about the actual affected consumer/path, which has not been supplied here.


## Final closing: compiled repair and actual native client outputs

Root supplied completed after/terminal.json, both plain/private native raw stdout/stderr, their complete Repl.send response records, after-client-analysis.json and the actual official-client analysis command/stdout. I independently parsed the raw frames and recomputed full native-value comparisons, without modifying or rerunning the check.

Each after worker returns three frames: header env0, the original accepted Proof_00000 object {}, and the original rejected Proof_00004 object with top-level messages. Each raw frame equals its retained actual client response; plain and private native JSON values are exactly equal for both originals without normalization. The rejected object has all 11 errors and 3 warnings, with the complete message data and source positions preserved. Both stderr streams are empty. Both actual workers report state complete, exit_code 0 and normal_eof true, using the new separate clean-build plain/private executables.

The supplied after analyzer imports the same installed official ReplResponse, asserts complete native-value equality and actual terminal status, and calls analyze(). It reports Proof_00000 valid and Proof_00004 lean_error for both methods. This closes the concrete demonstrated regression: the old single-request envelope made the official analyzer see valid for the rejected original, whereas projecting the native response restores its native error classification.

**Disposition: this minimal native-wire/client-side single-command repair is implemented, cleanly built and verified for the two retained original regression cases. No remaining blocking issue identified within this repair's scope.** Net +1 source line is justified. This is not a deployed HTTP-service test, all-source correctness proof, arbitrary interactive API qualification, new performance result, RQ answer or scientific contribution. Co-run durations/diagnostics are evidence only, not acceleration claims. Frozen batch source/data remain separate: their existing inner-response extraction means this ordinary-command defect does not automatically invalidate their matrix or unrelated earlier CPU results.

No additional experiment, generated correctness suite or another review cycle is required to publish this scoped repair and its retained before/after evidence.
