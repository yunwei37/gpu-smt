#!/bin/bash
set -eu
capture_root=/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture
export PATH="$capture_root/lean-4.9.0-rc1-linux/bin:$PATH"
export LEAN_NUM_THREADS=4
export XDG_CACHE_HOME="$capture_root/cache"
cd "$capture_root/mathlib4"
taskset -c 0-3 lake build Mathlib repl
