"""Our batched arithmetic point evaluator. No proof decision on float output."""
from pathlib import Path
import ctypes as C
import subprocess
import time
import numpy as np
from fractions import Fraction as Q
from point_proposals import samples,exact_point
from worker import verify

OPS={'+':2,'-':3,'nat_sub':4,'*':5,'neg':6,'pow':7,
 'true':8,'false':9,'and':10,'or':11,'not':12,'eq':13,'ne':14,'lt':15,'le':16}

def compile_program(ast):
 code=[];constants=[];depth=0;maximum=0
 def emit(op,arg=0,constant=0.0):
  nonlocal depth,maximum
  if op in[0,1,8,9]:depth+=1
  elif op not in[6,7,12]:depth-=1
  if depth<1:raise ValueError('invalid expression stack')
  maximum=max(maximum,depth);code.append((op,arg));constants.append(constant)
 def expression(e):
  tag=e[0]
  if tag=='q':
   constant=float(Q(int(e[1]),int(e[2])))
   if not np.isfinite(constant):raise ValueError('nonfinite literal')
   emit(0,constant=constant);return
  if tag=='v':
   if not 0<=e[1]<len(ast['variables']):raise ValueError('invalid variable')
   emit(1,e[1]);return
  if tag in['true','false']:emit(OPS[tag]);return
  if tag in['neg','not']:expression(e[1]);emit(OPS[tag]);return
  if tag=='pow':
   if not isinstance(e[2],int)or not 0<=e[2]<=8:raise ValueError('unsupported exponent')
   expression(e[1]);emit(7,e[2]);return
  if tag not in OPS:raise ValueError('unsupported expression')
  expression(e[1]);expression(e[2]);emit(OPS[tag])
 emit(8)
 for h in ast['hypotheses']:expression(h);emit(10)
 expression(ast['goal']);emit(12);emit(10)
 if depth!=1 or maximum>64:raise ValueError('unsupported expression stack depth')
 return code,constants,maximum

def pack(entries,count=4096):
 if count<1 or not entries or len(entries)>65535:raise ValueError('invalid batch shape')
 codes=[];constants=[];meta=[];domains=[];point_arrays=[];retained=[]
 point_offset=hit_offset=0
 for entry in entries:
  if not entry['payload']['supported']:raise ValueError('unsupported query must use native fallback')
  ast=entry['payload']['ast'];code,cs,depth=compile_program(ast)
  pool,indices,points=samples(ast,count)
  ds=[{'real':0,'rat':0,'int':1,'nat':2}[v['domain']]for v in ast['variables']]
  meta.append([len(codes),len(codes)+len(code),len(domains),len(ds),point_offset,count,hit_offset])
  retained.append(dict(entry=entry,pool=pool,indices=indices,stack_depth=depth))
  codes.extend(code);constants.extend(cs);domains.extend(ds);point_arrays.append(points.ravel())
  point_offset+=points.size;hit_offset+=count
 return dict(code=np.asarray(codes,dtype=np.int32),constants=np.asarray(constants,dtype=np.float64),
  meta=np.asarray(meta,dtype=np.int64),domains=np.asarray(domains,dtype=np.int32),
  points=np.concatenate(point_arrays),hits=np.zeros(hit_offset,dtype=np.uint8),
  retained=retained,count=count)

def reference_masks(batch):
 masks=[]
 for m in batch['meta']:
  start,end,domain_start,n,point_start,count,hit_start=map(int,m)
  x=batch['points'][point_start:point_start+count*n].reshape(count,n)
  valid=np.all(np.isfinite(x),axis=1);stack=[]
  with np.errstate(all='ignore'):
   for j,d in enumerate(batch['domains'][domain_start:domain_start+n]):
    if d:valid&=x[:,j]==np.floor(x[:,j])
    if d==2:valid&=x[:,j]>=0
   for pc in range(start,end):
    op,arg=map(int,batch['code'][pc])
    if op==0:stack.append(batch['constants'][pc]);continue
    if op==1:stack.append(x[:,arg]);continue
    if op in[8,9]:stack.append(op==8);continue
    if op==6:stack[-1]=-stack[-1];continue
    if op==7:
     base=stack.pop();value=1.0
     for _ in range(arg):value=value*base
     stack.append(value);continue
    if op==12:stack[-1]=np.logical_not(stack[-1]);continue
    b=stack.pop();a=stack.pop()
    if op==2:value=a+b
    elif op==3:value=a-b
    elif op==4:value=np.maximum(0,a-b)
    elif op==5:value=a*b
    elif op==10:value=np.logical_and(a,b)
    elif op==11:value=np.logical_or(a,b)
    elif op==13:value=a==b
    elif op==14:value=a!=b
    elif op==15:value=a<b
    elif op==16:value=a<=b
    stack.append(value)
  assert len(stack)==1
  masks.append(np.asarray(valid&stack[0],dtype=np.uint8))
 return np.concatenate(masks)

def exact_results(batch,masks):
 # GPU masks can only nominate grid indices; reconstruct exact rational points.
 if len(masks)!=len(batch['hits']):raise ValueError('invalid returned proposal shape')
 results=[]
 for i,record in enumerate(batch['retained']):
  entry=record['entry'];ast=entry['payload']['ast'];count=batch['count'];checked=0;witness=None
  for index in np.flatnonzero(masks[i*count:(i+1)*count]):
   point=exact_point(ast,record['pool'],record['indices'],int(index));checked+=1
   if verify(ast,point):
    witness=dict(point_index=int(index),point=[[str(x.numerator),str(x.denominator)]for x in point]);break
  results.append(dict(source_id=entry['source_id'],entry_ns=entry['entry_ns'],
   exact_counterexample=witness is not None,witness=witness,exact_candidates_checked=checked))
 return results

class Device:
 """Finite owned CUDA context; all transfers, kernel and cleanup are synchronous."""
 def __init__(self,ptx):
  self.api=C.CDLL('libcuda.so.1');self.context=C.c_void_p();self.module=C.c_void_p();self.fn=C.c_void_p()
  self.bind('cuInit',[C.c_uint])(0);dev=C.c_int()
  self.bind('cuDeviceGet',[C.POINTER(C.c_int),C.c_int])(C.byref(dev),0)
  name=C.create_string_buffer(256)
  self.bind('cuDeviceGetName',[C.c_void_p,C.c_int,C.c_int])(name,256,dev)
  self.name=name.value.decode()
  if 'RTX 5090'not in self.name:raise RuntimeError('This experiment uses RTX5090 only: '+self.name)
  self.bind('cuCtxCreate_v2',[C.POINTER(C.c_void_p),C.c_uint,C.c_int])(C.byref(self.context),0,dev)
  try:
   data=C.create_string_buffer(Path(ptx).read_bytes())
   self.bind('cuModuleLoadData',[C.POINTER(C.c_void_p),C.c_void_p])(C.byref(self.module),data)
   self.bind('cuModuleGetFunction',[C.POINTER(C.c_void_p),C.c_void_p,C.c_char_p])(C.byref(self.fn),self.module,b'arithmetic_points')
  except Exception:self.close();raise
 def bind(self,name,types):
  fn=getattr(self.api,name);fn.argtypes=types;fn.restype=C.c_int
  def call(*args):
   status=fn(*args)
   if status:raise RuntimeError(name+': CUDA error '+str(status))
  return call
 def evaluate(self,batch):
  start=time.perf_counter();pointers=[]
  arrays=[batch[k]for k in['code','constants','meta','domains','points','hits']]
  try:
   for array in arrays:
    ptr=C.c_uint64()
    self.bind('cuMemAlloc_v2',[C.POINTER(C.c_uint64),C.c_size_t])(C.byref(ptr),max(1,array.nbytes))
    pointers.append(ptr)
   allocated=time.perf_counter()
   for ptr,array in zip(pointers[:-1],arrays[:-1]):
    if array.nbytes:self.bind('cuMemcpyHtoD_v2',[C.c_uint64,C.c_void_p,C.c_size_t])(ptr,array.ctypes.data,array.nbytes)
   uploaded=time.perf_counter()
   parameters=(C.c_void_p*len(pointers))(*[C.cast(C.pointer(v),C.c_void_p)for v in pointers])
   self.bind('cuLaunchKernel',[C.c_void_p,C.c_uint,C.c_uint,C.c_uint,C.c_uint,C.c_uint,C.c_uint,C.c_uint,C.c_void_p,C.c_void_p,C.c_void_p])(
    self.fn,(batch['count']+255)//256,len(batch['meta']),1,256,1,1,0,None,parameters,None)
   self.bind('cuCtxSynchronize',[])()
   executed=time.perf_counter()
   self.bind('cuMemcpyDtoH_v2',[C.c_void_p,C.c_uint64,C.c_size_t])(batch['hits'].ctypes.data,pointers[-1],batch['hits'].nbytes)
   downloaded=time.perf_counter()
  finally:
   for pointer in reversed(pointers):self.bind('cuMemFree_v2',[C.c_uint64])(pointer)
  return dict(allocate_seconds=allocated-start,upload_seconds=uploaded-allocated,
   synchronized_kernel_seconds=executed-uploaded,download_seconds=downloaded-executed,
   free_seconds=time.perf_counter()-downloaded,whole_evaluate_seconds=time.perf_counter()-start)
 def close(self):
  if self.context.value:
   self.bind('cuCtxDestroy_v2',[C.c_void_p])(self.context);self.context=C.c_void_p()
 def __enter__(self):return self
 def __exit__(self,*_):self.close()

def compile_ptx(target,compiler):
 # Existing pinned CUDA12.8 compiler, native RTX5090 target, no new install.
 command=[str(compiler),'--ptx','-arch=compute_120','-std=c++17',
  str(Path(__file__).with_name('points.cu')),'-o',str(target)]
 result=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 Path(target).with_suffix('.compile.log').write_text(result.stdout)
 if result.returncode:raise RuntimeError('CUDA compilation failed: '+str(result.returncode))
 return command
