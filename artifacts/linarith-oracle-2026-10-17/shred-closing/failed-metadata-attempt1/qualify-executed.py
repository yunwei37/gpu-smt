"""Run unchanged upstream SHRED paired CLI on the first original miniF2F block."""
from pathlib import Path
import collections
import gzip
import json
import os
import re
import resource
import sys
import time

R = Path("/workspaces/repository")
A = Path(__file__).resolve().parent
S = Path("/tmp/gpu-smt-primary-opportunities-20261017/shred")
D = Path("/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture")
M = D / "mathlib4"
SDK = D / "lean-4.9.0-rc1-linux"
receipt = json.loads((A / "build-receipt.json").read_text())
os.environ["PATH"] = str(SDK / "bin") + ":" + os.environ["PATH"]
os.environ["LEAN_PATH"] = receipt["lean_path"]
os.sched_setaffinity(0, {4, 5, 6, 7})
resource.setrlimit(resource.RLIMIT_AS, (51539607552, 51539607552))
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
sys.path.insert(0, str(S / "src"))

from lean_prefix.profile import C0_BASE_CONTEXT, c0_verifier_declaration
from lean_prefix import certificate_prevalence as official
from lean_prefix.cli import main as official_cli

P = R / "artifacts/linarith-oracle-2026-10-17/prefix-opportunity"
with gzip.open(P / "minif2f-input.jsonl.gz", "rt") as stream:
    items = [json.loads(next(stream)) for _ in range(32)]
assert [item["index"] for item in items] == list(range(32))
native = {}
with gzip.open(P / "native-units.jsonl.gz", "rt") as stream:
    for line in stream:
        row = json.loads(line)
        if row["proposalId"].startswith("minif2f-"):
            index = int(row["proposalId"].split("-")[1])
            if index < 32:
                native[index] = row
        if len(native) == 32:
            break
prepared = []
for item in items:
    match = re.search(r":=\s*by\b", item["code"])
    assert match and item["code"].startswith(item["header"])
    assert item["header"].startswith(C0_BASE_CONTEXT)
    assert not item["header"][len(C0_BASE_CONTEXT):].strip()
    statement = item["code"][len(C0_BASE_CONTEXT):match.end()]
    proof = item["code"][match.end():] + "\n" + chr(96) * 3
    # Reconstruct all original bytes, including the extra blank header line.
    assert C0_BASE_CONTEXT + c0_verifier_declaration(statement, proof) == item["code"]
    parsed = native[item["index"]]
    prepared.append(dict(stratum="first_original_block",
        proposal_id="minif2f-" + str(item["index"]), theorem_name="minif2f-original-block-0",
        candidate_index=item["index"], expected_correct=None,
        theorem_statement=statement, proof=proof, native_eligible=bool(parsed["eligible"]),
        native_error=parsed.get("error"), units=parsed.get("units") or []))
with gzip.open(A / "prepared-mini32.jsonl.gz", "wt", compresslevel=1) as stream:
    for row in prepared:
        stream.write(json.dumps(row, ensure_ascii=False) + "\n")

trace = gzip.open(A / "qualification-wire.jsonl.gz", "wt", compresslevel=1)
def record(event):
    trace.write(json.dumps(event, ensure_ascii=False) + "\n")
    trace.flush()

class RecordedRepl(official.LeanRepl):
    serial = 0
    def __init__(self, *args, **kwargs):
        self.trace_mode = "baseline" if RecordedRepl.serial == 0 else "cached"
        RecordedRepl.serial += 1
        super().__init__(*args, **kwargs)
    def request(self, payload):
        start = time.monotonic_ns()
        try:
            result = super().request(payload)
        except BaseException as error:
            record(dict(event="failure", mode=self.trace_mode, request=payload,
                start_ns=start, end_ns=time.monotonic_ns(), error=repr(error)))
            raise
        record(dict(event="response", mode=self.trace_mode, request=payload,
            start_ns=start, end_ns=time.monotonic_ns(), response=result.response,
            native_cpu_seconds=result.cpu_seconds, native_wall_seconds=result.wall_seconds))
        return result
    def close(self):
        super().close()
        record(dict(event="close", mode=self.trace_mode, end_ns=time.monotonic_ns()))

# Observe complete replies without changing upstream selection/cache/checking.
official.LeanRepl = RecordedRepl
arguments = ["run-certificate-prevalence-theorem",
    "--input-artifact", str(A / "prepared-mini32.jsonl.gz"),
    "--theorem", "minif2f-original-block-0",
    "--lean-workspace", str(M), "--artifact", str(A / "qualification-pairs.jsonl.gz"),
    "--output", str(A / "qualification-official-report.json"),
    "--repl-executable", "/tmp/gpu-smt-linarith-oracle-20261017/prefix/repl-kernel/.lake/build/bin/repl"]
(A / "qualification-arguments.json").write_text(json.dumps(arguments, indent=2) + "\n")
started = time.monotonic_ns()
try:
    exit_code = official_cli(arguments)
finally:
    trace.close()
(A / "qualification-exit.json").write_text(json.dumps(dict(
    exit_code=exit_code, whole_driver_seconds=(time.monotonic_ns()-started)/1e9,
    scope="First original32 functional qualification, not full workload/service throughput; unchanged official CLI/cache implementation plus charged wire observation.",
    affinity=sorted(os.sched_getaffinity(0)), memory_limit_bytes=51539607552)) + "\n")
raise SystemExit(exit_code)
