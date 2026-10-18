from pathlib import Path
D=Path('/workspaces/repository/bench/lean-native/linarith-oracle')
A=Path(__file__).resolve().parent
source=(D/'run-race.py').read_text()
needle="exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})"
assert source.count(needle)==1
# The assembled run-batch program executes a fully expanded comparison source.
batch_exec="exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p),'BATCH':BATCH})"
newclass=(A/'Runner-source.py').read_text()
replacement="s=s.replace('def main():',"+repr(newclass+"def main():")+",1)\n"+batch_exec
patch="assert source.count("+repr(batch_exec)+")==1\nsource=source.replace("+repr(batch_exec)+","+repr(replacement)+",1)\n"
# The GPU dispatcher is the existing independently in-flight implementation.
old="str(R/'bench/lean-native/linarith-oracle/support-proxy.py')"
proxy='/workspaces/repository/artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/async-device-progress/request-sized-vmm/final-drain/support-proxy.py'
patch+="source=source.replace("+repr(old)+","+repr(repr(proxy))+",1)\n"
source=source.replace(needle,patch+needle,1)
exec(compile(source,str(D/'run-race.py'),'exec'),{'__name__':'__main__','__file__':str(D/'run-race.py')})
