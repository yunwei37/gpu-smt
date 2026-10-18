"""Retained root diagnostic; completed phase CPU is exclusive, cancellation residual is bounded."""
from pathlib import Path
import json,gzip,collections,argparse,resource,os,importlib.util
A=Path(__file__).resolve().parent
class Parts(__import__('io').RawIOBase):
 def __init__(self,paths):super().__init__();self.paths=iter(paths);self.current=None
 def readable(self):return True
 def readinto(self,b):
  while True:
   if self.current is None:
    try:self.current=open(next(self.paths),'rb')
    except StopIteration:return 0
   n=self.current.readinto(b)
   if n:return n
   self.current.close();self.current=None
 def close(self):
  if self.current:self.current.close()
  super().close()
RECOVERY=[]
def rows(p):
 import io
 if not p.exists()and not list(p.parent.glob(p.name+'.part*')):
  alternate=p.with_name(p.name+'.gz')
  if alternate.exists()or list(alternate.parent.glob(alternate.name+'.part*')):p=alternate
 parts=sorted(p.parent.glob(p.name+'.part*'))
 if p.exists():
  with p.open('rb')as f:zipped=f.read(2)==b'\x1f\x8b'
  f=gzip.open(p,'rt')if zipped else p.open()
 elif parts:f=io.TextIOWrapper(gzip.GzipFile(fileobj=io.BufferedReader(Parts(parts)),mode='rb'))
 else:return
 with f:
  for n,line in enumerate(f,1):
   if not line.strip():continue
   try:yield json.loads(line)
   except json.JSONDecodeError:
    if not p.name.startswith('numeric-phases.jsonl'):raise
    # Known flat schema only. Preserve all truncated fragments and recover intact objects.
    for fragment in line.split('{')[1:]:
     raw='{'+fragment
     try:yield json.loads(raw)
     except json.JSONDecodeError as e:RECOVERY.append({'path':str(p),'line':n,'error':str(e),'raw_fragment':raw})
def exclusive(events):
 opened={};stack=collections.defaultdict(list);done={};children=collections.Counter();defects=[]
 for x in events:
  if x.get('event')not in ['begin','end']:continue
  k=(x['pid'],x['id']);lane=(x['pid'],x['tid'])
  if x['event']=='begin':
   if k in opened or k in done:defects.append({'duplicate':list(k)});continue
   opened[k]=(x,stack[lane][-1]if stack[lane]else None);stack[lane].append(k)
  else:
   if k not in opened:defects.append({'end_without_begin':list(k)});continue
   start,parent=opened.pop(k)
   if not stack[lane]or stack[lane][-1]!=k:defects.append({'not_nested':list(k)})
   if k in stack[lane]:stack[lane].remove(k)
   cpu=x['thread_cpu_ns']-start['thread_cpu_ns']
   if parent:children[parent]+=cpu
   done[k]={'pid':x['pid'],'tid':x['tid'],'stage':x['stage'],'call_id':x.get('call_id'),
    'start_ns':start['wall_ns'],'end_ns':x['wall_ns'],'inclusive_cpu_ns':cpu}
 for k,x in done.items():x['exclusive_cpu_ns']=x['inclusive_cpu_ns']-children[k]
 for k,x in done.items():
  if x['exclusive_cpu_ns']<0:defects.append({'negative_exclusive':list(k),'ns':x['exclusive_cpu_ns']})
 return list(done.values()),[x for x,_ in opened.values()],defects
def analyze(run,input_path,native_cell=None,direct_cell=None):
 by_method={};call_map={};all_races=[];fidelity={}
 layouts=[('native',native_cell),('direct',direct_cell)]if native_cell and direct_cell else[(m,run/('rep1-'+m))for m in ['fast-hybrid','oracle-highs']]
 for index,(method,cell)in enumerate(layouts):
  t=json.loads((cell/'terminal.json').read_text());assert t['state']=='complete'
  costs=rows(cell/'lean-costs.jsonl.gz')
  for x in costs:
   if x.get('ty')in ['cost-native-roundtrip','cost-direct-roundtrip']:
    ci=x['call_id'];assert ci not in call_map
    call_map[ci]={'method':method,'source':x['source'],'kind':x['ty'],'start_ns':x['start_ns'],'end_ns':x['end_ns'],'has_certificate':x['answer'].get('cert')is not None}
  rs=rows(cell/'responses.jsonl.gz')
  by_method[method]={'whole_seconds':t['whole_ns']/1e9,'counts':t['counts'],'observer_errors':t['sampling_read_errors'],'RLIMIT_AS':t['effective_RLIMIT_AS']}
  if index==0:base={x['proof_id']:x for x in rs}
  else:
   cand={x['proof_id']:x for x in rs};assert cand.keys()==base.keys()
   fidelity={'verdict_differences':[k for k in base if base[k]['outcome']!=cand[k]['outcome']],
    'non_message_differences':[k for k in base if {a:b for a,b in base[k]['response'].items()if a!='messages'}!={a:b for a,b in cand[k]['response'].items()if a!='messages'}],
    'message_only_difference_IDs':[k for k in base if base[k]['response']!=cand[k]['response']]}
   assert not fidelity['verdict_differences']and not fidelity['non_message_differences']
  for x in rows(cell/'lp-races.jsonl'):
   x['method']=method;all_races.append(x)
 event_paths=set(cell.parent/'numeric-phases.jsonl'for _,cell in layouts)
 events=[x for path in event_paths for x in rows(path)]
 assert events,'missing numeric phase events'
 completed,open_stages,defects=exclusive(events)
 if defects:raise AssertionError(defects[:5])
 by_cpu=collections.defaultdict(collections.Counter);pid_completed=collections.Counter();call_cpu=collections.defaultdict(collections.Counter)
 source_less=collections.Counter()
 for x in completed:
  ci=x['call_id'];ns=x['exclusive_cpu_ns'];pid_completed[x['pid']]+=ns
  if ci not in call_map:source_less[x['stage']]+=1;continue
  method=call_map[ci]['method'];by_cpu[method][x['stage']]+=ns;call_cpu[ci][x['stage']]+=ns
 workers=[];seen=set()
 for race in all_races:
  for role in ['cpu','gpu','strong_cpu']:
   usage=race.get(role+'_exit')
   if not isinstance(usage,dict):continue
   pid=usage['pid'];assert pid not in seen;seen.add(pid)
   assert usage.get('wait_error')is None and usage.get('kill_error')is None,usage
   assert 'wait4_user_cpu_ns'in usage and'wait4_system_cpu_ns'in usage
   total=usage['wait4_user_cpu_ns']+usage['wait4_system_cpu_ns']
   observed=pid_completed[pid]
   # wait4 CPU is microsecond-granularity; retain signed differences rather than hide them.
   workers.append({'pid':pid,'method':race['method'],'call_id':race['call_id'],
    'role':'native_hybrid'if role=='cpu'else'external_HiGHS'if role=='gpu'else role,
    'signal':usage['signal'],'exit_code':usage['exit_code'],'total_cpu_ns':total,'completed_exclusive_phase_cpu_ns':observed,
    'unassigned_cpu_ns_signed':total-observed,
    'unmatched_stages':[x['stage']for x in open_stages if x['pid']==pid]})
 summary={}
 for method in by_method:
  ws=[x for x in workers if x['method']==method]
  summary[method]={'CPU_seconds_exclusive_completed_phases':{k:v/1e9 for k,v in by_cpu[method].items()},
   'reaped_children':len(ws),'cancelled_children':sum(x['signal']is not None for x in ws),
   'reaped_child_total_CPU_seconds':sum(x['total_cpu_ns']for x in ws)/1e9,
   'cancelled_child_total_CPU_seconds':sum(x['total_cpu_ns']for x in ws if x['signal']is not None)/1e9,
   'reaped_unassigned_CPU_seconds_upper_for_any_unmeasured_phase':sum(max(0,x['unassigned_cpu_ns_signed'])for x in ws)/1e9,
   'negative_usage_minus_phase_quantization_differences':[{'pid':x['pid'],'ns':x['unassigned_cpu_ns_signed']}for x in ws if x['unassigned_cpu_ns_signed']<0]}
 services={}
 for method,cell in layouts:
  p=cell.parent/(cell.name+'-backend')/'support-calls.jsonl.gz.phases'
  ev=list(rows(p));closed,unclosed,errors=exclusive(ev);assert not errors,errors
  totals=collections.Counter()
  for x in closed:totals[x['stage']]+=x['exclusive_cpu_ns']
  ends=[x for x in ev if x.get('event')=='process_retired']
  services[method]={'completed_stage_thread_CPU_seconds':{k:v/1e9 for k,v in totals.items()},
   'phase_events':len(ev),'unclosed_scopes':len(unclosed),'retirement_records':ends,
   'whole_service_process_CPU_seconds':sum(x['process_user_seconds']+x['process_system_seconds']for x in ends)if ends else None,
   'scope':'Caller-thread stageCPU excludes internal HiGHS pool threads. Whole processCPU includes them plus startup/bookkeeping. Concurrent processCPU interval differences are not per-request CPU.'}
  if ends:services[method]['unassigned_process_CPU_seconds']=services[method]['whole_service_process_CPU_seconds']-sum(totals.values())/1e9
 return {'methods':by_method,'fidelity':fidelity,'numeric_requests':len(call_map),'phase_events':len(events),
 'completed_scopes':len(completed),'unclosed_scopes':len(open_stages),'unclosed_scope_records':open_stages,'source_less_auxiliary_stage_counts':dict(source_less),
 'numeric_CPU':summary,'external_service_CPU':services,'workers':workers,
 'per_call_completed_exclusive_CPU_ns':{str(k):dict(v)for k,v in call_cpu.items()},
 'retained_partial_numeric_append_fragments':RECOVERY,
 'scope':('Current same-dualbackend native/direct strong-omega diagnostic. 'if native_cell else'Historical-fast-hybrid/direct qualification, not current strongest reference. ')+'ScalarAST path,equal8queues/4CPU4--7/48GiB.No GPU run. Completed exclusive phaseCPU is not whole-clock fraction; cancelled child residual bounds include startup/logger/unfinished work. These do not by themselves establish a scheduler-independent wall Amdahl upper bound. Root self-review.'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--native-cell',type=Path);p.add_argument('--direct-cell',type=Path);a=p.parse_args()
 os.sched_setaffinity(0,{12,13,14,15});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
 result=analyze(a.run,a.input,a.native_cell,a.direct_cell);a.out.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k not in ['workers','per_call_completed_exclusive_CPU_ns']},indent=2))
if __name__=='__main__':main()
