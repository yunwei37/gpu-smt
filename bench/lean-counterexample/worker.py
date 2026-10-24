"""Own exact arithmetic witness checker and observation worker. No solver."""
import fractions,itertools,json,os,random,sys,time,socket
Q=fractions.Fraction
def value(e,x):
 tag=e[0]
 if tag=='q':return Q(int(e[1]),int(e[2]))
 if tag=='v':return x[e[1]]
 if tag=='+':return value(e[1],x)+value(e[2],x)
 if tag=='-':return value(e[1],x)-value(e[2],x)
 if tag=='nat_sub':return max(Q(0),value(e[1],x)-value(e[2],x))
 if tag=='*':return value(e[1],x)*value(e[2],x)
 if tag=='neg':return -value(e[1],x)
 if tag=='pow':return value(e[1],x)**e[2]
 raise ValueError('unsupported arithmetic '+str(tag))
def proposition(e,x):
 tag=e[0]
 if tag=='true':return True
 if tag=='false':return False
 if tag=='and':return proposition(e[1],x)and proposition(e[2],x)
 if tag=='or':return proposition(e[1],x)or proposition(e[2],x)
 if tag=='not':return not proposition(e[1],x)
 a,b=value(e[1],x),value(e[2],x)
 if tag=='eq':return a==b
 if tag=='ne':return a!=b
 if tag=='lt':return a<b
 if tag=='le':return a<=b
 raise ValueError('unsupported proposition '+str(tag))
def verify(ast,x):
 if len(x)!=len(ast['variables']):return False
 for decl,v in zip(ast['variables'],x):
  if decl['domain']in ['nat','int']and v.denominator!=1:return False
  if decl['domain']=='nat'and v<0:return False
 return all(proposition(h,x)for h in ast['hypotheses'])and not proposition(ast['goal'],x)
def flatten(h):
 if h[0]=='and':return flatten(h[1])+flatten(h[2])
 return [h]
def constants(e):
 if not isinstance(e,list):return []
 if e and e[0]=='q':return [Q(int(e[1]),int(e[2]))]
 return sum((constants(a)for a in e[1:]if isinstance(a,list)),[])
def dependencies(e):
 if not isinstance(e,list):return set()
 if e[0]=='v':return {e[1]}
 return set().union(*(dependencies(a)for a in e[1:]if isinstance(a,list)))
def recipe(ast):
 hs=sum((flatten(h)for h in ast['hypotheses']),[])
 bindings=[]
 for h in hs:
  if h[0]!='eq':continue
  for a,b in [(h[1],h[2]),(h[2],h[1])]:
   if a[0]=='v'and a[1]not in dependencies(b):
    bindings.append((a[1],b));break
 return bindings
def points(ast,count=4096):
 pool=[Q(0),Q(1),Q(-1),Q(2),Q(-2),Q(1,2),Q(-1,2)]
 for q in constants(ast['goal'])+sum((constants(h)for h in ast['hypotheses']),[]):
  for v in [q,-q,q-1,q+1]:
   if v not in pool:pool.append(v)
 rng=random.Random(0);n=len(ast['variables']);bindings=recipe(ast)
 for i in range(count):
  if i<len(pool):x=[pool[i]]*n
  else:x=[rng.choice(pool)for _ in range(n)]
  for j,decl in enumerate(ast['variables']):
   if decl['domain']in['nat','int']:x[j]=Q(x[j].numerator//x[j].denominator)
   if decl['domain']=='nat':x[j]=abs(x[j])
  # Sampling recipes propose assignments only; verify rechecks every equation.
  for _ in range(n+1):
   previous=x.copy()
   for j,e in bindings:x[j]=value(e,x)
   if x==previous:break
  yield x
def search(ast,count=4096):
 for i,x in enumerate(points(ast,count)):
  if verify(ast,x):return dict(point=[[str(v.numerator),str(v.denominator)]for v in x],point_index=i,points_tested=i+1)
 return None
def provider_memory_sampler(host,port=5001,expected_backend='device'):
 identity=None
 def sample():
  nonlocal identity
  with socket.create_connection((host,port),timeout=1)as connection:
   connection.sendall(b'{"memory":true}\n')
   with connection.makefile('r')as stream:result=json.loads(stream.readline())
  current=(result['root_pid'],result['root_start_ticks'])
  if identity is None:identity=current
  if current!=identity or result.get('backend')!=expected_backend:
   raise RuntimeError('owned point provider identity/backend changed')
  if result['affinity']!=sorted(os.sched_getaffinity(0)):
   raise RuntimeError('owned point provider CPU eligibility changed')
  return result
 return sample

def screen_gpu(q):
 start=time.monotonic_ns()
 host=os.environ['GPU_SMT_CEX_GPU_HOST'];port=int(os.environ.get('GPU_SMT_CEX_GPU_PORT','5001'))
 with socket.create_connection((host,port))as connection:
  with connection.makefile('rwb')as stream:
   stream.write((json.dumps({'screen':q},separators=(',',':'))+'\n').encode());stream.flush()
   reply=json.loads(stream.readline())
 rpc_ns=time.monotonic_ns()-start
 if reply.get('source_id')!=q['source_id']or reply.get('entry_ns')!=q['entry_ns']:
  raise ValueError('point reply has wrong source/entry ownership')
 result=dict(exact_counterexample=False,gpu_rpc_ns=rpc_ns,provider=reply.get('timing'),
  provider_backend=reply.get('backend'))
 if reply.get('error'):
  result['fallback_error']=reply['error'];return result
 proposed=reply.get('candidate_point')
 if proposed is not None:
  check_start=time.monotonic_ns()
  point=[Q(int(n),int(d))for n,d in proposed]
  result['candidate_point_received']=True
  result['candidate_exact_recheck_passed']=verify(q['payload']['ast'],point)
  if result['candidate_exact_recheck_passed']:
   result.update(exact_counterexample=True,witness=dict(point=proposed,point_index=reply.get('point_index')))
  result['cpu_exact_recheck_ns']=time.monotonic_ns()-check_start
 return result

def answer(q):
 try:
  if q['payload']['supported']and q['mode']=='gpu':return screen_gpu(q)
  if q['payload']['supported']and q['mode']=='cpu':
   witness=search(q['payload']['ast'])
   if witness:return dict(exact_counterexample=True,witness=witness)
  return dict(exact_counterexample=False)
 except Exception as ex:return dict(exact_counterexample=False,fallback_error=repr(ex))

def main():
 for line in sys.stdin:
  started=time.monotonic_ns()
  try:
   q=json.loads(line)
   q.update(worker_pid=os.getpid(),repl_pid=os.getppid(),worker_started_ns=started)
   result=answer(q)
   q.update(worker_end_ns=time.monotonic_ns(),answer=result)
   with open(os.environ['GPU_SMT_CEX_LOG'],'a')as f:f.write(json.dumps(q,separators=(',',':'))+'\n')
  except Exception as ex:result={'exact_counterexample':False,'fallback_error':repr(ex)}
  print(json.dumps(result,separators=(',',':')),flush=True)
if __name__=='__main__':main()
