#!/bin/bash
cd /tmp/lean-kernel-arena
K=_build/checkers/official/src/.lake/build/bin/kernel
ND=_build/checkers/nanoda/src/target/release/nanoda_bin
LZ=_build/checkers/nanoda/src/target/release/nanoda_bin
NANODA_DIR=_build/checkers/nanoda/src
# parse-only on cslib
taskset -c 0-7 /usr/bin/time -f "PARSE-ONLY cslib wall=%e rss_kb=%M" $K --parse-only _build/tests/cslib.ndjson >/tmp/outpo-cslib.log 2>/tmp/tvpo-cslib.log
# parse-only on mathlib
taskset -c 0-7 /usr/bin/time -f "PARSE-ONLY mathlib wall=%e rss_kb=%M" $K --parse-only _build/tests/mathlib.ndjson >/tmp/outpo-mathlib.log 2>/tmp/tvpo-mathlib.log
# nanoda on mathlib 24 threads
python3 -c "import json;d=json.load(open('$NANODA_DIR/config.json'));d['num_threads']=24;json.dump(d,open('$NANODA_DIR/config.json','w'))"
/usr/bin/time -f "NANODA mathlib t24 wall=%e user=%U rss_kb=%M" taskset -c 0-23 $ND $NANODA_DIR/config.json < _build/tests/mathlib.ndjson >/tmp/nanoda-mathlib.out 2>/tmp/nanoda-mathlib.err
# official on mathlib (long)
taskset -c 0-7 /usr/bin/time -f "OFFICIAL mathlib wall=%e rss_kb=%M" $K _build/tests/mathlib.ndjson >/tmp/out-mathlib.log 2>/tmp/tv-mathlib.log
echo ALLDONE > /tmp/run_remaining.done
