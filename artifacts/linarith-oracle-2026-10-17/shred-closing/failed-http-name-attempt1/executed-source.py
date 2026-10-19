"""Matched native/SHRED replay through the existing official Kimina HTTP boundary."""
from pathlib import Path
import asyncio
import gzip
import importlib.util
import json
import os
import re
import resource
import subprocess
import sys
import time
from types import SimpleNamespace

R = Path("/workspaces/repository")
A = Path(__file__).resolve().parent
S = Path("/tmp/gpu-smt-primary-opportunities-20261017/shred")
D = Path("/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture")
K = Path("/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d")
U = Path("/workspaces/.agent-state/gpu-smt-deps/shred-closing-20261018")
M = D / "mathlib4"
SDK = D / "lean-4.9.0-rc1-linux"
sys.path[:0] = [str(S/"src"), str(K), str(K/"client")]
from lean_prefix.certificate_prevalence import wrap_final_tactic, CACHE_EXCLUDED_SYNTAX

os.sched_setaffinity(0, {4,5,6,7})
resource.setrlimit(resource.RLIMIT_AS, (51539607552,51539607552))
resource.setrlimit(resource.RLIMIT_CORE, (0,0))
receipt = json.loads((A/"build-receipt.json").read_text())
N = Path(json.loads((R/"artifacts/linarith-oracle-2026-10-17/formal-oracle-4.9/build-receipt.json").read_text())["library"])
build = dict(sdk=str(SDK), mathlib=str(M), lean_path=receipt["lean_path"],
    lean_src_path=":".join([str(S/"lean"), str(M)] + [str(p) for p in (M/".lake/packages").iterdir() if p.is_dir()]),
    library_paths=[str(N)] + [str(p/".lake/build/lib") for p in (N.parents[2]/".lake/packages").iterdir() if p.is_dir()],
    native_library=str(N/"libMathlib-Tactic-Linarith-1.so"))
assert Path(build["native_library"]).is_file()
(A/"http-build-receipt.json").write_text(json.dumps(build,indent=2)+"\n")
os.environ["PATH"] = str(SDK/"bin")+":"+os.environ["PATH"]
os.environ["LEAN_PATH"] = receipt["lean_path"]
spec = importlib.util.spec_from_file_location("official_http_capture", R/"bench/lean-native/linarith-oracle/kimina-http.py")
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)
args = SimpleNamespace(kimina=K, build=U,
    repl=Path("/tmp/gpu-smt-linarith-oracle-20261017/prefix/repl-kernel/.lake/build/bin/repl"),
    reference=R/"artifacts/lean-modern-native-compilation-2026-10-14/farkas-external-support")

def inputs(dataset):
    with gzip.open(R/f"artifacts/linarith-oracle-2026-10-17/prefix-opportunity/{dataset}-input.jsonl.gz","rt") as stream:
        rows = [json.loads(line) for line in stream]
    # First original32 plus every literal unavailable-source placeholder.
    return [row for row in rows if row["index"] < 32 or row["code"] == "None"]

def prepare(rows, dataset, out):
    requests = []
    mapped = {}
    for row in rows:
        match = re.search(r":=\s*by\b", row["code"])
        if match and row["code"].startswith(row["header"]):
            proof = row["code"][match.end():]
            mapped[str(row["index"])] = (match, proof)
            requests.append(json.dumps(dict(proposalId=str(row["index"]),proof=proof),ensure_ascii=False))
    command = [str(SDK/"bin/lake"), "env", "lean", "--run", str(S/"lean/LeanPrefix/Extract.lean")]
    result = subprocess.run(command,cwd=M,input="\n".join(requests)+"\n",
        capture_output=True,text=True)
    (out/"parser.stderr").write_text(result.stderr)
    with gzip.open(out/"parser.jsonl.gz","wt",compresslevel=1) as stream:
        stream.write(result.stdout)
    assert result.returncode == 0, "Retain parser failure before performance promotion"
    parsed = {row["proposalId"]:row for row in (json.loads(line) for line in result.stdout.splitlines())}
    assert set(parsed) == set(mapped)
    snippets = []
    counters = dict(sources=len(rows),wrapped=0,native_fallback=0,placeholder_sources=0)
    for row in rows:
        code = row["code"]
        item = parsed.get(str(row["index"]))
        if item and item.get("eligible") and item.get("units"):
            last = item["units"][-1]
            if last.get("syntaxKind") not in CACHE_EXCLUDED_SYNTAX:
                match, proof = mapped[str(row["index"])]
                try:
                    replacement = wrap_final_tactic(proof,item["units"])
                except Exception:
                    replacement = None
                if replacement is not None:
                    code = code[:match.end()] + replacement
                    counters["wrapped"] += 1
        if code.startswith(row["header"]):
            assert "import Mathlib\n" in row["header"]
            code = code.replace("import Mathlib\n","import Mathlib\nimport LeanPrefix.AutomaticCertificate\n",1)
        else:
            counters["placeholder_sources"] += 1
        snippets.append(dict(proof_id=dataset+"-"+str(row["index"]),code=code))
    counters["native_fallback"] = len(rows)-counters["wrapped"]
    (out/"preparation.json").write_text(json.dumps(counters,indent=2)+"\n")
    return snippets

async def main():
    root = A/"http-preflight"
    root.mkdir(exist_ok=False)
    for dataset in ("minif2f","proofnet"):
        for method in ("native","shred"):
            outer = time.monotonic_ns()
            rows = inputs(dataset)
            prep = root/dataset/(method+"-preparation")
            prep.mkdir(parents=True,exist_ok=False)
            snippets = prepare(rows,dataset,prep) if method == "shred" else [dict(proof_id=dataset+"-"+str(row["index"]),code=row["code"]) for row in rows]
            prep_seconds = (time.monotonic_ns()-outer)/1e9
            out = root/dataset/("rep1-"+method)
            result = await capture.cell(args,"stock",out,snippets,build)
            result.update(condition=method,dataset=dataset,input_preparation_seconds=prep_seconds,
                whole_with_input_preparation_seconds=(time.monotonic_ns()-outer)/1e9,
                scope="Existing SHRED module/last-tactic wrapper integrated with official Kimina HTTP; all real parser/preparation costs charged. Root self-review, not a new cache/system or full-workload result.")
            (out/"terminal.json").write_text(json.dumps(result,indent=2)+"\n")
            if result["state"] != "complete":
                return 1
    return 0

raise SystemExit(asyncio.run(main()))
