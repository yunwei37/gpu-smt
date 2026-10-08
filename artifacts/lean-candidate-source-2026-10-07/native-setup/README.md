# Exact native dependency restoration

Completed 2026-10-07–08 UTC in the retained owning Workspace. The source build of Mathlib and REPL exited0 at23:59:31UTC. See the pinned sources, adaptations, download hashes and binary identities in the adjacent JSON records and complete original/cache/failed/resumed build logs. No model, GPU or scientific performance run occurred in setup. The original miniF2F `mathd_algebra_478` command with explicit `sorry` returned exit0, a sorry goal and a warning; that is an **incomplete** proof. Exact transport bytes remain adjacent.

Lean4.9.0-rc1 is `be6c4894e0a6c542d56a6f4bb1238087267d21a0`, Mathlib is `2f65ba7f1a9144b20c8e7358513548e317d26de1`, and forked REPL is `3334a97b268ecc67beb36a75787f7e831208a724`. REPL binary SHA-256 is `f6a0201a2dc6b929a93b34e00e74e9c9888ba7f9a5a7b3c2ed0b89a199025c42`. Exact dependent revisions are in the upstream manifest. The vendor manifest substitutes local paths for those exact downloaded archives; no Lean/Mathlib/REPL source or options were changed. Lake emits seven git/path adaptation warnings on stderr; they remain raw, not suppressed or mistaken for native Lean diagnostics.

The retained dependency directory is `/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture`. `reproduce.sh` **only builds already restored sources**. `finish-setup.py` is the historical one-shot restoration/engagement script with its original owned-process wait; it is retained for provenance, not a portable reproduction entrypoint or research controller. Do not run it as a fresh reproduction. If the source tree is absent after dependency loss, use these steps from repository root. If sources already exist, skip archive restoration and use the build command below; the historical setup script expects an upstream manifest, not the adapted vendor manifest:

```bash
capture_root=/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture
mkdir -p "$capture_root/downloads" "$capture_root/logs"
cp -n artifacts/lean-candidate-source-2026-10-07/native-setup/setup.py "$capture_root/setup.py"
test ! -e "$capture_root/mathlib4/lake-manifest.json"
python3 "$capture_root/setup.py"
cp artifacts/lean-candidate-source-2026-10-07/native-setup/lake-manifest.vendor.json "$capture_root/mathlib4/lake-manifest.json"
```

`setup.py` fetches official exact-pinned archives, records actual download identities and extracts only absent source directories. Validate those downloads against retained `download-metadata.json`. The packaging fix below fetches official ProofWidgets v0.0.36 and restores only its16JS assets, rather than taking Lean build outputs from the release. Its pinned release hash is checked before extraction:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, tarfile, urllib.request
b = Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture')
p = b / 'downloads/ProofWidgets4-v0.0.36-release.tar.gz'
if not p.exists():
    urllib.request.urlretrieve('https://github.com/leanprover-community/ProofWidgets4/releases/download/v0.0.36/ProofWidgets4.tar.gz', p)
assert hashlib.sha256(p.read_bytes()).hexdigest() == '23f5a0e4bf8eb746e795ee04a57f5960714d9f303989667bdd12a00f0a143d36'
target = b / 'mathlib4/.lake/packages/proofwidgets/.lake/build'
with tarfile.open(p) as t:
    members = [m for m in t.getmembers() if m.name.startswith('./js/') and m.isfile()]
    assert len(members) == 16
    t.extractall(target, members=members, filter='data')
PY
export PATH="$capture_root/lean-4.9.0-rc1-linux/bin:$PATH"
export LEAN_NUM_THREADS=4
export XDG_CACHE_HOME="$capture_root/cache"
(cd "$capture_root/mathlib4" && taskset -c 0-3 lake build Mathlib repl)
```

This is a full source build, not a guaranteed fast cache download. The actual Azure cache had roughly100 misses before its owned request was stopped; do not claim a complete cache outage. The initial source build failed on missing JS, then the retained resumed build succeeded. Exact source/binary/transport records distinguish those attempts. Portable reproduction also needs ordinary C build tooling and network access to the public archives. Different local build/runtime libraries can change binary hashes, so record actual resulting identities.

Native verification must prepend the exact release bin directory to PATH: `Lean.findSysroot` calls `lean --print-prefix`. For single-CPU cost controls set `LEAN_NUM_THREADS=1` and use the runner's documented `taskset -c 0` invocation. Persistent pinned REPL output needs stock `stdbuf -oL`, supplied and identified by the warm runner; no native source patch is used. Affinity does not establish isolation from competing work.
