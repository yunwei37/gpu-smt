from pathlib import Path
import collections,csv,io,json,math,os,resource,subprocess,time
os.sched_setaffinity(0,{0,1});resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3));start=time.monotonic()
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-paper-native-pilot-step.txt').read_text().strip());e=s/'experiment-001'
frozen=lambda rev,path:subprocess.check_output(['git','show',rev+':'+path],cwd=r).decode()
W='127ddc4';M='3837eca';wp='workloads/openai-math/profile-overhead-4341/'
published=list(csv.DictReader(io.StringIO(frozen(W,wp+'module-modes.csv'))))
capture=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-profile-ab')
rows=[json.loads(x) for x in (capture/'results.jsonl').read_text().splitlines()]
assert len(rows)==14 and len({(x['module'],x['mode']) for x in rows})==14
assert {x['mode'] for x in rows}=={'baseline','profile_only'}
groups=collections.defaultdict(dict)
for row in rows:
 assert row['returncode']==0 and not row['sorry_warning']
 assert row['heartbeats']==200000 and row['native_memory_option_MiB']==8192 and row['threads']==1 and row['source_budget_edits']==0
 groups[row['module']][row['mode']]=row
 pub=next(x for x in published if x['module']==row['module'] and x['mode']==row['mode'])
 for key in ['wall_s','user_cpu_s','system_cpu_s','peak_rss_kib']:
  assert math.isclose(float(pub[key]),row[key],rel_tol=1e-12,abs_tol=1e-9)
 assert Path(row['log']).exists()
assert len(groups)==7 and all(set(v)=={'baseline','profile_only'} for v in groups.values())
assert all(rows[i]['mode']=='baseline' and rows[i+1]['mode']=='profile_only' and rows[i]['module']==rows[i+1]['module'] for i in range(0,14,2))
mode={}
for name in ['baseline','profile_only']:
 selected=[x for x in rows if x['mode']==name]
 mode[name]={'process_wall_sum_s':math.fsum(x['wall_s'] for x in selected),'CPU_sum_s':math.fsum(x['user_cpu_s']+x['system_cpu_s'] for x in selected),'wait4_peak_rss_range_bytes':[min(x['peak_rss_kib'] for x in selected)*1024,max(x['peak_rss_kib'] for x in selected)*1024]}
terminal=json.loads((capture/'capture-terminal.json').read_text());assert terminal['exit_code']==0 and terminal['max_native_lean_processes']==1
with (capture/'memory.csv').open() as f: memory=list(csv.DictReader(f))
rsskeys=[k for k in memory[0] if 'rss' in k.lower()];assert len(rsskeys)==1,rsskeys
assert max(int(float(x[rsskeys[0]])) for x in memory)==terminal['sampled_tree_peak_bytes']
mp='research/mechanisms-2026-10-30/';published_m=json.loads(frozen(M,mp+'c-fresh-differential.json'))
root=Path(published_m['raw_root']);native={};receipts={};events={}
for cell in ['stock','linked-off','linked-on']:
 p=root/('c-cold-v5-'+cell);receipts[cell]=json.loads((p/'receipt.json').read_text());assert receipts[cell]['exit']==0 and receipts[cell]['retired']
 native[cell]={}
 for line in (p/'stdout.txt').read_text().splitlines():
  at=line.find('{')
  if at<0:continue
  try:x=json.loads(line[at:])
  except json.JSONDecodeError:continue
  if 'allocatedHeartbeatDelta' in x:
   assert x['id'] not in native[cell];native[cell][x['id']]=x
 assert len(native[cell])==4
 events[cell]=[json.loads(x) for x in (p/'tactics.jsonl').read_text().splitlines()]
assert set(native['stock'])=={'independent','coupled','ordinary-error','budget'}
matched=[]
for cell in ['linked-off','linked-on']:
 for key,a in native['stock'].items():
  b=native[cell][key]
  for field in ['hasErrors','errors','infos','allocatedHeartbeatDelta']:assert a[field]==b[field],(cell,key,field)
  matched.append({'comparator':cell,'control':key,'equal_flags_diagnostics_InfoTree_raw_HB':True,'raw_HB_delta':a['allocatedHeartbeatDelta']})
timed=events['linked-on'];counts=dict(collections.Counter(x['event'] for x in timed));assert counts==published_m['event_counts']=={'source':8,'enter':1050,'exit':1050}
enters={x['id']:x for x in timed if x['event']=='enter'};exits={x['id']:x for x in timed if x['event']=='exit'}
assert len(enters)==len(exits)==1050 and set(enters)==set(exits)
stacks=collections.defaultdict(list);tags=collections.Counter()
for x in timed:
 if x['event']=='enter':
  thread=x['thread'];parent=stacks[thread][-1] if stacks[thread] else 0
  assert x['parent']==parent;stacks[thread].append(x['id'])
 elif x['event']=='exit':
  a=enters[x['id']];assert stacks[a['thread']].pop()==x['id']
  assert x['wall_ns']>=a['wall_ns'] and x['cpu_ns']>=a['cpu_ns'];tags[str(x['return_tag'])]+=1
assert all(not v for v in stacks.values()) and dict(tags)==published_m['return_tags']
sources=[(root/('c-cold-v5-'+cell)/'source.lean').read_bytes() for cell in native];assert sources[0]==sources[1]==sources[2]
result={'W_commit':W,'M_commit':M,'native_runs_by_root':0,'W_native_modules':7,'W_native_executions':14,'W_modes':mode,'W_wall_difference_s':mode['profile_only']['process_wall_sum_s']-mode['baseline']['process_wall_sum_s'],'W_wall_relative_difference':mode['profile_only']['process_wall_sum_s']/mode['baseline']['process_wall_sum_s']-1,'W_aggregate_capture':terminal,'W_memory_samples':len(memory),'M_fresh_processes':3,'M_tiny_controls':4,'M_stock_comparisons':matched,'M_callback_counts':counts,'M_balanced_per_thread_nesting':True,'M_return_tags_are_not_candidate_verdicts':dict(tags),'M_process_receipts':receipts,'limits':['W seven-module fixed-order pilot is not the full probability sample or a causal/population overhead bound.','W native compiler --profile differs from the older trace.profiler diagnostic in version,option,cohort and budget.','Compiler process wait4 peaks and one-second aggregate samples have different scopes.','No transitive axiom-closure or full service acceptance is established by compiler exit and lack of sorry warnings.','M four controls do not prove generic allocation transparency or full200/production parity.','No new-budget model, global speedup, Amdahl bound, COW gain or scientific-mainline change.'],'elapsed_s':time.monotonic()-start,'root_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'root_affinity':sorted(os.sched_getaffinity(0))}
(e/'native-pilot-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
