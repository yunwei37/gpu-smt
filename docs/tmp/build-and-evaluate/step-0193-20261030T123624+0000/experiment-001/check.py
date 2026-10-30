from pathlib import Path
import sys,types,json,collections,subprocess,os,time,resource,csv
os.sched_setaffinity(0,{0,1});t0=time.monotonic()
r=Path('/workspaces/repository');s=Path(__file__).resolve().parent
# Pinned published decoders execute analysis definitions only, never collector mains.
for name in ['analyze_dependency','analyze_c_timing']:
 code=subprocess.check_output(['git','show','9b67361:research/mechanisms-2026-10-30/'+name+'.py'],cwd=r,text=True)
 mod=types.ModuleType(name);mod.__file__=str(s/(name+'.py'));sys.modules[name]=mod;exec(compile(code,mod.__file__,'exec'),mod.__dict__)
a=sys.modules['analyze_c_timing']
term=json.loads((r/'research/mechanisms-2026-10-30/accepted-original-analysis/terminal.json').read_text())
assert term['state']=='complete' and len(term['cells'])==3 and term['elapsed_s']<=term['whole_group_limit_s']
rows={};receipts={};mempeak=0;events=None;models=None
for c in term['cells']:
 p=Path(c['raw_capture']);rec=json.loads((p/'receipt.json').read_text());receipts[c['cell']]=rec
 assert rec['exit']==0 and rec['retired'] and c['native_retired']
 birth=rec['start_ticks'];proc=Path('/proc')/str(rec['pid'])/'stat'
 if proc.exists():assert proc.read_text().split(') ')[1].split()[19]!=birth,'Original native process still alive'
 rs=a.read_rows(p/'stdout.txt');assert len(rs)==50 and len({x['id']for x in rs})==50
 assert all(not x['hasErrors'] for x in rs)
 rows[c['cell']]={x['id']:x for x in rs}
 for line in (p/'memory.jsonl').open():mempeak=max(mempeak,json.loads(line)['owned_rss_bytes'])
 if c['cell']=='linked-on':
  events=a.read_events(p/'tactics.jsonl');models=a.analyze(p)['rows']
ids=set(rows['stock']);assert all(set(v)==ids for v in rows.values())
diffs=collections.Counter()
for name in ['linked-off','linked-on']:
 for ident in ids:
  x,y=rows['stock'][ident],rows[name][ident]
  for k in ['hasErrors','errors','infos','allocatedHeartbeatDelta']:
   if x[k]!=y[k]:diffs[name+'/'+k]+=1
assert dict(diffs)=={'linked-off/allocatedHeartbeatDelta':29,'linked-on/allocatedHeartbeatDelta':30}
old=json.loads((r/'research/mechanisms-2026-10-30/native-cohort-analysis/local-model-per-source.json').read_text())
oldsel=[x for x in old if x['id']in ids];assert len(oldsel)==50
oldclasses=dict(collections.Counter(x['classification']for x in oldsel))
assert oldclasses=={'no_lean_errors':31,'diagnostic_budget_interruption':19}
assert len(models)==50 and all(x['complete_C_tree']for x in models)
cpu=sum(x['body_cpu_s']for x in models)
finite={}
for cores in [1,2,4,8]:
 saving=sum(x['finite_core_island_models'][str(cores)]['saved_cpu_s']for x in models)
 finite[str(cores)]={'modeled_latency_reduction_cpu_equivalent_s':saving,'modeled_body_s':cpu-saving,'ratio':cpu/(cpu-saving)}
# Check raw call/InfoTree-derived reanalysis against the published aggregate.
pub=json.loads((r/'research/mechanisms-2026-10-30/accepted-original-analysis/summary.json').read_text())
assert abs(cpu-pub['instrumented_body_cpu_s'])<1e-8
for k,v in finite.items():assert abs(v['ratio']-pub['finite_core_disjoint_allGoals_model'][k]['ratio'])<1e-10
qualified=sum(x['eligible_allGoals_nodes']for x in models);assert qualified==18
w=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-olean-types-v3')
wrows=[];modules=[];done=[]
for line in (w/'native.log').open():
 if line.startswith('AUDIT '):wrows.append(json.loads(line[6:]))
 elif line.startswith('MODULE '):modules.append(line[7:].strip())
 elif line.startswith('DONE '):done.append(line.strip())
assert len(modules)==len(set(modules))==135 and done==['DONE 135 135']
assert json.loads((w/'terminal.json').read_text())['returncode']==0
aux=[x for x in wrows if x['auxiliary_name']];dec=[x for x in aux if x['decide_shaped_auxiliary']]
groups=collections.defaultdict(set)
for x in aux:groups[x['type_group']].add(x['module'])
wstats={'objects':len(modules),'theorems':len(wrows),'auxiliaries':len(aux),'native_Expr_keys':len({x['expr_group']for x in aux}),'level_private_groups':len(groups),'cross_module_groups':sum(len(v)>1 for v in groups.values()),'decide_auxiliaries':len(dec),'decide_Expr_keys':len({x['expr_group']for x in dec}),'axiom_fields_all_unknown':all(x['axioms']is None for x in wrows)}
assert wstats=={'objects':135,'theorems':1799,'auxiliaries':743,'native_Expr_keys':601,'level_private_groups':604,'cross_module_groups':45,'decide_auxiliaries':45,'decide_Expr_keys':45,'axiom_fields_all_unknown':True}
result={'M_source':'9b67361','W_source':'4780b43','native_calls_started_by_root':0,'M_native_returns':150,'M_processes_retired':True,'M_flag_diagnostic_InfoTree_differences':0,'M_raw_HB_differences':dict(diffs),'M_old_same50_classes':oldclasses,'M_new_same50_classes':{'no_lean_errors':50},'M_body_cpu_by_cell_s':{k:sum(x['cpuNanoseconds']/1e9 for x in v.values())for k,v in rows.items()},'M_native_wall_by_cell_s':{k:v['wall_s']for k,v in receipts.items()},'M_group_wall_s':term['elapsed_s'],'M_sampled_owned_peak_bytes':mempeak,'M_qualified_allGoals_nodes':qualified,'M_qualified_allGoals_sources':sum(x['local_allGoals_eligible']for x in models),'M_finite_core_models':finite,'M_unlimited_model_ratio':cpu/(cpu-sum(x['local_allGoals_saved_cpu_s']for x in models)),'M_have_only_model_ratio':cpu/(cpu-sum(x['have_continuation_model_saved_cpu_s']for x in models)),'W_native_metadata':wstats,'limits':['Model is latency in serial CPU equivalents, not work removal or observed parallel execution.','No snapshot, merge, hidden state, diagnostics, heartbeat reconciliation or memory-admission costs measured.','Selected passes do not represent full7808 failures or service throughput.','Native type-group IDs are producer Expr equality, not a full replay key or expensive-failure cache eligibility.','Successfully serialized theorem types omit failures and absent PlanarPacking/Ramsey clusters.','Full imported axiom closure remains unknown.']}
result.update(root_elapsed_s=time.monotonic()-t0,root_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(s/'reanalysis.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
