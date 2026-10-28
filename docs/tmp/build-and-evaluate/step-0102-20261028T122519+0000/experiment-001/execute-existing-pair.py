from pathlib import Path
import datetime,importlib.util,json,os,subprocess,time,resource
R=Path('/workspaces/repository')
PY='/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(pid,birth):
    try:
        fields=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
        return fields if int(fields[19])==birth else None
    except FileNotFoundError:return None
def main():
    out=Path(__file__).parent
    m=json.loads((out/'manifest.json').read_text())
    assert m['state']=='root-reviewed-for-full-pair'
    prior=Path(m['previous_qualification'])
    assert json.loads((prior/'terminal.json').read_text())['state']=='timely-reply24-complete'
    old=json.loads((prior/'engine-launch.json').read_text())
    assert state(old['pid'],old['start_ticks']) is None or state(old['pid'],old['start_ticks'])[0]=='Z'
    cap=json.loads((prior/'engine.stdout').read_text())
    for row in cap['results']:
        for attempt in row['attempts']:
            for process in attempt['processes']:
                s=state(process['pid'],process['start_ticks'])
                assert s is None or s[0]=='Z'
    assert resource.getrlimit(resource.RLIMIT_AS)==(-1,-1)
    os.sched_setaffinity(0,{8,9,10,11})
    previous=m['source_context']
    spec=importlib.util.spec_from_file_location('warm_resource_context',out/'warm-run.py')
    warm_context=importlib.util.module_from_spec(spec);spec.loader.exec_module(warm_context)
    library_environment=warm_context.native_library_environment(previous)
    native_library=library_environment['LEAN_SERVER_NATIVE_DYNLIB']
    assert native_library==m['native_library']
    env=dict(os.environ,LEAN_SYSROOT=previous['sysroot'],LEAN_PATH=previous['LEAN_PATH'],
      **library_environment,PATH=previous['sysroot']+'/bin:'+os.environ['PATH'])
    for name,command,cwd in [
      ('warm',[PY,str(out/'warm-run.py'),'--phase','full','--out',str(out/'warm')],R),
      ('engine',[m['engine_binary'],'measure','--repl',m['warm_repl'],'--project',previous['project'],
       '--environment','lean49-resource-qualification-matched','--prepared-host',m['prepared_host'],
       '--sysroot',previous['sysroot'],'--cpus','8,9,10,11','--worker-cores','1','--memory-gib','48',
       '--policy','fifo'],Path(previous['project']))]:
        start=time.monotonic()
        with (out/(name+'.stdout')).open('wb')as dest,(out/(name+'.stderr')).open('wb')as err:
            with (out/'input7808.json').open('rb')as src:
                child=subprocess.Popen(command,cwd=cwd,env=env,stdin=src,stdout=dest,stderr=err,start_new_session=True)
                (out/(name+'-launch.json')).write_text(json.dumps({'utc':now(),'pid':child.pid,
                  'start_ticks':int(Path(f'/proc/{child.pid}/stat').read_text().rsplit(')',1)[1].split()[19]),
                  'command':command})+'\n')
                rc=child.wait()
        (out/(name+'-exit.json')).write_text(json.dumps({'utc':now(),'exit':rc,
          'external_seconds':time.monotonic()-start,'scope':'launch to complete output/exit;archive separately charged'})+'\n')
        if rc:raise RuntimeError(f'{name} qualification failed; preserve raw output')
        if name=='warm':
            done=json.loads((out/'warm/terminal.json').read_text())
            assert done['state']=='complete'and done['returned']==7808 and not done['native_survivors']
            raw=json.loads((out/'warm/results.json').read_text())
            assert raw['original_candidates']==json.loads((out/'input7808.json').read_text())['candidates']
            assert done['memory']['error']is None
            assert done['memory']['peak_sampled_native_repl_count']==4,'No actual four-worker warm engagement'
            observed_limits=[]
            with (out/'warm/memory-rss.jsonl').open()as samples:
                for line in samples:
                    for process in json.loads(line)['processes']:
                        if process['native_repl']:
                            observed_limits.extend(process.get('address_limit',[]))
            assert observed_limits and all('unlimited' in limit for limit in observed_limits),'Actual AS cap remains'
        else:
            done=json.loads((out/'engine.stdout').read_text())
            assert len(done['results'])==7808
            assert done['batch']==json.loads((out/'input7808.json').read_text())
            contexts=[json.loads(event['detail'])['prepared_context']
                for row in done['results']for attempt in row['attempts']for event in attempt['backend_events']
                if event['stage']=='prepared_ready']
            assert contexts and all(c.get('native_library')==native_library for c in contexts),'Prepared native compilation was not loaded'
            for row in done['results']:
                for attempt in row['attempts']:
                    for process in attempt['processes']:
                        current=state(process['pid'],process['start_ticks'])
                        assert current is None or current[0]=='Z','Engine qualification survivor'
    (out/'terminal.json').write_text(json.dumps({'utc':now(),'state':'full-pair-complete',
      'full_comparison_started':True,'resource_gain_claim':False,'next':'Root whole-population correctness/resource/performance review,then separately staged42 resource rerun'})+'\n')

if __name__=='__main__':main()
