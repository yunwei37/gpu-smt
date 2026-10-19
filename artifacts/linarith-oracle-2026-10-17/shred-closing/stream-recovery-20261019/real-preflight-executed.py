from pathlib import Path
import asyncio,gzip,json,runpy,subprocess,time,sys,datetime
R=Path("/workspaces/repository")
SOURCE=R/"artifacts/linarith-oracle-2026-10-17/shred-closing"
OUT=SOURCE/"stream-recovery-20261019"
D=runpy.run_path(str(SOURCE/"run-kimina.py"))
D["args"].concurrency=2
rows=D["inputs"]("minif2f",full=True)
chosen=set(range(32));chosen.update(x["index"]for x in rows if x["code"]=="None")
selection=json.loads((OUT/"failure-source-selection.json").read_text())
chosen.update(int(x.split("-")[1])for x in selection["selected_HTTP_failure_IDs"]+[selection["stalled_source_ID"]])
picked=[x for x in rows if x["index"]in chosen]
assert len(picked)==len(chosen)
destination=OUT/"real-preflight";destination.mkdir(exist_ok=False)
(destination/"source-ids.json").write_text(json.dumps(["minif2f-"+str(x["index"])for x in picked])+"\n")
with gzip.open(destination/"original-sources.jsonl.gz","wt",compresslevel=1)as stream:
 for row in picked:stream.write(json.dumps(row,ensure_ascii=False)+"\n")
async def main():
 for method in["native","shred"]:
  started=time.monotonic_ns();prep=destination/(method+"-preparation");prep.mkdir()
  snippets=D["prepare"](picked,"minif2f",prep)if method=="shred"else[dict(proof_id="minif2f-"+str(x["index"]),code=x["code"])for x in picked]
  prep_seconds=(time.monotonic_ns()-started)/1e9
  directory=destination/("rep1-"+method)
  result=await D["capture"].cell(D["args"],"stock",directory,snippets,D["build"])
  result.update(condition=method,dataset="minif2f",input_preparation_seconds=prep_seconds,
    whole_with_input_preparation_seconds=(time.monotonic_ns()-started)/1e9,
    application_repairs="Declared kimina-transport-logging.patch; large-line framing and NullHighlighter, same native solver/48GiB/source width2.",
    scope="Real-source dependency repair qualification, not corpus performance or unchanged upstream application. Root self-review.")
  (directory/"terminal.json").write_text(json.dumps(result,indent=2)+"\n")
  if result["state"]!="complete":return 1
  assert result["returned"]==len(picked)and not result["owned_live_descendants_after_shutdown"]
 return 0
raise SystemExit(asyncio.run(main()))
