from pathlib import Path
import os,subprocess,json,shlex,resource,time
R=Path('/workspaces/repository')
A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/native-queue-control'
T=Path('/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing')
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/native-queue-control')
os.sched_setaffinity(0,{4,5,6,7});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
env=dict(os.environ,LEAN_PATH=str(T/'.lake/build/lib/lean'))
replace={str(T/'REPL/Main.lean'):str(A/'Main.lean'),
 str(T/'.lake/build/lib/lean/REPL/Main.olean'):str(U/'Main.olean'),
 str(T/'.lake/build/lib/lean/REPL/Main.ilean'):str(U/'Main.ilean'),
 str(T/'.lake/build/ir/REPL/Main.c'):str(U/'Main.c'),
 str(T/'.lake/build/ir/REPL/Main.c.o.export'):str(U/'Main.c.o.export'),
 str(T/'.lake/build/bin/repl'):str(U/'repl')}
receipts=[]
for trace in ['lib/lean/REPL/Main.trace','ir/REPL/Main.c.o.export.trace','bin/repl.trace']:
 t=json.loads((T/'.lake/build'/trace).read_text())
 command=t['log'][0]['message']
 assert command.startswith('.> '),command[:100]
 args=shlex.split(command[3:])
 args=[replace.get(x,x) for x in args]
 print(json.dumps({'event':'build','trace':trace,'argv':args}),flush=True)
 start=time.monotonic();p=subprocess.run(args,cwd=T,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 receipts.append({'trace':trace,'argv':args,'exit':p.returncode,'seconds':time.monotonic()-start,'output':p.stdout})
 print(p.stdout,flush=True)
 (A/'build-receipt.json').write_text(json.dumps(receipts,indent=2)+'\n')
 if p.returncode:raise SystemExit(p.returncode)
print('BUILD_COMPLETE',flush=True)
