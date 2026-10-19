"""Finite requested24-source qualification then one fresh full miniF2F pair."""
from pathlib import Path
import asyncio,json,os,runpy,gzip,datetime
R=Path("/workspaces/repository")
A=R/"artifacts/linarith-oracle-2026-10-17"
O=A/"shred-closing/aggregate-budget-20261019"
os.environ["GPU_SMT_MEMORY_ROOT_PID"]=str(os.getpid())
D=runpy.run_path(str(A/"shred-closing/run-kimina.py"))
D["args"].concurrency=2
D["args"].per_repl_gib=24
D["args"].total_memory_gib=48
rows=D["inputs"]("minif2f",full=True)
selected=set(range(20))|{579,663,664,2518}
picked=[x for x in rows if x["index"]in selected]
assert len(picked)==24
Q=O/"qualification24";Q.mkdir(exist_ok=False)
(Q/"source-ids.json").write_text(json.dumps(["minif2f-"+str(x["index"])for x in picked])+"\n")
with gzip.open(Q/"original-sources.jsonl.gz","wt",compresslevel=1)as stream:
 for item in picked:stream.write(json.dumps(item,ensure_ascii=False)+"\n")
def event(**values):
 print(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**values)),flush=True)
async def measure(method,values,directory,injection=False):
 prep=directory.with_name(directory.name+"-preparation");prep.mkdir()
 import time
 started=time.monotonic_ns()
 snippets=D["prepare"](values,"minif2f",prep)if method=="shred"else[dict(proof_id="minif2f-"+str(x["index"]),code=x["code"])for x in values]
 prep_seconds=(time.monotonic_ns()-started)/1e9
 D["args"].skip_warm=injection
 D["args"].watchdog_test_threshold_bytes=64*1024**2 if injection else 0
 terminal=await D["capture"].cell(D["args"],"stock",directory,snippets,D["build"])
 terminal.update(condition=method,input_preparation_seconds=prep_seconds,
  whole_with_input_preparation_seconds=(time.monotonic_ns()-started)/1e9,
  application_repairs="Declared transport/logging plus kimina-aggregate-budget.patch; real live-worker semaphore, resource attribution and idempotent retirement.",
  fault_injection=injection,
  scope="Requested aggregate48GiB experiment point; source2/live2/native24GiB; root self-review. Injected failures are never performance evidence.")
 (directory/"terminal.json").write_text(json.dumps(terminal,indent=2)+"\n")
 assert terminal["state"]=="complete"and terminal["returned"]==len(values)
 assert not terminal["owned_live_descendants_after_shutdown"]
 summary=terminal["memory_watchdog"]
 assert summary["error"]is None and summary["samples"]>0
 assert summary["peak_sampled_native_repl_count"]<=2
 assert summary["budget_bytes"]==48*1024**3
 assert terminal["per_native_repl_address_limit_bytes"]==24*1024**3
 assert summary["peak_sampled_owned_rss_bytes"]<48*1024**3
 samples=[json.loads(x)for x in(directory/"memory-rss.jsonl").read_text().splitlines()]
 native_limits=[line for sample in samples for p in sample["processes"]if p["native_repl"]for line in p.get("address_limit",[])]
 assert native_limits and all(str(24*1024**3)in line for line in native_limits)
 if injection:
  kills=[x["kill"]for x in samples if "kill"in x]
  assert kills and all(x["source_id"]in[snippet["proof_id"]for snippet in snippets]for x in kills)
  for sample in samples:
   if "kill"in sample:
    assert sample["kill"]["victim_rss_bytes"]==max(p["rss"]for p in sample["processes"]if p["native_repl"])
  assert terminal["counts"].get("resource_failure",0)>0
  assert all(x["total_rss_bytes"]>64*1024**2 for x in kills)
 else:
  assert summary["effective_threshold_bytes"]==48*1024**3
 event(event="cell_qualified",method=method,injection=injection,counts=terminal["counts"],watchdog=summary)
 D["archive_closed"](directory)
 return terminal
async def main():
 # Test the actual independent guard kill/attribution before normal acquisition.
 await measure("native",picked[:2],Q/"fault-injection-real2",True)
 for method in["native","shred"]:
  await measure(method,picked,Q/("rep1-"+method))
 event(event="real24_qualification_closed",scope="Dependency only, separate fault injection; all resource failures preserved.")
 D["args"].skip_warm=False
 D["args"].watchdog_test_threshold_bytes=0
 D["main"].__globals__["A"]=O/"full-population"
 D["main"].__globals__["A"].mkdir(exist_ok=False)
 result=await D["main"](["minif2f"],full=True)
 event(event="full_minif2f_exit",code=result)
 return result
raise SystemExit(asyncio.run(main()))
