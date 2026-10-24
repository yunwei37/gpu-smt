"""Our finite rational-grid point proposals; exact checking stays in worker.py."""
import numpy as np
from fractions import Fraction as Q
from worker import constants,recipe,value,verify
def eval_array(e,x):
 t=e[0]
 if t=='q':return np.float64(float(Q(int(e[1]),int(e[2]))))
 if t=='v':return x[:,e[1]]
 if t=='+':return eval_array(e[1],x)+eval_array(e[2],x)
 if t=='-':return eval_array(e[1],x)-eval_array(e[2],x)
 if t=='nat_sub':return np.maximum(0,eval_array(e[1],x)-eval_array(e[2],x))
 if t=='*':return eval_array(e[1],x)*eval_array(e[2],x)
 if t=='neg':return -eval_array(e[1],x)
 if t=='pow':return eval_array(e[1],x)**e[2]
 if t=='true':return True
 if t=='false':return False
 if t=='and':return np.logical_and(eval_array(e[1],x),eval_array(e[2],x))
 if t=='or':return np.logical_or(eval_array(e[1],x),eval_array(e[2],x))
 if t=='not':return np.logical_not(eval_array(e[1],x))
 if t=='eq':return eval_array(e[1],x)==eval_array(e[2],x)
 if t=='ne':return eval_array(e[1],x)!=eval_array(e[2],x)
 if t=='lt':return eval_array(e[1],x)<eval_array(e[2],x)
 if t=='le':return eval_array(e[1],x)<=eval_array(e[2],x)
 raise ValueError('unsupported AST '+str(t))
def samples(ast,count=4096):
 pool=[Q(0),Q(1),Q(-1),Q(2),Q(-2),Q(1,2),Q(-1,2)]
 for q in constants(ast['goal'])+sum((constants(h)for h in ast['hypotheses']),[]):
  for v in [q,-q,q-1,q+1]:
   if v not in pool:pool.append(v)
 n=len(ast['variables']);rng=np.random.default_rng(0)
 indices=rng.integers(0,len(pool),size=(count,n))
 for i in range(min(count,len(pool))):indices[i,:]=i
 raw=np.array([float(q)for q in pool],dtype=np.float64)[indices]
 for j,d in enumerate(ast['variables']):
  if d['domain']in['nat','int']:raw[:,j]=np.floor(raw[:,j])
  if d['domain']=='nat':raw[:,j]=np.abs(raw[:,j])
 points=raw.copy()
 with np.errstate(all='ignore'):
  for _ in range(n+1):
   for j,e in recipe(ast):points[:,j]=eval_array(e,points)
 return pool,indices,points
def exact_point(ast,pool,indices,index):
 x=[pool[int(i)]for i in indices[index]]
 for j,d in enumerate(ast['variables']):
  if d['domain']in['nat','int']:x[j]=Q(x[j].numerator//x[j].denominator)
  if d['domain']=='nat':x[j]=abs(x[j])
 for _ in range(len(x)+1):
  old=x.copy()
  for j,e in recipe(ast):x[j]=value(e,x)
  if old==x:break
 return x
def find(ast,count=4096):
 pool,indices,points=samples(ast,count)
 mask=np.ones(count,dtype=bool)
 with np.errstate(all='ignore'):
  for h in ast['hypotheses']:mask&=eval_array(h,points)
  mask&=np.logical_not(eval_array(ast['goal'],points))
  mask&=np.all(np.isfinite(points),axis=1)
 for index in np.flatnonzero(mask):
  exact=exact_point(ast,pool,indices,int(index))
  if verify(ast,exact):
   return dict(point_index=int(index),point=[[str(v.numerator),str(v.denominator)]for v in exact],
    point_count=count,CPU_exact_checked=True)
 return None
