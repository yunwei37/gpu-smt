from pathlib import Path
import json,time,psutil,os
root=psutil.Process(283334);birth=root.create_time()
rows=[];start=time.monotonic();initial={}
for tick in range(16):
 now=time.monotonic();procs=root.children(recursive=True)
 entries=[]
 for p in procs:
  try:
   cmd=p.cmdline()
   if not cmd or Path(cmd[0]).name!='repl':continue
   times=p.cpu_times();cpu=times.user+times.system
   key=(p.pid,p.create_time());prev=initial.get(key)
   entries.append(dict(pid=p.pid,birth=key[1],rss=p.memory_info().rss,threads=p.num_threads(),affinity=p.cpu_affinity(),cpu_seconds=cpu,
    interval_cores=None if prev is None else (cpu-prev[0])/(now-prev[1])))
   initial[key]=(cpu,now)
  except psutil.NoSuchProcess:pass
 rows.append(dict(elapsed=now-start,repls=entries))
 time.sleep(1 if tick<15 else 0)
assert psutil.Process(root.pid).create_time()==birth
out=Path('/workspaces/repository/artifacts/engine-resource-profile-2026-10-25/observed-repl-cpu.json')
out.write_text(json.dumps(dict(root_pid=root.pid,root_birth=birth,scope='Existing legacy native capture, live interval CPU/RSS; no extra proof run or setting change',samples=rows),indent=2)+'\n')
