"""Clean arithmetic-family wall profiling through the unchanged native collector.

The primary run-batch entrypoint remains untouched while its active paired
series completes. Diagnostic clocks have their own denominators.
"""
from pathlib import Path
import sys
D=Path(__file__).resolve().parent
p=D/'run-batch.py'
source=p.read_text()
old="ns['EXTRA_IMPORT']='import GpuArithmetic.Stages\\\\nimport GpuArithmetic.Baseline\\\\nimport GpuArithmetic.Oracle\\\\nimport GpuArithmetic.CostOracle\\\\n'"
new="ns['EXTRA_IMPORT']='import GpuArithmetic.CostBaseline\\\\n' if name=='fast-hybrid' else 'import GpuArithmetic.CostOracle\\\\n'"
assert old in source, 'review corrected-family header against active collector'
source=source.replace(old,new,1)
exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
