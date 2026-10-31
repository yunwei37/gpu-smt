"""Bounded process-scoped perf experiments; all raw output remains on the PVC."""
from pathlib import Path
import os,sys,json,time,signal,subprocess,fcntl,argparse,resource,filecmp
BASE=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime')
LOCK=Path('/workspaces/.agent-state/gpu-smt-captures/pcore.lock')
EVENTS=','.join(f'cpu_core/{event}/{mode}' for event in ['cycles','instructions','cache-misses','LLC-load-misses','dTLB-load-misses'] for mode in ['u','k'])+',page-faults,context-switches,cpu-migrations'
def proc_tree(root):
    found={root};rows=[]
    procs={}
    for p in Path('/proc').iterdir():
        if not p.name.isdigit():continue
        try:
            fields=(p/'stat').read_text().rsplit(')',1)[1].split()
            procs[int(p.name)]=(int(fields[1]),int(fields[21])*os.sysconf('SC_PAGE_SIZE'),fields[19])
        except (OSError,ValueError,IndexError):pass
    for _ in range(12):
        add={pid for pid,(parent,rss,birth) in procs.items() if parent in found}
        if add<=found:break
        found|=add
    return [{'pid':p,'parent':procs[p][0],'rss':procs[p][1],'birth':procs[p][2]} for p in found if p in procs]
def native(spec):
    s=json.loads(Path(spec).read_text())
    assert os.sched_getaffinity(0)==set(range(8)), 'native helper must retain locked P-core affinity'
    def arm():
        signal.signal(signal.SIGALRM,signal.SIG_DFL)
        signal.setitimer(signal.ITIMER_REAL,s['wall_limit_s'])
        Path(s['native_cgroup'],'cgroup.procs').write_text(str(os.getpid()))
    started=time.monotonic()
    with Path(s['native_log']).open('w') as log:
        env=os.environ.copy()
        for key in ['GLIBC_TUNABLES','LEAN_NUM_THREADS','LD_PRELOAD']:env.pop(key,None)
        env.update(s['env'])
        p=subprocess.Popen(s['lean_argv'],env=env,stdout=log,stderr=subprocess.STDOUT,preexec_fn=arm)
        birth=Path(f'/proc/{p.pid}/stat').read_text().rsplit(')',1)[1].split()[19]
        Path(s['native_identity']).write_text(json.dumps({'pid':p.pid,'birth':birth})+'\n')
        _,status,u=os.wait4(p.pid,0)
    code=os.waitstatus_to_exitcode(status)
    row={'returncode':code,'wall_s':time.monotonic()-started,'user_s':u.ru_utime,'system_s':u.ru_stime,
      'peak_rss_kib':u.ru_maxrss,'minor_faults':u.ru_minflt,'major_faults':u.ru_majflt,
      'voluntary_switches':u.ru_nvcsw,'involuntary_switches':u.ru_nivcsw,'pid':p.pid,'birth':birth,
      'retired':not Path(f'/proc/{p.pid}').exists()}
    Path(s['native_receipt']).write_text(json.dumps(row,indent=2)+'\n')
    return code if code>=0 else 128-code
def run_one(module,config,mode,rep,group_remaining,inputs_path=None):
    inputs=json.loads(Path(inputs_path or BASE/'inputs.json').read_text());m=inputs['modules'][module]
    out=BASE/'runs'/f'{module}-{config}-{mode}-r{rep}';out.mkdir(parents=True,exist_ok=False)
    art=out/'artifact'/Path(*m['module'].split('.'));art.parent.mkdir(parents=True,exist_ok=True)
    args=[str(Path(inputs['sdk'])/'bin/lean'),'--root='+m['source_root'],'-j'+('1' if config=='threads1' else '8')]
    if config!='noM':args+=['-M'+str(m['memory_mib'])]
    args+=['-DautoImplicit=false']
    if m['heartbeat_arg'] is not None:args+=['-DmaxHeartbeats='+str(m['heartbeat_arg'])]
    for ext,flag in [('.olean','-o'),('.ilean','-i'),('.c','-c')]:
        if ext in m['outputs']:args += [flag,str(art)+ext]
    args += [m['source']]
    env=os.environ.copy()
    for key in ['GLIBC_TUNABLES','LEAN_NUM_THREADS','LD_PRELOAD']:env.pop(key,None)
    env.update(LEAN_PATH=inputs['LEAN_PATH'],LEAN_NUM_THREADS='1' if config=='threads1' else '8',TMPDIR=inputs['TMPDIR'])
    if config=='mmap_high':env['GLIBC_TUNABLES']='glibc.malloc.mmap_threshold=134217728'
    if config=='trim_high':env['GLIBC_TUNABLES']='glibc.malloc.trim_threshold=134217728'
    s=dict(module=module,config=config,mode=mode,rep=rep,lean_argv=args,env=env,
      wall_limit_s=min(m['wall_limit_s'],group_remaining-15),native_log=str(out/'native.log'),
      native_receipt=str(out/'native.json'),native_identity=str(out/'native-identity.json'),
      constant_outer_cgroup_GiB=15,pcore_affinity='0-7')
    # Environment contains inherited credentials: serialize only the intentionally measured settings.
    current=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
    assert current.name.startswith('cri-containerd-') and 'pod' in current.parent.name
    cg=current.parent/('proofserve-systime-'+str(os.getpid())+'-'+module+'-'+mode+'-'+str(rep)+'.scope')
    cg.mkdir();(cg/'memory.max').write_text(str(15*1024**3))
    s['native_cgroup']=str(cg)
    s['env']={k:env[k] for k in ['LEAN_PATH','LEAN_NUM_THREADS','TMPDIR','GLIBC_TUNABLES'] if k in env}
    public={k:v for k,v in s.items() if k!='env'}
    public['env']={k:env[k] for k in ['LEAN_PATH','LEAN_NUM_THREADS','TMPDIR','GLIBC_TUNABLES'] if k in env}
    (out/'command.json').write_text(json.dumps(public,indent=2)+'\n')
    spec=out/'private-spec.json'
    # Runtime-only specification includes only explicit experimental environment settings.
    fd=os.open(spec,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as f:json.dump(s,f)
    cmd=[sys.executable,str(Path(__file__).resolve()),'--native',str(spec)]
    if mode=='stat':cmd=['perf','stat','-x',';','-o',str(out/'perf-stat.csv'),'-e',EVENTS,'--']+cmd
    elif mode=='record':cmd=['perf','record','-o',str(out/'perf.data'),'-e','cpu_core/cycles/','-F','99','--call-graph','dwarf,8192','--']+cmd
    elif mode=='trace':cmd=['perf','trace','-s','-o',str(out/'perf-trace.txt'),'--']+cmd
    elif mode!='plain':raise ValueError(mode)
    cmd=['taskset','-c','0-7']+cmd
    with LOCK.open('a') as lock:
        queued=time.monotonic()
        fcntl.flock(lock,fcntl.LOCK_EX)
        queue_wait=time.monotonic()-queued
        start=time.monotonic();peak=0;stop=None
        with (out/'observer.log').open('w') as log,(out/'memory.jsonl').open('w') as mem:
            p=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            (out/'observer-identity.json').write_text(json.dumps({'pid':p.pid,'birth':Path(f'/proc/{p.pid}/stat').read_text().rsplit(')',1)[1].split()[19],'argv':cmd})+'\n')
            while p.poll() is None:
                rows=proc_tree(p.pid);rss=sum(x['rss'] for x in rows);peak=max(peak,rss)
                mem.write(json.dumps({'s':time.monotonic()-start,'rss_bytes':rss,'processes':rows})+'\n');mem.flush()
                if rss>16*1024**3:stop='M_RSS_16GiB'
                if time.monotonic()-start>s['wall_limit_s']+8:stop='outer_wall'
                if stop:
                    os.killpg(p.pid,signal.SIGKILL);p.wait();break
                time.sleep(1)
            rc=p.wait()
        # A failed observer must not leave an untracked Lean child behind.
        if (cg/'cgroup.procs').read_text().strip():
            (cg/'cgroup.kill').write_text('1')
            for _ in range(50):
                if not (cg/'cgroup.procs').read_text().strip():break
                time.sleep(.1)
            stop=stop or 'observer_exited_with_native_child'
        # Sampling is not a hard RSS cap; all outer/native limits and any overshoot remain explicit.
        result=dict(module=module,config=config,mode=mode,rep=rep,observer_rc=rc,observer_wall_s=time.monotonic()-start,
          sampled_tree_peak_bytes=peak,stop_reason=stop,raw=str(out),queue_wait_s=queue_wait)
        if Path(s['native_receipt']).exists():result.update(json.loads(Path(s['native_receipt']).read_text()))
        result['olean_exists']=Path(str(art)+'.olean').exists()
        baseline=BASE/'runs'/f'{module}-baseline-plain-r1'/'artifact'/Path(*m['module'].split('.'))
        result['olean_equal_baseline']=filecmp.cmp(str(art)+'.olean',str(baseline)+'.olean',shallow=False) if result['olean_exists'] and Path(str(baseline)+'.olean').exists() else None
        result['cgroup_memory_events']=(cg/'memory.events').read_text()
        result['cgroup_memory_peak_bytes']=int((cg/'memory.peak').read_text())
        result['native_cgroup_retired']=not (cg/'cgroup.procs').read_text().strip()
        if result['native_cgroup_retired']:cg.rmdir()
        else:raise RuntimeError('owned native cgroup not retired; do not release another native task')
        (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        spec.unlink()
    print(json.dumps(result),flush=True)
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument('--native');p.add_argument('--module',choices=['Grid','UMoments9','EnvelopePsiB'])
    p.add_argument('--config',default='baseline',choices=['baseline','mmap_high','trim_high','threads1','noM'])
    p.add_argument('--mode',default='plain',choices=['plain','stat','record','trace']);p.add_argument('--repeats',type=int,default=3)
    a=p.parse_args()
    if a.native:return native(a.native)
    os.sched_setaffinity(0,set(range(8,24)))
    started=time.monotonic()
    for rep in range(1,a.repeats+1):
        if time.monotonic()-started>1680:break
        target=BASE/'runs'/f'{a.module}-{a.config}-{a.mode}-r{rep}'
        if target.exists():raise FileExistsError('do not overwrite/duplicate existing attempt: '+str(target))
        run_one(a.module,a.config,a.mode,rep,1700-(time.monotonic()-started))
    return 0
if __name__=='__main__':sys.exit(main())
