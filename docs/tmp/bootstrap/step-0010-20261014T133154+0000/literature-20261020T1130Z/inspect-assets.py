"""Read pinned public workload metadata; lexical mentions are not dynamic costs."""
import collections
import csv
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
PIN = "8f5e8b36ab5fbdec6fd8d8f4ee0580d29647097a"
BASE = "https://raw.githubusercontent.com/utopia-group/VeriSoftBench/" + PIN + "/"
def read(name):
    with urllib.request.urlopen(BASE + name, timeout=30) as reply:
        return reply.read()
raw = read("data/verisoftbench.jsonl")
items = [json.loads(line) for line in raw.splitlines() if line.strip()]
repos = json.loads(read("repos.json"))["repos"]
token = re.compile(r"(?<![A-Za-z0-9_])bv_decide(?![A-Za-z0-9_])")
rows = []
for item in items:
    proof = item["ground_truth_proof"]
    root = item["lean_root"]
    rows.append(dict(id=item["id"], repository=root, path=item["rel_path"],
        toolchain=repos[root]["lean_toolchain"],
        proof_bv_decide_mentions=len(token.findall(proof)),
        complete_record_bv_decide_mentions=len(token.findall(json.dumps(item))),
        repository_commit=repos[root].get("commit"),
        import_count=len(item["imports"]), category=item["category"]))
with (OUT/"verisoftbench-task-metadata.csv").open("w") as target:
    writer=csv.DictWriter(target,fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
datasets={}
for label,relative in [
    ("original29750","artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl"),
    ("selected1000","artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl")]:
    count=0
    matched=[]
    with (ROOT/relative).open() as handle:
        for line in handle:
            if not line.strip():continue
            row=json.loads(line)
            count+=1
            if token.search(row["code"]):matched.append(row["proof_id"])
    datasets[label]=dict(source=relative,rows=count,explicit_token_source_ids=matched)
result=dict(scope="Root source-asset self-review only. Lexical mentions include comments/strings and do not establish execution, checked proofs, stage cost or GPU coverage. Ground-truth proofs are not generated candidate attempts.",
    source_pin=PIN,upstream_bytes=len(raw),tasks=len(rows),
    repositories=dict(collections.Counter(x["repository"] for x in rows)),
    task_toolchains=dict(collections.Counter(x["toolchain"] for x in rows)),
    ground_truth_token_task_ids=[x["id"] for x in rows if x["proof_bv_decide_mentions"]],
    complete_record_token_task_ids=[x["id"] for x in rows if x["complete_record_bv_decide_mentions"]],
    retained_datasets=datasets)
(OUT/"asset-analysis.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
