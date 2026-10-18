from pathlib import Path
import os
D=Path('/workspaces/repository/bench/lean-native/linarith-oracle')
source=(D/'run-race.py').read_text()
needle="exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})"
batch_exec="exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p),'BATCH':BATCH})"
frontend=os.environ.get('GPU_SMT_CONTROL_FRONTEND','native')
if frontend not in ['native','direct']:raise ValueError('native or direct frontend required')
target='GpuArithmetic.IntegerCostControl'if frontend=='native'else'GpuArithmetic.IntegerCostOracle'
transforms=[
 ("        old=R/'artifacts/lean-modern-native-compilation-2026-10-14'",
  "        os.environ['GPU_ARITHMETIC_STRONG_PROFILE']='1'\n        old=R/'artifacts/lean-modern-native-compilation-2026-10-14'"),
 ('GpuArithmetic.BatchBaseline','GpuArithmetic.IntegerCostControl'),
 ('GpuArithmetic.BatchOracle',target),
 ("out/'support-calls.jsonl'","out/'support-calls.jsonl.gz'")
]
replacement=''
for old,new in transforms:replacement+="assert "+repr(old)+" in s\ns=s.replace("+repr(old)+","+repr(new)+")\n"
target="        return await super().cell(rep,name,**kwargs)"
extra="""        if name=='fast-hybrid':
            if os.environ.get('GPU_SMT_STOCK_DEFAULT_TIERED')=='1':
                os.environ.pop('FARKAS_EXTERNAL_CPU_HYBRID',None)
            Path(os.environ['GPU_SMT_STOCK_ENGINE_RECEIPT']).write_text(json.dumps({'native_binary':os.environ.get('FARKAS_NATIVE_BIN'),'hybrid_override':os.environ.get('FARKAS_EXTERNAL_CPU_HYBRID'),'scope':'Actual inherited environment immediately before native worker creation; source selects tiered when override absent.'},indent=2)+'\\n')
"""+target
replacement+="assert "+repr(target)+" in s\ns=s.replace("+repr(target)+","+repr(extra)+",1)\n"
replacement+=batch_exec
patch="assert source.count("+repr(batch_exec)+")==1\nsource=source.replace("+repr(batch_exec)+","+repr(replacement)+",1)\n"
assert source.count(needle)==1
source=source.replace(needle,patch+needle,1)
exec(compile(source,str(D/'run-race.py'),'exec'),{'__name__':'__main__','__file__':str(D/'run-race.py')})
