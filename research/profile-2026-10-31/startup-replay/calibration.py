#!/usr/bin/env python3
# Same retained measurement routine, faster own-descendant discovery.
import importlib.util,fcntl,os,json,time
from pathlib import Path
root=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay')
spec=importlib.util.spec_from_file_location('measurement',root/'v2/measure.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.RAW=root/'calibration';m.ROOT=m.RAW/'sources/lean';m.ROOT.mkdir(parents=True,exist_ok=True)
ordered=sorted(m.small,key=lambda r:r['wall_s']);m.small=[ordered[0],ordered[len(ordered)//2],ordered[-1]]
def own_tree(pid):
 found=set();pending=[pid]
 while pending:
  pp=pending.pop()
  if pp in found:continue
  found.add(pp)
  try:
   for task in Path('/proc',str(pp),'task').iterdir():
    try:pending.extend(int(x)for x in(task/'children').read_text().split())
    except OSError:pass
  except OSError:pass
 return found
m.tree=own_tree
original=m.measure
def timed_observer(key,*args,**kwargs):
 start=time.process_time();r=original(key,*args,**kwargs)
 with(m.RAW/'observer.jsonl').open('a')as f:
  f.write(json.dumps(dict(key=key,observer_cpu_self_s=time.process_time()-start))+'\n')
 return r
m.measure=timed_observer
with open(m.BASE/'pcore.lock','a')as lock:
 print('waiting shared P-core lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX)
 os.sched_setaffinity(0,set(range(8)))
 m.done=set()
 m.startup()
 (m.RAW/'startup-terminal.json').write_text(json.dumps(dict(status='completed')))
