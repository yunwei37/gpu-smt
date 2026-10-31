#!/usr/bin/env python3
"""Version-matched stock leanchecker; repaired realpath-contained artifact tree."""
import os,time,sys,json,subprocess,signal,select,resource
from pathlib import Path
R=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3')
SDK=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.34.1-linux')
meta=json.loads((R/'preparation.json').read_text())
env=os.environ.copy();env['PATH']=str(SDK/'bin')+':'+env['PATH']
env['LEAN_SYSROOT']=str(SDK);env['LEAN_PATH']=meta['lean_path'];env['LEAN_NUM_THREADS']='8'
targets=json.loads((R/'targets.json').read_text())
active_group=None
def abort(signum,frame):
 if active_group is not None:
  try:os.killpg(active_group,signal.SIGKILL)
  except ProcessLookupError:pass
 raise SystemExit(128+signum)
signal.signal(signal.SIGTERM,abort)
signal.signal(signal.SIGINT,abort)
start=time.monotonic()
deadline=start+1700
def tree(pid):
 found=set();todo=[pid]
 while todo:
  pp=todo.pop()
  if pp in found:continue
  found.add(pp)
  try:
   for task in Path('/proc',str(pp),'task').iterdir():
    try:todo.extend(int(x)for x in(task/'children').read_text().split())
    except OSError:pass
  except OSError:pass
 return found
def rss(pid):
 try:return int(Path('/proc',str(pid),'statm').read_text().split()[1])*os.sysconf('SC_PAGE_SIZE')
 except (OSError,ValueError,IndexError):return 0
def run(key,module,fresh=False,limit=60,kind='target'):
 global active_group
 limit=min(limit,max(.1,deadline-time.monotonic()))
 cmd=[str(SDK/'bin/leanchecker'),'-v']+(['--fresh']if fresh else[])+[module]
 before=time.monotonic();observer=time.process_time();maxrss=0;samples=[];stop=None;kill_at=None
 with(R/(key+'.stdout')).open('w')as fo,(R/(key+'.stderr')).open('w')as fe:
  p=subprocess.Popen(cmd,cwd=R,env=env,stdout=fo,stderr=fe,start_new_session=True)
  active_group=p.pid
  fd=os.pidfd_open(p.pid)
  birth=Path('/proc',str(p.pid),'stat').read_text().rsplit(')',1)[1].split()[19]
  while True:
   pid,status,u=os.wait4(p.pid,os.WNOHANG)
   if pid:break
   current=sum(rss(x)for x in tree(p.pid));maxrss=max(maxrss,current)
   samples.append(dict(seconds=time.monotonic()-before,tree_rss_bytes=current))
   # Reserve 128 MiB for this small independent parent/driver within O's 12 GiB.
   if current>(12*1024**3-128*1024**2):stop=stop or 'rss_budget'
   if time.monotonic()-before>limit:stop=stop or 'wall_budget'
   if stop and kill_at is None:
    try:os.killpg(p.pid,signal.SIGTERM)
    except ProcessLookupError:pass
    kill_at=time.monotonic()
   elif kill_at is not None and time.monotonic()-kill_at>3:
    try:os.killpg(p.pid,signal.SIGKILL)
    except ProcessLookupError:pass
   select.select([fd],[],[],.1)
  os.close(fd);rc=os.waitstatus_to_exitcode(status);active_group=None
 wall=time.monotonic()-before
 stdout=(R/(key+'.stdout')).read_text(errors='replace');stderr=(R/(key+'.stderr')).read_text(errors='replace')
 wanted='replaying '+module+(' with --fresh'if fresh else'')
 reached=wanted in stdout.splitlines()
 row=dict(key=key,module=module,kind=kind,fresh=fresh,args=cmd,wall_s=wall,user_s=u.ru_utime,system_s=u.ru_stime,peak_rss_kib=u.ru_maxrss,
 sampled_tree_rss_max_bytes=maxrss,minor_faults=u.ru_minflt,major_faults=u.ru_majflt,returncode=rc,stop=stop,
 target_replay_announced=reached,success=rc==0 and stop is None and reached,observer_cpu_self_s=time.process_time()-observer,
 pid=p.pid,birth_ticks=birth,limit_s=limit,affinity=sorted(os.sched_getaffinity(0)),sample_interval_s=.1)
 (R/(key+'.rss.json')).write_text(json.dumps(samples))
 with(R/'results.jsonl').open('a')as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(row),flush=True)
 return row
def main():
 assert sorted(os.sched_getaffinity(0))==list(range(8))
 (R/'launch.json').write_text(json.dumps(dict(pid=os.getpid(),utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),locks_at_acquisition=Path('/proc/locks').read_text(),memory_budget_gib=12,own_parent_reserve_mib=128,phase_limit_s=1700,env_lean_sysroot=env['LEAN_SYSROOT'],lean_path=env['LEAN_PATH']),indent=2))
 (R/'version.txt').write_text(subprocess.check_output([str(SDK/'bin/lean'),'--version'],env=env,text=True))
 p=run('preflight',targets[0]['module'],limit=60,kind='preflight')
 if not p['success']:
  (R/'terminal.json').write_text(json.dumps(dict(status='preflight_failed',rows=1)))
  return 2
 (R/'preflight-terminal.json').write_text(json.dumps(dict(status='success',module=p['module'],returncode=0)))
 for i,t in enumerate(targets):
  if time.monotonic()>deadline-5:break
  limit=720 if t['module'].endswith('.Grid') else 360 if t['module'].endswith('.Amplitudes') else 60
  run(f'target-{i:02d}',t['module'],limit=limit)
 # Scope controls, including success-sized whole-closure samples.
 for i,module in enumerate(['Init.Data.Nat.Basic','Mathlib.Data.Nat.Basic',targets[0]['module']]):
  for fresh in [False,True]:
   if module==targets[0]['module'] and not fresh:continue
   if time.monotonic()>deadline-5:break
   run(f'scope-{i}-{int(fresh)}',module,fresh=fresh,limit=180,kind='scope')
 rows=[json.loads(x)for x in(R/'results.jsonl').read_text().splitlines()]
 (R/'terminal.json').write_text(json.dumps(dict(status='finished_bounded_matrix',rows=len(rows),target_rows=sum(x['kind']=='target'for x in rows),
 target_success=sum(x['kind']=='target'and x['success']for x in rows),scope_rows=sum(x['kind']=='scope'for x in rows),elapsed_s=time.monotonic()-start),indent=2))
 return 0
if __name__=='__main__':raise SystemExit(main())
