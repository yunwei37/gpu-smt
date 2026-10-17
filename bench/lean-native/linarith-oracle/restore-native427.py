"""Restore the pinned native arithmetic dependencies after Pod replacement.
Runs only inside the owning Workspace. Build/run files resolve onto its existing
PVC; no Workspace, service, scheduler or research checkout is created.
"""
from pathlib import Path
import datetime, json, os, shutil, subprocess, traceback

R = Path("/workspaces/repository")
STATE = Path("/workspaces/.agent-state/gpu-smt-native427-20261017-recovery")
T = Path("/tmp/gpu-smt-goedel427-20261014")
F = Path("/tmp/gpu-smt-farkas-fast427-20261014")
U = Path("/tmp/gpu-smt-linarith-oracle-20261017")
D = R / "artifacts/lean-modern-native-compilation-2026-10-14"
SNAP = D / "source-snapshot-20261015"
MATHLIB = "a3a10db0e9d66acbebf76c5e6a135066525ac900"
SDK_URL = "https://github.com/leanprover/lean4/releases/download/v4.27.0/lean-4.27.0-linux.tar.zst"
STATE.mkdir(exist_ok=True)
records = []
env = dict(os.environ)
env["PATH"] = str(T / "lean-4.27.0-linux/bin") + ":/usr/local/cargo/bin:" + env["PATH"]
env["CARGO_HOME"] = "/usr/local/cargo"
env["RUSTUP_HOME"] = "/usr/local/rustup"

def run(cmd, cwd=R):
    with (STATE / "restore-build.log").open("ab") as log:
        log.write((repr(cmd) + "\n").encode()); log.flush()
        proc = subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    records.append({"command": list(map(str, cmd)), "cwd": str(cwd), "exit": proc.returncode})
    proc.check_returncode()

def restore(group, dst, overlay=False):
    entries = json.loads((SNAP / "source-map.json").read_text())["entries"]
    for e in entries:
        if e["group"] != group:
            continue
        target = dst / e["source_relative_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        original = R / e["repository_path"]
        if target.exists() and target.read_bytes() != original.read_bytes():
            if group == "gc-repl" and any(
                x["group"] == "native-repl" and x["source_relative_path"] == e["source_relative_path"]
                and target.read_bytes() == (R / x["repository_path"]).read_bytes() for x in entries):
                continue
            bases = [R / x["repository_path"] for x in entries
                     if x["group"] == "gc-repl" and x["source_relative_path"] == e["source_relative_path"]]
            if not overlay or not any(target.read_bytes() == x.read_bytes() for x in bases):
                raise RuntimeError("preserve differing source: " + str(target))
        shutil.copyfile(original, target)

def main():
    for alias, name in [(T, "goedel427"), (F, "farkas-fast427"), (U, "linarith-oracle")]:
        target = STATE / name
        target.mkdir(exist_ok=True)
        if alias.is_symlink():
            assert alias.resolve() == target
        elif alias.exists():
            raise RuntimeError("preserve pre-existing path: " + str(alias))
        else:
            alias.symlink_to(target, target_is_directory=True)
    sdk = T / "lean-4.27.0-linux"
    archive = STATE / "lean-4.27.0-linux.tar.zst"
    if not sdk.exists():
        if not archive.exists():
            run(["curl", "-fL", "-o", str(archive), SDK_URL])
        run(["tar", "--zstd", "-xf", str(archive), "-C", str(T)])
    math = T / "mathlib4"
    if not math.exists():
        run(["git", "init", str(math)])
        run(["git", "remote", "add", "origin", "https://github.com/leanprover-community/mathlib4"], math)
        run(["git", "fetch", "--depth=1", "origin", MATHLIB], math)
        run(["git", "checkout", "--detach", "FETCH_HEAD"], math)
    got = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=math, text=True).strip()
    assert got == MATHLIB, got
    if not (math / ".lake/build/lib/lean/Mathlib.olean").exists():
        run(["lake", "exe", "cache", "get"], math)
    run(["lake", "build", "+Mathlib.Tactic.Linarith:dynlib"], math)
    fm = F / "mathlib4"
    if not fm.exists():
        fm.symlink_to(math, target_is_directory=True)
    assert fm.resolve() == math.resolve()
    pkg = F / "farkas427"
    restore("product-farkas", pkg)
    deps = pkg / ".lake/packages"
    if not deps.exists():
        deps.parent.mkdir(exist_ok=True)
        deps.symlink_to(math / ".lake/packages", target_is_directory=True)
    assert deps.resolve() == (math / ".lake/packages").resolve(), "preserve duplicate tree; deduplicate only after stopping its build"
    run(["lake", "build", "Farkas.Fast", "Farkas.Products"], pkg)
    repl = T / "repl-kimina-native-gc-header-repair"
    restore("gc-repl", repl)
    restore("native-repl", repl, overlay=True)
    run(["lake", "build", "repl"], repl)
    restore("external-support", U / "native")
    run(["cargo", "fetch", "--locked", "--manifest-path", str(U / "native/Cargo.toml")])
    for name in ["build-stages.py", "build-oracle.py", "build-strong-profile.py"]:
        run(["python3", str(R / "bench/lean-native/linarith-oracle" / name)])
    required = [Path(line) for line in (D / "native-load-list.txt").read_text().splitlines() if line]
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        raise RuntimeError("native closure missing: " + repr(missing[:10]))
    return {"status": "built; source-native matched preflight still required",
            "sdk": str(sdk), "mathlib_revision": got, "native_libraries": len(required)}

if __name__ == "__main__":
    result = {}
    code = 1
    try:
        result = main()
        code = 0
    except BaseException:
        result = {"status": "failed, not performance evidence", "error": traceback.format_exc()}
    result.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), commands=records)
    (STATE / "restore-terminal.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)
    raise SystemExit(code)
