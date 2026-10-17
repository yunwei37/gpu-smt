"""Run only the user-admitted 1,000-source arithmetic experiment, never the old matrices.
Sequential real native trials; no agents, scheduler, resource tuning or polling loop.
"""
from pathlib import Path
import subprocess, sys, json
R=Path('/workspaces/repository')
U=Path('/tmp/gpu-smt-linarith-oracle-20261017')
PY=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python')
RUN=R/'bench/lean-native/linarith-oracle/run-comparison.py'
OUT=U/'matched-top1000'
OUT.mkdir(exist_ok=False)
orders=[
 ['fast-hybrid','oracle','native','fast-highs'],
 ['fast-highs','native','oracle','fast-hybrid'],
 ['oracle','fast-hybrid','fast-highs','native']]
def run(label,methods,diagnostic=False):
 cmd=[str(PY),str(RUN),'--out',str(OUT/label),'--methods',*methods]
 if diagnostic:cmd.append('--diagnostic')
 with (OUT/(label+'.log')).open('wb') as log:
  subprocess.run(cmd,cwd=R,check=True,stdout=log,stderr=subprocess.STDOUT)
for rep,order in enumerate(orders,1):
 run('primary%d'%rep,order)
 # Separate full native-stage measurement after the first performance block.
 if rep==1:run('native-stages',['profile'],True)
print('All declared native timing and stage captures reached terminal; result review required.',flush=True)
