from pathlib import Path
import json,subprocess,os,resource,time,datetime
D=Path(__file__).parent;T=Path('/tmp/gpu-smt-goedel427-20261014')
row=next(json.loads(s) for s in (D/'input.jsonl').read_text().splitlines() if json.loads(s)['proof_id']=='Proof_02269')
folder=D/'native-eof-original02269';folder.mkdir()
(folder/'original-source.lean').write_text(row['code'])
lines=row['code'].splitlines();i=0;imports=[]
while i<len(lines) and (not lines[i].strip() or lines[i].strip().startswith('import ')):
 if lines[i].strip():imports.append(lines[i])
 i+=1
header='\n'.join(imports);body='\n'.join(lines[i:])
payload=(json.dumps({'cmd':header},ensure_ascii=False)+'\n\n'+json.dumps({'cmd':body,'env':0,'gc':True},ensure_ascii=False)+'\n\n').encode()
(folder/'native-input.jsonl').write_bytes(payload)
config=json.loads((D/'native-library.json').read_text())
env=dict(os.environ);env['PATH']=str(T/'lean-4.27.0-linux/bin')+os.pathsep+env['PATH']
env['LEAN_SERVER_NATIVE_DYNLIB']=config['load_manifest']
env['LD_LIBRARY_PATH']=os.pathsep.join(config['library_paths']+([env['LD_LIBRARY_PATH']] if env.get('LD_LIBRARY_PATH') else []))
command=['lake','env',str(T/'repl-kimina-native-gc/.lake/build/bin/repl')]
def prepare():
 resource.setrlimit(resource.RLIMIT_AS,(12*1024**3,12*1024**3))
 resource.setrlimit(resource.RLIMIT_CORE,(0,0))
 os.sched_setaffinity(0,{0,1,2,3})
started=time.monotonic()
with (folder/'stdout.raw').open('wb') as out,(folder/'stderr.raw').open('wb') as err:
 p=subprocess.Popen(command,cwd=T/'mathlib4',env=env,stdin=subprocess.PIPE,stdout=out,stderr=err,preexec_fn=prepare,start_new_session=True)
 try:p.communicate(payload,timeout=300);timeout=False
 except subprocess.TimeoutExpired:p.kill();p.wait();timeout=True
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,'cwd':str(T/'mathlib4'),'source_index':row['index'],'original_author':row['author'],'returncode':p.returncode,'timeout':timeout,'elapsed_s':time.monotonic()-started,'scope':'actual single native EOF discriminator with matching12GiBAS/300s timeout/0-3affinity; stderr file differs from unread source service PIPE, not a performance result'}
(folder/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record),flush=True)
print((folder/'stderr.raw').read_text(errors='replace')[-4000:],flush=True)
