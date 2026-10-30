from pathlib import Path
import collections,csv,io,json,math,os,resource,subprocess,time
os.sched_setaffinity(0,{0,1});resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3));start=time.monotonic()
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-paper-profile-validity-step.txt').read_text().strip());e=s/'experiment-001';rev='6f6f89608fae0783fad156704920ee8b93d767a1';prefix='research/mechanisms-2026-10-30/'
frozen=lambda name:subprocess.check_output(['git','show',rev+':'+prefix+name],cwd=r).decode()
reported=json.loads(frozen('profiler-400-summary.json'));capture=Path(reported['raw_capture'])
rows=[]
with (capture/'stdout.txt').open() as f:
 for line in f:
  if line.startswith('M_DAG '):
   item=json.loads(line[len('M_DAG '):])
   rows.append({k:item[k] for k in ['id','mode','hasErrors','errors','wallNanoseconds','cpuNanoseconds']})
assert len(rows)==400 and len({x['id'] for x in rows})==200
pairs=collections.defaultdict(dict)
for x in rows:
 assert x['mode'] not in pairs[x['id']];pairs[x['id']][x['mode']]=x
assert all(set(x)=={'control','observe'} for x in pairs.values())
assert all(rows[i]['mode']=='control' and rows[i+1]['mode']=='observe' and rows[i]['id']==rows[i+1]['id'] for i in range(0,400,2))
def classify(x):
 if not x['hasErrors']:return 'no_lean_errors'
 if any(any(marker in err for marker in ['maximum number of heartbeats','maximum recursion depth','deep recursion detected','(kernel) deterministic timeout']) for err in x['errors']):return 'diagnostic_budget_interruption'
 return 'ordinary_lean_error'
csvrows={(x['id'],x['mode']):x for x in csv.DictReader(io.StringIO(frozen('profiler-400-diagnostic.csv')))}
stats={}
for mode in ['control','observe']:
 selected=[x for x in rows if x['mode']==mode]
 classes=dict(collections.Counter(classify(x) for x in selected));ns=sum(x['wallNanoseconds'] for x in selected)
 for x in selected:
  row=csvrows[(x['id'],mode)]
  assert (row['error_flag']=='True')==x['hasErrors']
  assert row['classification']==classify(x),(x['id'],mode,row['classification'],classify(x),x['errors'])
  assert math.isclose(float(row['wall_seconds']),x['wallNanoseconds']/1e9,abs_tol=1e-9,rel_tol=1e-12)
 assert classes==reported['mode_statistics'][mode]['classes'],classes
 assert math.isclose(ns/1e9,reported['mode_statistics'][mode]['body_wall_s'],abs_tol=1e-9)
 stats[mode]={'units':len(selected),'classes':classes,'body_wall_ns':ns,'body_wall_s':ns/1e9}
changed=[{'id':key,'control_error':v['control']['hasErrors'],'observe_error':v['observe']['hasErrors'],'control_class':classify(v['control']),'observe_class':classify(v['observe']),'observe_errors':v['observe']['errors']} for key,v in pairs.items() if v['control']['hasErrors']!=v['observe']['hasErrors']]
assert len(changed)==reported['different_error_flags']==7
assert all(not x['control_error'] and x['observe_error'] and x['observe_class']=='diagnostic_budget_interruption' for x in changed)
claimed=json.loads(frozen('profiler-7-differences.json'));assert {x['id'] for x in changed}=={x['id'] for x in claimed}
diagnostics_differ=sum(v['control']['errors']!=v['observe']['errors'] for v in pairs.values())
class_transition=collections.Counter((classify(v['control']),classify(v['observe'])) for v in pairs.values())
receipt=json.loads((capture/'receipt.json').read_text());assert receipt['exit']==0 and receipt['retired'] and receipt['signals_sent']==0
assert receipt==reported['receipt']
cs=json.loads(frozen('c-timing-control-summary.json'));cp=Path(cs['raw_capture']);events=[json.loads(x) for x in (cp/'tactics.jsonl').read_text().splitlines()]
event_counts=dict(collections.Counter(x['event'] for x in events));assert event_counts==cs['events']=={'source':16};assert not cs['qualified']
source=frozen('DAG200.lean');tick=chr(96)
assert '.setNat '+tick+'maxHeartbeats 3000' in source and '.setBool '+tick+'trace.profiler (mode == "observe")' in source and '.setNat '+tick+'trace.profiler.threshold 0' in source
artifact_input=r/prefix/'dag200-input.json';input_scope='Retained program config verified; original input snapshot not found'
if artifact_input.exists():
 inputs=json.loads(artifact_input.read_text());assert len(inputs)==400
 ip=collections.defaultdict(dict)
 for x in inputs:ip[x['id']][x['mode']]=x['code']
 assert set(ip)==set(pairs) and all(v['control']==v['observe'] for v in ip.values())
 input_scope='Current retained 400-unit input has byte-equal source strings per pair and matches raw IDs; capture/source history remains the recorded producer provenance'
result={'M_commit':rev,'raw_rows':400,'source_pairs':200,'mode_order':'control then observe for every source','mode_statistics':stats,'flag_changes':changed,'raw_error_array_different_pairs':diagnostics_differ,'error_marker_units':{mode:{name:sum(any(token in error for error in row['errors']) for row in rows if row['mode']==mode) for name,token in [('kernel_deterministic_timeout','(kernel) deterministic timeout'),('public_heartbeat_error','maximum number of heartbeats'),('recursion_limit_error','maximum recursion depth')]} for mode in ['control','observe']},'class_transitions':[{'control':a,'observe':b,'sources':n} for (a,b),n in class_transition.items()],'observe_control_body_wall_ratio':stats['observe']['body_wall_ns']/stats['control']['body_wall_ns'],'whole_native_receipt':receipt,'raw_stdout_bytes':(capture/'stdout.txt').stat().st_size,'input_scope':input_scope,'C_raw_event_counts':event_counts,'C_hook_qualified':False,'native_runs_by_root':0,'raw_heartbeat_deltas_available':False,'full_production_acceptance_tested':False,'unmodified_candidate_DAG_speedup_inferred':False,'root_elapsed_s':time.monotonic()-start,'root_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'root_affinity':sorted(os.sched_getaffinity(0))}
(e/'profiler-validity-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
