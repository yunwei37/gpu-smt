from pathlib import Path
import subprocess,json,os,time,datetime,threading,queue
r=Path('/workspaces/repository');a=r/'artifacts/lean-modern-native-compilation-2026-10-14'
e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/service-integration'
p=Path('/tmp/gpu-smt-native-ref-branches-20261016');b=Path('/tmp/gpu-smt-goedel427-20261014');sdk=b/'lean-4.27.0-linux'
config=json.loads((a/'native-library.json').read_text())
env=dict(os.environ);env['PATH']=str(sdk/'bin')+os.pathsep+env['PATH'];env['LEAN_SYSROOT']=str(sdk)
env['LEAN_PATH']=subprocess.check_output([str(sdk/'bin/lake'),'env','printenv','LEAN_PATH'],cwd=b/'mathlib4',env=env,text=True).strip()
env['LEAN_SERVER_NATIVE_DYNLIB']=config['load_manifest'];env['LD_LIBRARY_PATH']=os.pathsep.join([str(p),str(sdk/'lib'),str(sdk/'lib/lean')]+config['library_paths'])
header='import Mathlib\nimport Aesop\n';items=[]
with (a/'input.jsonl').open() as f:
 for _ in range(4):items.append(json.loads(next(f)))
for item in items:assert item['code'].startswith(header)
payload=json.dumps({'cmd':header})+'\n\n'+''.join(json.dumps({'cmd':'\n\n'+item['code'][len(header):],'env':0,'custom_id':item['proof_id']})+'\n\n' for item in items)
for label,off in [('native-private',False),('native-shared-control',True)]:
 d=e/('concurrent3-'+label);d.mkdir(exist_ok=False);local=dict(env)
 if off:local['GPU_SMT_BRANCH_OFF']='1'
 else:local.pop('GPU_SMT_BRANCH_OFF',None)
 (d/'input.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in items));(d/'transport.txt').write_text(payload)
 started=time.monotonic_ns();proc=subprocess.Popen([str(p/'native-branch-backend')],cwd=b/'mathlib4',env=local,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=(d/'stderr').open('w'),text=True)
 rows=[]
 def read():
  with (d/'stdout').open('w') as out:
   for line in proc.stdout:
    out.write(line);out.flush()
    try:body=json.loads(line);rows.append({'observed_ns':time.monotonic_ns(),'response':body})
    except ValueError:pass
 reader=threading.Thread(target=read);reader.start()
 proc.stdin.write(payload);proc.stdin.close()
 try:proc.wait(timeout=300);state='exited'
 except subprocess.TimeoutExpired:proc.terminate();proc.wait();state='original-request-deadline'
 reader.join()
 (d/'observed-responses.json').write_text(json.dumps(rows,indent=2)+'\n')
 (d/'terminal.json').write_text(json.dumps({'state':state,'exit_code':proc.returncode,'whole_seconds':(time.monotonic_ns()-started)/1e9,'command':[str(p/'native-branch-backend')],'cwd':str(b/'mathlib4'),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'request_window':'four original requests admitted together after prepared header; finite integration, not full matrix','explicit_env':{k:local.get(k) for k in ['LEAN_SYSROOT','LEAN_PATH','LD_LIBRARY_PATH','LEAN_SERVER_NATIVE_DYNLIB','GPU_SMT_BRANCH_OFF']},'reader_note':'one reader owns stdout; main writes/closes stdin and waits only'},indent=2)+'\n')
 print(label,proc.returncode,len(rows),(d/'stderr').read_text()[-1200:],flush=True)
