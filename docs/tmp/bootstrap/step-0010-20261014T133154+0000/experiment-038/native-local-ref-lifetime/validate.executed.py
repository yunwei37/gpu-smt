from pathlib import Path
import json,subprocess,datetime,os
r=Path('/workspaces/repository')
n=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/native-local-ref-lifetime'
root=Path('/tmp/gpu-smt-native-local-ref-lifetime-20261017/build')
assert json.loads((n/'build.terminal.json').read_text())['exit_code']==0
sdk=Path('/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux')
cmd=json.loads((n.parent/'native-write-copy/witness-native-command.json').read_text())[0]['command']
cmd=[v.replace('experiment-038/native-write-copy','experiment-038/native-local-ref-lifetime').replace('/tmp/gpu-smt-native-write-copy-20261016','/tmp/gpu-smt-native-local-ref-lifetime-20261017') for v in cmd]
records=[]
for label,command in [('witness-compile',cmd),('witness-run',[str(root.parent/'native-ref-witness')]),('native-check',['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python','-u',str(n/'native-check.executed.py'),str(root),str(n/'native-check'),'plain,private'])]:
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (n/(label+'.stdout')).open('wb') as out,(n/(label+'.stderr')).open('wb') as err:
  z=subprocess.run(command,stdout=out,stderr=err,cwd=r)
 records.append({'label':label,'command':command,'exit_code':z.returncode,'start_utc':utc,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 (n/'validation.commands.json').write_text(json.dumps(records,indent=2)+'\n')
 if z.returncode:raise RuntimeError(label+' failed: '+str(z.returncode))
a=json.loads((n/'native-check/plain/responses.json').read_text())
b=json.loads((n/'native-check/private/responses.json').read_text())
assert a==b
(n/'validation.terminal.json').write_text(json.dumps({'state':'complete','normal_native_responses_equal':True,'original_sources':len(a),'witness_stdout':(n/'witness-run.stdout').read_text(),'scope':'finite qualification only; no performance or independent audit'},indent=2)+'\n')
print('finite qualification complete')
