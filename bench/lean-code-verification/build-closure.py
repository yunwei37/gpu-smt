"""Build only source-native external prerequisites, never the workload root."""
from pathlib import Path
import argparse,datetime,gzip,json,os,signal,subprocess,threading,time
import psutil

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--preparation',required=True,type=Path)
    ap.add_argument('--closure',required=True,type=Path)
    ap.add_argument('--out',required=True,type=Path)
    args=ap.parse_args()
    prep=json.loads(args.preparation.read_text());closure=json.loads(args.closure.read_text())
    sdk=Path(prep['SDK']);project=Path(prep['project']);mathlib=Path(prep['mathlib'])
    assert not closure['unresolved']
    args.out.mkdir(exist_ok=False)
    os.sched_setaffinity(0,{11})
    owner=psutil.Process();old=None
    if psutil.pid_exists(283334):
        candidate=psutil.Process(283334)
        if abs(candidate.create_time()-1792912973.05)<.01:old=candidate
    nodes=closure['modules'];seen=set();visiting=set();ordered=[]
    def visit(module):
        if module in seen or module not in nodes:return
        if module in visiting:raise RuntimeError('native import cycle: '+module)
        visiting.add(module)
        for imp in nodes[module]['imports']:visit(imp)
        visiting.remove(module);seen.add(module);ordered.append(module)
    visit(closure['root'])
    # Do not build root/project workloads while another capture owns the slot.
    targets=[m for m in ordered if not Path(nodes[m]['path']).is_relative_to(project)]
    assert closure['root']not in targets
    env=dict(os.environ,PATH=str(sdk/'bin')+os.pathsep+os.environ['PATH'])
    env.pop('LEAN_PATH',None)
    (args.out/'targets.json').write_text(json.dumps(targets,indent=2)+'\n')
    start=time.monotonic();stop=threading.Event();errors=[];active=None;completed=[]
    def watch():
        with gzip.open(args.out/'memory-samples.jsonl.gz','wt')as stream:
            while not stop.is_set():
                try:
                    members={}
                    for root in [owner]+([old]if old else[]):
                        try:
                            for q in [root]+root.children(recursive=True):
                                try:members[(q.pid,q.create_time())]=q.memory_info().rss
                                except psutil.NoSuchProcess:pass
                        except psutil.NoSuchProcess:pass
                    total=sum(members.values())
                    stream.write(json.dumps(dict(seconds=time.monotonic()-start,rss_bytes=total,
                        active_module=active[0]if active else None,
                        processes=[dict(pid=k[0],birth=k[1],rss_bytes=v)for k,v in members.items()]))+'\n')
                    stream.flush()
                    if total>48*1024**3:
                        errors.append('Combined48GiBpressure; terminate only newly admitted setup')
                        if active and active[1].poll()is None:os.killpg(active[1].pid,signal.SIGKILL)
                        return
                except Exception as e:
                    errors.append(repr(e))
                    if active and active[1].poll()is None:
                        try:os.killpg(active[1].pid,signal.SIGKILL)
                        except ProcessLookupError:pass
                    return
                stop.wait(1)
    thread=threading.Thread(target=watch,daemon=True);thread.start()
    initial=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),pid=os.getpid(),
        birth=owner.create_time(),sdk=str(sdk),cwd=str(mathlib),eligible_cpus=[11],
        targets=len(targets),aggregate_budget_bytes=48*1024**3,old_owner=old.pid if old else None,
        scope='Dependency source compilation only; sequential native Lake module olean facets in Mathlib own pinned manifest. Excludes all58project modules/workload root. Original7808group keeps its point; shared CPU interference retained. No candidate capture or new per-process limit.')
    (args.out/'launch.json').write_text(json.dumps(initial,indent=2)+'\n')
    (args.out/'run-source.py').write_bytes(Path(__file__).read_bytes())
    code=0
    try:
        for index,module in enumerate(targets):
            if errors:code=1;break
            command=[str(sdk/'bin/lake'),'build','+'+module+':olean']
            log=args.out/(str(index).zfill(4)+'.log');started=time.monotonic()
            with log.open('wb')as stream:
                process=subprocess.Popen(command,cwd=mathlib,env=env,stdout=stream,
                    stderr=subprocess.STDOUT,start_new_session=True)
                active=(module,process);result=process.wait();active=None
            row=dict(module=module,index=index,command=command,exit=result,
                seconds=time.monotonic()-started)
            completed.append(row)
            with(args.out/'commands.jsonl').open('a')as stream:stream.write(json.dumps(row)+'\n')
            with log.open('rb')as src,gzip.open(log.with_suffix('.log.gz'),'wb')as dst:
                import shutil;shutil.copyfileobj(src,dst)
            log.unlink()
            print(json.dumps(row),flush=True)
            if result:code=1;break
    except BaseException as e:
        errors.append(repr(e));code=1
        if active and active[1].poll()is None:
            os.killpg(active[1].pid,signal.SIGKILL);active[1].wait()
        raise
    finally:
        stop.set();thread.join()
        (args.out/'terminal.json').write_text(json.dumps(dict(state='complete'if code==0 and len(completed)==len(targets)else'incomplete',
            expected_modules=len(targets),returned=len(completed),errors=errors,
            seconds=time.monotonic()-start,exit=code,native_candidate_executions=0,
            project_workload_built=False),indent=2)+'\n')
    return code

if __name__=='__main__':raise SystemExit(main())
