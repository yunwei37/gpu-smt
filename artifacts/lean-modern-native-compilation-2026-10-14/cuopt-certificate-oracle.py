#!/usr/bin/env python3
# Thin NVIDIA26.8 C-API certificate-support adapter; exact repair/fallback is upstream Farkas.
from pathlib import Path
import ctypes as C, json, os, sys, math, subprocess, time
from fractions import Fraction
D=Path(__file__).parent
class CuOpt:
 def __init__(self,path,method=None):
  self.lib=C.CDLL(path)
  fs=self.lib.cuOptGetFloatSize();isize=self.lib.cuOptGetIntSize()
  self.F=C.c_double if fs==8 else C.c_float
  self.I=C.c_int32 if isize==4 else C.c_int64
  assert fs in [4,8] and isize in [4,8]
  P=C.c_void_p;I=self.I;F=self.F;ip=C.POINTER(I);fp=C.POINTER(F);pp=C.POINTER(P)
  bindings={
   'cuOptCreateProblem':[I,I,I,F,fp,ip,ip,fp,C.c_char_p,fp,fp,fp,C.c_char_p,pp],
   'cuOptCreateSolverSettings':[pp],
   'cuOptSetIntegerParameter':[P,C.c_char_p,I],
   'cuOptSolve':[P,P,pp],
   'cuOptGetTerminationStatus':[P,ip],
   'cuOptGetPrimalSolution':[P,fp],
   'cuOptDestroyProblem':[pp],
   'cuOptDestroySolverSettings':[pp],
   'cuOptDestroySolution':[pp]}
  for name,args in bindings.items():
   fn=getattr(self.lib,name);fn.argtypes=args;fn.restype=None if name.startswith('cuOptDestroy') else I
  self.method=method
 def ok(self,name,*args):
  status=getattr(self.lib,name)(*args)
  if status!=0:raise RuntimeError(name+' status '+str(status))
 def solve(self,lp):
  hyps=lp['hyps'];n=len(hyps)
  atoms=sorted({int(v) for _,cs in hyps for v,c in cs if int(c)!=0})
  strict=[j for j,(kind,_) in enumerate(hyps) if kind=='lt']
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
  m=len(atoms)+1;I=self.I;F=self.F
  coeff=(F*len(values))(*values);col=(I*len(columns))(*columns);off=(I*len(offsets))(*offsets)
  objective=(F*n)(*([0]*n));rhs=(F*m)(*([0]*(m-1)+[1]))
  lb=(F*n)(*([0]*n));ub=(F*n)(*([math.inf]*n))
  problem=C.c_void_p();settings=C.c_void_p();solution=C.c_void_p()
  try:
   self.ok('cuOptCreateProblem',m,n,1,0,objective,off,col,coeff,b'E'*m,rhs,lb,ub,b'C'*n,C.byref(problem))
   self.ok('cuOptCreateSolverSettings',C.byref(settings))
   # Console text would corrupt the upstream one-JSON-line daemon protocol.
   self.ok('cuOptSetIntegerParameter',settings,b'log_to_console',0)
   if self.method is not None:self.ok('cuOptSetIntegerParameter',settings,b'method',self.method)
   self.ok('cuOptSolve',problem,settings,C.byref(solution))
   status=I();self.ok('cuOptGetTerminationStatus',solution,C.byref(status))
   result=(F*n)();self.ok('cuOptGetPrimalSolution',solution,result)
   weights=list(result)
   if not all(math.isfinite(x) for x in weights):return None
   return weights
  finally:
   if solution:self.lib.cuOptDestroySolution(C.byref(solution))
   if settings:self.lib.cuOptDestroySolverSettings(C.byref(settings))
   if problem:self.lib.cuOptDestroyProblem(C.byref(problem))
class Oracle:
 def __init__(self,lib,method):
  self.cuopt=CuOpt(lib,method)
  self.exact=subprocess.Popen([str(D/'farkas-external-support'),'--serve'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
 def native(self,lp):
  self.exact.stdin.write(json.dumps(lp,separators=(',',':'))+'\n');self.exact.stdin.flush()
  line=self.exact.stdout.readline()
  if not line:raise RuntimeError('exact oracle exited')
  return json.loads(line)
 def run(self,lp):
  before=time.monotonic_ns();weights=None;error=None;attempts=[]
  try:weights=self.cuopt.solve(lp)
  except Exception as e:error=str(e)
  if weights:
   maximum=max(weights);seen=[]
   for tau in [1e-6,1e-9,0.0]:
    support=[j for j,x in enumerate(weights) if x>0 and x>tau*maximum]
    strict=[j for j,(kind,cs) in enumerate(lp['hyps']) if kind=='lt']
    if not any(j in strict for j in support) and strict:support.append(max(strict,key=lambda j:weights[j]))
    support.sort(key=lambda j:(-weights[j],j))
    if not support or support in seen:continue
    seen.append(support)
    answer=self.native(dict(lp,support=support))
    attempts.append({'support':len(support),'repaired':answer.get('support_repaired',False)})
    # Failed support repair already runs full exact fallback, so return that answer;
    # do not repeatedly pay tiered solve merely to try a different FP threshold.
    return answer,{'method':self.cuopt.method,'elapsed_ns':time.monotonic_ns()-before,'attempts':attempts,'gpu_error':error}
  return self.native(lp),{'method':self.cuopt.method,'elapsed_ns':time.monotonic_ns()-before,'attempts':attempts,'gpu_error':error}
 def close(self):
  self.exact.stdin.close();self.exact.wait()
def main():
 method=os.environ.get('CUOPT_CERT_METHOD')
 oracle=Oracle(os.environ['LIBCUOPT_LIBRARY_PATH'],int(method) if method is not None else None)
 try:
  for line in sys.stdin:
   if not line.strip():continue
   value=json.loads(line)
   if value.get('hello') is True:
    print(json.dumps({'farkas_protocol':1,'version':'cuopt26.8-exact-repair','engine':'cuopt-support'}),flush=True);continue
   answer,meta=oracle.run(value)
   if os.environ.get('CUOPT_CERT_TELEMETRY'):
    print(json.dumps(meta),file=sys.stderr,flush=True)
   print(json.dumps(answer),flush=True)
 finally:oracle.close()
if __name__=='__main__':main()
