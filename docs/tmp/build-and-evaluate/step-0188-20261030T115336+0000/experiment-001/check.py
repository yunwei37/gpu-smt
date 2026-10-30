from pathlib import Path
import os,sys,json,csv,collections,math,time,resource,datetime
os.sched_setaffinity(0,{0,1});t0=time.monotonic()
root=Path('/workspaces/repository');raw=Path('/workspaces/.agent-state/gpu-smt-captures/workloads')
selected=[json.loads(l) for l in (raw/'candidate-native-inputs/april.jsonl').open()]
assert len(selected)==39 and len({x['case_id'] for x in selected})==39
sel={x['case_id']:x for x in selected};strata=collections.defaultdict(list)
for x in selected:strata[tuple(x['stratum'])].append(x)
for key,rs in strata.items():
 N={r['stratum_population'] for r in rs};assert len(N)==1
 assert all(math.isclose(r['inclusion_probability'],len(rs)/next(iter(N)),rel_tol=1e-12) for r in rs)
assert sum(rs[0]['stratum_population'] for rs in strata.values())==1835
records=[];receipts=[]
for name in ['candidate-april-small-v3','candidate-april-remaining-v3']:
 p=raw/name;rows=[json.loads(l) for l in (p/'results.jsonl').open()]
 term=json.loads((p/'terminal.json').read_text());outer=json.loads((p/'capture-terminal.json').read_text())
 assert term['rows']==term['planned_rows']==len(rows) and not term['stopped_between_candidates_after_1500s'] and outer['exit_code']==0
 launch=json.loads((p/'launch.json').read_text())
 stat=Path('/proc')/str(launch['pid'])/'stat'
 if stat.exists():assert stat.read_text().split(') ',1)[1].split()[19]!=launch['birth_ticks']
 assert launch['self_wall_s']==30 and launch['heartbeats']==50000
 mem=list(csv.DictReader((p/'memory.csv').open()))
 # The trace uses original named fields; full tree includes retained old EPFL.
 assert mem
 receipts.append({'point':str(p),'terminal':term,'outer':outer,'launch':launch,'memory_fields':list(mem[0])})
 records+=rows
assert len(records)==78 and len({(x['case_id'],x['mode']) for x in records})==78
observed=collections.defaultdict(list);budget_types=collections.Counter();cap_edits=0
for x in records:
 a=sel[x['case_id']];assert x['mode'] in ['reference','candidate']
 assert x['native_version']=='4.22.0-rc4' and x['heartbeats']==50000 and x['native_memory_option_MiB']==6144 and x['threads']==1
 assert x['dataset_revision']==a['dataset_revision'] and x['stratum']==a['stratum']
 assert x['inclusion_probability']==a['inclusion_probability']
 assert x['returncode']==(0 if x['status']=='compile_ok' else 1)
 assert x['status'] in ['compile_ok','lean_error','budget_exceeded']
 cap_edits+=bool(x['source_budget_values_capped']);observed[(x['mode'],x['status'])].append(x)
 log=Path(x['log']).read_text().lower()
 if x['mode']=='candidate' and x['status']=='budget_exceeded':
  kinds=[]
  if 'maximum recursion depth' in log:kinds.append('recursion')
  if 'maximum number of heartbeats' in log:kinds.append('heartbeat')
  assert kinds;(budget_types[tuple(sorted(kinds))])+=1
costs=[];weighted=[]
for (mode,status),rs in sorted(observed.items()):
 total=math.fsum(x['wall_s'] for x in records if x['mode']==mode)
 cost=math.fsum(x['wall_s'] for x in rs)
 costs.append({'mode':mode,'status':status,'n':len(rs),'wall_s':cost,'share':cost/total})
 wcost=math.fsum(x['wall_s']/x['inclusion_probability'] for x in rs)
 wtotal=math.fsum(x['wall_s']/x['inclusion_probability'] for x in records if x['mode']==mode)
 weighted.append({'mode':mode,'status':status,'weighted_count':math.fsum(1/x['inclusion_probability'] for x in rs),
 'weighted_cost_s':wcost,'ratio_of_estimated_cost_totals':wcost/wtotal})
pub=root/'workloads/candidates/native-versioned/april39'
for fn,rows,costkey,sharekey in [('outcome-costs.csv',costs,'wall_sum_s','observed_wall_share'),('weighted-released-test.csv',weighted,'weighted_released_wall_s','weighted_observed_wall_share')]:
 original=list(csv.DictReader((pub/fn).open()));assert len(original)==len(rows)
 for x in original:
  z=next(y for y in rows if y['mode']==x['mode'] and y['status']==x['status'])
  k='wall_s' if fn=='outcome-costs.csv' else 'weighted_cost_s'
  k2='share' if fn=='outcome-costs.csv' else 'ratio_of_estimated_cost_totals'
  assert math.isclose(float(x[costkey]),z[k],rel_tol=1e-12)
  assert math.isclose(float(x[sharekey]),z[k2],rel_tol=1e-12)
assert budget_types=={('recursion',):12,('heartbeat',):3,('heartbeat','recursion'):1},budget_types
for id in sel:assert {x['mode'] for x in records if x['case_id']==id}=={'reference','candidate'}
data={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_invocations':0,'pairs':39,'native_returns':78,
 'references_distinct_source_strings':len({x['reference_source'] for x in selected}),'mutations_distinct_source_strings':len({x['source'] for x in selected}),
 'sample_recorded_budget_text':sum(x['recorded_budget_text'] for x in selected),'sampling_cells':len(strata),'released_mutation_test_rows':1835,
 'outcome_costs':costs,'weighted_cost_ratios':weighted,
 'mutation_budget_types':[{'diagnostics':list(k),'n':v} for k,v in sorted(budget_types.items())],
 'replay_rows_with_explicit_heartbeat_cap_edits':cap_edits,'whole_batches':receipts,
 'root_elapsed_s':time.monotonic()-t0,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({k:v for k,v in data.items() if k!='whole_batches'},indent=2))
