#!/usr/bin/env python3
"""Finite complete native placement comparison; no scheduler or promotion control."""
from pathlib import Path
import os,sys,json,subprocess,time,selectors,signal,zipfile,shutil,statistics,datetime
R=Path('/workspaces/repository');D=Path(__file__).parent
SDK=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
WORK=SDK.parent/'mathlib4'
STOCK=R/'artifacts/lean-service-lifecycle-2026-10-13/build1/Lean49PreparedBranches'
GATED=Path('/tmp/gpu-smt-experiment030-build/candidate')
SOURCE=R/'artifacts/lean-gpu-checking-2026-10-13/experiment022/source1'
sys.path.insert(0,str(SOURCE))
from analyze_lean_preparation import interpret
from lean_capture_warm import ResourceCapture
def environment():
 env=dict(os.environ)
 for name in list(env):
  if name.startswith(('LEAN_GPU_','LEAN_NATIVE_CLOSURE_','FARKAS_','GPU_SMT_')) or name=='LEAN_NUM_THREADS':env.pop(name,None)
 env['LEAN_SYSROOT']=str(SDK)
 env['LEAN_PATH']=json.loads((R/'artifacts/lean-native-boundary-2026-10-11/experiment012/preflight2/branch-minif2f-first32/receipt.json').read_text())['environment']['LEAN_PATH']
 env.update(GPU_SMT_PARENT_PREPARATION='header-cache',GPU_SMT_PARENT_SEED_FIRST_HEADER='1')
 return env
def run_phase(folder,label,method,input_file,mapping,observer):
 env=environment();env['GPU_SMT_WORKER_RETIRE_AFTER']=str(len(mapping))
 binary = Path('/tmp/gpu-smt-experiment030-build/profile-'+('candidate' if method=='gated' else 'warm')) if observer else (GATED if method=='gated' else STOCK)
 command=[str(binary),'warm-pool',str(input_file),str(SDK),'4']
 raw=folder/(label+'.stdout.bin');err=folder/(label+'.stderr.bin')
 begin=time.monotonic_ns();records={};admitted={};events=[];pending=b''
 with raw.open('xb') as stdout,err.open('xb') as stderr:
  proc=subprocess.Popen(command,cwd=WORK,env=env,stdout=subprocess.PIPE,stderr=stderr,start_new_session=True,bufsize=0)
  (folder/(label+'.command.json')).write_text(json.dumps({'command':command,'pid':proc.pid,'mapping':mapping,'begin_ns':begin,'native_defaults':'unset LEAN_NUM_THREADS; original300s/unlimited native memory'},indent=2)+'\n')
  selector=selectors.DefaultSelector();selector.register(proc.stdout,selectors.EVENT_READ)
  try:
   eof=False
   while not eof:
    if observer:observer.sample()
    for key,_ in selector.select(.1):
     chunk=os.read(key.fd,65536)
     if not chunk:eof=True;break
     stdout.write(chunk);pending+=chunk
     while b'\n' in pending:
      line,pending=pending.split(b'\n',1)
      if not line.strip():continue
      try:event=json.loads(line)
      except ValueError:events.append({'non_json_stdout':line.decode(errors='replace')});continue
      now=time.monotonic_ns();event['observer_monotonic_ns']=now
      summary={k:v for k,v in event.items() if k not in ('stdout_hex','native_response')}
      summary['raw_stdout_file']=raw.name;summary['parsed_event_number']=len(events)
      events.append(summary)
      kind=event.get('event')
      ordinal=event.get('ordinal') if method=='shared' else event.get('source_index')
      if kind=='admitted':admitted[ordinal]=event['monotonic_ns']
      if kind=='candidate':
       if ordinal not in range(len(mapping)):raise ValueError('native ordinal outside original phase input')
       ready=event.get('response_ready',bool(event.get('stdout_hex')))
       native=event.get('native_response') if method=='shared' else (json.loads(bytes.fromhex(event['stdout_hex'])) if ready else None)
       records[mapping[ordinal]]={'ordinal':mapping[ordinal],'native_response':native,'status':'response' if ready else 'unknown',
        'admission_monotonic_ns':admitted[ordinal],'terminal_observed_monotonic_ns':now,
        'native_event':summary,'phase':label,'elapsed_seconds':(now-admitted[ordinal])/1e9}
   code=proc.wait()
  except BaseException:
   try:os.killpg(proc.pid,signal.SIGKILL)
   except ProcessLookupError:pass
   proc.wait();raise
  finally:
   selector.close();proc.stdout.close()
 end=time.monotonic_ns()
 (folder/(label+'.terminal.json')).write_text(json.dumps({'returncode':code,'begin_ns':begin,'end_ns':end,'returned':len(records),'remaining_stdout_bytes':len(pending)},indent=2)+'\n')
 (folder/(label+'.events.jsonl')).write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events))
 return records,code
def summarize(rows,inputs):
 counts={};outcomes={};issues=[]
 for ordinal,row in rows.items():
  native=(row.get('native_response') or {}).get('native') or {}
  if row['status']=='response' and native.get('index')!=inputs[ordinal]['index']:issues.append({'native_index_mismatch':ordinal})
  outcome=interpret(native.get('response'),{'status':row['status'],'error':None},None,'warm')['outcome']
  basic=outcome if outcome in ('complete','rejected','incomplete') else 'operational'
  row.update(source_index=inputs[ordinal]['index'],outcome=outcome,basic=basic)
  outcomes[row['source_index']]=basic;counts[basic]=counts.get(basic,0)+1
 lat=sorted(row['elapsed_seconds'] for row in rows.values())
 return {'returned':len(rows),'expected':len(inputs),'counts':counts,'basic_by_index':outcomes,'issues':issues,
  'latency_seconds':{'median':statistics.median(lat),'p95':lat[int(.95*(len(lat)-1))],'p99':lat[int(.99*(len(lat)-1))]}} if lat else {'returned':0,'expected':len(inputs),'counts':counts,'issues':issues}
def archive(folder):
 target=folder.with_suffix('.zip')
 with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED) as z:
  for p in folder.rglob('*'):
   if p.is_file():z.write(p,p.relative_to(folder.parent))
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  for p in folder.rglob('*'):
   if p.is_file():assert z.read(str(p.relative_to(folder.parent)))==p.read_bytes()
 assert folder.resolve().is_relative_to(D.resolve())
 shutil.rmtree(folder)
def capture(out,label,method,source,profile=False):
 begin=time.monotonic_ns();folder=out/label;folder.mkdir()
 observer=ResourceCapture(folder) if profile else None
 (folder/'input.jsonl').write_bytes(source.read_bytes())
 lines=source.read_bytes().splitlines();inputs=[json.loads(x) for x in lines]
 rows,code=run_phase(folder,'primary',method,folder/'input.jsonl',list(range(len(inputs))),observer)
 fallback=[]
 if method=='shared' and code!=0:
  # Actual process failure, never a source-ID allowlist. Keep the shared partial
  # run and execute every unreturned original candidate through the native pool.
  fallback=[i for i in range(len(inputs)) if i not in rows]
  (folder/'fallback-input.jsonl').write_bytes(b'\n'.join(lines[i] for i in fallback)+b'\n')
  if fallback:
   recovered,fallback_code=run_phase(folder,'native-fallback','warm',folder/'fallback-input.jsonl',fallback,observer)
   rows.update(recovered)
   if fallback_code:code=fallback_code
   elif len(rows)==len(inputs):code=0
 if observer:observer.close()
 analysis=summarize(rows,inputs)
 (folder/'results.jsonl').write_text(''.join(json.dumps(rows[i],ensure_ascii=False)+'\n' for i in sorted(rows)))
 end=time.monotonic_ns()
 terminal={'method':method,'profile':profile,'begin_ns':begin,'end_ns':end,'whole_seconds':(end-begin)/1e9,'returncode':code,
  'fallback_indices':fallback,'shared_returned':len(inputs)-len(fallback) if method=='shared' else None,
  'whole_boundary':'input persistence, native initialization/preparation/evaluation, native worker failure/replacement, observer/output/EOF/cleanup; ZIP after clock',
  'host_load_end':os.getloadavg(),'expected_attempts':len(inputs)}
 (out/(label+'.terminal.json')).write_text(json.dumps(terminal,indent=2)+'\n')
 (out/(label+'.analysis.json')).write_text(json.dumps(analysis,indent=2)+'\n')
 print(json.dumps({'label':label,**terminal,'counts':analysis['counts'],'returned':analysis['returned']}),flush=True)
 if code==0 and analysis['returned']==len(inputs) and not analysis['issues']:archive(folder)
 else:raise RuntimeError('incomplete/invalid native cell; original partial retained')
 return analysis
def main():
 os.sched_setaffinity(0,{0,1,2,3})
 action=sys.argv[1]
 if action=='preflight':
  source=D/'preflight1/input.jsonl';out=D/'preflight1/results';out.mkdir()
  for method in ['gated','warm']:capture(out,method,method,source,True)
 elif action=='full':
  source=R/'artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs/proofnet/input.jsonl'
  out=D/'full1-proofnet';out.mkdir()
  for rep,order in enumerate([('warm','gated'),('gated','warm'),('warm','gated')]):
   pair={}
   for method in order:pair[method]=capture(out,f'rep{rep}-{method}',method,source)
   if pair['warm']['basic_by_index']!=pair['gated']['basic_by_index']:raise RuntimeError('full paired native outcomes differ; all raw retained')
  for method in ['gated','warm']:capture(out,'profile-'+method,method,source,True)
  (out/'acquisition-completed.md').write_text('All8 planned cells terminal. Result review required; no automatic speedup/RQ promotion.\n')
 else:raise ValueError('preflight or full')
if __name__=='__main__':main()
