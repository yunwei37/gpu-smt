from pathlib import Path
import os,subprocess,resource
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
p=Path('/workspaces/repository')
u=Path('/tmp/gpu-smt-linarith-oracle-20261017/two-sided-oracle')
env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(u),GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1')
cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(p/'bench/lean-native/linarith-oracle/run-race.py'),'--input',str(p/'artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl'),'--limit','1000','--width','8','--affinity','0','1','2','3','--native-buckets','--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl','--out',str(u/'full1000-reversed'),'--methods','oracle-highs','fast-hybrid']
subprocess.run(cmd,cwd=p,env=env,check=True)
