#!/tmp/gpu-smt-highs-1.15.1-20261014/bin/python
# Official HiGHS1.15.1 CPU support search, upstream exact repair/fallback and native Lean checking.
from pathlib import Path
import importlib.util,json,os,sys,math,subprocess
from fractions import Fraction
import highspy
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('certificateAdapter',D/'cuopt-certificate-oracle.py')
adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
class Highs:
 method='highs-default'
 def solve(self,value):
  hyps=value['hyps'];n=len(hyps)
  atoms=sorted({int(v) for kind,cs in hyps for v,c in cs if int(c)!=0})
  strict=[j for j,(kind,cs) in enumerate(hyps) if kind=='lt']
  if not strict:return None
  scales=[max([abs(int(c)) for v,c in cs]+[1]) for kind,cs in hyps]
  rows={a:{} for a in atoms}
  for j,(kind,cs) in enumerate(hyps):
   for a,c in cs:
    c=int(c)
    if c:rows[int(a)][j]=rows[int(a)].get(j,Fraction(0))+Fraction(c,scales[j])
  offsets=[0];columns=[];values=[]
  for a in atoms:
   for j,c in sorted(rows[a].items()):
    if not c:continue
    f=float(c)
    if not math.isfinite(f) or f==0:return None
    columns.append(j);values.append(f)
   offsets.append(len(values))
  columns.extend(strict);values.extend([1.0]*len(strict));offsets.append(len(values))
  m=len(atoms)+1
  lp=highspy.HighsLp();lp.num_col_=n;lp.num_row_=m
  lp.col_cost_=[0.0]*n;lp.col_lower_=[0.0]*n;lp.col_upper_=[highspy.kHighsInf]*n
  lp.row_lower_=[0.0]*(m-1)+[1.0];lp.row_upper_=lp.row_lower_
  lp.a_matrix_.format_=highspy.MatrixFormat.kRowwise
  lp.a_matrix_.start_=offsets;lp.a_matrix_.index_=columns;lp.a_matrix_.value_=values
  h=highspy.Highs()
  # Required for the existing one-JSON-line daemon transport; no solver tuning.
  h.setOptionValue('output_flag',False)
  if h.passModel(lp)!=highspy.HighsStatus.kOk:raise RuntimeError('HiGHS passModel failed')
  if h.run()==highspy.HighsStatus.kError:raise RuntimeError('HiGHS run failed')
  solution=h.getSolution()
  if not solution.value_valid:return None
  weights=list(solution.col_value)
  return weights if len(weights)==n and all(math.isfinite(x) for x in weights) else None
class Oracle(adapter.Oracle):
 def __init__(self):
  self.cuopt=Highs()
  self.exact=subprocess.Popen([str(D/'farkas-external-support'),'--serve'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
def main():
 oracle=Oracle()
 try:
  for line in sys.stdin:
   if not line.strip():continue
   value=json.loads(line)
   if value.get('hello') is True:
    print(json.dumps({'farkas_protocol':1,'version':'highs1.15.1-exact-repair','engine':'highs-support'}),flush=True);continue
   answer,meta=oracle.run(value)
   if os.environ.get('HIGHS_CERT_TELEMETRY'):print(json.dumps(meta),file=sys.stderr,flush=True)
   print(json.dumps(answer),flush=True)
 finally:oracle.close()
if __name__=='__main__':main()
