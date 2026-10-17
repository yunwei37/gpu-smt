"""Restore the pinned formal-prefix dependency paths in the existing Workspace.
Reuses the retained Lean4.9/Mathlib cache. No capture is launched by this build.
"""
from pathlib import Path
import datetime, json, os, shutil, subprocess, traceback

R = Path("/workspaces/repository")
STATE = Path("/workspaces/.agent-state/gpu-smt-native427-20261017-recovery")
DEPS = Path("/workspaces/.agent-state/gpu-smt-deps")
SDK = DEPS / "lean-4.9-capture/lean-4.9.0-rc1-linux"
MATH = SDK.parent / "mathlib4"
NATIVE = Path("/tmp/gpu-smt-native-mathlib-20261014")
SRC = Path("/tmp/gpu-smt-native-repl-20261014")
UPSTREAM = Path("/tmp/gpu-smt-primary-opportunities-20261017/shred")
U = Path("/tmp/gpu-smt-linarith-oracle-20261017/prefix")
REV = "a6616e99534ce777dcebfd56566eaaffb63997a8"
env = dict(os.environ)
env["PATH"] = str(SDK / "bin") + ":" + env["PATH"]
records = []

def run(cmd, cwd=R):
    with (STATE / "restore-prefix-build.log").open("ab") as log:
        log.write((repr(cmd) + "\n").encode()); log.flush()
        p = subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    records.append({"command": list(map(str, cmd)), "cwd": str(cwd), "exit": p.returncode})
    p.check_returncode()

def alias(path, target):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        assert path.resolve() == target.resolve()
    elif path.exists():
        raise RuntimeError("preserve existing path: " + str(path))
    else:
        path.symlink_to(target, target_is_directory=True)

def main():
    STATE.mkdir(exist_ok=True)
    U.mkdir(exist_ok=True)
    alias(NATIVE, MATH)
    run(["lake", "build", "+Mathlib.Tactic.Linarith:dynlib"], MATH)
    target = STATE / "native-repl49"
    alias(SRC, target)
    if not target.exists():
        shutil.copytree(MATH / ".lake/packages/REPL", target,
                        ignore=shutil.ignore_patterns(".git", ".lake"))
        (target / "REPL/Main.lean").write_bytes(
            (R / "artifacts/lean-native-compilation-2026-10-14/REPL-Main.native.lean").read_bytes())
    upstream = STATE / "shred"
    alias(UPSTREAM, upstream)
    if not upstream.exists():
        run(["git", "init", str(upstream)])
        run(["git", "remote", "add", "origin", "https://github.com/memo-ozdincer/shred"], upstream)
        run(["git", "fetch", "--depth=1", "origin", REV], upstream)
        run(["git", "checkout", "--detach", "FETCH_HEAD"], upstream)
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=upstream, text=True).strip() == REV
    run(["python3", str(R / "bench/lean-native/linarith-oracle/build-prefix-repl.py")])
    return {"status": "built; real32-source matched qualification still required",
            "shred_revision": REV, "native_mathlib": str(MATH),
            "build_scope": "retained owning-Workspace cache; source unchanged, native build products added"}

if __name__ == "__main__":
    code = 1
    try:
        result = main()
        code = 0
    except BaseException:
        result = {"status": "failed, not a performance result", "error": traceback.format_exc()}
    result.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), commands=records)
    (STATE / "restore-prefix-terminal.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)
    raise SystemExit(code)
