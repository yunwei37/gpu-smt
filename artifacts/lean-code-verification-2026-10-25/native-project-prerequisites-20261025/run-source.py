"""Build native prerequisites in their original package, never the workload root."""
from pathlib import Path
import argparse,datetime,gzip,json,os,signal,subprocess,threading,time
import psutil

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--preparation',required=True,type=Path)
    ap.add_argument('--closure',required=True,type=Path)
    ap.add_argument('--out',required=True,type=Path)
    modes=ap.add_mutually_exclusive_group()
    modes.add_argument('--library',choices=['LeanMLIR'],help='Diagnose an isolated original library context')
    modes.add_argument('--project-prerequisites',action='store_true',help='Prepare original root pins and mixed project prerequisites, excluding the workload')
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
    package=project if args.project_prerequisites else project/args.library if args.library else mathlib
    links=[]
    if args.library:
        # Reuse only dependencies at exactly the original subproject manifest pins.
        # Lake still owns all compiler settings and dependency facets.
        manifest=json.loads((package/'lake-manifest.json').read_text())
        packages=package/manifest.get('packagesDir','.lake/packages')
        packages.mkdir(parents=True,exist_ok=True)
        for entry in manifest['packages']:
            if entry['type']!='git':raise RuntimeError('unsupported library dependency '+entry['name'])
            source=mathlib if entry['name']=='mathlib'else mathlib/'.lake/packages'/entry['name']
            revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
            if revision!=entry['rev']:raise RuntimeError('dependency pin mismatch: '+entry['name'])
            destination=packages/entry['name']
            if destination.exists()or destination.is_symlink():
                if destination.resolve()!=source.resolve():raise RuntimeError('existing package path differs: '+str(destination))
            else:destination.symlink_to(source,target_is_directory=True)
            links.append(dict(name=entry['name'],revision=revision,source=str(source),link=str(destination)))
        targets=[m for m in ordered if Path(nodes[m]['path']).is_relative_to(package)]
    elif args.project_prerequisites:
        targets=[m for m in ordered if m!=closure['root']and Path(nodes[m]['path']).is_relative_to(project)]
    else:
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
        birth=owner.create_time(),sdk=str(sdk),cwd=str(package),eligible_cpus=[11],
        targets=len(targets),dependency_links=links,library=args.library,project_prerequisites=args.project_prerequisites,aggregate_budget_bytes=48*1024**3,old_owner=old.pid if old else None,
        scope='Dependency source compilation only; sequential native Lake olean facets in the original package manifest. Excludes the candidate workload root. Project modes check prior dependency facets without building before each leaf. Original7808group keeps its point; shared CPU interference retained. No candidate capture or new per-process limit.')
    (args.out/'launch.json').write_text(json.dumps(initial,indent=2)+'\n')
    (args.out/'run-source.py').write_bytes(Path(__file__).read_bytes())
    code=0
    try:
        if args.project_prerequisites:
            # Root context is required for reverse LeanMLIR -> SSA imports.
            # Honor every original root manifest pin, including its different Cli.
            manifest=json.loads((project/'lake-manifest.json').read_text())
            packages=project/manifest.get('packagesDir','.lake/packages')
            packages.mkdir(parents=True,exist_ok=True)
            for entry in manifest['packages']:
                if errors:raise RuntimeError('combined memory monitor stopped preparation')
                if entry['type']=='path':
                    if not(project/entry['dir']).is_dir():raise RuntimeError('missing original path package '+entry['name'])
                    continue
                if entry['type']!='git':raise RuntimeError('unsupported root dependency '+entry['name'])
                source=mathlib if entry['name']=='mathlib'else mathlib/'.lake/packages'/entry['name']
                destination=packages/entry['name']
                revision=None
                if source.is_dir()and(source/'.git').exists():
                    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
                if destination.exists()or destination.is_symlink():
                    actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=destination,text=True).strip()
                    if actual!=entry['rev']:raise RuntimeError('existing root dependency differs: '+entry['name'])
                elif revision==entry['rev']:
                    destination.symlink_to(source,target_is_directory=True)
                else:
                    destination.mkdir()
                    commands=[
                        ['git','init','--quiet',str(destination)],
                        ['git','-C',str(destination),'remote','add','origin',entry['url']],
                        ['git','-C',str(destination),'fetch','--depth=1','origin',entry['rev']],
                        ['git','-C',str(destination),'checkout','--quiet','--detach','FETCH_HEAD']]
                    with(args.out/('package-'+entry['name']+'.log')).open('wb')as stream:
                        for command in commands:
                            if errors:raise RuntimeError('combined memory monitor stopped package fetch')
                            process=subprocess.Popen(command,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
                            active=('package:'+entry['name'],process);result=process.wait();active=None
                            with(args.out/'package-commands.jsonl').open('a')as receipt:
                                receipt.write(json.dumps(dict(command=command,exit=result))+'\n')
                            if result:raise RuntimeError('original root dependency fetch failed: '+entry['name'])
                    actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=destination,text=True).strip()
                    if actual!=entry['rev']:raise RuntimeError('fetched root dependency differs: '+entry['name'])
                links.append(dict(name=entry['name'],revision=entry['rev'],path=str(destination),reused=destination.is_symlink()))
            (args.out/'root-dependencies.json').write_text(json.dumps(links,indent=2)+'\n')
        for index,module in enumerate(targets):
            if errors:code=1;break
            command=[str(sdk/'bin/lake'),'build','+'+module+':olean']
            log=args.out/(str(index).zfill(4)+'.log');started=time.monotonic()
            with log.open('wb')as stream:
                if args.library or args.project_prerequisites:
                    # Fail rather than launch a fan-out dependency rebuild when
                    # the explicitly prepared topological prerequisites are stale.
                    check=[str(sdk/'bin/lake'),'--no-build','build','+'+module+':deps']
                    process=subprocess.Popen(check,cwd=package,env=env,stdout=stream,
                        stderr=subprocess.STDOUT,start_new_session=True)
                    active=(module,process);dependency_exit=process.wait();active=None
                    with(args.out/'dependency-checks.jsonl').open('a')as receipt:
                        receipt.write(json.dumps(dict(module=module,command=check,exit=dependency_exit))+'\n')
                    if dependency_exit or errors:
                        raise RuntimeError('library dependency check failed: '+module)
                process=subprocess.Popen(command,cwd=package,env=env,stdout=stream,
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
