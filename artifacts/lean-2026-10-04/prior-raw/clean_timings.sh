#!/bin/bash
K=/tmp/lean-kernel-arena/_build/checkers/official/src/.lake/build/bin/kernel
T=/tmp/lean-kernel-arena/_build/tests
run(){ taskset -c 0-7 /usr/bin/time -f "$1 wall=%e user=%U sys=%S rss_kb=%M" $K $2 $3 >/dev/null 2>/tmp/ct.err; grep -o "$1 .*" /tmp/ct.err; }
for i in 1 2; do run "off_std_$i" "" $T/std.ndjson; run "po_std_$i" "--parse-only" $T/std.ndjson; done
run "off_cslib_1" "" $T/cslib.ndjson
run "po_cslib_1" "--parse-only" $T/cslib.ndjson
run "off_mathlib_1" "" $T/mathlib.ndjson
run "po_mathlib_1" "--parse-only" $T/mathlib.ndjson
echo CLEAN_DONE
