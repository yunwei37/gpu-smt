from pathlib import Path
import os,sys,json,collections,math,resource,time,datetime,csv
os.sched_setaffinity(0,{0,1});t0=time.monotonic()
root=Path('/workspaces/repository');m=root/'research/mechanisms-2026-10-30'
raw=Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/captures')
cells={}
for name in ['stock','linked-off','linked-on']:
 p=raw/('native-cohort-s0-'+name)
 with (p/'stdout.txt').open() as f:rows=[json.loads(l[6:]) for l in f if l.startswith('M_DAG ')]
 receipt=json.loads((p/'receipt.json').read_text())
 assert len(rows)==100 and len({r['id'] for r in rows})==100
 assert receipt['exit']==0 and receipt['retired']
 cells[name]={'rows':rows,'receipt':receipt,'source':(p/'source.lean').read_text()}
assert all([x['id'] for x in c['rows']]==[x['id'] for x in cells['stock']['rows']] for c in cells.values())
assert len({c['source'] for c in cells.values()})==1
comparisons={}
for name in ['linked-off','linked-on']:
 counts=collections.Counter();diffs=[]
 for a,b in zip(cells['stock']['rows'],cells[name]['rows']):
  fs=[f for f in ['hasErrors','errors','infos','allocatedHeartbeatDelta'] if a[f]!=b[f]];counts.update(fs)
  if 'allocatedHeartbeatDelta' in fs:
   diffs.append({'id':a['id'],'stock':a['allocatedHeartbeatDelta'],'comparator':b['allocatedHeartbeatDelta'],
    'delta':b['allocatedHeartbeatDelta']-a['allocatedHeartbeatDelta']})
 comparisons[name]={'difference_counts':dict(counts),'raw_heartbeat_differences':diffs}
 assert counts=={'allocatedHeartbeatDelta':33}
wraw=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/candidate-native-v1-snapshot-1109')
with (wraw/'results.jsonl').open() as f:allw=[json.loads(l) for l in f]
epfl=[r for r in allw if r['dataset']=='EPFL-evaluation'];assert len(epfl)==136
assert len({r['case_id'] for r in epfl})==136
costs={}
for key in ['compile_ok','lean_error','budget_exceeded']:
 rs=[r for r in epfl if r['status']==key];assert rs
 costs[key]={'n':len(rs),'wall_s':math.fsum(r['wall_s'] for r in rs)}
published=list(csv.DictReader((root/'workloads/candidates/native-versioned/epfl-completed136/cost-distribution.csv').open()))
for r in published:
 if r['observed_status'] in costs:
  x=costs[r['observed_status']];assert x['n']==int(r['n']) and math.isclose(x['wall_s'],float(r['wall_sum_s']),rel_tol=1e-12)
total=math.fsum(r['wall_s'] for r in epfl)
for x in costs.values():x['returned_prefix_wall_share']=x['wall_s']/total
wrong=[r['case_id'] for r in epfl if r['publisher_status']=='wrong_declaration' and r['status']=='compile_ok']
d={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_verifier_invocations':0,
 'M_shard0_complete_sources':100,'M_shard0_native_returns':300,'M_comparisons':comparisons,
 'M_process_receipts':{k:c['receipt'] for k,c in cells.items()},
 'M_body_totals':{k:{'wall_s':math.fsum(x['wallNanoseconds']/1e9 for x in c['rows']),
 'cpu_s':math.fsum(x['cpuNanoseconds']/1e9 for x in c['rows'])} for k,c in cells.items()},
 'M_full200_complete':False,'W_snapshot_rows':len(allw),'W_EPFL_returned':len(epfl),
 'W_EPFL_selected':144,'W_EPFL_unreturned':8,'W_EPFL_returned_prefix_wall_s':total,'W_EPFL_status_costs':costs,
 'W_wrong_declaration_compiler_ok_IDs':wrong,
 'limits':['Completed diagnostic shard0 only; full200/600 native comparisons pending.',
 'Heartbeat differences are raw counters, not diagnostic/pass-set mismatches or demonstrated budget flips.',
 'EPFL completed-prefix shares exclude all eight unreturned; no population weighting or time-tail conclusion.',
 'Compiler pass is not the publisher expected-declaration/forbidden-proof judge; seven such differences are not new false acceptances.',
 'No original or active capture modified.'],
 'root_elapsed_s':time.monotonic()-t0,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps({k:v for k,v in d.items() if k not in ['M_process_receipts','M_comparisons']},indent=2))
print('HB_DELTA_EXTREMA',{k:(min(x['delta'] for x in v['raw_heartbeat_differences']),max(x['delta'] for x in v['raw_heartbeat_differences'])) for k,v in comparisons.items()})
