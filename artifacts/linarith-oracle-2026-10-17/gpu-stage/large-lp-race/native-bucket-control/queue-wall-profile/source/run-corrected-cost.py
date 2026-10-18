"""Clean arithmetic-family wall profiling through the unchanged native collector.

The primary run-batch entrypoint remains untouched while its active paired
series completes. Diagnostic clocks have their own denominators.
"""
from pathlib import Path
import sys,os,json
D=Path(__file__).resolve().parent
# Pooled exact-fallback dispatch uses the primary's declared LP row gate.
# Missing it previously caused caught numerical panics followed by Lean
# fallback, producing valid verdicts with invalid timing attribution.
if '--cost-profile' in sys.argv:
    root=Path(sys.argv[sys.argv.index('--cost-root')+1]) if '--cost-root' in sys.argv else Path('/tmp/gpu-smt-linarith-oracle-20261017')
    receipt=root/'build-cost-receipt.json'
    if receipt.exists() and json.loads(receipt.read_text()).get('pooled'):
        value=os.environ.get('GPU_ARITHMETIC_RACE_MIN_ROWS')
        if value is None or not value.isdecimal() or int(value)<1:
            raise RuntimeError('Pooled profile requires the matched primary GPU_ARITHMETIC_RACE_MIN_ROWS before collection')
p=D/'run-batch.py'
source=p.read_text()
old="ns['EXTRA_IMPORT']='import GpuArithmetic.Stages\\\\nimport GpuArithmetic.Baseline\\\\nimport GpuArithmetic.Oracle\\\\nimport GpuArithmetic.CostOracle\\\\n'"
new="ns['EXTRA_IMPORT']='import GpuArithmetic.CostBaseline\\\\n' if name=='fast-hybrid' else 'import GpuArithmetic.CostOracle\\\\n'"
assert old in source, 'review corrected-family header against active collector'
source=source.replace(old,new,1)
exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
