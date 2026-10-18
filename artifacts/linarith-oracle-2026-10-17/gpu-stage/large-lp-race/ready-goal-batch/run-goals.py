from pathlib import Path
import os
D=Path('/workspaces/repository/bench/lean-native/linarith-oracle')
source=(D/'run-race.py').read_text()
needle="exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})"
batch_exec="exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p),'BATCH':BATCH})"
frontend=os.environ.get('GPU_SMT_CONTROL_FRONTEND','native')
if frontend not in ['native','direct']:raise ValueError('native or direct frontend required')
target='GpuArithmetic.GoalBatchOracle'
transforms=[
 ('GpuArithmetic.BatchBaseline','GpuArithmetic.IntegerControl'),
 ('GpuArithmetic.BatchOracle',target),
 ("out/'support-calls.jsonl'","out/'support-calls.jsonl.gz'")
]
replacement=''
for old,new in transforms:replacement+="assert "+repr(old)+" in s\ns=s.replace("+repr(old)+","+repr(new)+")\n"
replacement+=batch_exec
patch="assert source.count("+repr(batch_exec)+")==1\nsource=source.replace("+repr(batch_exec)+","+repr(replacement)+",1)\n"
assert source.count(needle)==1
source=source.replace(needle,patch+needle,1)
exec(compile(source,str(D/'run-race.py'),'exec'),{'__name__':'__main__','__file__':str(D/'run-race.py')})
