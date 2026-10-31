#!/usr/bin/env python3
"""No-declaration replay controls and user+kernel import profile."""
import importlib.util,fcntl,os,json
from pathlib import Path
base=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/v2')
spec=importlib.util.spec_from_file_location('measurement',base/'measure.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with open(m.BASE/'pcore.lock','a') as lock:
    print('waiting shared P-core lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX)
    os.sched_setaffinity(0,set(range(8)))
    print('acquired shared P-core lock',flush=True)
    for i,r in enumerate(m.small):
        target=base/'replay-oleans'/f'ImportOnly{i}.olean'
        if not target.exists():target.symlink_to(base/'artifacts'/f'imports-{i:02d}-0.olean')
        m.measure(f'empty-replay-{i:02d}',[str(m.SDK/'bin/leanchecker'),'-v',f'ImportOnly{i}'],90,dict(mode='empty_replay',module=r['module']))
    src=m.ROOT/'MathlibOnly.lean'
    m.measure('perf-all-mathlib',['perf','record','-F','199','-e','cycles','--call-graph','dwarf,8192','-o',str(base/'perf-all-mathlib.data'),'--']+m.lean_args(src,'perf-all-mathlib'),120,dict(mode='perf',module='mathlib-user-and-kernel'))
    (base/'controls-terminal.json').write_text(json.dumps(dict(status='completed')))
