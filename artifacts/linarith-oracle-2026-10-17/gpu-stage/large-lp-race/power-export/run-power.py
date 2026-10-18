from pathlib import Path
D=Path('/workspaces/repository/bench/lean-native/linarith-oracle')
import os
frontend=os.environ.get('GPU_SMT_COST_FRONTEND','direct')
if frontend not in ['native','direct','power']:raise ValueError('native/direct frontend')
target='GpuArithmetic.IntegerCostControl'if frontend=='native'else('GpuArithmetic.IntegerCostOracle'if frontend=='direct'else'GpuArithmetic.IntegerPowerOracle')
source=(D/'run-race.py').read_text()
needle="exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})"
assert source.count(needle)==1
batch_exec="exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p),'BATCH':BATCH})"
# Patch only the fully assembled private comparison program.
transforms=[
 ("GpuArithmetic.BatchBaseline", "GpuArithmetic.IntegerCostControl"),
 ("GpuArithmetic.BatchOracle", target),
 ("        old=R/'artifacts/lean-modern-native-compilation-2026-10-14'",
  "        os.environ['GPU_ARITHMETIC_STRONG_PROFILE']='1'\n        old=R/'artifacts/lean-modern-native-compilation-2026-10-14'"),
 ("'oracle.jsonl'","'lean-costs.jsonl.gz'"),
 ("out/'support-calls.jsonl'","out/'support-calls.jsonl.gz'")
]
replacement=''
for old,new in transforms:
 replacement+="assert "+repr(old)+" in s\ns=s.replace("+repr(old)+","+repr(new)+")\n"
replacement+=batch_exec
patch="assert source.count("+repr(batch_exec)+")==1\nsource=source.replace("+repr(batch_exec)+","+repr(replacement)+",1)\n"
patch+="source=source.replace("+repr("str(R/'bench/lean-native/linarith-oracle/support-proxy.py')")+","+repr(repr(str(Path(__file__).resolve().parent/'support-proxy.py')))+",1)\n"
source=source.replace(needle,patch+needle,1)
exec(compile(source,str(D/'run-race.py'),'exec'),{'__name__':'__main__','__file__':str(D/'run-race.py')})
