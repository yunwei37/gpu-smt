from pathlib import Path
D=Path('/workspaces/repository/bench/lean-native/linarith-oracle')
source=(D/'run-race.py').read_text()
needle="exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})"
assert needle in source
source=source.replace(needle,'assert source.count("\'support-calls.jsonl\'")==1\nsource=source.replace("\'support-calls.jsonl\'","\'support-calls.jsonl.gz\'",1)\nassert source.count(".get(name,\'import GpuArithmetic.BatchOracle\\\\\\\\n\')")==1\nsource=source.replace(".get(name,\'import GpuArithmetic.BatchOracle\\\\\\\\n\')",".get(name,\'import GpuArithmetic.BatchBaseline\\\\\\\\n\')",1)'+'\n'+needle,1)
exec(compile(source,str(D/'run-race.py'),'exec'),{'__name__':'__main__','__file__':str(D/'run-race.py')})
