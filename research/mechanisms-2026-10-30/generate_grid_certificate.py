"""Batch scan and emit the untrusted grid payload; generated artifacts stay on PVC."""
from pathlib import Path
import json, re, subprocess, time
HERE = Path(__file__).resolve().parent
def generate(output: Path):
    import run_finite
    output = run_finite.persistent_capture_path(output)
    output.mkdir(parents=True, exist_ok=False)
    binary = output / "compute-reference"
    generation_began = time.monotonic()
    began = time.monotonic()
    command = ["cc", "-O3", "-std=c11", str(HERE / "compute_reference.c"), "-o", str(binary)]
    compile_result = subprocess.run(command, capture_output=True, text=True)
    (output / "compile.stdout").write_text(compile_result.stdout)
    (output / "compile.stderr").write_text(compile_result.stderr)
    compile_result.check_returncode()
    compile_s = time.monotonic() - began
    began = time.monotonic()
    result = subprocess.run([str(binary)], capture_output=True, text=True)
    wall_s = time.monotonic() - began
    (output / "numeric.stdout").write_text(result.stdout)
    (output / "numeric.stderr").write_text(result.stderr)
    result.check_returncode()
    pairs = [(int(m), int(n)) for m,n in re.findall(r"solution=(\d+),(\d+)", result.stdout)]
    payload = "[" + ", ".join(f"({m}, {n})" for m,n in pairs) + "]"
    source = (HERE / "ReflectedGridCertificate.lean").read_text()
    source, count = re.subn(r"def certificate : List \(Nat × Nat\) := .*", "def certificate : List (Nat × Nat) := " + payload, source)
    assert count == 1
    (output / "ReflectedGridCertificate.lean").write_text(source)
    record = {"generation_wall_s_before_receipt": time.monotonic()-generation_began, "compile_argv": command, "compile_wall_s": compile_s, "scan_process_wall_s": wall_s,
              "solution_pairs": pairs, "source": str(output / "ReflectedGridCertificate.lean"),
              "trust": "untrusted numeric proposals; Lean checks completeness and soundness"}
    (output / "generation.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record), flush=True)
    return record
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(); p.add_argument("output", type=Path)
    generate(p.parse_args().output)
