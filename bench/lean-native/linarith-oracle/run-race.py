"""Matched native/CPU/GPU experiment for size-gated cancellable speculation.

oracle-hint is the CPU-only mechanism ablation; oracle-gpu adds GPU racing.
Both use identical large-LP eligibility and exact CPU work. The legacy name
is retained solely to reuse the unchanged source-native batch collector.
"""
from pathlib import Path
import os
D=Path(__file__).resolve().parent
p=D/'run-batch.py';source=p.read_text()
root=Path(os.environ.get('GPU_ARITHMETIC_RACE_ROOT','/tmp/gpu-smt-linarith-oracle-20261017/race-oracle-pooled'))
source=source.replace("BATCH=Path('/tmp/gpu-smt-linarith-oracle-20261017/batch-oracle')","BATCH=Path("+repr(str(root))+")",1)
needle="        if name not in ['oracle-highs','oracle-gpu']:"
insert="""        os.environ['GPU_ARITHMETIC_RACE_WORKER']=str(BATCH/'farkas-race-worker')
        os.environ['GPU_ARITHMETIC_RACE_LOG']=str(self.args.out/(kwargs.get('label') or ('rep%d-%s' % (rep,name)))/'lp-races.jsonl')
        if name=='oracle-hint':
            os.environ['GPU_ARITHMETIC_RACE_CPU_ONLY']='1'
        else:
            os.environ.pop('GPU_ARITHMETIC_RACE_CPU_ONLY',None)
"""
# This inserts text inside run-batch's generated Runner, not outside its source.
assert needle in source;source=source.replace(needle,insert.replace('\n',r'\n')+needle,1)
minimum_ready=int(os.environ.get('GPU_ARITHMETIC_GPU_MIN_READY','2'))
if minimum_ready<1:raise ValueError('minimum ready requests must be positive')
source=source.replace("argv+=['--host',os.environ['GPU_SMT_CUOPT_HOST']", "argv+=['--min-batch',"+repr(str(minimum_ready))+",'--host',os.environ['GPU_SMT_CUOPT_HOST']",1)
lp_method=os.environ.get('GPU_ARITHMETIC_GPU_LP_METHOD','PDLP')
if lp_method not in ['PDLP','Barrier']:raise ValueError('unsupported GPU method')
source=source.replace("argv+=['--min-batch'", "argv+=['--lp-method',"+repr(lp_method)+",'--min-batch'",1)
if os.environ.get('GPU_ARITHMETIC_GPU_INDEPENDENT_JOBS')=='1':
    source=source.replace("argv+=['--lp-method'", "argv+=['--independent-jobs','--lp-method'",1)
if os.environ.get('GPU_ARITHMETIC_GPU_ORIGINAL_FEASIBILITY')=='1':
    source=source.replace("'--lp-method',", "'--original-feasibility','--lp-method',",1)
if not os.environ.get('GPU_ARITHMETIC_RACE_MIN_ROWS'):
    raise RuntimeError('Set GPU_ARITHMETIC_RACE_MIN_ROWS from the retained native LP row distribution')
# Match the GPU/CPU candidates against the same native daemon concurrency.
old=r"{'fast-hybrid':'import GpuArithmetic.Baseline\\n',"
new=r"{'fast-hybrid':'import GpuArithmetic.BatchBaseline\\n',"
assert old in source
source=source.replace(old,new,1)
needle=r"\n        if name.startswith('fast-'):"+chr(34)+")"
replacement=r"\n        if name.startswith('fast-'):\n            os.environ['GPU_ARITHMETIC_BATCH']='1'"+chr(34)+")"
assert needle in source
source=source.replace(needle,replacement,1)
exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
