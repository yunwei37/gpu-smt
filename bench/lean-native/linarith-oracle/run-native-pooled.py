"""Strong native control with concurrent daemon reuse, without the AST oracle.

Only the namespace of native round-trip clients changes. Use the unchanged
pinned native hybrid binary, same original source, same baseline tactics.
The inherited fast-hybrid label is retained in raw collector rows.
"""
from pathlib import Path
D=Path(__file__).resolve().parent;p=D/'run-batch.py'
source=p.read_text()
source=source.replace("BATCH=Path('/tmp/gpu-smt-linarith-oracle-20261017/batch-oracle')","BATCH=Path('/tmp/gpu-smt-linarith-oracle-20261017/race-oracle-pooled')",1)
old=r"{'fast-hybrid':'import GpuArithmetic.Baseline\\n',"
new=r"{'fast-hybrid':'import GpuArithmetic.BatchBaseline\\n',"
assert old in source
source=source.replace(old,new,1)
needle=r"\n        if name.startswith('fast-'):"+chr(34)+")"
replacement=r"\n        if name.startswith('fast-'):\n            os.environ['GPU_ARITHMETIC_BATCH']='1'"+chr(34)+")"
assert needle in source
source=source.replace(needle,replacement,1)
exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
