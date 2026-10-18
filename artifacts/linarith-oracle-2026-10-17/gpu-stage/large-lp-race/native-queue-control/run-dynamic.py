from pathlib import Path
D=Path('/workspaces/repository/bench/lean-native/linarith-oracle')
A=Path('/workspaces/repository/artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/native-queue-control')
source=(D/'run-race.py').read_text()
needle="exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})"
assert source.count(needle)==1
old="p=R/'bench/lean-native/linarith-oracle/run-comparison.py'"
patch="assert source.count("+repr(old)+")==1\nsource=source.replace("+repr(old)+","+repr("p=Path("+repr(str(A/'run-comparison-dynamic.py'))+")")+",1)\n"
source=source.replace(needle,patch+needle,1)
exec(compile(source,str(D/'run-race.py'),'exec'),{'__name__':'__main__','__file__':str(D/'run-race.py')})
