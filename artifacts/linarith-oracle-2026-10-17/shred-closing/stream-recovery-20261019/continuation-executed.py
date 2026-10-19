from pathlib import Path
import os,select,json,datetime,subprocess,gzip
R=Path("/workspaces/repository")
A=R/"artifacts/linarith-oracle-2026-10-17"
OUT=A/"shred-closing/stream-recovery-20261019"
PY="/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python"
def event(**values):
 print(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**values)),flush=True)
def run(name,command):
 event(event="start",name=name,command=command,application_repairs="kimina-transport-logging.patch")
 with(OUT/(name+".log")).open("wb")as stream:
  result=subprocess.run(command,cwd=R,stdout=stream,stderr=subprocess.STDOUT)
 event(event="exit",name=name,code=result.returncode)
 if result.returncode:raise SystemExit(result.returncode)

# Join the already-running recorded finite qualification without polling or
# restarting it. This is one finite experiment sequence, not an agent/scheduler.
launch=json.loads((OUT/"real-preflight-launch.json").read_text())
pid=launch["pid"]
try:
 fd=os.pidfd_open(pid)
except ProcessLookupError:
 fd=None
if fd is not None:
 try:
  command=Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
  assert str(OUT/"real-preflight-executed.py").encode() in command
  event(event="join_existing_qualification",pid=pid)
  select.select([fd],[],[])
 finally:os.close(fd)
root=OUT/"real-preflight"
for method in["native","shred"]:
 directory=root/("rep1-"+method)
 terminal=json.loads((directory/"terminal.json").read_text())
 assert terminal["state"]=="complete"
 assert terminal["expected"]==terminal["returned"]==54
 assert terminal["source_concurrency"]==2
 assert terminal["affinity"]==[4,5,6,7]
 assert terminal["memory_limit_bytes"]==51539607552
 assert not terminal["owned_live_descendants_after_shutdown"]
 events=[json.loads(x)for x in(directory/"http.jsonl").read_text().splitlines()]
 replies=[x for x in events if x["event"]=="response" and
   any(s.get("id")=="minif2f-2518"for s in json.loads(x.get("request","{}")).get("snippets",[]))]
 assert any(x.get("status")==200 for x in replies),"Previously stalled source must actually return"
 log=(directory/"server.log").read_text(errors="replace")
 assert "LimitOverrunError"not in log
 event(event="qualification_method_closed",method=method,returned=terminal["returned"],
       operational=terminal.get("operational"),source2518_statuses=[x.get("status")for x in replies])
 # Archive only after terminal retirement; no live stream is moved.
 receipt=[]
 for source in list(directory.iterdir()):
  if source.is_file()and source.suffix in[".jsonl",".log"]:
   raw=source.read_bytes();packed=gzip.compress(raw,compresslevel=1,mtime=0)
   assert gzip.decompress(packed)==raw
   dest=source.with_name(source.name+".gz");assert not dest.exists()
   dest.write_bytes(packed);assert gzip.decompress(dest.read_bytes())==raw
   receipt.append(dict(source=source.name,archive=dest.name,raw_bytes=len(raw),gzip_bytes=len(packed),byte_equal_roundtrip=True))
   source.unlink()
 (directory/"raw-archive.json").write_text(json.dumps(receipt,indent=2)+"\n")
event(event="real_qualification_closed",scope="Dependency-only; selected54 are not a corpus performance result.")
run("full-minif2f",[PY,"-u",str(A/"shred-closing/run-kimina.py"),"--datasets","minif2f","--concurrency","2","--out",str(OUT/"full-population"),"--full"])
REC=A/"workspace-interruption-20261019"
for name in["resume-current29750-after-repair.py","resume-formal49-after-repair.py","resume-older29750-after-repair.py"]:
 run(name.removesuffix(".py"),[PY,"-u",str(REC/name)])
event(event="finite_continuation_closed")
