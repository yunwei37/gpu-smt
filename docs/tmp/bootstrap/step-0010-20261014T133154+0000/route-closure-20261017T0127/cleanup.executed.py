from pathlib import Path
import json,gzip,shutil,datetime,os
n=Path(__file__).resolve().parent
state=Path('/workspaces/.agent-state')
before=json.loads((n/'before-stop.json').read_text())
paths=sorted({x['path'] for x in before['fd_outputs'] if x['bytes']>1000000000})
# Project OMP stdout only. Session state and benchmark outputs are excluded.
assert len(paths)==4
open_handles=[]
for d in Path('/proc').iterdir():
 if not d.name.isdecimal():continue
 try:
  for fd in (d/'fd').iterdir():
   try:
    if os.readlink(fd) in paths:open_handles.append(str(fd))
   except OSError:pass
 except OSError:pass
assert not open_handles,open_handles
out=state/'gpu-smt-omp-retired-20261017'
out.mkdir(exist_ok=True)
rows=[];free0=shutil.disk_usage(state).free
for value in paths:
 p=Path(value)
 assert p.resolve().is_relative_to(Path('/tmp')) or p.resolve().is_relative_to(state)
 st=p.stat();target=out/(p.name+'.gz')
 assert not target.exists()
 with p.open('rb') as src,gzip.open(target,'wb',compresslevel=1) as dst:
  shutil.copyfileobj(src,dst,8*1024*1024)
 # Read the whole gzip to its CRC-checked EOF; retain source if this fails.
 length=0
 with gzip.open(target,'rb') as z:
  while chunk:=z.read(8*1024*1024):length+=len(chunk)
 assert length==st.st_size and p.stat().st_size==st.st_size and p.stat().st_mtime_ns==st.st_mtime_ns
 with p.open('rb') as f:
  (out/(p.name+'.head.bin')).write_bytes(f.read(65536))
  f.seek(max(0,st.st_size-65536));(out/(p.name+'.tail.bin')).write_bytes(f.read())
 compressed=target.stat().st_size
 p.unlink()
 rows.append({'original':str(p),'original_bytes':st.st_size,'archive':str(target),'archive_bytes':compressed,'gzip_crc_eof_verified':True,'original_removed':True})
 (n/'cleanup-receipt.json').write_text(json.dumps({'rows':rows,'state_directory_preserved':str(state/'omp'),'free_before':free0,'free_after_current':shutil.disk_usage(state).free,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
 print('RECLAIMED',p.name,st.st_size-compressed,flush=True)
print('COMPLETE',sum(x['original_bytes']-x['archive_bytes'] for x in rows),flush=True)
