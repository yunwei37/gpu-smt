from pathlib import Path
import os,resource,subprocess,json,datetime
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-omega-cost';U=Path('/tmp/gpu-smt-linarith-oracle-20261017/strong-omega-cost')
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
receipt=json.loads((A/'build-receipt.json').read_text());assert len(receipt['commands'])==12 and all(x['exit']==0 for x in receipt['commands'])
python='/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python'
input=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/ready-goal-batch/argument-goals/preflight-input.jsonl'
for label,normal in [('normal',True),('profile',False)]:
 out=U/('qualification15-'+label)
 if normal and(out/'terminal.json').exists():
  assert json.loads((out/'terminal.json').read_text())['state']=='complete'
  print('Retain already closed normal control; continue failed diagnostic wrapper',flush=True)
  continue
 env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U.parent/'native-omega-control')if normal else str(U),GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1',
 GPU_SMT_NATIVE_OMEGA_CONTROL='1',GPU_SMT_OMEGA_CONTROL_LOG=str(out/'omega-calls.jsonl'),GPU_SMT_CONTROL_FRONTEND='direct')
 if not normal:env['GPU_ARITHMETIC_NUMERIC_PHASE_LOG']=str(out/'numeric-phases.jsonl')
 script=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/native-omega-control/run-control.py'if normal else A/'run-profile.py'
 cmd=[python,str(script),'--out',str(out),'--input',str(input),'--limit','0','--width','8','--affinity','4','5','6','7','--native-buckets','--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl','--methods',*(['oracle-highs']if normal else['fast-hybrid','oracle-highs'])]
 if not normal:cmd+=['--diagnostic']
 print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd}),flush=True)
 subprocess.run(cmd,cwd=R,env=env,check=True)
(A/'qualification-terminal.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'complete'})+'\n')
