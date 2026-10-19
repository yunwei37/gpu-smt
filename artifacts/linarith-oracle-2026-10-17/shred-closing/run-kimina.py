"""Matched native/SHRED replay through the existing official Kimina HTTP boundary."""
from pathlib import Path
import argparse
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
SOURCE = Path(__file__).resolve().parent
A = SOURCE
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
receipt = json.loads((SOURCE/"build-receipt.json").read_text())
N = Path(json.loads((R/"artifacts/linarith-oracle-2026-10-17/formal-oracle-4.9/build-receipt.json").read_text())["library"])
build = dict(sdk=str(SDK), mathlib=str(M), lean_path=receipt["lean_path"],
    lean_src_path=":".join([str(S/"lean"), str(M)] + [str(p) for p in (M/".lake/packages").iterdir() if p.is_dir()]),
    library_paths=[str(N)] + [str(p/".lake/build/lib") for p in (N.parents[2]/".lake/packages").iterdir() if p.is_dir()],
    native_library=str(N/"libMathlib-Tactic-Linarith-1.so"))
assert Path(build["native_library"]).is_file()
os.environ["PATH"] = str(SDK/"bin")+":"+os.environ["PATH"]
os.environ["LEAN_PATH"] = receipt["lean_path"]
spec = importlib.util.spec_from_file_location("official_http_capture", R/"bench/lean-native/linarith-oracle/kimina-http.py")
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)
args = SimpleNamespace(kimina=K, build=U,
    repl=Path("/tmp/gpu-smt-linarith-oracle-20261017/prefix/repl-kernel/.lake/build/bin/repl"),
    reference=R/"artifacts/lean-modern-native-compilation-2026-10-14/farkas-external-support")

def inputs(dataset, full=False):
    with gzip.open(R/f"artifacts/linarith-oracle-2026-10-17/prefix-opportunity/{dataset}-input.jsonl.gz","rt") as stream:
        rows = [json.loads(line) for line in stream]
    if full:
        assert [row["index"] for row in rows] == list(range(len(rows)))
        assert len(rows) == (7808 if dataset == "minif2f" else 5952)
        return rows
    # Qualification includes real accepted cases without selecting by speed.
    selected = set(range(32))
    if dataset == "proofnet":
        control = R/"artifacts/linarith-oracle-2026-10-17/formal-oracle-4.9/full-populations/proofnet/stock"
        assert json.loads((control/"terminal.json").read_text())["state"] == "complete"
        with gzip.open(control/"results.jsonl.gz", "rt") as stream:
            positive = next(row for row in (json.loads(line) for line in stream) if row["outcome"] == "complete")
        start = positive["index"] // 32 * 32
        selected.update(range(start, start+32))
    return [row for row in rows if row["index"] in selected or row["code"] == "None"]

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
    counters = dict(sources=len(rows),wrapped=0,native_fallback=0,placeholder_sources=0,source_header_mismatches=0)
    fallbacks = []
    for row in rows:
        code = row["code"]
        item = parsed.get(str(row["index"]))
        reason = "no_top_level_by_or_source_header_mismatch" if item is None else "native_parser_ineligible"
        if item and item.get("eligible") and item.get("units"):
            last = item["units"][-1]
            if last.get("syntaxKind") not in CACHE_EXCLUDED_SYNTAX:
                match, proof = mapped[str(row["index"])]
                try:
                    replacement = wrap_final_tactic(proof,item["units"])
                except Exception as error:
                    replacement = None
                    reason = "upstream_wrap_exception: " + repr(error)
                if replacement is not None:
                    code = code[:match.end()] + replacement
                    counters["wrapped"] += 1
                    reason = None
            else:
                reason = "upstream_registered_syntax_exclusion"
        if reason is not None:
            fallbacks.append(dict(proof_id=dataset+"-"+str(row["index"]), reason=reason,
                native_error=item.get("error") if item else None))
        if row["code"] == "None":
            counters["placeholder_sources"] += 1
        if code.startswith(row["header"]):
            assert "import Mathlib\n" in row["header"]
            code = code.replace("import Mathlib\n","import Mathlib\nimport LeanPrefix.AutomaticCertificate\n",1)
        else:
            counters["source_header_mismatches"] += 1
        snippets.append(dict(proof_id=dataset+"-"+str(row["index"]),code=code))
    counters["native_fallback"] = len(rows)-counters["wrapped"]
    (out/"preparation.json").write_text(json.dumps(counters,indent=2)+"\n")
    (out/"fallbacks.json").write_text(json.dumps(fallbacks,indent=2)+"\n")
    return snippets

def archive_closed(directory):
    receipt = []
    for path in list(directory.iterdir()):
        if not path.is_file() or path.suffix not in (".jsonl", ".log"):
            continue
        raw = path.read_bytes()
        archive = path.with_name(path.name+".gz")
        assert not archive.exists()
        packed = gzip.compress(raw, compresslevel=1, mtime=0)
        assert gzip.decompress(packed) == raw
        archive.write_bytes(packed)
        assert gzip.decompress(archive.read_bytes()) == raw
        receipt.append(dict(source=path.name, archive=archive.name,
            raw_bytes=len(raw), archive_bytes=len(packed), byte_equal_roundtrip=True))
        path.unlink()
    (directory/"raw-archive.json").write_text(json.dumps(dict(
        scope="Lossless archival only after complete measured lifecycle; active files untouched. Export cost is separate from verification clocks.", files=receipt),indent=2)+"\n")

async def main(datasets, full=False):
    (A/"http-build-receipt.json").write_text(json.dumps(build,indent=2)+"\n")
    root = A/("http-full" if full else "http-preflight")
    root.mkdir(exist_ok=False)
    for dataset in datasets:
        for method in ("native","shred"):
            outer = time.monotonic_ns()
            rows = inputs(dataset, full=full)
            prep = root/dataset/(method+"-preparation")
            prep.mkdir(parents=True,exist_ok=False)
            snippets = prepare(rows,dataset,prep) if method == "shred" else [dict(proof_id=dataset+"-"+str(row["index"]),code=row["code"]) for row in rows]
            prep_seconds = (time.monotonic_ns()-outer)/1e9
            (root/dataset/"source-ids.json").write_text(json.dumps([item["proof_id"] for item in snippets])+"\n")
            out = root/dataset/("rep1-"+method)
            result = await capture.cell(args,"stock",out,snippets,build)
            result.update(condition=method,dataset=dataset,input_preparation_seconds=prep_seconds,
                whole_with_input_preparation_seconds=(time.monotonic_ns()-outer)/1e9,
                full_original_population=full,
                scope="Existing SHRED module/wrapper integrated with official Kimina HTTP; real parser/preparation costs charged. One fixed-order shared-host block, native verification comparison only; env/message differences exposed. Root self-review, not a new cache/system.")
            (out/"terminal.json").write_text(json.dumps(result,indent=2)+"\n")
            if result["state"] != "complete":
                return 1
            assert not result["owned_live_descendants_after_shutdown"]
            archive_closed(out)
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--datasets", nargs="+", choices=["minif2f","proofnet"], default=["minif2f","proofnet"])
    parser.add_argument("--full", action="store_true", help="Both methods process every original source without qualification selection")
    parser.add_argument("--concurrency", type=int, default=8, help="Same source concurrency for both methods; default retains earlier captures")
    options = parser.parse_args()
    args.concurrency = options.concurrency
    A = options.out
    A.mkdir(parents=True, exist_ok=False)
    raise SystemExit(asyncio.run(main(options.datasets, full=options.full)))
