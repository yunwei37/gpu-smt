#!/usr/bin/env bash
set -euo pipefail
export AUTOVERUS_DEPS=/workspaces/.agent-state/gpu-smt-deps/autoverus-verus-33269
export RUSTUP_HOME="$AUTOVERUS_DEPS/rustup"
export CARGO_HOME="$AUTOVERUS_DEPS/cargo"
export CARGO_BUILD_JOBS=4
export PATH=/usr/local/cargo/bin:$PATH
mkdir -p "$RUSTUP_HOME" "$CARGO_HOME/bin"
cp /usr/local/cargo/bin/rustup "$CARGO_HOME/bin/rustup"
for proxy in cargo rustc rustdoc rustfmt; do ln -sf rustup "$CARGO_HOME/bin/$proxy"; done
export PATH="$CARGO_HOME/bin:$PATH"
rustup toolchain install 1.76.0 --profile minimal --component rustfmt --component rustc-dev --component llvm-tools
cd "$AUTOVERUS_DEPS/verus-33269ac6a0ea33a08109eefe5016c1fdd0ce9fbd/source"
curl -fL https://github.com/Z3Prover/z3/releases/download/z3-4.12.5/z3-4.12.5-x64-glibc-2.31.zip -o "$AUTOVERUS_DEPS/z3-4.12.5-x64-glibc-2.31.zip"
unzip -o "$AUTOVERUS_DEPS/z3-4.12.5-x64-glibc-2.31.zip" -d "$AUTOVERUS_DEPS"
cp "$AUTOVERUS_DEPS/z3-4.12.5-x64-glibc-2.31/bin/z3" z3
source ../tools/activate
vargo build --release
