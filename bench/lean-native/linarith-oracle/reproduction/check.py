"""Check a Lean source with the built CPU oracle; retain all command output."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", type=Path, required=True)
    parser.add_argument("--log-dir", type=Path, required=True,
                        help="New directory for this verification's logs")
    parser.add_argument("source", type=Path,
                        help="Lean file importing GpuArithmetic.IntegerPowerOracle")
    args = parser.parse_args()
    build = args.build.resolve()
    source = args.source.resolve()
    logs = args.log_dir.resolve()
    logs.mkdir(parents=True, exist_ok=False)
    record = json.loads((build / "build.json").read_text())
    env = dict(os.environ)
    env.update(LEAN_PATH=record["lean_path"], LEAN_SRC_PATH=record["lean_src_path"])
    env["LD_LIBRARY_PATH"] = os.pathsep.join(
        record["library_paths"] + [env.get("LD_LIBRARY_PATH", "")])
    env.update(
        GPU_ARITHMETIC_BATCH="1",
        GPU_ARITHMETIC_ORACLE=str(build / "arithmetic-batchd"),
        FARKAS_NATIVE_BIN=str(build / "farkas-batchd"),
        FARKAS_EXTERNAL_CPU_HYBRID="1",
        GPU_ARITHMETIC_RACE_WORKER=str(build / "farkas-race-worker"),
        GPU_ARITHMETIC_RACE_MIN_ROWS="11",
        GPU_ARITHMETIC_NEGATIVE_CERTIFICATES="1",
        GPU_ARITHMETIC_STRONG_PROFILE="1",
        GPU_SMT_NATIVE_OMEGA_CONTROL="1",
        GPU_ARITHMETIC_RACE_LOG=str(logs / "lp-races.jsonl"),
    )
    # This public entrypoint selects the measured CPU provider explicitly.
    for key in ["GPU_ARITHMETIC_RACE_CPU_ONLY", "GPU_ARITHMETIC_STRONG_CPU_SOCKET"]:
        env.pop(key, None)
    with tempfile.TemporaryDirectory(prefix="lean-oracle-") as socket_dir:
        address = str(Path(socket_dir) / "support.sock")
        env["GPU_ARITHMETIC_SUPPORT_SOCKET"] = address
        command = [sys.executable, str(ROOT / "support-proxy.py"),
                   "--backend", "highs", "--negative-certificates",
                   "--socket", address, "--log", str(logs / "support-calls.jsonl")]
        with (logs / "support-stderr.log").open("w") as errors:
            proxy = subprocess.Popen(command, env=env, stdout=subprocess.PIPE,
                                     stderr=errors, text=True)
            try:
                ready = proxy.stdout.readline()
                (logs / "support-start.json").write_text(ready)
                if not ready or not json.loads(ready).get("ready"):
                    raise RuntimeError("CPU support startup failed; see logs")
                lean = Path(record["sdk"]) / "bin/lean"
                command = [str(lean), *["--load-dynlib=" + s for s in record["libraries"]],
                           "--json", str(source)]
                with (logs / "lean.jsonl").open("w") as output:
                    status = subprocess.run(command, env=env, stdout=output,
                                            stderr=subprocess.STDOUT).returncode
                (logs / "result.json").write_text(json.dumps({
                    "returncode": status, "source": str(source), "command": command,
                    "provider": "CPU HiGHS", "scope": "Functional verification, not a timing benchmark"
                }, indent=2) + "\n")
                return status
            finally:
                if proxy.poll() is None:
                    proxy.terminate()
                proxy.wait()


if __name__ == "__main__":
    raise SystemExit(main())
