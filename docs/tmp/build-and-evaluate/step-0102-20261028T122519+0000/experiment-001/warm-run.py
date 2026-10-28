"""Finite retained Kimina warm resource baseline; no oracle or new service.

Runs official Manager/run_checks directly, matching CLI-level engine transport.
The only native cap adaptation sets Repl.max_memory_bytes to RLIM_INFINITY.
One existing owned-tree watchdog supplies resource attribution; preempted sources
are retried exclusively after peers and warm idle workers retire.
"""
from pathlib import Path
import argparse,asyncio,collections,datetime,gzip,importlib.util,json,os,resource,signal,sys,time

ROOT=Path('/workspaces/repository')
KIMINA=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
MEMORY=ROOT/'bench/lean-native/linarith-oracle/memory_budget.py'
INPUT=ROOT/'artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z/input7808.json.gz'
CONTEXT=ROOT/'artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z/manifest.json'

def alive(pid,birth):
    try:
        tail=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
        return int(tail[19])==birth and tail[0]!='Z'
    except FileNotFoundError:
        return False

def no_other_collection():
    # Inspect the recorded owner, not another Workspace's processes.
    pointer=Path('/tmp/gpu-smt-active-prepared-policy7808.txt')
    if pointer.exists():
        previous=Path(pointer.read_text().strip())
        for launch in previous.glob('*/launch.json'):
            row=json.loads(launch.read_text())
            if alive(row['pid'],row['start_ticks']):
                raise RuntimeError(f"Retained native collection still live: {launch}")
    if resource.getrlimit(resource.RLIMIT_AS)!=(-1,-1):
        raise RuntimeError('An inherited fixed address-space cap would invalidate this resource point')

def native_library_environment(context):
    project=Path(context['project'])
    library=project/'.lake/build/lib/libMathlib-Tactic-Linarith-1.so'
    if not library.is_file():raise RuntimeError('Retained native Mathlib library missing')
    paths=[]
    for entry in context['LEAN_PATH'].split(os.pathsep)+[str(Path(context['sysroot'])/'lib'),str(Path(context['sysroot'])/'lib/lean')]:
        path=Path(entry)
        if not path.is_absolute():path=project/path
        path=path.resolve()
        if path.is_dir()and str(path)not in paths:paths.append(str(path))
    return {'LEAN_SERVER_NATIVE_DYNLIB':str(library),'LD_LIBRARY_PATH':os.pathsep.join(paths)}

async def main(args):
    no_other_collection()
    os.sched_setaffinity(0,{8,9,10,11})
    context=json.loads(CONTEXT.read_text())
    sdk=context['sysroot'];project=context['project']
    # Warm GC support is the retained native REPL, not the frozen arithmetic oracle.
    repl=Path('/tmp/gpu-smt-linarith-oracle-20261017/prefix/repl-kernel/.lake/build/bin/repl')
    if not repl.is_file():raise RuntimeError('Retained native warm REPL missing')
    os.environ.update(PATH=sdk+'/bin:'+os.environ['PATH'],LEAN_SYSROOT=sdk,
        LEAN_PATH=context['LEAN_PATH'],LEAN_SERVER_PROJECT_DIR=project,
        LEAN_SERVER_REPL_PATH=str(repl),LEAN_SERVER_LEAN_VERSION='v4.9.0-rc1',
        LEAN_SERVER_MAX_REPLS='4',LEAN_SERVER_ENVIRONMENT='prod',GPU_SMT_MEMORY_DIRECTORY=str(args.out),
        GPU_SMT_CEX_MODE='off')
    # Match the historical strong native compilation without its disabled CEX wrapper.
    library_environment=native_library_environment(context)
    os.environ.update(library_environment)
    native_library=library_environment['LEAN_SERVER_NATIVE_DYNLIB']
    # No arithmetic oracle, numeric service, counterexample provider or profiling hook.
    for key in list(os.environ):
        if key.startswith('GPU_ARITHMETIC_') or key in ['GPU_SMT_CANDIDATE_TIMING']:
            os.environ.pop(key)
    sys.path[:0]=[str(KIMINA),str(KIMINA/'client')]
    from kimina_client import Snippet
    from server.repl import Repl
    from server.manager import Manager
    from server.routers.check import run_checks
    from server.split import split_snippet
    from server import benchmark_memory
    from loguru import logger
    import psutil
    args.out.mkdir(parents=True,exist_ok=False)
    logger.remove()
    logger.add(args.out/'kimina.log',level='INFO',enqueue=False)
    # Explicit benchmark-local resource adaptation; installed source is untouched.
    original_init=Repl.__init__
    original_close=Repl.close
    created=[];retirements={}
    def uncapped_init(self,*a,**kw):
        original_init(self,*a,**kw)
        self.max_memory_bytes=resource.RLIM_INFINITY
        created.append(self)
    async def close_once(self):
        process=self.proc
        if process is None:return
        # Manager destruction schedules close asynchronously. Retain and await
        # that same official operation once per native Process object, avoiding
        # both a second close against a recycled PID and unawaited retirement.
        task=retirements.get(process)
        if task is None:
            task=asyncio.create_task(original_close(self))
            retirements[process]=task
        await asyncio.shield(task)
    Repl.__init__=uncapped_init
    Repl.close=close_once
    spec=importlib.util.spec_from_file_location('retained_resource_watchdog',MEMORY)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    watchdog=mod.MemoryWatchdog(os.getpid(),48*1024**3,48*1024**3,4,repl,args.out)
    source=json.loads(gzip.decompress(INPUT.read_bytes()))
    candidates=source['candidates']
    if args.phase=='qualification':
        # Real ordinary and heavy inputs exercise resource retry, not a toy.
        candidates=[source['candidates'][i]for i in list(range(16))+[1885,2325,2507,3086,3209,3683,3685,7230]]
    ids=[v['id']for v in candidates]
    assert len(set(ids))==len(ids)
    headers=[split_snippet(v['code']).header for v in candidates]
    header=next((x for x in headers if x),'')
    manager=Manager(max_repls=4,init_repls={header:4}if header else {})
    loop=asyncio.get_running_loop();owner=asyncio.current_task()
    watchdog.on_error=lambda:loop.call_soon_threadsafe(owner.cancel)
    attempts={v['id']:[]for v in candidates};final={};physical=[];preempted=[]
    ledger=(args.out/'attempts.jsonl').open('w')
    started=time.monotonic();failure=None
    def record(value):
        ledger.write(json.dumps(value,ensure_ascii=False)+'\n');ledger.flush()
    async def close_workers():
        # Official manager schedules asynchronous close. Await the same owned
        # Repl.close operations first so the next phase cannot overlap retirement.
        await asyncio.gather(*(w.close()for w in created))
        manager._free.clear();manager._busy.clear()
    async def execute(candidate,exclusive=False):
        begin=time.monotonic()
        try:
            response=await asyncio.wait_for(run_checks(
                [Snippet(id=candidate['id'],code=candidate['code'])],
                candidate['timeout_ms']/1000,False,manager,True),candidate['timeout_ms']/1000)
            assert len(response)==1
            assert response[0].id in [candidate['id'],candidate['id']+'-header']
            value=response[0]
            status='resource_failure'if(value.error or '').startswith('resource_failure:')else value.analyze().status.value
            result=value.model_dump(exclude_none=True)
        except TimeoutError:
            status='timeout_error';result={'id':candidate['id'],'error':'complete admitted native attempt deadline'}
        except Exception as exc:
            # Preserve source-level transport/backend faults as rows, not lost work.
            status='server_error';result={'id':candidate['id'],'error':repr(exc)}
        row={'id':candidate['id'],'exclusive':exclusive,'wall_seconds':time.monotonic()-begin,
             'status':status,'result':result,'source_unchanged':True}
        attempts[candidate['id']].append(row);physical.append(row);record(row)
        # Only an actual concurrent watchdog preemption gets an exclusive retry.
        retry=not exclusive and status=='resource_failure'and 'aggregate RSS watchdog:'in result.get('error','')
        if retry:preempted.append(candidate)
        else:final[candidate['id']]=row
    for sig in [signal.SIGINT,signal.SIGTERM]:
        loop.add_signal_handler(sig,owner.cancel)
    watchdog.start()
    try:
        await manager.initialize_repls()
        warm_ready=time.monotonic()-started
        loaded=[]
        for process in watchdog.owned():
            try:
                command=process.cmdline()
                if not command or Path(command[0]).name!=repl.name:continue
                before=process.create_time()
                paths={line.split()[-1]for line in Path('/proc',str(process.pid),'maps').read_text().splitlines()if len(line.split())>=6}
                assert native_library in paths,'Warm native compilation was not actually mapped'
                assert before==process.create_time()
                loaded.append({'pid':process.pid,'birth':before,'native_library':native_library,'mapped':True})
            except psutil.NoSuchProcess:raise RuntimeError('Warm worker exited before native-library readiness')
        assert len(loaded)==4,'Native-library readiness must cover all four warm REPLs'
        (args.out/'native-library-readiness.json').write_text(json.dumps(loaded,indent=2)+'\n')
        # A shared queue never dispatches a fifth native request. When pressure
        # preempts an attempt, drain peers,retire all idle warm states,then retry
        # actual preempted sources one at a time. No predicted rejection.
        pending=iter(candidates);active=set();exhausted=False
        while not exhausted or active:
            while len(active)<4 and not exhausted and not preempted:
                # Actual RSS guard is the final authority; do not admit new
                # source work at/above the total budget while peers can retire.
                total=0
                for process in watchdog.owned():
                    try:total+=process.memory_info().rss
                    except psutil.NoSuchProcess:pass
                if total>=48*1024**3:
                    if not active:
                        await close_workers()
                        continue
                    break
                candidate=next(pending,None)
                if candidate is None:exhausted=True;break
                active.add(asyncio.create_task(execute(candidate)))
            if active:
                done,active=await asyncio.wait(active,return_when=asyncio.FIRST_COMPLETED)
                for task in done:task.result()
            if preempted:
                if active:
                    await asyncio.gather(*active)
                    active.clear()
                await close_workers()
                while preempted:
                    candidate=preempted.pop(0)
                    await execute(candidate,exclusive=True)
        assert set(final)==set(ids)
        if watchdog.error:raise RuntimeError(watchdog.error)
        await close_workers()
        statuses=collections.Counter(v['status']for v in final.values())
        (args.out/'results.json').write_text(json.dumps({
            'original_candidates':candidates,'results':[final[i]for i in ids],
            'attempts':attempts},ensure_ascii=False)+'\n')
        terminal={'state':'complete','returned':len(final),'counts':dict(statuses),
          'preparation_seconds':warm_ready,'whole_seconds':time.monotonic()-started,
          'physical_attempts':len(physical),'scope':'official retained Kimina Manager/run_checks;CLI-level transport;not HTTP latency;all native outcomes/retries charged'}
    except BaseException as exc:
        failure=repr(exc)
        for task in list(locals().get('active',set())):task.cancel()
        await asyncio.gather(*list(locals().get('active',set())),return_exceptions=True)
        await close_workers()
        terminal={'state':'failed-or-interrupted','error':failure,'returned':len(final),
                  'whole_seconds':time.monotonic()-started}
    finally:
        watchdog.stop();ledger.close()
        terminal.update(memory=watchdog.summary(),resources={'memory_bytes':48*1024**3,
         'cpus':[8,9,10,11],'maximum_native_workers':4,'per_process_AS':None},
         source_repl=str(repl),native_library=native_library,source_context=context,phase=args.phase,
         adaptation='benchmark-local Repl.max_memory_bytes=RLIM_INFINITY;installed source unchanged',
         UTC=datetime.datetime.now(datetime.timezone.utc).isoformat())
        # Independent actual process check,including reparented owned descendants.
        survivors=[]
        for proc in watchdog.owned():
            try:
                command=proc.cmdline()
                if proc.pid!=os.getpid()and command:
                    survivors.append({'pid':proc.pid,'birth':proc.create_time(),'command':command})
            except Exception:pass
        terminal['native_survivors']=survivors
        if survivors:terminal['state']='failed-retirement'
        (args.out/'terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
    print(json.dumps(terminal))
    if terminal['state']!='complete':raise RuntimeError(failure or terminal['state'])

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=['qualification','full'],required=True)
    parser.add_argument('--out',type=Path,required=True)
    asyncio.run(main(parser.parse_args()))
