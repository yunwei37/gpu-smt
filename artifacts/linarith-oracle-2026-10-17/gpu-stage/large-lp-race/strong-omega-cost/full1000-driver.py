from pathlib import Path
import os,resource,subprocess,json,datetime
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-omega-cost';U=Path('/tmp/gpu-smt-linarith-oracle-20261017/strong-omega-cost')
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
q=json.loads((A/'corrected-qualification-numeric-analysis.json').read_text())
assert not q['fidelity']['verdict_differences']and not q['fidelity']['non_message_differences']
for method in ['native','direct']:
 assert q['numeric_CPU'][method]['reaped_children']>0
 assert q['numeric_CPU'][method]['CPU_seconds_exclusive_completed_phases'].get('lp_float_solve',0)>0
 assert q['external_service_CPU'][method]['retirement_records']
 assert q['methods'][method]['counts']=={'complete':7,'rejected':8}
(A/'full1000-admission.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'qualification':'corrected-qualification-numeric-analysis.json','normal_CPU_observer_control':'qualification-observer-analysis.json',
 'same_dual_backend_both_frontends':True,'private_default_Cargo_target':True,'scope':'One full own-clock native/direct diagnostic pair, not a new primary speedup or GPU matrix. Explicitly excludes initial historical-fast-hybrid native route.'},indent=2)+'\n')
input=R/'artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl';assert len(input.read_text().splitlines())==1000
for frontend in ['native','direct']:
 out=U/('full1000-'+frontend)
 env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U),GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1',
 GPU_SMT_NATIVE_OMEGA_CONTROL='1',GPU_SMT_OMEGA_CONTROL_LOG=str(out/'omega-calls.jsonl'),GPU_SMT_COST_FRONTEND=frontend,
 GPU_ARITHMETIC_NUMERIC_PHASE_LOG=str(out/'numeric-phases.jsonl'))
 cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(A/'run-profile.py'),'--out',str(out),'--input',str(input),'--limit','1000','--width','8','--affinity','4','5','6','7','--native-buckets','--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl','--methods','oracle-highs','--diagnostic']
 print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frontend':frontend,'argv':cmd}),flush=True)
 subprocess.run(cmd,cwd=R,env=env,check=True)
 print(json.dumps({'closed_frontend':frontend,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}),flush=True)
(A/'full1000-terminal.json').write_text(json.dumps({'state':'complete','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
