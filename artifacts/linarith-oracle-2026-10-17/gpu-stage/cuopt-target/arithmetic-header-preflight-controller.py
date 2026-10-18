from pathlib import Path
import subprocess,json,resource,os,datetime
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{0,1,2,3})
r=Path('/workspaces/repository');q=Path('/tmp/gpu-smt-linarith-oracle-20261017/batch-oracle')
py='/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python'
src=q/'direct-feasibility-native24-input.jsonl'
steps=[
 [py,str(q/'run-batch-stacked-control.py'),'--out',str(q/'header-stacked24'),'--input',str(src),'--methods','fast-hybrid','--affinity','0','1','2','3'],
 [py,str(r/'bench/lean-native/linarith-oracle/run-batch.py'),'--out',str(q/'header-clean24'),'--input',str(src),'--methods','fast-hybrid','oracle','oracle-highs','--affinity','0','1','2','3']]
out=[]
for i,argv in enumerate(steps):
 with (q/('header-preflight-step%d.log'%i)).open('w')as log:
  begin=datetime.datetime.now(datetime.timezone.utc).isoformat()
  code=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT).returncode
 out.append({'step':i,'argv':argv,'start':begin,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':code})
 (q/'header-preflight-controller-terminal.json').write_text(json.dumps({'finished_steps':out,'all_planned_complete':len(out)==len(steps)},indent=2)+'\n')
 print('PREFLIGHT_STEP_ENDED',i,code,flush=True)
 if code:raise SystemExit(code)
