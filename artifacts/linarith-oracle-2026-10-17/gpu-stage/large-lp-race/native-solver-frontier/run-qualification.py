from pathlib import Path
D=Path('/workspaces/repository/bench/lean-native/linarith-oracle')
source=(D/'run-race.py').read_text()
needle="exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})"
inject='assert "[\'fast-hybrid\',\'oracle\',\'oracle-hint\',\'oracle-highs\',\'oracle-gpu\']" in source\nsource=source.replace("[\'fast-hybrid\',\'oracle\',\'oracle-hint\',\'oracle-highs\',\'oracle-gpu\']","[\'fast-hybrid\',\'fast-tiered\',\'fast-highs\',\'oracle\',\'oracle-hint\',\'oracle-highs\',\'oracle-gpu\']",1)\nassert "{\'fast-hybrid\':\'import GpuArithmetic.BatchBaseline\\\\\\\\n\'," in source\nsource=source.replace("{\'fast-hybrid\':\'import GpuArithmetic.BatchBaseline\\\\\\\\n\',","{\'fast-tiered\':\'import GpuArithmetic.BatchBaseline\\\\\\\\n\',\'fast-highs\':\'import GpuArithmetic.BatchBaseline\\\\\\\\n\',\'fast-hybrid\':\'import GpuArithmetic.BatchBaseline\\\\\\\\n\',",1)'
assert needle in source
source=source.replace(needle,inject+'\n'+needle,1)
exec(compile(source,str(D/'run-race.py'),'exec'),{'__name__':'__main__','__file__':str(D/'run-race.py')})
