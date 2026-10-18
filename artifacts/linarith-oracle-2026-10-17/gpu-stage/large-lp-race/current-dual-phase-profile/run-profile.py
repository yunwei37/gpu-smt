from pathlib import Path
D=Path('/workspaces/repository/bench/lean-native/linarith-oracle')
source=(D/'run-race.py').read_text()
needle="exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})"
assert source.count(needle)==1
batch_exec="exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p),'BATCH':BATCH})"
# Patch only the fully assembled private comparison program.
transforms=[
 ("GpuArithmetic.BatchBaseline", "GpuArithmetic.CostBaseline"),
 ("GpuArithmetic.BatchOracle", "GpuArithmetic.CostOracle"),
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
source=source.replace(needle,patch+needle,1)
exec(compile(source,str(D/'run-race.py'),'exec'),{'__name__':'__main__','__file__':str(D/'run-race.py')})
