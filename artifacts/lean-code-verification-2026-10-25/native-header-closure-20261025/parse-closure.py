"""Use the workload's own Lean header parser; never elaborate candidate bodies."""
from pathlib import Path
import argparse,collections,datetime,gzip,json,os,signal,subprocess,threading,time
import psutil

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--preparation',required=True,type=Path)
    ap.add_argument('--root',required=True)
    ap.add_argument('--out',required=True,type=Path)
    args=ap.parse_args()
    prep=json.loads(args.preparation.read_text())
    sdk=Path(prep['SDK']);project=Path(prep['project']);mathlib=Path(prep['mathlib'])
    args.out.mkdir(exist_ok=False)
    roots=[project]
    manifest=json.loads((project/'lake-manifest.json').read_text())
    roots += [project/p['dir']for p in manifest['packages']if p['type']=='path']
    roots += [mathlib]+sorted((mathlib/'.lake/packages').glob('*'))
    roots=[p for p in roots if p.is_dir()]
    owner=psutil.Process();old=None
    if psutil.pid_exists(283334):
        candidate=psutil.Process(283334)
        if abs(candidate.create_time()-1792912973.05)<.01:old=candidate
    os.sched_setaffinity(0,{11})
    helper=Path(__file__).with_name('ParseImports.lean')
    env=dict(os.environ,PATH=str(sdk/'bin')+os.pathsep+os.environ['PATH'])
    env.pop('LEAN_PATH',None)
    command=[str(sdk/'bin/lean'),'--run',str(helper)]
    started=time.monotonic();stop=threading.Event();samples=[];error=[];process=None
    def watch():
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
                samples.append(dict(seconds=time.monotonic()-started,rss_bytes=total,
                    processes=[dict(pid=k[0],birth=k[1],rss_bytes=v)for k,v in members.items()]))
                if total>48*1024**3:
                    error.append('combined research RSS exceeds48GiB; abort new source parsing only')
                    if process and process.poll()is None:os.killpg(process.pid,signal.SIGKILL)
                    return
            except Exception as e:
                error.append(repr(e))
                if process and process.poll()is None:
                    try:os.killpg(process.pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                return
            stop.wait(1)
    thread=threading.Thread(target=watch,daemon=True)
    graph={};unresolved=[];collisions=[];parsed=[];queue=collections.deque([args.root])
    def locate(module):
        rel=Path(*module.split('.')).with_suffix('.lean')
        found=[root/rel for root in roots if(root/rel).is_file()]
        if len(found)>1:collisions.append(dict(module=module,paths=[str(p)for p in found]))
        return found[0]if found else None
    try:
        with (args.out/'stderr.log').open('wb')as stderr:
            process=subprocess.Popen(command,cwd=project,env=env,stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,stderr=stderr,text=True,start_new_session=True)
            thread.start()
            seen=set()
            while queue:
                module=queue.popleft()
                if module in seen:continue
                seen.add(module)
                path=locate(module)
                if path is None:
                    rel=Path(*module.split('.'))
                    if (sdk/'lib/lean'/rel).with_suffix('.olean').exists():continue
                    unresolved.append(module);continue
                process.stdin.write(json.dumps(str(path))+'\n');process.stdin.flush()
                line=process.stdout.readline()
                if not line:raise RuntimeError('native header parser ended before response: '+str(process.poll()))
                try:row=json.loads(line)
                except json.JSONDecodeError:
                    (args.out/'unexpected-stdout.txt').write_text(line+process.stdout.read())
                    raise
                assert row['path']==str(path)
                if row['header_errors']:raise RuntimeError('native header errors: '+str(path))
                parsed.append(row)
                names=[x['module']for x in row['imports']]
                graph[module]=dict(path=str(path),imports=names,import_flags=row['imports'])
                queue.extend(names)
            process.stdin.close();code=process.wait()
            if code or error:raise RuntimeError(f'parser exit{code}; monitor{error}')
    finally:
        if process and process.poll()is None:
            os.killpg(process.pid,signal.SIGKILL);process.wait()
        stop.set()
        if thread.ident:thread.join()
        (args.out/'raw-headers.jsonl.gz').write_bytes(gzip.compress(
            ''.join(json.dumps(x)+'\n'for x in parsed).encode(),mtime=0))
        (args.out/'memory-samples.jsonl.gz').write_bytes(gzip.compress(
            ''.join(json.dumps(x)+'\n'for x in samples).encode(),mtime=0))
        receipt=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            command=command,parser_source=str(helper),root=args.root,cwd=str(project),
            seconds=time.monotonic()-started,parsed_modules=len(graph),unresolved=unresolved,
            resolution_collisions=collisions,monitor_errors=error,
            aggregate_peak_rss_bytes=max((x['rss_bytes']for x in samples),default=None),
            existing_owner_pid=old.pid if old else None,
            scope='Source header parsing only. SDK builtins excluded; import flags retained. No candidate body/import initialization is executed; not compiled dependency readiness.',
            source_roots=[str(p)for p in roots],native_candidate_executions=0)
        (args.out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
        (args.out/'closure.json').write_text(json.dumps(dict(root=args.root,modules=graph,
            unresolved=unresolved,scope=receipt['scope']),indent=2)+'\n')
        (args.out/'ParseImports.lean').write_bytes(helper.read_bytes())
        (args.out/'parse-closure.py').write_bytes(Path(__file__).read_bytes())
        print(json.dumps(receipt),flush=True)

if __name__=='__main__':main()
