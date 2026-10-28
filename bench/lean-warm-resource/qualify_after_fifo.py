"""Continue the existing finite capture with the requested resource preflight.

No schedule/service/AI session. Wait once on the exact current CLI pidfd,retain
its complete result,retire the paused old serial wrapper without resuming its
policy queue,then execute one warm/engine real qualification pair. Stop for root
result review;do not launch full throughput or workload policies automatically.
"""
from pathlib import Path
import collections,datetime,gzip,importlib.util,json,os,select,signal,subprocess,time

R=Path('/workspaces/repository')
PY='/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(pid,birth):
    try:
        fields=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
        return fields if int(fields[19])==birth else None
    except FileNotFoundError:return None
def main():
    own=Path('/tmp/gpu-smt-active-warm-resource-qualification.txt')
    out=Path(own.read_text().strip());m=json.loads((out/'manifest.json').read_text())
    old=Path(m['retained_fifo_root']);previous=json.loads((old/'manifest.json').read_text())
    launch=json.loads((old/'block1-fifo/launch.json').read_text())
    pid,birth=launch['pid'],launch['start_ticks']
    original=state(previous['controller_pid'],previous['controller_start_ticks'])
    assert original and original[0]=='T','Old policy wrapper must remain stopped'
    assert not(old/'block1-task-memory').exists()
    os.sched_setaffinity(0,{8,9,10,11})
    (out/'controller-start.json').write_text(json.dumps({'utc':now(),'pid':os.getpid(),
      'start_ticks':int(Path('/proc/self/stat').read_text().rsplit(')',1)[1].split()[19]),
      'adopted_fifo_pid':pid,'adopted_fifo_start_ticks':birth})+'\n')
    fields=state(pid,birth)
    if fields and fields[0]!='Z':
        fd=os.pidfd_open(pid);poll=select.poll();poll.register(fd,select.POLLIN)
        poll.poll();os.close(fd) # No repeated agent polling or new runtime timer.
    observed=now();fields=state(pid,birth)
    # It is still a child of the paused original controller,so Linux retains
    # its wait status until that wrapper retires. Never infer exit0 from a file.
    code=fields[49]if fields and len(fields)>49 else None
    retained=old/'block1-fifo'
    capture=json.loads((retained/'capture.json').read_text())
    assert len(capture['results'])==7808
    for row in capture['results']:
        for attempt in row['attempts']:
            for process in attempt['processes']:
                current=state(process['pid'],process['start_ticks'])
                assert current is None or current[0]=='Z','Native survivor before next collection'
    (out/'retained-fifo-terminal.json').write_text(json.dumps({
      'observed_exit_utc':observed,'kernel_wait_status':code,'lifecycle_seconds':capture['lifecycle_seconds'],
      'returned':len(capture['results']),'counts':dict(collections.Counter(v['outcome']['status']for v in capture['results'])),
      'original_external_controller_clock':None,'scope':'Original frozen FIFO result;wrapper was paused,not a final matched warm ratio. Internal capture remains exact.'},indent=2)+'\n')
    assert code in [0,'0'],'Preserve nonzero native controller exit before new work'
    spec=importlib.util.spec_from_file_location('closed_archive',R/'artifacts/hotspot-mechanisms-2026-10-25/prepared71-20261026/execute.py')
    archive=importlib.util.module_from_spec(spec);spec.loader.exec_module(archive)
    for f in [retained/'capture.json',retained/'resource-events.jsonl']:archive.archive_closed(f)
    core_rows=[]
    for core in sorted(Path(previous['project']).glob('core*'),key=lambda p:p.stat().st_size if p.is_file()else 0):
        if not core.is_file()or not(core.name=='core'or(core.name.startswith('core.')and core.name[5:].isdigit())):continue
        st=core.stat();destination=core.with_suffix(core.suffix+'.gz')
        assert not destination.exists(),'Never overwrite an existing private core archive'
        archive.archive_closed(core)
        core_rows.append({'source':str(core),'archive':str(destination),'source_bytes':st.st_size,
                          'stored_bytes':destination.stat().st_size,'full_byte_comparison':True})
    (out/'retained-private-core-archives.json').write_text(json.dumps(core_rows,indent=2)+'\n')
    original=state(previous['controller_pid'],previous['controller_start_ticks'])
    if original:
        assert original[0]=='T'
        # SIGTERM is pending before SIGCONT,so no automatic next policy bytecode runs.
        os.kill(previous['controller_pid'],signal.SIGTERM)
        os.kill(previous['controller_pid'],signal.SIGCONT)
    del capture
    env=dict(os.environ,LEAN_SYSROOT=previous['sysroot'],LEAN_PATH=previous['LEAN_PATH'],
      PATH=previous['sysroot']+'/bin:'+os.environ['PATH'])
    for name,command,cwd in [
      ('warm',[PY,str(out/'warm-run.py'),'--phase','qualification','--out',str(out/'warm')],R),
      ('engine',[str(out/'gpu-smt'),'measure','--repl',m['warm_repl'],'--project',previous['project'],
       '--environment','lean49-resource-qualification-matched','--prepared-host',str(out/'prepared-host'),
       '--sysroot',previous['sysroot'],'--cpus','8,9,10,11','--worker-cores','1','--memory-gib','48',
       '--policy','fifo'],Path(previous['project']))]:
        start=time.monotonic()
        with (out/(name+'.stdout')).open('wb')as dest,(out/(name+'.stderr')).open('wb')as err:
            with (out/'input24.json').open('rb')as src:
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
            assert done['state']=='complete'and done['returned']==24 and not done['native_survivors']
            raw=json.loads((out/'warm/results.json').read_text())
            assert raw['original_candidates']==json.loads((out/'input24.json').read_text())['candidates']
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
            assert len(done['results'])==24
            assert done['batch']==json.loads((out/'input24.json').read_text())
            for row in done['results']:
                for attempt in row['attempts']:
                    for process in attempt['processes']:
                        current=state(process['pid'],process['start_ticks'])
                        assert current is None or current[0]=='Z','Engine qualification survivor'
    (out/'terminal.json').write_text(json.dumps({'utc':now(),'state':'qualification-pair-complete',
      'full_comparison_started':False,'resource_gain_claim':False,'next':'Root result review and resource repair before full matched run or workload-policy gains'})+'\n')

if __name__=='__main__':
    try:main()
    except BaseException as exc:
        pointer=Path('/tmp/gpu-smt-active-warm-resource-qualification.txt')
        if pointer.exists():
            out=Path(pointer.read_text().strip())
            (out/'controller-error.json').write_text(json.dumps({'utc':now(),'error':repr(exc)})+'\n')
        raise
