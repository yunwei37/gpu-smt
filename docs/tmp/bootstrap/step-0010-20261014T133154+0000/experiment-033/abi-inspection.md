# Pinned export ABI inspection

Actual generated ExprDefEq.c from installed4.27 source declares and defines
lean_is_expr_def_eq with six lean_object* arguments and lean_object* result.
The generator process ended and its full2,076,210byteCfile/emptydiagnostic log
are retained privately. Its first launcher did not retain an actual exitcode;
do not invent one. This is dependency inspection, not native preflight/result.

Expr.lean's own source exports constant-time flags. Its separate synchronous
generation has an actual returncode in expr-flags-abi-command.json and complete
generated C retained privately. Wrapper ownership must match those definitions
and the original six-argument export before linking a private executable.
No active SDK/library/source/binary is changed.
