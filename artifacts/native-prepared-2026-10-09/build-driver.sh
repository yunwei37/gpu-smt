#!/usr/bin/env bash
set -euo pipefail
source_root=/workspaces/.agent-state/gpu-smt-deps/z3-4.16.0-source
repo_root=/workspaces/repository
cd "$source_root/build"
g++ -D_MP_INTERNAL -DNDEBUG -D_EXTERNAL_RELEASE -std=c++20 -fvisibility=hidden -fvisibility-inlines-hidden -mfpmath=sse -msse -msse2 -O3 -fPIC -I../src -c "$repo_root/bench/native_z3_prepared.cpp" -o "$repo_root/artifacts/native-prepared-2026-10-09/native_z3_prepared.o"
g++ -o "$repo_root/artifacts/native-prepared-2026-10-09/native-z3-prepared" "$repo_root/artifacts/native-prepared-2026-10-09/native_z3_prepared.o" shell/mem_initializer.o shell/gparams_register_modules.o shell/install_tactic.o libz3.a -lrt -lpthread
