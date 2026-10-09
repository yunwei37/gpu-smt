#!/usr/bin/env bash
set -euo pipefail
export RUSTUP_HOME=/workspaces/.agent-state/gpu-smt-deps/autoverus-verus-33269/rustup
export CARGO_HOME=/workspaces/.agent-state/gpu-smt-deps/autoverus-verus-33269/cargo
export PATH="$CARGO_HOME/bin:$PATH"
export RUSTUP_TOOLCHAIN=1.76.0
python3 -u bench/autoverus_native_capture.py --cohort-raw artifacts/autoverus-source-2026-10-07/cohort/raw --verus /workspaces/.agent-state/gpu-smt-deps/autoverus-verus-33269/verus-33269ac6a0ea33a08109eefe5016c1fdd0ce9fbd/source/target-verus/release/verus --real-z3 /workspaces/.agent-state/gpu-smt-deps/autoverus-verus-33269/verus-33269ac6a0ea33a08109eefe5016c1fdd0ce9fbd/source/target-verus/release/z3 --out artifacts/autoverus-native-2026-10-09/preflight2 --repeat 1 --cores 8 --timeout 120 --indices 0,11
