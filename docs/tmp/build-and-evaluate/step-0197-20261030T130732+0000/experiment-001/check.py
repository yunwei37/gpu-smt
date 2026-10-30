from pathlib import Path
import json,csv,collections,time,resource,os
os.sched_setaffinity(0,{0,1});start=time.monotonic()
r=Path('/workspaces/repository');e=Path(__file__).parent;b=Path('/workspaces/.agent-state/gpu-smt-captures/workloads');p=b/'openai4341-native-batch3'
rows=[json.loads(x)for x in (p/'results.jsonl').open()];assert len(rows)==len({x['module']for x in rows})==171
counts=dict(collections.Counter(x['status']for x in rows));assert counts=={'compile_ok':108,'wall_budget_exceeded':1,'dependency_not_compiled':62}
calls=[x for x in rows if 'returncode'in x];assert len(calls)==109
assert all(x['returncode']==0 and not x['sorry_warning']for x in rows if x['status']=='compile_ok')
assert all('returncode'not in x and 'wall_s'not in x for x in rows if x['status']=='dependency_not_compiled')
for x in calls:
 proc=Path('/proc')/str(x['pid'])/'stat'
 if proc.exists():assert proc.read_text().split(') ')[1].split()[19]!=x['birth_ticks']
 assert x['heartbeat_budget']==100000 and x['lean_memory_option_MiB']==8192 and x['threads']==1
 assert x['replaced_source_budget_settings']==0
grid=next(x for x in rows if x['status']=='wall_budget_exceeded');assert grid['module']=='OAI.Analysis.PlanarPacking.Grid' and grid['returncode']==-14
term=json.loads((p/'terminal.json').read_text());cap=json.loads((p/'capture-terminal.json').read_text());assert cap['exit_code']==0 and term['rows']==171
memory=list(csv.DictReader((p/'memory.csv').open()));print('MEMORY_COLUMNS',list(memory[0]))
# Capture receipt records the independent1s combined owned-tree peak.
peak=cap['sampled_tree_peak_bytes'];assert peak==13104529408
assert max(int(x['tree_rss_bytes'])for x in memory)==peak
assert max(int(x['native_lean_processes'])for x in memory)==2
csvrows=list(csv.DictReader((r/'workloads/openai-math/native-batch3-4341/modules.csv').open()));assert {x['module']for x in csvrows}=={x['module']for x in rows}
for x,y in zip(rows,csvrows):assert x['module']==y['module'] and x['status']==y['status']
targets=list(csv.DictReader((r/'workloads/openai-math/native-batch3-4341/targets.csv').open()))
states={x['module']:x['status']for x in rows};assert len(targets)==10
assert all(x['native_status']==states[x['module']]for x in targets)
original=[x for x in targets if x['role']=='probability_sample'];extra=[x for x in targets if x['role']!='probability_sample']
assert len(original)==9 and len(extra)==1 and sum(x['native_status']=='compile_ok'for x in original)==7
prior=[json.loads(l)for tag in ['openai4341-native','openai4341-native-expanded','openai4341-native-resume100k']for l in(b/tag/'results.jsonl').read_text().splitlines()]
oldobjects={x['module']for x in prior if x['status']=='compile_ok'}
newobjects={x['module']for x in rows if x['status']=='compile_ok'}
assert len(oldobjects)==135 and not(oldobjects&newobjects)
allobjects=oldobjects|newobjects;assert len(allobjects)==243
objects=Path('/workspaces/.agent-state/gpu-smt-workloads/openai4341-oleans')
assert all((objects/Path(*m.split('.')).with_suffix('.olean')).is_file()for m in allobjects)
frame=list(csv.DictReader((r/'workloads/openai-math/build-planning-4eaee875/sample-targets.csv').open()));assert len(frame)==53
frameavailable=[x['module']for x in frame if x['module']in allobjects]
j1=[json.loads(l)for l in (b/'candidate-epfl-pending-v3/results.jsonl').read_text().splitlines()]
j2=[json.loads(l)for l in (b/'epfl-search-threads2/results.jsonl').read_text().splitlines()]
assert len(j2)==2;paired=[]
for x in j2:
 y=next(t for t in j1 if t['case_id']==x['case_id'])
 assert y['status']=='wall_budget_exceeded'and x['status']=='budget_exceeded'and y['returncode']==-14 and x['returncode']==1
 assert y['heartbeats']==x['heartbeats']==10000 and y['native_memory_option_MiB']==x['native_memory_option_MiB']==6144
 assert (b/'epfl-search-threads2'/str(x['index'])).with_suffix('.lean').read_bytes()==(b/'candidate-epfl-pending-v3'/str(y['index'])).with_suffix('.lean').read_bytes()
 log=Path(x['log']).read_text();assert 'heartbeats'in log
 paired.append({'id':x['case_id'],'j1_wall_s':y['wall_s'],'j1_CPU_s':y['user_cpu_s']+y['system_cpu_s'],'j2_wall_s':x['wall_s'],'j2_CPU_s':x['user_cpu_s']+x['system_cpu_s'],'j2_prior_unsolved_goals':'unsolved goals'in log})
surface=list(csv.DictReader((r/'workloads/candidates/native-versioned/epfl-completed136/first-error-surface.csv').open()));assert sum(int(x['requests'])for x in surface)==71
result={'W_source':'e6fdc90','new_native_calls_by_root':0,'raw_capture':str(p),'records':171,'actual_native_calls':109,'statuses':counts,'native_wall_sum_s':sum(x['wall_s']for x in calls),'user_cpu_sum_s':sum(x['user_cpu_s']for x in calls),'system_cpu_sum_s':sum(x['system_cpu_s']for x in calls),'capture_elapsed_s':cap['elapsed_s'],'combined_old_new_sampled_RSS_peak_bytes':peak,'target_endpoints':{'original_selected':9,'original_compile_ok':7,'original_blocked':2,'extra_unweighted_probe':1,'extra_native_invoked':False},'grid':grid,'grid_CPU_to_wall':(grid['user_cpu_s']+grid['system_cpu_s'])/grid['wall_s'],'available_compiled_object_union':243,'same_initial53frame_endpoint_objects_available':len(frameavailable),'available_frame_endpoints':frameavailable,'all_available_objects_exist':True,'worker_contrast':paired,'first_error_surface_whole_request_sum_s':sum(float(x['whole_request_wall_s'])for x in surface),'limits':['Separate100kHB,j1,M8192,120sself-wall module point; not original-unbounded timings or a full-library sample.','62dependent modules have no invocation or measured zero-time outcome.','Historical old sleeping Lean RSS is charged; requestedj1 is not measured one OSthread.','Grid CPU>wall does not establish a specific phase,cause or hardware bottleneck.','Worker contrast jointly changesCLI-jandLEAN_NUM_THREADS; not isolatedcausalflagproof or a speedup/pass.','First error message categories group whole-request clocks,not tactic/phase attribution.','Compiled object union spans points; no homogeneous summed wallclock,axiom audit or fullcache eligibility.','Extra HighMoments source-text repetitions/namespaces do not establish native typed equality.']}
result.update(root_elapsed_s=time.monotonic()-start,root_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
