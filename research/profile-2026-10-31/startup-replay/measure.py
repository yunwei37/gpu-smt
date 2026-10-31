#!/usr/bin/env python3
"""Bounded startup/import/replay measurements; raw outputs stay on PVC."""
import os,sys,json,time,signal,subprocess,pathlib,re,fcntl,csv
from pathlib import Path
BASE=Path('/workspaces/.agent-state/gpu-smt-captures')
RAW=BASE/'profile-2026-10-31/startup-replay'
A=Path('/workspaces/.agent-state/gpu-smt-workloads')
SDK=A/'toolchains/lean-4.34.1-linux'
OLD=BASE/'workloads/openai4341-standard-artifacts-a'
ROOT=RAW/'sources/lean'
ROOT.mkdir(parents=True,exist_ok=True)
env=os.environ.copy()
env['PATH']=str(SDK/'bin')+':'+env['PATH']
env['LEAN_NUM_THREADS']='8'
env['TMPDIR']=str(RAW/'tmp')
(RAW/'tmp').mkdir(exist_ok=True)
env['LEAN_PATH']=':'.join([str(OLD/'artifacts'),str(A/'rellich4341-oleans'),str(A/'openai4341-oleans'),(BASE/'workloads/mathlib4341-setup/LEAN_PATH.txt').read_text().strip()])
rows=[json.loads(x) for x in (OLD/'results.jsonl').read_text().splitlines()]
small=[r for r in rows if r['wall_s']<5 and r['status']=='compile_ok']
def imports(text):
    # Match source-native import lines, preserving modifiers; bodies never run.
    # Existing selected sources use plain line-oriented imports.
    return '\n'.join(x for x in text.splitlines() if re.match(r'^\s*(?:(?:public|meta|private)\s+)*import\s+',x))+'\n'
def tree(pid):
    found={pid}; changed=True
    while changed:
        changed=False
        for d in Path('/proc').iterdir():
            if not d.name.isdigit() or int(d.name) in found:continue
            try:
                stat=(d/'stat').read_text().rsplit(')',1)[1].split()
                if int(stat[1]) in found:found.add(int(d.name));changed=True
            except (OSError,ValueError):pass
    return found
def smaps(pid):
    vals={}
    try:
        for x in Path('/proc',str(pid),'smaps_rollup').read_text().splitlines():
            z=x.split()
            if len(z)>2 and z[1].isdigit(): vals[z[0].rstrip(':')]=int(z[1])
    except OSError:pass
    return vals
def measure(key,cmd,limit=90,extra=None):
    start=time.monotonic(); samples=[]; cause=None
    out=RAW/(key+'.stdout');err=RAW/(key+'.stderr')
    with out.open('w') as fo,err.open('w') as fe:
        p=subprocess.Popen(cmd,env=env,cwd=ROOT,stdout=fo,stderr=fe,start_new_session=True)
        birth=Path('/proc',str(p.pid),'stat').read_text().rsplit(')',1)[1].split()[19]
        while True:
            pid,status,u=os.wait4(p.pid,os.WNOHANG)
            if pid:break
            vals={}
            for pp in tree(p.pid):
                for k,v in smaps(pp).items():vals[k]=vals.get(k,0)+v
            samples.append(dict(seconds=time.monotonic()-start,**vals))
            if vals.get('Rss',0)>12*1024**2:cause='rss_budget'
            if time.monotonic()-start>limit:cause='wall_budget'
            if cause:
                try:os.killpg(p.pid,signal.SIGKILL)
                except ProcessLookupError:pass
            time.sleep(.1)
        p.returncode=os.waitstatus_to_exitcode(status)
    end=time.monotonic()
    (RAW/(key+'.smaps.json')).write_text(json.dumps(samples))
    r=dict(key=key,args=cmd,wall_s=end-start,user_s=u.ru_utime,system_s=u.ru_stime,
      peak_rss_kib=u.ru_maxrss,minor_faults=u.ru_minflt,major_faults=u.ru_majflt,
      voluntary_switches=u.ru_nvcsw,involuntary_switches=u.ru_nivcsw,
      returncode=p.returncode,stop=cause,pid=p.pid,birth_ticks=birth,limit_s=limit,
      sampled_tree_peaks_kib={k:max([s.get(k,0) for s in samples],default=0) for k in ['Rss','Pss','Shared_Clean','Shared_Dirty','Private_Clean','Private_Dirty']},
      sample_interval_s=.1,**(extra or {}))
    with (RAW/'results.jsonl').open('a') as f:f.write(json.dumps(r)+'\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(r),flush=True)
    return r
def lean_args(src,key):
    out=RAW/'artifacts'/key;out.parent.mkdir(exist_ok=True)
    return [str(SDK/'bin/lean'),'--root='+str(ROOT),'-j8','-M9216','-DautoImplicit=false',
      '-o',str(out)+'.olean','-i',str(out)+'.ilean','-c',str(out)+'.c',str(src)]
def startup():
    for i,r in enumerate(small):
        original=(A/'openai-math-4eaee875'/r['path']).read_text()
        src=ROOT/r['path'].removeprefix('lean/');src.parent.mkdir(parents=True,exist_ok=True);src.write_text(original)
        imp=ROOT/(f'ImportOnly{i}.lean');imp.write_text(imports(original))
        for rep in range(3):
            for mode,path in [('build',src),('imports',imp)]:
                key=f'{mode}-{i:02d}-{rep}'
                if key in done:continue
                measure(key,lean_args(path,key),90,dict(mode=mode,module=r['module'],rep=rep,historical_build_s=r['wall_s'],imports=imports(original)))
    src=ROOT/'MathlibOnly.lean';src.write_text('import Mathlib\n')
    for rep in range(3):
        key=f'mathlib-{rep}'
        if key not in done:measure(key,lean_args(src,key),90,dict(mode='mathlib',rep=rep))
def replay():
    allrows=rows[:]
    for name in ['openai4341-grid-j8-1200','openai4341-amplitudes-j8-1200']:
        allrows += [json.loads(x) for x in (BASE/'workloads'/name/'results.jsonl').read_text().splitlines()]
    for i,r in enumerate(allrows):
        key=f'replay-{i:02d}'
        if key in done:continue
        measure(key,[str(SDK/'bin/leanchecker'),'-j8','-v',r['module']],180,dict(mode='replay',module=r['module'],historical_build_s=r['wall_s'],historical_build_source=str(OLD) if i<26 else 'separate '+r['module']))
def perf():
    # Separate profiled runs: full Mathlib import and min/median/max selected dependency import.
    selected=sorted(range(len(small)),key=lambda i:small[i]['wall_s'])
    jobs=[('mathlib',ROOT/'MathlibOnly.lean')]+[(f'deps-{i}',ROOT/(f'ImportOnly{i}.lean'))for i in [selected[0],selected[len(selected)//2],selected[-1]]]
    for name,src in jobs:
        key='perf-'+name
        if key in done:continue
        cmd=['perf','record','-F','199','-e','cycles:u','--call-graph','dwarf,8192','-o',str(RAW/(key+'.data')),'--']+lean_args(src,key)
        measure(key,cmd,120,dict(mode='perf',module=name))
if __name__=='__main__':
    phase=sys.argv[1];lock=open(BASE/'pcore.lock','a')
    print('waiting for shared P-core lock',flush=True)
    fcntl.flock(lock,fcntl.LOCK_EX)
    os.sched_setaffinity(0,set(range(8)))
    print('acquired shared P-core lock',flush=True)
    done={json.loads(x)['key'] for x in (RAW/'results.jsonl').read_text().splitlines()}if (RAW/'results.jsonl').exists() else set()
    (RAW/(phase+'-launch.json')).write_text(json.dumps(dict(pid=os.getpid(),phase=phase,affinity=sorted(os.sched_getaffinity(0)),utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),lean_path=env['LEAN_PATH'],sdk=str(SDK),rss_budget_gib=12)))
    try:
        globals()[phase]()
        (RAW/(phase+'-terminal.json')).write_text(json.dumps(dict(status='completed',utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))))
    finally:fcntl.flock(lock,fcntl.LOCK_UN)
