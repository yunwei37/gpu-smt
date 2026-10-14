"""Finite complete-source comparison using the official native frontend/export.

Run one context per process, sequentially. Resume only terminal complete cells;
failed/partial directories remain intact and require a fresh output root.
"""
import argparse,collections,datetime,hashlib,importlib.util,json,os,pathlib,resource,shutil,signal,subprocess,time

def file_hash(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()

def analyze(folder, rows):
    records=[json.loads(line) for line in (folder/'stdout.jsonl').read_text().splitlines()]
    jobs=[x for x in records if 'index' in x]
    if [x['index'] for x in jobs] != [x['index'] for x in rows]:
        raise RuntimeError('missing or reordered original inputs; retain incomplete cell')
    if not records or records[-1].get('finished') != len(rows):
        raise RuntimeError('missing complete native EOF record')
    outcomes=collections.Counter()
    archive_ns=sum(int(x.get('preparation_archive_ns',0)) for x in records)
    projection=[]
    for job in jobs:
        r=job['result'];code=r['backend_code']
        outcome=('operational' if code==3 else 'accepted' if r['accepted'] else
                 'rejected' if r['has_errors'] or code==1 else 'incomplete' if r['has_sorry'] else 'unknown')
        outcomes[outcome]+=1
        if not job['cached']:archive_ns+=int(r.get('archive_ns',0))
        projection.append({'index':job['index'],'outcome':outcome,'source_sha256':next(x['source_sha256'] for x in rows if x['index']==job['index'])})
    result={'attempts':len(jobs),'outcomes':dict(outcomes),'archive_seconds':archive_ns/1e9,
            'candidate_rows':projection,'scope':'complete source outcomes; not diagnostic-text or mathematical equivalence proof'}
    (folder/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

def main():
    p=argparse.ArgumentParser()
    for key in ['inputs','native','backend','sysroot','workspace','out']:
        p.add_argument('--'+key,type=pathlib.Path,required=True)
    paths=p.add_mutually_exclusive_group(required=True)
    paths.add_argument('--lean-path')
    paths.add_argument('--lean-path-file',type=pathlib.Path)
    p.add_argument('--cpus',default='13,14,15,16')
    p.add_argument('--repetitions',type=int,default=3)
    p.add_argument('--profiles',action='store_true')
    p.add_argument('--contexts',nargs='*',help='explicit preflight only; omit for all24 declared contexts')
    a=p.parse_args()
    if a.lean_path_file:a.lean_path=a.lean_path_file.read_text().strip()
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    cpus={int(x) for x in a.cpus.split(',')}
    if not cpus <= os.sched_getaffinity(0):raise RuntimeError('requested unavailable CPU set')
    os.sched_setaffinity(0,cpus)
    a.out.mkdir(parents=True,exist_ok=True)
    original=[json.loads(x) for x in (a.inputs/'jobs.jsonl').read_text().splitlines()]
    groups={}
    for r in original:
        if a.contexts and r['base'] not in a.contexts:continue
        item=dict(r,input=str((a.inputs/r['input']).resolve()))
        if file_hash(pathlib.Path(item['input']))!=r['source_sha256']:raise RuntimeError('source bytes changed')
        groups.setdefault(r['base'],[]).append(item)
    if not groups:raise RuntimeError('no original context')
    for base,rows in groups.items():
        if file_hash(a.workspace/base)!=rows[0]['original_sha256']:raise RuntimeError('original context bytes changed')
    env=dict(os.environ,LEAN_SYSROOT=str(a.sysroot),LEAN_PATH=a.lean_path,
             PATH=str(a.sysroot/'bin')+':'+os.environ.get('PATH',''),PYTHONDONTWRITEBYTECODE='1')
    env.pop('LEAN_NUM_THREADS',None)
    hashes={str(x):file_hash(x) for x in [a.native,a.backend,a.inputs/'jobs.jsonl']}
    receipt=a.out/'execution.json'
    current={'arguments':vars(a),'hashes':hashes,'cpu_set':sorted(cpus),'contexts':list(groups),
             'attempts_per_condition':sum(map(len,groups.values())),'native_runtime':'default LEAN_NUM_THREADS unset'}
    serial=json.loads(json.dumps(current,default=str))
    if receipt.exists():
        if json.loads(receipt.read_text())!=serial:raise RuntimeError('resume source/config differs')
    else:
        receipt.write_text(json.dumps(serial,indent=2)+'\n')
        shutil.copy2(__file__,a.out/'executed-runner.py')
    metrics_spec=importlib.util.spec_from_file_location('resources',pathlib.Path(__file__).parent/'lean_capture_warm.py')
    metrics=importlib.util.module_from_spec(metrics_spec);metrics_spec.loader.exec_module(metrics)
    conditions=[(f'rep{rep}',mode,False) for rep in range(a.repetitions)
                for mode in (['native-full','external-prefix'] if rep%2==0 else ['external-prefix','native-full'])]
    if a.profiles:conditions += [('profile',mode,True) for mode in ['external-prefix','native-full']]
    for repeat,mode,profile in conditions:
        for c,(base,rows) in enumerate(groups.items()):
            folder=a.out/f'{repeat}-ctx{c:02d}-{mode}'
            if (folder/'terminal.json').exists() and (folder/'analysis.json').exists():
                if json.loads((folder/'terminal.json').read_text())['returncode']==0:
                    print('reuse complete',folder.name,flush=True);continue
            if folder.exists():raise RuntimeError('preserve partial/failed condition: '+str(folder))
            folder.mkdir();(folder/'inputs.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
            command=['/usr/bin/time','-v','-o',str((folder/'process-time.txt').resolve()),
                str(a.native),mode,str((folder/'inputs.jsonl').resolve()),str((folder/'witnesses').resolve()),str(a.sysroot),str(a.backend)]
            (folder/'command.json').write_text(json.dumps({'command':command,'cwd':str(a.workspace),
                'LEAN_PATH':a.lean_path,'cpu_set':sorted(cpus),'load':os.getloadavg(),'hashes':hashes},indent=2)+'\n')
            begin=time.monotonic();start=datetime.datetime.now(datetime.timezone.utc).isoformat()
            sampler=metrics.ResourceCapture(folder) if profile else None
            with (folder/'stdout.jsonl').open('xb') as out,(folder/'stderr.txt').open('xb') as err:
                proc=subprocess.Popen(command,cwd=a.workspace,env=env,stdout=out,stderr=err,start_new_session=True)
                def stop(signum,frame):
                    os.killpg(proc.pid,signal.SIGKILL)
                    raise KeyboardInterrupt
                old={s:signal.signal(s,stop) for s in [signal.SIGINT,signal.SIGTERM]}
                try:
                    if sampler:
                        while True:
                            sampler.sample()
                            try:
                                returncode=proc.wait(timeout=1)
                                break
                            except subprocess.TimeoutExpired:pass
                    else:returncode=proc.wait()
                    if returncode and mode == 'external-prefix':
                        # An unexportable prefix before any candidate is a
                        # native-fallback boundary, not a missing corpus cell.
                        out.flush();err.flush()
                        output=(folder/'stdout.jsonl').read_text()
                        captured=[json.loads(line) for line in output.splitlines() if line.strip()]
                        diagnostics=(folder/'stderr.txt').read_bytes()
                        unsupported=(b'unsafe and partial definitions are not supported' in diagnostics or
                                     (b'PANIC at dumpConstant' in diagnostics and b'not found in environment' in diagnostics))
                        if unsupported and not any('index' in row for row in captured):
                            fallback={'event':'unsupported_prefix_native_fallback',
                                      'initial_returncode':returncode,
                                      'initial_elapsed_seconds':time.monotonic()-begin,
                                      'original_prefix_stdout_bytes':(folder/'stdout.jsonl').stat().st_size,
                                      'original_prefix_stderr_bytes':(folder/'stderr.txt').stat().st_size,
                                      'reason':'native exporter cannot represent prefix; no candidate processed',
                                      'native_and_backend_unchanged':True,
                                      'all_original_source_inputs_retained':True}
                            fallback_command=list(command)
                            fallback_command[3]=str((folder/'native-fallback-process-time.txt').resolve())
                            fallback_command[5]='native-full'
                            fallback['command']=fallback_command
                            (folder/'native-fallback.json').write_text(json.dumps(fallback,indent=2)+'\n')
                            out.write((json.dumps(fallback)+'\n').encode());out.flush()
                            # Keep the same resource sampler alive across both
                            # native processes. Whole clock includes both attempts.
                            proc=subprocess.Popen(fallback_command,cwd=a.workspace,env=env,
                                                  stdout=out,stderr=err,start_new_session=True)
                            if sampler:
                                while True:
                                    sampler.sample()
                                    try:
                                        returncode=proc.wait(timeout=1)
                                        break
                                    except subprocess.TimeoutExpired:pass
                            else:returncode=proc.wait()
                            fallback['native_fallback_returncode']=returncode
                            fallback['complete_condition_elapsed_seconds']=time.monotonic()-begin
                            (folder/'native-fallback.json').write_text(json.dumps(fallback,indent=2)+'\n')
                finally:
                    for s,h in old.items():signal.signal(s,h)
                    if sampler:sampler.close()
            terminal={'returncode':returncode,'whole_seconds':time.monotonic()-begin,'start_utc':start,
                      'finish_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':base,'profile':profile,
                      'scope':'process start through complete frontend/backend EOF and process exit, lossless archival included'}
            (folder/'terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
            if returncode:raise RuntimeError('native/backend condition failed; all raw retained')
            summary=analyze(folder,rows)
            print(json.dumps(dict(cell=folder.name,seconds=terminal['whole_seconds'],outcomes=summary['outcomes'])),flush=True)
    (a.out/'acquisition-completed.txt').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')

if __name__=='__main__':main()
