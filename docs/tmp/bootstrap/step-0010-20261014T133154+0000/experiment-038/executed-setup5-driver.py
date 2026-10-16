from pathlib import Path
import subprocess,os,json,time,datetime,resource
r=Path('/workspaces/repository');a=r/'artifacts/lean-modern-native-compilation-2026-10-14'
p=Path('/tmp/gpu-smt-native-ref-branches-20261016');b=Path('/tmp/gpu-smt-goedel427-20261014');sdk=b/'lean-4.27.0-linux'
e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038'
env=dict(os.environ);env['PATH']=str(sdk/'bin')+os.pathsep+env['PATH']
env['LEAN_SYSROOT']=str(sdk)
env['LEAN_PATH']=subprocess.check_output([str(sdk/'bin/lake'),'env','printenv','LEAN_PATH'],cwd=b/'mathlib4',env=env,text=True).strip()
config=json.loads((a/'native-library.json').read_text())
env['LEAN_SERVER_NATIVE_DYNLIB']=config['load_manifest']
env['LD_LIBRARY_PATH']=os.pathsep.join([str(p),str(sdk/'lib'),str(sdk/'lib/lean')]+config['library_paths'])
item=json.loads(next((a/'input.jsonl').open()))
header='import Mathlib\nimport Aesop\n'
assert item['code'].startswith(header)
body='\n\n'+item['code'][len(header):]
payload=json.dumps({'cmd':header})+'\n\n'+json.dumps({'cmd':body,'env':0})+'\n\n'
(e/'setup-original-input.json').write_text(json.dumps(item,indent=2)+'\n')
(e/'setup-transport.txt').write_text(payload)
(e/'setup-environment.json').write_text(json.dumps({k:env[k] for k in ['LEAN_PATH','LEAN_SERVER_NATIVE_DYNLIB','LD_LIBRARY_PATH']},indent=2)+'\n')
for label,exe,off in [('branch-off',p/'native-branch-setup',True),('branch-on',p/'native-branch-setup',False)]:
 target=e/('setup5-'+label);target.mkdir(exist_ok=False)
 local=dict(env)
 local['GPU_SMT_MAP_RECEIPT']=str(target/'maps')
 if off:local['GPU_SMT_BRANCH_OFF']='1'
 else:local.pop('GPU_SMT_BRANCH_OFF',None)
 tick=time.monotonic();proc=subprocess.Popen([str(exe)],cwd=b/'mathlib4',env=local,stdin=subprocess.PIPE,stdout=(target/'stdout').open('w'),stderr=(target/'stderr').open('w'),text=True)
 (target/'launch.json').write_text(json.dumps({'command':[str(exe)],'cwd':str(b/'mathlib4'),'pid':proc.pid,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'policy':'one original command; original 300s request deadline retained for finite setup; no full collector or performance claim'},indent=2)+'\n')
 try:
  proc.communicate(payload,timeout=300);state='exited'
 except subprocess.TimeoutExpired:
  proc.terminate();proc.wait();state='original-request-deadline'
 (target/'terminal.json').write_text(json.dumps({'state':state,'exit_code':proc.returncode,'seconds':time.monotonic()-tick},indent=2)+'\n')
 print(label,proc.returncode,time.monotonic()-tick,(target/'stdout').read_text()[-3000:],(target/'stderr').read_text()[-1500:],flush=True)
