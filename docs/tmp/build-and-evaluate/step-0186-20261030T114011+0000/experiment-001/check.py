from pathlib import Path
import os,sys,json,collections,math,time,resource,datetime
os.sched_setaffinity(0,{0,1});t0=time.monotonic()
root=Path('/workspaces/repository');m=root/'research/mechanisms-2026-10-30'
point=Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/native-cohort-matrix')
terminal=json.loads((point/'terminal.json').read_text());assert len(terminal['cells'])==6
byid=collections.defaultdict(dict);receipts=[];sources_by_shard=collections.defaultdict(list)
tree_peak=0;maxgap=0;source_metrics={};exclusive=collections.Counter();event_count=collections.Counter()
def parse_events(path):
 global exclusive,event_count
 current=None;stacks=collections.defaultdict(list);frames={};seen=set();out={}
 for l in path.open():
  e=json.loads(l);ev=e['event'];event_count[ev]+=1
  if ev=='source':
   name,mode=e['name'].rsplit('|',1);assert e['open_frames']==0 and not frames and not any(stacks.values())
   if mode=='observe':
    assert current is None and name not in out;current=name;out[name]={'entries':0,'exits':0,'largest_leaf_cpu_ns':0,'roots_cpu_ns':0}
   else:
    assert mode=='off' and current==name;current=None
  elif ev=='enter':
   assert current is not None and e['id'] not in seen
   stack=stacks[e['thread']];assert e['parent']==(stack[-1] if stack else 0)
   seen.add(e['id']);frames[e['id']]={**e,'source':current,'child_cpu_ns':0,'children':0}
   stack.append(e['id']);out[current]['entries']+=1
  elif ev=='exit':
   n=frames.pop(e['id']);assert n['source']==current and stacks[n['thread']][-1]==e['id']
   stacks[n['thread']].pop()
   dur=e['cpu_ns']-n['cpu_ns'];assert dur>=n['child_cpu_ns']>=0 and e['wall_ns']>=n['wall_ns']
   exclusive[n['kind']]+=dur-n['child_cpu_ns'];out[current]['exits']+=1
   if n['parent']:
    parent=frames[n['parent']];parent['child_cpu_ns']+=dur;parent['children']+=1
   else:out[current]['roots_cpu_ns']+=dur
   if n['children']==0:out[current]['largest_leaf_cpu_ns']=max(out[current]['largest_leaf_cpu_ns'],dur)
  else:raise ValueError(ev)
 assert current is None and not frames and all(not v for v in stacks.values())
 assert all(v['entries']==v['exits'] for v in out.values())
 return out
for cell in terminal['cells']:
 assert cell['rows']==cell['expected']==100 and cell['native_retired'] and cell['client_exit']==cell['native_exit']==0
 p=Path(cell['raw_capture']);receipt=json.loads((p/'receipt.json').read_text())
 assert receipt['exit']==0 and receipt['retired'];receipts.append(receipt)
 stat=Path('/proc')/str(receipt['pid'])/'stat'
 if stat.exists():assert stat.read_text().split(') ',1)[1].split()[19]!=str(receipt['start_ticks']), 'same birth native still alive'
 with (p/'stdout.txt').open() as f:rs=[json.loads(l[6:]) for l in f if l.startswith('M_DAG ')]
 assert len(rs)==100 and len({r['id'] for r in rs})==100
 sources_by_shard[cell['shard']].append(([r['id'] for r in rs],(p/'source.lean').read_text()))
 for row in rs:
  assert cell['cell'] not in byid[row['id']];byid[row['id']][cell['cell']]=row
 last=None;peak=0
 with (p/'memory.jsonl').open() as f:
  for l in f:
   e=json.loads(l);peak=max(peak,e['owned_rss_bytes'])
   if last is not None:maxgap=max(maxgap,e['elapsed_s']-last)
   last=e['elapsed_s']
 assert peak==receipt['sampled_peak_owned_rss_bytes'];tree_peak=max(tree_peak,peak)
 if cell['cell']=='linked-on':
  es=parse_events(p/'tactics.jsonl');assert set(es)=={r['id'] for r in rs}
  assert not (set(source_metrics)&set(es));source_metrics.update(es)
for values in sources_by_shard.values():assert all(x==values[0] for x in values)
ids={r['id'] for r in json.loads((m/'retained-analysis/stratified200.json').read_text())['selected']}
assert set(byid)==ids and len(ids)==200 and set(source_metrics)==ids
counts=collections.Counter();hb_diffs=[];classification=collections.Counter()
for id,cells in byid.items():
 assert set(cells)=={'stock','linked-off','linked-on'}
 a=cells['stock']
 for name in ['linked-off','linked-on']:
  b=cells[name]
  for field in ['hasErrors','errors','infos','allocatedHeartbeatDelta']:
   if a[field]!=b[field]:
    counts[name+'/'+field]+=1
    if field=='allocatedHeartbeatDelta':hb_diffs.append({'id':id,'comparator':name,'stock':a[field],'observed':b[field],'delta':b[field]-a[field]})
 a=cells['linked-on'];text='\n'.join(a['errors']).lower()
 classification['no_lean_errors' if not a['hasErrors'] else 'diagnostic_budget_interruption' if any(v in text for v in ['maximum number of heartbeats','deterministic timeout','maximum recursion depth']) else 'ordinary_lean_error']+=1
assert counts=={'linked-off/allocatedHeartbeatDelta':63,'linked-on/allocatedHeartbeatDelta':62}
totals={name:{'wall_s':math.fsum(c[name]['wallNanoseconds']/1e9 for c in byid.values()),'cpu_s':math.fsum(c[name]['cpuNanoseconds']/1e9 for c in byid.values())} for name in ['stock','linked-off','linked-on']}
body=totals['linked-on']['cpu_s'];leaf=math.fsum(x['largest_leaf_cpu_ns']/1e9 for x in source_metrics.values())
published=json.loads((m/'native-cohort-analysis/summary.json').read_text())
assert math.isclose(leaf,published['sum_per_source_largest_atomic_leaf_cpu_s'],rel_tol=1e-12)
assert math.isclose(body,published['instrumented_body_cpu_s'],rel_tol=1e-12)
for k,v in exclusive.items():assert math.isclose(v/1e9,published['exclusive_cpu_by_kind_s'][k],rel_tol=1e-10,abs_tol=1e-8),(k,v)
assert dict(classification)==published['classification'], (classification,published['classification'])
data={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_invocations':0,'matrix_finished_utc':terminal['finished_utc'],
 'complete_cells':6,'sources':200,'native_returns':600,'differences':dict(counts),'raw_hb_differences':hb_diffs,'classification':dict(classification),
 'body_totals':totals,'whole_process_wall_s_by_cell':{k:math.fsum(c['wall_s'] for c in terminal['cells'] if c['cell']==k) for k in totals},
 'whole_process_receipts':receipts,'sampled_peak_owned_tree_rss_bytes':tree_peak,'max_sample_gap_s':maxgap,
 'C_event_counts':dict(event_count),'complete_C_sources':len(source_metrics),'largest_leaf_cpu_sum_s':leaf,
 'fixed_work_atomic_leaf_ceiling':body/leaf,'eqRefl_exclusive_CPU_s':exclusive['Lean.Parser.Tactic.eqRefl']/1e9,
 'eqRefl_share_of_instrumented_body_CPU':exclusive['Lean.Parser.Tactic.eqRefl']/1e9/body,
 'longest_leaf':max(({'id':id,'largest_leaf_CPU_s':v['largest_leaf_cpu_ns']/1e9,'body_CPU_s':byid[id]['linked-on']['cpuNanoseconds']/1e9} for id,v in source_metrics.items()),key=lambda x:x['largest_leaf_CPU_s']),
 'root_elapsed_s':time.monotonic()-t0,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({k:v for k,v in data.items() if k not in ['raw_hb_differences','whole_process_receipts']},indent=2))
